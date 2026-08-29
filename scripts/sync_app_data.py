#!/usr/bin/env python3
"""Copy extracted JSON/CSV into the static app data folder."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data"
DST = ROOT / "workspace-app" / "data"


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for path in SRC.iterdir():
        if path.suffix in {".json", ".csv"}:
            shutil.copy2(path, DST / path.name)
    print(f"synced {len(list(DST.iterdir()))} files to {DST}")


if __name__ == "__main__":
    main()
