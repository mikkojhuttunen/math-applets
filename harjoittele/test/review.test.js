import test from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import {
  CHECKS, verdictProblem, topicOf, paramsFromSearch, searchFromParams, buildQueue, progress,
  setVerdict, clearVerdict, buildReviewFile, reviewFileName, parseReviewFile, mergeReviews,
  countOutcomes, approvedText, fixesText,
} from '../js/review.js';
import { loadItems } from '../js/items.js';
import { SITE_DIR, fileFetch, fileUrl } from './helpers.js';

const NOW = new Date('2026-10-17T10:00:00Z');
const ALL = Object.fromEntries(CHECKS.map((c) => [c.id, true]));
const ITEMS = [
  { id: 'ALG-04-MC-002', gradeBand: '7-9', goals: ['S3.02'], kind: 'choice', pupilReady: false, stem: 'Sievennä.' },
  { id: 'ALG-04-NE-001', gradeBand: '7-9', goals: ['S3.02'], kind: 'entry', pupilReady: false, stem: 'Laske.' },
  { id: 'NUM-01-MC-001', gradeBand: '7-9', goals: ['S2.01'], kind: 'choice', pupilReady: false, stem: 'Kumpi?' },
  { id: 'A36.S2.04-sub-1-001', gradeBand: '1-6', goals: ['A36.S2.04'], kind: 'entry', pupilReady: false, stem: 'Laske 5 − 2.' },
  { id: 'ALG-01-MC-001', gradeBand: '7-9', goals: ['S3.01'], kind: 'choice', pupilReady: true, stem: 'Valmis.' },
];

test('approve needs all four checks; fix and reject need a comment', () => {
  assert.match(verdictProblem('approve', '', {}), /Rastita/);
  assert.match(verdictProblem('approve', '', { answer: true }), /Rastita/);
  assert.strictEqual(verdictProblem('approve', '', ALL), '');
  assert.match(verdictProblem('fix', '   '), /kommentti/);
  assert.strictEqual(verdictProblem('fix', 'Vastaus 4 on väärin'), '');
  assert.match(verdictProblem('reject', ''), /kommentti/);
  assert.match(verdictProblem('maybe', 'x'), /Tuntematon/);
  assert.match(verdictProblem('fix', 'x'.repeat(2001)), /pitkä/);
});

test('topicOf: bank topic for 7-9, goal for 1-6', () => {
  assert.strictEqual(topicOf(ITEMS[0]), 'ALG-04');
  assert.strictEqual(topicOf(ITEMS[3]), 'A36.S2.04');
});

test('URL parameters round trip and ignore junk', () => {
  const f = paramsFromSearch('?lk=7-9&aihe=ALG-04&tyyppi=valinta&kaikki=1');
  assert.deepStrictEqual(f, { band: '7-9', topic: 'ALG-04', kind: 'valinta', all: true });
  assert.strictEqual(searchFromParams(f), '?lk=7-9&aihe=ALG-04&tyyppi=valinta&kaikki=1');
  assert.deepStrictEqual(paramsFromSearch('?lk=5&tyyppi=x'), { band: '', topic: '', kind: '', all: false });
  assert.strictEqual(searchFromParams({}), '');
});

test('buildQueue leaves out approved items and applies filters', () => {
  assert.deepStrictEqual(buildQueue(ITEMS, {}).map((i) => i.id), ['A36.S2.04-sub-1-001', 'ALG-04-MC-002', 'ALG-04-NE-001', 'NUM-01-MC-001']);
  assert.deepStrictEqual(buildQueue(ITEMS, { band: '1-6' }).map((i) => i.id), ['A36.S2.04-sub-1-001']);
  assert.deepStrictEqual(buildQueue(ITEMS, { topic: 'alg-04' }).map((i) => i.id), ['ALG-04-MC-002', 'ALG-04-NE-001']);
  assert.deepStrictEqual(buildQueue(ITEMS, { topic: 'S2.01' }).map((i) => i.id), ['NUM-01-MC-001']);
  assert.deepStrictEqual(buildQueue(ITEMS, { kind: 'vastaus' }).map((i) => i.id), ['A36.S2.04-sub-1-001', 'ALG-04-NE-001']);
  const verdicts = setVerdict({}, 'ALG-04-MC-002', 'approve', '');
  assert.deepStrictEqual(buildQueue(ITEMS, { topic: 'ALG-04', unjudged: true }, verdicts).map((i) => i.id), ['ALG-04-NE-001']);
});

test('progress counts verdicts inside the queue only', () => {
  let v = setVerdict({}, 'ALG-04-MC-002', 'approve', '');
  v = setVerdict(v, 'ALG-04-NE-001', 'fix', ' tarkenna ');
  v = setVerdict(v, 'OTHER-1', 'reject', 'x');
  assert.strictEqual(v['ALG-04-NE-001'].comment, 'tarkenna');
  assert.deepStrictEqual(progress(buildQueue(ITEMS, { topic: 'ALG-04' }), v), { total: 2, judged: 2, approve: 1, fix: 1, reject: 0 });
  assert.strictEqual(clearVerdict(v, 'OTHER-1')['OTHER-1'], undefined);
});

test('review file: build, name and parse', () => {
  const verdicts = { 'B-2': { verdict: 'fix', comment: 'x' }, 'A-1': { verdict: 'approve', comment: '' } };
  const file = buildReviewFile({ reviewer: '  Maija   Äänätön ', verdicts, bankSize: 740, now: NOW });
  assert.strictEqual(file.reviewer, 'Maija Äänätön');
  assert.deepStrictEqual(file.verdicts.map((v) => v.id), ['A-1', 'B-2']);
  assert.strictEqual(file.created, '2026-10-17');
  assert.strictEqual(reviewFileName('Maija Äänätön', NOW), 'tarkistus-maija-aanaton-2026-10-17.json');
  assert.strictEqual(reviewFileName('', NOW), 'tarkistus-tarkastaja-2026-10-17.json');
  const parsed = parseReviewFile(JSON.stringify(file));
  assert.strictEqual(parsed.ok, true);
  assert.strictEqual(parsed.file.bankItems, 740);
  assert.strictEqual(parsed.file.verdicts.length, 2);
});

