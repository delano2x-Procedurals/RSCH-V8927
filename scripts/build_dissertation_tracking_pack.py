#!/usr/bin/env python3
"""Build one master xlsx + one consolidated docx for dissertation document tracking."""

from __future__ import annotations

import csv
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path("/workspace")
DOCS = ROOT / "docs"
TEMPLATES = DOCS / "notion" / "templates"
OUT = ROOT / "downloads"
TODAY = "2026-09-08"
PACK_VERSION = "v1.0"
NOTION_URL = (
    "https://app.notion.com/p/8927_Amalgamation_db-3d52df1d624080149230cc6252b942c5"
    "?source=copy_link"
)

NAVY = "1F3A5F"
RUST = "9A3412"
GOLD = "C4A35A"
WHITE = "FFFFFF"
PALE = "F4F1EA"
PALE_RUST = "FBEAE6"
PALE_GREEN = "E8F0E6"
THIN = Border(
    left=Side(style="thin", color="C5C9D1"),
    right=Side(style="thin", color="C5C9D1"),
    top=Side(style="thin", color="C5C9D1"),
    bottom=Side(style="thin", color="C5C9D1"),
)
HEADER_FONT = Font(name="Calibri", bold=True, color=WHITE, size=10)
BODY_FONT = Font(name="Calibri", size=10)
BOLD_FONT = Font(name="Calibri", size=10, bold=True)
BOLD_RUST = Font(name="Calibri", size=10, bold=True, color=RUST)
WRAP = Alignment(wrap_text=True, vertical="top")


def read_csv(name: str) -> list[dict[str, str]]:
    path = TEMPLATES / name
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def style_header(ws, ncols: int):
    fill = PatternFill("solid", fgColor=NAVY)
    for col in range(1, ncols + 1):
        cell = ws.cell(1, col)
        cell.fill = fill
        cell.font = HEADER_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = THIN
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(ncols)}1"
    ws.row_dimensions[1].height = 32


def autosize(ws, widths: dict[int, int] | None = None):
    for col in range(1, ws.max_column + 1):
        w = widths.get(col) if widths else None
        if w is None:
            longest = 12
            for row in ws.iter_rows(min_col=col, max_col=col, max_row=min(ws.max_row, 40)):
                val = row[0].value
                if val:
                    longest = max(longest, min(len(str(val)), 42))
            w = longest + 2
        ws.column_dimensions[get_column_letter(col)].width = w


def write_sheet(wb, name, headers, rows, bold_if=None, widths=None, note=None):
    ws = wb.create_sheet(name)
    if note:
        ws.sheet_properties.tabColor = GOLD
    for j, h in enumerate(headers, 1):
        ws.cell(1, j, h)
    style_header(ws, len(headers))
    for i, row in enumerate(rows, 2):
        flag = False
        if bold_if:
            flag = bold_if(row)
        fill = PatternFill("solid", fgColor=PALE_RUST if flag else (PALE if i % 2 == 0 else WHITE))
        for j, h in enumerate(headers, 1):
            cell = ws.cell(i, j, row.get(h, ""))
            cell.font = BOLD_RUST if flag else BODY_FONT
            cell.alignment = WRAP
            cell.border = THIN
            cell.fill = fill
        ws.row_dimensions[i].height = 48 if flag else 36
    autosize(ws, widths)
    ws.sheet_view.showGridLines = False
    return ws


def change_rows():
    return [
        {
            "log_id": "CL-0001",
            "date": TODAY,
            "delta": "KEEP",
            "what_changed": "Locked study facts remain: GQI + CIT; n = 12; VCST on Need only; PLU operational; hybrid Fereday & Muir-Cochrane; Delve = CAQDAS only; spoken protocol ITDR-GQI-INT-v0.1.1 unchanged.",
            "why": "Change-tracking file already locked these. A tracking pack must not drift the dissertation.",
            "source": "docs/change-tracking-update.md",
            "artifact_now": "01_LIFECYCLE + 09_NEED_OV + CH3_CONTROL",
        },
        {
            "log_id": "CL-0002",
            "date": TODAY,
            "delta": "NEW",
            "what_changed": "One master workbook replaces ad-hoc use of Origins13 ROS plus scattered CSVs as the live tracker. Origins13 remains the template, not a second live codebook.",
            "why": "User asked for one xlsx. Origins philosophy is input-once / ID tracking. Duplicate live codebooks create drift.",
            "source": "Origins13_ROSv1_v1.2_ChapterIII.xlsx README/NAVIGATION",
            "artifact_now": "downloads/Dissertation_Document_Tracking_Master.xlsx",
        },
        {
            "log_id": "CL-0003",
            "date": TODAY,
            "delta": "REPLACE",
            "what_changed": "Origins CH3_CONTROL sample 10–15 is replaced in this pack by locked n = 12. Origins GQI_INTERVIEW_QS IQ-01… stems are not the spoken protocol.",
            "why": "Week 8 lock set sample at 12. Spoken wording lives in interview-items.csv (Q0, L1–L3, A–F, Q-close). Copying Origins IQ numbers would silently rewrite the instrument.",
            "source": "Origins CH3_CONTROL / GQI_INTERVIEW_QS vs docs/notion/templates/interview-items.csv",
            "artifact_now": "CH3_CONTROL + 05_INTERVIEW_ITEMS",
        },
        {
            "log_id": "CL-0004",
            "date": TODAY,
            "delta": "NEW",
            "what_changed": "Full Need overview (ITM specialization alignment + VCST placement + PQ1/PQ2) is now a first-class tracker sheet and Word section, with a weekly/daily work schedule tied to artifacts.",
            "why": "Reviewer asked for specialization/Need. User asked for OV of full Need with understood work schedules.",
            "source": "docs/chapter-i-need-for-the-study.md; workflow SOP report",
            "artifact_now": "09_NEED_OV + 10_WORK_SCHEDULE + Word §§1–3",
        },
        {
            "log_id": "CL-0005",
            "date": TODAY,
            "delta": "NEW",
            "what_changed": "Uploaded PDFs registered with allowed-use. Neville (2011) was already in the nest. Joos (2019), Khurram & Charreire Petit (2015), EMR 2023 analysis roadmap, Daniel & Daniel (2019), Christensen (2023/2024) are added.",
            "why": "User asked for updated reference materials and to see why each source changed. Course PDFs must not silently become theory spine or method.",
            "source": "Wk3/Wk8/Wk10 PDFs + Christensen + Hinkley CAS",
            "artifact_now": "03_REFERENCES + 08_PARKING_LOT + Word §5",
        },
        {
            "log_id": "CL-0006",
            "date": TODAY,
            "delta": "KEEP",
            "what_changed": "Agle et al. (1999) remains build-on empirical test of PLU. It is not replaced by Joos (2019) or Wood et al. (2021) as the definitional source.",
            "why": "Updated-references.md proposed Wood et al. (2021) as a currency swap for Agle 1999 in the Project Plan list. Codebook still needs the original empirical test as build-on, not a replacement definition.",
            "source": "docs/updated-references.md vs symbols.csv",
            "artifact_now": "03_REFERENCES (KEEP Agle 1999; NEW Wood 2021 as additional review)",
        },
        {
            "log_id": "CL-0007",
            "date": TODAY,
            "delta": "NEW",
            "what_changed": "Wood et al. (2021) added as current salience review (build_on). Does not replace Mitchell et al. (1997).",
            "why": "Currency pass for Chapter II What We Know. Operational defs stay Mitchell.",
            "source": "docs/updated-references.md",
            "artifact_now": "REF-WOOD-2021",
        },
        {
            "log_id": "CL-0008",
            "date": TODAY,
            "delta": "PARK",
            "what_changed": "Christensen (2023/2024) three concepts of power (Foucault, Bourdieu, Habermas) parked. Optional memo language for P only.",
            "why": "Educational-theory power concepts are not Mitchell’s utilitarian/coercive/normative means. Using them as codebook parents would pre-write themes and leave GQI.",
            "source": "christensen-2023-three-concepts-of-power.pdf",
            "artifact_now": "08_PARKING_LOT PL-CHRISTENSEN-2023",
        },
        {
            "log_id": "CL-0009",
            "date": TODAY,
            "delta": "PARK",
            "what_changed": "Daniel & Daniel (2019) Hinkley Point C CAS parked. Not the study design.",
            "why": "This dissertation is GQI + CIT of SME ITDRPaaS incidents, not a megaproject process/CAS model. Comparative only.",
            "source": "RSCH-v8927_wk8 Hinkley Point C PDF",
            "artifact_now": "08_PARKING_LOT PL-DANIEL-2019",
        },
        {
            "log_id": "CL-0010",
            "date": TODAY,
            "delta": "NEW",
            "what_changed": "Qual analysis SOP mapped from MD procedural package + presentation plan + Chapter III hybrid steps. Eisenhardt/Gioia/Langley templates from the EMR editorial are recorded as not-this.",
            "why": "Wk8 editorial is useful for knowing adjacent templates. This study already locked Fereday & Muir-Cochrane. Naming Gioia as the method would contradict Chapter III.",
            "source": "MD_Qualitative_Analysis_Procedural_Package; EMR editorial 2023; chapter-iii-methodology.md",
            "artifact_now": "06_ANALYSIS_SOP",
        },
        {
            "log_id": "CL-0011",
            "date": TODAY,
            "delta": "NEW",
            "what_changed": "Folder map from proposal through deposit; Notion amalgamation DB URL recorded. MCP not authenticated this session so live Notion write is pending.",
            "why": "User supplied https://app.notion.com/p/8927_Amalgamation_db-… as the nest. Repo CSV headers stay the round-trip contract.",
            "source": "User Notion link; docs/notion/README.md",
            "artifact_now": "07_FOLDER_MAP + NAVIGATION",
        },
        {
            "log_id": "CL-0012",
            "date": TODAY,
            "delta": "KEEP",
            "what_changed": "Instructor original Word and spoken interview wording are not edited.",
            "why": "source/originals/ is the instructor trail. Protocol IDs are never reused when retired.",
            "source": "source/originals/MW_Wk5_to_wk8_Edit_5Sep26.docx",
            "artifact_now": "07_FOLDER_MAP (do-not-edit row)",
        },
    ]


