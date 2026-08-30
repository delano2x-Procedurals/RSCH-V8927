export const TABS = [
  { href: "index.html", id: "00_README", label: "README" },
  { href: "dashboard.html", id: "01_DASHBOARD", label: "Dashboard" },
  { href: "parking-lot.html", id: "02_PARKING_LOT", label: "Parking lot" },
  { href: "references.html", id: "03_REFERENCES_MASTER", label: "References" },
  { href: "citations.html", id: "11_CITATION_INSERTS", label: "Citation inserts" },
  { href: "theory-spine.html", id: "04_THEORY_AND_SPINE", label: "Theory & spine" },
  { href: "leadership.html", id: "05_LEADERSHIP_ALIGNMENT", label: "Leadership" },
  { href: "methods.html", id: "06_QUAL_METHODS_AND_TOOLS", label: "Qual methods" },
  { href: "archive.html", id: "07_SOURCE_ARCHIVE", label: "Source archive" },
  { href: "rq1.html", id: "08_RQ1_ANALYSIS", label: "RQ1 analysis" },
  { href: "sop.html", id: "14_SOP_RQ1", label: "SOP / data statement" },
  { href: "interview-protocol.html", id: "09_INTERVIEW_PROTOCOL", label: "Interview protocol" },
  { href: "analysis-templates.html", id: "10_ANALYSIS_TEMPLATES", label: "Analysis templates" },
];

const PAGE = document.body.dataset.page || "";

function currentHref() {
  const file = (location.pathname.split("/").pop() || "index.html") || "index.html";
  return file === "" ? "index.html" : file;
}

export function renderChrome() {
  if (!document.querySelector('link[rel="icon"]')) {
    const icon = document.createElement("link");
    icon.rel = "icon";
    icon.href = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect fill='%23c9a227' width='16' height='16'/></svg>";
    document.head.append(icon);
  }
  const header = document.createElement("header");
  header.className = "site-header";
  header.innerHTML = `
    <div class="inner">
      <div class="brand">
        <h1>BMGT 8044 amalgamated research workspace</h1>
        <div class="meta">RSCH-V8927 · Class 3 of 3 · generic qualitative interviews</div>
      </div>
      <nav class="toc" aria-label="Table of contents for all tabs">${TABS.map((t) => {
        const current = t.href === currentHref() || t.id === PAGE;
        return `<a href="${t.href}" ${current ? 'aria-current="page"' : ""}>${t.label}</a>`;
      }).join("")}</nav>
    </div>`;
  document.body.prepend(header);

  const strip = document.createElement("div");
  strip.className = "pl-strip";
  strip.innerHTML = `
    <form class="inner" id="pl-add-form">
      <div>
        <label for="pl-title">Park an item from this tab</label>
        <input id="pl-title" name="title" required placeholder="What needs a later decision?">
      </div>
      <div>
        <label for="pl-why">Why parked</label>
        <input id="pl-why" name="why" placeholder="Open question, missing source, ethics check">
      </div>
      <div>
        <label for="pl-link">Linked ID</label>
        <input id="pl-link" name="linked" placeholder="REF-018 / THEME-04 / IQ-02">
      </div>
      <button type="submit">Add to parking lot</button>
      <a class="btn secondary" href="parking-lot.html">Open parking lot</a>
      <a class="btn secondary" href="dashboard.html">Search on Dashboard</a>
      <span id="pl-add-status" class="empty-chips"></span>
    </form>
    <form class="inner" id="cite-add-form">
      <div>
        <label for="cite-ref">Citation insert (REF- / XREF-)</label>
        <input id="cite-ref" name="ref" required placeholder="REF-018" list="cite-ref-ids">
      </div>
      <div>
        <label for="cite-loc">Locator</label>
        <input id="cite-loc" name="locator" placeholder="p. 12 / para. 4">
      </div>
      <div>
        <label for="cite-used">Insert into</label>
        <input id="cite-used" name="used" placeholder="IQ-02 / Delve code / RQ1 memo">
      </div>
      <div>
        <label for="cite-notes">Notes</label>
        <input id="cite-notes" name="notes" placeholder="Why this citation is used">
      </div>
      <button type="submit">Save citation insert</button>
      <a class="btn secondary" href="citations.html">Open citation log</a>
      <span id="cite-add-status" class="empty-chips"></span>
      <datalist id="cite-ref-ids"></datalist>
    </form>`;
  header.after(strip);

  const footer = document.createElement("footer");
  footer.innerHTML = `Source workbooks are unchanged in <code>source/originals/</code>. Excel twin: <code>workbook/BMGT8044_Amalgamated_Research_Workspace.xlsx</code>. Delve is the CAQDAS tool in use. Search lives only on the Dashboard.`;
  document.body.append(footer);

  document.getElementById("pl-add-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const title = document.getElementById("pl-title").value.trim();
    const why = document.getElementById("pl-why").value.trim();
    const linked = document.getElementById("pl-link").value.trim();
    const id = addParkingItem({ title, why, linked, fromTab: PAGE || currentHref() });
    e.target.reset();
    const note = document.getElementById("pl-add-status");
    if (note) note.textContent = `${id} parked. It appears on the Parking lot tab.`;
    window.dispatchEvent(new CustomEvent("parking-lot-changed"));
  });

  fillCiteIds();
  document.getElementById("cite-add-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const refId = document.getElementById("cite-ref").value.trim().toUpperCase();
    const locator = document.getElementById("cite-loc").value.trim();
    const usedIn = document.getElementById("cite-used").value.trim();
    const notes = document.getElementById("cite-notes").value.trim();
    const rec = await saveCitationFromStrip({ refId, locator, usedIn, notes, fromTab: PAGE || currentHref() });
    const note = document.getElementById("cite-add-status");
    if (!rec) {
      if (note) note.textContent = `No match for ${refId}`;
      return;
    }
    e.target.reset();
    if (note) note.textContent = `${rec.id} saved: ${rec.parenthetical}`;
    window.dispatchEvent(new CustomEvent("citation-inserts-changed"));
  });
}

