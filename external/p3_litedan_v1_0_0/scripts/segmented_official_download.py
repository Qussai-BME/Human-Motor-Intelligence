#!/usr/bin/env python3
"""Safely download one official archive using multiple HTTP byte ranges.

This is a transport-only optimization. Every range response is checked for HTTP 206
and exact Content-Range/byte count; segments are concatenated in deterministic order,
the assembled file must match the official Content-Length and be a valid ZIP before it
replaces the normal staged archive. No raw file or cache is built from a partial.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

USER_AGENT = "LiteDAN-Paper3-segmented-official-download/1.1"
CONTENT_RANGE = re.compile(r"bytes\s+(\d+)-(\d+)/(\d+)", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ranges_after(offset: int, total: int, connections: int) -> list[tuple[int, int]]:
    remaining = total - offset
    if remaining <= 0:
        return []
    chunk = (remaining + connections - 1) // connections
    ranges = []
    start = offset
    while start < total:
        end = min(total - 1, start + chunk - 1)
        ranges.append((start, end))
        start = end + 1
    return ranges


def fetch_range(url: str, start: int, end: int, total: int, path: Path, attempts: int) -> dict:
    headers = {
        "User-Agent": USER_AGENT,
        "Range": f"bytes={start}-{end}",
        "Accept-Encoding": "identity",
    }
    expected = end - start + 1
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.unlink(missing_ok=True)
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(30, 180)) as response:
                if response.status_code != 206:
                    raise RuntimeError(f"range {start}-{end}: expected HTTP 206, got {response.status_code}")
                match = CONTENT_RANGE.fullmatch(response.headers.get("Content-Range", "").strip())
                if not match:
                    raise RuntimeError(f"range {start}-{end}: malformed Content-Range {response.headers.get('Content-Range')!r}")
                got_start, got_end, got_total = (int(value) for value in match.groups())
                if (got_start, got_end, got_total) != (start, end, total):
                    raise RuntimeError(f"range {start}-{end}: received Content-Range {got_start}-{got_end}/{got_total}")
                written = 0
                with temporary.open("wb") as handle:
                    for block in response.iter_content(chunk_size=1024 * 1024):
                        if block:
                            handle.write(block)
                            written += len(block)
            if written != expected or temporary.stat().st_size != expected:
                raise RuntimeError(f"range {start}-{end}: wrote {written}, expected {expected}")
            os.replace(temporary, path)
            return {"start": start, "end": end, "bytes": written, "path": str(path), "attempt": attempt}
        except (OSError, RuntimeError, requests.RequestException) as exc:
            last_error = exc
            temporary.unlink(missing_ok=True)
    raise RuntimeError(f"range {start}-{end}: failed after {attempts} attempts: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-size", type=int, required=True)
    parser.add_argument("--connections", type=int, default=4)
    parser.add_argument("--range-attempts", type=int, default=3)
    args = parser.parse_args()
    if args.connections < 1 or args.range_attempts < 1:
        raise ValueError("connections and range-attempts must be positive")
    if args.expected_size <= 0:
        raise ValueError("expected-size must be positive")

    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    partial = output.with_suffix(output.suffix + ".part")
    if output.exists() and output.stat().st_size == args.expected_size and zipfile.is_zipfile(output):
        print(f"reused complete validated archive: {output} sha256={sha256_file(output)}")
        return 0
    prefix = partial.stat().st_size if partial.exists() else 0
    if prefix > args.expected_size:
        partial.unlink()
        prefix = 0
    segment_root = output.parent / f".{output.name}.segments"
    shutil.rmtree(segment_root, ignore_errors=True)
    segment_root.mkdir()
    try:
        tasks = ranges_after(prefix, args.expected_size, args.connections)
        results = []
        with ThreadPoolExecutor(max_workers=len(tasks) or 1) as executor:
            future_map = {
                executor.submit(fetch_range, args.url, start, end, args.expected_size, segment_root / f"{start:012d}-{end:012d}.part", args.range_attempts): (start, end)
                for start, end in tasks
            }
            for future in as_completed(future_map):
                results.append(future.result())
        results.sort(key=lambda item: item["start"])
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".zip", delete=False) as handle:
            assembled = Path(handle.name)
            if prefix:
                with partial.open("rb") as source:
                    shutil.copyfileobj(source, handle, length=1024 * 1024)
            for result in results:
                with Path(result["path"]).open("rb") as source:
                    shutil.copyfileobj(source, handle, length=1024 * 1024)
        if assembled.stat().st_size != args.expected_size:
            raise RuntimeError(f"assembled archive size {assembled.stat().st_size}, expected {args.expected_size}")
        if not zipfile.is_zipfile(assembled):
            raise RuntimeError("assembled archive is not a valid ZIP")
        os.replace(assembled, output)
        partial.unlink(missing_ok=True)
        print(f"segmented download complete: bytes={output.stat().st_size} sha256={sha256_file(output)} output={output}")
        return 0
    finally:
        shutil.rmtree(segment_root, ignore_errors=True)
        try:
            assembled.unlink(missing_ok=True)  # type: ignore[name-defined]
        except UnboundLocalError:
            pass


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError, requests.RequestException) as exc:
        print(f"SEGMENTED DOWNLOAD ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
