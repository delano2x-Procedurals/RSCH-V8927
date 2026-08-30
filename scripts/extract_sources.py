#!/usr/bin/env python3
"""Extract every non-empty cell from source workbooks and build searchable records."""
from __future__ import annotations

import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT / "source" / "originals"
INVENTORY = ROOT / "source" / "inventory"
DATA = ROOT / "data"


def colrow(cell_ref: str | None) -> tuple[int, int]:
    m = re.match(r"([A-Z]+)(\d+)", cell_ref or "")
    if not m:
        return 0, 0
    col = 0
    for ch in m.group(1):
        col = col * 26 + (ord(ch) - 64)
    return col, int(m.group(2))


def col_letter(n: int) -> str:
    out = []
    while n:
        n, r = divmod(n - 1, 26)
        out.append(chr(65 + r))
    return "".join(reversed(out)) or "A"


def load_sst(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET_fromstring(zf.read("xl/sharedStrings.xml"))
    strings = []
    for si in root.findall("m:si", NS):
        strings.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))
    return strings


def ET_fromstring(raw: bytes):
    import xml.etree.ElementTree as ET

    return ET.fromstring(raw)


def cell_val(c, sst: list[str]) -> str:
    t = c.get("t")
    v = c.find("m:v", NS)
    is_el = c.find("m:is", NS)
    if t == "s" and v is not None and v.text:
        return sst[int(v.text)]
    if t == "inlineStr" and is_el is not None:
        return "".join(x.text or "" for x in is_el.findall(".//m:t", NS))
    if v is not None and v.text:
        return v.text
    return ""


