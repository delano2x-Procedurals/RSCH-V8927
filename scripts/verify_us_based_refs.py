#!/usr/bin/env python3
"""Verify U.S.-based reference swaps on MW_Wk5_to_wk8_Edit_6Sep26.docx."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from lxml import etree

DOC = Path("/workspace/downloads/MW_Wk5_to_wk8_Edit_6Sep26.docx")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

SEMINAL_KEEP = [
    "Mitchell et al., 1997",
    "Donaldson & Preston, 1995",
    "Freeman et al., 2004",
    "Freeman et al., 2020",
    "Flanagan, 1954",
    "Lincoln & Guba, 1985",
    "Caelli et al., 2003",
    "Kahlke, 2014",
    "Percy et al., 2015",
    "Fereday & Muir-Cochrane, 2006",
    "Malterud et al., 2016",
]

REQUIRED_INTEXT = [
    "U.S. Small Business Administration, 2026",
    "Ampel et al., 2024",
    "Morse, 2015",
    "Paulus, 2023",
    "Guest et al., 2020",
    "Resnik, 2018",
    "Saldaña, 2021",
    "Tracy, 2010",
    "Gremler, 2004",
    "Guest et al. (2006)",
]

FORBIDDEN_IN_BODY = [
    "Ekinci",
    "Molete",
    "Korstjens",
    "Carcary",
    "Naeem",
    "Miteu",
    "Braun",
    "Nowell",
    "Chell",
    "Butterfield",
    "Haan",
    "Vasileiou",
    "Koerber",
    "Mojtahedi",
    "Creswell & Poth, 1998",
]

REQUIRED_LIST = [
    "Gremler, D. D. (2004)",
    "Guest, G., Namey, E., & Chen, M. (2020)",
    "Morse, J. M. (2015)",
    "Paulus, T. M. (2023)",
    "Resnik, D. B. (2018)",
    "Saldaña, J. (2021)",
    "U.S. Small Business Administration. (2026)",
    "Freeman, R. E., Phillips, R., & Sisodia, R. (2020). Tensions in stakeholder theory.",
    "https://doi.org/10.1177/0007650318773750",
]

SPOKEN_STEMS = [
    "Q0. Please walk me through one specific disruption",
    "L1. In that event, who actually moved what got restored first",
    "F3. Looking back, what would you point to if you had to defend that restoration",
]


def main() -> int:
    errors = []
    doc = Document(str(DOC))
    if len(doc.paragraphs) != 228:
        errors.append(f"paragraph count {len(doc.paragraphs)} != 228")

    with ZipFile(DOC) as z:
        comments = etree.fromstring(z.read("word/comments.xml")).findall(".//w:comment", NS)
        if len(comments) != 36:
            errors.append(f"comment count {len(comments)} != 36")
        droot = etree.fromstring(z.read("word/document.xml"))
        starts = droot.findall(".//w:commentRangeStart", NS)
        if len(starts) != 36:
            errors.append(f"commentRangeStart {len(starts)} != 36")

    body = "\n".join(p.text for p in doc.paragraphs[:154])
    table_text = ""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                table_text += "\n" + cell.text
    refs = "\n".join(p.text for p in doc.paragraphs[157:])

    for s in SEMINAL_KEEP:
        if s not in body and s.replace(", ", " ") not in body:
            # Freeman 2004 may appear as "Freeman et al., 2004"
            if s not in body:
                errors.append(f"seminal missing from body: {s}")

    for s in REQUIRED_INTEXT:
        if s not in body:
            errors.append(f"required U.S. in-text missing: {s}")

    for s in FORBIDDEN_IN_BODY:
        if s in body:
            errors.append(f"forbidden leftover in body: {s}")

    for s in REQUIRED_LIST:
        if s not in refs:
            errors.append(f"required list entry missing: {s}")

    for s in SPOKEN_STEMS:
        if s not in table_text:
            errors.append(f"spoken interview stem changed/missing: {s}")

    bold_intext = []
    for i, p in enumerate(doc.paragraphs[:154]):
        for r in p.runs:
            if r.bold and (r.text or "").strip():
                if "RSCH" in r.text or "Topic Endorsement" in r.text or "V8926" in r.text:
                    continue
                bold_intext.append((i, r.text.strip()))

    bold_refs = []
    for p in doc.paragraphs[157:]:
        t = p.text.strip()
        if not t:
            continue
        if any(r.bold and (r.text or "").strip() for r in p.runs):
            bold_refs.append(t.split("(")[0].strip())

    freeman_p = next((p for p in doc.paragraphs[157:] if "Phillips" in p.text and "2020" in p.text), None)
    if freeman_p is None or not freeman_p._element.findall(f"{{{W}}}hyperlink"):
        errors.append("Freeman et al. 2020 DOI is not a hyperlink")

    print(f"paragraphs={len(doc.paragraphs)}")
    print(f"comments=36")
    print(f"in-text bold={bold_intext}")
    print(f"bold leftover list authors={bold_refs}")
    print(f"bold leftover count={len(bold_refs)}")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
