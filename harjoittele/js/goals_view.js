// Data for the goal browser (tavoitteet.html). No DOM.

import { misconceptionIds, sortIds } from './filters.js';

export const BAND_TITLES = { '1-2': 'Luokat 1–2', '3-6': 'Luokat 3–6', '7-9': 'Luokat 7–9' };

// One row per curriculum goal with what the site has for it.
// items: all items, drafts included (pupilReady tells them apart).
export function goalRows(goals, items, goalApplets = {}) {
  const byGoal = new Map();
  for (const item of items) {
    for (const g of item.goals) {
      if (!byGoal.has(g)) byGoal.set(g, []);
      byGoal.get(g).push(item);
    }
  }
  return sortIds(Object.keys(goals)).map((id) => {
    const list = byGoal.get(id) || [];
    return {
      id,
      ...goals[id],
      items: list.length,
      reviewed: list.filter((i) => i.pupilReady).length,
      misconceptions: sortIds([...new Set(list.flatMap((i) => misconceptionIds(i)))].filter((m) => !/[a-z]$/.test(m))),
      applets: goalApplets[id] || [],
    };
  });
}

function norm(s) {
  return String(s || '').toLocaleLowerCase('fi').trim();
}

// filters: { query, band: '' | '1-2' | '3-6' | '7-9', withContent: bool }
// An exact id match returns just that goal.
export function searchGoals(rows, { query = '', band = '', withContent = false } = {}) {
  const q = norm(query);
  const exact = rows.filter((r) => norm(r.id) === q);
  if (exact.length) return exact;
  return rows.filter((r) => {
    if (band && r.band !== band) return false;
    if (withContent && !r.items && !r.applets.length) return false;
    if (!q) return true;
    return [r.id, r.text, r.area].some((s) => norm(s).includes(q));
  });
}

// [{ band, areas: [{ area, rows }] }] in file order.
export function groupRows(rows) {
  const bands = new Map();
  for (const r of rows) {
    if (!bands.has(r.band)) bands.set(r.band, new Map());
    const areas = bands.get(r.band);
    const key = r.area || '';
    if (!areas.has(key)) areas.set(key, []);
    areas.get(key).push(r);
  }
  return [...bands].map(([band, areas]) => ({ band, areas: [...areas].map(([area, list]) => ({ area, rows: list })) }));
}
