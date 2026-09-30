import test from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { parseNumber, parseNumberList, parseExpression, checkAnswer, checkChoice } from '../js/answers.js';
import { loadItems } from '../js/items.js';
import { SITE_DIR, fileFetch, fileUrl } from './helpers.js';

const f = (n, d = 1) => ({ n: BigInt(n), d: BigInt(d) });

test('parseNumber reads the forms buggy_rules.parse_answer reads', () => {
  const cases = [
    ['7', f(7)], ['5/6', f(5, 6)], ['10/12', f(5, 6)], ['1 1/6', f(7, 6)], ['0,5', f(1, 2)], ['0.5', f(1, 2)],
    ['−3', f(-3)], ['-1 1/2', f(-3, 2)], ['  42 ', f(42)], ['+4', f(4)], [',5', f(1, 2)],
  ];
  for (const [text, want] of cases) assert.deepStrictEqual(parseNumber(text), want, text);
});

test('parseNumber also takes thousands spaces and units', () => {
  assert.deepStrictEqual(parseNumber('1 000'), f(1000));
  assert.deepStrictEqual(parseNumber('12 500,5'), f(25001, 2));
  assert.deepStrictEqual(parseNumber('5 cm'), f(5));
  assert.deepStrictEqual(parseNumber('12 €'), f(12));
  assert.deepStrictEqual(parseNumber('3,5 m²'), f(7, 2));
  assert.deepStrictEqual(parseNumber('90°'), f(90));
  assert.deepStrictEqual(parseNumber('2,50e'), f(5, 2));
});

test('parseNumber rejects what is not a number', () => {
  for (const t of ['', 'abc', '1/0', '2x', '5 %', '1 2', '1,2,3', '3 -', '4 kpl']) assert.strictEqual(parseNumber(t), null, t);
});

test('parseNumberList splits on ; tai ja and comma-space', () => {
  assert.deepStrictEqual(parseNumberList('2; −3'), [f(2), f(-3)]);
  assert.deepStrictEqual(parseNumberList('x = 2 tai x = −3'), [f(2), f(-3)]);
  assert.deepStrictEqual(parseNumberList('2,5, 3'), [f(5, 2), f(3)]);
  assert.strictEqual(parseNumberList('2; kolme'), null);
});

test('parseExpression handles implicit multiplication and powers', () => {
  const at = (t, v) => parseExpression(t)(v);
  assert.strictEqual(at('5x + 35', { x: 2 }), 45);
  assert.strictEqual(at('3(x + 1)', { x: 2 }), 9);
  assert.strictEqual(at('x(x − 1)', { x: 4 }), 12);
  assert.strictEqual(at('(x + 1)(x − 1)', { x: 3 }), 8);
  assert.strictEqual(at('2x²', { x: 3 }), 18);
  assert.strictEqual(at('−x^2', { x: 3 }), -9);
  assert.strictEqual(at('6x · 2 ÷ 4', { x: 1 }), 3);
  assert.strictEqual(at('1,5x', { x: 2 }), 3);
  for (const bad of ['', '5x +', '(x + 1', 'x ! 2', '2 3']) assert.strictEqual(parseExpression(bad), null, bad);
});

const typedItem = {
  answer: { kind: 'typed', value: '776' },
  wrong: [
    { match: '836', misconception: 'NUM-10a', feedback: null },
    { match: '736', misconception: 'NUM-10b', feedback: 'palaute' },
  ],
};

test('checkAnswer: correct, misconception, other wrong, unreadable', () => {
  assert.strictEqual(checkAnswer(typedItem, ' 776 ').result, 'correct');
  assert.deepStrictEqual(checkAnswer(typedItem, '736'), { result: 'wrong', misconception: 'NUM-10b', feedback: 'palaute', ambiguous: false });
  assert.deepStrictEqual(checkAnswer(typedItem, '700'), { result: 'wrong', misconception: null, feedback: null, ambiguous: false });
  assert.strictEqual(checkAnswer(typedItem, 'seitsemänsataa').result, 'unreadable');
  assert.strictEqual(checkAnswer(typedItem, '').result, 'unreadable');
});

test('checkAnswer: equal wrong answers from two rules are ambiguous', () => {
  const item = { answer: { kind: 'typed', value: '5' }, wrong: [{ match: '7', misconception: 'A' }, { match: '14/2', misconception: 'B' }] };
  assert.deepStrictEqual(checkAnswer(item, '7'), { result: 'wrong', misconception: null, feedback: null, ambiguous: true });
});

