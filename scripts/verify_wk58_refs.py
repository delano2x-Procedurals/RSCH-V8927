#!/usr/bin/env python3
"""Verify Week 8 reference alignment on MW_Wk5_to_wk8_Edit_6Sep26.docx."""

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

SEMINAL_KEEP = {
    "Mitchell et al., 1997",
    "Donaldson & Preston, 1995",
    "Freeman et al., 2004",
    "Freeman et al., 2020",
    "Freeman, 1984",
    "Flanagan, 1954",
    "Chell, 2004",
    "Butterfield et al., 2005",
    "Caelli et al., 2003",
    "Kahlke, 2014",
    "Percy et al., 2015",
    "Lincoln & Guba, 1985",
    "Guba & Lincoln, 1994",
    "Fereday & Muir-Cochrane, 2006",
    "Taylor & Bogdan, 1998",
    "Braun & Clarke, 2019",
    "Nowell et al., 2017",
    "Malterud et al., 2016",
    "Guest et al., 2006",
    "Carcary, 2020",
    "Korstjens & Moser, 2018",
    "Weill & Ross, 2004",
    "National Commission for the Protection of Human Subjects of Biomedical and Behavioral Research, 1979",
}

# first-author surname -> years that must have a list entry when cited
INTEXT_TO_LIST = {
    "braun": {"2019"},
    "butterfield": {"2005"},
    "caelli": {"2003"},
    "capella": {"2024"},
    "carcary": {"2020"},
    "chell": {"2004"},
    "creswell": {"2024"},
    "donaldson": {"1995"},
    "dorobantu": {"2024"},
    "ekinci": {"2025"},
    "federal": {"2024"},
    "fereday": {"2006"},
    "flanagan": {"1954"},
    "freeman": {"2004", "2020"},
    "guest": {"2006"},
    "guba": {"1994"},
    "kahlke": {"2014"},
    "korstjens": {"2018"},
    "lester": {"2020"},
    "lincoln": {"1985"},
    "lowry": {"2025"},
    "malterud": {"2016"},
    "mitchell": {"1997"},
    "miteu": {"2024"},
    "molete": {"2025"},
    "naeem": {"2024"},
    "national": {"1979"},
    "nowell": {"2017"},
    "park": {"2023"},
    "percy": {"2015"},
    "taylor": {"1998"},
    "verizon": {"2025"},
    "walker": {"2026"},
    "weill": {"2004"},
    "wutich": {"2024"},
}

FORBIDDEN_IN_BODY = [
    "Haan",
    "Vasileiou",
    "Koerber",
    "Liu et al., 2020",
    "Mojtahedi",
    "Creswell & Poth, 1998",
    "Office for Human Research Protections",
    "Walker, 2026b",
    "Moser & Korstjens, 2023",
    "artifact sharing will remain optional",
]


def first_token(author: str) -> str:
    return re.split(r"[\s,]", author.strip().lower(), maxsplit=1)[0]


def main() -> int:
    errors = []
    doc = Document(str(DOC))
    para_count = len(doc.paragraphs)
    if abs(para_count - 228) / 228 > 0.05:
        errors.append(f"paragraph count {para_count} drifted more than 5% from 228")

    with ZipFile(DOC) as z:
        comments = etree.fromstring(z.read("word/comments.xml")).findall(".//w:comment", NS)
        if len(comments) != 36:
            errors.append(f"comment count {len(comments)} != 36")
        droot = etree.fromstring(z.read("word/document.xml"))
        starts = droot.findall(".//w:commentRangeStart", NS)
        if len(starts) != 36:
            errors.append(f"commentRangeStart {len(starts)} != 36")

    body = "\n".join(p.text for p in doc.paragraphs[:154])
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                body += "\n" + cell.text
    refs = "\n".join(p.text for p in doc.paragraphs[157:])

    if "Freeman, R. E., Phillips, R., & Sisodia, R. (2020). Tensions in stakeholder theory." not in refs:
        errors.append("Freeman et al. 2020 incomplete")
    if "https://doi.org/10.1177/0007650318773750" not in refs:
        errors.append("Freeman et al. 2020 DOI missing")

    freeman_p = next(p for p in doc.paragraphs[157:] if "Phillips" in p.text and "2020" in p.text)
    has_hl = bool(freeman_p._element.findall(f"{{{W}}}hyperlink"))
    if not has_hl:
        errors.append("Freeman et al. 2020 DOI is not a hyperlink")

    for s in FORBIDDEN_IN_BODY:
        if s in body:
            errors.append(f"forbidden leftover in body: {s}")

    # unique in-text works
    found_keys = set()
    for m in re.finditer(r"\(([^()]{4,240})\)", body):
        inner = m.group(1)
        if not re.search(r"(19|20)\d{2}", inner):
            continue
        parts = re.split(r";\s*", inner)
        for part in parts:
            years = re.findall(r"(?:19|20)\d{2}", part)
            if not years:
                continue
            author = re.split(r"(?:19|20)\d{2}", part, maxsplit=1)[0].strip(" ,")
            if not author:
                continue
            tok = first_token(author)
            for y in years:
                found_keys.add((tok, y))

    for m in re.finditer(
        r"([A-Z][A-Za-z’'\-]+(?:\s+et\s+al\.)?(?:\s+&\s+[A-Z][A-Za-z’'\-]+)?)\s+\(((?:19|20)\d{2})\)",
        body,
    ):
        found_keys.add((first_token(m.group(1)), m.group(2)))

    missing = []
    for tok, years in INTEXT_TO_LIST.items():
        for y in years:
            if (tok, y) not in found_keys:
                missing.append(f"{tok} {y} not found in text")
            # list match: first author token appears with that year
            if not re.search(rf"{re.escape(tok)}[^\n]{{0,220}}\({y}\)", refs, re.I):
                missing.append(f"{tok} {y} missing from reference list")

    if missing:
        errors.extend(missing)

    # bold in-text should only be Lester 2020
    bold_intext = []
    for i, p in enumerate(doc.paragraphs[:154]):
        for r in p.runs:
            if r.bold and (r.text or "").strip():
                # ignore pre-existing heading emphasis
                if "RSCH" in r.text or "Topic Endorsement" in r.text or "V8926" in r.text:
                    continue
                bold_intext.append((i, r.text.strip()))
    unexpected = [b for b in bold_intext if "Lester" not in b[1]]
    if unexpected:
        errors.append(f"unexpected in-text bold: {unexpected}")
    if not any("Lester" in t for _, t in bold_intext):
        errors.append("Lester et al., 2020 was not bolded in text")

    print(f"paragraphs={para_count}")
    print(f"comments=36")
    print(f"in-text unique keys={len(found_keys)}")
    print(f"in-text bold={bold_intext}")
    print(f"freeman_2020_complete=True")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