def lifecycle_rows():
    stages = [
        ("LC-01", "Proposal / Alignment Map", "In progress", "Project Plan nodes match locked facts", "09_NEED_OV; SPINE in Word", "Advisor packet accepted"),
        ("LC-02", "Chapter I Need / specialization / VCST", "Drafted", "Four Need paragraphs + ITM table pasted", "docs/chapter-i-need-for-the-study.md", "Need node closed; VCST not on Constructs"),
        ("LC-03", "Chapter II literature", "In progress", "Seminal keep + build-on; synthesis matrix rows", "03_REFERENCES; 08_PARKING_LOT", "Every claim has allowed-use"),
        ("LC-04", "Chapter III methodology", "Drafted", "GQI/CIT/hybrid TA/Delve-as-store", "docs/chapter-iii-methodology.md; CH3_CONTROL", "No “analyzed using Delve”"),
        ("LC-05", "IRB / ethics", "Not started", "Consent, recording, de-ID, member-check SOP", "collection-analysis-revision-packet.md §7", "IRB approval letter filed"),
        ("LC-06", "Recruitment (n = 12)", "Not started", "P## screen, 10–200 SME, 36-month incident", "RECRUITMENT rows in 10_WORK_SCHEDULE", "12 eligible consented"),
        ("LC-07", "Collection (CIT interviews)", "Not started", "60–75 min; Q0 then skip-rules", "05_INTERVIEW_ITEMS", "12 CLEAN transcripts"),
        ("LC-08", "Delve coding + interval CSV", "Not started", "STRUCTURAL + FRAMEWORK_DEDUCTIVE + BOUNDARY; EMERGENT empty until MU lock", "04_CODEBOOK; 06_ANALYSIS_SOP", "Dated backup each coded interview"),
        ("LC-09", "Chapter IV findings", "Not started", "PQ1 and PQ2 answered separately; themes are claims", "06_ANALYSIS_SOP steps 6–7", "Boundary case per construct"),
        ("LC-10", "Chapter V interpretation", "Not started", "Implications; limitations; no new theory from Christensen/CAS", "08_PARKING_LOT", "VCST not a theme title"),
        ("LC-11", "Defense / deposit", "Not started", "Final Word + this xlsx freeze + CSV nest", "07_FOLDER_MAP", "Committee sign-off"),
    ]
    rows = []
    for sid, stage, status, required, artifacts, done_when in stages:
        rows.append(
            {
                "stage_id": sid,
                "stage": stage,
                "status": status,
                "required_artifacts": required,
                "lives_in": artifacts,
                "done_when": done_when,
                "owner": "Walker",
                "blocked_by": "",
            }
        )
    return rows


