// Marks exercise items as approved or reviewed.
// Reads item ids from a text file (any layout, for example the list made by
// the merge tab of tarkista.html, or the text copied with "Kopioi
// tunnisteet" in opettaja.html) and changes "status": "draft" in the
// matching exercise file:
//
//   grades 7-9 ids (ALG-01-MC-001)  ->  "approved"  in math-misconceptions/exercises
//   grades 1-6 ids (A36.S2.04-...)  ->  "reviewed"  in math-misconceptions/grades1-6/exercises/grades1-6
//
//   node tools/set_status.js ids.txt --dry   show what would change
//   node tools/set_status.js ids.txt         write the changes
//
// Grades 1-6 items also need the expert sign-off described in
// EXPERT_REVIEW_REQUIRED.md before pupils use them. Feedback texts
// (data/misconceptions_fi.json) are edited by hand, see README.md.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { editStatus } from '../js/status_edit.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..', '..');
const EXERCISES_7_9 = path.join(REPO, 'math-misconceptions', 'exercises');
const BATCHES_1_6 = path.join(REPO, 'math-misconceptions', 'grades1-6', 'exercises', 'grades1-6');
const ID_7_9 = /\b([A-Z]{2,3}-\d{2})-([A-Z]{2})-(\d{3})\b/g;
const ID_1_6_LIKE = /\b[A-Z]\d\d\.[A-Z]\d\.\d\d-[A-Za-z0-9-]+/g;

const args = process.argv.slice(2);
const dry = args.includes('--dry');
const idFile = args.find((a) => !a.startsWith('--'));
if (!idFile) {
  console.error('Usage: node tools/set_status.js <idfile> [--dry]');
  process.exit(2);
}
const text = fs.readFileSync(idFile, 'utf8');

let changed = 0;
let already = 0;
const missing = [];
const edits = new Map(); // file -> text being edited

function edit(file, id, band) {
  if (!edits.has(file)) edits.set(file, fs.readFileSync(file, 'utf8'));
  const r = editStatus(edits.get(file), id, band);
  if (r.result === 'missing') return missing.push(id);
  if (r.result === 'already') return already++;
  edits.set(file, r.text);
  changed++;
}

// Grades 7-9: one file per topic and type, status right after the id.
const wanted = new Map();
for (const m of text.matchAll(ID_7_9)) {
  const file = path.join(EXERCISES_7_9, m[1], `${m[2]}.json`);
  if (!wanted.has(file)) wanted.set(file, new Set());
  wanted.get(file).add(m[0]);
}
for (const [file, ids] of [...wanted].sort()) {
  for (const id of ids) {
    if (!fs.existsSync(file)) { missing.push(id); continue; }
    edit(file, id, '7-9');
  }
}

// Grades 1-6: batch files, status somewhere after the id inside the same item.
const known16 = new Map();
if (fs.existsSync(BATCHES_1_6)) {
  for (const f of fs.readdirSync(BATCHES_1_6).filter((n) => /^batch-.*\.json$/.test(n))) {
    const file = path.join(BATCHES_1_6, f);
    for (const item of JSON.parse(fs.readFileSync(file, 'utf8'))) known16.set(item.id, file);
  }
}
const tokens = new Set(text.split(/[\s,;]+/).filter(Boolean));
for (const id of tokens) {
  const file = known16.get(id);
  if (file) edit(file, id, '1-6');
}
for (const m of text.matchAll(ID_1_6_LIKE)) if (!known16.has(m[0])) missing.push(m[0]);

if (!dry) for (const [file, content] of edits) fs.writeFileSync(file, content);

console.log(`${dry ? 'Would change' : 'Changed'} ${changed} item(s); ${already} already done.`);
if (missing.length) {
  console.log(`Not found (${missing.length}): ${[...new Set(missing)].join(', ')}`);
  process.exit(1);
}
