#!/usr/bin/env python3
"""Update Proposed Data Analysis Plan for the Capella header.

Third person. Current citations. Sentence-case raw/clean in running text.
Bold = change from the highlighted attachment. Preserves Word comments.
Does not add paragraphs. Spoken interview stems unchanged.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

SRC = Path("/workspace/downloads/MW_Wk5_to_wk8_Edit_6Sep26.docx")
OUT = Path("/workspace/downloads/MW_Wk5_to_wk8_Edit_6Sep26.docx")
ART = Path("/opt/cursor/artifacts/MW_Wk5_to_wk8_Edit_6Sep26.docx")
ALIAS = Path("/workspace/downloads/MW_Wk5_to_wk8_Edit_6Sep26_updated.docx")
ART_ALIAS = Path("/opt/cursor/artifacts/MW_Wk5_to_wk8_Edit_6Sep26_updated.docx")

P1 = [
    (
        "The researcher will analyze de-identified critical-incident interviews from the locked sample of 12 U.S. SME IT, network, systems, infrastructure, or operations managers using hybrid deductive–inductive codebook thematic analysis within a generic qualitative inquiry (Caelli et al., 2003; Fereday & Muir-Cochrane, 2006; Kahlke, 2014; Percy et al., 2015). ",
        False,
    ),
    (
        "That technique is appropriate to the project framework because power, legitimacy, and urgency remain sensitizing probes (Mitchell et al., 1997), while value-creation stakeholder theory remains on Need / What We Know and is not imported as a codebook theme (Freeman et al., 2020). ",
        True,
    ),
    (
        "Before coding, the researcher will complete a scope register that records the purpose, research question, framework role, eligibility rules, participant count, and required deliverables, and will keep three work areas separate: ",
        False,
    ),
    ("raw recordings, clean analytic files, and presentation outputs", True),
    (
        ". Each interview will receive a stable identifier. The researcher will produce a verbatim transcript, strip person, firm, vendor, and product names, complete a seven-day factual member check, and read each ",
        False,
    ),
    ("clean transcript", True),
    (" in full before formal coding (Lincoln & Guba, 1985). Delve will store ", False),
    ("clean transcripts", True),
    (
        ", the versioned codebook, memos, and snippet URLs. Delve will not perform the analysis ",
        False,
    ),
    ("(Paulus, 2023)", True),
    (".", False),
]

P2 = [
    (
        "Second, the researcher will import the nested start-list of STRUCTURAL, FRAMEWORK_DEDUCTIVE, and BOUNDARY codes and create one excerpt record for each bounded passage that requires analysis, attaching its source locator, speaker, incident context, and provisional code (Fereday & Muir-Cochrane, 2006; Paulus, 2023). A passage may receive more than one code when it conveys distinct ideas. Power, legitimacy, and urgency will function as sensitizing probes, not predetermined theme titles (Mitchell et al., 1997). Decision rights, escalation, evidentiary standards, and recoverability assurance will be coded as enactment evidence, not as a fourth salience attribute. Each code definition will state its meaning, inclusion criteria, exclusion criteria, and a source-linked example; uncertain assignments will be flagged for review. EMERGENT child codes will remain empty until meaning units are locked ",
        False,
    ),
    ("(Saldaña, 2021; Taylor & Bogdan, 1998)", True),
    (
        ". Coding changes will be recorded with the date, reason, and affected records. Spreadsheet lookup and Delve retrieval may support these records; interpretive approval will remain with the researcher (Fereday & Muir-Cochrane, 2006).",
        False,
    ),
]

P3 = [
    (
        "Third, the researcher will lock meaning units that state a practice claim before any theme name is written, confirm each unit with a named excerpt and a negative or boundary case, and group related units only when they describe the same salience-to-assurance bargain rather than the same recovery topic ",
        False,
    ),
    ("(Saldaña, 2021; Taylor & Bogdan, 1998; Walker, 2026)", True),
    (
        ". For every proposed theme, the researcher will record its central claim, contributing categories, representative excerpts, exceptions, and research-question relevance, then return to the original passages to inspect context. Candidate categories may be retained, revised, split, combined, or rejected, with earlier versions preserved. This is iterative interpretive work, not an automatic promotion of frequently used labels into themes, and it is ",
        False,
    ),
    ("not reflexive thematic analysis as the analytic method (Saldaña, 2021; Fereday & Muir-Cochrane, 2006)", True),
    (
        ". The locked n = 12 will be reported as the planned participant count, not as proof of saturation; adequacy will be assessed through richness, relevant variation, question coverage, and whether later interviews still change the meaning-unit inventory ",
        False,
    ),
    ("(Malterud et al., 2016; Guest et al., 2020)", True),
    (".", False),
]

P4 = [
    (
        "Fourth, the researcher will write two separate syntheses from the reviewed theme records: one for stakeholder-claim management and salience shifts, and one for decision rights, escalation, and recoverability assurance (Lester et al., 2020; Percy et al., 2015). Presentation will include a meaning-unit evidence table, a theme-to-question map, and a narrative that pairs each interpretive claim with source-verified excerpts and relevant boundary cases. ",
        False,
    ),
    (
        "Every published quotation, participant label, source locator, and thematic claim will receive a source check",
        True,
    ),
    (
        "; table titles and theme names will be compared with the narrative. Participant counts, excerpt counts, and source counts will remain separate. The researcher will close the revision log, record unresolved gaps, and release a dated version of the report, codebook, and CSV nest (Paulus, 2023). Clerical software and retrieval aids will not replace researcher interpretation; every quotation and thematic claim will remain grounded in the ",
        False,
    ),
    ("clean transcript", True),
    (" and the dated audit trail (Tracy, 2010). Findings will distinguish managers’ reported interpretations from independently documented actions and will not claim statistical generalization.", False),
]


def set_run_font(run, *, size=12, bold=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold


def write_mixed(paragraph, parts) -> None:
    for r in paragraph.runs:
        r.text = ""
    first = True
    for text, bold in parts:
        if first and paragraph.runs:
            run = paragraph.runs[0]
            run.text = text
            set_run_font(run, bold=bold)
            first = False
        else:
            run = paragraph.add_run(text)
            set_run_font(run, bold=bold)
            first = False
    paragraph.paragraph_format.line_spacing = 2.0


def rewrite_raw_clean_in_ethics(doc: Document) -> None:
    for p in doc.paragraphs:
        if "Honesty and integrity will govern" in p.text and "raw notes" not in p.text.lower().replace("raw notes", "raw notes"):
            pass
        if p.text.startswith("Honesty and integrity will govern"):
            new = (
                p.text.replace("RAW notes", "raw notes")
                .replace("CLEAN transcripts", "clean transcripts")
                .replace("RAW recordings", "raw recordings")
            )
            if new == p.text:
                return
            # rebuild keeping existing bold where possible is hard; rewrite with targeted bold
            parts = []
            # keep prior bold labels if present
            t = new
            # simple: write whole para, bold the sentence-case labels
            parts = [
                ("Honesty and integrity will govern collection, storage, analysis, reporting, and any later discussion of the study ", False),
                ("(Resnik, 2018)", True),
                (". ", False),
                ("Data security: ", True),
                ("recordings and ", False),
                ("raw notes", True),
                (" will be stored in an encrypted, password-protected directory separate from ", False),
                ("clean transcripts", True),
                (" and the Delve audit nest. ", False),
                ("Confidentiality: ", True),
                ("the researcher will not continue a session from memory if recording fails, will not invent contents a manager did not state, and will ", False),
                ("not claim that Delve performed the analysis", True),
                (". ", False),
                ("Privacy: ", True),
                ("findings will be disseminated", True),
                (
                    " as de-identified patterned accounts of named U.S. SME recovery events, without employer, owner, vendor, or product names, so the study can report how managers enacted whose claim counted, who decided, and what counted as enough proof without exposing the participant or the firm.",
                    False,
                ),
            ]
            write_mixed(p, parts)
            return


def main() -> None:
    doc = Document(str(SRC))
    p1 = next(p for p in doc.paragraphs if p.text.startswith("The researcher will analyze de-identified"))
    p2 = next(p for p in doc.paragraphs if p.text.startswith("Second, the researcher will import"))
    p3 = next(p for p in doc.paragraphs if p.text.startswith("Third, the researcher will lock meaning units"))
    p4 = next(p for p in doc.paragraphs if p.text.startswith("Fourth, the researcher will write two separate"))
    write_mixed(p1, P1)
    write_mixed(p2, P2)
    write_mixed(p3, P3)
    write_mixed(p4, P4)
    rewrite_raw_clean_in_ethics(doc)
    doc.save(str(OUT))
    shutil.copy2(OUT, ART)
    shutil.copy2(OUT, ALIAS)
    shutil.copy2(OUT, ART_ALIAS)
    print("updated analysis offering")


if __name__ == "__main__":
    main()
