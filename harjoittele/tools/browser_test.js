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

async function pageWithGuards(browser, origin) {
  const page = await browser.newPage({ viewport: { width: 360, height: 800 } });
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

try {
  // Pupil view: all current items are drafts, so the page says so.
  {
    const { page, problems } = await pageWithGuards(browser, origin);
    await page.goto(`${origin}/harjoittele/`);
    await page.waitForSelector('#app a[href="?luonnokset=1"]');
    check((await page.textContent('#app')).includes('Tarkistettuja tehtäviä ei ole vielä'), 'pupil view: empty message missing');
    check(await page.isHidden('#draft-banner'), 'pupil view: draft banner visible');
    await commonChecks(page, 'pupil view');
    problems.forEach((p) => failures.push(`pupil view: ${p}`));
    await page.close();
  }

  // Draft preview: a full round.
  {
    const { page, problems } = await pageWithGuards(browser, origin);
    await page.goto(`${origin}/harjoittele/?luonnokset=1`);
    await page.waitForSelector('.stem');
    check(await page.isVisible('#draft-banner'), 'draft view: banner hidden');

    const byStem = await page.evaluate(async () => {
      const { loadItems } = await import('./js/items.js');
      const { items } = await loadItems(new URL('data/manifest.json', location.href).href, { includeDrafts: true });
      return Object.fromEntries(items.map((i) => [i.stem, { answer: i.answer.value, wrong: i.wrong }]));
    });
    const current = async () => byStem[await page.textContent('.stem')];
    const submit = async (text) => {
      await page.fill('#answer', text);
      await page.click('button[type=submit]');
    };

    // Item 1: unreadable, then a misconception answer, then another wrong one.
    let item = await current();
    await submit('kolme');
    check((await page.textContent('.feedback')).includes('En saanut vastauksesta selvää'), 'unreadable message missing');
    const mis = item.wrong[0];
    await submit(mis.match);
    const retryText = await page.textContent('.feedback');
    check(retryText.includes('Yritä vielä kerran') && retryText.includes(`Virhekäsitys: ${mis.misconception}`), `retry after ${mis.match} not shown: ${retryText}`);
    check(!retryText.includes('Tarkista laskusi'), 'draft misconception text not used');
    await submit('1');
    const reveal = await page.textContent('.feedback');
    check(reveal.includes(`Oikea vastaus: ${item.answer}`), `reveal missing: ${reveal}`);
    check(await page.isDisabled('#answer'), 'answer field not locked after reveal');
    await page.click('text=Seuraava');

    // Item 2: typed with the number pad.
    item = await current();
    for (const ch of item.answer) await page.click(`.pad .key:text-is("${ch}")`);
    check((await page.inputValue('#answer')) === item.answer, 'number pad input wrong');
    await page.click('.pad .key[aria-label="poista merkki"]');
    await page.click(`.pad .key:text-is("${item.answer.slice(-1)}")`);
    await page.click('button[type=submit]');
    check((await page.textContent('.feedback')).includes('Oikein!'), 'pad answer not accepted');
    await page.click('text=Seuraava');

    // Items 3-5: correct on the first try, submitted with Enter.
    for (let i = 3; i <= 5; i++) {
      item = await current();
      await page.fill('#answer', item.answer);
      await page.press('#answer', 'Enter');
      await page.click(i === 5 ? 'text=Katso tulos' : 'text=Seuraava');
    }
    const summary = await page.textContent('#app');
    check(summary.includes('Sait 4/5 oikein') && summary.includes('Ensimmäisellä yrityksellä 4/5'), `summary wrong: ${summary}`);
    await commonChecks(page, 'draft round');
    await page.click('text=Uusi kierros');
    check((await page.textContent('.progress')).includes('Tehtävä 1/5'), 'new round did not start');
    problems.forEach((p) => failures.push(`draft round: ${p}`));
    await page.close();
  }
} finally {
  await browser.close();
  server.close();
}

if (failures.length) {
  console.log('BROWSER TEST FAILED');
  failures.forEach((f) => console.log(`  - ${f}`));
  process.exit(1);
}
console.log('BROWSER TEST OK');
