#!/usr/bin/env python3
"""Sanity checks for extracted IDs, pages, and last-three search rules."""
from __future__ import annotations

import json
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
    ]
    for name in pages:
        text = (ROOT / "workspace-app" / name).read_text()
        assert 'class="toc"' in (ROOT / "workspace-app" / "js" / "nav.js").read_text()
        assert "<h2" in text

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
