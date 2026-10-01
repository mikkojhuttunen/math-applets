// Browser test of the practice page with Playwright (Chromium).
//   NODE_PATH=$(npm root -g) node tools/browser_test.js
// Serves the repo root itself, so no other server is needed. Not part of
// `npm test`, because Playwright is not a dependency of this folder.

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  console.log('SKIP: playwright not found (set NODE_PATH=$(npm root -g))');
  process.exit(0);
}

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };

function serve() {
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]);
    let p = path.join(REPO, rel);
    if (!p.startsWith(REPO)) return res.writeHead(403).end();
    if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
    if (!fs.existsSync(p)) return res.writeHead(404).end();
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise((r) => server.listen(0, '127.0.0.1', () => r(server)));
}

const failures = [];
function check(cond, message) {
  if (!cond) failures.push(message);
}

async function pageWithGuards(context, origin) {
  const page = await context.newPage();
  await page.setViewportSize({ width: 360, height: 800 });
  const problems = [];
  page.on('console', (m) => m.type() === 'error' && problems.push(`console: ${m.text()}`));
  page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`));
  page.on('request', (r) => !r.url().startsWith(origin) && problems.push(`foreign request: ${r.url()}`));
  return { page, problems };
}

async function commonChecks(page, label) {
  const text = await page.evaluate(() => document.body.innerText);
  check(!/NaN|undefined/.test(text), `${label}: NaN or undefined on screen`);
  const width = await page.evaluate(() => document.documentElement.scrollWidth);
  check(width <= 360, `${label}: horizontal scroll (${width}px)`);
  check((await page.getAttribute('html', 'lang')) === 'fi', `${label}: lang is not fi`);
}

const server = await serve();
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
const context = await browser.newContext({ permissions: ['clipboard-read', 'clipboard-write'] });

try {
  // Pupil view: all current items are drafts, so the page says so.
  {
    const { page, problems } = await pageWithGuards(context, origin);
    await page.goto(`${origin}/harjoittele/`);
    await page.waitForSelector('#app a[href="?luonnokset=1"]');
    check((await page.textContent('#app')).includes('Tarkistettuja tehtäviä ei ole vielä'), 'pupil view: empty message missing');
    check(await page.isHidden('#draft-banner'), 'pupil view: draft banner visible');
    await commonChecks(page, 'pupil view');
    problems.forEach((p) => failures.push(`pupil view: ${p}`));
    await page.close();
  }

  // Data the test needs, read the same way the pages read it.
  let data;
  {
    const page = await browser.newPage();
    await page.goto(`${origin}/harjoittele/`);
    data = await page.evaluate(async () => {
      const { loadItems } = await import('./js/items.js');
      const { answerText } = await import('./js/round.js');
      const { items } = await loadItems(new URL('data/manifest.json', location.href).href, { includeDrafts: true });
      return items.map((i) => ({ id: i.id, kind: i.kind, stem: i.stem, answer: answerText(i), wrong: i.wrong || [], options: i.options || [] }));
    });
    await page.close();
  }
  const byStem = Object.fromEntries(data.map((i) => [i.stem, i]));
  const entry = data.find((i) => i.kind === 'entry' && i.wrong.length && /^\d+$/.test(i.answer));
  const choice = data.find((i) => i.kind === 'choice' && i.options.some((o) => !o.correct && o.misconception));

  // One typed item: unreadable, misconception answer, another wrong answer, reveal.
  if (entry) {
    const { page, problems } = await pageWithGuards(context, origin);
    await page.goto(`${origin}/harjoittele/?luonnokset=1&tehtava=${encodeURIComponent(entry.id)}`);
    await page.waitForSelector('.stem');
    check(await page.isVisible('#draft-banner'), 'draft view: banner hidden');
    const submit = async (text) => {
      await page.fill('#answer', text);
      await page.click('button[type=submit]');
    };
    await submit('kolme');
    check((await page.textContent('.feedback')).includes('En saanut vastauksesta selvää'), 'unreadable message missing');
    const mis = entry.wrong[0];
    await submit(mis.match);
    const retryText = await page.textContent('.feedback');
    check(retryText.includes('Yritä vielä kerran') && retryText.includes(`Virhekäsitys: ${mis.misconception}`), `retry after ${mis.match} not shown: ${retryText}`);
    check(!retryText.includes('Tarkista laskusi'), 'draft misconception text not used');
    await submit('1');
    const reveal = await page.textContent('.feedback');
    check(reveal.includes(`Oikea vastaus: ${entry.answer}`), `reveal missing: ${reveal}`);
    check(await page.isDisabled('#answer'), 'answer field not locked after reveal');
    await page.click('text=Katso tulos');
    check((await page.textContent('#app')).includes('Sait 0/1 oikein'), 'single-item summary wrong');
    await commonChecks(page, 'typed item');
    problems.forEach((p) => failures.push(`typed item: ${p}`));
    await page.close();
  } else failures.push('no typed item with stored wrong answers to test');

  // One choice item: wrong option is disabled and explained, right one accepted.
  if (choice) {
    const { page, problems } = await pageWithGuards(context, origin);
    await page.goto(`${origin}/harjoittele/?luonnokset=1&tehtava=${encodeURIComponent(choice.id)}`);
    await page.waitForSelector('.option');
    const wrongOpt = choice.options.find((o) => !o.correct && o.misconception);
    const wrongBtn = page.locator('.option', { has: page.locator(`.option-text:text-is("${wrongOpt.text}")`) });
    await wrongBtn.click();
    check(await wrongBtn.isDisabled(), 'wrong option not disabled');
    check((await page.textContent('.feedback')).includes(`Virhekäsitys: ${wrongOpt.misconception}`), 'choice misconception not shown');
    // The right option by its letter key.
    const rightBtn = page.locator('.option', { has: page.locator(`.option-text:text-is("${choice.answer}")`) });
    const letter = await rightBtn.getAttribute('data-letter');
    await page.keyboard.press(letter.toLowerCase());
    check((await page.textContent('.feedback')).includes('Oikein!'), 'right option not accepted by its letter key');
    problems.forEach((p) => failures.push(`choice item: ${p}`));
    await page.close();
  }

  // A full random round, all correct; the first typed item goes in with the pad.
  {
    const { page, problems } = await pageWithGuards(context, origin);
    await page.goto(`${origin}/harjoittele/?luonnokset=1`);
    let padUsed = false;
    for (let n = 1; n <= 5; n++) {
      await page.waitForSelector('.stem');
      const item = byStem[await page.textContent('.stem')];
      if (item.kind === 'choice') {
        await page.locator('.option', { has: page.locator(`.option-text:text-is("${item.answer}")`) }).click();
      } else if (!padUsed && /^[\d/,−\s]+$/.test(item.answer)) {
        const keys = [...item.answer].map((ch) => (ch === ' ' ? 'väli' : ch));
        for (const k of keys) await page.click(`.pad .key:text-is("${k}")`);
        await page.click('.pad .key[aria-label="poista merkki"]');
        await page.click(`.pad .key:text-is("${keys[keys.length - 1]}")`);
        check((await page.inputValue('#answer')) === item.answer, 'number pad input wrong');
        await page.press('#answer', 'Enter');
        padUsed = true;
      } else {
        await page.fill('#answer', item.answer);
        await page.press('#answer', 'Enter');
      }
      check((await page.textContent('.feedback')).includes('Oikein'), `item ${item.id} not accepted with ${item.answer}`);
      await page.click(n === 5 ? 'text=Katso tulos' : 'text=Seuraava');
    }
    const summary = await page.textContent('#app');
    check(summary.includes('Sait 5/5 oikein') && summary.includes('Ensimmäisellä yrityksellä 5/5'), `summary wrong: ${summary}`);
    await commonChecks(page, 'full round');
    await page.click('text=Uusi kierros');
    check((await page.textContent('.progress')).includes('Tehtävä 1/5'), 'new round did not start');
    problems.forEach((p) => failures.push(`full round: ${p}`));
    await page.close();
  }

  // Teacher view: counts, filters, selection, copy list, feedback tab, print sheet.
  {
    const { page, problems } = await pageWithGuards(context, origin);
    await page.goto(`${origin}/harjoittele/opettaja.html`);
    await page.waitForSelector('#item-list .item');
    const count = await page.textContent('#item-count');
    check(count.includes(`/ ${data.length} tehtävää`), `teacher count wrong: ${count}`);
    await page.selectOption('select[name=band]', '1-6');
    await page.fill('input[name=query]', entry.id);
    await page.waitForFunction(() => document.querySelectorAll('#item-list .item').length === 1);
    const card = await page.textContent('#item-list .item');
    check(card.includes(`Oikea vastaus: ${entry.answer}`) && card.includes(entry.wrong[0].match), 'item card missing answer or wrong answers');
    check(card.includes('luonnos'), 'draft feedback badge missing');
    await page.check('#item-list .item input[type=checkbox]');
    check((await page.textContent('#selection-count')).includes('1 tehtävää'), 'selection not counted');
    await page.click('#copy-ids');
    const copied = await page.evaluate(() => navigator.clipboard.readText().catch(() => document.getElementById('copy-fallback').value));
    check(copied.includes(entry.id) && copied.includes('"reviewed"'), `copied ids wrong: ${copied}`);
    await page.reload();
    await page.waitForSelector('#item-list .item');
    check((await page.textContent('#selection-count')).includes('1 tehtävää'), 'selection not kept after reload');
    await page.click('#clear-selection');
    check(await page.isHidden('#selection-bar'), 'selection not cleared');
    await page.click('#tab-texts');
    const texts = await page.textContent('#text-list');
    check(texts.includes('NUM-10a') && texts.includes('Oppilaalle'), 'feedback tab empty');
    await page.click('#tab-items');
    await page.evaluate(() => (window.print = () => {}));
    await page.click('#print-sheet');
    const sheet = await page.textContent('#print');
    check(sheet.includes('Harjoitus') && sheet.includes('Vastaukset'), 'print sheet not built');
    await commonChecks(page, 'teacher view');
    problems.forEach((p) => failures.push(`teacher view: ${p}`));
    await page.close();
  }
} finally {
  await context.close();
  await browser.close();
  server.close();
}

if (failures.length) {
  console.log('BROWSER TEST FAILED');
  failures.forEach((f) => console.log(`  - ${f}`));
  process.exit(1);
}
console.log('BROWSER TEST OK');