def extra_refs():
    return [
        {
            "ref_id": "REF-WOOD-2021",
            "ref_class": "seminal_theory",
            "origin": "build_on",
            "citation_status": "confirmed",
            "apa": "Wood, D. J., Mitchell, R. K., Agle, B. R., & Bryan, L. M. (2021). Stakeholder identification and salience after 20 years: Progress, problems, and prospects. Business & Society, 60(1), 196–245. https://doi.org/10.1177/0007650318816522",
            "allowed_use": "Chapter II current review of salience research; does not replace Mitchell 1997 operational defs",
            "do_not_use_for": "Spoken questions; theme titles; replacing Mitchell 1997",
            "create_new": "yes",
            "link_from": "03_REFERENCES",
            "instrument_version": "ITDR-GQI-INT-v0.1.1",
            "status": "active",
            "delta": "NEW",
            "why_delta": "Currency review requested in updated-references.md. Added as additional build-on, not as a swap that deletes Agle 1999 from the codebook nest.",
        },
        {
            "ref_id": "REF-JOOS-2019",
            "ref_class": "seminal_theory",
            "origin": "build_on",
            "citation_status": "confirmed",
            "apa": "Joos, H. C. (2019). Influences on managerial perceptions of stakeholder salience: Two decades of research in review. Management Review Quarterly, 69, 3–37. https://doi.org/10.1007/s11301-018-0144-8",
            "allowed_use": "What We Know: inner/outer context that shapes how managers perceive PLU. Sensitizing only.",
            "do_not_use_for": "Replacing Mitchell 1997; adding personality variables as codebook parents; findings",
            "create_new": "yes",
            "link_from": "Wk3 PDF 8044-8927_Wk3_Influences_on_managerial_perce",
            "instrument_version": "ITDR-GQI-INT-v0.1.1",
            "status": "active",
            "delta": "NEW",
            "why_delta": "Course PDF now registered. Review of contextual influences; not a new salience attribute.",
        },
        {
            "ref_id": "REF-KHURRAM-2015",
            "ref_class": "seminal_theory",
            "origin": "build_on",
            "citation_status": "confirmed",
            "apa": "Khurram, S., & Charreire Petit, S. (2017). Investigating the dynamics of stakeholder salience: What happens when the institutional change process unfolds? Journal of Business Ethics, 143(4), 663–680. https://doi.org/10.1007/s10551-015-2766-2",
            "allowed_use": "What We Know: salience attributes can shift as institutional logic shifts. Supports mid-incident C2 probes.",
            "do_not_use_for": "Study design (this is not an institutional-change case of microfinance); theme titles",
            "create_new": "yes",
            "link_from": "Wk10 PDF Investigating the Dynamics of Stakeholder Salience",
            "instrument_version": "ITDR-GQI-INT-v0.1.1",
            "status": "active",
            "delta": "NEW",
            "why_delta": "Course PDF. Dynamics claim already implied by C2; do not import the Pakistan microfinance field as this study’s site.",
        },
        {
            "ref_id": "REF-EMR-ROADMAP-2023",
            "ref_class": "seminal_method",
            "origin": "build_on",
            "citation_status": "verify",
            "apa": "Editorial. (2023). A roadmap for data analysis in qualitative research. European Management Review, 20(2), 190–196. (Duplicate course PDF of the same editorial; authors/page run EM-RAUS230022 — confirm named editorial authors before courseroom paste.)",
            "allowed_use": "Know Eisenhardt / Gioia / Langley templates so they can be refused as this study’s method",
            "do_not_use_for": "Declaring Gioia, Eisenhardt, or Langley as the analytic method; replacing Fereday & Muir-Cochrane 2006",
            "create_new": "yes",
            "link_from": "Wk8 duplicate editorials",
            "instrument_version": "ITDR-GQI-INT-v0.1.1",
            "status": "active",
            "delta": "NEW",
            "why_delta": "Two identical PDFs collapsed to one register row. Roadmap is adjacent-method literacy, not a method swap.",
        },
        {
            "ref_id": "REF-DANIEL-2019",
            "ref_class": "comparative",
            "origin": "build_on",
            "citation_status": "confirmed",
            "apa": "Daniel, E., & Daniel, P. A. (2019). Megaprojects as complex adaptive systems: The Hinkley Point C case. International Journal of Project Management, 37(8), 1017–1033. https://doi.org/10.1016/j.ijproman.2019.05.001",
            "allowed_use": "Parking lot / comparative complexity talk only",
            "do_not_use_for": "Design; sampling; coding system; Chapter IV themes; replacing GQI",
            "create_new": "yes",
            "link_from": "Wk8 Hinkley Point C PDF",
            "instrument_version": "ITDR-GQI-INT-v0.1.1",
            "status": "parked",
            "delta": "PARK",
            "why_delta": "Nuclear megaproject CAS is not SME ITDRPaaS GQI. Parked so it cannot leak into method prose.",
        },
        {
            "ref_id": "REF-CHRISTENSEN-2023",
            "ref_class": "comparative",
            "origin": "build_on",
            "citation_status": "confirmed",
            "apa": "Christensen, G. (2024). Three concepts of power: Foucault, Bourdieu, and Habermas. Power and Education, 16(2), 182–195. https://doi.org/10.1177/17577438231187129",
            "allowed_use": "Optional P-memo language only after a concrete force/withhold/override example exists",
            "do_not_use_for": "Replacing Mitchell power; Delve parent codes; interview stems; educational-theory redesign",
            "create_new": "yes",
            "link_from": "christensen-2023 PDF",
            "instrument_version": "ITDR-GQI-INT-v0.1.1",
            "status": "parked",
            "delta": "PARK",
            "why_delta": "Three social-theory powers are not PLU. Parked to stop construct inflation.",
        },
        {
            "ref_id": "REF-TRACKING-PACK-2026",
            "ref_class": "audit_artifact",
            "origin": "audit_artifact",
            "citation_status": "confirmed",
            "apa": "Walker, M. (2026). Dissertation document tracking pack (Pack v1.0) [Unpublished research operating file]. Capella University, RSCH-V8927. downloads/Dissertation_Document_Tracking_Master.xlsx; downloads/Dissertation_Document_Tracking_Pack.docx.",
            "allowed_use": "Document control; change log; work schedule; folder map",
            "do_not_use_for": "Literature source; findings",
            "create_new": "yes",
            "link_from": "this pack",
            "instrument_version": "ITDR-GQI-INT-v0.1.1",
            "status": "active",
            "delta": "NEW",
            "why_delta": "The consolidated tracker itself is an audit artifact.",
        },
    ]


def analysis_sop_rows():
    return [
        {"step": "0", "sop_stage": "Inputs before analysis", "action": "Confirm CLEAN transcript, P##, incident named, instrument_version, signed consent.", "delve": "Import CLEAN only", "evidence": "INTERVIEW_INFRA row", "not_this": "Coding RAW files", "source": "MD procedural package §1; Chapter III data prep"},
        {"step": "1", "sop_stage": "Code manual", "action": "Import codebook.csv nest. STRUCTURAL + FRAMEWORK_DEDUCTIVE + BOUNDARY. EMERGENT empty.", "delve": "Codes import", "evidence": "04_CODEBOOK version", "not_this": "Gioia 1st-order labels as the method", "source": "Fereday & Muir-Cochrane 2006; Chapter III"},
        {"step": "2", "sop_stage": "Structural + sensitizing pass", "action": "Tag PQ1/PQ2/CONTEXT/UNANTICIPATED then P/L/U/Lev/DR/ESC/EV/RA where a concrete example or boundary exists.", "delve": "Apply nested codes; memo skip_if", "evidence": "Snippet URLs", "not_this": "Pre-named Power theme", "source": "codebook.csv; interview skip rules"},
        {"step": "3", "sop_stage": "Meaning-unit lock", "action": "Write a practice-claim sentence grounded in a named excerpt before any EMERGENT child or theme name.", "delve": "Memo on snippet", "evidence": "MU table row", "not_this": "Themes emerged", "source": "Aronson 1994; Taylor & Bogdan 1998; procedural package hierarchy correction"},
        {"step": "4", "sop_stage": "Inductive codes", "action": "Add EMERGENT children only for patterned claims the template does not already name. Do not copy power/legitimacy/urgency/leverage_location into EMERGENT.", "delve": "New child under EMERGENT", "evidence": "update-log.csv", "not_this": "Eisenhardt cross-case as default", "source": "Chapter III steps 4–5"},
        {"step": "5", "sop_stage": "Categories", "action": "Group MUs that describe the same salience-to-assurance bargain, not the same recovery topic.", "delve": "Category memo", "evidence": "Category list", "not_this": "Topic headings Governance/Power", "source": "Chapter III; presentation plan"},
        {"step": "6", "sop_stage": "Theme as claim", "action": "Name a patterned-meaning sentence with excerpts plus at least one corpus boundary/negative case.", "delve": "Theme memo after MU lock", "evidence": "THEMES sheet later; empty now", "not_this": "Frequency = importance", "source": "Braun & Clarke quality practice; Nowell 2017"},
        {"step": "7", "sop_stage": "Two answers", "action": "Write PQ1 answer (claim attention) and PQ2 answer (enactment) separately.", "delve": "n/a", "evidence": "Chapter IV outline", "not_this": "One governance theme", "source": "Chapter III step 7"},
        {"step": "8", "sop_stage": "Export / weekly nest", "action": "Export Codes + Snippets; copy templates to interval-backups/YYYY-MM-DD; append update-log (or type=no_change).", "delve": "CSV export", "evidence": "docs/notion/interval-backups", "not_this": "Overwriting codebook descriptions with a thin Delve export", "source": "docs/notion/README.md"},
        {"step": "9", "sop_stage": "Presentation", "action": "Chapter IV tables: construct → excerpt → MU → claim. Member-check is on CLEAN transcript only.", "delve": "Snippet URL in table footnote", "evidence": "Ch IV draft", "not_this": "NIST scores; CAS diagrams from Hinkley", "source": "Qualitative Data Analysis and Presentation Plan; QUAL Example4-1 analysis node"},
    ]


