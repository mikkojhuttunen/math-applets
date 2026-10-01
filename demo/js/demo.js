// Demo site: school level -> season -> topic -> a round of five exercises.
// Screens are addressed by the hash (#7-9/talvi/2), so the back button and
// shared links work. The exercise engine (checking, feedback, rounds) is
// the practice pages' own, imported read-only from ../harjoittele/js/.

import { loadItems } from '../../harjoittele/js/items.js';
import { loadMisconceptions, feedbackFor } from '../../harjoittele/js/misconceptions.js';
import { createRound, answerText, presentOptions } from '../../harjoittele/js/round.js';
import { parseSubtraction, columnLayout } from '../../harjoittele/js/columns.js';
import { el } from '../../harjoittele/js/dom.js';
import { normalizeLukio, topicItems, seasonOf, parseHash, hashFor } from './plan.js';

const ROUND_SIZE = 5;
const SEASON_ICONS = { syksy: '🍂', talvi: '❄️', kevat: '🌱' };
const SITE = new URL('../', location.href);

const app = document.getElementById('app');
const crumbs = document.getElementById('crumbs');
const title = document.getElementById('title');
const lead = document.getElementById('lead');
const HOME_TITLE = title.textContent;
const HOME_LEAD = lead.textContent;

let plan = { seasons: [], levels: [] };
let bank = [];
let lukio = [];
let texts = {};
let goalApplets = {};
let appletTitles = {};
let round = null;
let pool = [];

function show(...nodes) {
  app.replaceChildren(...nodes.filter(Boolean));
}

function link(state, cls, ...children) {
  return el('a', { class: cls, href: hashFor(state) }, ...children);
}

function setHeader(state) {
  const level = plan.levels.find((l) => l.id === state.level);
  const season = plan.seasons.find((s) => s.id === state.season);
  const parts = [link({}, '', 'Etusivu')];
  if (level) parts.push(el('span', { class: 'sep', text: '›' }), link({ level: level.id }, '', level.short || level.title));
  if (season && state.topic !== undefined) parts.push(el('span', { class: 'sep', text: '›' }), link({ level: level.id, season: season.id }, '', season.title));
  crumbs.replaceChildren(...(level ? parts : []));
  title.textContent = level ? level.title : HOME_TITLE;
  lead.textContent = level ? '' : HOME_LEAD;
  lead.hidden = Boolean(level);
}

function feedbackText(id) {
  const f = feedbackFor(texts, id, { includeDrafts: true });
  return f ? f.pupil : null;
}

function itemsOf(topic) {
  return topicItems(topic, bank, lukio);
}

function countText(n) {
  return n === 1 ? '1 tehtävä' : `${n} tehtävää`;
}

// ---------------------------------------------------------------- screens ---

function renderHome() {
  const tiles = plan.levels.map((level) => {
    let n = 0;
    for (const s of plan.seasons) for (const t of level.seasons[s.id] || []) n += itemsOf(t).length;
    return link({ level: level.id }, `tile lvl-${level.id}`,
      el('span', { class: 'tile-title', text: level.short || level.title }),
      el('span', { class: 'tile-sub', text: level.short ? 'Lukio' : 'Perusopetus' }),
      el('span', { class: 'tile-sub', text: countText(n) }));
  });
  show(el('h2', { text: 'Valitse kouluaste' }), el('div', { class: 'tiles' }, ...tiles));
}

function seasonButtons(level, current) {
  const now = seasonOf();
  return el('div', { class: 'seasons', role: 'group', 'aria-label': 'Vuodenaika' },
    ...plan.seasons.map((s) =>
      el('a', { class: 'season', href: hashFor({ level: level.id, season: s.id }), 'aria-current': s.id === current ? 'true' : 'false' },
        el('span', { class: 'icon', 'aria-hidden': 'true', text: SEASON_ICONS[s.id] || '' }),
        el('span', { text: s.title }),
        s.id === now ? el('span', { class: 'now', text: 'nyt' }) : null)));
}

function topicBadge(topic) {
  if (topic.grade) return el('span', { class: 'grade', text: `${topic.grade}. lk` });
  if (topic.course) return el('span', { class: 'grade', text: topic.course });
  return null;
}

function renderLevel(state) {
  const level = plan.levels.find((l) => l.id === state.level);
  const seasonId = state.season || seasonOf();
  const topics = level.seasons[seasonId] || [];
  const list = topics.map((topic, i) => {
    const n = itemsOf(topic).length;
    if (!n) {
      return el('div', { class: 'topic empty' }, el('span', { class: 'topic-title' }, topicBadge(topic), topic.title), el('span', { class: 'topic-count', text: 'ei vielä tehtäviä' }));
    }
    return link({ level: level.id, season: seasonId, topic: i }, `topic lvl-${level.id}`,
      el('span', { class: 'topic-title' }, topicBadge(topic), topic.title),
      el('span', { class: 'topic-count', text: countText(n) }));
  });
  show(
    el('h2', { text: 'Vuodenaika' }),
    seasonButtons(level, seasonId),
    el('h2', { text: 'Aiheet' }),
    ...(list.length ? list : [el('p', { class: 'empty', text: 'Tälle vuodenajalle ei ole vielä aiheita.' })]),
  );
}

