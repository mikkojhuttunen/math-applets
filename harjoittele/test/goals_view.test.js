import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { goalRows, searchGoals, groupRows } from '../js/goals_view.js';
import { loadItems } from '../js/items.js';
import { SITE_DIR, fileFetch, fileUrl } from './helpers.js';

const REPO = path.resolve(SITE_DIR, '..');
const goals = {
  'A36.S2.04': { text: 'käyttää yhteen- ja vähennyslaskualgoritmeja', band: '3-6', area: 'S2 Luvut ja laskutoimitukset' },
  'A36.S4.01': { text: 'tunnistaa kulmia', band: '3-6', area: 'S4 Geometria' },
  'S4.05': { text: 'piirtää suoran', band: '7-9', area: 'S4 Funktiot', grade: '8' },
};
const items = [
  { id: 'a', goals: ['A36.S2.04'], pupilReady: true, misconceptions: ['NUM-10'], wrong: [{ misconception: 'NUM-10a' }] },
  { id: 'b', goals: ['A36.S2.04'], pupilReady: false, misconceptions: ['NUM-10'], wrong: [] },
];

test('goalRows counts items, reviewed items, misconceptions and applets', () => {
  const rows = goalRows(goals, items, { 'S4.05': ['yla-aste-7-9/suoran-yhtalo.html'] });
  const r = rows.find((x) => x.id === 'A36.S2.04');
  assert.deepStrictEqual([r.items, r.reviewed, r.misconceptions], [2, 1, ['NUM-10']]);
  assert.deepStrictEqual(rows.find((x) => x.id === 'S4.05').applets, ['yla-aste-7-9/suoran-yhtalo.html']);
  assert.strictEqual(rows.find((x) => x.id === 'A36.S4.01').items, 0);
});

test('searchGoals: exact id, text, band and content filter', () => {
  const rows = goalRows(goals, items, { 'S4.05': ['x.html'] });
  assert.deepStrictEqual(searchGoals(rows, { query: 'a36.s2.04' }).map((r) => r.id), ['A36.S2.04']);
  assert.deepStrictEqual(searchGoals(rows, { query: 'KULMIA' }).map((r) => r.id), ['A36.S4.01']);
  assert.deepStrictEqual(searchGoals(rows, { query: 'geometria' }).map((r) => r.id), ['A36.S4.01']);
  assert.deepStrictEqual(searchGoals(rows, { band: '7-9' }).map((r) => r.id), ['S4.05']);
  assert.deepStrictEqual(searchGoals(rows, { withContent: true }).map((r) => r.id), ['A36.S2.04', 'S4.05']);
  assert.strictEqual(searchGoals(rows, { query: 'ei löydy' }).length, 0);
});

test('groupRows groups by band and area', () => {
  const g = groupRows(goalRows(goals, items));
  assert.deepStrictEqual(g.map((b) => [b.band, b.areas.map((a) => a.area)]), [
    ['3-6', ['S2 Luvut ja laskutoimitukset', 'S4 Geometria']],
    ['7-9', ['S4 Funktiot']],
  ]);
});

test('goal_applets.json: goals exist and applet files exist', () => {
  const real = JSON.parse(fs.readFileSync(path.join(SITE_DIR, 'data', 'goals.json'), 'utf8')).goals;
  const map = JSON.parse(fs.readFileSync(path.join(SITE_DIR, 'data', 'goal_applets.json'), 'utf8')).applets;
  for (const [goal, applets] of Object.entries(map)) {
    assert.ok(real[goal], `unknown goal ${goal}`);
    for (const a of applets) assert.ok(fs.existsSync(path.join(REPO, a)), `${goal}: missing ${a}`);
  }
});

test('with the real data every goal used by the banks shows its items', async () => {
  const real = JSON.parse(fs.readFileSync(path.join(SITE_DIR, 'data', 'goals.json'), 'utf8')).goals;
  const { items: all } = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  const rows = goalRows(real, all);
  const total = rows.reduce((n, r) => n + r.items, 0);
  assert.strictEqual(total, all.reduce((n, i) => n + i.goals.length, 0));
  assert.strictEqual(rows.length, Object.keys(real).length);
});
