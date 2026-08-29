# Notion nest: interval CSV backups for the GQI instrument and Delve audit

This folder is the **offline nest** of the interview instrument until a Notion workspace is connected. Do not put identifiable transcripts here. De-identify first (`P##`, role only, `SME-A`, `Platform-1`).

Parent instrument: [../gqi-semistructured-interview-guide.md](../gqi-semistructured-interview-guide.md) (`ITDR-GQI-INT-v0.1.1`). Spoken wording is unchanged from v0.1.

Companions: [../chapter-iii-methodology.md](../chapter-iii-methodology.md) · [../symbols-definitions-refs.md](../symbols-definitions-refs.md)

## Folder layout

```
docs/notion/
  README.md                 (this file)
  templates/                (canonical headers + current working rows)
    references.csv
    interview-items.csv
    codebook.csv
    construct-index.csv
    leverage-memo.csv
    symbols.csv
    update-log.csv
    snippets.csv            (header only until Delve exports exist)
  interval-backups/
    YYYY-MM-DD/             (dated drop of the files above)
```

When Notion is available, create a parent page **ITDR-GQI audit nest** with one database per CSV. Database properties must match the CSV headers exactly so an interval export/import stays round-trippable.

## What each CSV is

| File | Updates when | Delve counterpart |
| --- | --- | --- |
| `references.csv` | A source is added, retired, or its allowed-use changes. Header includes `origin` and `citation_status`. | Not imported to Delve. Literature + instrument register. |
| `symbols.csv` | A symbol, operational def, or original/build-on link changes | Not imported to Delve as theme titles. Memo values only. |
| `interview-items.csv` | Spoken wording, skip rule, or status (`active` / `retired`) | Code descriptions may need a matching edit |
| `codebook.csv` | A structural, sensitizing, or boundary code is added, renamed, or merged | Delve codebook import / Codes export |
| `construct-index.csv` | Question ID or `code_id` mapping changes | Nested code names |
| `leverage-memo.csv` | After each interview | Delve memo on L1–L3 snippets |
| `snippets.csv` | After each Delve export | Delve Snippets CSV (keep snippet URLs) |
| `update-log.csv` | Every change or weekly `no_change` | Code-revision memos |

## Interval

- After each interview that is coded in Delve.
- At least weekly while coding is active.
- If nothing changed that week, append `type=no_change` to `update-log.csv` and still copy the running templates into a dated folder so the gap is visible.

## How to drop a backup

1. Export **Codes** and **Snippets** from Delve as CSV.
2. Copy `docs/notion/templates/*.csv` plus the two Delve exports into `docs/notion/interval-backups/YYYY-MM-DD/`.
3. Name Delve files `codebook.csv` (Codes) and `snippets.csv` (Snippets) in that dated folder. Do not overwrite `templates/codebook.csv` with a Delve export that has dropped the start-list descriptions.
4. Append one row to `templates/update-log.csv` (`type=delve_export` or `type=instrument_edit`).
5. Copy the updated `update-log.csv` into the same dated folder.

## How to update the instrument from this nest

1. Bump `instrument_version` in the markdown guide **before** changing question text.
2. Edit `templates/interview-items.csv`. Retired IDs stay in the file with `status=retired` and `replaced_by=` filled. Never reuse a retired ID.
3. If a construct or Delve code changed, edit `templates/codebook.csv` and `templates/construct-index.csv`, then update the Delve nest the same day. Write a Delve memo stating why.
4. Log the change in `templates/update-log.csv`.
5. Drop a dated backup (see above).

## Linking keys (do not rename)

- `instrument_id` / `instrument_version`
- `question_id` (`Q0`, `L1` … `F3`, `Q-close`)
- `code_id` (Delve nested name)
- `participant_id` (`P##`)
- Delve snippet URL (from Snippets export)

## Seminal vs new

`references.csv` column `origin` is one of:

- `original` — source that defines the symbol or method; do not replace
- `build_on` — later work that extends, tests, or situates the construct; not a replacement definition
- `software` — new software citation if not already in the Project Plan
- `new_instrument` — this protocol (`ITDR-GQI-INT-v0.1.1`); unpublished; not a theory source
- `audit_artifact` — dated CSV exports and Chapter III/glossary files; not literature

Column `citation_status` is `confirmed` or `verify` (use `verify` when a 2023–2025 DOI cannot be confirmed).

Column `ref_class` remains:

- `seminal_theory` — keep; do not replace
- `seminal_method` — keep; do not replace
- `seminal_trustworthiness` — keep; do not replace
- `software` — CAQDAS citation
- `new_instrument` — unpublished protocol
- `audit_artifact` — dated CSV exports; not literature
