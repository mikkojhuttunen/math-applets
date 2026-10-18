import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { editStatus, updateManifest, serializeManifest } from '../js/status_edit.js';
import { makeZip, readZip, crc32 } from '../js/zip.js';
import { buildManifest, serialize } from '../tools/build_manifest.js';

const FIXTURE_ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'repo');
const F79 = 'math-misconceptions/exercises/ALG-08/NE.json';
const F16 = 'math-misconceptions/grades1-6/exercises/grades1-6/batch-20260101-0000.json';

test('editStatus changes one item and nothing else', () => {
  const text = fs.readFileSync(path.join(FIXTURE_ROOT, F79), 'utf8');
  const r = editStatus(text, 'ALG-08-NE-001', '7-9');
  assert.strictEqual(r.result, 'changed');
  assert.strictEqual(r.from, 'draft');
  assert.strictEqual(text.length - r.text.length, 'draft'.length - 'approved'.length);
  assert.deepStrictEqual(JSON.parse(r.text).items.map((i) => i.status), ['approved', 'approved']);
  const again = editStatus(r.text, 'ALG-08-NE-001', '7-9');
  assert.strictEqual(again.result, 'already');
  assert.strictEqual(editStatus(text, 'ALG-08-NE-099', '7-9').result, 'missing');
});

test('editStatus on grades 1-6 stays inside the item', () => {
  const text = fs.readFileSync(path.join(FIXTURE_ROOT, F16), 'utf8');
  const r = editStatus(text, 'A36.S2.04-sub-20260930-1820-004', '1-6');
  assert.strictEqual(r.result, 'changed');
  assert.deepStrictEqual(JSON.parse(r.text).map((i) => i.status), ['draft', 'reviewed', 'reviewed']);
});

test('updateManifest equals what build_manifest writes after the same edits', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'manifest-'));
  fs.cpSync(FIXTURE_ROOT, root, { recursive: true });
  const before = buildManifest(root);
  const changes = [];
  for (const [rel, band, id] of [[F79, '7-9', 'ALG-08-NE-001'], [F16, '1-6', 'A36.S2.04-sub-20260930-1820-001'], [F16, '1-6', 'A36.S2.04-sub-20260930-1820-004']]) {
    const file = path.join(root, rel);
    const r = editStatus(fs.readFileSync(file, 'utf8'), id, band);
    fs.writeFileSync(file, r.text);
    changes.push({ path: `../${rel}`, from: r.from, to: band === '7-9' ? 'approved' : 'reviewed' });
  }
  assert.strictEqual(serializeManifest(updateManifest(before, changes)), serialize(buildManifest(root)));
  assert.notStrictEqual(serializeManifest(before), serialize(buildManifest(root)));
});

test('updateManifest drops a status that reaches zero and rejects unknown files', () => {
  const m = buildManifest(FIXTURE_ROOT);
  const next = updateManifest(m, [{ path: `../${F16}`, from: 'draft', to: 'reviewed' }, { path: `../${F16}`, from: 'draft', to: 'reviewed' }]);
  assert.deepStrictEqual(next.files.find((f) => f.path.endsWith('batch-20260101-0000.json')).by_status, { reviewed: 3 });
  assert.strictEqual(m.files[0].by_status.draft, 2);
  assert.throws(() => updateManifest(m, [{ path: '../nope.json', from: 'draft', to: 'approved' }]), /Not in manifest/);
});

test('zip: round trip with non-ASCII text, and a standard unzip reads it', async () => {
  const entries = [{ name: 'math-misconceptions/exercises/ALG-01/MC.json', text: '{"teksti": "Sievennä äö"}\n' }, { name: 'harjoittele/data/manifest.json', text: '{}\n' }];
  const zip = makeZip(entries);
  assert.deepStrictEqual(readZip(zip), entries);
  assert.strictEqual(crc32(new TextEncoder().encode('123456789')), 0xcbf43926);
  const corrupt = zip.slice();
  corrupt[30 + entries[0].name.length + 2] ^= 0xff;
  assert.throws(() => readZip(corrupt), /checksum|zip|central/);
  const file = path.join(os.tmpdir(), `zip-test-${process.pid}.zip`);
  fs.writeFileSync(file, zip);
  const { spawnSync } = await import('node:child_process');
  const r = spawnSync('unzip', ['-t', file], { encoding: 'utf8' });
  if (!r.error) assert.strictEqual(r.status, 0, r.stdout + r.stderr);
  fs.rmSync(file, { force: true });
});
