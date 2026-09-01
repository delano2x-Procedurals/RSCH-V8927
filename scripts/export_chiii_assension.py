#!/usr/bin/env python3
"""Export Assension registers to data/ for the workspace-app."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "_CHPT III_Assension_db"
DATA = ROOT / "data"


def load_csv(name: str) -> list[dict]:
    path = DB / "registers" / name
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    headers = load_csv("header-index.csv")
    for rec in headers:
        rec["href_md"] = rec["md_link"]
        rec["href_howto"] = rec["howto_link"].replace(" ", "%20")
    payload = {
        "folder": "_CHPT III_Assension_db",
        "instrument_version": "ITDR-GQI-INT-v0.1.1",
        "headers": headers,
        "spine_map": load_csv("spine-map.csv"),
        "alignment_testers": load_csv("alignment-testers.csv"),
        "how_to_notes": load_csv("how-to-notes.csv"),
    }
    out = DATA / "chiii_assension.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(headers)} headers)")


if __name__ == "__main__":
    main()
