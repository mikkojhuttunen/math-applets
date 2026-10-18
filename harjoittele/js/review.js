// Logic of the review page (tarkista.html). No DOM, so it can be tested.
//
// A reviewer judges items one by one: approve, fix (needs changes) or
// reject. The judgments live in the reviewer's browser and leave it as a
// small JSON file the reviewer sends to whoever collects them. The
// collector merges the files on the same page and gets a list of ids to
// approve (read by tools/set_status.js) and a list of comments to act on.

export const VERDICTS = ['approve', 'fix', 'reject'];
export const FILE_FORMAT = 'harjoittele-tarkistus';
export const FILE_VERSION = 1;
export const MAX_COMMENT = 2000;
export const MAX_NAME = 60;

// Every item must pass these four checks before it can be approved.
export const CHECKS = [
  { id: 'answer', text: 'Oikea vastaus on varmasti oikein (laskin itse).' },
  { id: 'wrong', text: 'Väärät vaihtoehdot tai väärät vastaukset ovat varmasti vääriä.' },
  { id: 'text', text: 'Tehtävän ja palautteen suomi on selkeää eikä paljasta vastausta.' },
  { id: 'level', text: 'Tehtävä sopii luokka-asteelle ja tavoitteelle.' },
];

export function cleanName(name) {
  return String(name || '').replace(/\s+/g, ' ').trim().slice(0, MAX_NAME);
}

export function verdictProblem(verdict, comment, checks = {}) {
  if (!VERDICTS.includes(verdict)) return 'Tuntematon arvio.';
  const text = String(comment || '').trim();
  if (text.length > MAX_COMMENT) return `Kommentti on liian pitkä (enintään ${MAX_COMMENT} merkkiä).`;
  if (verdict === 'approve') {
    return CHECKS.every((c) => checks[c.id]) ? '' : 'Rastita kaikki neljä tarkistusta ennen hyväksymistä.';
  }
  return text ? '' : 'Kirjoita lyhyt kommentti: mitä pitää korjata tai miksi hylkäät.';
}

// Topic of an item for the topic filter: ALG-04 for grades 7-9, the goal id for 1-6.
export function topicOf(item) {
  if (item.gradeBand === '7-9') return item.id.split('-').slice(0, 2).join('-');
  return (item.goals && item.goals[0]) || item.id;
}

// URL parameters: ?lk=7-9  ?aihe=ALG-04  ?tyyppi=valinta|vastaus  ?kaikki=1
export function paramsFromSearch(search) {
  const p = new URLSearchParams(search);
  const band = p.get('lk');
  const kind = p.get('tyyppi');
  return {
    band: band === '1-6' || band === '7-9' ? band : '',
    topic: (p.get('aihe') || '').slice(0, 30),
    kind: kind === 'valinta' || kind === 'vastaus' ? kind : '',
    all: p.get('kaikki') === '1',
  };
}

export function searchFromParams(f) {
  const p = new URLSearchParams();
  if (f.band) p.set('lk', f.band);
  if (f.topic) p.set('aihe', f.topic);
  if (f.kind) p.set('tyyppi', f.kind);
  if (f.all) p.set('kaikki', '1');
  const s = p.toString();
  return s ? `?${s}` : '';
}

export function sortItems(items) {
  return [...items].sort((a, b) => a.id.localeCompare(b.id, 'fi', { numeric: true }));
}

// Items to review: drafts only (pupil-ready ones are done), then the filters.
// With f.unjudged the items that already have a verdict are left out.
export function buildQueue(items, f, verdicts = {}) {
  const out = items.filter((item) => {
    if (item.pupilReady) return false;
    if (f.band && item.gradeBand !== f.band) return false;
    if (f.topic && topicOf(item).toLowerCase() !== f.topic.toLowerCase() && !item.goals.includes(f.topic)) return false;
    if (f.kind === 'valinta' && item.kind !== 'choice') return false;
    if (f.kind === 'vastaus' && item.kind !== 'entry') return false;
    if (f.unjudged && verdicts[item.id]) return false;
    return true;
  });
  return sortItems(out);
}

export function progress(queue, verdicts) {
  const p = { total: queue.length, judged: 0, approve: 0, fix: 0, reject: 0 };
  for (const item of queue) {
    const v = verdicts[item.id];
    if (!v) continue;
    p.judged++;
    p[v.verdict]++;
  }
  return p;
}

export function setVerdict(verdicts, id, verdict, comment) {
  const next = { ...verdicts };
  next[id] = { verdict, comment: String(comment || '').trim() };
  return next;
}

export function clearVerdict(verdicts, id) {
  const next = { ...verdicts };
  delete next[id];
  return next;
}

function today(now) {
  return (now || new Date()).toISOString().slice(0, 10);
}

export function buildReviewFile({ reviewer, verdicts, bankSize, now }) {
  const rows = Object.entries(verdicts)
    .filter(([, v]) => v && VERDICTS.includes(v.verdict))
    .sort(([a], [b]) => a.localeCompare(b, 'fi', { numeric: true }))
    .map(([id, v]) => ({ id, verdict: v.verdict, comment: v.comment || '' }));
  return { format: FILE_FORMAT, version: FILE_VERSION, reviewer: cleanName(reviewer), created: today(now), bank: { items: bankSize || 0 }, verdicts: rows };
}

export function reviewFileName(reviewer, now) {
  const slug = cleanName(reviewer).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'tarkastaja';
  return `tarkistus-${slug}-${today(now)}.json`;
}