test('parseReviewFile rejects bad input', () => {
  const good = { format: 'harjoittele-tarkistus', version: 1, reviewer: 'A', verdicts: [{ id: 'x', verdict: 'approve' }] };
  assert.strictEqual(parseReviewFile(JSON.stringify(good)).ok, true);
  const bad = (patch) => parseReviewFile(JSON.stringify({ ...good, ...patch })).ok;
  assert.strictEqual(parseReviewFile('{ei json').ok, false);
  assert.strictEqual(parseReviewFile('null').ok, false);
  assert.strictEqual(bad({ format: 'muu' }), false);
  assert.strictEqual(bad({ version: 2 }), false);
  assert.strictEqual(bad({ reviewer: '  ' }), false);
  assert.strictEqual(bad({ verdicts: 'x' }), false);
  assert.strictEqual(bad({ verdicts: [{ id: 'x', verdict: 'nope' }] }), false);
  assert.strictEqual(bad({ verdicts: [{ id: '', verdict: 'fix' }] }), false);
  assert.strictEqual(bad({ verdicts: [{ id: 'x', verdict: 'fix' }, { id: 'x', verdict: 'fix' }] }), false);
});

function file(reviewer, rows) {
  return { reviewer, created: '2026-10-17', bankItems: 740, verdicts: rows.map(([id, verdict, comment = '']) => ({ id, verdict, comment })) };
}
const BY_ID = Object.fromEntries(ITEMS.map((i) => [i.id, i]));

test('mergeReviews outcomes with one and two approvals needed', () => {
  const a = file('Aino', [['ALG-04-MC-002', 'approve'], ['ALG-04-NE-001', 'approve'], ['NUM-01-MC-001', 'fix', 'D on väärin']]);
  const b = file('Eero', [['ALG-04-MC-002', 'approve'], ['ALG-04-NE-001', 'reject', 'Ei sovi'], ['NUM-01-MC-001', 'approve'], ['ZZZ-99-MC-001', 'approve']]);
  const one = mergeReviews([a, b], { itemsById: BY_ID, minApprovals: 1 });
  const get = (m, id) => m.rows.find((r) => r.id === id);
  assert.strictEqual(get(one, 'ALG-04-MC-002').outcome, 'ready');
  assert.strictEqual(get(one, 'ALG-04-NE-001').outcome, 'conflict');
  assert.strictEqual(get(one, 'NUM-01-MC-001').outcome, 'conflict');
  assert.strictEqual(get(one, 'ZZZ-99-MC-001').known, false);
  const solo = mergeReviews([file('Aino', [['ALG-04-MC-002', 'approve']])], { itemsById: BY_ID, minApprovals: 2 });
  assert.strictEqual(solo.rows[0].outcome, 'waiting');
  const only = mergeReviews([file('Aino', [['ALG-04-NE-001', 'fix', 'k']]), file('Eero', [['NUM-01-MC-001', 'reject', 'r']])], { itemsById: BY_ID });
  assert.strictEqual(get(only, 'ALG-04-NE-001').outcome, 'fix');
  assert.strictEqual(get(only, 'NUM-01-MC-001').outcome, 'reject');
});

test('same reviewer in two files counts once, later file wins', () => {
  const first = file('Aino', [['ALG-04-MC-002', 'fix', 'kesken']]);
  const second = file('aino', [['ALG-04-MC-002', 'approve']]);
  const m = mergeReviews([first, second], { itemsById: BY_ID, minApprovals: 2 });
  assert.deepStrictEqual(m.people, ['Aino']);
  assert.strictEqual(m.rows[0].approve, 1);
  assert.strictEqual(m.rows[0].fix, 0);
  assert.strictEqual(m.rows[0].outcome, 'waiting');
});

test('count, approved list and fix list', () => {
  const a = file('Aino', [['ALG-04-MC-002', 'approve'], ['ALG-04-NE-001', 'fix', 'Vastaus puuttuu'], ['ALG-01-MC-001', 'approve'], ['ZZZ-99-MC-001', 'approve']]);
  const m = mergeReviews([a], { itemsById: BY_ID });
  assert.deepStrictEqual(countOutcomes(m.rows), { ready: 1, waiting: 0, conflict: 0, fix: 1, reject: 0, unknown: 1, already: 1 });
  const text = approvedText(m.rows, NOW);
  assert.ok(text.includes('1 kpl'));
  assert.deepStrictEqual(text.match(/[A-Z]{2,3}-\d{2}-[A-Z]{2}-\d{3}/g), ['ALG-04-MC-002']);
  const fixes = fixesText(m.rows, BY_ID, NOW);
  assert.ok(fixes.includes('ALG-04-NE-001 (korjattava)'));
  assert.ok(fixes.includes('Aino korjattava: Vastaus puuttuu'));
  assert.ok(fixes.includes('Tehtävä: Laske.'));
  assert.ok(!fixes.includes('ALG-04-MC-002'));
});

test('against the real bank: every reviewable draft is queued and topics exist', async () => {
  const r = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  const queue = buildQueue(r.items, {});
  assert.strictEqual(queue.length, r.items.filter((i) => !i.pupilReady).length);
  assert.ok(queue.every((i) => topicOf(i)));
  assert.strictEqual(new Set(queue.map((i) => i.id)).size, queue.length);
});
