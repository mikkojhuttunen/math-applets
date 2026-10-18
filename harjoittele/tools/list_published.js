// Prints the ids of all items that are already published in the repo
// (grades 7-9: "approved", grades 1-6: "reviewed"), one per line.
// Paste the output into the box "Päivitä julkaistut listasta" on the
// review page (Tehtäväpankin tarkistus).
//
//   node harjoittele/tools/list_published.js

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..', '..');
const BANK = path.join(REPO, 'math-misconceptions');
const DONE = new Set(['approved', 'reviewed']);
const ids = [];

const dir79 = path.join(BANK, 'exercises');
if (fs.existsSync(dir79)) {
  for (const topic of fs.readdirSync(dir79)) {
    const tdir = path.join(dir79, topic);
    if (!fs.statSync(tdir).isDirectory()) continue;
    for (const f of fs.readdirSync(tdir).filter((n) => n.endsWith('.json'))) {
      const data = JSON.parse(fs.readFileSync(path.join(tdir, f), 'utf8'));
      for (const it of data.items || []) if (DONE.has(it.status)) ids.push(it.id);
    }
  }
}
const dir16 = path.join(BANK, 'grades1-6', 'exercises', 'grades1-6');
if (fs.existsSync(dir16)) {
  for (const f of fs.readdirSync(dir16).filter((n) => /^batch-.*\.json$/.test(n))) {
    for (const it of JSON.parse(fs.readFileSync(path.join(dir16, f), 'utf8'))) if (DONE.has(it.status)) ids.push(it.id);
  }
}
console.log(ids.join('\n'));
