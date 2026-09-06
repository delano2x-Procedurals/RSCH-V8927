#!/usr/bin/env python3
"""Validate the standalone four-paragraph data-analysis download."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "docs" / "courseroom-data-analysis-4para.md"
DOCX = ROOT / "downloads" / "WALKER_Project_Plan_Data_Analysis_4para.docx"
SOP = ROOT / "docs" / "amalgamation-wk8-10-qda-sop.md"


def extract_docx_text(path: Path) -> str:
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    paras = []
    for para in root.iter(f"{ns}p"):
        texts = [t.text or "" for t in para.iter(f"{ns}t")]
        line = "".join(texts).strip()
        if line:
            paras.append(line)
    return paras


def main() -> int:
    errors: list[str] = []
    if not MD.exists():
        errors.append(f"missing {MD}")
    if not DOCX.exists():
        errors.append(f"missing {DOCX}")
    text = MD.read_text(encoding="utf-8") if MD.exists() else ""
    body_start = text.find("The researcher will analyze")
    body = text[body_start : text.find("\n---\n", body_start)] if body_start != -1 else ""
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    if len(paras) != 4:
        errors.append(f"markdown body is {len(paras)} paragraphs, expected 4")
    for needle in (
        "Fereday",
        "locked sample of 12",
        "meaning units",
        "Delve will not perform the analysis",
        "Naeem",
        "Mitchell",
        "Shoogleit" not in text and "Edinburgh" not in text,
    ):
        if needle is True:
            continue
        if needle is False:
            errors.append("fashion-sample debris leaked into the insert")
            continue
        if isinstance(needle, str) and needle not in text:
            errors.append(f"markdown: missing {needle}")
    if "Shoogleit" in text or "Edinburgh June 2014" in text:
        errors.append("fashion-sample debris leaked into the insert")
    if "I will" in text or "I am" in text:
        errors.append("first-person language")
    if SOP.exists() and "Offering C detailed four-paragraph" in SOP.read_text(encoding="utf-8"):
        errors.append("SOP was modified with the courseroom analysis insert")
    if DOCX.exists():
        docx_paras = extract_docx_text(DOCX)
        joined = "\n".join(docx_paras)
        if "Fereday" not in joined or "locked sample of 12" not in joined:
            errors.append("docx missing core analysis language")
        if "Items marked NEW" in joined:
            errors.append("docx leaked revision-packet intro")
    if errors:
        print("Courseroom data-analysis validation FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("Courseroom data-analysis validation OK")
    print(f"  {DOCX} ({DOCX.stat().st_size} bytes)")
    print("  four-paragraph body confirmed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
