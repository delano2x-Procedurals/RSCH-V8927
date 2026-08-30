import { loadJSON, getParkingAdditions } from "./nav.js";
import { escapeHtml } from "./search.js";

export function renderRecords(targetId, records, columns) {
  const el = document.getElementById(targetId);
  if (!el) return;
  const head = columns.map((c) => `<th>${escapeHtml(c.label)}</th>`).join("");
  const rows = records
    .map((rec) => {
      const tds = columns
        .map((c) => {
          let val = rec[c.key];
          if (Array.isArray(val)) val = val.join(", ");
          if (c.key === "id") {
            return `<td id="${escapeHtml(rec.id)}"><strong>${escapeHtml(rec.id)}</strong></td>`;
          }
          if (c.key === "status") {
            return `<td><span class="badge ${escapeHtml(rec.status || "")}">${escapeHtml(rec.status || "—")}</span></td>`;
          }
          return `<td>${escapeHtml(val ?? "")}</td>`;
        })
        .join("");
      return `<tr>${tds}</tr>`;
    })
    .join("");
  el.innerHTML = `<div class="results-meta">${records.length} rows</div>
    <table><thead><tr>${head}</tr></thead><tbody>${rows || `<tr><td colspan="${columns.length}">None</td></tr>`}</tbody></table>`;
}

export async function initReferences() {
  const refs = await loadJSON("data/references.json");
  const extra = await loadJSON("data/extra_refs.json");
  renderRecords("ref-table", refs, [
    { key: "id", label: "ID" },
    { key: "section_name", label: "Week / section" },
    { key: "item_type", label: "Type" },
    { key: "item_title", label: "Title" },
    { key: "item_author", label: "Author" },
    { key: "item_journal_title", label: "Journal" },
    { key: "item_publication_date", label: "Year" },
    { key: "item_doi", label: "DOI" },
    { key: "permalink", label: "Permalink" },
    { key: "apa", label: "APA / citation insert source" },
    { key: "used_in_tab", label: "Used in tab" },
    { key: "comps_audit_tag", label: "Comps audit tag" },
    { key: "gap_note", label: "Gap note" },
  ]);
  renderRecords("xref-table", extra, [
    { key: "id", label: "ID" },
    { key: "title", label: "Title / citation" },
    { key: "apa", label: "Full text" },
    { key: "item_url", label: "URL" },
    { key: "source_row", label: "Source row" },
  ]);
}

export async function initThemes() {
  const themes = await loadJSON("data/themes.json");
  renderRecords("theme-table", themes, [
    { key: "id", label: "ID" },
    { key: "theme", label: "Theme" },
    { key: "description", label: "Description" },
    { key: "references", label: "References" },
  ]);
}

export async function initParking() {
  const source = await loadJSON("data/parking_lot.json");
  const local = getParkingAdditions();
  renderRecords("pl-local", local, [
    { key: "id", label: "ID" },
    { key: "title", label: "Item" },
    { key: "why_parked", label: "Why parked" },
    { key: "linked_id", label: "Linked ID" },
    { key: "status", label: "Status" },
    { key: "source_tab", label: "From tab" },
  ]);
  renderRecords("pl-source", source, [
    { key: "id", label: "ID" },
    { key: "title", label: "Item" },
    { key: "why_parked", label: "Source text" },
    { key: "status", label: "Status" },
    { key: "source_row", label: "Source row" },
    { key: "week", label: "Week tag" },
  ]);
}

export async function initTheory() {
  const theory = await loadJSON("data/theory.json");
  const spine = await loadJSON("data/spine.json");
  const constructs = theory.filter((r) => ["TH-0068", "TH-0069", "TH-0070", "TH-0071", "TH-0072", "TH-0073", "TH-0074", "TH-0075", "TH-0076", "TH-0077", "TH-0078"].includes(r.id) || /Phenomenon|Construct|Boundary conditions|Evidence implications/.test(r.title));
  renderRecords("construct-table", constructs.slice(0, 20), [
    { key: "id", label: "ID" },
    { key: "title", label: "Row" },
    { key: "description", label: "Extracted text" },
  ]);
  renderRecords("spine-table", spine, [
    { key: "id", label: "ID" },
    { key: "title", label: "Spine statement" },
    { key: "classification", label: "Classification" },
    { key: "explanation", label: "Explanation" },
  ]);
  renderRecords("theory-all", theory, [
    { key: "id", label: "ID" },
    { key: "title", label: "Title" },
    { key: "source_row", label: "Row" },
    { key: "description", label: "All cell text" },
  ]);
}

export async function initMethods() {
  const archive = await loadJSON("data/archive.json");
  const methods = archive.filter((r) => r.used_in_tab === "06_QUAL_METHODS_AND_TOOLS");
  renderRecords("methods-table", methods, [
    { key: "id", label: "ID" },
    { key: "item_type", label: "Source" },
    { key: "title", label: "Title" },
    { key: "description", label: "Text" },
  ]);
}

export async function initArchive() {
  const archive = await loadJSON("data/archive.json");
  const tabs = [...new Set(archive.map((r) => r.source_tab))];
  const sel = document.getElementById("archive-tab");
  sel.innerHTML = `<option value="">All archived tabs</option>` + tabs.map((t) => `<option>${escapeHtml(t)}</option>`).join("");
  const paint = () => {
    const val = sel.value;
    const rows = val ? archive.filter((r) => r.source_tab === val) : archive;
    renderRecords("archive-table", rows, [
      { key: "id", label: "ID" },
      { key: "item_type", label: "Class" },
      { key: "source_tab", label: "Source tab" },
      { key: "title", label: "Title" },
      { key: "description", label: "Full retained text" },
    ]);
  };
  sel.addEventListener("change", paint);
  paint();
}

export async function initInterview() {
  const qs = await loadJSON("data/interview_questions.json");
  renderRecords("iq-table", qs, [
    { key: "id", label: "ID" },
    { key: "construct", label: "Construct" },
    { key: "question", label: "Interview question" },
    { key: "review_question", label: "Review question" },
    { key: "ethical_check", label: "Ethical extraction check" },
    { key: "status", label: "Status" },
    { key: "linked_refs", label: "Linked IDs" },
    { key: "citation_insert", label: "Citation insert" },
  ]);
}

const inits = {
  "03_REFERENCES_MASTER": initReferences,
  "05_LEADERSHIP_ALIGNMENT": initThemes,
  "02_PARKING_LOT": initParking,
  "04_THEORY_AND_SPINE": initTheory,
  "06_QUAL_METHODS_AND_TOOLS": initMethods,
  "07_SOURCE_ARCHIVE": initArchive,
  "09_INTERVIEW_PROTOCOL": initInterview,
};

const boot = inits[document.body.dataset.page];
if (boot) {
  const start = () => boot().catch((err) => {
    const main = document.querySelector("main");
    if (main) main.insertAdjacentHTML("beforeend", `<p class="callout warn">${escapeHtml(err.message)}</p>`);
  });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
  window.addEventListener("parking-lot-changed", () => {
    if (document.body.dataset.page === "02_PARKING_LOT") start();
  });
}
