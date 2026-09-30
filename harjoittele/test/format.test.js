import test from 'node:test';
import assert from 'node:assert';
import { formatNumber } from '../js/format.js';

test('formatNumber uses decimal comma and U+2212', () => {
  assert.strictEqual(formatNumber(3.5), '3,5');
  assert.strictEqual(formatNumber(-2), '−2');
  assert.strictEqual(formatNumber(-0.25), '−0,25');
  assert.strictEqual(formatNumber(0.1 + 0.2), '0,3');
  assert.strictEqual(formatNumber(776), '776');
});

test('formatNumber never returns NaN or undefined text', () => {
  for (const v of [NaN, Infinity, undefined, null, '5']) {
    assert.strictEqual(formatNumber(v), '');
  }
});