def folder_rows():
    return [
        {"folder": "docs/", "owns": "Paste-ready chapter prose and logs", "through_completion": "Ch I–III stay here until Word merge; Ch IV–V added later", "do_not": "Identifiable transcripts"},
        {"folder": "docs/notion/templates/", "owns": "Canonical CSV headers (round-trip to Notion)", "through_completion": "Edit here, then dated backup", "do_not": "Rename linking keys"},
        {"folder": "docs/notion/interval-backups/", "owns": "Dated codebook/items/refs snapshots", "through_completion": "After each coded interview + weekly", "do_not": "PII"},
        {"folder": "workspace-app/", "owns": "Local HTML nest of the same IDs", "through_completion": "Optional viewer; not the audit original", "do_not": "A second codebook"},
        {"folder": "source/originals/", "owns": "Instructor Word and original xlsx", "through_completion": "Never overwrite", "do_not": "Silent edits"},
        {"folder": "source/inventory/", "owns": "JSON extracts / lineage", "through_completion": "Provenance only", "do_not": "Live interview IDs"},
        {"folder": "downloads/", "owns": "Courseroom Word + THIS pack", "through_completion": "Upload Tracking_Pack.docx; keep Master.xlsx as operating file", "do_not": "Replace instructor original"},
        {"folder": "scripts/", "owns": "export_docx.py; this builder", "through_completion": "Regenerate pack after CSV edits", "do_not": "Hand-edit generated xlsx as the only copy of IDs — edit CSVs first"},
        {"folder": "Notion 8927_Amalgamation_db", "owns": NOTION_URL, "through_completion": "One DB per CSV header when MCP is connected", "do_not": "A second codebook; identifiable data"},
    ]


def parking_rows():
    return [
        {
            "park_id": "PL-CHRISTENSEN-2023",
            "item": "Foucault / Bourdieu / Habermas power",
            "why_parked": "Different concept of power than Mitchell’s capacity to force, withhold, or override in a named incident.",
            "allowed_later": "Optional P memo after a concrete override example",
            "never": "Delve parent; spoken stem; Ch IV heading",
            "ref_id": "REF-CHRISTENSEN-2023",
        },
        {
            "park_id": "PL-DANIEL-2019",
            "item": "Hinkley Point C as complex adaptive system",
            "why_parked": "Megaproject process model; not GQI of SME ITDRPaaS incidents.",
            "allowed_later": "Ch V limitation / adjacent complexity sentence if needed",
            "never": "Design; sampling; coding",
            "ref_id": "REF-DANIEL-2019",
        },
        {
            "park_id": "PL-EMR-TEMPLATES-2023",
            "item": "Eisenhardt / Gioia / Langley analysis templates",
            "why_parked": "Useful literacy; locked method is hybrid codebook TA.",
            "allowed_later": "Chapter III ‘why not adjacent methods’ table",
            "never": "Replacing Fereday & Muir-Cochrane",
            "ref_id": "REF-EMR-ROADMAP-2023",
        },
        {
            "park_id": "PL-ORIGINS-IQ",
            "item": "Origins GQI_INTERVIEW_QS IQ-01… wording",
            "why_parked": "Template stems, not the approved spoken protocol.",
            "allowed_later": "Historical comparison only",
            "never": "Live interview",
            "ref_id": "REF-WALKER-2026-INSTRUMENT",
        },
        {
            "park_id": "PL-ORIGINS-N-10-15",
            "item": "Origins sample 10–15",
            "why_parked": "Week 8 locked n = 12.",
            "allowed_later": "Information-power discussion may still cite Malterud; the operating n is 12",
            "never": "Reopening n as a range in the Project Plan",
            "ref_id": "REF-MALTERUD-2016",
        },
    ]


def need_rows():
    return [
        {"block_id": "N-01", "node": "Specialization", "paste_status": "Ready", "text": "PhD in Business Management, Information Technology Management (Capella University, 2024). The object of study is IT-management governance of competing recovery claims on ITDRPaaS, not a restore script."},
        {"block_id": "N-02", "node": "Foundation theory", "paste_status": "Locked", "text": "Stakeholder-claim management and corporate objective: Donaldson & Preston (1995); Freeman et al. (2004). Do not replace."},
        {"block_id": "N-03", "node": "Needed construct (VCST)", "paste_status": "Ready — Need/What We Know only", "text": "Freeman, Phillips, & Sisodia (2020) value-creation stakeholder theory: cooperative value creation and trade; apparent tensions with strategic-technical narratives. Not a Delve code, spoken stem, or Ch IV title."},
        {"block_id": "N-04", "node": "Operational lens", "paste_status": "Locked on Constructs", "text": "Mitchell et al. (1997) power, legitimacy, urgency. Leverage is enacted combination, not a fourth attribute."},
        {"block_id": "N-05", "node": "Gap / why now", "paste_status": "Ready", "text": "Unknown is operational: how SME IT managers translate mid-incident salience shifts into decision rights, escalation, and evidentiary standards inside ITDRPaaS (Dorobantu et al., 2024; Mitchell et al., 1997)."},
        {"block_id": "N-06", "node": "PQ1", "paste_status": "Implied until official RQ locks", "text": "How do U.S. SME IT and network managers describe stakeholder-claim management and salience shifts (power, legitimacy, urgency) during ITDRPaaS recovery or testing incidents?"},
        {"block_id": "N-07", "node": "PQ2", "paste_status": "Implied until official RQ locks", "text": "How do those shifts get enacted as decision rights, escalation pathways, and evidentiary / recoverability-assurance standards that managers can defend to stakeholders?"},
        {"block_id": "N-08", "node": "Who needs the study", "paste_status": "Ready", "text": "SME IT/network managers who must defend restoration; executives/customers/providers whose claims compete; IT-management scholarship lacking an incident-level enactment account."},
        {"block_id": "N-09", "node": "Unit of analysis", "paste_status": "Locked", "text": "One U.S. SME IT/network/systems/infrastructure/operations manager; one named disruption, failover, test, or operational recovery in 36 months using external/managed recovery; firm 10–200 personnel; n = 12; interviews only."},
    ]


def schedule_rows():
    return [
        {"cadence": "Daily", "block": "Writing (20–60 min)", "clock": "First protected block", "artifact": "Current lifecycle stage prose (now: Ch I Need paste / Ch II synthesis)", "metric": "200–300 words or one locked paragraph", "source": "Boice/Martin via workflow report"},
        {"cadence": "Daily", "block": "Structured reading", "clock": "Second block 30–60 min", "artifact": "03_REFERENCES row + note in literature matrix when a source is actually read", "metric": "1 source with allowed-use filled", "source": "Workflow synthesis matrix"},
        {"cadence": "Daily", "block": "Microbreaks", "clock": "20s every 20–30 min; 5–10 min hourly", "artifact": "None (health SOP)", "metric": "Stand/stretch logged if pain flare", "source": "Workflow ergonomics"},
        {"cadence": "Daily", "block": "End-of-day log", "clock": "Last 10 min", "artifact": "00_CHANGE_LOG only if a register actually changed; else skip", "metric": "Tomorrow’s 3 tasks written", "source": "PDCA"},
        {"cadence": "Weekly", "block": "Sprint review", "clock": "Sunday / Friday close", "artifact": "01_LIFECYCLE status; 10_WORK_SCHEDULE checkboxes", "metric": "Pages/sections vs plan; n of sources added", "source": "Workflow weekly review"},
        {"cadence": "Weekly", "block": "Instrument / codebook freeze check", "clock": "If any wording temptation", "artifact": "05_INTERVIEW_ITEMS status must stay active; bump version BEFORE any spoken change", "metric": "Spoken text unchanged unless version bump", "source": "docs/notion/README.md"},
        {"cadence": "Weekly (coding phase)", "block": "Interval CSV backup", "clock": "After each coded interview, else weekly no_change", "artifact": "docs/notion/interval-backups/YYYY-MM-DD/", "metric": "update-log row exists", "source": "notion README"},
        {"cadence": "Weekly", "block": "Accountability", "clock": "Advisor or writing group", "artifact": "Need OV + one appendix table from this xlsx", "metric": "One external share", "source": "Workflow accountability"},
        {"cadence": "Per interview", "block": "Collection day", "clock": "60–75 min + same-day de-ID", "artifact": "CLEAN transcript; leverage-memo headers; artifact path A/B/C", "metric": "Recorder file + P## row", "source": "Revision packet protocol"},
        {"cadence": "Monthly", "block": "Chapter tracker", "clock": "Last weekend", "artifact": "01_LIFECYCLE vs Capella QUAL Example4-1 nodes", "metric": "Each Project Plan heading has a status", "source": "Project_Plan_QUAL_Example4-1.docx"},
        {"cadence": "IRB gate", "block": "No recruitment before approval", "clock": "Hard gate", "artifact": "LC-05", "metric": "Approval letter", "source": "Chapter III ethics"},
        {"cadence": "Defense gate", "block": "Freeze pack", "clock": "Pre-deposit", "artifact": "xlsx + docx + CSV nest dated", "metric": "No live edits after freeze tag", "source": "This pack"},
    ]


