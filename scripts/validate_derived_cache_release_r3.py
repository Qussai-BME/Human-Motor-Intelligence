from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_derived_cache_release_r3.py CACHE_ROOT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    failures: list[str] = []
    records: list[dict[str, object]] = []
    for forbidden in root.rglob("*"):
        if forbidden.is_file() and forbidden.suffix.lower() in {".bdf", ".edf", ".gdf", ".set", ".fif"}:
            failures.append(f"raw recording present: {forbidden.relative_to(root)}")
    for npz in sorted(root.rglob("*.npz")):
        provenance = npz.with_name(npz.stem + ".provenance.json")
        if not provenance.is_file():
            failures.append(f"missing provenance: {provenance.relative_to(root)}")
            continue
        try:
            import numpy as np
            with np.load(npz, allow_pickle=False) as data:
                keys = sorted(data.files)
                shapes = {key: list(data[key].shape) for key in keys}
                dtypes = {key: str(data[key].dtype) for key in keys}
        except Exception as exc:
            failures.append(f"invalid NPZ {npz.relative_to(root)}: {exc}")
            continue
        try:
            metadata = json.loads(provenance.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid provenance {provenance.relative_to(root)}: {exc}")
            continue
        if not isinstance(metadata, dict):
            failures.append(f"provenance is not an object: {provenance.relative_to(root)}")
        records.append({
            "cache": npz.relative_to(root).as_posix(),
            "provenance": provenance.relative_to(root).as_posix(),
            "cache_sha256": sha256(npz),
            "provenance_sha256": sha256(provenance),
            "bytes": npz.stat().st_size,
            "arrays": keys,
            "shapes": shapes,
            "dtypes": dtypes,
        })
    if not records:
        failures.append("no NPZ caches found")
    report = {
        "status": "pass" if not failures else "fail",
        "root": str(root),
        "npz_count": len(records),
        "provenance_pair_count": len(records),
        "records": records,
        "failures": failures,
        "scope": "P4/P5 derived caches only; P6 R3 decoder-quality cache does not exist because R3 was not executed",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
