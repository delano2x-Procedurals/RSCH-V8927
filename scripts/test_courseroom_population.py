#!/usr/bin/env python3
"""Validate the standalone courseroom Population download."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "docs" / "courseroom-population.md"
DOCX = ROOT / "downloads" / "WALKER_Project_Plan_Population.docx"
SOP = ROOT / "docs" / "amalgamation-wk8-10-qda-sop.md"


def extract_docx_text(path: Path) -> str:
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    paras = []
    for para in root.iter(f"{ns}p"):
        texts = [t.text or "" for t in para.iter(f"{ns}t")]
        paras.append("".join(texts))
    return "\n".join(paras)


def main() -> int:
    errors: list[str] = []
    if not MD.exists():
        errors.append(f"missing {MD}")
    if not DOCX.exists():
        errors.append(f"missing {DOCX}")
    text = MD.read_text(encoding="utf-8") if MD.exists() else ""
    docx = extract_docx_text(DOCX) if DOCX.exists() else ""
    for label, body in (("markdown", text), ("docx", docx)):
        for needle in (
            "## Population",
            "10 to 200",
            "36 months",
            "Percy",
            "Malterud",
            "Flanagan",
            "ITDRPaaS",
            "locked sample of 12",
        ):
            if needle not in body and not (label == "docx" and needle == "## Population" and "Population" in body):
                errors.append(f"{label}: missing {needle}")
        if "Items marked NEW" in body:
            errors.append(f"{label}: leaked revision-packet intro")
        if "I will" in body or "I am" in body:
            errors.append(f"{label}: first-person language")
    if SOP.exists():
        sop = SOP.read_text(encoding="utf-8")
        if "## Courseroom paste" in sop or "Project Plan: Population" in sop:
            errors.append("SOP was modified with courseroom population paste")
    if errors:
        print("Courseroom population validation FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("Courseroom population validation OK")
    print(f"  {DOCX} ({DOCX.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