def workbook_sheets(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    import xml.etree.ElementTree as ET

    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {rel.get("Id"): rel.get("Target") for rel in rels}
    out = []
    for sh in wb.findall("m:sheets/m:sheet", NS):
        name = sh.get("name")
        rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rid_to_target.get(rid, "")
        path = target.lstrip("/")
        if not path.startswith("xl/"):
            path = "xl/" + target.lstrip("/")
        out.append((name, path))
    return out


def dump_sheet(zf: zipfile.ZipFile, path: str, sst: list[str]) -> dict:
    root = ET_fromstring(zf.read(path))
    rows: dict[int, dict[int, str]] = defaultdict(dict)
    for c in root.findall(".//m:c", NS):
        col, row = colrow(c.get("r"))
        if col < 1 or row < 1:
            continue
        val = cell_val(c, sst)
        if val and str(val).strip():
            rows[row][col] = str(val).strip()
    row_payload = []
    for r in sorted(rows):
        cells = {col_letter(c): rows[r][c] for c in sorted(rows[r])}
        row_payload.append({"row": r, "cells": cells})
    return {
        "max_row": max(rows) if rows else 0,
        "max_col": max((max(cols) for cols in rows.values()), default=0),
        "nonempty_rows": len(rows),
        "nonempty_cells": sum(len(cols) for cols in rows.values()),
        "rows": row_payload,
    }


def extract_workbook(xlsx_path: Path) -> dict:
    with zipfile.ZipFile(xlsx_path) as zf:
        sst = load_sst(zf)
        sheets_meta = []
        sheets = {}
        for name, path in workbook_sheets(zf):
            payload = dump_sheet(zf, path, sst)
            sheets[name] = payload
            sheets_meta.append(
                {
                    "name": name,
                    "path": path,
                    "nonempty_rows": payload["nonempty_rows"],
                    "nonempty_cells": payload["nonempty_cells"],
                    "max_row": payload["max_row"],
                    "max_col": payload["max_col"],
                }
            )
    return {
        "file": xlsx_path.name,
        "sheet_count": len(sheets_meta),
        "sheets": sheets_meta,
        "data": sheets,
    }


def row_text(row: dict, letters: list[str]) -> dict[str, str]:
    return {k: row.get(k, "") for k in letters}


def flatten_row(row: dict) -> str:
    return " | ".join(f"{k}:{v}" for k, v in row.items() if v)


def build_structured(inventory: dict) -> dict:
    reading = inventory["BMGT8044_Reading_List-2.xlsx"]["data"]
    align = inventory["BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx"]["data"]
    formatted = inventory["BMGT8044_Wk7_Leadership_Theories_Alignment_v01_formatted.xlsx"]["data"]

    references = []
    sheet0 = {r["row"]: r["cells"] for r in reading["Sheet0"]["rows"]}
    header = sheet0.get(11, {})
    field_map = {
        "D": "section_name",
        "E": "section_description",
        "I": "item_type",
        "J": "item_title",
        "K": "item_chapter_title",
        "L": "item_author",
        "M": "item_chapter_author",
        "N": "item_journal_title",
        "O": "item_publication_date",
        "P": "item_edition",
        "Q": "item_isbn",
        "R": "item_issn",
        "S": "item_lccn",
        "T": "item_oclc",
        "U": "item_publisher",
        "V": "item_place",
        "W": "item_volume",
        "X": "item_issue",
        "Y": "item_pages",
        "Z": "item_page_range",
        "AA": "item_editor",
        "AB": "item_doi",
        "AC": "item_chapter_number",
        "AD": "item_url",
        "AE": "item_notes",
        "AF": "item_availability",
        "AG": "item_due_date",
        "AH": "item_tags",
        "AI": "item_student_note",
        "AJ": "permalink",
    }
    for idx, row_num in enumerate(sorted(k for k in sheet0 if k >= 12), start=1):
        cells = sheet0[row_num]
        rec = {dest: cells.get(src, "") for src, dest in field_map.items()}
        rec["id"] = f"REF-{idx:03d}"
        rec["source_file"] = "BMGT8044_Reading_List-2.xlsx"
        rec["source_tab"] = "Sheet0"
        rec["source_row"] = row_num
        rec["week"] = rec["section_name"]
        rec["type"] = "Reference"
        rec["title"] = rec["item_title"] or rec["section_name"]
        rec["apa"] = "; ".join(
            x
            for x in [
                rec["item_author"],
                rec["item_title"],
                rec["item_journal_title"],
                rec["item_publication_date"],
                rec["item_doi"],
            ]
            if x
        )
        rec["search_text"] = " ".join(
            str(v) for v in rec.values() if isinstance(v, str)
        )
        rec["used_in_tab"] = "03_REFERENCES_MASTER"
        rec["comps_audit_tag"] = rec.get("item_tags") or ""
        rec["gap_note"] = rec.get("item_student_note") or ""
        rec["status"] = ""
        references.append(rec)

    extra_refs = []
    ref_sheet = {r["row"]: r["cells"] for r in reading[" REFERENCES"]["rows"]}
    extra_n = 1
    for row_num, cells in ref_sheet.items():
        text = " ".join(cells.values())
        if not text.strip():
            continue
        extra_refs.append(
            {
                "id": f"XREF-{extra_n:03d}",
                "type": "Reference",
                "title": cells.get("B") or cells.get("C") or text[:120],
                "apa": cells.get("C") or text,
                "item_url": cells.get("D", ""),
                "week": "Supplemental",
                "item_type": "Supplemental",
                "source_file": "BMGT8044_Reading_List-2.xlsx",
                "source_tab": " REFERENCES",
                "source_row": row_num,
                "used_in_tab": "03_REFERENCES_MASTER",
                "comps_audit_tag": "",
                "gap_note": "",
                "search_text": text,
                "status": "",
            }
        )
        extra_n += 1

    themes = []
    theme_sheet = {r["row"]: r["cells"] for r in align["Sheet1"]["rows"]}
    for idx, row_num in enumerate(sorted(k for k in theme_sheet if k >= 2), start=1):
        cells = theme_sheet[row_num]
        themes.append(
            {
                "id": f"THEME-{idx:02d}",
                "type": "Theme",
                "theme": cells.get("A", ""),
                "title": cells.get("A", ""),
                "description": cells.get("B", ""),
                "references": cells.get("C", ""),
                "apa": cells.get("C", ""),
                "week": "Leadership alignment",
                "item_type": "Leadership theme",
                "source_file": "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
                "source_tab": "Sheet1",
                "source_row": row_num,
                "used_in_tab": "05_LEADERSHIP_ALIGNMENT",
                "search_text": " ".join(cells.values()),
                "status": "",
            }
        )

    parking = []
    pl_sheet = {r["row"]: r["cells"] for r in reading[" Parkinglot_"]["rows"]}
    pl_idx = 1
    for row_num in sorted(pl_sheet):
        cells = pl_sheet[row_num]
        text = " ".join(cells.values()).strip()
        if not text:
            continue
        title = cells.get("C") or cells.get("B") or cells.get("A") or text[:140]
        week = ""
        a = cells.get("A", "")
        if re.match(r"(?i)wk\s*\d+|week\s*\d+", a):
            week = a
        parking.append(
            {
                "id": f"PL-{pl_idx:03d}",
                "type": "Parking lot",
                "title": title[:200],
                "item": title,
                "why_parked": cells.get("C") or text,
                "source_tab": " Parkinglot_",
                "linked_id": "",
                "status": "open" if row_num >= 58 else "resolved",
                "owner": "Member",
                "due": "",
                "resolution": "" if row_num >= 58 else "Retained from source parking lot as course/context note",
                "returned_to_tab": "",
                "week": week or "Parking lot",
                "item_type": "Parking lot",
                "source_file": "BMGT8044_Reading_List-2.xlsx",
                "source_row": row_num,
                "used_in_tab": "02_PARKING_LOT",
                "search_text": text,
                "cells": cells,
            }
        )
        pl_idx += 1

    theory_rows = []
    th = {r["row"]: r["cells"] for r in reading["Theory Academic Definition"]["rows"]}
    for idx, row_num in enumerate(sorted(th), start=1):
        cells = th[row_num]
        text = " ".join(cells.values())
        theory_rows.append(
            {
                "id": f"TH-{idx:04d}",
                "type": "Theory",
                "title": (cells.get("D") or cells.get("C") or cells.get("A") or cells.get("E") or text[:140]),
                "description": text,
                "week": "Theory definitions",
                "item_type": "Theory",
                "source_file": "BMGT8044_Reading_List-2.xlsx",
                "source_tab": "Theory Academic Definition",
                "source_row": row_num,
                "used_in_tab": "04_THEORY_AND_SPINE",
                "search_text": text,
                "status": "",
                "cells": cells,
            }
        )

    spine_rows = []
    sp = {r["row"]: r["cells"] for r in reading["Dissertation Spine_db"]["rows"]}
    for idx, row_num in enumerate(sorted(sp), start=1):
        cells = sp[row_num]
        text = " ".join(cells.values())
        spine_rows.append(
            {
                "id": f"SP-{idx:03d}",
                "type": "Theory",
                "title": cells.get("C") or cells.get("D") or text[:140],
                "description": cells.get("E") or text,
                "classification": cells.get("D", ""),
                "explanation": cells.get("E", ""),
                "week": "Dissertation spine",
                "item_type": "Spine",
                "source_file": "BMGT8044_Reading_List-2.xlsx",
                "source_tab": "Dissertation Spine_db",
                "source_row": row_num,
                "used_in_tab": "04_THEORY_AND_SPINE",
                "search_text": text,
                "status": "",
                "cells": cells,
            }
        )

    archive = []

    def add_archive(file_key: str, tab: str, type_label: str, used: str, week: str):
        payload = inventory[file_key]["data"].get(tab)
        if not payload:
            return
        for idx, row in enumerate(payload["rows"], start=1):
            text = " ".join(row["cells"].values())
            if len(text) < 8:
                continue
            first = next(iter(row["cells"].values()))
            archive.append(
                {
                    "id": f"ARC-{len(archive)+1:04d}",
                    "type": "Archive",
                    "title": (first[:160] if first else text[:160]),
                    "description": text,
                    "week": week,
                    "item_type": type_label,
                    "source_file": file_key,
                    "source_tab": tab,
                    "source_row": row["row"],
                    "used_in_tab": used,
                    "search_text": text,
                    "status": "archive",
                    "cells": row["cells"],
                }
            )

    add_archive("BMGT8044_Reading_List-2.xlsx", "ORIGINS_LXI", "Origins/LXI", "07_SOURCE_ARCHIVE", "Origins")
    add_archive("BMGT8044_Reading_List-2.xlsx", "KEY WORD_db", "Keyword db", "07_SOURCE_ARCHIVE", "Keywords")
    add_archive("BMGT8044_Reading_List-2.xlsx", "Qual Tool Recco", "Qual tool", "06_QUAL_METHODS_AND_TOOLS", "Methods")
    add_archive("BMGT8044_Reading_List-2.xlsx", "Reserch Preperation_db", "Research prep", "07_SOURCE_ARCHIVE", "Prep")
    add_archive("BMGT8044_Reading_List-2.xlsx", "APA- Direct Quoting", "APA quoting", "07_SOURCE_ARCHIVE", "APA")
    add_archive("BMGT8044_Reading_List-2.xlsx", "STKHLDR  MGMT", "Stakeholder mgmt", "07_SOURCE_ARCHIVE", "Stakeholder")
    add_archive("BMGT8044_Reading_List-2.xlsx", "Stakeholder theory", "Stakeholder article", "07_SOURCE_ARCHIVE", "Stakeholder")
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        "Data Collection Steps&Analysis",
        "ARCHIVE_COMPARATIVE quantitative plan",
        "07_SOURCE_ARCHIVE",
        "Archive comparative",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        "Sheet3",
        "Reviewer notes",
        "07_SOURCE_ARCHIVE",
        "Archive",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        "Qual Data Analysis Methods",
        "Qual methods",
        "06_QUAL_METHODS_AND_TOOLS",
        "Methods",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        "Research Methods_Step7",
        "Research design notes",
        "07_SOURCE_ARCHIVE",
        "Archive",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        "Quan Data Analysis Methods",
        "ARCHIVE_COMPARATIVE quantitative methods",
        "07_SOURCE_ARCHIVE",
        "Archive comparative",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        " 8055 Wk1",
        "RSCH8055 week 1",
        "07_SOURCE_ARCHIVE",
        "Archive",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        "Sheet8",
        "Practice planning",
        "07_SOURCE_ARCHIVE",
        "Archive",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
        "Sheet9",
        "Week 7 CAQDAS",
        "06_QUAL_METHODS_AND_TOOLS",
        "Week 7",
    )
    add_archive(
        "BMGT8044_Wk7_Leadership_Theories_Alignment_v01_formatted.xlsx",
        "Sheet1",
        "Leadership themes formatted copy",
        "07_SOURCE_ARCHIVE",
        "Lineage",
    )

    interview_questions = [
        {
            "id": "IQ-01",
            "type": "Interview",
            "construct": "Phenomenon / recoverability assurance",
            "title": "How does the participant describe recoverability assurance after a disruption?",
            "question": "Would the participant walk the researcher through a recent incident in which recoverability had to be demonstrated to others, including what counted as sufficient assurance?",
            "review_question": "Does the follow-up still ask about assurance production, or has it drifted into general IT operations?",
            "ethical_check": "Limits extraction to the incident the participant elects to narrate; no pressure to name clients or disclose restricted artifacts.",
            "linked_refs": ["REF-018", "REF-021", "TH-phenomenon"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "recoverability assurance critical incident disruption evidence",
        },
        {
            "id": "IQ-02",
            "type": "Interview",
            "construct": "Stakeholder salience — power",
            "title": "Whose claims carried authority during the incident?",
            "question": "In that incident, whose requests or objections most strongly shaped who could authorize recovery actions, and how did the participant recognize that authority?",
            "review_question": "Does the review probe power as perceived by the participant, rather than the researcher’s preferred hierarchy?",
            "ethical_check": "Avoids asking the participant to evaluate named individuals for competence; focuses on role-based claims.",
            "linked_refs": ["SP-019"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "power authority stakeholder salience decision rights",
        },
        {
            "id": "IQ-03",
            "type": "Interview",
            "construct": "Stakeholder salience — legitimacy",
            "title": "Which claims were treated as legitimate evidence requirements?",
            "question": "Which parties’ evidence or documentation requirements were treated as legitimate during recovery, and which claims were set aside?",
            "review_question": "Does the follow-up stay with legitimacy of claims, not the researcher’s view of who should have been heard?",
            "ethical_check": "Does not invite gossip about colleagues; asks about claims and artifacts, not personal character.",
            "linked_refs": ["SP-019", "REF-021"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "legitimacy evidence requirements stakeholder claims",
        },
        {
            "id": "IQ-04",
            "type": "Interview",
            "construct": "Stakeholder salience — urgency",
            "title": "How did urgency change prioritization and escalation?",
            "question": "When time pressure increased, how did the participant decide whose urgency justified escalation or a lowered evidence threshold?",
            "review_question": "Does the review question still test urgency as a salience attribute rather than a generic stress story?",
            "ethical_check": "Allows the participant to withhold commercially sensitive timelines.",
            "linked_refs": ["SP-025"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "urgency escalation evidence threshold PLU",
        },
        {
            "id": "IQ-05",
            "type": "Interview",
            "construct": "Decision-rights clarity",
            "title": "How were recovery decision rights understood?",
            "question": "How did the participant know who held decision rights for failover, restoration, exception approval, or communication to stakeholders?",
            "review_question": "Is the question still about decision rights, or has it become a general org-chart question?",
            "ethical_check": "Does not require the participant to produce internal RACI charts if that would breach policy.",
            "linked_refs": ["SP-031"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "decision rights governance ITDRPaaS authority",
        },
        {
            "id": "IQ-06",
            "type": "Interview",
            "construct": "Ethical / character-based leadership",
            "title": "How did the participant hold self and others to an assurance standard?",
            "question": "In that incident, how did the participant describe the standard they held themselves to when others wanted faster assurance than the evidence supported?",
            "review_question": "Does the follow-up still connect leadership self-discipline to assurance ethics, not charisma?",
            "ethical_check": "Frames leadership as the participant’s own account; does not score the participant against a preferred theory.",
            "linked_refs": ["THEME-03", "THEME-04", "THEME-06"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "ethical leadership servant character integrity assurance",
        },
        {
            "id": "IQ-07",
            "type": "Interview",
            "construct": "Adaptive leadership under change",
            "title": "How did the participant adapt governance when the incident changed?",
            "question": "When the disruption unfolded differently than planned, what did the participant change about stakeholder communication, evidence, or escalation?",
            "review_question": "Does the review still ask about adaptation of governance, not a heroic-leader narrative?",
            "ethical_check": "Invites process description rather than blame assignment.",
            "linked_refs": ["THEME-07"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "adaptive leadership change incident governance",
        },
        {
            "id": "IQ-08",
            "type": "Interview",
            "construct": "Trustworthiness / member meaning",
            "title": "How should the researcher check the participant’s meaning?",
            "question": "If the researcher summarized the incident as a story about whose claims counted, what would the participant correct?",
            "review_question": "Is this still a member-check on meaning, not a request for the participant to validate the researcher’s theory?",
            "ethical_check": "Gives the participant the last word on interpretation of their account.",
            "linked_refs": ["REF-035"],
            "status": "aligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "member check trustworthiness meaning qualitative ethics",
        },
        {
            "id": "IQ-09",
            "type": "Interview",
            "construct": "Template — unaligned placeholder",
            "title": "Unaligned draft question (template)",
            "question": "[Draft] What does the participant think about leadership in general?",
            "review_question": "This question does not map to a defined construct and must not be used for extraction until aligned.",
            "ethical_check": "Flagged unaligned: extraction from this prompt would invent codes not warranted by the protocol.",
            "linked_refs": [],
            "status": "unaligned",
            "week": "Interview protocol",
            "item_type": "Interview question",
            "used_in_tab": "09_INTERVIEW_PROTOCOL",
            "search_text": "unaligned template leadership general",
            "citation_insert": "",
        },
    ]
    for q in interview_questions:
        q.setdefault("citation_insert", "")

    index = [
        {
            "id": "TOOL-DELVE",
            "type": "Tool",
            "title": "Delve (delvetool.com) — primary CAQDAS tool in use",
            "excerpt": "Delve is the named product used for coding, retrieval, memoing, and audit. CAQDAS is the category, not the tool name.",
            "week": "Methods",
            "status": "in use",
            "used_in_tab": "06_QUAL_METHODS_AND_TOOLS",
            "source_tab": "tool_usage",
            "item_type": "Tool",
            "href": "methods.html#TOOL-DELVE",
            "search_text": "Delve delvetool CAQDAS qualitative coding memo audit reflexive thematic analysis",
        },
        {
            "id": "SOP-RQ1",
            "type": "SOP",
            "title": "RQ1 SOP, abstract, key wording, and APA 7 data statement",
            "excerpt": "Step-by-step procedure and data statement for evaluating analysis strategies. Delve is the CAQDAS product in use.",
            "week": "RQ1",
            "status": "in use",
            "used_in_tab": "14_SOP_RQ1",
            "source_tab": "sop",
            "item_type": "SOP",
            "href": "sop.html#SOP-RQ1",
            "search_text": "SOP step-by-step data statement abstract key wording APA7 RQ1 Delve ethical extraction",
        },
    ]
    for bucket in (
        references,
        extra_refs,
        themes,
        parking,
        theory_rows,
        spine_rows,
        interview_questions,
        archive,
    ):
        for rec in bucket:
            index.append(
                {
                    "id": rec["id"],
                    "type": rec.get("type", ""),
                    "title": rec.get("title") or rec.get("theme") or rec.get("question") or rec["id"],
                    "excerpt": (
                        rec.get("description")
                        or rec.get("apa")
                        or rec.get("item")
                        or rec.get("question")
                        or rec.get("search_text")
                        or ""
                    )[:280],
                    "week": rec.get("week", ""),
                    "status": rec.get("status", ""),
                    "used_in_tab": rec.get("used_in_tab", ""),
                    "source_tab": rec.get("source_tab", ""),
                    "item_type": rec.get("item_type", rec.get("type", "")),
                    "href": page_for(rec.get("used_in_tab", ""), rec["id"]),
                    "search_text": rec.get("search_text", ""),
                }
            )

    lineage = []
    for fname, wb in inventory.items():
        for sheet in wb["sheets"]:
            lineage.append(
                {
                    "source_file": fname,
                    "source_tab": sheet["name"],
                    "nonempty_rows": sheet["nonempty_rows"],
                    "nonempty_cells": sheet["nonempty_cells"],
                    "destination_tab": destination_for(fname, sheet["name"]),
                    "notes": notes_for(fname, sheet["name"]),
                }
            )

    return {
        "references": references,
        "extra_refs": extra_refs,
        "themes": themes,
        "parking_lot": parking,
        "theory": theory_rows,
        "spine": spine_rows,
        "interview_questions": interview_questions,
        "archive": archive,
        "index": index,
        "lineage": lineage,
        "counts": {
            "references": len(references),
            "extra_refs": len(extra_refs),
            "themes": len(themes),
            "parking_lot": len(parking),
            "parking_open": sum(1 for p in parking if p["status"] == "open"),
            "parking_resolved": sum(1 for p in parking if p["status"] == "resolved"),
            "theory": len(theory_rows),
            "spine": len(spine_rows),
            "interview_questions": len(interview_questions),
            "interview_aligned": sum(1 for q in interview_questions if q["status"] == "aligned"),
            "interview_unaligned": sum(1 for q in interview_questions if q["status"] == "unaligned"),
            "archive": len(archive),
            "index": len(index),
        },
        "header_row_sheet0": header,
    }


def page_for(tab: str, rec_id: str) -> str:
    mapping = {
        "02_PARKING_LOT": "parking-lot.html",
        "03_REFERENCES_MASTER": "references.html",
        "04_THEORY_AND_SPINE": "theory-spine.html",
        "05_LEADERSHIP_ALIGNMENT": "leadership.html",
        "06_QUAL_METHODS_AND_TOOLS": "methods.html",
        "07_SOURCE_ARCHIVE": "archive.html",
        "09_INTERVIEW_PROTOCOL": "interview-protocol.html",
        "08_RQ1_ANALYSIS": "rq1.html",
        "10_ANALYSIS_TEMPLATES": "analysis-templates.html",
        "14_SOP_RQ1": "sop.html",
    }
    page = mapping.get(tab, "dashboard.html")
    return f"{page}#{rec_id}"


def destination_for(fname: str, sheet: str) -> str:
    key = (fname, sheet.strip())
    table = {
        ("BMGT8044_Reading_List-2.xlsx", "Sheet0"): "03_REFERENCES_MASTER",
        ("BMGT8044_Reading_List-2.xlsx", "ORIGINS_LXI"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Reading_List-2.xlsx", "Theory Academic Definition"): "04_THEORY_AND_SPINE",
        ("BMGT8044_Reading_List-2.xlsx", "REFERENCES"): "03_REFERENCES_MASTER",
        ("BMGT8044_Reading_List-2.xlsx", "KEY WORD_db"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Reading_List-2.xlsx", "Qual Tool Recco"): "06_QUAL_METHODS_AND_TOOLS",
        ("BMGT8044_Reading_List-2.xlsx", "Dissertation Spine_db"): "04_THEORY_AND_SPINE",
        ("BMGT8044_Reading_List-2.xlsx", "Reserch Preperation_db"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Reading_List-2.xlsx", "Parkinglot_"): "02_PARKING_LOT",
        ("BMGT8044_Reading_List-2.xlsx", "APA- Direct Quoting"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Reading_List-2.xlsx", "STKHLDR  MGMT"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Reading_List-2.xlsx", "Stakeholder theory"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx", "Sheet1"): "05_LEADERSHIP_ALIGNMENT",
        (
            "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
            "Data Collection Steps&Analysis",
        ): "07_SOURCE_ARCHIVE (ARCHIVE_COMPARATIVE)",
        ("BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx", "Sheet3"): "07_SOURCE_ARCHIVE",
        (
            "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
            "Qual Data Analysis Methods",
        ): "06_QUAL_METHODS_AND_TOOLS",
        (
            "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
            "Research Methods_Step7",
        ): "07_SOURCE_ARCHIVE",
        (
            "BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx",
            "Quan Data Analysis Methods",
        ): "07_SOURCE_ARCHIVE (ARCHIVE_COMPARATIVE)",
        ("BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx", "8055 Wk1"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx", "Sheet8"): "07_SOURCE_ARCHIVE",
        ("BMGT8044_Wk7_Leadership_Theories_Alignment_v01.xlsx", "Sheet9"): "06_QUAL_METHODS_AND_TOOLS",
        (
            "BMGT8044_Wk7_Leadership_Theories_Alignment_v01_formatted.xlsx",
            "Sheet1",
        ): "07_SOURCE_ARCHIVE (formatted duplicate of leadership table)",
    }
    return table.get(key, "07_SOURCE_ARCHIVE")


def notes_for(fname: str, sheet: str) -> str:
    if "formatted" in fname and sheet == "Sheet1":
        return "Near-duplicate of cleaner leadership table; retained for lineage."
    if sheet == "Data Collection Steps&Analysis":
        return "Classmate quantitative Qualtrics/regression plan; not the member study design."
    if sheet == "Quan Data Analysis Methods":
        return "Quantitative methods notes retained as comparative archive."
    return "All nonempty cells extracted to JSON."


def main() -> None:
    INVENTORY.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    inventory = {}
    summary = []
    for path in sorted(ORIGINALS.glob("*.xlsx")):
        extracted = extract_workbook(path)
        inventory[path.name] = extracted
        out = INVENTORY / f"{path.stem}.json"
        # write sheet data separately to keep files manageable
        slim = {"file": extracted["file"], "sheet_count": extracted["sheet_count"], "sheets": extracted["sheets"]}
        out.write_text(json.dumps(slim, indent=2, ensure_ascii=False), encoding="utf-8")
        for name, payload in extracted["data"].items():
            safe = re.sub(r"[^\w.-]+", "_", name).strip("_")
            (INVENTORY / f"{path.stem}__{safe}.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
        summary.append(slim)
        print(f"extracted {path.name}: {extracted['sheet_count']} sheets")

    structured = build_structured(inventory)
    (DATA / "references.json").write_text(json.dumps(structured["references"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "extra_refs.json").write_text(json.dumps(structured["extra_refs"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "themes.json").write_text(json.dumps(structured["themes"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "parking_lot.json").write_text(json.dumps(structured["parking_lot"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "theory.json").write_text(json.dumps(structured["theory"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "spine.json").write_text(json.dumps(structured["spine"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "interview_questions.json").write_text(
        json.dumps(structured["interview_questions"], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DATA / "archive.json").write_text(json.dumps(structured["archive"], ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "index.json").write_text(json.dumps(structured["index"], ensure_ascii=False), encoding="utf-8")
    (DATA / "counts.json").write_text(json.dumps(structured["counts"], indent=2), encoding="utf-8")
    (DATA / "search_history.json").write_text(
        json.dumps({"last_three": [], "note": "Browser localStorage is the live store; Excel LastSearch1-3 mirrors exports."}, indent=2),
        encoding="utf-8",
    )
    (INVENTORY / "lineage.json").write_text(json.dumps(structured["lineage"], indent=2, ensure_ascii=False), encoding="utf-8")
    (INVENTORY / "workbooks.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("counts", json.dumps(structured["counts"], indent=2))


if __name__ == "__main__":
    main()
