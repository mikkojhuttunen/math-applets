// One practice round: a few items, up to two tries each. No DOM, nothing
// stored, so the whole flow can be unit-tested.
//
//   const round = createRound(items, { size: 5, random, feedback })
//   round.current()           -> { item, number, total, attempt }
//   round.answer(text)        -> outcome (typed items)
//   round.choose(optionId)    -> outcome (choice items)
//   round.next()              -> false when the round is over
//   round.summary()           -> { total, correct, firstTry, results }
//
// outcome.status:
//   'correct'     right answer (first or second try)
//   'retry'       wrong on the first try; outcome.text is the feedback
//   'reveal'      wrong on the second try; outcome.correctAnswer is shown
//   'unreadable'  could not read the typed answer; does not use a try

import { checkAnswer, checkChoice } from './answers.js';
import { formatNumber } from './format.js';

export const TEXT = {
  generalHint: 'Ei aivan. Tarkista laskusi ja yritä vielä kerran.',
  unreadable: 'En saanut vastauksesta selvää. Kirjoita luku, esimerkiksi 25, 3,5 tai 3/4.',
  unreadableExpression: 'En saanut vastauksesta selvää. Kirjoita lauseke, esimerkiksi 2x + 6.',
  correct: 'Oikein!',
};

export function shuffle(list, random = Math.random) {
  const a = list.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Options of a choice item in a fresh random order, each with the letter
// shown on its button (A, B, C ...). Grading uses option ids, so the order
// does not matter.
export function presentOptions(item, random = Math.random) {
  return shuffle(item.options || [], random).map((o, i) => ({ ...o, letter: 'ABCDEFGH'[i] }));
}

// The correct answer as shown to the pupil after the second try.
export function answerText(item) {
  if (item.kind === 'choice') return (item.options.find((o) => o.correct) || {}).text || '';
  const a = item.answer;
  switch (a.kind) {
    case 'typed':
      return a.value;
    case 'number':
      return formatNumber(a.value) + (a.unit ? ` ${a.unit}` : '');
    case 'set':
      return a.values.map((v) => formatNumber(v)).join(' tai ');
    case 'expression':
      return a.reference;
    default:
      return '';
  }
}

// feedback(misconceptionId) -> Finnish text or null; supplied by the page
// (misconceptions.feedbackFor), so the round does not know about drafts.
export function createRound(items, { size = 5, random = Math.random, feedback = () => null } = {}) {
  const picked = shuffle(items, random).slice(0, size);
  let index = 0;
  let attempt = 1;
  let finished = false;
  const results = [];

  // Still returns the item after it is settled, until next().
  function current() {
    if (index >= picked.length) return null;
    return { item: picked[index], number: index + 1, total: picked.length, attempt };
  }

  function wrongText(check) {
    if (check.feedback) return check.feedback;
    const fromCatalogue = check.misconception ? feedback(check.misconception) : null;
    return fromCatalogue || TEXT.generalHint;
  }

  function settle(check, given) {
    const item = picked[index];
    if (check.result === 'correct') {
      results.push({ item, correct: true, attempts: attempt, given });
      finished = true;
      return { status: 'correct', text: item.feedbackCorrect || TEXT.correct, misconception: null };
    }
    if (attempt === 1) {
      attempt = 2;
      return { status: 'retry', text: wrongText(check), misconception: check.misconception };
    }
    results.push({ item, correct: false, attempts: 2, given, misconception: check.misconception });
    finished = true;
    return {
      status: 'reveal',
      text: wrongText(check),
      misconception: check.misconception,
      correctAnswer: answerText(item),
      solution: item.solution,
    };
  }

  function answer(text) {
    const c = current();
    if (!c || finished || c.item.kind !== 'entry') return null;
    const check = checkAnswer(c.item, text);
    if (check.result === 'unreadable') {
      const expr = c.item.answer.kind === 'expression';
      return { status: 'unreadable', text: expr ? TEXT.unreadableExpression : TEXT.unreadable, misconception: null };
    }
    return settle(check, text);
  }

  function choose(optionId) {
    const c = current();
    if (!c || finished || c.item.kind !== 'choice') return null;
    const check = checkChoice(c.item, optionId);
    if (check.result === 'unreadable') return null;
    return settle(check, optionId);
  }

  // After 'correct' or 'reveal': move on. Returns false at the end.
  function next() {
    if (!finished) return current() !== null;
    index += 1;
    attempt = 1;
    finished = false;
    return index < picked.length;
  }

  function summary() {
    return {
      total: picked.length,
      correct: results.filter((r) => r.correct).length,
      firstTry: results.filter((r) => r.correct && r.attempts === 1).length,
      results,
    };
  }

  return { current, answer, choose, next, summary, get settled() { return finished; } };
}
