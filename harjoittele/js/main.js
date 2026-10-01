// Practice page: a start screen to pick a topic, then rounds of five.
// URL parameters (shareable):
//   ?tavoite=A36.S2.04   one curriculum goal
//   ?luokat=1-6          one grade band
//   ?virhe=NUM-10        items about one misconception
//   ?tehtava=<id>        one item (the teacher view's "Kokeile" link)
//   ?luonnokset=1        drafts and draft feedback (teacher preview, WD2)

import { loadItems } from './items.js';
import { loadMisconceptions, feedbackFor } from './misconceptions.js';
import { createRound, answerText, presentOptions } from './round.js';
import { el } from './dom.js';
import { parseSubtraction, columnLayout } from './columns.js';
import { filterItems, filtersFromParams, paramsFromFilters, topicTitle, startChoices } from './filters.js';

const ROUND_SIZE = 5;
const drafts = new URLSearchParams(location.search).get('luonnokset') === '1';
const app = document.getElementById('app');
const BAND_TITLES = { '1-6': 'Luokat 1–6', '7-9': 'Luokat 7–9' };

let items = [];
let texts = {};
let goals = {};
let topics = {};
let round = null;
let pool = [];
let topicLabel = '';

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
  const nodes = [topicBar(), progress(c), draftInfo(item), el('p', { class: 'stem', text: item.stem })];

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
      const given = input.value;
      handleOutcome(round.answer(given), feedback, () => {
        input.disabled = true;
        check.disabled = true;
      }, () => input.select(), { item, given });
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

// Subtraction in columns: the pupil's answer with the differing columns
// marked. After the second try also the correct row and the borrows.
function columnsView(item, given, reveal) {
  const sub = item && item.kind === 'entry' && parseSubtraction(item.stem);
  const layout = sub && columnLayout(sub.a, sub.b, given);
  if (!layout || !layout.wrong.length) return null;
  const cols = layout.width + 1;
  const grid = el('div', { class: 'columns', style: `grid-template-columns: repeat(${cols}, 1.6em)` });
  const cell = (text, cls = '') => grid.append(el('span', { class: `c ${cls}`.trim(), text }));
  const row = (label, values, classOf = () => '') => {
    cell(label, 'op');
    values.forEach((v, i) => cell(v, classOf(i)));
  };
  if (reveal) row('', layout.carry, () => 'carry');
  row('', layout.top);
  row('\u2212', layout.bottom, () => 'line');
  row('', layout.given, (i) => (layout.wrong.includes(i) ? 'wrong' : ''));
  if (reveal) row('', layout.correct, () => 'right');
  const legend = reveal
    ? 'Ylärivillä pienet luvut näyttävät lainaamisen. Punaisella merkityissä sarakkeissa vastauksesi poikkeaa oikeasta (alin rivi).'
    : 'Punaisella merkityissä sarakkeissa on virhe. Laske ne uudelleen.';
  const columns = layout.wrong.length;
  return el('figure', { class: 'columns-box' }, grid,
    el('figcaption', { class: 'meta', text: legend }),
    el('span', { class: 'sr-only', text: `Virhe ${columns} sarakkeessa.` }));
}

