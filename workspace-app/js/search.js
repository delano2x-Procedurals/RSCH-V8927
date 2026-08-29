import { loadJSON } from "./nav.js";

export const SEARCH_KEY = "bmgt8044_last_searches";
export const EXCEL_MIRROR_KEY = "bmgt8044_last_search_excel";

export function getLastThree() {
  try {
    return JSON.parse(localStorage.getItem(SEARCH_KEY) || "[]").slice(0, 3);
  } catch {
    return [];
  }
}

function facetKey(facets) {
  return JSON.stringify({
    type: facets.type || "",
    week: facets.week || "",
    status: facets.status || "",
    used: facets.used || "",
  });
}

export function recordSearch(query, facets) {
  const entry = {
    q: (query || "").trim(),
    facets: {
      type: facets.type || "",
      week: facets.week || "",
      status: facets.status || "",
      used: facets.used || "",
    },
    ts: Date.now(),
  };
  if (!entry.q && !entry.facets.type && !entry.facets.week && !entry.facets.status && !entry.facets.used) {
    return getLastThree();
  }
  const next = getLastThree().filter(
    (item) => !(item.q === entry.q && facetKey(item.facets) === facetKey(entry.facets))
  );
  next.unshift(entry);
  const lastThree = next.slice(0, 3);
  localStorage.setItem(SEARCH_KEY, JSON.stringify(lastThree));
  const mirror = {
    LastSearch1: lastThree[0] || null,
    LastSearch2: lastThree[1] || null,
    LastSearch3: lastThree[2] || null,
    updated: new Date().toISOString(),
  };
  localStorage.setItem(EXCEL_MIRROR_KEY, JSON.stringify(mirror));
  return lastThree;
}

export function matches(rec, query, facets) {
  if (facets.type && rec.type !== facets.type) return false;
  if (facets.week && rec.week !== facets.week) return false;
  if (facets.status && rec.status !== facets.status) return false;
  if (facets.used && rec.used_in_tab !== facets.used) return false;
  const q = (query || "").trim().toLowerCase();
  if (!q) return true;
  const hay = `${rec.id} ${rec.type} ${rec.title} ${rec.excerpt} ${rec.week} ${rec.status} ${rec.used_in_tab} ${rec.source_tab} ${rec.item_type} ${rec.search_text}`.toLowerCase();
  return q.split(/\s+/).every((part) => hay.includes(part));
}

