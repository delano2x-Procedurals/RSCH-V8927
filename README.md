# RSCH-V8927

CLASS 3 of 3. BMGT 8044 amalgamated research workspace.

The member’s two Excel workbooks (reading list and Week 7 leadership-theory alignment, plus the formatted duplicate) are preserved in `source/originals/`. They are joined here as shared pages so references, constructs, interview questions, and analysis notes stay on one trail.

## Paste-ready GQI and Chapter III

Usage and change-tracking log (including Gibran epigraph statements): [docs/change-tracking-update.md](docs/change-tracking-update.md).

Paste-ready Chapter I Need for the Study opening: [docs/chapter-i-need-for-the-study.md](docs/chapter-i-need-for-the-study.md). States the Information Technology Management specialization, how the ITDRPaaS project aligns with it, and the needed construct (value-creation stakeholder theory; Freeman et al., 2020).

Paste-ready GQI interview instrument: [docs/gqi-semistructured-interview-guide.md](docs/gqi-semistructured-interview-guide.md) (`ITDR-GQI-INT-v0.1.1`). Spoken protocol is unchanged from v0.1.

Paste-ready Chapter III (Methodology): [docs/chapter-iii-methodology.md](docs/chapter-iii-methodology.md). Analytic method is hybrid deductive–inductive codebook thematic analysis (Fereday & Muir-Cochrane, 2006). Delve is CAQDAS support only.

Symbols / original vs build-on refs: [docs/symbols-definitions-refs.md](docs/symbols-definitions-refs.md).

Interval CSV backups (Delve codebook, items, references, symbols): [docs/notion/](docs/notion/README.md).

Dissertation tracking pack (one xlsx + one Word file, bolded what/why): [downloads/Dissertation_Document_Tracking_Master.xlsx](downloads/Dissertation_Document_Tracking_Master.xlsx) and [downloads/Dissertation_Document_Tracking_Pack.docx](downloads/Dissertation_Document_Tracking_Pack.docx). Rebuild with `python3 scripts/build_dissertation_tracking_pack.py`.

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
5. Theory and spine
6. Leadership alignment
7. Qualitative methods and tools
8. Source archive (includes ARCHIVE_COMPARATIVE quantitative classmate plan)
9. RQ1 analysis (third-person appropriateness statement)
10. Interview protocol
11. Analysis templates

Excel twin: `workbook/BMGT8044_Amalgamated_Research_Workspace.xlsx` (`LastSearch1–3` on the Dashboard sheet).
