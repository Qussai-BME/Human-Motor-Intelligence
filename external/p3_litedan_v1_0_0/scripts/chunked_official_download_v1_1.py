#!/usr/bin/env python3
"""Safely fetch one official NinaPro ZIP through resumable verified small ranges.

This is a recovery transport fallback only. Each completed range is accepted only
when its HTTP 206 Content-Range and byte count exactly match the requested span.
The final archive is assembled in order and is accepted only at the official
advertised length and after ZIP-container validation. No downstream cache process
can consume partial ranges, incomplete assemblies, or a failed archive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

USER_AGENT = "LiteDAN-Paper3-chunked-official-download/1.1"
CONTENT_RANGE = re.compile(r"bytes\s+(\d+)-(\d+)/(\d+)", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def range_path(root: Path, start: int, end: int) -> Path:
    return root / f"{start:012d}-{end:012d}.part"


def complete_ranges(total: int, chunk_bytes: int) -> list[tuple[int, int]]:
    return [(start, min(total - 1, start + chunk_bytes - 1)) for start in range(0, total, chunk_bytes)]


def existing_valid(path: Path, expected: int) -> bool:
    return path.exists() and path.stat().st_size == expected


def fetch_range(url: str, start: int, end: int, total: int, path: Path, attempts: int) -> dict[str, object]:
    expected = end - start + 1
    if existing_valid(path, expected):
        return {"start": start, "end": end, "bytes": expected, "path": str(path), "status": "reused"}
    headers = {
        "User-Agent": USER_AGENT,
        "Range": f"bytes={start}-{end}",
        "Accept-Encoding": "identity",
    }
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.unlink(missing_ok=True)
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(30, 90)) as response:
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
                    for block in response.iter_content(chunk_size=64 * 1024):
                        if block:
                            handle.write(block)
                            written += len(block)
            if written != expected or temporary.stat().st_size != expected:
                raise RuntimeError(f"range {start}-{end}: wrote {written}, expected {expected}")
            os.replace(temporary, path)
            return {"start": start, "end": end, "bytes": written, "path": str(path), "status": f"downloaded_attempt_{attempt}"}
        except (OSError, RuntimeError, requests.RequestException) as exc:
            last_error = exc
            temporary.unlink(missing_ok=True)
            if attempt < attempts:
                time.sleep(min(30, 3 * attempt))
    raise RuntimeError(f"range {start}-{end}: failed after {attempts} attempts: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-size", type=int, required=True)
    parser.add_argument("--chunk-bytes", type=int, default=1024 * 1024)
    parser.add_argument("--connections", type=int, default=2)
    parser.add_argument("--range-attempts", type=int, default=3)
    args = parser.parse_args()
    if args.expected_size <= 0 or args.chunk_bytes <= 0 or args.connections < 1 or args.range_attempts < 1:
        raise ValueError("expected-size, chunk-bytes, connections, and range-attempts must be positive")

    output: Path = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.stat().st_size == args.expected_size and zipfile.is_zipfile(output):
        print(f"reused complete validated archive: {output} sha256={sha256_file(output)}")
        return 0

    root = output.parent / f".{output.name}.chunked_segments"
    root.mkdir(parents=True, exist_ok=True)
    ranges = complete_ranges(args.expected_size, args.chunk_bytes)
    pending = [(start, end) for start, end in ranges if not existing_valid(range_path(root, start, end), end - start + 1)]
    print(json.dumps({"status": "range_recovery_start", "total_ranges": len(ranges), "pending_ranges": len(pending), "chunk_bytes": args.chunk_bytes, "connections": args.connections}), flush=True)
    try:
        completed = len(ranges) - len(pending)
        with ThreadPoolExecutor(max_workers=min(args.connections, max(1, len(pending)))) as executor:
            futures = {
                executor.submit(fetch_range, args.url, start, end, args.expected_size, range_path(root, start, end), args.range_attempts): (start, end)
                for start, end in pending
            }
            for future in as_completed(futures):
                result = future.result()
                completed += 1
                if completed == len(ranges) or completed % 25 == 0:
                    print(json.dumps({"status": "range_progress", "completed_ranges": completed, "total_ranges": len(ranges), "last_range": [result["start"], result["end"]]}), flush=True)

        with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".zip", delete=False) as handle:
            assembled = Path(handle.name)
            for start, end in ranges:
                part = range_path(root, start, end)
                expected = end - start + 1
                if not existing_valid(part, expected):
                    raise RuntimeError(f"missing or invalid completed range {start}-{end}")
                with part.open("rb") as source:
                    shutil.copyfileobj(source, handle, length=1024 * 1024)
        if assembled.stat().st_size != args.expected_size:
            raise RuntimeError(f"assembled archive size {assembled.stat().st_size}, expected {args.expected_size}")
        if not zipfile.is_zipfile(assembled):
            raise RuntimeError("assembled archive is not a valid ZIP")
        os.replace(assembled, output)
        sha256 = sha256_file(output)
        manifest = {
            "url": args.url,
            "expected_size": args.expected_size,
            "chunk_bytes": args.chunk_bytes,
            "connections": args.connections,
            "range_count": len(ranges),
            "sha256": sha256,
            "validation": {"exact_size": True, "zipfile": True, "range_content_range_and_size": True},
        }
        output.with_suffix(output.suffix + ".chunked_transport.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"chunked download complete: bytes={output.stat().st_size} sha256={sha256} output={output}")
        return 0
    finally:
        try:
            assembled.unlink(missing_ok=True)  # type: ignore[name-defined]
        except UnboundLocalError:
            pass


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, requests.RequestException) as exc:
        print(f"CHUNKED DOWNLOAD ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