function fmtTime(ts) {
  try {
    return new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

export function renderChips(el, onPick) {
  const items = getLastThree();
  if (!items.length) {
    el.innerHTML = `<span class="empty-chips">No stored searches yet. Enter, Search, or change a facet to store one.</span>`;
    return;
  }
  el.innerHTML = items
    .map((item, i) => {
      const label = item.q || "(facets only)";
      const extra = [item.facets.type, item.facets.week, item.facets.status, item.facets.used]
        .filter(Boolean)
        .join(" · ");
      return `<button type="button" class="chip" data-i="${i}">${i + 1}. ${escapeHtml(label)}${extra ? " · " + escapeHtml(extra) : ""}<time>${fmtTime(item.ts)}</time></button>`;
    })
    .join("");
  el.querySelectorAll(".chip").forEach((btn) => {
    btn.addEventListener("click", () => onPick(items[Number(btn.dataset.i)]));
  });
}

export function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

export function resultRow(rec) {
  return `<tr>
    <td><a href="${rec.href}">${escapeHtml(rec.id)}</a></td>
    <td><span class="badge">${escapeHtml(rec.type)}</span></td>
    <td>${escapeHtml(rec.title)}</td>
    <td>${escapeHtml(rec.excerpt)}</td>
    <td>${escapeHtml(rec.used_in_tab || rec.source_tab || "")}</td>
    <td><span class="badge ${escapeHtml(rec.status || "")}">${escapeHtml(rec.status || "—")}</span></td>
  </tr>`;
}

export async function initDashboard() {
  const index = await loadJSON("data/index.json");
  const counts = await loadJSON("data/counts.json");

  document.getElementById("n-ref").textContent = counts.references;
  document.getElementById("n-theme").textContent = counts.themes;
  document.getElementById("n-pl-open").textContent = counts.parking_open;
  document.getElementById("n-iq-aligned").textContent = counts.interview_aligned;
  document.getElementById("n-iq-unaligned").textContent = counts.interview_unaligned;
  document.getElementById("n-index").textContent = counts.index;

  const qEl = document.getElementById("q");
  const typeEl = document.getElementById("facet-type");
  const weekEl = document.getElementById("facet-week");
  const statusEl = document.getElementById("facet-status");
  const usedEl = document.getElementById("facet-used");
  const chipsEl = document.getElementById("last-three");
  const bodyEl = document.getElementById("result-body");
  const metaEl = document.getElementById("result-meta");
  const excelEl = document.getElementById("excel-mirror");

  const types = [...new Set(index.map((r) => r.type).filter(Boolean))].sort();
  const weeks = [...new Set(index.map((r) => r.week).filter(Boolean))].sort();
  const statuses = [...new Set(index.map((r) => r.status).filter(Boolean))].sort();
  const used = [...new Set(index.map((r) => r.used_in_tab).filter(Boolean))].sort();
  fillSelect(typeEl, types);
  fillSelect(weekEl, weeks);
  fillSelect(statusEl, statuses);
  fillSelect(usedEl, used);

  const params = new URLSearchParams(location.search);
  if (params.get("q")) qEl.value = params.get("q");
  if (params.get("type")) typeEl.value = params.get("type");

  const facetsOf = () => ({
    type: typeEl.value,
    week: weekEl.value,
    status: statusEl.value,
    used: usedEl.value,
  });

  function paint(store) {
    const query = qEl.value;
    const facets = facetsOf();
    const hits = index.filter((r) => matches(r, query, facets));
    metaEl.textContent = `${hits.length} of ${index.length} data points`;
    bodyEl.innerHTML = hits.slice(0, 200).map(resultRow).join("") || `<tr><td colspan="6">No matching data points.</td></tr>`;
    if (hits.length > 200) {
      metaEl.textContent += ` · showing first 200`;
    }
    if (store) recordSearch(query, facets);
    renderChips(chipsEl, (item) => {
      qEl.value = item.q || "";
      typeEl.value = item.facets.type || "";
      weekEl.value = item.facets.week || "";
      statusEl.value = item.facets.status || "";
      usedEl.value = item.facets.used || "";
      paint(false);
    });
    const mirror = JSON.parse(localStorage.getItem(EXCEL_MIRROR_KEY) || "{}");
    excelEl.textContent = `LastSearch1: ${label(mirror.LastSearch1)} · LastSearch2: ${label(mirror.LastSearch2)} · LastSearch3: ${label(mirror.LastSearch3)}`;
  }

  function label(entry) {
    if (!entry) return "(empty)";
    return entry.q || "(facets only)";
  }

  qEl.addEventListener("input", () => paint(false));
  qEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      paint(true);
    }
  });
  document.getElementById("do-search").addEventListener("click", () => paint(true));
  [typeEl, weekEl, statusEl, usedEl].forEach((el) => el.addEventListener("change", () => paint(true)));
  document.getElementById("clear-filters").addEventListener("click", () => {
    qEl.value = "";
    typeEl.value = "";
    weekEl.value = "";
    statusEl.value = "";
    usedEl.value = "";
    paint(false);
  });
  document.getElementById("export-history").addEventListener("click", () => {
    const blob = new Blob(
      [JSON.stringify({ last_three: getLastThree(), excel_mirror: JSON.parse(localStorage.getItem(EXCEL_MIRROR_KEY) || "{}") }, null, 2)],
      { type: "application/json" }
    );
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "search_history.json";
    a.click();
    URL.revokeObjectURL(a.href);
  });

  paint(Boolean(qEl.value || typeEl.value));
}

function fillSelect(el, values) {
  const keep = el.value;
  el.innerHTML = `<option value="">All</option>` + values.map((v) => `<option>${escapeHtml(v)}</option>`).join("");
  el.value = keep;
}

if (document.body.dataset.page === "01_DASHBOARD") {
  const start = () =>
    initDashboard().catch((err) => {
      const meta = document.getElementById("result-meta");
      if (meta) meta.textContent = err.message;
    });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
}