def ch3_control_rows():
    return [
        {"control_area": "Study design", "locked_specification": "Generic qualitative inquiry (GQI)", "why_locked": "Accounts of events/decisions/artifacts, not essence", "status": "Locked", "delta": "KEEP"},
        {"control_area": "Interview stance", "locked_specification": "Critical incident technique", "why_locked": "Named 36-month ITDRPaaS event", "status": "Locked", "delta": "KEEP"},
        {"control_area": "Analytic method", "locked_specification": "Hybrid deductive–inductive codebook TA (Fereday & Muir-Cochrane, 2006)", "why_locked": "Need RQ map + versioned codebook", "status": "Locked", "delta": "KEEP"},
        {"control_area": "CAQDAS", "locked_specification": "Delve stores; Delve does not analyze", "why_locked": "Stop software-as-method", "status": "Locked", "delta": "KEEP"},
        {"control_area": "Sample", "locked_specification": "n = 12 (not a range)", "why_locked": "Week 8 courseroom lock", "status": "Locked", "delta": "REPLACE vs Origins 10–15"},
        {"control_area": "SME size", "locked_specification": "10–200 personnel; SBA <500 is federal bound only", "why_locked": "Study screen tighter than SBA", "status": "Locked", "delta": "KEEP"},
        {"control_area": "Collection", "locked_specification": "Interviews only", "why_locked": "No NIST/ISO scoring; artifacts optional Path A/B/C", "status": "Locked", "delta": "KEEP"},
        {"control_area": "VCST", "locked_specification": "Need / What We Know only", "why_locked": "Foundation construct; not PLU", "status": "Locked", "delta": "KEEP"},
        {"control_area": "Spoken protocol", "locked_specification": "ITDR-GQI-INT-v0.1.1", "why_locked": "Wording freeze", "status": "Locked", "delta": "KEEP vs Origins IQ-01"},
        {"control_area": "Paradigm language", "locked_specification": "GQI interpretive; not phenomenology wording", "why_locked": "Language-drift list", "status": "Locked", "delta": "KEEP"},
    ]


