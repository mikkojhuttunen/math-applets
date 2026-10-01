// Goal browser (tavoitteet.html): every curriculum goal with its exercises,
// a practice link and related applets. ?haku= and ?luokat= are shareable.

import { loadItems } from './items.js';
import { loadMisconceptions } from './misconceptions.js';
import { goalRows, searchGoals, groupRows, BAND_TITLES } from './goals_view.js';
import { topicTitle } from './filters.js';
import { el } from './dom.js';

const $ = (id) => document.getElementById(id);
const form = $('goal-filters');
let rows = [];
let topics = {};
let texts = {};
let appletNames = {};

async function json(url, key) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`HTTP ${r.status} ${url}`);
  const d = await r.json();
  return key ? d[key] || {} : d;
}

// Applet titles from the front page's own links (same site).
async function loadAppletNames() {
  try {
    const html = await (await fetch(new URL('../index.html', location.href))).text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    return Object.fromEntries([...doc.querySelectorAll('a[href$=".html"]')].map((a) => [a.getAttribute('href'), a.textContent.trim()]));
  } catch {
    return {};
  }
}

function goalCard(r) {
  const links = [];
  if (r.reviewed) {
    links.push(el('a', { class: 'go', href: `index.html?tavoite=${encodeURIComponent(r.id)}`, text: `Harjoittele (${r.reviewed} tehtävää)` }));
  } else if (r.items) {
    links.push(el('a', { href: `index.html?tavoite=${encodeURIComponent(r.id)}&luonnokset=1`, text: `Esikatsele luonnoksia (${r.items})` }));
  }
  const parts = [
    el('div', { class: 'item-head' },
      el('code', { text: r.id }),
      r.grade ? el('span', { text: `lk ${r.grade}` }) : null,
      r.items ? el('span', { class: r.reviewed ? 'badge ok' : 'badge draft', text: `${r.items} tehtävää, ${r.reviewed} tarkistettu` }) : null),
    el('p', { class: 'goal-text', text: `Oppilas osaa ${r.text}` }),
  ];
  if (topics[r.id]) parts.push(el('p', { class: 'meta', text: `Harjoituksen nimi: ${topicTitle(r.id, topics)}` }));
  if (links.length) parts.push(el('p', { class: 'goal-links' }, ...links));
  if (r.applets.length) {
    parts.push(el('p', { class: 'text-block' }, el('span', { class: 'label', text: 'Appletit' }),
      ...r.applets.flatMap((a, i) => [i ? ', ' : '', el('a', { href: `../${a}`, text: appletNames[a] || a.split('/').pop() })])));
  }
  if (r.misconceptions.length) {
    parts.push(el('p', { class: 'text-block' }, el('span', { class: 'label', text: 'Virhekäsitykset tehtävissä' }),
      r.misconceptions.map((m) => (texts[m] ? `${m} ${texts[m].name_fi}` : m)).join('; ')));
  }
  return el('article', { class: 'card item goal' }, ...parts);
}

function render() {
  const f = new FormData(form);
  const filters = { query: f.get('haku') || '', band: f.get('luokat') || '', withContent: f.get('sisalto') === 'on' };
  const found = searchGoals(rows, filters);
  $('goal-count').textContent = found.length
    ? `Näytetään ${found.length} / ${rows.length} tavoitetta.`
    : 'Hakuehdoilla ei löytynyt tavoitteita.';
  const nodes = [];
  for (const { band, areas } of groupRows(found)) {
    nodes.push(el('h2', { text: BAND_TITLES[band] || band }));
    for (const { area, rows: list } of areas) {
      if (area) nodes.push(el('h3', { class: 'area', text: area }));
      nodes.push(...list.map(goalCard));
    }
  }
  $('goal-list').replaceChildren(...nodes);
  const p = new URLSearchParams();
  if (filters.query) p.set('haku', filters.query);
  if (filters.band) p.set('luokat', filters.band);
  if (filters.withContent) p.set('sisalto', '1');
  history.replaceState(null, '', p.toString() ? `?${p}` : location.pathname);
}

async function init() {
  const params = new URLSearchParams(location.search);
  form.elements.haku.value = params.get('haku') || '';
  form.elements.luokat.value = params.get('luokat') || '';
  form.elements.sisalto.checked = params.get('sisalto') === '1';
  const base = new URL('data/', location.href);
  try {
    const [goals, loaded, goalApplets, tp, t, names] = await Promise.all([
      json(new URL('goals.json', base), 'goals'),
      loadItems(new URL('manifest.json', base).href, { includeDrafts: true }),
      json(new URL('goal_applets.json', base), 'applets').catch(() => ({})),
      json(new URL('topics_fi.json', base), 'topics').catch(() => ({})),
      loadMisconceptions(new URL('misconceptions_fi.json', base).href).catch(() => ({})),
      loadAppletNames(),
    ]);
    rows = goalRows(goals, loaded.items, goalApplets);
    topics = tp;
    texts = t;
    appletNames = Object.fromEntries(Object.entries(names).map(([k, v]) => [k.replace(/^\.\//, ''), v]));
  } catch (e) {
    $('goal-count').textContent = 'Tavoitteiden lataaminen epäonnistui.';
    $('goal-count').className = 'error';
    console.error(e);
    return;
  }
  form.addEventListener('input', render);
  form.addEventListener('submit', (e) => e.preventDefault());
  render();
}

init();