const CITE_KEY = "bmgt8044_citation_inserts";

async function fillCiteIds() {
  try {
    const [refs, extra] = await Promise.all([
      loadJSON("data/references.json"),
      loadJSON("data/extra_refs.json"),
    ]);
    const list = document.getElementById("cite-ref-ids");
    if (!list) return;
    list.innerHTML = [...refs, ...extra]
      .map((r) => `<option value="${r.id}">${r.id} ${(r.item_title || r.title || "").replace(/</g, "")}</option>`)
      .join("");
  } catch {
    /* datalist is optional */
  }
}

async function saveCitationFromStrip({ refId, locator, usedIn, notes, fromTab }) {
  const [refs, extra] = await Promise.all([
    loadJSON("data/references.json"),
    loadJSON("data/extra_refs.json"),
  ]);
  const ref = refs.find((r) => r.id === refId) || extra.find((r) => r.id === refId);
  if (!ref) return null;
  let items = [];
  try {
    items = JSON.parse(localStorage.getItem(CITE_KEY) || "[]");
  } catch {
    items = [];
  }
  const author = (ref.item_author || ref.title || "Unknown").replace(/;$/, "");
  const year = ref.item_publication_date || "n.d.";
  const loc = locator ? `, ${locator}` : "";
  const rec = {
    id: `CIT-${String(items.length + 1).padStart(3, "0")}`,
    type: "Citation insert",
    ref_id: refId,
    title: ref.item_title || ref.title || refId,
    parenthetical: `(${author}, ${year}${loc})`,
    narrative: `${author} (${year}${loc})`,
    apa: ref.apa || "",
    locator: locator || "",
    used_in: usedIn || fromTab,
    notes: notes || "",
    created_at: new Date().toISOString(),
  };
  items.push(rec);
  localStorage.setItem(CITE_KEY, JSON.stringify(items));
  return rec;
}

const PL_KEY = "bmgt8044_parking_additions";

export function getParkingAdditions() {
  try {
    return JSON.parse(localStorage.getItem(PL_KEY) || "[]");
  } catch {
    return [];
  }
}

export function addParkingItem({ title, why, linked, fromTab }) {
  const items = getParkingAdditions();
  const id = `PL-L${String(items.length + 1).padStart(3, "0")}`;
  items.push({
    id,
    type: "Parking lot",
    title,
    why_parked: why,
    linked_id: linked,
    status: "open",
    owner: "Member",
    source_tab: fromTab,
    used_in_tab: "02_PARKING_LOT",
    created_at: new Date().toISOString(),
  });
  localStorage.setItem(PL_KEY, JSON.stringify(items));
  return id;
}

export async function loadJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to load ${path}`);
  return res.json();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", renderChrome);
} else {
  renderChrome();
}
