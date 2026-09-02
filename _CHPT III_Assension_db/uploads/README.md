# Incoming uploads (no RAW identifiers)

Drop later documentation, committee templates, theory notes, and workbook revisions here. This folder is part of `_CHPT III_Assension_db`. It is not a transcript store.

**Get and use the Excel offering:** [SOP-get-and-use-offering.md](SOP-get-and-use-offering.md) — where the file is, how to download it, how to rename a WORKING copy so the clean master stays clean.

## Already here

| File | Role |
| --- | --- |
| [`ITDRPaaS_Governance_Artifact_Workbook.xlsx`](ITDRPaaS_Governance_Artifact_Workbook.xlsx) | Uploaded operational offering (RACI, DR Plan, incident command, delegation, failover, risk exception, audit trail). Spine chain SAL → DR → ESC → AE → RA as an organizing model, not a proven theory. |
| [`ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx`](ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx) | Improved twin: Chapter I–V needed-item tabs, Theory, Qualitative, U.S. SME, Qualitative Analysis, Lit review, plus the original artifact sheets with a Chapter / dissertation-event column. Built by `python3 scripts/build_chiii_assension_workbook.py`. |

## How to add a file

1. Copy the file into this folder. Prefer de-identified names (`P##`, `SME-A`, `Platform-1`).
2. Append a row to [`../registers/crosswalk.csv`](../registers/crosswalk.csv) (`target_kind` = `upload` or `template`).
3. If the file is theory, also add or update a row in [`../templates/theory.csv`](../templates/theory.csv).
4. If the file is a Chapter I–V template, map it on the matching `templates/chapter-*-needed-items.csv`.
5. Do not overwrite a prior upload. Use a dated name (`YYYY-MM-DD-short-title.ext`).

## Do not upload

- RAW recordings or CLEAN transcripts with residual identifiers
- Credentials, IP addresses, customer identifiers, unredacted network diagrams
- Verbatim copyrighted chapters (link the citation instead)