def build_workbook(path: Path):
    wb = Workbook()
    # README
    ws = wb.active
    ws.title = "README"
    intro = [
        ["Dissertation Document Tracking Master", PACK_VERSION, TODAY],
        ["Study", "GQI of U.S. SME IT/network managers’ ITDRPaaS governance", "Walker / RSCH-V8927"],
        ["Template parent", "Origins13_ROSv1_v1.2 Chapter III ROS", "Input once. Organize once. Reuse by ID."],
        ["Companion Word", "downloads/Dissertation_Document_Tracking_Pack.docx", "Bold = NEW/REPLACE/why"],
        ["Notion nest (pending MCP auth)", NOTION_URL, "CSV headers must match"],
        [],
        ["Rule", "Detail"],
        ["Do not duplicate", "CSVs in docs/notion/templates/ remain canonical for interview/codebook IDs. This workbook is the operating view + change log."],
        ["Do not edit", "source/originals/; spoken_text in 05_INTERVIEW_ITEMS without a version bump"],
        ["Bold rows", "delta = NEW, REPLACE, or PARK in 00_CHANGE_LOG and 03_REFERENCES"],
        ["Primary chain", "SAL (P/L/U) → Lev → DR → ESC → EV → RA  |  VCST stays on Need"],
    ]
    for r in intro:
        ws.append(r)
    ws["A1"].font = Font(name="Calibri", bold=True, size=16, color=NAVY)
    for row in ws.iter_rows(min_row=1, max_row=12, max_col=3):
        for c in row:
            c.alignment = WRAP
            if not (c.font and c.font.bold):
                c.font = BODY_FONT
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 88
    ws.column_dimensions["C"].width = 40
    ws.sheet_properties.tabColor = NAVY

    nav_headers = ["order", "group", "sheet", "purpose", "action"]
    nav_rows = [
        {"order": 1, "group": "Governance", "sheet": "README", "purpose": "Operating rules", "action": "VIEW"},
        {"order": 2, "group": "Governance", "sheet": "NAVIGATION", "purpose": "This list", "action": "VIEW"},
        {"order": 3, "group": "Audit", "sheet": "00_CHANGE_LOG", "purpose": "What/why deltas; bold NEW/REPLACE/PARK", "action": "READ FIRST"},
        {"order": 4, "group": "Lifecycle", "sheet": "01_LIFECYCLE", "purpose": "Proposal → deposit", "action": "UPDATE STATUS"},
        {"order": 5, "group": "Lock", "sheet": "CH3_CONTROL", "purpose": "Locked Ch III specs (n=12)", "action": "VIEW / CONTROL"},
        {"order": 6, "group": "Need", "sheet": "09_NEED_OV", "purpose": "Full Need / ITM / VCST / PQs", "action": "PASTE SOURCE"},
        {"order": 7, "group": "Schedule", "sheet": "10_WORK_SCHEDULE", "purpose": "Daily/weekly/monthly SOP", "action": "USE"},
        {"order": 8, "group": "Constructs", "sheet": "02_CONSTRUCT_INDEX", "purpose": "PQ × question × code", "action": "VIEW"},
        {"order": 9, "group": "Constructs", "sheet": "02b_SYMBOLS", "purpose": "P L U Lev DR ESC EV RA VCST defs", "action": "VIEW"},
        {"order": 10, "group": "Literature", "sheet": "03_REFERENCES", "purpose": "Merged register + new PDFs", "action": "APPEND BY ID"},
        {"order": 11, "group": "Analysis", "sheet": "04_CODEBOOK", "purpose": "Delve start-list", "action": "VERSION"},
        {"order": 12, "group": "Collection", "sheet": "05_INTERVIEW_ITEMS", "purpose": "Spoken protocol", "action": "FREEZE"},
        {"order": 13, "group": "Analysis", "sheet": "06_ANALYSIS_SOP", "purpose": "Fereday hybrid + package steps", "action": "FOLLOW"},
        {"order": 14, "group": "System", "sheet": "07_FOLDER_MAP", "purpose": "Folders through completion", "action": "VIEW"},
        {"order": 15, "group": "Boundary", "sheet": "08_PARKING_LOT", "purpose": "Christensen, CAS, Gioia, Origins IQ", "action": "DO NOT PROMOTE"},
        {"order": 16, "group": "Collection", "sheet": "11_LEVERAGE_MEMO", "purpose": "Header-only until P01", "action": "FILL AFTER INTERVIEW"},
        {"order": 17, "group": "Audit", "sheet": "12_UPDATE_LOG", "purpose": "CSV nest history + this pack", "action": "APPEND"},
        {"order": 18, "group": "Offering", "sheet": "13_SOP", "purpose": "Daily/weekly/stage SOP for this offering", "action": "FOLLOW"},
        {"order": 19, "group": "Offering", "sheet": "14_SUCCESS", "purpose": "Abstract-to-success gates vs prior outputs", "action": "VIEW"},
    ]
    write_sheet(wb, "NAVIGATION", nav_headers, nav_rows)

    cl_headers = ["log_id", "date", "delta", "what_changed", "why", "source", "artifact_now"]
    write_sheet(
        wb,
        "00_CHANGE_LOG",
        cl_headers,
        change_rows(),
        bold_if=lambda r: r["delta"] in {"NEW", "REPLACE", "PARK"},
        widths={1: 12, 2: 14, 3: 12, 4: 55, 5: 45, 6: 40, 7: 36},
    )

    write_sheet(
        wb,
        "01_LIFECYCLE",
        ["stage_id", "stage", "status", "required_artifacts", "lives_in", "done_when", "owner", "blocked_by"],
        lifecycle_rows(),
        widths={1: 12, 2: 36, 3: 14, 4: 40, 5: 36, 6: 32, 7: 12, 8: 18},
    )

    write_sheet(
        wb,
        "CH3_CONTROL",
        ["control_area", "locked_specification", "why_locked", "status", "delta"],
        ch3_control_rows(),
        bold_if=lambda r: "REPLACE" in r["delta"],
        widths={1: 22, 2: 55, 3: 40, 4: 12, 5: 28},
    )

    write_sheet(
        wb,
        "09_NEED_OV",
        ["block_id", "node", "paste_status", "text"],
        need_rows(),
        widths={1: 12, 2: 28, 3: 28, 4: 90},
    )

    write_sheet(
        wb,
        "10_WORK_SCHEDULE",
        ["cadence", "block", "clock", "artifact", "metric", "source"],
        schedule_rows(),
        widths={1: 22, 2: 32, 3: 28, 4: 55, 5: 36, 6: 32},
    )

    constructs = read_csv("construct-index.csv")
    write_sheet(wb, "02_CONSTRUCT_INDEX", list(constructs[0].keys()), constructs)

    symbols = read_csv("symbols.csv")
    write_sheet(wb, "02b_SYMBOLS", list(symbols[0].keys()), symbols, widths={i: 22 for i in range(1, 8)} | {4: 40, 5: 40, 6: 28, 7: 36})

    refs = read_csv("references.csv")
    for r in refs:
        r["delta"] = "KEEP"
        r["why_delta"] = "Already in the GQI nest. Seminal/build-on rules unchanged."
    refs.extend(extra_refs())
    ref_headers = list(refs[0].keys())
    write_sheet(
        wb,
        "03_REFERENCES",
        ref_headers,
        refs,
        bold_if=lambda r: r.get("delta") in {"NEW", "REPLACE", "PARK"},
        widths={1: 26, 2: 18, 3: 14, 4: 14, 5: 55, 6: 36, 7: 28, 12: 12, 13: 40},
    )

    codebook = read_csv("codebook.csv")
    write_sheet(wb, "04_CODEBOOK", list(codebook[0].keys()), codebook)

    items = read_csv("interview-items.csv")
    write_sheet(wb, "05_INTERVIEW_ITEMS", list(items[0].keys()), items, widths={5: 55, 6: 28})

    write_sheet(
        wb,
        "06_ANALYSIS_SOP",
        ["step", "sop_stage", "action", "delve", "evidence", "not_this", "source"],
        analysis_sop_rows(),
        widths={1: 8, 2: 26, 3: 50, 4: 22, 5: 22, 6: 28, 7: 36},
    )

    write_sheet(
        wb,
        "07_FOLDER_MAP",
        ["folder", "owns", "through_completion", "do_not"],
        folder_rows(),
        widths={1: 36, 2: 40, 3: 45, 4: 36},
    )

    write_sheet(
        wb,
        "08_PARKING_LOT",
        ["park_id", "item", "why_parked", "allowed_later", "never", "ref_id"],
        parking_rows(),
        bold_if=lambda r: True,
        widths={1: 24, 2: 40, 3: 45, 4: 36, 5: 32, 6: 26},
    )

    lev = read_csv("leverage-memo.csv")
    write_sheet(wb, "11_LEVERAGE_MEMO", list(lev[0].keys()), lev)

    ulog = read_csv("update-log.csv")
    if not any(r.get("log_id") == "UL-0005" for r in ulog):
        ulog.append(
            {
                "log_id": "UL-0005",
                "timestamp_utc": "2026-09-08T02:30:00Z",
                "type": "pack_create",
                "instrument_version": "ITDR-GQI-INT-v0.1.1",
                "changed_by": "researcher",
                "files_touched": "downloads/Dissertation_Document_Tracking_Master.xlsx; downloads/Dissertation_Document_Tracking_Pack.docx; docs/notion/templates/references.csv; docs/notion/templates/update-log.csv",
                "summary": "Consolidated tracking pack. Spoken wording unchanged. New PDF refs + parking lot. Sample remains 12.",
                "delve_export": "N",
                "backup_folder": "docs/notion/templates",
            }
        )
    write_sheet(wb, "12_UPDATE_LOG", list(ulog[0].keys()), ulog, widths={6: 50, 7: 50})

    sop_rows = [
        {"id": "SOP-D1", "cadence": "Daily", "step": "Three-task plan + writing 20–60 min", "artifact": "Current 01_LIFECYCLE stage", "stop_rule": "No mid-session edit"},
        {"id": "SOP-D2", "cadence": "Daily", "step": "Read one source; fill allowed-use", "artifact": "03_REFERENCES", "stop_rule": "Parked sources stay parked"},
        {"id": "SOP-W1", "cadence": "Weekly", "step": "Change log then lifecycle; confirm n=12 and v0.1.1", "artifact": "00_CHANGE_LOG; CH3_CONTROL", "stop_rule": "Need markdown wins if Word drifted"},
        {"id": "SOP-W2", "cadence": "Weekly (coding)", "step": "Interval backup or no_change", "artifact": "docs/notion/interval-backups", "stop_rule": "Do not overwrite codebook descriptions"},
        {"id": "SOP-G1", "cadence": "IRB gate", "step": "Consent / de-ID / member-check ready", "artifact": "revision packet §7", "stop_rule": "No recruitment"},
        {"id": "SOP-I1", "cadence": "Interview day", "step": "Q0 first; skip-rules; CLEAN same day", "artifact": "05_INTERVIEW_ITEMS; P##", "stop_rule": "No memory-only session; no codebook words in stems"},
        {"id": "SOP-A1", "cadence": "Analysis", "step": "MU lock before EMERGENT; two PQ answers", "artifact": "06_ANALYSIS_SOP", "stop_rule": "Not Gioia; not analyzed-using-Delve"},
    ]
    write_sheet(wb, "13_SOP", ["id", "cadence", "step", "artifact", "stop_rule"], sop_rows, widths={1: 10, 2: 18, 3: 48, 4: 36, 5: 40})

    success_rows = [
        {"outcome": "Need placed", "prior_output": "chapter-i-need-for-the-study.md", "pass": "VCST on Need only; ITM alignment pasted", "fail": "VCST as Delve code or theme title"},
        {"outcome": "Gap operational", "prior_output": "PQ1 / PQ2 in Need + Ch III", "pass": "Two Chapter IV answers", "fail": "One governance theme"},
        {"outcome": "Trail inspectable", "prior_output": "notion templates + update-log", "pass": "Every change has an ID and log row", "fail": "Second live codebook"},
        {"outcome": "Gates honored", "prior_output": "CH3_CONTROL; parking lot", "pass": "n=12; v0.1.1; IRB before recruit; parked stays parked", "fail": "Origins IQ-01 or n=10–15 reopened"},
        {"outcome": "Offering done (Wk 10)", "prior_output": "tracking pack xlsx + docx", "pass": "One xlsx + one Word show locks, Need OV, schedule, next status", "fail": "Treating this SOP as a new study"},
    ]
    write_sheet(wb, "14_SUCCESS", ["outcome", "prior_output", "pass", "fail"], success_rows, widths={1: 22, 2: 36, 3: 48, 4: 40})

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path, refs


# ----- Word -----
NEW_COLOR = RGBColor(0x9A, 0x34, 0x12)
NAVY_RGB = RGBColor(0x1F, 0x3A, 0x5F)


def set_run_font(run, *, bold=None, italic=None, size=12, color=None):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_runs(paragraph, text, *, size=12, bold=False, italic=False, color=None):
    run = paragraph.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic, color=color)


def style_p(p, *, after=6, before=0, align=None, double=True):
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    if double:
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        p.paragraph_format.line_spacing = 2.0
    if align:
        p.alignment = align
    return p


