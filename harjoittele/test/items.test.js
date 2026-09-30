import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { normalize1to6, normalize7to9, loadItems } from '../js/items.js';
import { buildManifest, serialize } from '../tools/build_manifest.js';
import { SITE_DIR, TEST_DIR, fileFetch, fileUrl } from './helpers.js';

const FIXTURE_REPO = path.join(TEST_DIR, 'fixtures', 'repo');

// A manifest for the fixture repo, written where loadItems expects it
// (<repo>/harjoittele/data/manifest.json), in a temporary copy.
function fixtureManifestUrl() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'harjoittele-'));
  fs.cpSync(FIXTURE_REPO, tmp, { recursive: true });
  const dataDir = path.join(tmp, 'harjoittele', 'data');
  fs.mkdirSync(dataDir, { recursive: true });
  fs.writeFileSync(path.join(dataDir, 'manifest.json'), serialize(buildManifest(tmp)));
  return { url: fileUrl(path.join(dataDir, 'manifest.json')), tmp };
}

test('1-6 numeric entry keeps the answer as typed and lists misconception answers', () => {
  const item = normalize1to6({
    id: 'x-1', goal: 'A36.S2.04', level: 'T', type: 'numeric_entry', stem_fi: 'Laske 916 − 140.',
    answer: '776', workbook: ['NUM-10'], status: 'draft',
    misconceptions: { 'NUM-10a': { answer: '836' } },
  });
  assert.strictEqual(item.kind, 'entry');
  assert.deepStrictEqual(item.answer, { kind: 'typed', value: '776' });
  assert.deepStrictEqual(item.wrong, [{ match: '836', misconception: 'NUM-10a', feedback: null }]);
  assert.strictEqual(item.pupilReady, false);
  assert.deepStrictEqual(item.goals, ['A36.S2.04']);
});

test('1-6 choice marks the correct option and misconception options', () => {
  const item = normalize1to6({
    id: 'x-2', type: 'choice', stem_fi: 'Kumpi?', answer: '5', options: ['5', '15', '7'],
    misconceptions: { 'NUM-10a': { answer: '15' } }, status: 'reviewed',
  });
  assert.strictEqual(item.kind, 'choice');
  assert.deepStrictEqual(item.options.map((o) => [o.id, o.correct, o.misconception]), [
    ['a', true, null], ['b', false, 'NUM-10a'], ['c', false, null],
  ]);
  assert.strictEqual(item.pupilReady, true);
  assert.ok(normalize1to6({ id: 'x-3', type: 'choice', stem_fi: 'K', answer: '9', options: ['1', '2'] }).skip);
});

test('7-9 items: NE and MC load, figures and other types are skipped', () => {
  const ne = normalize7to9({
    id: 'N-1', type: 'NE', status: 'approved', curriculum: { ops: ['S3.02'], grade: 7, level: 'T' },
    misconceptions: ['ALG-08'], prompt: { text: 'Avaa sulut' },
    payload: { answer: { kind: 'number', value: 3 }, wrong: [{ match: 4, misconception: 'ALG-08', feedback: 'F' }] },
    feedback: { correct: 'Oikein' }, solution: { steps: ['a'], final: 'b' },
  });
  assert.strictEqual(ne.kind, 'entry');
  assert.deepStrictEqual(ne.wrong, [{ match: '4', misconception: 'ALG-08', feedback: 'F' }]);
  assert.strictEqual(ne.grade, 7);
  const mc = normalize7to9({
    id: 'M-1', type: 'MC', prompt: { text: 'Valitse' }, payload: {
      options: [
        { id: 'a', text: '1', misconception: null, feedback: '' },
        { id: 'b', text: '2', misconception: 'NUM-03', feedback: 'Ei' },
      ], correct: ['a'] },
  });
  assert.strictEqual(mc.kind, 'choice');
  assert.strictEqual(mc.options[1].misconception, 'NUM-03');
  assert.strictEqual(normalize7to9({ id: 'F', type: 'NE', prompt: { text: 't', figure: { src: 'x' } } }).skip, 'needs a figure');
  assert.match(normalize7to9({ id: 'E', type: 'ES', prompt: { text: 't' } }).skip, /not supported/);
});

test('loadItems serves only reviewed items to pupils, all items with includeDrafts', async () => {
  const { url, tmp } = fixtureManifestUrl();
  try {
    const pupil = await loadItems(url, { fetchImpl: fileFetch });
    assert.deepStrictEqual(pupil.errors, []);
    assert.strictEqual(pupil.items.length, 2);
    assert.ok(pupil.items.every((i) => i.pupilReady));
    assert.strictEqual(pupil.skipped.filter((s) => s.reason === 'not reviewed').length, 3);

    const teacher = await loadItems(url, { fetchImpl: fileFetch, includeDrafts: true });
    assert.strictEqual(teacher.items.length, 5);
    assert.deepStrictEqual(teacher.items.map((i) => i.gradeBand), ['1-6', '1-6', '1-6', '7-9', '7-9']);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test('a missing file is reported, the others still load', async () => {
  const { url, tmp } = fixtureManifestUrl();
  try {
    fs.rmSync(path.join(tmp, 'math-misconceptions', 'exercises', 'ALG-08', 'NE.json'));
    const r = await loadItems(url, { fetchImpl: fileFetch, includeDrafts: true });
    assert.strictEqual(r.errors.length, 1);
    assert.strictEqual(r.items.length, 3);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test('every item in the real repo loads or is skipped with a reason', async () => {
  const r = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  const manifest = JSON.parse(fs.readFileSync(path.join(SITE_DIR, 'data', 'manifest.json'), 'utf8'));
  assert.deepStrictEqual(r.errors, []);
  assert.strictEqual(r.items.length + r.skipped.length, manifest.totals.items);
  assert.ok(r.skipped.every((s) => s.reason));
});
