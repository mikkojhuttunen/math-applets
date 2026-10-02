// Browser test of the demo site, with Playwright (Chromium).
//   NODE_PATH=$(npm root -g) node tools/browser_test.js
// Uses the practice pages' rules (tools/check_pages.js in harjoittele/):
// at 360 px no console errors, no requests to other sites, no horizontal
// scrolling, no NaN / undefined / decimal point / hyphen-minus on screen.
// Checks the start screen, every level and season, the first question of
// every topic, and plays one full round per level through to the summary.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { serve, checkPage } from '../../harjoittele/tools/check_pages.js';

const require = createRequire(import.meta.url);
const DEMO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const plan = JSON.parse(fs.readFileSync(path.join(DEMO, 'data/plan.json'), 'utf8'));

async function playRound(page) {
  for (let n = 0; n < 5; n++) {
    await page.waitForSelector('.stem');
    for (let attempt = 0; attempt < 6; attempt++) {
      if (await page.$('.feedback button.primary')) break;
      if (await page.$('#answer')) {
        await page.fill('#answer', '98765');
        await page.click('button[type=submit]');
      } else {
        await page.click('.option:not(:disabled)');
      }
    }
    await page.click('.feedback button.primary');
  }
  await page.waitForSelector('text=/Sait \\d\\/\\d oikein/');
}

async function main() {
  let chromium;
  try {
    ({ chromium } = require('playwright'));
  } catch {
    console.log('SKIP: playwright not found (set NODE_PATH=$(npm root -g) or npm install playwright)');
    process.exit(0);
  }
  const server = await serve();
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const specs = [{ url: 'demo/', wait: '.tile' }];
  for (const level of plan.levels) {
    specs.push({ url: `demo/#${level.id}`, wait: '.season' });
    for (const s of plan.seasons) {
      specs.push({ url: `demo/#${level.id}/${s.id}`, wait: '.topic' });
      (level.seasons[s.id] || []).forEach((_, i) => specs.push({ url: `demo/#${level.id}/${s.id}/${i}`, wait: '.stem' }));
    }
    const s = plan.seasons.find((x) => (level.seasons[x.id] || []).length);
    specs.push({ url: `demo/#${level.id}/${s.id}/0`, label: 'full round', wait: '.stem', prepare: playRound });
  }
  let failed = 0;
  try {
    for (const spec of specs) {
      const problems = await checkPage(context, origin, spec);
      const name = spec.label ? `${spec.url} (${spec.label})` : spec.url;
      if (problems.length) {
        failed++;
        console.log(`FAIL ${name}`);
        problems.forEach((p) => console.log(`  - ${p}`));
      }
    }
    console.log(`${specs.length} screens checked`);
    console.log(failed ? 'DEMO TEST FAILED' : 'DEMO TEST OK');
  } finally {
    await context.close();
    await browser.close();
    server.close();
  }
  process.exit(failed ? 1 : 0);
}

main();
