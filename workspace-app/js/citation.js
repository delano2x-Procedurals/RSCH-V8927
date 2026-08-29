import { loadJSON } from "./nav.js";
import { escapeHtml } from "./search.js";

export const CITE_KEY = "bmgt8044_citation_inserts";

export function getCitationInserts() {
  try {
    return JSON.parse(localStorage.getItem(CITE_KEY) || "[]");
  } catch {
    return [];
  }
}

export function parenthetical(ref, locator) {
  const author = (ref.item_author || ref.title || "Unknown").replace(/;$/, "");
  const year = ref.item_publication_date || "n.d.";
  const loc = locator ? `, ${locator}` : "";
  return `(${author}, ${year}${loc})`;
}

export function narrative(ref, locator) {
  const author = (ref.item_author || ref.title || "Unknown").replace(/;$/, "");
  const year = ref.item_publication_date || "n.d.";
  const loc = locator ? `, ${locator}` : "";
  return `${author} (${year}${loc})`;
}

export function addCitationInsert({ refId, locator, usedIn, notes, ref }) {
  const items = getCitationInserts();
  const id = `CIT-${String(items.length + 1).padStart(3, "0")}`;
  const rec = {
    id,
    type: "Citation insert",
    ref_id: refId,
    title: ref ? ref.item_title || ref.title : refId,
    parenthetical: ref ? parenthetical(ref, locator) : "",
    narrative: ref ? narrative(ref, locator) : "",
    apa: ref ? ref.apa || "" : "",
    locator: locator || "",
    used_in: usedIn || "",
    notes: notes || "",
    created_at: new Date().toISOString(),
  };
  items.push(rec);
  localStorage.setItem(CITE_KEY, JSON.stringify(items));
  return rec;
}

function byId(refs, extra, id) {
  return refs.find((r) => r.id === id) || extra.find((r) => r.id === id) || null;
}

export function renderCitationLog(el, items) {
  if (!el) return;
  const rows = items
    .map(
      (c) => `<tr id="${escapeHtml(c.id)}">
      <td><strong>${escapeHtml(c.id)}</strong></td>
      <td>${escapeHtml(c.ref_id)}</td>
      <td>${escapeHtml(c.title)}</td>
      <td><textarea class="cite-out">${escapeHtml(c.parenthetical)}</textarea></td>
      <td><textarea class="cite-out">${escapeHtml(c.narrative)}</textarea></td>
      <td><textarea class="cite-out">${escapeHtml(c.apa)}</textarea></td>
      <td>${escapeHtml(c.locator)}</td>
      <td>${escapeHtml(c.used_in)}</td>
      <td>${escapeHtml(c.notes)}</td>
    </tr>`
    )
    .join("");
  el.innerHTML = `<div class="results-meta">${items.length} saved citation inserts (browser)</div>
    <table>
      <thead><tr>
        <th>CIT-ID</th><th>REF-ID</th><th>Title</th><th>Parenthetical insert</th>
        <th>Narrative insert</th><th>APA</th><th>Locator</th><th>Used in</th><th>Notes</th>
      </tr></thead>
      <tbody>${rows || `<tr><td colspan="9">None saved yet. Use the citation insert strip on any tab.</td></tr>`}</tbody>
    </table>`;
}

export async function initCitationPage() {
  const refs = await loadJSON("data/references.json");
  const extra = await loadJSON("data/extra_refs.json");
  const all = [...refs, ...extra];
  const datalist = document.getElementById("ref-ids");
  if (datalist) {
    datalist.innerHTML = all.map((r) => `<option value="${escapeHtml(r.id)}">${escapeHtml(r.id)} ${escapeHtml(r.item_title || r.title || "")}</option>`).join("");
  }
  const paint = () => renderCitationLog(document.getElementById("cite-log"), getCitationInserts());
  paint();
  window.addEventListener("citation-inserts-changed", paint);

  const preview = () => {
    const id = document.getElementById("cite-page-ref").value.trim().toUpperCase();
    const loc = document.getElementById("cite-page-loc").value.trim();
    const ref = byId(refs, extra, id);
    const box = document.getElementById("cite-preview");
    if (!ref) {
      box.textContent = id ? `No match for ${id}` : "Enter a REF- or XREF- ID to preview inserts.";
      return;
    }
    box.textContent = `Parenthetical: ${parenthetical(ref, loc)}\nNarrative: ${narrative(ref, loc)}\nAPA: ${ref.apa || ""}`;
  };
  document.getElementById("cite-page-ref").addEventListener("input", preview);
  document.getElementById("cite-page-loc").addEventListener("input", preview);
  document.getElementById("cite-page-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const refId = document.getElementById("cite-page-ref").value.trim().toUpperCase();
    const locator = document.getElementById("cite-page-loc").value.trim();
    const usedIn = document.getElementById("cite-page-used").value.trim();
    const notes = document.getElementById("cite-page-notes").value.trim();
    const ref = byId(refs, extra, refId);
    if (!ref) {
      document.getElementById("cite-page-status").textContent = `No match for ${refId}`;
      return;
    }
    const rec = addCitationInsert({ refId, locator, usedIn, notes, ref });
    document.getElementById("cite-page-status").textContent = `${rec.id} saved. Parenthetical: ${rec.parenthetical}`;
    e.target.reset();
    preview();
    window.dispatchEvent(new CustomEvent("citation-inserts-changed"));
  });
  document.getElementById("export-cites").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(getCitationInserts(), null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "citation_inserts.json";
    a.click();
    URL.revokeObjectURL(a.href);
  });
}

if (document.body.dataset.page === "11_CITATION_INSERTS") {
  const start = () => initCitationPage().catch((err) => {
    const main = document.querySelector("main");
    if (main) main.insertAdjacentHTML("beforeend", `<p class="callout warn">${escapeHtml(err.message)}</p>`);
  });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
}
