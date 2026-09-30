#!/usr/bin/env node
// Automaattinen perustarkistus appletille (APPLET_SPEC.md, kohta 5).
// Käyttö: node scripts/check_applet.js [--shots <kansio>] <polku.html> [<polku.html> ...]
// --shots tallentaa kuvakaappaukset (360 px ja 1000 px, vaalea ja tumma) annettuun kansioon.
// Tarkistaa leveyksillä 360 px ja 1000 px, vaaleassa ja tummassa teemassa:
// konsolivirheet, sivuttaisvieritys, ulkoiset resurssit, lang="fi" ja viewport,
// sekä jokaisen liukusäätimen ääripäät. Tulostaa lopuksi CHECK OK tai CHECK FAILED.
"use strict";
const path = require("path");
const { execSync } = require("child_process");

function loadPlaywright() {
  try { return require("playwright"); } catch (_) {}
  const root = execSync("npm root -g").toString().trim();
  return require(path.join(root, "playwright"));
}

async function checkFile(browser, file, shots) {
  const url = "file://" + path.resolve(file);
  const problems = [];
  for (const width of [360, 1000]) {
    for (const scheme of ["light", "dark"]) {
      const tag = `${width}px/${scheme}`;
      const page = await browser.newPage({ viewport: { width, height: 800 }, colorScheme: scheme });
      const errors = [];
      const external = [];
      page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
      page.on("pageerror", e => errors.push(String(e)));
      page.on("request", r => { if (!r.url().startsWith("file:") && !r.url().startsWith("data:")) external.push(r.url()); });
      await page.goto(url);
      await page.waitForTimeout(200);

      const meta = await page.evaluate(() => ({
        lang: document.documentElement.lang,
        viewport: !!document.querySelector('meta[name="viewport"]'),
        title: document.title,
      }));
      if (width === 360 && scheme === "light") {
        if (meta.lang !== "fi") problems.push(`html lang on "${meta.lang}", pitää olla "fi"`);
        if (!meta.viewport) problems.push("viewport-meta puuttuu");
        if (!meta.title) problems.push("title puuttuu");
      }

      const ranges = await page.$$eval('input[type="range"]', els => els.map(e => e.id || e.name || ""));
      for (let i = 0; i < ranges.length; i++) {
        for (const end of ["min", "max"]) {
          await page.$$eval('input[type="range"]', (els, [i, end]) => {
            const el = els[i];
            el.value = el[end];
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
          }, [i, end]);
          const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
          if (overflow > 1) problems.push(`${tag}: sivuttaisvieritys ${overflow} px, kun säädin #${ranges[i] || i} = ${end}`);
          const bad = await page.evaluate(() => /NaN|undefined|Infinity/.test(document.body.innerText));
          if (bad) problems.push(`${tag}: sivulla näkyy NaN/undefined/Infinity, kun säädin #${ranges[i] || i} = ${end}`);
        }
      }

      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (overflow > 1) problems.push(`${tag}: sivuttaisvieritys ${overflow} px`);
      if (shots) {
        await page.goto(url);
        await page.waitForTimeout(200);
        const out = path.join(shots, `${path.basename(file, ".html")}-${width}-${scheme}.png`);
        await page.screenshot({ path: out, fullPage: true });
        console.log(`     kuva: ${out}`);
      }
      for (const e of errors) problems.push(`${tag}: konsolivirhe: ${e}`);
      for (const u of external) problems.push(`${tag}: ulkoinen resurssi: ${u}`);
      await page.close();
    }
  }
  return [...new Set(problems)];
}

(async () => {
  const args = process.argv.slice(2);
  let shots = null;
  const si = args.indexOf("--shots");
  if (si !== -1) { shots = args[si + 1]; args.splice(si, 2); require("fs").mkdirSync(shots, { recursive: true }); }
  const files = args;
  if (!files.length) { console.error("Käyttö: node scripts/check_applet.js <polku.html> [...]"); process.exit(2); }
  const { chromium } = loadPlaywright();
  const opts = {};
  if (process.env.PLAYWRIGHT_BROWSERS_PATH === "/opt/pw-browsers") opts.executablePath = "/opt/pw-browsers/chromium";
  let browser;
  try { browser = await chromium.launch(); } catch (_) { browser = await chromium.launch(opts); }
  let failed = false;
  for (const f of files) {
    const probs = await checkFile(browser, f, shots);
    if (probs.length) { failed = true; console.log(`FAIL ${f}`); for (const p of probs) console.log("  - " + p); }
    else console.log(`ok   ${f}`);
  }
  await browser.close();
  console.log(failed ? "CHECK FAILED" : "CHECK OK");
  process.exit(failed ? 1 : 0);
})();
