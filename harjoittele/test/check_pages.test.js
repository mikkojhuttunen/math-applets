import test from 'node:test';
import assert from 'node:assert';
import { textProblems, PAGES } from '../tools/check_pages.js';

test('textProblems accepts Finnish number format and ids', () => {
  assert.deepStrictEqual(textProblems('Laske 3,5 − 1,25. Oikea vastaus: −4. Luokat 1–6.'), []);
  assert.deepStrictEqual(textProblems('A36.S2.04-sub-20260930-1653-001 · S3.02 · batch-20260930-1653.json'), []);
  assert.deepStrictEqual(textProblems('https://mikkojhuttunen.github.io/math-applets/harjoittele/index.html'), []);
  assert.deepStrictEqual(textProblems('Laske 6/7 + 2/9 = 68/63'), []);
});

test('textProblems finds NaN, undefined, decimal points and hyphen minus', () => {
  const p = textProblems('NaN ja undefined, 3.5 ja (-4) sekä x = -2');
  assert.strictEqual(p.length, 4);
  assert.match(p.join(' | '), /NaN.*undefined.*decimal point.*hyphen-minus/);
});

test('the page list covers every page of the site', () => {
  const urls = PAGES.map((p) => p.url.split('?')[0]);
  for (const page of ['harjoittele/', 'harjoittele/opettaja.html', 'harjoittele/tavoitteet.html', 'harjoittele/testaa.html', 'index.html']) {
    assert.ok(urls.includes(page), page);
  }
});
