# SOP: get and use the dissertation Excel offering

Use this when you need the workbook that holds Chapter I–V input, theory, qualitative, U.S. SME, analysis, and lit-review rows. Keep one **clean master** in the repo. Work only on a **dated working copy**.

Instrument and method do not change: `ITDR-GQI-INT-v0.1.1`; hybrid codebook TA; Delve is CAQDAS only. No RAW identifiers in any copy.

---

## 1. What the offering is

| File | Role | Touch this? |
| --- | --- | --- |
| [`ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx`](ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx) | **Use this.** Dissertation repository input place. Chapter I–V tabs plus Theory, Qualitative, U.S. SME, Qualitative Analysis, Lit review, plus the original artifact sheets. | Download, then copy. Do not type into the repo file. |
| [`ITDRPaaS_Governance_Artifact_Workbook.xlsx`](ITDRPaaS_Governance_Artifact_Workbook.xlsx) | Original uploaded operational offering (RACI, DR Plan, failover, etc.). Kept as lineage. | Read only. |
| `workbook/BMGT8044_Amalgamated_Research_Workspace.xlsx` | Website twin (Dashboard, parking lot, references). | Not the dissertation input place. |

Rebuild the Assension twin from CSVs with `python3 scripts/build_chiii_assension_workbook.py`. That overwrites the **master** in this folder. It does not touch your working copy if you renamed it.

---

## 2. Where it is

In the clone, from the repo root:

```
_CHPT III_Assension_db/uploads/ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx
```

Companions in the same folder:

- this SOP
- [`README.md`](README.md) (upload rules)
- the original `.xlsx` (do not use for new Chapter I–V rows)

On GitHub (this branch): open the repo → `_CHPT III_Assension_db` → `uploads` → `ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx`.

On the local site (after `python3 -m http.server 4173 --directory workspace-app`):

http://127.0.0.1:4173/_CHPT%20III_Assension_db/uploads/ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx

---

## 3. How to get a copy (download)

**Cursor / local clone**

1. In the file tree, open `_CHPT III_Assension_db/uploads/`.
2. Right-click `ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx` → Download, or copy the file in Finder/Explorer.
3. Or from a terminal at the repo root:

```bash
cp "_CHPT III_Assension_db/uploads/ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx" \
  "$HOME/Downloads/ITDRPaaS_CHIII_Assension_WORKING_$(date +%Y-%m-%d).xlsx"
```

**GitHub in the browser**

1. Open the `uploads` folder on the branch that has this nest.
2. Click `ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx`.
3. Use **Download raw file** (or the download icon). Do not open it only as a GitHub preview and type there.

**Local HTTP server**

1. Start `python3 -m http.server 4173 --directory workspace-app`.
2. Open the URL in section 2.
3. Save the file. Then rename it (section 4) before you edit.

---

## 4. Rename so the clean master stays clean

Immediately after download, make a **working copy** with a date and your use. Leave the repo filename untouched.

Suggested name:

```
ITDRPaaS_CHIII_Assension_WORKING_YYYY-MM-DD.xlsx
```

Examples:

- `ITDRPaaS_CHIII_Assension_WORKING_2026-09-02.xlsx` — today’s input session
- `ITDRPaaS_CHIII_Assension_WORKING_2026-09-02_ChI-defs.xlsx` — Chapter I definitions only

Rules:

1. Never overwrite `ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx` in `uploads/` by saving Excel “in place” on the repo path.
2. Never overwrite `ITDRPaaS_Governance_Artifact_Workbook.xlsx` (lineage).
3. If you must put a filled file back in the repo, **add** it with a dated name. Do not replace the master.

```bash
# clean master stays
# working copy lives next to Downloads or in uploads/ under a dated name
cp "$HOME/Downloads/ITDRPaaS_CHIII_Assension_WORKING_2026-09-02.xlsx" \
  "_CHPT III_Assension_db/uploads/2026-09-02-ITDRPaaS_CHIII_Assension_WORKING.xlsx"
```

Then log that dated file on [`../registers/crosswalk.csv`](../registers/crosswalk.csv) (`target_kind=upload`).

---

## 5. How to use the working copy

Open the **WORKING** file in Excel or LibreOffice. Start on `00_ReadMe`. Then add rows on the tab that matches the dissertation event:

| Tab | Add / create |
| --- | --- |
| `01_ChI_Introduction` | Problem, purpose, official or implied questions, definitions |
| `02_ChII_LitReview` | What We Know / Don’t Know / Gap items |
| `03_ChIII_Methodology` | Chapter III header work (links back to how-to pages) |
| `04_ChIV_Findings` | Leave Theme/Finding empty until meaning units are locked |
| `05_ChV_Discussion` | Interpretation only; do not newly name themes |
| `06_Theory` | PLU, leverage, SAL → DR → ESC → AE → RA (not a proven theory) |
| `07_Qualitative` | GQI, CIT, instrument rules |
| `08_US_SME` | 10–200 U.S. SME, 36-month incident, inclusion |
| `09_Qual_Analysis` | Hybrid codebook TA; Delve is not the method |
| `10_Lit_Review` | original vs build-on vs new-instrument vs audit-artifact |
| Artifact sheets after that | RACI, DR Plan, incident command, delegation, failover, exception, audit trail |

**Do**

- Add a new row. Keep the ID scheme (`CH3-EV-###`, `THY-###`, `ART-###`, or the next free ID on that sheet).
- Fill `status` (`needed` / `in_nest` / `partial` / `reserved` / `done`).
- Point `where_it_lives` or `companion` at a real file (`docs/…`, `_CHPT III_Assension_db/pages/…`).
- Record material decisions on `Audit Trail` (new row; do not overwrite a prior rationale).

**Do not**

- Type identifiers, employer names, or unredacted recovery diagrams.
- Promote PLU codes to Chapter IV theme titles.
- Treat SAL → DR → ESC → AE → RA as a finished theory.
- Rebuild the master with `build_chiii_assension_workbook.py` if you still have unsaved edits only in the repo file. Those edits would be lost. Keep them on the WORKING copy.

How-to notes for Chapter III headers: [`../layout.md`](../layout.md).

---

## 6. Keep a clean copy (checklist)

1. Master in repo: `ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx` — download source only.
2. Working file: `…_WORKING_YYYY-MM-DD.xlsx` — this is where you type.
3. After a session: Save As a new dated name if the day already has a file (`…_WORKING_2026-09-02b.xlsx`).
4. Optional return to the nest: copy the dated WORKING file into `uploads/` and log it. Do not replace the master.
5. To refresh a **blank** master from CSVs: run `python3 scripts/build_chiii_assension_workbook.py`, then download again and make a **new** WORKING copy.

---

## 7. If something is missing

- Tabs empty after a rebuild: the CSVs in [`../templates/`](../templates/) are the source. Edit those, rebuild, then download a new WORKING copy.
- Need the website tables instead of Excel: open http://127.0.0.1:4173/chapter-iii.html.
- Need the original operational offering only: use `ITDRPaaS_Governance_Artifact_Workbook.xlsx` (read only).
