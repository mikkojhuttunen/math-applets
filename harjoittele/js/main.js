// Practice page: loads the exercises and runs rounds of five.
// ?luonnokset=1 shows draft exercises and draft feedback (teacher preview, WD2).

import { loadItems } from './items.js';
import { loadMisconceptions, feedbackFor } from './misconceptions.js';
import { createRound, answerText, presentOptions } from './round.js';
import { el } from './dom.js';

const ROUND_SIZE = 5;
const params = new URLSearchParams(location.search);
const drafts = params.get('luonnokset') === '1';
// ?tehtava=<id>: just that one item (the teacher view's "Kokeile" link).
const onlyItem = params.get('tehtava');
const app = document.getElementById('app');

let items = [];
let texts = {};
let round = null;

function show(...nodes) {
  app.replaceChildren(...nodes.filter(Boolean));
}

function feedbackText(id) {
  const f = feedbackFor(texts, id, { includeDrafts: drafts });
  return f ? f.pupil : null;
}

// ------------------------------------------------------------ number pad ---

const PAD_NUMBER = [
  ['7', '8', '9', '⌫'],
  ['4', '5', '6', '−'],
  ['1', '2', '3', '/'],
  ['0', ',', 'väli', 'C'],
];
const PAD_EXPRESSION = [['x', '(', ')', '+']];
const PAD_LABELS = { '⌫': 'poista merkki', '−': 'miinus', '/': 'murtoviiva', väli: 'välilyönti', C: 'tyhjennä' };

function pressKey(input, key) {
  const start = input.selectionStart ?? input.value.length;
  const end = input.selectionEnd ?? input.value.length;
  if (key === 'C') {
    input.value = '';
  } else if (key === '⌫') {
    if (start !== end) input.setRangeText('', start, end, 'end');
    else if (start > 0) input.setRangeText('', start - 1, start, 'end');
  } else {
    input.setRangeText(key === 'väli' ? ' ' : key, start, end, 'end');
  }
}

function numberPad(input, expression) {
  const rows = expression ? [...PAD_EXPRESSION, ...PAD_NUMBER] : PAD_NUMBER;
  const pad = el('div', { class: 'pad', role: 'group', 'aria-label': 'Numeronäppäimistö' });
  for (const row of rows) {
    for (const key of row) {
      const b = el('button', { type: 'button', class: 'key', 'aria-label': PAD_LABELS[key], text: key });
      // Keep the answer field's cursor where it is.
      b.addEventListener('pointerdown', (e) => e.preventDefault());
      b.addEventListener('click', () => pressKey(input, key));
      pad.append(b);
    }
  }
  return pad;
}

// --------------------------------------------------------------- screens ---

function progress(c) {
  const dots = el('div', { class: 'dots', 'aria-hidden': 'true' });
  for (let i = 1; i <= c.total; i++) {
    dots.append(el('span', { class: i < c.number ? 'dot done' : i === c.number ? 'dot now' : 'dot' }));
  }
  return el('div', { class: 'progress' }, el('span', { text: `Tehtävä ${c.number}/${c.total}` }), dots);
}

function draftInfo(item) {
  if (!drafts) return null;
  return el('p', { class: 'meta', text: `${item.id} · ${item.status}` });
}

function renderQuestion() {
  const c = round.current();
  const item = c.item;
  const feedback = el('div', { class: 'feedback', 'aria-live': 'polite' });
  const nodes = [progress(c), draftInfo(item), el('p', { class: 'stem', text: item.stem })];

  if (item.kind === 'entry') {
    const expression = item.answer.kind === 'expression';
    const input = el('input', {
      id: 'answer', class: 'answer', type: 'text', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false',
      inputmode: expression ? 'text' : 'decimal', placeholder: item.hint || 'Vastaus', 'aria-label': 'Vastaus',
    });
    const check = el('button', { type: 'submit', class: 'primary', text: 'Tarkista' });
    const form = el('form', { class: 'answer-row' }, input, check);
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (round.settled) return;
      handleOutcome(round.answer(input.value), feedback, () => {
        input.disabled = true;
        check.disabled = true;
      }, () => input.select());
    });
    nodes.push(form, feedback, numberPad(input, expression));
  } else {
    const options = el('div', { class: 'options', role: 'group', 'aria-label': 'Vaihtoehdot' });
    for (const opt of presentOptions(item)) {
      const b = el('button', { type: 'button', class: 'option', 'data-letter': opt.letter },
        el('span', { class: 'letter', 'aria-hidden': 'true', text: opt.letter }), el('span', { class: 'option-text', text: opt.text }));
      b.addEventListener('click', () => {
        if (round.settled) return;
        const out = round.choose(opt.id);
        if (out && out.status === 'retry') b.disabled = true;
        handleOutcome(out, feedback, () => options.querySelectorAll('button').forEach((x) => (x.disabled = true)));
      });
      options.append(b);
    }
    nodes.push(options, feedback);
  }
  show(...nodes);
  const first = app.querySelector('#answer, .option');
  if (first && !matchMedia('(pointer: coarse)').matches) first.focus();
}

