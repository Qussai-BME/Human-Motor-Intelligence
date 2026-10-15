#!/usr/bin/env python3
"""Regenerate release/RELEASE_MANIFEST.json (sorted paths, sizes, SHA-256) for the current tree.

Covers every file in the tree (including `historical/`; caches and VCS metadata excluded) except the manifest itself. Run after any change and before tagging a release.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}
SELF = ROOT / "release" / "RELEASE_MANIFEST.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    old = json.loads(SELF.read_text()) if SELF.exists() else {}
    files = []
    for p in sorted(ROOT.rglob("*"), key=lambda q: q.relative_to(ROOT).as_posix()):
        if not p.is_file() or p == SELF or any(part in EXCLUDE for part in p.parts):
            continue
        files.append({"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)})
    manifest = {k: v for k, v in old.items() if k not in {"files", "file_count"}}
    manifest.update({"release_name": "Human Motor Intelligence — P6 C1, Audit and C2 Scientific Release", "version": "1.2.0", "release_date": "2026-10-11", "scientific_status": "P6 scientifically complete as C1 (registered replay, 0/60), post-hoc audit (C1 endpoint unreachable by design) and C2 registered follow-up (control success follows confidence-gate passage, not accuracy); R03 retained as engineering/preflight baseline.", "manifest_self_excluded": True, "file_count": len(files), "files": files})
    SELF.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {SELF.relative_to(ROOT)} with {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