def heading(doc, text, level=1, new=False):
    p = doc.add_paragraph()
    style_p(p, after=8, before=12)
    color = NEW_COLOR if new else NAVY_RGB
    add_runs(p, text, size={1: 16, 2: 14, 3: 12}.get(level, 12), bold=True, color=color)
    return p


def para(doc, text, *, bold=False, italic=False, color=None):
    p = doc.add_paragraph()
    style_p(p)
    add_runs(p, text, bold=bold, italic=italic, color=color)
    return p


def mixed_para(doc, parts):
    """parts: list of (text, bold)."""
    p = doc.add_paragraph()
    style_p(p)
    for text, bold in parts:
        add_runs(p, text, bold=bold, color=NEW_COLOR if bold else None)
    return p


def add_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            add_runs(p, val, size=10, bold=(i == 0) or val.startswith("NEW") or val.startswith("REPLACE") or val.startswith("PARK"))
    doc.add_paragraph()


def build_docx(path: Path, refs: list[dict]):
    doc = Document()
    sec = doc.sections[0]
    for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, m, Inches(1))
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = hp.add_run("Walker — RSCH-V8927 / BMGT-8044 — Tracking Pack v1.0")
    set_run_font(r, size=10, italic=True)

    for line, kw in [
        ("Max D. Walker", dict(bold=True, size=12)),
        ("Capella University", dict(size=12)),
        ("RSCH-V8927 Doctoral Project Development — Framework Development", dict(size=12)),
        ("Information Technology Management specialization", dict(size=12, italic=True)),
    ]:
        p = doc.add_paragraph()
        style_p(p, after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        add_runs(p, line, **kw)
    p = doc.add_paragraph()
    style_p(p, after=18, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_runs(p, "Dissertation Document Tracking Pack", size=16, bold=True, color=NAVY_RGB)
    p = doc.add_paragraph()
    style_p(p, after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_runs(p, "One companion Excel file. Bold marks what changed and why.", size=12, italic=True)

    para(
        doc,
        "Companion workbook: downloads/Dissertation_Document_Tracking_Master.xlsx (Origins13 ROS template + live GQI CSV nest). Notion amalgamation database (write pending authentication): "
        + NOTION_URL,
        italic=True,
    )

    heading(doc, "1. Purpose and locked study facts")
    para(
        doc,
        "This pack is a document-control system that tracks the dissertation from the current constructs and folders through Chapter V and deposit. It is not a new method, not a new codebook, and not a new spoken protocol.",
    )
    add_table(
        doc,
        [
            ["Item", "Locked value"],
            ["Program / specialization", "PhD in Business Management, Information Technology Management"],
            ["Method", "GQI; critical-incident interviews"],
            ["n", "12 (not a range)"],
            ["Unit", "One U.S. SME IT/network/systems/infrastructure/operations manager; one named 36-month external-recovery incident; firm 10–200"],
            ["Collection", "Interviews only. No NIST/ISO/BCM scoring"],
            ["Foundation theory", "Donaldson & Preston (1995); Freeman et al. (2004)"],
            ["Needed construct", "VCST — Freeman, Phillips, & Sisodia (2020) — Need / What We Know only"],
            ["Operational lens", "Mitchell et al. (1997) P, L, U; Lev is enacted combination"],
            ["Analytic method", "Hybrid codebook thematic analysis (Fereday & Muir-Cochrane, 2006)"],
            ["CAQDAS", "Delve stores; Delve does not analyze"],
            ["Instrument", "ITDR-GQI-INT-v0.1.1 (spoken text unchanged)"],
        ],
    )

    heading(doc, "2. What changed and why", new=True)
    para(
        doc,
        "Read this section before using any new source. Bold labels are NEW (added to the nest), REPLACE (a prior operating spec is superseded in this pack only), PARK (registered so it cannot leak into method), or KEEP.",
        italic=True,
    )
    cl_tbl = [["ID", "Delta", "What changed", "Why"]]
    for r in change_rows():
        cl_tbl.append([r["log_id"], r["delta"], r["what_changed"][:220], r["why"][:180]])
    add_table(doc, cl_tbl)
    mixed_para(
        doc,
        [
            ("REPLACE vs Origins: ", True),
            ("the live sample is 12, not Origins’ 10–15. The live questions are Q0/L/A–F/Q-close, not Origins IQ-01 stems. ", False),
            ("NEW: ", True),
            ("Need overview + work schedule sheets. ", False),
            ("PARK: ", True),
            ("Christensen’s three powers, Hinkley CAS, and Eisenhardt/Gioia/Langley templates.", False),
        ],
    )

    heading(doc, "3. Full Need overview")
    para(
        doc,
        "This study is undertaken in the Doctor of Philosophy in Business Management program with a specialization in Information Technology Management. That specialization advances the theory and practice of leading information-technology strategic planning and management in complex environments. The proposed project aligns with that specialization because the object of study is an IT-management governance problem: how U.S. SME IT and network managers handle competing recovery claims, allocate decision rights, escalate contested choices, and defend restoration when disaster recovery is delivered on an external platform (ITDRPaaS).",
    )
    mixed_para(
        doc,
        [
            ("Needed construct (this update, Need / What We Know only): ", True),
            ("value-creation stakeholder theory (Freeman, Phillips, & Sisodia, 2020). Distinctive stakeholder work describes human actors cooperatively engaged in value creation and trade. In an ITDRPaaS incident those actors include executives, customers, providers, regulators, and the IT managers who must decide whose claim moves restore order. Stakeholder-salience theory then supplies the middle-range attention mechanism: power, legitimacy, and urgency (Mitchell et al., 1997).", False),
        ],
    )
    para(
        doc,
        "What remains unknown is operational rather than definitional. The literature already states that claims must be managed and that salience directs attention. It does not yet show how SME IT managers translate mid-incident salience shifts into decision rights, escalation pathways, and evidentiary standards inside ITDRPaaS when disruption forces time-critical choices. That unknown sits inside Information Technology Management.",
    )
    para(
        doc,
        "PQ1. How do U.S. SME IT and network managers describe stakeholder-claim management and salience shifts (power, legitimacy, urgency) during ITDRPaaS recovery or testing incidents? PQ2. How do those shifts get enacted as decision rights, escalation pathways, and evidentiary / recoverability-assurance standards that managers can defend to stakeholders?",
    )
    add_table(
        doc,
        [
            ["Specialization demand", "How this project aligns"],
            ["Lead IT strategic planning in complex environments", "ITDRPaaS is provider-dependent recovery; unit is one named incident"],
            ["Collaborative relationships among IT and other leaders", "PQ1: whose claim moved restore order and what supplied that pull"],
            ["IT policies and processes", "PQ2: decision rights, escalation, enough proof"],
            ["Ethical/legal IT management; practical solutions", "Recoverability assurance as reviewable evidence, not a compliance score"],
        ],
    )

    heading(doc, "4. Document-tracking SOP and work schedule", new=True)
    para(
        doc,
        "The workflow report’s daily writing, structured reading, and weekly PDCA are bound here to this study’s artifacts. Do not invent a second task app as the system of record; the xlsx plus the CSV nest is the system of record.",
    )
    add_table(
        doc,
        [
            ["Cadence", "Block", "Tied artifact", "Done when"],
            ["Daily", "20–60 min writing, no mid-session edit", "Current lifecycle stage (now Need/Ch II)", "200–300 words or one locked paragraph"],
            ["Daily", "30–60 min structured reading", "03_REFERENCES allowed-use", "One source row complete"],
            ["Daily", "Microbreaks / stand", "Health SOP (not a chapter)", "Hourly movement"],
            ["Weekly", "Sprint review", "01_LIFECYCLE status", "Three next tasks written"],
            ["Weekly (coding)", "Interval backup or no_change", "docs/notion/interval-backups", "update-log row"],
            ["Per interview", "60–75 min CIT + same-day CLEAN", "05_INTERVIEW_ITEMS; P##", "Recorder file exists"],
            ["IRB gate", "No recruitment", "LC-05", "Approval letter"],
            ["Monthly", "Map to QUAL Example4-1 headings", "Project Plan nodes", "Each heading has status"],
        ],
    )
    mixed_para(
        doc,
        [
            ("NEW schedule rule: ", True),
            ("spoken protocol is not a weekly rewrite target. If wording must change, bump instrument_version first, retire the old question_id, never reuse it.", False),
        ],
    )

    heading(doc, "5. Construct and folder map")
    para(
        doc,
        "Primary chain: P / L / U (Mitchell) → Lev (enacted combination) → DR → ESC → EV → RA. VCST sits behind Need only. Folders: docs/ (prose), docs/notion/templates/ (canonical CSVs), interval-backups/ (dated), source/originals/ (do not edit), downloads/ (this pack), workspace-app/ (viewer, not original), Notion amalgamation DB when authenticated.",
    )
    add_table(
        doc,
        [
            ["Symbol", "Spoken stand-in", "Delve code", "Not this"],
            ["P", "request; pressure; delay; override; stop", "power", "Power as a theme title; Foucault/Bourdieu/Habermas as parents"],
            ["L", "right to ask; out of line", "legitimacy", "NIST scoring"],
            ["U", "time-critical; time pressure", "urgency", "Spoken ‘urgency’ unless participant said it"],
            ["Lev", "who moved / who could have stopped it", "leverage_location", "Fourth salience attribute"],
            ["DR / ESC / EV / RA", "supposed vs actual; trigger; enough proof; what would you point to", "decision_rights / escalation / evidentiary_standards / recoverability_assurance", "A priori Ch IV headings"],
        ],
    )

    heading(doc, "6. Updated reference materials", new=True)
    para(
        doc,
        "After paste, select the list → Paragraph → Special: Hanging 0.5 in. Bold entries are NEW or PARK in this pack. KEEP rows are already confirmed in the nest.",
        italic=True,
    )
    para(doc, "KEEP (do not replace definitions): Mitchell et al. (1997); Donaldson and Preston (1995); Freeman et al. (2004); Freeman, Phillips, and Sisodia (2020); Flanagan (1954); Chell (2004) / Gremler (2004) as U.S. CIT application; Caelli et al. (2003); Kahlke (2014); Percy et al. (2015); Fereday and Muir-Cochrane (2006); Lincoln and Guba (1985); Malterud et al. (2016). Neville et al. (2011) remains build-on for urgency-as-amplifier; it does not drop urgency from the instrument.")
    heading(doc, "6.1 NEW and PARK register rows", level=2, new=True)
    for r in refs:
        if r.get("delta") in {"NEW", "PARK", "REPLACE"}:
            p = doc.add_paragraph()
            style_p(p)
            add_runs(p, f"{r['delta']}. ", bold=True, color=NEW_COLOR)
            add_runs(p, r["apa"] + " Allowed use: " + r["allowed_use"] + " Why: " + r.get("why_delta", ""))
    heading(doc, "6.2 KEEP nest (short list)", level=2)
    para(
        doc,
        "Full APA lines remain on 03_REFERENCES. Do not balloon the Project Plan list: Joos (2019) and Khurram and Charreire Petit (2015/2017) are What We Know build-on for managerial perception and shifting attributes. The EMR 2023 editorial is method-literacy only. Duplicate Wk8 roadmap PDFs are one row.",
    )

    heading(doc, "7. Analysis and presentation procedure")
    para(
        doc,
        "Follow 06_ANALYSIS_SOP. Hierarchy correction from the MD procedural package remains: codes are not themes; lock meaning units before theme names; stakeholder-salience constructs are sensitizing probes. Presentation in Chapter IV is two answers (PQ1, PQ2) with excerpt → MU → claim tables and a required boundary case per construct. Member-check is on the CLEAN transcript, not on theme titles.",
    )
    mixed_para(
        doc,
        [
            ("Not this (Wk8 editorial): ", True),
            ("do not switch the analytic method to Gioia, Eisenhardt multiple-case, or Langley process templates. Those names stay in the parking lot so Chapter III can say why they were refused.", False),
        ],
    )

    heading(doc, "8. How to use the companion xlsx")
    para(
        doc,
        "Open README, then 00_CHANGE_LOG (bold rows first), then 09_NEED_OV and 10_WORK_SCHEDULE. Update 01_LIFECYCLE status only. Add literature as a new REF-ID on 03_REFERENCES; do not paste a second bibliography into Word without the ID. After interviews, fill 11_LEVERAGE_MEMO and export Delve to the dated CSV nest. Rebuild this pack with scripts/build_dissertation_tracking_pack.py if CSV templates change.",
    )

    heading(doc, "9. Parking lot and not-this rules", new=True)
    add_table(
        doc,
        [
            ["Park ID", "Item", "Never"],
            ["PL-CHRISTENSEN-2023", "Three concepts of power", "Delve parents; spoken stems; Ch IV headings"],
            ["PL-DANIEL-2019", "Hinkley Point C CAS", "Design, sampling, coding"],
            ["PL-EMR-TEMPLATES-2023", "Eisenhardt / Gioia / Langley", "Replacing Fereday & Muir-Cochrane"],
            ["PL-ORIGINS-IQ", "Origins IQ-01 wording", "Live interview"],
            ["PL-ORIGINS-N-10-15", "Sample range 10–15", "Reopening n in the Project Plan"],
        ],
    )

    heading(doc, "10. What will not change")
    para(
        doc,
        "Spoken interview wording remains ITDR-GQI-INT-v0.1.1; n = 12; VCST placement on Need only; instructor original Word in source/originals/; phenomenology and confirmatory wording stay out; Delve is not the method.",
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    return path


def patch_csv_templates(new_refs: list[dict]):
    existing = read_csv("references.csv")
    have = {r["ref_id"] for r in existing}
    path = TEMPLATES / "references.csv"
    with path.open(newline="", encoding="utf-8") as f:
        fieldnames = csv.DictReader(f).fieldnames
    add = []
    for r in new_refs:
        if r["ref_id"] in have:
            continue
        row = {k: r.get(k, "") for k in fieldnames}
        add.append(row)
    if add:
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            for row in add:
                w.writerow(row)
    ul_path = TEMPLATES / "update-log.csv"
    with ul_path.open(encoding="utf-8") as f:
        ul_text = f.read()
    if "UL-0005" not in ul_text:
        with ul_path.open(newline="", encoding="utf-8") as f:
            ul_fields = csv.DictReader(f).fieldnames
        with ul_path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=ul_fields)
            w.writerow(
                {
                    "log_id": "UL-0005",
                    "timestamp_utc": "2026-09-08T02:30:00Z",
                    "type": "pack_create",
                    "instrument_version": "ITDR-GQI-INT-v0.1.1",
                    "changed_by": "researcher",
                    "files_touched": "downloads/Dissertation_Document_Tracking_Master.xlsx; downloads/Dissertation_Document_Tracking_Pack.docx; docs/notion/templates/references.csv",
                    "summary": "Tracking pack v1.0. New PDF refs Joos 2019, Khurram 2015, EMR roadmap 2023, Daniel 2019 parked, Christensen 2023 parked, Wood 2021. Spoken wording unchanged. n=12.",
                    "delve_export": "N",
                    "backup_folder": "docs/notion/templates",
                }
            )


def main():
    xlsx = OUT / "Dissertation_Document_Tracking_Master.xlsx"
    docx_path = OUT / "Dissertation_Document_Tracking_Pack.docx"
    _, refs = build_workbook(xlsx)
    build_docx(docx_path, refs)
    patch_csv_templates(extra_refs())
    print("wrote", xlsx, "sheets", "ok")
    print("wrote", docx_path)
    print("xlsx_bytes", xlsx.stat().st_size, "docx_bytes", docx_path.stat().st_size)


if __name__ == "__main__":
    main()
