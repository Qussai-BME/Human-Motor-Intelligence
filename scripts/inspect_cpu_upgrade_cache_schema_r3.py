from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


def inspect_one(path: Path) -> dict[str, object]:
    with np.load(path, allow_pickle=False) as data:
        result: dict[str, object] = {"file": path.name, "keys": sorted(data.files), "arrays": {}}
        for key in sorted(data.files):
            value = data[key]
            item: dict[str, object] = {"shape": list(value.shape), "dtype": str(value.dtype)}
            if value.ndim == 1 and value.size <= 100:
                item["sample"] = value.tolist()
            result["arrays"][key] = item
        return result


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: inspect_cpu_upgrade_cache_schema_r3.py P4_ROOT P5_ROOT", file=sys.stderr)
        return 2
    output: dict[str, object] = {}
    for label, raw in (("p4", sys.argv[1]), ("p5", sys.argv[2])):
        root = Path(raw)
        files = sorted(root.glob("*.npz"))
        output[label] = {
            "root": str(root),
            "count": len(files),
            "first": inspect_one(files[0]) if files else None,
            "last": inspect_one(files[-1]) if files else None,
        }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
