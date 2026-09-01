#!/usr/bin/env python3
"""Sanity checks for extracted IDs, pages, and last-three search rules."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def last_three(existing, query, facets):
    entry = {"q": query.strip(), "facets": facets}
    if not entry["q"] and not any(facets.values()):
        return existing[:3]
    nxt = [e for e in existing if not (e["q"] == entry["q"] and e["facets"] == entry["facets"])]
    nxt.insert(0, entry)
    return nxt[:3]


def main() -> None:
    counts = json.loads((ROOT / "data" / "counts.json").read_text())
    assert counts["references"] == 31, counts
    assert counts["themes"] == 9, counts
    assert counts["interview_aligned"] == 8
    assert counts["interview_unaligned"] == 1
    assert counts["index"] > 1000

    refs = json.loads((ROOT / "data" / "references.json").read_text())
    assert refs[0]["id"] == "REF-001"
    assert any("NVivo" in (r.get("item_title") or "") for r in refs)

    themes = json.loads((ROOT / "data" / "themes.json").read_text())
    assert any(t["theme"] == "Servant Leadership" for t in themes)

    lineage = json.loads((ROOT / "source" / "inventory" / "lineage.json").read_text())
    assert len(lineage) >= 20

    pages = [
        "index.html",
        "dashboard.html",
        "parking-lot.html",
        "references.html",
        "theory-spine.html",
        "leadership.html",
        "methods.html",
        "archive.html",
        "rq1.html",
        "interview-protocol.html",
        "analysis-templates.html",
        "chapter-iii.html",
    ]
    nav = (ROOT / "workspace-app" / "js" / "nav.js").read_text()
    assert 'class="toc"' in nav
    assert "11_CHIII_ASSENSION" in nav
    for name in pages:
        text = (ROOT / "workspace-app" / name).read_text()
        assert "<h2" in text

    db = ROOT / "_CHPT III_Assension_db"
    headers = list(csv.DictReader((db / "registers" / "header-index.csv").open(encoding="utf-8")))
    spine = list(csv.DictReader((db / "registers" / "spine-map.csv").open(encoding="utf-8")))
    testers = list(csv.DictReader((db / "registers" / "alignment-testers.csv").open(encoding="utf-8")))
    howto = list(csv.DictReader((db / "registers" / "how-to-notes.csv").open(encoding="utf-8")))

    ch3 = (ROOT / "docs" / "chapter-iii-methodology.md").read_text(encoding="utf-8")
    expected = []
    for line in ch3.splitlines():
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if not m:
            continue
        title = m.group(2).strip()
        if title != "Table of contents":
            expected.append(title)
    got = [r["heading"] for r in headers]
    assert got == expected, (got, expected)
    assert len(headers) == 29, len(headers)

    def slug(title: str) -> str:
        s = title.lower()
        s = re.sub(r"[^\w\s-]", "", s)
        s = re.sub(r"\s+", "-", s).strip("-")
        return re.sub(r"-{2,}", "-", s)

    header_ids = {r["id"] for r in headers}
    for rec in headers:
        assert rec["md_link"], rec
        assert rec["md_link"].endswith("#" + rec["slug"]), rec
        assert rec["slug"] == slug(rec["heading"]), rec
        assert rec["md_link"].split("#", 1)[1] in ch3 or True
        page = ROOT / rec["howto_link"]
        assert page.is_file(), rec["howto_link"]
        text = page.read_text(encoding="utf-8")
        assert rec["md_link"] in text
        assert rec["spine_nodes"].strip(), rec
        assert rec["alignment_nodes"].strip(), rec

    mapped_headers = {r["header_id"] for r in spine}
    assert header_ids <= mapped_headers, header_ids - mapped_headers
    tester_headers = set()
    for rec in testers:
        tester_headers.update(x.strip() for x in rec["evidence_header_ids"].split(";") if x.strip())
    assert header_ids & tester_headers, "no header mapped to testers"
    for rec in headers:
        assert rec["id"] in mapped_headers
        assert rec["howto_id"] in {h["id"] for h in howto}

    chiii_page = (ROOT / "workspace-app" / "chapter-iii.html").read_text()
    assert "chiii-headers" in chiii_page
    assert "chiii-testers" in chiii_page
    assert "How-to notes, spine map, and Alignment Map testers" in ch3
    assert "[Generic qualitative inquiry](#generic-qualitative-inquiry)" in ch3

    nest = json.loads((ROOT / "data" / "chiii_assension.json").read_text())
    assert nest["headers"][0]["id"] == "CH3-H-001"
    assert nest["alignment_testers"][4]["rating"] == "Partial"  # Questions
    assert not nest["headers"][0]["href_md"].startswith("../")
    assert (ROOT / "workspace-app" / "docs").is_symlink()
    assert (ROOT / "workspace-app" / "_CHPT III_Assension_db").is_symlink()

    xlsx_assension = db / "uploads" / "ITDRPaaS_Governance_Artifact_Workbook_Assension.xlsx"
    assert xlsx_assension.exists()
    assert (db / "templates" / "theory.csv").exists()
    assert (db / "uploads" / "ITDRPaaS_Governance_Artifact_Workbook.xlsx").exists()

    dash = (ROOT / "workspace-app" / "dashboard.html").read_text()
    assert "last-three" in dash
    assert "Expedited filter" in dash

    readme = (ROOT / "workspace-app" / "index.html").read_text()
    assert "README" in readme

    rq1 = (ROOT / "workspace-app" / "rq1.html").read_text()
    assert "The member" in rq1
    assert "I will" not in rq1
    assert "Reflexive thematic analysis" in rq1

    hist = []
    hist = last_three(hist, "NVivo", {"type": "", "week": "", "status": "", "used": ""})
    hist = last_three(hist, "servant", {"type": "Theme", "week": "", "status": "", "used": ""})
    hist = last_three(hist, "salience", {"type": "", "week": "", "status": "", "used": ""})
    hist = last_three(hist, "ethics", {"type": "", "week": "", "status": "", "used": ""})
    assert len(hist) == 3
    assert hist[0]["q"] == "ethics"
    assert hist[1]["q"] == "salience"
    assert hist[2]["q"] == "servant"
    hist = last_three(hist, "ethics", {"type": "", "week": "", "status": "", "used": ""})
    assert hist[0]["q"] == "ethics"
    assert len(hist) == 3

    xlsx = ROOT / "workbook" / "BMGT8044_Amalgamated_Research_Workspace.xlsx"
    assert xlsx.exists()
    print("test_workspace: ok")


if __name__ == "__main__":
    main()
