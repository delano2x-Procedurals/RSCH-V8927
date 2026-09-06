# Change tracking update (usage + Gibran inclusion)

**Date:** 6 September 2026  
**Working Word file:** `downloads/MW_Wk5_to_wk8_Edit_6Sep26.docx` (same bytes as `downloads/MW_Wk5_to_wk8_Edit_6Sep26_updated.docx`)  
**Word now includes:** front-matter Gibran epigraph (On Work) plus an end appendix with the usage/tracking log and all Gibran inclusion statements.  
**Instructor file (do not overwrite):** `source/originals/MW_Wk5_to_wk8_Edit_5Sep26.docx` (Marc’s 36 comments)  
**Course trail:** BMGT-8044 → RSCH-V8927  
**Researcher:** Max D. Walker  
**Branch:** `cursor/need-for-study-opening-2c68`

Use this file as the usage log. It says what changed, where to paste it, what must not move, and which Gibran lines may be included.

---

## How to use this file

| If you need to… | Open |
| --- | --- |
| Paste Chapter I Need / specialization / VCST | [chapter-i-need-for-the-study.md](chapter-i-need-for-the-study.md) |
| See what Marc’s comments closed | [wk8-comment-response.md](wk8-comment-response.md) |
| Paste a current APA list (U.S. preference applied) | [us-based-references.md](us-based-references.md) |
| See the earlier currency/swap list | [updated-references.md](updated-references.md) |
| Check in-text ↔ list alignment | [citation-alignment-audit.md](citation-alignment-audit.md) |
| Lock construct placement (VCST vs PLU) | [symbols-definitions-refs.md](symbols-definitions-refs.md) |
| Speak the interview | [gqi-semistructured-interview-guide.md](gqi-semistructured-interview-guide.md) (`ITDR-GQI-INT-v0.1.1`) |
| Include a Gibran epigraph | [Gibran statements for inclusion](#gibran-statements-for-inclusion) in this file |

---

## Locked study facts (do not drift)

| Item | Locked value |
| --- | --- |
| Program / specialization | PhD in Business Management, Information Technology Management (Capella) |
| Method | Generic qualitative inquiry (GQI); critical-incident interviews |
| Official RQ (Word file) | Perceptions of U.S. SME IT/network managers regarding establishment and governance of ITDRPaaS where competing stakeholder priorities influence DR decisions |
| Unit of analysis | One U.S. SME IT / network / systems / infrastructure / operations manager; one named disruption, failover, test, or operational recovery in 36 months using external/managed recovery |
| SME size | 10–200 personnel (study screen). U.S. SBA (2026) supplies the federal small-firm bound (<500); the study still tightens to 10–200 |
| Sample | **12** (locked; not a range) |
| Collection | Interviews only. No artifact collection, no NIST/ISO/BCM scoring |
| Foundation theory | Stakeholder theory (Donaldson & Preston, 1995; Freeman et al., 2004) |
| Needed construct | Value-creation stakeholder theory (VCST) — Freeman, Phillips, & Sisodia (2020) |
| Operational lens | Stakeholder salience / PLU — Mitchell et al. (1997) |
| Analytic method | Hybrid deductive–inductive codebook thematic analysis (Fereday & Muir-Cochrane, 2006). Delve is CAQDAS only |
| Spoken protocol | Unchanged (`ITDR-GQI-INT-v0.1.1`) |
| Word comments | 36 remain in the working file |
| Gibran (1923) | Epigraph / front matter only. Not a scholarly claim |

**VCST placement.** Need / What We Know / Alignment / Gap foundation only. Not a spoken stem, Delve code, fourth salience attribute, or Chapter IV theme title. Does not replace Donaldson and Preston (1995), Freeman et al. (2004), or Mitchell et al. (1997).

---

## Working-file map

| File | Role |
| --- | --- |
| `downloads/MW_Wk5_to_wk8_Edit_6Sep26.docx` | Week 8 courseroom file. Marc’s comments intact. |
| `source/originals/MW_Wk5_to_wk8_Edit_5Sep26.docx` | Instructor original. Do not edit. |
| `docs/chapter-i-need-for-the-study.md` | Four-paragraph Need opening (fuller than the Word Alignment node) |
| `docs/change-tracking-update.md` | This usage / tracking log |
| `docs/updated-references.md` | Currency pass (keep / replace / drop). Gibran is now **include-epigraph** |
| `docs/us-based-references.md` | U.S.-preference pass actually applied in Word |
| `docs/citation-alignment-audit.md` | In-text / list check |
| `docs/wk8-comment-response.md` | Comment-by-comment closure |
| `docs/notion/templates/references.csv` | Register (includes `REF-FREEMAN-2020`, `REF-GIBRAN-1923`) |
| `workspace-app/` | README + Theory & spine Need block |

---

## Chronological change log

### Pass 1 — Need / specialization / VCST

**Ask:** Need for opening of the dissertation; state specialization and how the project aligns; add the needed construct (reviewer highlight: Freeman et al., 2020).

**Done**

- Wrote four paste-ready Need paragraphs in `docs/chapter-i-need-for-the-study.md`.
- Locked `VCST` on Need / What We Know only (`docs/symbols-definitions-refs.md`, `docs/notion/templates/symbols.csv`).
- Registered `REF-FREEMAN-2020` and `REF-CHAPTER-I-NEED`.
- Added a Need block on the workspace README and Theory & spine pages.
- Spoken interview protocol **not** changed.

**Usage.** Paste the four Need paragraphs into a Chapter I *Need for the Study* node when that heading exists. In this Project Plan template the matching node is **Alignment to the Program of Study** (see Pass 2). Do not paste the four paragraphs *and* the two Alignment paragraphs as a stack.

### Pass 2 — Apply opening to Marc’s Week 5–8 Project Plan

**Ask:** Update `MW_Wk5_to_wk8_Edit_5Sep26_.docx`. Keep comments intact.

**Done** (script: `scripts/edit_wk58_project_plan.py`)

| Node | Change |
| --- | --- |
| Alignment to the Program of Study (C1/C2) | Two paragraphs: ITM specialization + project alignment; VCST + Mitchell PLU + GQI. **Not** a separate Need heading |
| General problem (C3–C6) | Practice claims sourced; Erdiaw-Kwasie (2017) removed from that sentence |
| Gap (C7/C8) | Removed “to be GQI experienced.” Who cares / why now / Freeman 2020 / ITM alignment |
| Terms (C9/C10) | **Term. Definition** format |
| Method (C11) | Duplicate “Honoring experience…” sentence removed |
| Population (C12–C15) | 10–200 personnel |
| Sample (C16–C18) | Locked at 12 |
| Constructs (C19) | Stakeholder theory / Freeman 2020 / Mitchell 1997 |
| Measures (C20/C21–C26/C30) | Interviews only; SME panel + mock/pilot as next steps; 4-column RQ / IQ / RQ-alignment / framework-alignment table |
| Credibility (C27) | Credibility language |
| Audit (C31) | Dated audit trail |
| References (C34/C35) | APA 7th pass started; **not fully closed** |

**Integrity after Pass 2:** comments 36; body grew from 221 (original) to 228 paragraphs because of the interview-alignment table and interview-only / SME-pilot sentences.

### Pass 3 — Updated references (currency; same length)

**Ask:** Align citations; prefer most current; if not, mark **BOLD**; keep same length; also provide paste-ready replacements.

**Done**

- `docs/updated-references.md` + `/opt/cursor/artifacts/updated_references.md`
- Seminal keep set held.
- Ten verified replacements listed. Many list leftovers marked **BOLD**.
- Gibran (1923) was marked **drop (wrong source)** in that pass. **Superseded by this update** (see [Gibran](#gibran-statements-for-inclusion)).

### Pass 4 — U.S.-based references

**Ask:** Prefer U.S. settings / journals / authors / federal sources.

**Done in the Word file** (same-length in-text swaps; 36 comments kept; 228 paragraphs at that point)

| Old in-text | New in-text | Claim |
| --- | --- | --- |
| Ekinci et al., 2025 | U.S. Small Business Administration, 2026 | U.S. SME size class |
| Molete et al., 2025 | Ampel et al., 2024 | SME IT / cyber recovery practice |
| Korstjens & Moser, 2018 | Morse, 2015 | Credibility / rigor tactics |
| Carcary, 2020 | Paulus, 2023 | CAQDAS / audit-trail workflow |
| Naeem et al., 2024 | Guest, Namey, & Chen, 2020 | Saturation as an analytic decision |
| Miteu, 2024 | Resnik, 2018 | Research ethics / integrity |
| Braun & Clarke, 2019 | Saldaña, 2021 | Codes vs themes; meaning units |
| Nowell et al., 2017 | Tracy, 2010 | Qualitative quality / confirmability |
| Chell, 2004 | Gremler, 2004 | Organizational CIT application |
| Butterfield et al., 2005 | Gremler, 2004 | Same CIT cluster; Flanagan 1954 kept |

**List slots replaced-in:** Gremler (2004); Guest, Namey, & Chen (2020); Morse (2015); Paulus (2023); Resnik (2018); Saldaña (2021); U.S. Small Business Administration (2026).

**CIT tension (do not silently undo).** Workspace method rules still treat CIT as Flanagan / Chell / Butterfield. The U.S. pass put Gremler (2004) in-text with Flanagan (1954). If CIT lineage must be restored later, keep Flanagan and treat Gremler as the U.S. application.

**Guest (2006) vs Guest (2020).** Guest et al. (2006) stays for the reserved stopping-discussion sentence only. Guest, Namey, and Chen (2020) is the current U.S. companion for stopping as an analytic decision.

### Pass 5 — This update (usage tracking + Gibran inclusion)

**Ask:** Full update of changes for usage and tracking, including Gibran statements for inclusion.

**Done**

- This file is the master usage / tracking log.
- Gibran (1923) status changed from **drop** to **include-epigraph**.
- APA line restored in the Word reference list (alphabetically between Gabriel and Gremler).
- Register row `REF-GIBRAN-1923` added.
- Paste-ready Gibran statements supplied below. The recommended primary line is now the Project Plan epigraph. The remaining statements sit in the Word **Usage and Tracking Update** appendix. They are **not** inserted into Alignment, Gap, method, or findings.

**Length note.** The Word file is 262 paragraphs: Alignment / Gap / method body is unchanged; the added lines are the front-matter epigraph and the tracking appendix. Word comments remain 36.

### Pass 6 — Scholarly clarity + citation alignment (bolded updates)

**Ask:** Edit the highlighted methodology cluster for scholarly clarity; update necessary citations; **bold** the changes.

**Done in the Word file** (comments still 36)

| Old / problem | Now (bold in the Word file) |
| --- | --- |
| Creswell & Poth, 1998 / 2018 | **Creswell & Poth, 2024** |
| Ekinci et al., 2025 (SME size) | **U.S. Small Business Administration, 2026** |
| Vasileiou / Hennink “not statistical power” | **Wutich et al., 2024** |
| Naeem et al., 2024 (saturation as decision) | **Guest et al., 2020** |
| Carcary, 2020 (audit trail) | **Paulus, 2023** |
| Miteu, 2024 (ethics) | **Resnik, 2018** |
| “Inclusion criteria…” prose | **Inclusion.** / **Exclusion.** Term. Definition format |
| “stakeholders-salience participants”; “Findings and will”; “Delvetool”; broken Guest 2006 sentence | Corrected scholarly wording |

Malterud et al. (2016) stays (seminal information power). Guest et al. (2006) stays only for the reserved stopping-discussion sentence. Hennink & Kaiser (2022) is **not** used in-text (U.S. preference is Wutich et al., 2024).

---

## In-text citation map (current Word file)

Use this when editing later so swaps are not reversed by accident.

| Claim | Current in-text | Do not put back |
| --- | --- | --- |
| ITM specialization / catalog | Capella University, 2024 | — |
| VCST (needed construct) | Freeman et al., 2020 | — |
| Stakeholder-claim management | Donaldson & Preston, 1995; Freeman et al., 2004 | — |
| Salience / PLU | Mitchell et al., 1997 | — |
| Why-now legitimacy clock | Dorobantu et al., 2024 | — |
| Cyber / recovery practice | FBI, 2024; Verizon, 2025; Lowry et al., 2025; Park et al., 2023; Ampel et al., 2024 | Molete et al., 2025 (list leftover only) |
| U.S. small-firm bound | U.S. Small Business Administration, 2026 | Ekinci et al., 2025 |
| GQI design | Caelli et al., 2003; Kahlke, 2014; Percy et al., 2015 | — |
| CIT opening | Flanagan, 1954; Gremler, 2004 | Chell / Butterfield in-text (list leftovers) |
| Hybrid TA method | Fereday & Muir-Cochrane, 2006 | — |
| Codes vs themes | Saldaña, 2021 | Braun & Clarke, 2019 in-text |
| Information power / n | Malterud et al., 2016; Wutich et al., 2024 | — |
| Saturation as decision | Guest et al., 2020 | Naeem et al., 2024 in-text |
| Stopping-discussion (named) | Guest et al., 2006 | Using 2006 as the interview method |
| Credibility | Morse, 2015; Lincoln & Guba, 1985 | Korstjens & Moser, 2018 in-text |
| Quality / confirmability | Tracy, 2010 | Nowell et al., 2017 in-text |
| CAQDAS / audit trail | Paulus, 2023 | Carcary, 2020 in-text |
| Ethics | Resnik, 2018; Belmont, 1979 | Miteu, 2024 in-text |
| Worldview / five approaches book | Creswell & Poth, 2024 | Creswell & Poth, 1998 |
| Epigraph (optional) | Gibran, 1923 | Using Gibran for SME size, salience, method, or findings |

**Lowry et al. (2025)** is Lowry, Vance, and Vance, *Inexpert supervision*, *Management Science*, https://doi.org/10.1287/mnsc.2023.04147. It is not Lowry, Petter, and Leimeister. Park et al. (2023) is the U.S. crisis-IT / resilience source. Neither paper is a dedicated “recoverability assurance” definition source.

---

## Gibran statements for inclusion

**Source (U.S., public domain):** Gibran, K. (1923). *The prophet*. Alfred A. Knopf.  
**Status:** **include-epigraph**. Restored after the currency pass had marked it drop (wrong scholarly source).  
**Allowed use:** front matter, dedication, or a section epigraph.  
**Forbidden use:** SME size, salience / PLU definitions, VCST, GQI/CIT/TA method, saturation, ethics, findings, or theme titles. Gibran does **not** replace Freeman et al. (2020).

APA 7th list line (now in the Word References node):

Gibran, K. (1923). *The prophet*. Alfred A. Knopf.

Lines below are from the 1923 Knopf text (U.S. public-domain wording). Include **one** as the Project Plan / dissertation epigraph unless a committee asks for more.

### Recommended primary (On Work) — IT-manager labor under recovery

> Work is love made visible.

*Gibran, 1923, On Work*

**Place:** title page, dedication, or opening of Alignment / Need.  
**Not this:** method source; proof that recovery work is “love”; a construct.

Optional companion line from the same sermon (use only if a second line is wanted):

> And all work is empty save when there is love.

*Gibran, 1923, On Work*

### Recommended secondary (On Giving) — cooperative value / recovery

> You give but little when you give of your possessions. It is when you give of yourself that you truly give.

*Gibran, 1923, On Giving*

**Place:** front matter near the VCST sentence, or a Chapter I epigraph on cooperative recovery.  
**Not this:** a substitute for Freeman, Phillips, and Sisodia (2020). VCST remains the scholarly construct.

### Optional (On Laws) — plans versus enacted decision rights

> You delight in laying down laws, yet you delight more in breaking them.

*Gibran, 1923, On Laws*

**Place:** epigraph before Constructs or Measures if the tone is plans vs enacted rights.  
**Not this:** NIST / ISO / BCM scoring; a finding that managers break policy.

### Optional (On Talking) — interview / CIT stance

> You talk when you cease to be at peace with your thoughts.

*Gibran, 1923, On Talking*

**Place:** epigraph before the interview protocol or Chapter III collection.  
**Not this:** a GQI, CIT, or saturation citation.

### Optional (On Reason and Passion) — Chapter I tone

> Your reason and your passion are the rudder and the sails of your seafaring soul.

*Gibran, 1923, On Reason and Passion*

**Place:** optional Chapter I tone line.  
**Not this:** theory; PLU; recoverability assurance.

### Paste-ready epigraph block (copy one)

Use this format so the line is visibly an epigraph, not a literature claim:

> Work is love made visible.  
> — Kahlil Gibran, *The Prophet* (1923)

If the line is used, keep the Gibran (1923) reference-list entry. If no epigraph is used in a given submission, the list entry may stay (harmless) or be removed for that file only; do not delete it from this tracking log.

### Register lock

| Field | Value |
| --- | --- |
| `ref_id` | `REF-GIBRAN-1923` |
| Allowed | Epigraph / front matter / dedication |
| Do not use for | SME size; salience; VCST; method; ethics; findings; theme titles; spoken questions |
| Spoken protocol | Not spoken |
| Delve | Not a code |

---

## What is still open

| Item | Status |
| --- | --- |
| C34 / C35 full APA 7th of leftover list rows | Open. Leftovers stay **BOLD** |
| In-text **Lester et al., 2020** | U.S. write-up source; no verified 2021–2026 write-up partner. Leave unless a same-length swap is found |
| BOLD list leftovers (non-U.S. or dated, not swapped) | Brinkmann & Kvale 2017; Butterfield 2005; Cooper & Endacott 2007; Erdiaw-Kwasie 2017; Fischer 2020; Gabriel & Shafique 2024; Kvale & Brinkmann 2015; Liu 2020; Mojtahedi & Oo 2017; Molete 2025; Nowell et al. 2017; Örtenblad 2007; van der Kamp 2023; de Vaujany 2025; Vos 2022; plus unused U.S. leftovers still in the list (Creswell & Miller 2000; Fusch 2018; Kenny 2017; Koerber 2008; Lester 2020; Narayanan 2020; Nowell & Albrecht 2019; Stieb 2009; Williams 2017) |
| Official RQ labels vs workspace PQ1 / PQ2 | Word uses the official RQ wording. Workspace Need file still shows implied PQ1/PQ2. Labels may be replaced without changing the unit of analysis |
| Chell / Butterfield vs Gremler | U.S. in-text is Gremler + Flanagan. Do not silently revert |
| Unused current orphans | Some current sources sit in the list without in-text use. Do not balloon the list |

---

## Do-not-change list

- Marc’s 36 Word comments (replace run text; do not delete comment XML).
- Spoken interview stems (Q0, L, A–F) in `docs/gqi-semistructured-interview-guide.md`.
- Sample **n = 12**.
- Interviews only.
- VCST off Constructs / codebook / Chapter IV theme titles.
- Seminal keep set: Mitchell et al. 1997; Donaldson & Preston 1995; Freeman 1984; Freeman et al. 2004; Freeman, Phillips & Sisodia 2020; Flanagan 1954; Lincoln & Guba 1985; Caelli et al. 2003; Kahlke 2014; Percy et al. 2015; Fereday & Muir-Cochrane 2006; Malterud et al. 2016.
- Do not invent citations. Hot-link DOIs when a DOI exists.
- Do not use Gibran (1923) as support for an empirical or methodological claim.