// Returns { ok: true, file } or { ok: false, error }. The file comes from a
// colleague, so every field is checked and nothing is trusted.
export function parseReviewFile(text) {
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    return { ok: false, error: 'Tiedosto ei ole JSON-muotoinen.' };
  }
  if (!data || data.format !== FILE_FORMAT) return { ok: false, error: 'Tämä ei ole tarkistustiedosto.' };
  if (data.version !== FILE_VERSION) return { ok: false, error: 'Tiedoston versio ei täsmää.' };
  const reviewer = cleanName(data.reviewer);
  if (!reviewer) return { ok: false, error: 'Tiedostosta puuttuu tarkastajan nimi.' };
  if (!Array.isArray(data.verdicts)) return { ok: false, error: 'Tiedostosta puuttuu arviolista.' };
  const seen = new Set();
  const verdicts = [];
  for (const v of data.verdicts) {
    if (!v || typeof v.id !== 'string' || !v.id || v.id.length > 80) return { ok: false, error: 'Arviolistassa on virheellinen tunniste.' };
    if (!VERDICTS.includes(v.verdict)) return { ok: false, error: `Tunnisteen ${v.id.slice(0, 40)} arvio on tuntematon.` };
    if (seen.has(v.id)) return { ok: false, error: `Tunniste ${v.id.slice(0, 40)} on listassa kahdesti.` };
    seen.add(v.id);
    verdicts.push({ id: v.id, verdict: v.verdict, comment: typeof v.comment === 'string' ? v.comment.slice(0, MAX_COMMENT) : '' });
  }
  const created = typeof data.created === 'string' ? data.created.slice(0, 10) : '';
  const bankItems = data.bank && Number.isFinite(data.bank.items) ? data.bank.items : 0;
  return { ok: true, file: { reviewer, created, bankItems, verdicts } };
}

// Files with the same reviewer name count as one person; where both judge
// the same item, the file added later wins.
export function combineByReviewer(files) {
  const people = new Map();
  for (const f of files) {
    const key = f.reviewer.toLowerCase();
    if (!people.has(key)) people.set(key, { reviewer: f.reviewer, verdicts: new Map() });
    const person = people.get(key);
    for (const v of f.verdicts) person.verdicts.set(v.id, v);
  }
  return [...people.values()];
}

// rule.minApprovals: approvals needed (default 1); anyone's fix or reject
// stops an item from being ready.
// outcome: ready | waiting | conflict | fix | reject
export function mergeReviews(files, { itemsById = {}, minApprovals = 1 } = {}) {
  const people = combineByReviewer(files);
  const byId = new Map();
  for (const person of people) {
    for (const v of person.verdicts.values()) {
      if (!byId.has(v.id)) byId.set(v.id, []);
      byId.get(v.id).push({ reviewer: person.reviewer, verdict: v.verdict, comment: v.comment });
    }
  }
  const rows = [];
  for (const [id, judgments] of byId) {
    const approve = judgments.filter((j) => j.verdict === 'approve').length;
    const fix = judgments.filter((j) => j.verdict === 'fix').length;
    const reject = judgments.filter((j) => j.verdict === 'reject').length;
    let outcome;
    if (approve && fix + reject) outcome = 'conflict';
    else if (reject) outcome = 'reject';
    else if (fix) outcome = 'fix';
    else outcome = approve >= minApprovals ? 'ready' : 'waiting';
    const item = itemsById[id] || null;
    rows.push({ id, judgments, approve, fix, reject, outcome, known: Boolean(item), alreadyApproved: Boolean(item && item.pupilReady) });
  }
  rows.sort((a, b) => a.id.localeCompare(b.id, 'fi', { numeric: true }));
  return { people: people.map((p) => p.reviewer), rows };
}

export function countOutcomes(rows) {
  const c = { ready: 0, waiting: 0, conflict: 0, fix: 0, reject: 0, unknown: 0, already: 0 };
  for (const r of rows) {
    if (!r.known) c.unknown++;
    else if (r.alreadyApproved) c.already++;
    else c[r.outcome]++;
  }
  return c;
}

// Ids to approve, one per line, for tools/set_status.js. The header has no
// ids in it, because the script reads every id it finds in the text.
export function approvedText(rows, now) {
  const ids = rows.filter((r) => r.outcome === 'ready' && r.known && !r.alreadyApproved).map((r) => r.id);
  const head = `Hyväksyttävät tehtävät ${today(now)}, ${ids.length} kpl. Aja: node tools/set_status.js <tämä tiedosto>`;
  return `${head}\n\n${ids.join('\n')}\n`;
}

const LABEL = { approve: 'hyväksyy', fix: 'korjattava', reject: 'hylkää' };

// Comments to act on: every item with a fix, reject or conflict outcome.
export function fixesText(rows, itemsById = {}, now) {
  const list = rows.filter((r) => ['fix', 'reject', 'conflict'].includes(r.outcome));
  const parts = [`Korjattavat ja ristiriitaiset tehtävät ${today(now)}, ${list.length} kpl`];
  for (const r of list) {
    const item = itemsById[r.id];
    parts.push('');
    parts.push(`${r.id} (${r.outcome === 'conflict' ? 'ristiriita' : r.outcome === 'reject' ? 'hylätty' : 'korjattava'})`);
    if (item) parts.push(`  Tehtävä: ${item.stem}`);
    for (const j of r.judgments) parts.push(`  ${j.reviewer} ${LABEL[j.verdict]}${j.comment ? `: ${j.comment}` : ''}`);
  }
  return `${parts.join('\n')}\n`;
}
