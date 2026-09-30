import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { feedbackFor, parentId, loadMisconceptions } from '../js/misconceptions.js';
import { loadItems } from '../js/items.js';
import { SITE_DIR, fileFetch, fileUrl } from './helpers.js';

const REPO = path.resolve(SITE_DIR, '..');
const FI_PATH = path.join(SITE_DIR, 'data', 'misconceptions_fi.json');
const fi = JSON.parse(fs.readFileSync(FI_PATH, 'utf8')).misconceptions;
const source = JSON.parse(fs.readFileSync(path.join(SITE_DIR, 'data', 'misconceptions_source.json'), 'utf8')).misconceptions;

test('Finnish texts cover exactly the ids of the source catalogue', () => {
  assert.deepStrictEqual(Object.keys(fi).sort(), source.map((s) => s.id).sort());
});

test('every entry is complete, short enough and in Finnish number format', () => {
  for (const [id, e] of Object.entries(fi)) {
    for (const k of ['name_fi', 'pupil', 'teacher']) {
      assert.ok(typeof e[k] === 'string' && e[k].trim().length > 0, `${id} ${k}`);
      assert.doesNotMatch(e[k], /\d\.\d/, `${id} ${k}: decimal point`);
      assert.doesNotMatch(e[k], /(^|[\s(=])-(\s|\d|\()/, `${id} ${k}: hyphen used as minus`);
      assert.doesNotMatch(e[k], /NaN|undefined/, `${id} ${k}`);
    }
    assert.ok(e.pupil.length <= 220, `${id} pupil text is ${e.pupil.length} characters`);
    assert.ok(e.teacher.length <= 320, `${id} teacher text is ${e.teacher.length} characters`);
    assert.ok(['draft', 'reviewed'].includes(e.status), `${id} status`);
    for (const a of e.applets || []) assert.ok(fs.existsSync(path.join(REPO, a)), `${id} applet ${a}`);
  }
});

test('every misconception used by the exercise banks has a text', async () => {
  const { items } = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  const used = new Set();
  for (const item of items) {
    item.misconceptions.forEach((m) => used.add(m));
    (item.wrong || []).forEach((w) => w.misconception && used.add(w.misconception));
    (item.options || []).forEach((o) => o.misconception && used.add(o.misconception));
  }
  assert.ok(used.size > 0);
  for (const id of used) assert.ok(feedbackFor(fi, id, { includeDrafts: true }), `no text for ${id}`);
});

test('feedbackFor: drafts only with includeDrafts, sub-variants fall back to the parent', () => {
  const texts = {
    'NUM-10': { name_fi: 'N', pupil: 'P', teacher: 'T', status: 'reviewed' },
    'NUM-10a': { name_fi: 'Na', pupil: 'Pa', teacher: 'Ta', status: 'draft' },
  };
  assert.strictEqual(parentId('NUM-10a'), 'NUM-10');
  assert.strictEqual(parentId('NUM-10'), null);
  assert.strictEqual(feedbackFor(texts, 'NUM-10a'), null);
  assert.strictEqual(feedbackFor(texts, 'NUM-10a', { includeDrafts: true }).pupil, 'Pa');
  assert.strictEqual(feedbackFor(texts, 'NUM-10b').pupil, 'P');
  assert.strictEqual(feedbackFor(texts, 'NUM-99'), null);
  assert.strictEqual(feedbackFor(texts, null), null);
});

test('loadMisconceptions reads the data file', async () => {
  const texts = await loadMisconceptions(fileUrl(FI_PATH), { fetchImpl: fileFetch });
  assert.strictEqual(Object.keys(texts).length, source.length);
});

test('misconceptions_source.json is up to date (run: python3 tools/extract_misconceptions.py)', (t) => {
  const r = spawnSync('python3', [path.join(SITE_DIR, 'tools', 'extract_misconceptions.py'), '--check'], { encoding: 'utf8' });
  if (r.error) return t.skip('python3 not available');
  assert.strictEqual(r.status, 0, r.stdout + r.stderr);
});