function handleOutcome(out, feedback, lock, retry, context = {}) {
  if (!out) return;
  const kind = out.status === 'correct' ? 'ok' : out.status === 'unreadable' ? 'info' : 'bad';
  const parts = [el('p', { class: `msg ${kind}`, text: out.text })];
  if (out.status === 'retry' || out.status === 'reveal') {
    parts.push(columnsView(context.item, context.given, out.status === 'reveal'));
  }
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
    feedback.replaceChildren(...parts.filter(Boolean));
    next.focus();
    return;
  }
  feedback.replaceChildren(...parts.filter(Boolean));
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
  const change = el('button', { type: 'button', text: 'Vaihda aihe' });
  change.addEventListener('click', () => navigate({}));
  show(
    el('h2', { text: `Sait ${s.correct}/${s.total} oikein` }),
    el('p', { class: 'status', text: `Ensimmäisellä yrityksellä ${s.firstTry}/${s.total}.` }),
    list,
    el('div', { class: 'actions' }, again, change),
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

// ------------------------------------------------------- start / routing ---

function urlFor(filters) {
  const p = paramsFromFilters(filters);
  if (drafts) p.set('luonnokset', '1');
  const q = p.toString();
  return q ? `?${q}` : location.pathname;
}

function navigate(filters) {
  history.pushState(null, '', urlFor(filters));
  route();
}

function topicBar() {
  const change = el('a', { href: urlFor({}), text: 'Vaihda aihe' });
  change.addEventListener('click', (e) => {
    e.preventDefault();
    navigate({});
  });
  return el('p', { class: 'topic-bar' }, el('span', { text: topicLabel }), change);
}

function renderStart() {
  const groups = startChoices(items).map(({ band, goals: list }) =>
    el('div', { class: 'topic-group' },
      el('h3', { text: BAND_TITLES[band] || band }),
      ...list.map(({ id, count }) => {
        const b = el('a', { class: 'topic', href: urlFor({ goal: id }) },
          el('span', { class: 'topic-title', text: topicTitle(id, topics, goals) }),
          el('span', { class: 'topic-count', text: `${count} tehtävää` }));
        b.addEventListener('click', (e) => {
          e.preventDefault();
          navigate({ goal: id });
        });
        return b;
      })));
  const mixed = el('button', { type: 'button', text: 'Kaikki aiheet sekaisin' });
  mixed.addEventListener('click', () => {
    topicLabel = 'Kaikki aiheet';
    pool = items;
    startRound();
  });
  show(el('h2', { text: 'Valitse aihe' }), ...groups, el('div', { class: 'actions' }, mixed));
}

function describe(filters) {
  const parts = [];
  if (filters.goal) parts.push(topicTitle(filters.goal, topics, goals));
  if (filters.band) parts.push(BAND_TITLES[filters.band] || filters.band);
  if (filters.misconception) parts.push(`virhetyyppi ${filters.misconception}`);
  return parts.join(' · ');
}

function route() {
  const params = new URLSearchParams(location.search);
  const onlyItem = params.get('tehtava');
  const { filters, active } = filtersFromParams(params);
  if (items.length === 0) return renderEmpty();
  if (onlyItem) {
    pool = items.filter((i) => i.id === onlyItem);
    topicLabel = pool.length ? topicTitle(pool[0].goals[0], topics, goals) : onlyItem;
    if (!pool.length) return show(el('p', { text: `Tehtävää ${onlyItem} ei löytynyt${drafts ? '' : ' tarkistetuista tehtävistä'}.` }));
    return startRound();
  }
  if (!active) return renderStart();
  pool = filterItems(items, filters);
  topicLabel = describe(filters);
  if (!pool.length) {
    const back = el('a', { href: urlFor({}), text: 'Valitse toinen aihe' });
    back.addEventListener('click', (e) => {
      e.preventDefault();
      navigate({});
    });
    return show(el('p', { text: `Valinnalla ”${topicLabel}” ei ole vielä tehtäviä.` }), el('p', {}, back));
  }
  startRound();
}

window.addEventListener('popstate', route);

function startRound() {
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
    const optional = (name, key) =>
      fetch(new URL(name, base)).then((r) => r.json()).then((d) => d[key] || {}).catch(() => ({}));
    const [loaded, t, g, tp] = await Promise.all([
      loadItems(new URL('manifest.json', base).href, { includeDrafts: drafts }),
      loadMisconceptions(new URL('misconceptions_fi.json', base).href).catch(() => ({})),
      optional('goals.json', 'goals'),
      optional('topics_fi.json', 'topics'),
    ]);
    items = loaded.items;
    texts = t;
    goals = g;
    topics = tp;
    if (loaded.errors.length) console.warn('Some exercise files failed to load', loaded.errors);
  } catch (e) {
    show(el('p', { class: 'error', text: 'Tehtävien lataaminen epäonnistui. Päivitä sivu hetken kuluttua.' }));
    console.error(e);
    return;
  }
  route();
}

init();
