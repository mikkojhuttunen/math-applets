import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { misconceptionIds, filterItems, summarize, sortIds, selectionText } from '../js/filters.js';
import { loadItems } from '../js/items.js';
import { SITE_DIR, fileFetch, fileUrl } from './helpers.js';

const A = { id: 'a1', stem: 'Laske 916 − 140.', gradeBand: '1-6', goals: ['A36.S2.04'], pupilReady: false, misconceptions: ['NUM-10'],
  wrong: [{ match: '836', misconception: 'NUM-10a' }] };
const B = { id: 'b1', stem: 'Kumpi on suurempi?', gradeBand: '1-6', goals: ['A36.S2.11'], pupilReady: true, misconceptions: ['NUM-12'],
  options: [{ id: 'a', misconception: null }, { id: 'b', misconception: 'NUM-12' }] };
const C = { id: 'c1', stem: 'Avaa sulut', gradeBand: '7-9', goals: ['S3.02'], pupilReady: false, misconceptions: ['ALG-08'],
  wrong: [{ match: '5x − 35', misconception: 'ALG-07' }] };

test('misconceptionIds collects tags, wrong answers, options and parents', () => {
  assert.deepStrictEqual(misconceptionIds(A), ['NUM-10', 'NUM-10a']);
  assert.deepStrictEqual(misconceptionIds(B), ['NUM-12']);
  assert.deepStrictEqual(misconceptionIds(C), ['ALG-07', 'ALG-08']);
});

test('filterItems by status, band, goal, misconception and text', () => {
  const all = [A, B, C];
  assert.deepStrictEqual(filterItems(all, { status: 'draft' }).map((i) => i.id), ['a1', 'c1']);
  assert.deepStrictEqual(filterItems(all, { status: 'reviewed' }).map((i) => i.id), ['b1']);
  assert.deepStrictEqual(filterItems(all, { band: '7-9' }).map((i) => i.id), ['c1']);
  assert.deepStrictEqual(filterItems(all, { goal: 'A36.S2.04' }).map((i) => i.id), ['a1']);
  assert.deepStrictEqual(filterItems(all, { misconception: 'NUM-10a' }).map((i) => i.id), ['a1']);
  assert.deepStrictEqual(filterItems(all, { misconception: 'ALG-07' }).map((i) => i.id), ['c1']);
  assert.deepStrictEqual(filterItems(all, { query: '916' }).map((i) => i.id), ['a1']);
  assert.deepStrictEqual(filterItems(all, { query: 'B1' }).map((i) => i.id), ['b1']);
  assert.strictEqual(filterItems(all, {}).length, 3);
});

test('summarize counts statuses, goals and misconceptions', () => {
  const s = summarize([A, B, C]);
  assert.deepStrictEqual([s.total, s.reviewed, s.draft], [3, 1, 2]);
  assert.deepStrictEqual(s.byGoal, { 'A36.S2.04': 1, 'A36.S2.11': 1, 'S3.02': 1 });
  assert.strictEqual(s.byMisconception['NUM-10'], 1);
});

test('sortIds sorts numbers inside ids naturally', () => {
  assert.deepStrictEqual(sortIds(['A36.S2.12', 'A36.S2.4', 'NUM-10b', 'NUM-10a', 'NUM-9']),
    ['A36.S2.4', 'A36.S2.12', 'NUM-9', 'NUM-10a', 'NUM-10b']);
  assert.strictEqual(selectionText(['b', 'a']), 'a\nb');
});

test('teacher view counts agree with the manifest', async () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(SITE_DIR, 'data', 'manifest.json'), 'utf8'));
  const { items, skipped } = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  const s = summarize(items);
  assert.strictEqual(s.total + skipped.length, manifest.totals.items);
  // With nothing skipped, the per-goal and per-status counts must match exactly.
  if (skipped.length === 0) {
    assert.deepStrictEqual(s.byGoal, manifest.totals.by_goal);
    const reviewed = (manifest.totals.by_status.reviewed || 0) + (manifest.totals.by_status.approved || 0);
    assert.strictEqual(s.reviewed, reviewed);
  }
});

import { filtersFromParams, paramsFromFilters, topicTitle, startChoices } from '../js/filters.js';
import { buildGoals, serialize as serializeGoals, GOALS_PATH, parseGoals } from '../tools/build_goals.js';

test('URL parameters to filters and back', () => {
  const { filters, active } = filtersFromParams(new URLSearchParams('tavoite=A36.S2.04&virhe=NUM-10'));
  assert.deepStrictEqual(filters, { goal: 'A36.S2.04', band: '', misconception: 'NUM-10' });
  assert.strictEqual(active, true);
  assert.strictEqual(filtersFromParams(new URLSearchParams('luonnokset=1')).active, false);
  assert.strictEqual(paramsFromFilters(filters).toString(), 'tavoite=A36.S2.04&virhe=NUM-10');
});

test('topicTitle prefers the hand-written title, then the curriculum text', () => {
  const goals = { 'A36.S2.01': { text: 'ymmärtää kymmenjärjestelmän' } };
  assert.strictEqual(topicTitle('A36.S2.04', { 'A36.S2.04': 'Vähennyslasku' }, goals), 'Vähennyslasku');
  assert.strictEqual(topicTitle('A36.S2.01', {}, goals), 'Ymmärtää kymmenjärjestelmän');
  assert.strictEqual(topicTitle('X.1', {}, goals), 'X.1');
});

test('startChoices groups goals with item counts by band', () => {
  assert.deepStrictEqual(startChoices([A, B, C]), [
    { band: '1-6', goals: [{ id: 'A36.S2.04', count: 1 }, { id: 'A36.S2.11', count: 1 }] },
    { band: '7-9', goals: [{ id: 'S3.02', count: 1 }] },
  ]);
});

test('parseGoals reads only section 3 tables, with area and 7-9 grade', () => {
  const md = [
    '## 2. Tavoitteet', '| S2.01 | ei tämä | 7 | T1 |',
    '## 3. Atomiset', '### S2 Luvut', '| ID | Oppilas osaa… | Lk | T |', '| S2.01 | laskea | 7 | T10 |',
    '#### S3 Algebra', '| A36.S3.01 | tutkia | T5 |',
    '## 4. Kriteerit', '| S2.02 | ei tämäkään | 8 | T1 |',
  ].join('\n');
  assert.deepStrictEqual(parseGoals(md), {
    'S2.01': { text: 'laskea', band: '7-9', area: 'S2 Luvut', grade: '7' },
    'A36.S3.01': { text: 'tutkia', band: '3-6', area: 'S3 Algebra' },
  });
});

test('data/goals.json is up to date (run: node tools/build_goals.js)', () => {
  assert.strictEqual(fs.readFileSync(GOALS_PATH, 'utf8'), serializeGoals(buildGoals()));
});

test('every goal used by the banks exists and has a pupil title', async () => {
  const goals = JSON.parse(fs.readFileSync(GOALS_PATH, 'utf8')).goals;
  const topics = JSON.parse(fs.readFileSync(path.join(SITE_DIR, 'data', 'topics_fi.json'), 'utf8')).topics;
  const { items } = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  for (const g of new Set(items.flatMap((i) => i.goals))) {
    assert.ok(goals[g], `goal ${g} is not in the curriculum files`);
    assert.ok(topics[g], `goal ${g} has no title in data/topics_fi.json`);
  }
  for (const g of Object.keys(topics)) assert.ok(goals[g], `topics_fi.json has an unknown goal ${g}`);
});
