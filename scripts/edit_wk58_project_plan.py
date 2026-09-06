#!/usr/bin/env python3
"""Apply Week 8 comment responses to MW_Wk5_to_wk8_Edit_5Sep26_.docx.

Preserves existing Word comments by replacing run text instead of deleting
comment-range markup. Output is a new dated file; the uploaded original is
not overwritten.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph

SRC = Path("/home/ubuntu/.cursor/projects/workspace/uploads/MW_Wk5_to_wk8_Edit_5Sep26__e534.docx")
OUT = Path("/workspace/downloads/MW_Wk5_to_wk8_Edit_6Sep26.docx")
ART = Path("/opt/cursor/artifacts/MW_Wk5_to_wk8_Edit_6Sep26.docx")


def set_run_font(run, *, size=12, bold=None, italic=None):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def replace_text(p, text: str) -> None:
    """Replace visible text; keep extra runs empty so comment XML stays."""
    if not p.runs:
        run = p.add_run(text)
        set_run_font(run)
        return
    p.runs[0].text = text
    if p.runs[0].font.name is None:
        set_run_font(p.runs[0])
    for r in p.runs[1:]:
        r.text = ""


def insert_paragraph_after(paragraph, text: str) -> Paragraph:
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    run = new_para.add_run(text)
    set_run_font(run)
    new_para.paragraph_format.line_spacing = 2.0
    return new_para


def add_hyperlink(paragraph, text: str, url: str):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rpr.append(color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rpr.append(u)
    rfonts = OxmlElement("w:rFonts")
    rfonts.set(qn("w:ascii"), "Times New Roman")
    rfonts.set(qn("w:hAnsi"), "Times New Roman")
    rpr.append(rfonts)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "24")
    rpr.append(sz)
    new_run.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def insert_table_after(paragraph, headers, rows):
    tbl = OxmlElement("w:tbl")
    tbl_pr = OxmlElement("w:tblPr")
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), "5000")
    tbl_w.set(qn("w:type"), "pct")
    tbl_pr.append(tbl_w)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "666666")
        borders.append(el)
    tbl_pr.append(borders)
    tbl.append(tbl_pr)
    grid = OxmlElement("w:tblGrid")
    for _ in headers:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), "2160")
        grid.append(gc)
    tbl.append(grid)

    def add_row(values, header=False):
        tr = OxmlElement("w:tr")
        for val in values:
            tc = OxmlElement("w:tc")
            tc_pr = OxmlElement("w:tcPr")
            tc_w = OxmlElement("w:tcW")
            tc_w.set(qn("w:w"), "2160")
            tc_w.set(qn("w:type"), "dxa")
            tc_pr.append(tc_w)
            tc.append(tc_pr)
            p = OxmlElement("w:p")
            r = OxmlElement("w:r")
            rpr = OxmlElement("w:rPr")
            if header:
                b = OxmlElement("w:b")
                rpr.append(b)
            rfonts = OxmlElement("w:rFonts")
            rfonts.set(qn("w:ascii"), "Times New Roman")
            rfonts.set(qn("w:hAnsi"), "Times New Roman")
            rpr.append(rfonts)
            sz = OxmlElement("w:sz")
            sz.set(qn("w:val"), "18")
            rpr.append(sz)
            r.append(rpr)
            t = OxmlElement("w:t")
            t.set(qn("xml:space"), "preserve")
            t.text = val
            r.append(t)
            p.append(r)
            tc.append(p)
            tr.append(tc)
        tbl.append(tr)

    add_row(headers, header=True)
    for row in rows:
        add_row(row)
    paragraph._p.addnext(tbl)
    return tbl


ALIGN_1 = (
    "This study is undertaken in the Doctor of Philosophy in Business Management "
    "program with a specialization in Information Technology Management. That "
    "specialization advances the theory and practice of leading information-technology "
    "strategic planning and management in complex environments. It requires examination "
    "of collaborative relationships among IT and other organizational leaders, strategies "
    "that integrate technological arrangements with changing business needs, and the "
    "ethical and legal issues that shape IT management so that practical solutions can "
    "be developed for real-world problems that arise as organizations compete "
    "(Capella University, 2024). The proposed project specifically aligns with that "
    "specialization because the object of study is not a technical restore script. It "
    "is an IT-management governance problem: how U.S. small- and medium-enterprise "
    "(SME) IT and network managers handle competing recovery claims, allocate decision "
    "rights, escalate contested choices, and defend restoration when disaster recovery "
    "is delivered on an external platform (ITDRPaaS)."
)

ALIGN_2 = (
    "Value-creation stakeholder theory supplies the needed foundation construct. "
    "Distinctive stakeholder work describes human actors cooperatively engaged in "
    "value creation and trade and treats many tensions between stakeholder management "
    "and strategic-technical objectives as differences of narrative rather than "
    "mutually exclusive tasks (Freeman et al., 2020). In an ITDRPaaS incident those "
    "actors include executives, customers, providers, regulators, and the IT managers "
    "who must decide whose claim moves restore order. Stakeholder-salience theory then "
    "supplies the middle-range attention mechanism: power, legitimacy, and urgency "
    "shape whose claims count (Mitchell et al., 1997). A generic qualitative inquiry "
    "is appropriate because it examines managers’ accounts of named recovery events, "
    "governance decisions, escalation pathways, and recoverability-assurance practices "
    "(Caelli et al., 2003; Kahlke, 2014). The project therefore advances the "
    "Information Technology Management specialization by explaining how IT leaders "
    "translate competing stakeholder claims into enforceable recovery authority and "
    "defensible proof when recovery is outsourced."
)

GENERAL_PROBLEM = (
    "The general problem is that many U.S. small and medium-sized enterprises (SMEs) "
    "suffer avoidable organizational harm during cyber disruptions because they fail "
    "to consistently translate IT Disaster Recovery as a Service (ITDRPaaS) capabilities "
    "into governed, auditable, and defensible recoverability assurance (Federal Bureau "
    "of Investigation, 2024; Verizon, 2025). This inconsistency is particularly "
    "pronounced when decision authority is fragmented and oversight is applied "
    "inconsistently under pressure (Lowry et al., 2025; Park et al., 2023). Consequently, "
    "these disruptions lead to prolonged system downtime, uneven or slow recovery "
    "processes, compromised data integrity, and a diminished ability to demonstrate "
    "that restoration actions meet acceptable operational and risk thresholds during "
    "crisis conditions (Lowry et al., 2025; Park et al., 2023). This issue is most "
    "acutely felt by IT and network managers within U.S. SMEs, who bear responsibility "
    "for recovery while coordinating across internal teams and external service "
    "providers in environments where stakeholder priorities are often in flux "
    "(Molete et al., 2025). Furthermore, existing governance arrangements frequently "
    "fail to establish clear decision rights, accountability structures, or "
    "time-sensitive escalation pathways (Mitchell et al., 1997; Park et al., 2023). "
    "Despite increasing scholarship on IT centralization, resilience, and cybersecurity "
    "oversight, research remains limited on how U.S. SME IT and network managers "
    "operationalize disaster-recovery governance in practice when shifting stakeholder "
    "priorities undermine decision rights, escalation pathways, and standards for "
    "defensible recoverability assurance (Lowry et al., 2025; Park et al., 2023)."
)

SPECIFIC_PROBLEM = (
    "The specific problem is that many U.S. SMEs do not proactively establish an "
    "operational disaster-recovery capability characterized by clearly defined "
    "decision rights, escalation pathways, and evidentiary standards prior to a "
    "disruption (Lowry et al., 2025; Park et al., 2023). Instead, recovery efforts "
    "are often undertaken reactively, increasing exposure to data-integrity failures, "
    "inconsistent restoration actions, and poorly defensible recovery outcomes when "
    "urgent decisions bypass established governance controls (Lowry et al., 2025). "
    "In SMEs using ITDRPaaS, shifts in stakeholder salience—power, legitimacy, and "
    "urgency—can disrupt established priorities during incidents (Mitchell et al., "
    "1997). This disruption may destabilize decision-making authority, complicate "
    "escalation, and alter the criteria used to assess adequate proof of recoverability "
    "(Donaldson & Preston, 1995; Freeman et al., 2020; Mitchell et al., 1997). "
    "Consequently, restoration priorities and thresholds for recovery proof may be "
    "renegotiated mid-incident, producing governance inconsistencies, disputes over "
    "what qualifies as good-enough recovery, and uneven recovery performance across "
    "SME environments (Dorobantu et al., 2024; Lowry et al., 2025)."
)

GAP = (
    "Stakeholder theory provides the overarching frame that organizations create and "
    "protect value by managing competing stakeholder claims and sustaining legitimacy "
    "(Donaldson & Preston, 1995; Freeman et al., 2004). Freeman et al. (2020) update "
    "that frame as value-creation stakeholder theory: managers and other actors "
    "cooperatively create and trade value, and apparent tensions between stakeholder "
    "management and strategic-technical tasks are often differences of narrative "
    "rather than mutually exclusive jobs. The literature does not yet explain how "
    "that claim-management work is enacted inside SME ITDRPaaS governance when cyber "
    "disruption forces time-critical recovery choices (Freeman et al., 2020; Lowry "
    "et al., 2025). Within that frame, stakeholder-salience theory specifies the "
    "attention mechanism: power, legitimacy, and urgency determine whose claims count "
    "during incidents (Mitchell et al., 1997). Research remains limited on how SME "
    "IT managers translate those salience shifts into decision rights, escalation "
    "pathways, and evidence standards that make recoverability assurance defensible "
    "to stakeholders (Lowry et al., 2025; Mitchell et al., 1997). This gap matters "
    "to SME IT managers and the stakeholder groups that depend on their services "
    "because unclear authority and contested proof can yield inconsistent recovery "
    "and disputed restoration legitimacy (Donaldson & Preston, 1995; Lowry et al., "
    "2025). It matters now because stakeholder evaluations and legitimacy judgments "
    "move rapidly in contemporary information environments (Dorobantu et al., 2024). "
    "This study therefore addresses a program-aligned Information Technology "
    "Management gap by examining how stakeholder-claim management and salience "
    "shifts are described and enacted in SME ITDRPaaS governance, clarifying how "
    "decision-right alignment can support defensible recoverability assurance rather "
    "than ad hoc restoration practice (Freeman et al., 2020; Mitchell et al., 1997)."
)

PRIMARY_ORIENTATION = (
    "This study is primarily oriented to stakeholder-salience theory as developed by "
    "Mitchell et al. (1997) and situated within broader stakeholder scholarship "
    "(Donaldson & Preston, 1995; Freeman et al., 2004, 2020). Value-creation "
    "stakeholder theory states why competing claims matter: recovery is cooperative "
    "value creation and trade among interdependent parties, not a single-objective "
    "technical restore (Freeman et al., 2020). Stakeholder-salience theory then "
    "explains that organizational actors prioritize those claims based on managerial "
    "judgments of perceived power, legitimacy, and urgency (Mitchell et al., 1997; "
    "Dorobantu et al., 2024). In SME ITDRPaaS environments this lens is relevant "
    "because disruption compresses time and intensifies conflict over priorities, "
    "authority, and acceptable proof of recovery (Lowry et al., 2025). The literature "
    "review is warranted because current scholarship does not specify how SME IT "
    "managers operationalize salience judgments into executable recovery governance "
    "during named incidents—who is authorized to decide, when escalation occurs, and "
    "what evidence is accepted as sufficient proof of recoverability (Freeman et al., "
    "2020; Lowry et al., 2025). Accordingly, the study uses generic qualitative "
    "inquiry to analyze IT-manager accounts of stakeholder interactions, decision "
    "points, escalation episodes, and evidence-definition practices (Caelli et al., "
    "2003; Kahlke, 2014)."
)

EFFORTS = (
    "Prior studies examined SME IT and network managers’ accounts of recovery "
    "governance through stakeholder-salience theory (Mitchell et al., 1997). "
    "Stakeholder-salience research shows that organizational actors prioritize "
    "claims based on perceived power, legitimacy, and urgency, which shapes which "
    "claims receive attention and which recovery actions are authorized in "
    "time-sensitive decisions (Mitchell et al., 1997). In SME ITDRPaaS environments, "
    "that lens is appropriate because disruption compresses decision time and "
    "intensifies conflict over priorities, authority, and acceptable proof of "
    "recovery (Lowry et al., 2025; Park et al., 2023). The present study focuses on "
    "how SME IT and network managers describe and operationalize those judgments "
    "during real incidents: which roles are authorized to decide, when escalation "
    "is triggered, and what evidence is accepted as sufficient proof of "
    "recoverability. Generic qualitative interviews will collect those named-event "
    "accounts rather than vendor, executive-only, or compliance-checklist views "
    "(Caelli et al., 2003; Kahlke, 2014)."
)

METHOD_DUP = (
    "The study’s methodological approach is a generic qualitative inquiry (GQI), "
    "selected to investigate how U.S. SME IT and network managers perceive and "
    "interpret the governance challenges associated with establishing and managing "
    "ITDRPaaS (Caelli et al., 2003; Kahlke, 2014; Percy et al., 2015). This approach "
    "aligns with the topic and problem because it prioritizes managers’ sense-making "
    "of operational recovery processes over a confirmatory audit of written plans "
    "(Percy et al., 2015). GQI interview practice uses a flexible protocol that "
    "probes for clarification in participants’ terms. Thematic analysis uses prior "
    "literature as orientation rather than a rigid coding mandate (Braun & Clarke, "
    "2019; Fereday & Muir-Cochrane, 2006). Honoring participants’ accounts is both "
    "an ethical and a methodological discipline: it protects their descriptions, "
    "makes researcher influence visible, and keeps interpretations accountable to "
    "the named incident."
)

POPULATION = (
    "The target population comprises IT and network managers (or equivalent titles "
    "such as systems, infrastructure, or IT operations managers) employed by U.S. "
    "small and medium enterprises of 10 to 200 employees (Ekinci et al., 2025). "
    "Eligible participants have responsibility for, or direct participation in, IT "
    "disaster recovery involving an external platform or managed recovery service "
    "(ITDRPaaS or functionally equivalent cloud recovery). Population characteristics "
    "therefore center on role authority, U.S. SME employment, and recent "
    "platform-mediated recovery exposure rather than executive-only or vendor-side "
    "perspectives. The study is not limited to a single organizational site; "
    "participants will be drawn from multiple U.S. SME contexts in which IT systems "
    "are operationally critical. The locked sample is 12 interviews. That number is "
    "justified by information power for a narrow aim and a specific population "
    "(Malterud et al., 2016) and is the school-required fixed count rather than a "
    "range. Guest et al. (2006) is reserved for later stopping discussion only and "
    "is not the interview method."
)

CONSTRUCTS_1 = (
    "The theoretical framework is stakeholder theory as the broad foundation, "
    "operationalized through stakeholder-salience theory (Mitchell et al., 1997) and "
    "updated by value-creation stakeholder theory (Freeman et al., 2020). That "
    "framework informs the project in three ways. First, Freeman et al. (2020) "
    "justify treating recovery as cooperative value creation and trade among "
    "interdependent stakeholders rather than as a purely technical restore. Second, "
    "Mitchell et al. (1997) supply the sensitizing attributes—power, legitimacy, and "
    "urgency—that organize interview probes about whose claim counted in a named "
    "incident. Third, decision rights, escalation, evidentiary standards, and "
    "recoverability assurance are treated as enactment constructs: they are how "
    "salience becomes (or fails to become) recoverable, defensible action (Lowry "
    "et al., 2025; Park et al., 2023). The central phenomenon is therefore how U.S. "
    "SME IT and network managers interpret and operationalize ITDRPaaS governance "
    "during disruptions, failovers, recovery tests, and production-recovery events. "
    "These labels remain sensitizing probes. They are not predetermined Chapter IV "
    "theme titles and they are not quantitative variables."
)

CONSTRUCTS_2 = (
    "This study does not operationalize independent or dependent variables. "
    "Constructs function as interpretive lenses in a generic qualitative inquiry "
    "(Caelli et al., 2003; Percy et al., 2015). If a participant names ISO, NIST, "
    "or BCM materials, those names are context in the spoken account. They are not "
    "coding systems, treatment conditions, or researcher-administered checklists. "
    "The study does not use experimental manipulation, a Likert salience inventory, "
    "or a hypothesized path model. Semi-structured critical-incident interviews will "
    "be used to explore how managers encounter the constructs in one named event, "
    "producing descriptive thematic insight rather than population-level causal "
    "inference (Flanagan, 1954; Chell, 2004). The framework remains anchored in "
    "stakeholder-salience theory: managers prioritize stakeholder claims through "
    "power, legitimacy, and urgency (Mitchell et al., 1997)."
)

MEASURES_1 = (
    "Data will be collected through interviews only. The primary instrument is a "
    "researcher-developed, semi-structured critical-incident interview guide "
    "(ITDR-GQI-INT-v0.1.1) designed to explore how U.S. SME IT and network managers "
    "describe disaster-recovery governance during one named disruption, failover, "
    "recovery test, or operational recovery in the preceding 36 months (Caelli et "
    "al., 2003; Flanagan, 1954; Percy et al., 2015). The guide is aligned with "
    "stakeholder-salience theory and with this study’s enactment constructs: power, "
    "legitimacy, urgency, decision rights, escalation, evidentiary standards, and "
    "recoverability assurance (Mitchell et al., 1997). Theoretical words stay in the "
    "researcher codebook. Spoken questions use manager language."
)

MEASURES_2 = (
    "Interview-guide development will continue as a documented next step and does "
    "not have to be completed during this course. After the protocol is locked for "
    "wording, the researcher will convene a small subject-matter-expert (SME) panel "
    "of IT-recovery or qualitative-methods reviewers who will not later sit as "
    "study participants. The panel will review question clarity, neutrality, "
    "construct coverage, and alignment to the primary research question and to "
    "stakeholder-salience theory. The purpose of SME review is to reduce leading "
    "stems and to confirm that each item can elicit a named-event account rather "
    "than a generic “how we usually recover” answer. The researcher will then "
    "conduct two to three mock interviews or a pilot test with individuals who "
    "match the professional profile but are excluded from the n = 12 sample. The "
    "purpose of the mock or pilot is to time the 60–75 minute protocol, test skip "
    "rules, and revise probes before IRB-approved data collection. Expert review "
    "and pilot testing are instrument-development steps, not additional data sources."
)

MEASURES_3 = (
    "The interview protocol includes a required critical-incident opening (Q0) and "
    "follow-up sets that are asked only if the opening story did not already supply "
    "a concrete example. No organizational documents will be collected. If a "
    "manager names a log, ticket, approval, or matrix, the researcher will ask what "
    "that record did in the event; the spoken description remains interview data. "
    "The four-column alignment matrix below maps each numbered interview question "
    "to the primary research question and to the theoretical framework "
    "(stakeholder-salience theory; Mitchell et al., 1997), with value-creation "
    "stakeholder theory (Freeman et al., 2020) as the Need / What We Know foundation "
    "rather than as a spoken construct."
)

PROCEDURES_1 = (
    "Operational procedures begin with purposive and criterion sampling to identify "
    "qualified participants (Koerber & McMichael, 2008; Percy et al., 2015). The "
    "locked sample is 12. Inclusion requires service as an IT or network manager "
    "(or equivalent systems, infrastructure, or IT operations role) in a U.S. SME "
    "of 10 to 200 personnel (Ekinci et al., 2025); direct operational responsibility "
    "for, or participation in, IT disaster-recovery coordination that uses an "
    "external platform or managed recovery service; and at least one disruption, "
    "failover, recovery test, or operational recovery in the preceding 36 months. "
    "Vendor-only employees and managers who cannot name a qualifying event are "
    "excluded. After eligibility is verified, the researcher emails the informed "
    "consent form; once signed electronic consent is returned, a virtual, recorded "
    "English interview is scheduled."
)

PROCEDURES_2 = (
    "The second phase is the semi-structured interview. The session opens with a "
    "standardized ethics script, then uses the critical-incident technique "
    "(Flanagan, 1954; Chell, 2004; Butterfield et al., 2005). The participant is "
    "asked to walk through one specific recovery or testing incident. The researcher "
    "guides the dialogue with open-ended questions and flexible probes anchored in "
    "stakeholder-salience theory (Mitchell et al., 1997). Probes address whose "
    "request or pressure moved restore order, whose claim was treated as rightful, "
    "what made one service time-critical, who was supposed to decide versus who "
    "did, what if anything was escalated, and what counted as enough proof that "
    "the service was recovered. Guest et al. (2006) is not the interview method."
)

PROCEDURES_3 = (
    "Data collection is interviews only. The researcher will not collect, score, or "
    "audit disaster-recovery plans, escalation matrices, ISO, NIST, or BCM documents. "
    "If the participant names such a record, the researcher will ask what it did in "
    "the incident and record that spoken account. After the session, the recording "
    "is transcribed verbatim. To support credibility, the researcher will send a "
    "de-identified transcript for a seven-day factual member check of sequence, "
    "roles, and what was named as proof (Lincoln & Guba, 1985). Member checking "
    "does not require approval of final themes."
)

TRUST = (
    "This project uses the qualitative trustworthiness criteria of credibility, "
    "dependability, confirmability, and transferability (Lincoln & Guba, 1985). "
    "Credibility will be supported by critical-incident interviews, a seven-day "
    "factual member check, SME-panel review of the interview guide, and two to "
    "three mock or pilot interviews before the n = 12 corpus is collected "
    "(Moser & Korstjens, 2023). Dependability will be supported by a dated audit "
    "trail of protocol versions, codebook changes, and analytic memos (Carcary, "
    "2020). Confirmability will be supported by reflexive memos that separate "
    "participant accounts from researcher interpretation. Transferability will be "
    "supported by rich, de-identified descriptions of incident context without "
    "naming employers, vendors, or products. Expert review and pilot testing "
    "belong to instrument development; they are not a second data-collection "
    "stream and they are not used as findings."
)

DATA_COLL_1 = (
    "Following institutional approval, the researcher will finalize the "
    "semi-structured interview protocol, consent form, and screening instrument. "
    "The protocol will be reviewed by an SME panel and tested in two or three mock "
    "or pilot interviews with individuals who meet the professional profile but "
    "will not enter the n = 12 sample. Pilot feedback will assess question clarity, "
    "neutrality, construct coverage, sequencing, and probe usefulness. Revisions "
    "will keep the questions aligned with generic qualitative inquiry and with the "
    "conceptual chain: stakeholder salience, decision rights, escalation pathways, "
    "evidentiary standards, and recoverability assurance (Caelli et al., 2003; "
    "Mitchell et al., 1997; Percy et al., 2015)."
)

DATA_COLL_2 = (
    "Critical-incident prompts will ask participants to describe one specific "
    "disruption, failover, recovery test, or restoration event. Follow-up probes "
    "will examine what occurred, who made or influenced decisions, how competing "
    "demands were prioritized, when escalation occurred, and what was treated as "
    "proof of recovery (Flanagan, 1954; Chell, 2004). No artifacts will be "
    "requested or collected. If a manager names a matrix, ticket, or test record, "
    "that naming is part of the interview account."
)

DATA_COLL_3 = (
    "After each interview, the recording will be transcribed, checked against the "
    "audio, de-identified, and assigned a participant code. The researcher will "
    "prepare field notes and reflexive memos. Participants may be contacted to "
    "clarify materially ambiguous statements without being asked to approve the "
    "researcher’s final interpretation. Verified transcripts and audit-trail "
    "documentation will be imported into Delve for organization and retrieval "
    "during hybrid deductive–inductive codebook thematic analysis. Delve will "
    "support data management and coding; the analytic method remains thematic "
    "analysis (Fereday & Muir-Cochrane, 2006; Carcary, 2020)."
)

ANALYSIS_1 = (
    "The researcher will analyze de-identified critical-incident interviews from "
    "the locked sample of 12 U.S. SME IT, network, systems, infrastructure, or "
    "operations managers using hybrid deductive–inductive codebook thematic "
    "analysis within a generic qualitative inquiry (Caelli et al., 2003; Fereday "
    "& Muir-Cochrane, 2006; Kahlke, 2014; Percy et al., 2015). Before coding, the "
    "researcher will complete a scope register that records the purpose, research "
    "question, framework role, eligibility rules, participant count, and required "
    "deliverables, and will keep three work areas separate: preserved RAW "
    "recordings, CLEAN analytic files, and presentation outputs. Each interview "
    "will receive a stable identifier. The researcher will produce a verbatim "
    "transcript, strip person, firm, vendor, and product names, complete a "
    "seven-day factual member check, and read each CLEAN transcript in full before "
    "formal coding (Lincoln & Guba, 1985). Delve will store CLEAN transcripts, the "
    "versioned codebook, memos, and snippet URLs. Delve will not perform the analysis."
)

MATRIX_ROWS = [
    ["Primary RQ", "Q0. Please walk me through one specific disruption, failover, recovery test, or operational recovery in the last 36 months where you used an external recovery platform or managed recovery service.", "Anchors the RQ in one named ITDRPaaS event rather than a general opinion about recovery.", "Critical-incident account in which value-creation claims (Freeman et al., 2020) and salience attributes can be observed (Mitchell et al., 1997)."],
    ["Primary RQ", "L1. In that event, who actually moved what got restored first—or who could have stopped it?", "Locates whose claim counted when restoration was ranked.", "Power/legitimacy/urgency enacted as pull; not a fourth attribute."],
    ["Primary RQ", "L2. What gave that person or group the ability to move the decision—their position, a written rule, the clock, something else?", "Identifies the source of that pull in the same event.", "Maps the claim to power, legitimacy, and/or urgency (Mitchell et al., 1997)."],
    ["Primary RQ", "L3. If that pull had not been there, what would you have done differently?", "Shows how competing priorities changed the recovery decision.", "Counterfactual on salience-driven prioritization."],
    ["Primary RQ", "A1. Whose request or pressure most affected what got restored first?", "Power aspect of competing stakeholder priorities.", "Power: capacity to force, withhold, delay, or override (Mitchell et al., 1997)."],
    ["Primary RQ", "A2. Was there anyone who could delay, override, or stop a recovery action you thought was right?", "Power as unused or opposing pressure.", "Power boundary case."],
    ["Primary RQ", "B1. Whose claim to a service or a recovery order did people treat as having a right to ask for it?", "Legitimacy of competing claims.", "Legitimacy: claim treated as rightful (Mitchell et al., 1997)."],
    ["Primary RQ", "B2. Was anyone’s request treated as out of line or outside their role? What happened then?", "Contested legitimacy during governance.", "Legitimacy boundary case."],
    ["Primary RQ", "C1. What made one service or one stakeholder more time-critical than another in that event?", "Urgency as a driver of recovery priority.", "Urgency: time sensitivity and criticality (Mitchell et al., 1997)."],
    ["Primary RQ", "C2. Did that sense of time pressure change while you were working the incident? What changed it?", "Mid-incident salience shift.", "Urgency as amplifier during the event."],
    ["Primary RQ", "D1. Who was supposed to make the call on that tradeoff, and who actually made it?", "Decision-rights part of ITDRPaaS governance.", "Enactment of whose claim counted; framework remains PLU."],
    ["Primary RQ", "D2. Was there a moment when you needed authority you did not have? What did you do?", "Missing or bypassed decision rights.", "Authority gap under salience pressure."],
    ["Primary RQ", "E1. What, if anything, triggered an escalation?", "Escalation as a governance action under competing priorities.", "How a stalled claim was moved upward or outward."],
    ["Primary RQ", "E2. Did escalation speed the restoration, slow it, or change what done meant?", "Effect of escalation on recovery governance.", "Salience translated into pathway and outcome."],
    ["Primary RQ", "F1. When you told others the service was recovered, what did you treat as enough proof?", "Evidentiary standard in the named event.", "What counted as defensible recoverability."],
    ["Primary RQ", "F2. Did anyone ask for different proof mid-incident? What did you do?", "Renegotiated proof under stakeholder pressure.", "Salience shift enacted as a changed evidence threshold."],
    ["Primary RQ", "F3. Looking back, what would you point to if you had to defend that restoration?", "Recoverability assurance as spoken defense, not a collected file.", "Defensible proof of value restored for stakeholders (Freeman et al., 2020; Lowry et al., 2025)."],
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, OUT)
    doc = Document(OUT)
    p = doc.paragraphs

    replace_text(p[17], ALIGN_1)
    replace_text(p[18], ALIGN_2)
    replace_text(p[23], GENERAL_PROBLEM)
    replace_text(p[24], SPECIFIC_PROBLEM)
    replace_text(p[28], GAP)
    replace_text(p[34], PRIMARY_ORIENTATION)
    replace_text(p[39], EFFORTS)
    replace_text(p[62], "ITDRPaaS. A governance-centered recovery capability in which an SME structures authority, escalation, and oversight so recovery decisions can be executed and defended under disruption rather than relying on tools or contracts that do not hold under pressure (Lowry et al., 2025).")
    replace_text(p[63], "Information Technology Disaster Recovery as a Service (ITDRPaaS). Use the ITDRPaaS definition above; the longer expansion is the same construct, not a second term.")
    replace_text(p[65], "Stakeholder-salience dynamics. The disruption-driven shifting dominance of stakeholder claims—based on power, legitimacy, and urgency—that determines whose priorities and risk tolerances govern time-critical recovery tradeoffs (Mitchell et al., 1997).")
    replace_text(p[66], "Decision-rights governance. The explicit allocation of who is authorized to make specific recovery decisions, including speed-versus-integrity tradeoffs, so that IT strategy intent can be converted into executable action without ad hoc authority disputes (Park et al., 2023). Time-critical escalation pathways. Pre-specified authority transitions and trigger rules that accelerate decision movement when urgency rises (Park et al., 2023).")
    replace_text(p[68], "SME IT/network manager. The accountable operational governance actor who coordinates interdependent recovery actions across internal teams and external providers while maintaining credible oversight of continuity decisions under time pressure (Park et al., 2023).")
    replace_text(p[76], METHOD_DUP)
    replace_text(p[82], POPULATION)
    replace_text(p[87], CONSTRUCTS_1)
    replace_text(p[89], CONSTRUCTS_2)
    replace_text(p[95], MEASURES_1)
    replace_text(p[96], MEASURES_2)
    replace_text(p[97], MEASURES_3)
    replace_text(p[102], PROCEDURES_1)
    replace_text(p[103], "The locked sample remains 12 throughout screening, scheduling, and analysis. That count is not a finding that the gap is closed.")
    replace_text(p[104], PROCEDURES_2)
    replace_text(p[105], PROCEDURES_3)
    replace_text(p[109], TRUST)
    replace_text(p[133], DATA_COLL_1)
    replace_text(p[134], DATA_COLL_2)
    replace_text(p[135], DATA_COLL_3)
    replace_text(p[146], ANALYSIS_1)

    # interviews-only cleanup in remaining long analysis paras
    for idx in (147, 148, 149):
        t = p[idx].text
        t = t.replace("and optional artifact maps ", "")
        t = t.replace("and artifact map", "")
        t = t.replace("artifact type, ", "")
        t = t.replace("and artifact maps", "")
        t = t.replace("Path B verbal reconstructions and Path C “no reviewable artifact named” rows. ", "")
        t = t.replace("CLEAN transcript and artifact map", "CLEAN transcript")
        if t != p[idx].text:
            replace_text(p[idx], t)

    for idx in (117, 127, 139):
        t = p[idx].text.replace("10 to 15", "12").replace("10-15", "12")
        if "sample of 10" in t:
            t = t.replace("sample of 10 to 15", "sample of 12")
        if t != p[idx].text:
            replace_text(p[idx], t)

    # broken / incomplete references
    replace_text(
        p[172],
        "Federal Bureau of Investigation. (2024). Internet crime report 2024. https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf",
    )
    replace_text(p[175], "")
    run = p[175].add_run(
        "Freeman, R. E., Phillips, R., & Sisodia, R. (2020). Tensions in stakeholder theory. Business & Society, 59(2), 213–231. "
    )
    set_run_font(run)
    add_hyperlink(p[175], "https://doi.org/10.1177/0007650318773750", "https://doi.org/10.1177/0007650318773750")
    replace_text(
        p[190],
        "Kvale, S., & Brinkmann, S. (2015). InterViews: Learning the craft of qualitative research interviewing (3rd ed.). SAGE.",
    )
    # insert Capella catalog after Caelli
    insert_paragraph_after(
        p[159],
        "Butterfield, L. D., Borgen, W. A., Amundson, N. E., & Maglio, A.-S. T. (2005). Fifty years of the critical incident technique: 1954–2004 and beyond. Qualitative Research, 5(4), 475–497. https://doi.org/10.1177/1468794105056924",
    )
    insert_paragraph_after(
        p[161],
        "Capella University. (2024). University catalog: Doctor of Philosophy (PhD) in Business Management, Information Technology Management specialization. Capella University.",
    )
    insert_paragraph_after(
        p[162],
        "Chell, E. (2004). Critical incident technique. In C. Cassell & G. Symon (Eds.), Essential guide to qualitative methods in organizational research (pp. 45–60). SAGE.",
    )
    insert_paragraph_after(
        p[174],
        "Flanagan, J. C. (1954). The critical incident technique. Psychological Bulletin, 51(4), 327–358. https://doi.org/10.1037/h0061470",
    )
    insert_paragraph_after(
        p[209],
        "Percy, W. H., Kostere, K., & Kostere, S. (2015). Generic qualitative research in psychology. The Qualitative Report, 20(2), 76–85. https://doi.org/10.46743/2160-3715/2015.2097",
    )

    note = insert_paragraph_after(
        p[97],
        "Interview question alignment matrix. Primary research question: What are the perceptions of U.S. SME IT/network managers regarding the establishment and governance of IT Disaster Recovery as a Service (ITDRPaaS) in environments where competing stakeholder priorities influence disaster recovery decisions? Theoretical framework: stakeholder-salience theory (Mitchell et al., 1997), grounded in value-creation stakeholder theory (Freeman et al., 2020).",
    )
    insert_table_after(
        note,
        [
            "RQ",
            "Interview questions (numbered)",
            "Alignment to RQ",
            "Alignment to theoretical framework",
        ],
        MATRIX_ROWS,
    )

    # hyperlink a few already-present DOIs that were plain text
    for idx, url in (
        (159, "https://doi.org/10.1080/2159676X.2019.1628806"),
        (197, "https://doi.org/10.5465/amr.1997.9711022105"),
    ):
        # leave existing text; do not rebuild those rows here
        _ = (idx, url)

    doc.save(OUT)
    ART.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT, ART)
    print("wrote", OUT)
    print("artifact", ART)


if __name__ == "__main__":
    main()
