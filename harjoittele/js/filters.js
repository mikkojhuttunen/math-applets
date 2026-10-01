// Filtering and counting of items, shared by the practice page and the
// teacher view. No DOM.

import { parentId } from './misconceptions.js';

// Every misconception id an item touches: its own tags, and the ids on its
// stored wrong answers or wrong options, plus their parents (NUM-10a -> NUM-10).
export function misconceptionIds(item) {
  const ids = new Set(item.misconceptions || []);
  for (const w of item.wrong || []) if (w.misconception) ids.add(w.misconception);
  for (const o of item.options || []) if (o.misconception) ids.add(o.misconception);
  for (const id of [...ids]) {
    const p = parentId(id);
    if (p) ids.add(p);
  }
  return [...ids].sort();
}

// filters: { status: 'all' | 'draft' | 'reviewed', band: '' | '1-6' | '7-9',
//            goal: '', misconception: '', query: '' }
export function filterItems(items, filters = {}) {
  const q = (filters.query || '').trim().toLowerCase();
  return items.filter((item) => {
    if (filters.status === 'draft' && item.pupilReady) return false;
    if (filters.status === 'reviewed' && !item.pupilReady) return false;
    if (filters.band && item.gradeBand !== filters.band) return false;
    if (filters.goal && !item.goals.includes(filters.goal)) return false;
    if (filters.misconception && !misconceptionIds(item).includes(filters.misconception)) return false;
    if (q && !`${item.id} ${item.stem}`.toLowerCase().includes(q)) return false;
    return true;
  });
}

function countInto(counter, key) {
  counter[key] = (counter[key] || 0) + 1;
}

// { total, reviewed, draft, byGoal: {id: n}, byMisconception: {id: n} }
export function summarize(items) {
  const s = { total: items.length, reviewed: 0, draft: 0, byGoal: {}, byMisconception: {} };
  for (const item of items) {
    if (item.pupilReady) s.reviewed++;
    else s.draft++;
    item.goals.forEach((g) => countInto(s.byGoal, g));
    misconceptionIds(item).forEach((m) => countInto(s.byMisconception, m));
  }
  return s;
}

// Natural sort for ids such as A36.S2.4 / A36.S2.12 and NUM-10a.
export function sortIds(ids) {
  return [...ids].sort((a, b) => a.localeCompare(b, 'fi', { numeric: true }));
}

// Selected ids grouped for the copy-out list, in natural order.
export function selectionText(ids) {
  return sortIds(ids).join('\n');
}

// Filters from the practice page's URL: ?tavoite=, ?luokat=, ?virhe=.
// Returns the filter object for filterItems() and a list of what was set.
export function filtersFromParams(params) {
  const filters = {
    goal: params.get('tavoite') || '',
    band: params.get('luokat') || '',
    misconception: params.get('virhe') || '',
  };
  return { filters, active: Object.values(filters).some(Boolean) };
}

export function paramsFromFilters(filters) {
  const p = new URLSearchParams();
  if (filters.goal) p.set('tavoite', filters.goal);
  if (filters.band) p.set('luokat', filters.band);
  if (filters.misconception) p.set('virhe', filters.misconception);
  return p;
}

// Topic title for pupils: the hand-written title if there is one, else the
// curriculum text with a capital first letter, else the id.
export function topicTitle(goalId, topics = {}, goals = {}) {
  if (topics[goalId]) return topics[goalId];
  const g = goals[goalId];
  if (g && g.text) return g.text.charAt(0).toUpperCase() + g.text.slice(1);
  return goalId;
}

// Goals that have items, grouped by grade band, for the start screen.
// [{ band: '1-6' | '7-9', goals: [{ id, count }] }]
export function startChoices(items) {
  const bands = new Map();
  for (const item of items) {
    if (!bands.has(item.gradeBand)) bands.set(item.gradeBand, new Map());
    const counts = bands.get(item.gradeBand);
    for (const g of item.goals) counts.set(g, (counts.get(g) || 0) + 1);
  }
  return [...bands.keys()].sort().map((band) => ({
    band,
    goals: sortIds([...bands.get(band).keys()]).map((id) => ({ id, count: bands.get(band).get(id) })),
  }));
}
