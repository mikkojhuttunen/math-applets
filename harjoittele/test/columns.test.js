import test from 'node:test';
import assert from 'node:assert';
import { parseSubtraction, columnLayout } from '../js/columns.js';
import { loadItems } from '../js/items.js';
import path from 'node:path';
import { SITE_DIR, fileFetch, fileUrl } from './helpers.js';

test('parseSubtraction reads the stem, U+2212 or hyphen', () => {
  assert.deepStrictEqual(parseSubtraction('Laske 453 − 127.'), { a: 453, b: 127 });
  assert.deepStrictEqual(parseSubtraction('Laske 800 - 406.'), { a: 800, b: 406 });
  assert.strictEqual(parseSubtraction('Laske 3/4 + 1/2.'), null);
  assert.strictEqual(parseSubtraction('Laske 12 − 30.'), null);
});

test('453 − 127: the three NUM-10 variants and where they go wrong', () => {
  const right = columnLayout(453, 127, '326');
  assert.deepStrictEqual(right.correct, ['3', '2', '6']);
  assert.deepStrictEqual(right.carry, ['', '4', '13']);
  assert.deepStrictEqual(right.wrong, []);
  assert.deepStrictEqual(columnLayout(453, 127, '334').wrong, [1, 2]); // NUM-10a
  assert.deepStrictEqual(columnLayout(453, 127, '324').wrong, [2]); // NUM-10b
  assert.deepStrictEqual(columnLayout(453, 127, '336').wrong, [1]); // NUM-10c
});

test('borrowing across a zero', () => {
  const l = columnLayout(800, 406, '394');
  assert.deepStrictEqual(l.carry, ['7', '9', '10']);
  assert.deepStrictEqual(l.wrong, []);
});

test('shorter numbers are right-aligned; a longer answer widens the grid', () => {
  const l = columnLayout(120, 7, '113');
  assert.deepStrictEqual(l.bottom, ['', '', '7']);
  assert.deepStrictEqual(l.carry, ['', '1', '10']);
  const wide = columnLayout(52, 17, '1035');
  assert.strictEqual(wide.width, 4);
  assert.deepStrictEqual(wide.correct, ['', '', '3', '5']);
  assert.deepStrictEqual(wide.wrong, [0, 1]);
});

test('answers that are not whole numbers get no layout', () => {
  for (const g of ['', '3,5', '−10', 'abc']) assert.strictEqual(columnLayout(453, 127, g), null, g);
});

test('every subtraction item: the stored wrong answers differ from the correct one in some column', async () => {
  const { items } = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  const subs = items.filter((i) => i.kind === 'entry' && parseSubtraction(i.stem));
  assert.ok(subs.length > 0);
  for (const item of subs) {
    const { a, b } = parseSubtraction(item.stem);
    assert.strictEqual(String(a - b), item.answer.value, item.id);
    for (const w of item.wrong) assert.ok(columnLayout(a, b, w.match).wrong.length > 0, `${item.id} ${w.match}`);
  }
});
