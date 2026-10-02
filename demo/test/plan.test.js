import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { loadItems } from '../../harjoittele/js/items.js';
import { checkAnswer, checkChoice } from '../../harjoittele/js/answers.js';
import { normalizeLukio, topicItems, seasonOf, parseHash, hashFor, planCounts } from '../js/plan.js';

const DEMO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REPO = path.resolve(DEMO, '..');
const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const fetchImpl = async (url) => {
  const p = fileURLToPath(url);
  if (!fs.existsSync(p)) return { ok: false, status: 404 };
  return { ok: true, json: async () => read(p) };
};

const plan = read(path.join(DEMO, 'data/plan.json'));
const lukioRaw = read(path.join(DEMO, 'data/lukio_items.json'));
const lukio = normalizeLukio(lukioRaw);
const bank = (await loadItems(pathToFileURL(path.join(REPO, 'harjoittele/data/manifest.json')).href, { fetchImpl, includeDrafts: true })).items;

test('every level has all three seasons with at least one topic', () => {
  assert.deepEqual(plan.levels.map((l) => l.id), ['1-3', '4-6', '7-9', 'pitka', 'lyhyt']);
  for (const level of plan.levels) {
    for (const s of plan.seasons) assert.ok((level.seasons[s.id] || []).length > 0, `${level.id} ${s.id}`);
  }
});

test('every topic has at least five exercises', () => {
  for (const row of planCounts(plan, bank, lukio)) assert.ok(row.count >= 5, `${row.level}/${row.season}/${row.title}: ${row.count}`);
});

test('grade-limited topics take only that grade', () => {
  const topic = { goal: 'S1.04', grade: 7 };
  const items = topicItems(topic, bank, lukio);
  assert.ok(items.length > 0);
  assert.ok(items.every((i) => i.grade === 7));
});

test('applet paths in the plan exist', () => {
  for (const level of plan.levels) {
    for (const topics of Object.values(level.seasons)) {
      for (const t of topics) for (const a of t.applets || []) assert.ok(fs.existsSync(path.join(REPO, a)), a);
    }
  }
});

test('every lukio item loads, and its answers grade as intended', () => {
  assert.equal(lukio.length, lukioRaw.items.length);
  const ids = new Set();
  for (const item of lukio) {
    assert.ok(!ids.has(item.id), `duplicate ${item.id}`);
    ids.add(item.id);
    if (item.kind === 'entry') {
      const right = item.answer.kind === 'typed' ? item.answer.value
        : item.answer.kind === 'expression' ? item.answer.reference
          : item.answer.kind === 'set' ? item.answer.values.join('; ') : String(item.answer.value);
      assert.equal(checkAnswer(item, right).result, 'correct', `${item.id} correct answer`);
      for (const w of item.wrong) {
        const r = checkAnswer(item, w.match);
        assert.equal(r.result, 'wrong', `${item.id} ${w.match}`);
        assert.equal(r.feedback, w.feedback, `${item.id} ${w.match} gets its own feedback`);
      }
    } else {
      for (const o of item.options) assert.equal(checkChoice(item, o.id).result, o.correct ? 'correct' : 'wrong');
    }
  }
});

test('lukio answers are mathematically right', () => {
  const byId = Object.fromEntries(lukio.map((i) => [i.id, i]));
  const num = (id) => byId[id].answer.value;
  const V = (x) => -2 * x * x + 40 * x - 100;
  assert.equal(num('DEMO-MAB-toisen-asteen-malli-01'), [...Array(41).keys()].reduce((b, x) => (V(x) > V(b) ? x : b), 0));
  assert.equal(num('DEMO-MAB-toisen-asteen-malli-02'), V(10));
  assert.equal(num('DEMO-MAB-toisen-asteen-malli-04'), 3 * (-2) ** 2 - 2);
  assert.ok(Math.abs(num('DEMO-MAB-prosentit-talous-03') - 1000 * 1.02 ** 2) < 1e-9);
  assert.ok(Math.abs(num('DEMO-MAB-prosentit-talous-02') - 110 * 0.9) < 1e-9);
  assert.equal(num('DEMO-MAA9-integraali-04'), 3 ** 3 / 3);
  assert.equal(num('DEMO-MAA2-yhtalot-05'), 6 / 2);
  assert.equal(num('DEMO-MAA6-derivaatta-03'), 2 * 1 - 2);
  assert.ok(Math.abs(num('DEMO-MAA7-yksikkoympyra-02') - Math.cos(Math.PI)) < 1e-12);
  assert.equal(num('DEMO-MAA8-eksp-log-01'), Math.log2(8));
});

test('seasonOf follows the school year', () => {
  const at = (m) => seasonOf(new Date(2026, m - 1, 15));
  assert.deepEqual([1, 2, 3, 6, 7, 8, 11, 12].map(at), ['talvi', 'talvi', 'kevat', 'kevat', 'syksy', 'syksy', 'syksy', 'talvi']);
});

test('hash round trip and fallbacks', () => {
  for (const s of [{}, { level: '7-9' }, { level: '7-9', season: 'talvi' }, { level: '7-9', season: 'talvi', topic: 2 }]) {
    assert.deepEqual(parseHash(hashFor(s), plan), s);
  }
  assert.deepEqual(parseHash('#x/y', plan), {});
  assert.deepEqual(parseHash('#1-3/joulu/0', plan), { level: '1-3' });
  assert.deepEqual(parseHash('#1-3/syksy/99', plan), { level: '1-3', season: 'syksy' });
});
