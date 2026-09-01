#!/usr/bin/env python3
"""Seed `_CHPT III_Assension_db` registers, how-to pages, and inventory.json."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "_CHPT III_Assension_db"
CH3 = ROOT / "docs" / "chapter-iii-methodology.md"
MD_BASE = "docs/chapter-iii-methodology.md"

SPINE = {
    "Problem": "SME IT/network managers must handle competing restoration claims on external platforms without a clear account of how authority and proof are enacted under time pressure.",
    "Purpose": "Describe how those managers account for stakeholder-claim management and salience shifts in one named ITDRPaaS recovery or test event, and how those shifts are enacted as decision rights, escalation, and defensible proof.",
    "Questions": "Implied PQ1 (claim attention / salience shifts) and PQ2 (enactment as rights, escalation, proof). Official RQ wording will replace these labels when locked.",
    "Framework": "Mitchell et al. (1997) power, legitimacy, urgency as sensitizing attributes; leverage as the enacted combination; PQ2 constructs as enactment probes.",
    "Data sources": "Critical-incident interviews; optional redacted artifacts or verbal reconstructions of what those artifacts did in the event.",
    "Instrument questions": "ITDR-GQI-INT-v0.1.1: Q0; Set L; Sets A–F; Q-close; skip-if-covered; boundary cases.",
    "Collection": "One-to-one recorded video interviews, 60–75 minutes, plus artifact intake Paths A/B/C.",
    "Codes": "STRUCTURAL, FRAMEWORK_DEDUCTIVE, BOUNDARY, then EMERGENT after meaning-unit lock.",
    "Categories": "Grouped meaning units that describe the same salience-to-assurance bargain, named in Chapter IV.",
    "Themes_ChIV": "Patterned-meaning claims, not topic headings, named in Chapter IV.",
    "Findings_ChIV": "Chapter IV reports. Not claimed in Chapter III.",
    "Conclusions_ChV": "Chapter V interprets. Not claimed in Chapter III.",
}


def github_slug(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def parse_headings() -> list[dict]:
    lines = CH3.read_text(encoding="utf-8").splitlines()
    rows = []
    parent = None
    n = 0
    for i, line in enumerate(lines, 1):
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        if title == "Table of contents":
            continue
        n += 1
        hid = f"CH3-H-{n:03d}"
        if level == 2:
            parent = hid
            parent_id = ""
        else:
            parent_id = parent or ""
        slug = github_slug(title)
        rows.append(
            {
                "id": hid,
                "level": f"H{level}",
                "parent_id": parent_id,
                "heading": title,
                "slug": slug,
                "line": i,
                "md_link": f"{MD_BASE}#{slug}",
                "howto_file": f"H-{n:03d}-{slug}.md",
            }
        )
    return rows


HEADERS: list[dict] = []  # filled in main after parse; content keyed by heading


# heading -> (spine_nodes, alignment_nodes, tester_status, purpose, do, do_not, tester_check, companions)
META = {
    "Introduction": (
        "Problem; Purpose; Questions",
        "Topic / Problem; Gap; Questions",
        "Strong",
        "State what Chapter III plans and what it must not claim.",
        "Keep the chapter as Capella operations-cluster prose. Name GQI, CIT, hybrid codebook TA, and Delve as CAQDAS only.",
        "Do not name Chapter IV themes, write 'lived experience,' or say data will be analyzed using Delve.",
        "Tester checks Topic/Problem and Gap restatement without findings.",
        "docs/chapter-iii-methodology.md#introduction | docs/alignment-assessment-data-collection.md",
    ),
    "Research Design": (
        "Purpose; Framework; Data sources",
        "Methodology",
        "Strong",
        "Declare GQI + CIT with a sensitizing, not confirmatory, framework.",
        "Keep unit of analysis as one U.S. SME manager recounting one qualifying ITDRPaaS incident in 36 months.",
        "Do not convert the design into phenomenology, an audit, or a confirmatory test of Mitchell et al. (1997).",
        "Tester checks Methodology* for GQI language and absence of essence claims.",
        "docs/gqi-semistructured-interview-guide.md | docs/alignment-assessment-data-collection.md",
    ),
    "Generic qualitative inquiry": (
        "Purpose; Framework; Data sources",
        "Methodology",
        "Strong",
        "Justify GQI as accounts of external events, decisions, and artifacts.",
        "Permit theoretically informed items only if they stay in manager language and constructs are not treated as conclusions.",
        "Do not use lived experience, essence, or voices as analytic claims.",
        "Tester checks Methodology* against Capella GQI (not phenomenology).",
        "docs/chapter-iii-methodology.md#generic-qualitative-inquiry",
    ),
    "Critical-incident interview stance": (
        "Data sources; Collection",
        "Methodology; Data Collection",
        "Strong",
        "Bind talk to one named disruption, failover, test, or operational recovery.",
        "Use CIT because the gap is operational: competing claims when restoration is ranked, delayed, or declared done.",
        "Do not treat Guest et al. (2006) as the interview method.",
        "Tester checks that Data Collection stays incident-bound.",
        "docs/gqi-semistructured-interview-guide.md | docs/collection-analysis-revision-packet.md",
    ),
    "Framework role: sensitizing, not confirmatory": (
        "Framework; Codes",
        "Constructs / Phenomena / Variables; What We Know",
        "Strong",
        "Place PLU and enactment constructs on Constructs, not as pre-named themes.",
        "Cite Mitchell et al. (1997) as original; later work as build-on. Keep leverage as enacted combination, not a fourth attribute.",
        "Do not pre-write Chapter IV themes from the seven labels.",
        "Tester checks Constructs are sensitizing probes, not a priori findings.",
        "docs/symbols-definitions-refs.md | docs/notion/templates/codebook.csv",
    ),
    "Alignment spine": (
        "Problem; Purpose; Questions; Framework; Data sources; Instrument questions; Collection; Codes; Categories; Themes_ChIV; Findings_ChIV; Conclusions_ChV",
        "Topic / Problem; Gap; Questions; Constructs / Phenomena / Variables; Methodology; Measures/Artifacts; Data Collection; Data Analysis",
        "Strong",
        "Keep the planned chain intact from Problem through Chapter V interpretation.",
        "Use the spine table as the alignment tester for every later header. Empty Theme/Finding cells until Chapter IV.",
        "Do not claim SAL → DR → ESC → AE as a proven substantive theory.",
        "Tester walks Problem → Purpose → PQs → Framework → sources → items → collection → codes → categories → themes.",
        "docs/chapter-iii-methodology.md#alignment-spine | workspace-app/theory-spine.html",
    ),
    "Population and Sampling": (
        "Purpose; Collection",
        "Population; Sample",
        "Strong",
        "Name who can close the Gap and how they are selected.",
        "Keep U.S. SME IT/network/systems/infrastructure/operations managers on external recovery platforms.",
        "Do not recruit vendor-only staff or executives with no operational recovery role.",
        "Tester checks Population* and Sample* against inclusion and information power.",
        "docs/chapter-iii-methodology.md#population-and-sampling",
    ),
    "Population": (
        "Purpose",
        "Population",
        "Strong",
        "Bound the population at U.S. SMEs (10–200 personnel) with a named ITDRPaaS incident in 36 months.",
        "Require a direct operational recovery role on an external platform or managed recovery service.",
        "Do not include vendor staff whose only role is operating the platform for clients.",
        "Tester checks Population* matches the Gap (SME managers, not large-enterprise command).",
        "docs/alignment-assessment-data-collection.md",
    ),
    "Sampling strategy": (
        "Collection; Questions",
        "Sample",
        "Strong",
        "Justify n = 10–15 with information power, not automatic saturation.",
        "Use purposive/criterion sampling. Stopping is an analytic decision from the codebook and meaning-unit inventory.",
        "Do not use Guest et al. (2006) to justify CIT, sample size in advance, or a claim that 12 interviews suffice.",
        "Tester checks Sample* for information power (Malterud et al., 2016).",
        "docs/chapter-iii-methodology.md#sampling-strategy",
    ),
    "Recruitment": (
        "Collection",
        "Recruitment; Procedures",
        "Strong",
        "Protect PQ2 data quality by recruiting individually, not through a supervisor chain.",
        "Screen inclusion, email consent, then schedule 60–75 minutes. Assign P## before the call.",
        "Do not continue an interview from a generic 'how we usually recover' account.",
        "Tester checks Recruitment* channel, length, and consent sequence.",
        "docs/gqi-semistructured-interview-guide.md | docs/collection-analysis-revision-packet.md",
    ),
    "Instrumentation": (
        "Instrument questions; Data sources",
        "Measures/Artifacts",
        "Strong",
        "Name the primary interview guide and the secondary artifact review.",
        "Keep theoretical labels in the codebook. Spoken questions use manager language.",
        "Do not treat the unpublished instrument as a theory source.",
        "Tester checks Measures/Artifacts have collectable items for each construct.",
        "docs/gqi-semistructured-interview-guide.md | docs/notion/templates/interview-items.csv",
    ),
    "Primary instrument": (
        "Instrument questions; Questions",
        "Measures/Artifacts; Data Collection",
        "Strong",
        "Run ITDR-GQI-INT-v0.1.1: ethics, Q0, Set L, Sets A–F, Q-close, skip-if-covered, boundary cases.",
        "Skip a set only when a concrete example already exists. Boundary cases are valid data.",
        "Do not introduce power, legitimacy, urgency, or proof in Q0.",
        "Tester checks each Gap construct has a collectable item or skip-plus-boundary.",
        "docs/gqi-semistructured-interview-guide.md | docs/notion/templates/construct-index.csv | workspace-app/interview-protocol.html",
    ),
    "Researcher-only leverage diagnostic": (
        "Framework; Codes",
        "Constructs / Phenomena / Variables; Data Analysis",
        "Strong",
        "Complete one leverage-memo row after the session; never read it to the participant.",
        "Map attribute_mix to Mitchell type names as memo values only.",
        "Do not import Mitchell type names into Delve as theme titles or Chapter IV headings. Leverage is not a fourth salience attribute.",
        "Tester checks Constructs vs Data Analysis: memo labels are not findings.",
        "docs/symbols-definitions-refs.md | docs/notion/templates/leverage-memo.csv",
    ),
    "Secondary instrument: artifacts as context": (
        "Data sources; Collection",
        "Measures/Artifacts; Procedures",
        "Strong",
        "Review objects the manager names in the incident via Path A (redacted share), B (verbal reconstruction), or C (none named).",
        "File Path A as P##_ART##. Recode empty Path A after 14 days as Path B. Path C is a recoverability-assurance boundary.",
        "Do not score artifacts against NIST/ISO/BCM. Do not invent contents the participant did not state. Refusal to share does not end the interview.",
        "Tester checks Measures/Artifacts have an obtain / refuse / de-identify / map rule.",
        "docs/collection-analysis-revision-packet.md | docs/gqi-semistructured-interview-guide.md",
    ),
    "Data Collection": (
        "Collection; Instrument questions",
        "Data Collection; Procedures",
        "Strong",
        "Execute one recorded 60–75 minute video interview plus artifact intake.",
        "Confirm consent and inclusion; read the ethics script; keep probes inside the named event; stop if the recorder fails.",
        "Do not offer forced choices or continue from memory. Completeness is a collection standard, not a finding.",
        "Tester checks Data Collection* has written steps, not only named instruments.",
        "docs/gqi-semistructured-interview-guide.md | docs/collection-analysis-revision-packet.md",
    ),
    "Data Preparation and Management": (
        "Collection; Codes",
        "Procedures; Dependability",
        "Strong",
        "Move RAW → CLEAN → ANALYTIC, with dated CSV nest backups.",
        "Import only CLEAN transcripts to Delve. Member-check CLEAN facts, not ANALYTIC theme names.",
        "Do not put RAW identifiers in the public nest. Participants may not delete a de-identified contested decision.",
        "Tester checks Dependability* for a retraceable audit trail.",
        "docs/notion/README.md | docs/notion/templates/update-log.csv",
    ),
    "Qualitative Data Analysis": (
        "Codes; Categories; Themes_ChIV; Findings_ChIV",
        "Data Analysis",
        "Strong",
        "Name hybrid codebook TA as the method; keep Theme/Finding cells empty.",
        "Lock meaning units before theme names. Import STRUCTURAL, FRAMEWORK_DEDUCTIVE, and BOUNDARY; leave EMERGENT empty at first code.",
        "Do not write that data will be analyzed using Delve, or that themes emerged.",
        "Tester checks Data Analysis stays a reduction method, not pre-named themes.",
        "docs/notion/templates/codebook.csv | workspace-app/analysis-templates.html",
    ),
    "Declaration of method": (
        "Codes; Categories",
        "Data Analysis; Methodology",
        "Strong",
        "Declare hybrid deductive–inductive codebook thematic analysis (Fereday & Muir-Cochrane, 2006).",
        "Cite Braun and Clarke for quality of thematic practice only. Default trustworthiness is audit trail, not kappa.",
        "Do not mix ICR with a claim that the study is doing reflexive TA.",
        "Tester checks Data Analysis names a method that can map PQ1/PQ2 onto a versioned codebook.",
        "docs/chapter-iii-methodology.md#declaration-of-method",
    ),
    "Why this method and not the adjacent alternatives": (
        "Codes; Framework",
        "Data Analysis; Methodology",
        "Strong",
        "Reject reflexive TA as method, purely inductive TA, confirmatory Mitchell coding, NIST scoring, and Delve-as-method.",
        "Keep the adjacent-choice table in the chapter when reviewers ask 'why not NVivo/RTA/content analysis.'",
        "Do not treat CAQDAS as the analytic method.",
        "Tester checks Methodology and Data Analysis do not drift into audit or phenomenology.",
        "docs/chapter-iii-methodology.md#why-this-method-and-not-the-adjacent-alternatives",
    ),
    "Analytic steps (adapted hybrid codebook TA)": (
        "Codes; Categories; Themes_ChIV",
        "Data Analysis",
        "Strong",
        "Follow the written hybrid steps: lock meaning units, apply template codes, add EMERGENT after lock, group, then name themes in Chapter IV.",
        "Require a named excerpt and a boundary/negative case before promoting a unit.",
        "Do not name themes in Chapter III. Frequency is not importance.",
        "Tester checks Practice 2 lock-before-name is still the reduction rule.",
        "docs/collection-analysis-revision-packet.md | workspace-app/analysis-templates.html",
    ),
    "Delve nested start-list (import; do not treat as themes)": (
        "Codes",
        "Data Analysis; Constructs / Phenomena / Variables",
        "Strong",
        "Import the nested start-list as filing and sensitizing devices.",
        "Keep STRUCTURAL / FRAMEWORK_DEDUCTIVE / BOUNDARY names identical to docs/notion/templates/codebook.csv.",
        "Do not treat imported codes as Chapter IV headings.",
        "Tester checks Constructs inform Measures; they do not pre-write Data Analysis themes.",
        "docs/notion/templates/codebook.csv | docs/notion/templates/construct-index.csv",
    ),
    "Planned-analysis matrix": (
        "Instrument questions; Codes; Questions; Themes_ChIV; Findings_ChIV",
        "Measures/Artifacts; Data Analysis; Questions",
        "Partial",
        "Map every question ID to PQ, structural code, and planned framework/boundary codes.",
        "Leave Category / Theme / Finding columns empty. Official RQ labels replace PQ1/PQ2 in Maps-to without changing question IDs.",
        "Do not require every ID to be asked aloud; skipped rows still map.",
        "Questions tester stays Partial until official RQ wording is locked.",
        "docs/chapter-iii-methodology.md#planned-analysis-matrix | docs/notion/templates/interview-items.csv",
    ),
    "Ten control rules": (
        "Codes; Themes_ChIV; Findings_ChIV; Conclusions_ChV",
        "Data Analysis; Dependability",
        "Strong",
        "Govern coding, memoing, and write-up. A violation is a dependability incident logged the same day.",
        "Method first, software second. Codes are not themes. Themes are claims. Do not write that themes emerged.",
        "Do not treat leverage as a fourth salience attribute or NIST/ISO/BCM as a coding system.",
        "Tester checks Dependability* has enforceable write-up rules.",
        "docs/chapter-iii-methodology.md#ten-control-rules",
    ),
    "Chapter III versus Chapter IV versus Chapter V": (
        "Themes_ChIV; Findings_ChIV; Conclusions_ChV",
        "Data Analysis; Questions",
        "Strong",
        "Keep the chapter split: III plans, IV reports, V interprets.",
        "Do not offer implications in III or IV. Do not newly name themes in V.",
        "Do not treat Delve or the CSV nest as a contribution.",
        "Tester checks the spine end-nodes stay empty in this chapter.",
        "docs/chapter-iii-methodology.md#chapter-iii-versus-chapter-iv-versus-chapter-v",
    ),
    "Optional: committee-required second coder and ICR": (
        "Codes",
        "Dependability; Data Analysis",
        "Strong",
        "Keep ICR optional and off by default for this single-researcher dissertation.",
        "Activate only if the committee requires a second coder. Do not mix ICR with reflexive TA.",
        "Do not make kappa a default quality claim.",
        "Tester checks Dependability does not require multiple coders as a GQI condition.",
        "docs/chapter-iii-methodology.md#optional-committee-required-second-coder-and-icr",
    ),
    "Trustworthiness": (
        "Collection; Codes; Findings_ChIV",
        "Dependability; Procedures",
        "Strong",
        "Use credibility, dependability, confirmability, and transferability (Lincoln & Guba, 1985).",
        "Keep member check factual-only. Treat saturation as a decision guide, not a badge that n = 10–15 earns.",
        "Do not claim 10–15 U.S. SME managers represent all ITDRPaaS settings.",
        "Tester checks Dependability* for a visible audit trail and threat mitigations.",
        "docs/chapter-iii-methodology.md#trustworthiness",
    ),
    "Ethical Protections": (
        "Collection",
        "Procedures; Recruitment",
        "Strong",
        "Submit to Capella IRB before recruitment; treat organizational risk as a Gap-data threat.",
        "Optional artifacts, factual member check, encrypted RAW storage, pause/skip/stop for distress.",
        "Do not put RAW identifiers in courseroom appendices or the public CSV nest.",
        "Tester checks Procedures* protect contested authority and failed-proof talk.",
        "docs/gqi-semistructured-interview-guide.md | docs/collection-analysis-revision-packet.md",
    ),
    "Chapter Summary": (
        "Problem; Purpose; Questions; Collection; Codes; Themes_ChIV; Conclusions_ChV",
        "Methodology; Data Analysis",
        "Strong",
        "Restate the planned chain without converting it into findings.",
        "Repeat GQI, CIT, U.S. SME sample, instrument ID, hybrid codebook TA, and the III/IV/V split.",
        "Do not sneak theme titles into the summary.",
        "Tester checks the summary still plans rather than reports.",
        "docs/chapter-iii-methodology.md#chapter-summary",
    ),
    "References": (
        "Framework",
        "What We Know; Methodology; Data Analysis",
        "Strong",
        "Keep seminal vs build-on vs software vs new-instrument vs audit-artifact classes intact.",
        "Match docs/notion/templates/references.csv origin and citation_status columns.",
        "Do not use Guest et al. (2006) as the interview method or Delve as a literature source for analysis.",
        "Tester checks What We Know citations are used only for allowed purposes.",
        "docs/notion/templates/references.csv | docs/symbols-definitions-refs.md",
    ),
}


def csv_write(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def page_text(h: dict, meta: tuple) -> str:
    spine, testers, status, purpose, do, do_not, tester_check, companions = meta
    hid = h["id"]
    heading = h["heading"]
    md_link = h["md_link"]
    parent = h["parent_id"] or "—"
    links = [c.strip() for c in companions.split("|")]
    link_md = "\n".join(f"- `{x}`" for x in links)
    return f"""# {hid} · {heading}

