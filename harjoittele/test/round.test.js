import test from 'node:test';
import assert from 'node:assert';
import { createRound, shuffle, answerText, presentOptions, TEXT } from '../js/round.js';

function entry(id, answer, wrong = []) {
  return { id, kind: 'entry', stem: `Laske ${id}`, answer: { kind: 'typed', value: answer }, wrong, feedbackCorrect: null };
}
const seq = (...values) => { let i = 0; return () => values[i++ % values.length]; };
const noShuffle = () => 0.999999;

const items = [
  entry('a', '776', [{ match: '836', misconception: 'NUM-10a', feedback: null }]),
  entry('b', '10'),
  entry('c', '3/4'),
];

test('shuffle keeps every item exactly once', () => {
  const out = shuffle([1, 2, 3, 4, 5], seq(0.1, 0.7, 0.3, 0.9));
  assert.deepStrictEqual([...out].sort(), [1, 2, 3, 4, 5]);
});

test('a round takes at most size items', () => {
  const r = createRound(items, { size: 2, random: noShuffle });
  assert.strictEqual(r.current().total, 2);
  assert.strictEqual(createRound(items, { size: 5 }).current().total, 3);
});

test('correct on the first try', () => {
  const r = createRound(items, { size: 3, random: noShuffle });
  const first = r.current().item;
  const out = r.answer(answerText(first));
  assert.strictEqual(out.status, 'correct');
  assert.strictEqual(out.text, TEXT.correct);
  assert.strictEqual(r.next(), true);
  assert.strictEqual(r.current().number, 2);
});

test('misconception answer gives the catalogue text, second wrong reveals the answer', () => {
  const r = createRound([items[0]], { feedback: (id) => (id === 'NUM-10a' ? 'Lainaa kymmenen.' : null) });
  const out1 = r.answer('836');
  assert.deepStrictEqual([out1.status, out1.text, out1.misconception], ['retry', 'Lainaa kymmenen.', 'NUM-10a']);
  assert.strictEqual(r.current().attempt, 2);
  const out2 = r.answer('700');
  assert.strictEqual(out2.status, 'reveal');
  assert.strictEqual(out2.text, TEXT.generalHint);
  assert.strictEqual(out2.correctAnswer, '776');
  assert.deepStrictEqual([r.current().number, r.current().total], [1, 1]);
  assert.strictEqual(r.next(), false);
  assert.strictEqual(r.current(), null);
  assert.deepStrictEqual(r.summary(), { total: 1, correct: 0, firstTry: 0, results: r.summary().results });
});

test('without a text (draft or unknown), the general hint is shown', () => {
  const r = createRound([items[0]]);
  assert.strictEqual(r.answer('836').text, TEXT.generalHint);
});

test('unreadable answer does not use a try', () => {
  const r = createRound([items[1]]);
  assert.strictEqual(r.answer('kymmenen').status, 'unreadable');
  assert.strictEqual(r.current().attempt, 1);
  assert.strictEqual(r.answer('9').status, 'retry');
  assert.strictEqual(r.answer('10').status, 'correct');
  const s = r.summary();
  assert.strictEqual(s.correct, 1);
  assert.strictEqual(s.firstTry, 0);
});

test('answers are ignored once the item is settled, next() is needed', () => {
  const r = createRound([items[1], items[2]], { random: noShuffle });
  r.answer(answerText(r.current().item));
  assert.strictEqual(r.answer('1'), null);
  assert.strictEqual(r.settled, true);
  assert.strictEqual(r.current().number, 1, 'current() still gives the settled item');
  r.next();
  assert.strictEqual(r.settled, false);
});

test('choice items use choose(), item feedback wins over the catalogue', () => {
  const item = {
    id: 'm', kind: 'choice', stem: 'Kumpi?', feedbackCorrect: 'Hyvä!',
    options: [
      { id: 'a', text: '1/4', correct: true, misconception: null, feedback: null },
      { id: 'b', text: '1/8', correct: false, misconception: 'NUM-12', feedback: 'Nimittäjä kertoo osien määrän.' },
    ],
  };
  const r = createRound([item], { feedback: () => 'catalogue' });
  assert.strictEqual(r.answer('1/4'), null);
  const out = r.choose('b');
  assert.deepStrictEqual([out.status, out.text], ['retry', 'Nimittäjä kertoo osien määrän.']);
  assert.deepStrictEqual([r.choose('a').status, r.summary().correct], ['correct', 1]);
});

test('answerText formats every answer kind in Finnish', () => {
  assert.strictEqual(answerText({ kind: 'entry', answer: { kind: 'number', value: -2.5, unit: 'cm' } }), '−2,5 cm');
  assert.strictEqual(answerText({ kind: 'entry', answer: { kind: 'set', values: [3, -3] } }), '3 tai −3');
  assert.strictEqual(answerText({ kind: 'entry', answer: { kind: 'expression', reference: '5x + 35' } }), '5x + 35');
});

test('presentOptions shuffles and letters the options; grading follows the id, not the position', () => {
  const item = {
    id: 'm', kind: 'choice', stem: 'Kumpi?',
    options: [
      { id: 'a', text: '1/4', correct: true, misconception: null },
      { id: 'b', text: '1/8', correct: false, misconception: 'NUM-12' },
      { id: 'c', text: '1/2', correct: false, misconception: null },
    ],
  };
  const shown = presentOptions(item, seq(0.1, 0.1));
  assert.deepStrictEqual(shown.map((o) => o.letter), ['A', 'B', 'C']);
  assert.deepStrictEqual([...shown.map((o) => o.id)].sort(), ['a', 'b', 'c']);
  assert.notStrictEqual(shown.map((o) => o.id).join(''), 'abc');
  const right = shown.find((o) => o.correct);
  assert.strictEqual(createRound([item]).choose(right.id).status, 'correct');
  assert.strictEqual(item.options[0].letter, undefined, 'item itself is not changed');
});