function appletLinks(topic) {
  const paths = topic.applets || goalApplets[topic.goal] || [];
  if (!paths.length) return null;
  return el('div', { class: 'applets' },
    el('strong', { text: 'Tutki myös appletilla:' }),
    el('ul', {}, ...paths.map((p) => el('li', {}, el('a', { href: new URL(p, SITE).href, text: appletTitles[p] || p.split('/').pop() })))));
}

function renderTopic(state) {
  const level = plan.levels.find((l) => l.id === state.level);
  const topic = level.seasons[state.season][state.topic];
  pool = itemsOf(topic);
  if (!pool.length) {
    return show(el('p', { text: `Aiheessa ”${topic.title}” ei ole vielä tehtäviä.` }), el('p', {}, link({ level: level.id, season: state.season }, '', 'Valitse toinen aihe')));
  }
  startRound(state, topic);
}

// --------------------------------------------------------------- the round ---

const PAD = [
  ['7', '8', '9', '⌫'],
  ['4', '5', '6', '−'],
  ['1', '2', '3', '/'],
  ['0', ',', 'väli', 'C'],
];
const PAD_EXPRESSION = [['x', '²', '(', ')'], ['+', '·', '^', ';']];
const PAD_LABELS = { '⌫': 'poista merkki', '−': 'miinus', '/': 'murtoviiva', väli: 'välilyönti', C: 'tyhjennä', '²': 'toiseen', '·': 'kertomerkki', '^': 'potenssi' };

function pressKey(input, key) {
  const start = input.selectionStart ?? input.value.length;
  const end = input.selectionEnd ?? input.value.length;
  if (key === 'C') input.value = '';
  else if (key === '⌫') {
    if (start !== end) input.setRangeText('', start, end, 'end');
    else if (start > 0) input.setRangeText('', start - 1, start, 'end');
  } else input.setRangeText(key === 'väli' ? ' ' : key, start, end, 'end');
}

function numberPad(input, expression) {
  const pad = el('div', { class: 'pad', role: 'group', 'aria-label': 'Numeronäppäimistö' });
  for (const row of expression ? [...PAD_EXPRESSION, ...PAD] : PAD) {
    for (const key of row) {
      const b = el('button', { type: 'button', class: 'key', 'aria-label': PAD_LABELS[key], text: key });
      b.addEventListener('pointerdown', (e) => e.preventDefault());
      b.addEventListener('click', () => pressKey(input, key));
      pad.append(b);
    }
  }
  return pad;
}

function progress(c) {
  const dots = el('div', { class: 'dots', 'aria-hidden': 'true' });
  for (let i = 1; i <= c.total; i++) dots.append(el('span', { class: i < c.number ? 'dot done' : i === c.number ? 'dot now' : 'dot' }));
  return el('div', { class: 'progress' }, el('span', { text: `Tehtävä ${c.number}/${c.total}` }), dots);
}

function columnsView(item, given, reveal) {
  const sub = item && item.kind === 'entry' && parseSubtraction(item.stem);
  const layout = sub && columnLayout(sub.a, sub.b, given);
  if (!layout || !layout.wrong.length) return null;
  const grid = el('div', { class: 'columns', style: `grid-template-columns: repeat(${layout.width + 1}, 1.6em)` });
  const cell = (text, cls = '') => grid.append(el('span', { class: `c ${cls}`.trim(), text }));
  const row = (label, values, classOf = () => '') => {
    cell(label, 'op');
    values.forEach((v, i) => cell(v, classOf(i)));
  };
  if (reveal) row('', layout.carry, () => 'carry');
  row('', layout.top);
  row('−', layout.bottom, () => 'line');
  row('', layout.given, (i) => (layout.wrong.includes(i) ? 'wrong' : ''));
  if (reveal) row('', layout.correct, () => 'right');
  const legend = reveal
    ? 'Ylärivillä pienet luvut näyttävät lainaamisen. Punaisella merkityissä sarakkeissa vastauksesi poikkeaa oikeasta (alin rivi).'
    : 'Punaisella merkityissä sarakkeissa on virhe. Laske ne uudelleen.';
  return el('figure', { class: 'columns-box' }, grid, el('figcaption', { class: 'meta', text: legend }));
}

let current = { state: null, topic: null };

function topicBar() {
  return el('p', { class: 'topic-bar' }, el('span', { text: current.topic.title }),
    link({ level: current.state.level, season: current.state.season }, '', 'Vaihda aihe'));
}

