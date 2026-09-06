#!/usr/bin/env python3
"""Validate the filled Weeks 8–10 QDA SOP and the n = 12 lock."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOP_MD = ROOT / "docs" / "amalgamation-wk8-10-qda-sop.md"
SOP_DOCX = (
    ROOT
    / "downloads"
    / "AMALGAMATION_wk8_10_Step-by-Step_SOP_for_Qualitative_Data_Analysis.docx"
)
LOCK_FILES = [
    ROOT / "docs" / "chapter-iii-methodology.md",
    ROOT / "docs" / "symbols-definitions-refs.md",
    ROOT / "docs" / "collection-analysis-revision-packet.md",
    ROOT / "docs" / "alignment-assessment-data-collection.md",
]


def extract_docx_text(path: Path) -> str:
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    paras = []
    for para in root.iter(f"{ns}p"):
        texts = [t.text or "" for t in para.iter(f"{ns}t")]
        paras.append("".join(texts))
    return "\n".join(paras)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def check_sop_text(text: str, label: str, errors: list[str]) -> None:
    require("n = 12" in text or "n = 12 locked" in text, f"{label}: missing n = 12 lock language", errors)
    require("locked at 12" in text.lower() or "locked at **12**" in text.lower() or "sample is locked at 12" in text.lower(), f"{label}: missing locked-at-12 sentence", errors)
    require("Malterud" in text, f"{label}: missing Malterud information-power citation", errors)
    require("Naeem" in text, f"{label}: missing Naeem stopping citation", errors)
    require("Percy" in text, f"{label}: missing Percy purposive-sampling citation", errors)
    require("Fereday" in text, f"{label}: missing Fereday hybrid codebook TA citation", errors)
    require("Lincoln" in text and "Guba" in text, f"{label}: missing Lincoln & Guba", errors)
    require("ITDR-GQI-INT-v0.1.1" in text, f"{label}: missing instrument ID", errors)
    require("Delve" in text, f"{label}: missing Delve CAQDAS", errors)
    require("PQ1" in text and "PQ2" in text, f"{label}: missing implied project questions", errors)
    require("10 to 200" in text, f"{label}: missing firm-size bound", errors)
    require("36 months" in text, f"{label}: missing 36-month inclusion window", errors)
    for heading in (
        "3.1 Introduction",
        "3.2 Research design",
        "3.3 Role of the researcher",
        "3.4 Participant selection",
        "3.5 Instrumentation",
        "3.7 Qualitative data analysis",
        "3.8 Trustworthiness",
        "3.9 Ethical assurances",
    ):
        require(heading in text, f"{label}: missing heading {heading}", errors)

    # Forbidden leftover template language
    require("[Insert" not in text, f"{label}: leftover [Insert placeholder", errors)
    require("[NVivo / MAXQDA" not in text, f"{label}: leftover NVivo/MAXQDA placeholder", errors)
    require("lived experience" not in text.lower() or "does not use “lived experience”" in text or 'does not use "lived experience"' in text or "Lived experience / essence" in text or "lived experience / essence" in text.lower(), f"{label}: uses lived-experience as method language", errors)
    require("analyzed using Delve" not in text.lower() or "Do not write" in text or "do not write" in text.lower(), f"{label}: claims analysis is performed by Delve", errors)
    require("N = 12 to 20" not in text and "12 to 20 participants" not in text, f"{label}: leftover 12–20 range", errors)
    require("10 to 15 managers" not in text and "10–15 participants" not in text, f"{label}: leftover 10–15 sample range", errors)


def check_lock_files(errors: list[str]) -> None:
    for path in LOCK_FILES:
        text = path.read_text(encoding="utf-8")
        require("12" in text, f"{path.name}: missing 12", errors)
        # Planned 10–15 range should no longer be the locked sample language
        leftover_ranges = re.findall(r"planned (?:sample )?is 10 to 15", text, flags=re.I)
        require(not leftover_ranges, f"{path.name}: still says planned sample is 10 to 15", errors)
        require(
            "locked at 12" in text.lower() or "n = 12 locked" in text.lower() or "sample of 12" in text.lower(),
            f"{path.name}: missing n = 12 lock phrasing",
            errors,
        )


def main() -> int:
    errors: list[str] = []
    require(SOP_MD.exists(), f"missing {SOP_MD}", errors)
    require(SOP_DOCX.exists(), f"missing {SOP_DOCX}", errors)
    if SOP_MD.exists():
        check_sop_text(SOP_MD.read_text(encoding="utf-8"), "SOP markdown", errors)
    if SOP_DOCX.exists():
        check_sop_text(extract_docx_text(SOP_DOCX), "SOP docx", errors)
        require(SOP_DOCX.stat().st_size > 20_000, "SOP docx is unexpectedly small", errors)
    check_lock_files(errors)

    if errors:
        print("QDA SOP validation FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("QDA SOP validation OK")
    print(f"  markdown: {SOP_MD}")
    print(f"  docx:     {SOP_DOCX} ({SOP_DOCX.stat().st_size} bytes)")
    print("  n = 12 lock confirmed in SOP and companion methodology files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
