export const TABS = [
  { href: "index.html", id: "00_README", label: "README" },
  { href: "dashboard.html", id: "01_DASHBOARD", label: "Dashboard" },
  { href: "parking-lot.html", id: "02_PARKING_LOT", label: "Parking lot" },
  { href: "references.html", id: "03_REFERENCES_MASTER", label: "References" },
  { href: "theory-spine.html", id: "04_THEORY_AND_SPINE", label: "Theory & spine" },
  { href: "leadership.html", id: "05_LEADERSHIP_ALIGNMENT", label: "Leadership" },
  { href: "methods.html", id: "06_QUAL_METHODS_AND_TOOLS", label: "Qual methods" },
  { href: "archive.html", id: "07_SOURCE_ARCHIVE", label: "Source archive" },
  { href: "rq1.html", id: "08_RQ1_ANALYSIS", label: "RQ1 analysis" },
  { href: "interview-protocol.html", id: "09_INTERVIEW_PROTOCOL", label: "Interview protocol" },
  { href: "analysis-templates.html", id: "10_ANALYSIS_TEMPLATES", label: "Analysis templates" },
];

const PAGE = document.body.dataset.page || "";

function currentHref() {
  const file = (location.pathname.split("/").pop() || "index.html") || "index.html";
  return file === "" ? "index.html" : file;
}

export function renderChrome() {
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
    </form>`;
  header.after(strip);

  const footer = document.createElement("footer");
  footer.innerHTML = `Source workbooks are unchanged in <code>source/originals/</code>. Search lives only on the Dashboard. Clearing filters does not clear the last three searches.`;
  document.body.append(footer);

  document.getElementById("pl-add-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const title = document.getElementById("pl-title").value.trim();
    const why = document.getElementById("pl-why").value.trim();
    const linked = document.getElementById("pl-link").value.trim();
    addParkingItem({ title, why, linked, fromTab: PAGE || currentHref() });
    e.target.reset();
    alert(`Parked as a local item. Open the parking lot to review.`);
  });
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