function startRound(state, topic) {
  current = { state, topic };
  round = createRound(pool, { size: ROUND_SIZE, feedback: feedbackText });
  renderQuestion();
}

function renderQuestion() {
  const c = round.current();
  const item = c.item;
  const feedback = el('div', { class: 'feedback', 'aria-live': 'polite' });
  const nodes = [topicBar(), progress(c), el('p', { class: 'stem', text: item.stem })];
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
    nodes.push(form, feedback, numberPad(input, expression || item.answer.kind === 'set'));
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
  show(el('div', { class: 'card' }, ...nodes.filter(Boolean)), appletLinks(current.topic));
  const first = app.querySelector('#answer, .option');
  if (first && !matchMedia('(pointer: coarse)').matches) first.focus();
}

function handleOutcome(out, feedback, lock, retry, context = {}) {
  if (!out) return;
  const kind = out.status === 'correct' ? 'ok' : out.status === 'unreadable' ? 'info' : 'bad';
  const parts = [el('p', { class: `msg ${kind}`, text: out.text })];
  if (out.status === 'retry' || out.status === 'reveal') parts.push(columnsView(context.item, context.given, out.status === 'reveal'));
  if (out.status === 'retry') parts.push(el('p', { class: 'msg', text: 'Yritä vielä kerran.' }));
  if (out.status === 'reveal') {
    parts.push(el('p', { class: 'msg' }, 'Oikea vastaus: ', el('strong', { text: out.correctAnswer })));
    if (out.solution && out.solution.steps) parts.push(el('ol', { class: 'steps' }, ...out.solution.steps.map((s) => el('li', { text: s }))));
  }
  if (out.status === 'correct' || out.status === 'reveal') {
    lock();
    const c = round.current();
    const next = el('button', { type: 'button', class: 'primary', text: c.number === c.total ? 'Katso tulos' : 'Seuraava' });
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
    const tail = r.correct ? '' : ` (oikea vastaus ${answerText(r.item)})`;
    list.append(el('li', { class: r.correct ? 'ok' : 'bad' }, el('span', { class: 'mark', text: r.correct ? '✓' : '✗' }), ` ${r.item.stem}${tail}`));
  }
  const again = el('button', { type: 'button', class: 'primary', text: 'Uusi kierros' });
  again.addEventListener('click', () => startRound(current.state, current.topic));
  show(el('div', { class: 'card' },
    topicBar(),
    el('h2', { text: `Sait ${s.correct}/${s.total} oikein` }),
    el('p', { class: 'status', text: `Ensimmäisellä yrityksellä ${s.firstTry}/${s.total}.` }),
    list,
    el('div', { class: 'actions' }, again, link({ level: current.state.level, season: current.state.season }, 'button-link', 'Vaihda aihe'))));
  again.focus();
}

document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName || '')) return;
  const letter = e.key.length === 1 ? e.key.toUpperCase() : '';
  const b = letter && app.querySelector(`.option[data-letter="${letter}"]:not(:disabled)`);
  if (b) {
    e.preventDefault();
    b.click();
  }
});

// ---------------------------------------------------------------- routing ---

function route() {
  const state = parseHash(location.hash, plan);
  setHeader(state);
  if (state.topic !== undefined) renderTopic(state);
  else if (state.level) renderLevel(state);
  else renderHome();
  window.scrollTo(0, 0);
}

window.addEventListener('hashchange', route);

async function json(url, fallback) {
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch (e) {
    if (fallback !== undefined) return fallback;
    throw e;
  }
}

async function readAppletTitles() {
  try {
    const html = await (await fetch(new URL('index.html', SITE))).text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const titles = {};
    for (const a of doc.querySelectorAll('li > a[href]')) titles[a.getAttribute('href')] = a.textContent.trim();
    return titles;
  } catch {
    return {};
  }
}

async function init() {
  const data = new URL('data/', location.href);
  const practice = new URL('harjoittele/data/', SITE);
  try {
    const [p, loaded, l, t, ga, titles] = await Promise.all([
      json(new URL('plan.json', data)),
      loadItems(new URL('manifest.json', practice).href, { includeDrafts: true }),
      json(new URL('lukio_items.json', data), { items: [] }),
      loadMisconceptions(new URL('misconceptions_fi.json', practice).href).catch(() => ({})),
      json(new URL('goal_applets.json', practice), {}),
      readAppletTitles(),
    ]);
    plan = p;
    bank = loaded.items;
    lukio = normalizeLukio(l);
    texts = t;
    goalApplets = ga.applets || {};
    appletTitles = titles;
  } catch (e) {
    show(el('p', { class: 'error', text: 'Tehtävien lataaminen epäonnistui. Päivitä sivu hetken kuluttua.' }));
    console.error(e);
    return;
  }
  route();
}

init();
