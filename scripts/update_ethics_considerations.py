#!/usr/bin/env python3
"""Update Ethical Considerations (attachment 1) with bolded changes.

Preserves Word comments. Does not add paragraphs. Header text stays
'Ethical Considerations'. Spoken interview stems are unchanged.
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

# (text, bold). Bold = change from the yellow attachment.
P1 = [
    (
        "Ethical Considerations for this generic qualitative inquiry name the ethical issues and the plan that will meet Capella’s privacy, confidentiality, and data security standard (Resnik, 2018). ",
        True,
    ),
    (
        "Ethics shapes study design, the process of discovery, and the significance of the findings, and it requires the researcher to weigh the human cost of inquiry ",
        False,
    ),
    ("(Resnik, 2018)", True),
    (
        ". Participants will be U.S. small and medium-sized enterprise (SME) IT, network, systems, infrastructure, or operations managers in firms of 10 to 200 personnel. In that setting ",
        False,
    ),
    ("the primary ethical issue is re-identification", True),
    (
        ": a named recovery event, a role title, and a platform type can expose a person or firm more easily than in a large enterprise. The researcher will not begin identification, screening, or scheduling until the Capella University Institutional Review Board has granted written approval. The design follows the Belmont Report’s principles of respect for persons, beneficence, and justice (National Commission for the Protection of Human Subjects of Biomedical and Behavioral Research, 1979). Respect for persons will be enacted through voluntary participation, signed electronic consent, a recorded permission-to-record check, and the right to skip any question or stop at any time without penalty. Beneficence will be enacted by treating SME organizational disclosure as both a ",
        False,
    ),
    ("privacy issue and a threat to candid Gap data", True),
    (
        ": the researcher will not recruit through a supervisor, owner, employer command chain, or vendor account manager; ",
        False,
    ),
    ("collection remains interviews only", True),
    ("; identifiers will be stripped to P##, role only, SME-X, and Platform-X; and member checking will be a seven-day factual review of sequence, roles, and ", False),
    ("named proof", True),
    (
        " so contested recovery decisions are not edited out. Justice will be enacted by placing the research burden on operational U.S. SME managers who can name a qualifying event, and by excluding vendor-only staff and command-visible recruitment paths.",
        False,
    ),
]

P2 = [
    (
        "Honesty and integrity will govern collection, storage, analysis, reporting, and any later discussion of the study ",
        False,
    ),
    ("(Resnik, 2018)", True),
    (". ", False),
    ("Data security: ", True),
    (
        "recordings and RAW notes will be stored in an encrypted, password-protected directory separate from CLEAN transcripts and the Delve audit nest. ",
        False,
    ),
    ("Confidentiality: ", True),
    (
        "the researcher will not continue a session from memory if recording fails, will not invent contents a manager did not state, and will ",
        False,
    ),
    ("not claim that Delve performed the analysis", True),
    (". ", False),
    ("Privacy: ", True),
    ("findings will be disseminated", True),
    (
        " as de-identified patterned accounts of named U.S. SME recovery events, without employer, owner, vendor, or product names, so the study can report how managers enacted whose claim counted, who decided, and what counted as enough proof without exposing the participant or the firm.",
        False,
    ),
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


def main() -> None:
    doc = Document(str(SRC))
    p1 = next(p for p in doc.paragraphs if p.text.startswith("Ethics is a guiding principle") or p.text.startswith("Ethical Considerations for this generic"))
    p2 = next(p for p in doc.paragraphs if p.text.startswith("Honesty and integrity will govern"))
    write_mixed(p1, P1)
    write_mixed(p2, P2)
    doc.save(str(OUT))
    shutil.copy2(OUT, ART)
    shutil.copy2(OUT, ALIAS)
    shutil.copy2(OUT, ART_ALIAS)
    print("updated ethics paragraphs")
    print("p1", p1.text[:120])
    print("p2", p2.text[:120])


if __name__ == "__main__":
    main()
