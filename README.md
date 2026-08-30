# RSCH-V8927

CLASS 3 of 3. BMGT 8044 amalgamated research workspace.

The member’s two Excel workbooks (reading list and Week 7 leadership-theory alignment, plus the formatted duplicate) are preserved in `source/originals/`. They are joined here as shared pages so references, constructs, interview questions, and analysis notes stay on one trail.

## Paste-ready GQI and Chapter III

Paste-ready GQI interview instrument: [docs/gqi-semistructured-interview-guide.md](docs/gqi-semistructured-interview-guide.md) (`ITDR-GQI-INT-v0.1.1`). Spoken protocol is unchanged from v0.1.

Paste-ready Chapter III (Methodology): [docs/chapter-iii-methodology.md](docs/chapter-iii-methodology.md). Analytic method is hybrid deductive–inductive codebook thematic analysis (Fereday & Muir-Cochrane, 2006). Delve is CAQDAS support only.

Symbols / original vs build-on refs: [docs/symbols-definitions-refs.md](docs/symbols-definitions-refs.md).

Interval CSV backups (Delve codebook, items, references, symbols): [docs/notion/](docs/notion/README.md).

## Open the workspace

```bash
./scripts/install.sh
python3 -m http.server 4173 --directory workspace-app
```

Then open http://127.0.0.1:4173/ — README is first; Dashboard (search + last three searches) is second.

## Tab order

1. README
2. Dashboard (counts + expedited filter; last three searches stored on Search / Enter / facet change)
3. Parking lot (tied to every tab)
4. References master
5. Citation inserts (parenthetical / narrative / APA from REF- IDs)
6. Theory and spine
7. Leadership alignment
8. Qualitative methods and tools (Delve is the CAQDAS product in use)
9. Source archive (includes ARCHIVE_COMPARATIVE quantitative classmate plan)
10. RQ1 analysis (third-person appropriateness statement)
11. SOP / data statement (abstract, key wording, APA 7 data statement, 12 steps)
12. Interview protocol
13. Analysis templates

Excel twin: `workbook/BMGT8044_Amalgamated_Research_Workspace.xlsx` (same tabs, including `11_CITATION_INSERTS` and `12_TOOL_USAGE`).
