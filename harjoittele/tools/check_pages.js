// Page check for the practice pages, with Playwright (Chromium).
//   NODE_PATH=$(npm root -g) node tools/check_pages.js             check the pages
//   NODE_PATH=$(npm root -g) node tools/check_pages.js --self-test fixture must fail every rule
//
// Rules, at 360 px width: no console errors or page errors, no requests to
// other origins, lang="fi", no horizontal scrolling, and in the visible
// text no NaN / undefined, no decimal point between digits and no
// hyphen-minus used as a minus sign (Finnish format: 3,5 and −4).
// Curriculum ids such as A36.S2.04 and file names are ignored.
// Serves the repository root itself. Exit code 1 on any problem.

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png' };

// Pages to check, relative to the site root. `prepare` brings the page
// into a state worth checking.
export const PAGES = [
  { url: 'index.html' },
  { url: 'harjoittele/' },
  { url: 'harjoittele/?luonnokset=1' },
  {
    url: 'harjoittele/?luonnokset=1',
    label: 'round in progress',
    prepare: async (page) => {
      await page.click('text=Kaikki aiheet sekaisin');
      await page.waitForSelector('.stem');
    },
  },
  { url: 'harjoittele/?tavoite=X9.99' },
  { url: 'harjoittele/opettaja.html', wait: '#item-list .item' },
  {
    url: 'harjoittele/opettaja.html',
    label: 'feedback texts tab',
    prepare: async (page) => {
      await page.waitForSelector('#item-list .item');
      await page.click('#tab-texts');
      await page.uncheck('input[name=used]');
    },
  },
  { url: 'harjoittele/tavoitteet.html', wait: '.goal' },
];

export function serve(root = REPO) {
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]);
    let p = path.join(root, rel);
    if (!p.startsWith(root)) return res.writeHead(403).end();
    if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
    if (!fs.existsSync(p)) return res.writeHead(404).end();
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise((r) => server.listen(0, '127.0.0.1', () => r(server)));
}

// Visible-text rules. Exported for unit tests.
export function textProblems(text) {
  const problems = [];
  const cleaned = text
    .replace(/\s+/g, ' ')
    .replace(/\S*\bS\d\.\d{2}\S*/g, ' ') // curriculum ids and item ids
    .replace(/\S+\.(?:html|json|md|js|css)\b/g, ' ') // file names
    .replace(/https?:\/\/\S+/g, ' ');
  if (/\bNaN\b/.test(cleaned)) problems.push('NaN on screen');
  if (/\bundefined\b/.test(cleaned)) problems.push('undefined on screen');
  const dot = /\d\.\d/.exec(cleaned);
  if (dot) problems.push(`decimal point: …${cleaned.slice(Math.max(0, dot.index - 15), dot.index + 15).trim()}…`);
  const minus = /(^|[\s(=])-\d/.exec(cleaned);
  if (minus) problems.push(`hyphen-minus as minus: …${cleaned.slice(Math.max(0, minus.index - 10), minus.index + 12).trim()}…`);
  return problems;
}

export async function checkPage(context, origin, spec) {
  const page = await context.newPage();
  await page.setViewportSize({ width: 360, height: 800 });
  const problems = [];
  page.on('console', (m) => m.type() === 'error' && problems.push(`console error: ${m.text()}`));
  page.on('pageerror', (e) => problems.push(`page error: ${e.message}`));
  page.on('request', (r) => {
    if (!r.url().startsWith(origin) && !r.url().startsWith('data:')) problems.push(`request to another site: ${r.url()}`);
  });
  await page.route((url) => !url.href.startsWith(origin), (route) => route.abort());
  try {
    await page.goto(`${origin}/${spec.url}`);
    if (spec.wait) await page.waitForSelector(spec.wait);
    if (spec.prepare) await spec.prepare(page);
    await page.waitForLoadState('networkidle');
    if ((await page.getAttribute('html', 'lang')) !== 'fi') problems.push('html lang is not "fi"');
    const width = await page.evaluate(() => document.documentElement.scrollWidth);
    if (width > 360) problems.push(`horizontal scrolling: page is ${width}px wide at 360px`);
    problems.push(...textProblems(await page.evaluate(() => document.body.innerText)));
  } catch (e) {
    problems.push(`check failed: ${e.message.split('\n')[0]}`);
  }
  // A console error about the aborted foreign request repeats the request problem.
  const unique = [...new Set(problems.filter((p) => !/console error: Failed to load resource/.test(p)))];
  await page.close();
  return unique;
}

// The front page must link to the practice pages, and the link must work.
async function checkFrontPageLink(context, origin) {
  const page = await context.newPage();
  await page.goto(`${origin}/index.html`);
  const href = await page.getAttribute('a[href^="harjoittele"]', 'href').catch(() => null);
  const problems = [];
  if (!href) problems.push('front page has no link to harjoittele/');
  else {
    const res = await page.goto(new URL(href, `${origin}/index.html`).href);
    if (!res || !res.ok()) problems.push(`front page link ${href} does not open`);
  }
  await page.close();
  return problems;
}

async function main(argv) {
  let chromium;
  try {
    ({ chromium } = require('playwright'));
  } catch {
    console.log('SKIP: playwright not found (set NODE_PATH=$(npm root -g) or npm install playwright)');
    process.exit(0);
  }
  const selfTest = argv.includes('--self-test');
  const server = await serve();
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const context = await browser.newContext();
  let failed = 0;
  try {
    if (selfTest) {
      const problems = await checkPage(context, origin, { url: 'harjoittele/test/fixtures/pages/broken.html' });
      const expected = ['console error', 'request to another site', 'lang', 'horizontal scrolling', 'NaN', 'undefined', 'decimal point', 'hyphen-minus'];
      const missing = expected.filter((e) => !problems.some((p) => p.includes(e)));
      const idFlagged = problems.some((p) => p.includes('A36'));
      problems.forEach((p) => console.log(`  found: ${p}`));
      if (missing.length || idFlagged) {
        console.log(`SELF-TEST FAILED: rules that did not fire: ${missing.join(', ') || '-'}${idFlagged ? '; a curriculum id was flagged' : ''}`);
        failed = 1;
      } else console.log('SELF-TEST OK: every rule fired on the broken fixture');
    } else {
      for (const spec of PAGES) {
        const problems = await checkPage(context, origin, spec);
        const name = spec.label ? `${spec.url} (${spec.label})` : spec.url;
        if (problems.length) {
          failed++;
          console.log(`FAIL ${name}`);
          problems.forEach((p) => console.log(`  - ${p}`));
        } else console.log(`ok   ${name}`);
      }
      const link = await checkFrontPageLink(context, origin);
      if (link.length) {
        failed++;
        link.forEach((p) => console.log(`FAIL ${p}`));
      } else console.log('ok   front page link to harjoittele/');
      console.log(failed ? 'PAGE CHECK FAILED' : 'PAGE CHECK OK');
    }
  } finally {
    await context.close();
    await browser.close();
    server.close();
  }
  process.exit(failed ? 1 : 0);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2));
}
