import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildManifest, serialize, MANIFEST_PATH } from '../tools/build_manifest.js';

const FIXTURE_ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'repo');

test('manifest lists both formats with counts', () => {
  const m = buildManifest(FIXTURE_ROOT);
  assert.deepStrictEqual(
    m.files.map((f) => [f.path, f.format, f.items]),
    [
      ['../math-misconceptions/grades1-6/exercises/grades1-6/batch-20260101-0000.json', 'grades1-6', 3],
      ['../math-misconceptions/exercises/ALG-08/NE.json', 'grades7-9', 2],
    ]
  );
  assert.strictEqual(m.totals.items, 5);
  assert.deepStrictEqual(m.totals.by_status, { approved: 1, draft: 3, reviewed: 1 });
  assert.deepStrictEqual(m.totals.by_goal, { 'A36.S2.04': 3, 'S3.02': 2 });
  assert.deepStrictEqual(m.totals.by_misconception, { 'ALG-08': 2, 'NUM-10': 3 });
});

test('a missing source folder gives an empty manifest, not an error', () => {
  const m = buildManifest(path.join(FIXTURE_ROOT, 'does-not-exist'));
  assert.deepStrictEqual(m.files, []);
  assert.strictEqual(m.totals.items, 0);
});

test('every listed file exists relative to harjoittele/', () => {
  const m = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  for (const f of m.files) {
    assert.ok(fs.existsSync(path.join(path.dirname(MANIFEST_PATH), '..', f.path)), f.path);
  }
});

test('data/manifest.json is up to date with the repo (run: node tools/build_manifest.js)', () => {
  assert.strictEqual(fs.readFileSync(MANIFEST_PATH, 'utf8'), serialize(buildManifest()));
});