test('checkAnswer: typed fractions compare by value', () => {
  const item = { answer: { kind: 'typed', value: '5/6' }, wrong: [] };
  assert.strictEqual(checkAnswer(item, '10/12').result, 'correct');
  assert.strictEqual(checkAnswer({ answer: { kind: 'typed', value: '0,5' } }, '1/2').result, 'correct');
});

test('checkAnswer: number with tolerance, set, expression', () => {
  const num = { answer: { kind: 'number', value: 3.14, tolerance: 0.01 }, wrong: [{ match: '6,28', misconception: 'X', feedback: 'F' }] };
  assert.strictEqual(checkAnswer(num, '3,145').result, 'correct');
  assert.strictEqual(checkAnswer(num, '6,28').misconception, 'X');
  const set = { answer: { kind: 'set', values: [2, -3] }, wrong: [{ match: '2', misconception: 'Y', feedback: 'F' }] };
  assert.strictEqual(checkAnswer(set, '−3; 2').result, 'correct');
  assert.strictEqual(checkAnswer(set, 'x = 2 tai x = −3').result, 'correct');
  assert.strictEqual(checkAnswer(set, '2').misconception, 'Y');
  const ex = {
    answer: { kind: 'expression', variables: ['x'], reference: '5x + 35', samples: [[-2], [0], [3]] },
    wrong: [{ match: '5x + 7', misconception: 'ALG-08', feedback: 'Kerroin 5 kertoo myös sulun jälkimmäisen termin.' }],
  };
  assert.strictEqual(checkAnswer(ex, '35 + 5x').result, 'correct');
  assert.strictEqual(checkAnswer(ex, '5(x + 7)').result, 'correct');
  assert.strictEqual(checkAnswer(ex, '5x+7').misconception, 'ALG-08');
  assert.strictEqual(checkAnswer(ex, '5y + 35').result, 'wrong');
  assert.strictEqual(checkAnswer(ex, '5x +').result, 'unreadable');
});

test('checkChoice', () => {
  const item = { options: [{ id: 'a', correct: true }, { id: 'b', correct: false, misconception: 'M', feedback: 'F' }] };
  assert.strictEqual(checkChoice(item, 'a').result, 'correct');
  assert.deepStrictEqual(checkChoice(item, 'b'), { result: 'wrong', misconception: 'M', feedback: 'F', ambiguous: false });
  assert.strictEqual(checkChoice(item, 'z').result, 'unreadable');
});

test('every real item: its answer is correct, each stored wrong answer is recognised', async () => {
  const { items } = await loadItems(fileUrl(path.join(SITE_DIR, 'data', 'manifest.json')), { fetchImpl: fileFetch, includeDrafts: true });
  assert.ok(items.length > 0);
  for (const item of items) {
    if (item.kind === 'choice') {
      const right = item.options.find((o) => o.correct);
      assert.strictEqual(checkChoice(item, right.id).result, 'correct', item.id);
      continue;
    }
    const own = item.answer.kind === 'typed' ? item.answer.value
      : item.answer.kind === 'expression' ? item.answer.reference
      : item.answer.kind === 'number' ? String(item.answer.value) : item.answer.values.join('; ');
    assert.strictEqual(checkAnswer(item, own).result, 'correct', `${item.id} answer ${own}`);
    for (const w of item.wrong) {
      const r = checkAnswer(item, w.match);
      assert.strictEqual(r.result, 'wrong', `${item.id} wrong ${w.match}`);
      assert.ok(r.misconception === w.misconception || r.ambiguous, `${item.id} ${w.match} -> ${w.misconception}`);
    }
  }
});

test('fixture 7-9 items from the example generator check out too', async () => {
  const file = path.join(SITE_DIR, 'test', 'fixtures', 'repo', 'math-misconceptions', 'exercises', 'ALG-08', 'NE.json');
  const { normalize7to9 } = await import('../js/items.js');
  for (const raw of JSON.parse(fs.readFileSync(file, 'utf8')).items) {
    const item = normalize7to9(raw);
    assert.strictEqual(checkAnswer(item, item.answer.reference).result, 'correct', raw.id);
    for (const w of item.wrong) assert.strictEqual(checkAnswer(item, w.match).misconception, w.misconception, raw.id);
  }
});
