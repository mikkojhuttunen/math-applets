// Finnish feedback texts per misconception (data/misconceptions_fi.json).
//
// feedbackFor(texts, id, { includeDrafts }) returns
//   { id, name, pupil, teacher, applets, status }  or null.
// A sub-variant without its own entry falls back to its parent
// (NUM-10a -> NUM-10). Like exercises (WD2), draft texts are returned only
// with includeDrafts (teacher view); pupils then get the page's general hint.

export async function loadMisconceptions(url, { fetchImpl = globalThis.fetch } = {}) {
  const res = await fetchImpl(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  return data.misconceptions || {};
}

export function parentId(id) {
  const m = /^([A-Z]{3}-\d{2})[a-z]$/.exec(id || '');
  return m ? m[1] : null;
}

export function feedbackFor(texts, id, { includeDrafts = false } = {}) {
  if (!texts || !id) return null;
  for (const key of [id, parentId(id)]) {
    const entry = key && texts[key];
    if (!entry) continue;
    if (entry.status !== 'reviewed' && !includeDrafts) return null;
    return {
      id: key,
      name: entry.name_fi,
      pupil: entry.pupil,
      teacher: entry.teacher,
      applets: entry.applets || [],
      status: entry.status,
    };
  }
  return null;
}
