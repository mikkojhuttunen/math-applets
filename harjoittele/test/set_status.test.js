import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { SITE_DIR } from './helpers.js';

// Builds a tiny repo in a temp folder: the script under test, one grades
// 7-9 topic file and one grades 1-6 batch file.
function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'set-status-'));
  const tools = path.join(root, 'harjoittele', 'tools');
  fs.mkdirSync(tools, { recursive: true });
  fs.mkdirSync(path.join(root, 'harjoittele', 'js'), { recursive: true });
  fs.copyFileSync(path.join(SITE_DIR, 'tools', 'set_status.js'), path.join(tools, 'set_status.js'));
  fs.copyFileSync(path.join(SITE_DIR, 'js', 'status_edit.js'), path.join(root, 'harjoittele', 'js', 'status_edit.js'));
  fs.writeFileSync(path.join(root, 'harjoittele', 'package.json'), '{"type":"module"}');
  const topic = path.join(root, 'math-misconceptions', 'exercises', 'ALG-01');
  fs.mkdirSync(topic, { recursive: true });
  const item = (id) => ({ schema_version: '1.0', id, type: 'MC', status: 'draft', lang: 'fi' });
  const topicFile = path.join(topic, 'MC.json');
  fs.writeFileSync(topicFile, JSON.stringify({ topic: 'ALG-01', items: [item('ALG-01-MC-001'), item('ALG-01-MC-002')] }, null, 2) + '\n');
  const batches = path.join(root, 'math-misconceptions', 'grades1-6', 'exercises', 'grades1-6');
  fs.mkdirSync(batches, { recursive: true });
  const small = (id) => ({ id, goal: 'A36.S2.04', type: 'numeric_entry', stem_fi: 'Laske.', answer: '1', source: 'template', status: 'draft' });
  const batchFile = path.join(batches, 'batch-20260930-1653.json');
  fs.writeFileSync(batchFile, JSON.stringify([small('A36.S2.04-sub-20260930-1653-001'), small('A36.S2.04-sub-20260930-1653-002')], null, 2) + '\n');
  return { root, topicFile, batchFile };
}

function run(root, ids, ...flags) {
  const idFile = path.join(root, 'ids.txt');
  fs.writeFileSync(idFile, ids);
  const r = spawnSync(process.execPath, [path.join(root, 'harjoittele', 'tools', 'set_status.js'), idFile, ...flags], { encoding: 'utf8' });
  return { code: r.status, out: r.stdout + r.stderr };
}

const statuses = (file) => {
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  return (data.items || data).map((i) => i.status);
};

test('approves 7-9 items and reviews 1-6 items, leaving the others as drafts', () => {
  const f = fixture();
  const r = run(f.root, 'Hyväksyttävät, 2 kpl\n\nALG-01-MC-002\nA36.S2.04-sub-20260930-1653-001\n');
  assert.strictEqual(r.code, 0, r.out);
  assert.deepStrictEqual(statuses(f.topicFile), ['draft', 'approved']);
  assert.deepStrictEqual(statuses(f.batchFile), ['reviewed', 'draft']);
  assert.match(r.out, /Changed 2 item/);
});

test('dry run changes nothing; a second run reports them as already done', () => {
  const f = fixture();
  const ids = 'ALG-01-MC-001\nA36.S2.04-sub-20260930-1653-002\n';
  assert.strictEqual(run(f.root, ids, '--dry').code, 0);
  assert.deepStrictEqual(statuses(f.topicFile), ['draft', 'draft']);
  run(f.root, ids);
  const again = run(f.root, ids);
  assert.match(again.out, /Changed 0 item\(s\); 2 already done/);
});

test('unknown ids are reported and the exit code is 1, known ids are still written', () => {
  const f = fixture();
  const r = run(f.root, 'ALG-01-MC-001\nALG-09-MC-001\nA36.S2.04-sub-20260930-1653-099\n');
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /Not found \(2\)/);
  assert.deepStrictEqual(statuses(f.topicFile), ['approved', 'draft']);
});