function handleOutcome(out, feedback, lock, retry) {
  if (!out) return;
  const kind = out.status === 'correct' ? 'ok' : out.status === 'unreadable' ? 'info' : 'bad';
  const parts = [el('p', { class: `msg ${kind}`, text: out.text })];
  if (drafts && out.misconception) parts.push(el('p', { class: 'meta', text: `Virhekäsitys: ${out.misconception}` }));
  if (out.status === 'retry') parts.push(el('p', { class: 'msg', text: 'Yritä vielä kerran.' }));
  if (out.status === 'reveal') {
    parts.push(el('p', { class: 'msg' }, 'Oikea vastaus: ', el('strong', { text: out.correctAnswer })));
    if (out.solution && out.solution.steps) {
      parts.push(el('ol', { class: 'steps' }, ...out.solution.steps.map((s) => el('li', { text: s }))));
    }
  }
  if (out.status === 'correct' || out.status === 'reveal') {
    lock();
    const last = round.current().number === round.current().total;
    const next = el('button', { type: 'button', class: 'primary', text: last ? 'Katso tulos' : 'Seuraava' });
    next.addEventListener('click', () => (round.next() ? renderQuestion() : renderSummary()));
    parts.push(next);
    feedback.replaceChildren(...parts);
    next.focus();
    return;
  }
  feedback.replaceChildren(...parts);
  if (retry) retry();
}

function renderSummary() {
  const s = round.summary();
  const list = el('ul', { class: 'results' });
  for (const r of s.results) {
    const mark = r.correct ? '✓' : '✗';
    const tail = r.correct ? '' : ` (oikea vastaus ${answerText(r.item)})`;
    list.append(el('li', { class: r.correct ? 'ok' : 'bad' }, el('span', { class: 'mark', text: mark }), ` ${r.item.stem}${tail}`));
  }
  const again = el('button', { type: 'button', class: 'primary', text: 'Uusi kierros' });
  again.addEventListener('click', startRound);
  show(
    el('h2', { text: `Sait ${s.correct}/${s.total} oikein` }),
    el('p', { class: 'status', text: `Ensimmäisellä yrityksellä ${s.firstTry}/${s.total}.` }),
    list,
    again,
  );
  again.focus();
}

// Letter keys A-H choose an option on choice items.
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName || '')) return;
  const letter = e.key.length === 1 ? e.key.toUpperCase() : '';
  const b = letter && app.querySelector(`.option[data-letter="${letter}"]:not(:disabled)`);
  if (b) {
    e.preventDefault();
    b.click();
  }
});

function startRound() {
  const pool = onlyItem ? items.filter((i) => i.id === onlyItem) : items;
  round = createRound(pool, { size: ROUND_SIZE, feedback: feedbackText });
  renderQuestion();
}

function renderEmpty() {
  show(
    el('p', { text: 'Tarkistettuja tehtäviä ei ole vielä. Opettaja tarkistaa tehtävät ennen kuin ne tulevat harjoiteltaviksi.' }),
    el('p', { class: 'meta' }, 'Opettajalle: ', el('a', { href: '?luonnokset=1', text: 'esikatsele luonnoksia' })),
  );
}

async function init() {
  if (drafts) document.getElementById('draft-banner').hidden = false;
  const base = new URL('data/', location.href);
  try {
    const [loaded, t] = await Promise.all([
      loadItems(new URL('manifest.json', base).href, { includeDrafts: drafts }),
      loadMisconceptions(new URL('misconceptions_fi.json', base).href).catch(() => ({})),
    ]);
    items = loaded.items;
    texts = t;
    if (loaded.errors.length) console.warn('Some exercise files failed to load', loaded.errors);
  } catch (e) {
    show(el('p', { class: 'error', text: 'Tehtävien lataaminen epäonnistui. Päivitä sivu hetken kuluttua.' }));
    console.error(e);
    return;
  }
  if (onlyItem && !items.some((i) => i.id === onlyItem)) {
    show(el('p', { text: `Tehtävää ${onlyItem} ei löytynyt${drafts ? '' : ' tarkistetuista tehtävistä'}.` }));
    return;
  }
  if (items.length === 0) renderEmpty();
  else startRound();
}

init();
