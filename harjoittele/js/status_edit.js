// Changes the `status` of items in exercise files, as text, without
// re-serialising the JSON, so the diff in git shows only the status lines.
// Shared by tools/set_status.js (Node) and the merge tab of tarkista.html
// (browser). No DOM, no fs.

const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export const STATUS_FOR_BAND = { '7-9': 'approved', '1-6': 'reviewed' };

// text: contents of an exercise file. band: '7-9' or '1-6'.
// Returns { text, result: 'changed' | 'already' | 'missing', from }.
// Grades 7-9 items have "type" and "status" right after the id; grades 1-6
// items have other fields in between, so the first status after the id is
// the item's own.
export function editStatus(text, id, band, status = STATUS_FOR_BAND[band]) {
  const e = escapeRe(id);
  const re = band === '7-9'
    ? new RegExp(`("id": "${e}",\\s*"type": "[A-Z]+",\\s*"status": ")([a-z]+)(")`)
    : new RegExp(`("id": "${e}"[\\s\\S]*?"status": ")([a-z]+)(")`);
  const m = text.match(re);
  if (!m) return { text, result: 'missing', from: null };
  if (m[2] === status) return { text, result: 'already', from: m[2] };
  return { text: text.replace(re, `$1${status}$3`), result: 'changed', from: m[2] };
}

function sortKeys(obj) {
  return Object.fromEntries(Object.entries(obj).sort(([a], [b]) => a.localeCompare(b)));
}

function move(counts, from, to) {
  const next = { ...counts };
  next[from] = (next[from] || 0) - 1;
  if (next[from] <= 0) delete next[from];
  next[to] = (next[to] || 0) + 1;
  return sortKeys(next);
}

// manifest: parsed data/manifest.json. changes: [{ path, from, to }] with
// `path` as in the manifest (../math-misconceptions/...). Returns a new
// manifest with only the status counts changed, equal to what
// tools/build_manifest.js would write.
export function updateManifest(manifest, changes) {
  const next = JSON.parse(JSON.stringify(manifest));
  for (const c of changes) {
    const file = next.files.find((f) => f.path === c.path);
    if (!file) throw new Error(`Not in manifest: ${c.path}`);
    file.by_status = move(file.by_status, c.from, c.to);
    next.totals.by_status = move(next.totals.by_status, c.from, c.to);
  }
  return next;
}

export function serializeManifest(manifest) {
  return `${JSON.stringify(manifest, null, 2)}\n`;
}
