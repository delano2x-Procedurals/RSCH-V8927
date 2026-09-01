# `_CHPT III_Assension_db`

Working database for Capella Chapter III (Methodology) after the `rsch-v8927` / `v8927_Build` workspace. Same `_db` sense as `Dissertation Spine_db` and `KEY WORD_db`.

The paste-ready chapter stays in [`docs/chapter-iii-methodology.md`](../docs/chapter-iii-methodology.md). This nest is the TOC, layout, how-to notes, spine map, and Alignment Map tester tracker. It does not rewrite spoken interview wording.

Instrument: `ITDR-GQI-INT-v0.1.1`. Analytic method: hybrid codebook thematic analysis (Fereday & Muir-Cochrane, 2006). Delve is CAQDAS support only.

## Start here

1. Open [`layout.md`](layout.md) for the Chapter III TOC with a link on every H2 and H3.
2. Use [`registers/header-index.csv`](registers/header-index.csv) as the source of truth for header IDs, permalinks, spine nodes, and tester status.
3. Follow the how-to page for the header you are editing (`pages/H-###-….md`).
4. Rescore [`registers/alignment-testers.csv`](registers/alignment-testers.csv) against the **current** chapter, not the older collection draft.
5. Drop later theory notes, templates, or committee files in [`uploads/`](uploads/README.md) and log them on [`registers/crosswalk.csv`](registers/crosswalk.csv).

Workspace-app tracker: [`workspace-app/chapter-iii.html`](../workspace-app/chapter-iii.html) (`11_CHIII_ASSENSION`).

## IDs

| Prefix | Object |
| --- | --- |
| `CH3-H-###` | Chapter III header |
| `CH3-HT-###` | How-to note |
| `CH3-SP-###` | Header ↔ spine-node row |
| `CH3-AT-###` | Alignment Map tester |
| `CH3-XW-###` | Crosswalk to a companion file |
| `CH3-EV-###` | Dissertation-event / needed-item row (Chapter I–V templates) |

Do not reuse a retired ID. Append a new row; set `status=retired` on the old one.

## How to add a header

1. Add the heading in `docs/chapter-iii-methodology.md`.
2. List it in that file’s TOC **and** in [`layout.md`](layout.md) with the GitHub-style slug (`#heading-text`).
3. Run `python3 scripts/seed_chiii_assension.py` only after adding a META entry in that script, **or** append rows by hand to the five CSVs and add `pages/H-###-slug.md`.
4. Map the header to at least one spine node and one alignment tester.
5. Sync app data: `python3 scripts/export_chiii_assension.py && python3 scripts/sync_app_data.py`.
6. Append `registers/how-to-notes.csv` and a crosswalk row.

## How testers are rescored

Score `Strong` / `Partial` / `Weak` against the paste-ready chapter as it stands today.

- `Strong` — the marker has written steps that can collect or reduce Gap data.
- `Partial` — the marker is conceptually right but still missing a locked artifact (example: official RQ wording).
- `Weak` — the marker names an intent with no collectable step.

The older memo in [`docs/alignment-assessment-data-collection.md`](../docs/alignment-assessment-data-collection.md) is historical. `alignment-testers.csv` is the live scorecard.

## Confidentiality

Do not put identifiable transcripts, RAW recordings, credentials, IP addresses, customer identifiers, or unredacted recovery diagrams here. De-identify first (`P##`, role only, `SME-A`, `Platform-1`).

## Folder layout

```
_CHPT III_Assension_db/
  README.md
  layout.md
  inventory.json
  registers/
    header-index.csv
    spine-map.csv
    alignment-testers.csv
    how-to-notes.csv
    crosswalk.csv
  pages/                 one how-to note per Chapter III header
  templates/             Chapter I–V needed items, theory, qualitative, U.S. SME, lit review
  uploads/               incoming docs and workbooks (no RAW identifiers)
```
