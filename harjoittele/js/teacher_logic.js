// Filtering and counting for the teacher view (opettaja.html). No DOM.

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