**Chapter header:** [{heading}](../../{md_link})
**Level:** {h["level"]} · **Parent:** `{parent}` · **Tester status:** {status}

## Purpose

{purpose}

## How to keep the spine intact

**Do.** {do}

**Do not.** {do_not}

## Spine nodes this header must serve

{spine}

## Alignment tester check

{tester_check}

Markers: {testers}

## Companion links

- Chapter header: [`{md_link}`](../../{md_link})
- Assension layout: [../layout.md](../layout.md)
- Header register: [../registers/header-index.csv](../registers/header-index.csv)
{link_md}

## Upload / later template slot

Drop related theory notes, interview templates, or committee feedback for this header in [`../uploads/`](../uploads/README.md) and log the file on [`../registers/crosswalk.csv`](../registers/crosswalk.csv). Do not place identifiable transcripts here.
"""


def main() -> None:
    headers = parse_headings()
    missing = [h["heading"] for h in headers if h["heading"] not in META]
    if missing:
        raise SystemExit(f"Missing META for: {missing}")

    pages = DB / "pages"
    pages.mkdir(parents=True, exist_ok=True)
    (DB / "registers").mkdir(parents=True, exist_ok=True)

    header_rows = []
    howto_rows = []
    spine_rows = []
    cross_rows = []
    inventory = []
    sp_n = 0
    xw_n = 0
    ht_n = 0

    default_cross = [
        ("docs/gqi-semistructured-interview-guide.md", "instrument", "Spoken protocol companion"),
        ("docs/symbols-definitions-refs.md", "theory", "Symbol and original vs build-on lock"),
        ("docs/notion/templates/construct-index.csv", "codebook", "Question ID to code_id map"),
        ("docs/notion/templates/codebook.csv", "codebook", "Delve nested start-list"),
        ("docs/collection-analysis-revision-packet.md", "howto", "Paste-ready collection and analysis steps"),
        ("workspace-app/interview-protocol.html", "workspace", "Interview protocol alignment tab"),
    ]

    for h in headers:
        meta = META[h["heading"]]
        spine, testers, status, purpose, do, do_not, tester_check, companions = meta
        howto_rel = f"_CHPT III_Assension_db/pages/{h['howto_file']}"
        ht_n += 1
        htid = f"CH3-HT-{ht_n:03d}"
        row = {
            "id": h["id"],
            "level": h["level"],
            "parent_id": h["parent_id"],
            "heading": h["heading"],
            "slug": h["slug"],
            "md_link": h["md_link"],
            "howto_link": howto_rel,
            "howto_id": htid,
            "spine_nodes": spine,
            "alignment_nodes": testers,
            "tester_status": status,
            "companions": companions,
            "status": "active",
        }
        header_rows.append(row)
        howto_rows.append(
            {
                "id": htid,
                "header_id": h["id"],
                "heading": h["heading"],
                "purpose": purpose,
                "do": do,
                "do_not": do_not,
                "spine_check": spine,
                "tester_check": tester_check,
                "companion_links": companions,
                "howto_link": howto_rel,
            }
        )
        (pages / h["howto_file"]).write_text(page_text(h, meta), encoding="utf-8")

        for node in [n.strip() for n in spine.split(";") if n.strip()]:
            sp_n += 1
            spine_rows.append(
                {
                    "id": f"CH3-SP-{sp_n:03d}",
                    "header_id": h["id"],
                    "heading": h["heading"],
                    "spine_node": node,
                    "this_study": SPINE.get(node, ""),
                    "alignment_tester": testers.split(";")[0].strip(),
                    "notes": purpose,
                }
            )

        seen = set()
        extras = [(p.strip(), "companion", "Listed companion") for p in companions.split("|") if p.strip()]
        for path, kind, why in default_cross + extras:
            key = (h["id"], path)
            if key in seen:
                continue
            seen.add(key)
            xw_n += 1
            anchor = ""
            if "#" in path and not path.startswith("docs/chapter-iii"):
                path, anchor = path.split("#", 1)
            cross_rows.append(
                {
                    "id": f"CH3-XW-{xw_n:03d}",
                    "header_id": h["id"],
                    "heading": h["heading"],
                    "target_path": path,
                    "target_anchor": anchor,
                    "why": why,
                    "target_kind": kind,
                }
            )

        inventory.append(
            {
                **row,
                "href_md": h["md_link"],
                "href_howto": howto_rel.replace(" ", "%20"),
            }
        )

    testers = [
        {
            "id": "CH3-AT-001",
            "marker": "Topic / Problem",
            "map_cluster": "downward",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-001; CH3-H-006",
            "remaining_gap": "Keep practice-problem wording; do not recast as tool failure.",
            "next_howto": "_CHPT III_Assension_db/pages/H-001-introduction.md",
            "companion_link": "docs/alignment-assessment-data-collection.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-002",
            "marker": "What We Know",
            "map_cluster": "downward",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-005; CH3-H-029",
            "remaining_gap": "Keep original vs build-on classes; do not replace Mitchell definitions.",
            "next_howto": "_CHPT III_Assension_db/pages/H-005-framework-role-sensitizing-not-confirmatory.md",
            "companion_link": "docs/notion/templates/references.csv",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-003",
            "marker": "What We Don’t Know",
            "map_cluster": "downward",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-001; CH3-H-006",
            "remaining_gap": "Unknown remains enactment of salience as rights, escalation, and proof.",
            "next_howto": "_CHPT III_Assension_db/pages/H-006-alignment-spine.md",
            "companion_link": "docs/alignment-assessment-data-collection.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-004",
            "marker": "Gap",
            "map_cluster": "downward",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-001; CH3-H-006",
            "remaining_gap": "Who-cares / why-now stay on the Gap node, not as theme titles.",
            "next_howto": "_CHPT III_Assension_db/pages/H-001-introduction.md",
            "companion_link": "docs/alignment-assessment-data-collection.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-005",
            "marker": "Questions",
            "map_cluster": "downward",
            "rating": "Partial",
            "evidence_header_ids": "CH3-H-001; CH3-H-006; CH3-H-022",
            "remaining_gap": "Official RQ wording is not locked; PQ1/PQ2 stand in. Paste approved RQs without changing the unit of analysis.",
            "next_howto": "_CHPT III_Assension_db/pages/H-022-planned-analysis-matrix.md",
            "companion_link": "docs/chapter-iii-methodology.md#planned-analysis-matrix",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-006",
            "marker": "Constructs / Phenomena / Variables",
            "map_cluster": "downward",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-005; CH3-H-013; CH3-H-021; CH3-H-023",
            "remaining_gap": "Keep the seven labels as sensitizing probes. Do not promote them to Chapter IV headings.",
            "next_howto": "_CHPT III_Assension_db/pages/H-005-framework-role-sensitizing-not-confirmatory.md",
            "companion_link": "docs/symbols-definitions-refs.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-007",
            "marker": "Methodology",
            "map_cluster": "operations",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-002; CH3-H-003; CH3-H-004; CH3-H-018",
            "remaining_gap": "Watch language drift into phenomenology or audit.",
            "next_howto": "_CHPT III_Assension_db/pages/H-003-generic-qualitative-inquiry.md",
            "companion_link": "docs/gqi-semistructured-interview-guide.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-008",
            "marker": "Measures/Artifacts",
            "map_cluster": "downward",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-011; CH3-H-012; CH3-H-014; CH3-H-022",
            "remaining_gap": "Artifact Path C must stay a boundary, not missing data.",
            "next_howto": "_CHPT III_Assension_db/pages/H-012-primary-instrument.md",
            "companion_link": "docs/gqi-semistructured-interview-guide.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-009",
            "marker": "Data Collection",
            "map_cluster": "operations",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-004; CH3-H-015",
            "remaining_gap": "Completeness is a collection standard, not a finding.",
            "next_howto": "_CHPT III_Assension_db/pages/H-015-data-collection.md",
            "companion_link": "docs/collection-analysis-revision-packet.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-010",
            "marker": "Procedures",
            "map_cluster": "quality",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-010; CH3-H-015; CH3-H-016; CH3-H-027",
            "remaining_gap": "Keep artifact fallback and factual-only member check; they protect PQ2 talk.",
            "next_howto": "_CHPT III_Assension_db/pages/H-027-ethical-protections.md",
            "companion_link": "docs/collection-analysis-revision-packet.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-011",
            "marker": "Dependability",
            "map_cluster": "quality",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-016; CH3-H-023; CH3-H-026",
            "remaining_gap": "Log control-rule violations the same day. Keep snippet URLs in the CSV nest.",
            "next_howto": "_CHPT III_Assension_db/pages/H-023-ten-control-rules.md",
            "companion_link": "docs/notion/README.md",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-012",
            "marker": "Population",
            "map_cluster": "operations",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-007; CH3-H-008",
            "remaining_gap": "Stay inside 10–200 U.S. SME personnel; exclude vendor-only staff.",
            "next_howto": "_CHPT III_Assension_db/pages/H-008-population.md",
            "companion_link": "docs/chapter-iii-methodology.md#population",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-013",
            "marker": "Sample",
            "map_cluster": "operations",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-009",
            "remaining_gap": "Do not claim n = 10–15 saturates the Gap. Stopping remains analytic.",
            "next_howto": "_CHPT III_Assension_db/pages/H-009-sampling-strategy.md",
            "companion_link": "docs/chapter-iii-methodology.md#sampling-strategy",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-014",
            "marker": "Recruitment",
            "map_cluster": "operations",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-010; CH3-H-027",
            "remaining_gap": "Never recruit through a supervisor, employer command chain, or vendor account manager.",
            "next_howto": "_CHPT III_Assension_db/pages/H-010-recruitment.md",
            "companion_link": "docs/chapter-iii-methodology.md#recruitment",
            "status": "current_chapter",
        },
        {
            "id": "CH3-AT-015",
            "marker": "Data Analysis",
            "map_cluster": "downward",
            "rating": "Strong",
            "evidence_header_ids": "CH3-H-017; CH3-H-018; CH3-H-020; CH3-H-021; CH3-H-022; CH3-H-023; CH3-H-024",
            "remaining_gap": "Theme and Finding columns stay empty. Codes are not themes.",
            "next_howto": "_CHPT III_Assension_db/pages/H-018-declaration-of-method.md",
            "companion_link": "docs/chapter-iii-methodology.md#qualitative-data-analysis",
            "status": "current_chapter",
        },
    ]

    csv_write(
        DB / "registers" / "header-index.csv",
        [
            "id",
            "level",
            "parent_id",
            "heading",
            "slug",
            "md_link",
            "howto_link",
            "howto_id",
            "spine_nodes",
            "alignment_nodes",
            "tester_status",
            "companions",
            "status",
        ],
        header_rows,
    )
    csv_write(
        DB / "registers" / "spine-map.csv",
        ["id", "header_id", "heading", "spine_node", "this_study", "alignment_tester", "notes"],
        spine_rows,
    )
    csv_write(
        DB / "registers" / "alignment-testers.csv",
        [
            "id",
            "marker",
            "map_cluster",
            "rating",
            "evidence_header_ids",
            "remaining_gap",
            "next_howto",
            "companion_link",
            "status",
        ],
        testers,
    )
    csv_write(
        DB / "registers" / "how-to-notes.csv",
        [
            "id",
            "header_id",
            "heading",
            "purpose",
            "do",
            "do_not",
            "spine_check",
            "tester_check",
            "companion_links",
            "howto_link",
        ],
        howto_rows,
    )
    csv_write(
        DB / "registers" / "crosswalk.csv",
        ["id", "header_id", "heading", "target_path", "target_anchor", "why", "target_kind"],
        cross_rows,
    )

    (DB / "inventory.json").write_text(
        json.dumps(
            {
                "folder": "_CHPT III_Assension_db",
                "instrument_version": "ITDR-GQI-INT-v0.1.1",
                "chapter": "III",
                "header_count": len(header_rows),
                "headers": inventory,
                "alignment_testers": testers,
                "spine_nodes": SPINE,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"seeded {len(header_rows)} headers, {len(spine_rows)} spine rows, {len(testers)} testers")


if __name__ == "__main__":
    main()
