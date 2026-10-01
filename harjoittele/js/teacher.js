// Teacher view (opettaja.html): all items and feedback texts, drafts
// included, with filters, a selection of ids to mark as reviewed, and a
// printable worksheet. The page cannot change the JSON files; it gives the
// teacher the ids to change.

import { loadItems } from './items.js';
import { loadMisconceptions, feedbackFor } from './misconceptions.js';
import { answerText } from './round.js';
import { filterItems, summarize, sortIds, selectionText, paramsFromFilters } from './filters.js';
import { el } from './dom.js';

const PAGE = 40;
const STORE_KEY = 'harjoittele.opettaja.valinnat';

let items = [];
let texts = {};
let usage = {};
let shownItems = PAGE;
const selected = { items: new Set(), texts: new Set() };

const $ = (id) => document.getElementById(id);

// ---------------------------------------------------------- selection ---
// Kept in this browser only (teacher's own review work, not pupil data).

function saveSelection() {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify({ items: [...selected.items], texts: [...selected.texts] }));
  } catch {
    /* storage unavailable: selection lasts until the page is closed */
  }
}

function loadSelection() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
    (raw.items || []).forEach((id) => selected.items.add(id));
    (raw.texts || []).forEach((id) => selected.texts.add(id));
  } catch {
    /* ignore */
  }
}

function updateSelectionBar() {
  const n = selected.items.size;
  const m = selected.texts.size;
  $('selection-bar').hidden = n + m === 0;
  $('selection-count').textContent = `Valittu: ${n} tehtävää, ${m} palautetekstiä`;
  $('copy-fallback').hidden = true;
}

function toggle(set, id, on) {
  if (on) set.add(id);
  else set.delete(id);
  saveSelection();
  updateSelectionBar();
}

function selectionReport() {
  const parts = [];
  const byFile = new Map();
  for (const id of selected.items) {
    const item = items.find((i) => i.id === id);
    const key = item ? item.file.replace(/^\.\.\//, '') : '(ei löydy)';
    if (!byFile.has(key)) byFile.set(key, []);
    byFile.get(key).push(id);
  }
  for (const [file, ids] of [...byFile].sort()) {
    const item = items.find((i) => i.id === ids[0]);
    const status = item && item.gradeBand === '7-9' ? 'approved' : 'reviewed';
    parts.push(`${file} (status → "${status}"):\n${selectionText(ids)}`);
  }
  if (selected.texts.size) {
    parts.push(`harjoittele/data/misconceptions_fi.json (status → "reviewed"):\n${selectionText([...selected.texts])}`);
  }
  return parts.join('\n\n') + '\n';
}

async function copyIds() {
  const text = selectionReport();
  try {
    await navigator.clipboard.writeText(text);
    $('selection-count').textContent = 'Tunnisteet kopioitu leikepöydälle.';
  } catch {
    const ta = $('copy-fallback');
    ta.value = text;
    ta.hidden = false;
    ta.select();
  }
}

// -------------------------------------------------------------- items ---

function statusBadge(ready, draftLabel = 'LUONNOS') {
  return el('span', { class: ready ? 'badge ok' : 'badge draft', text: ready ? 'TARKISTETTU' : draftLabel });
}

function feedbackCell(id, own) {
  if (own) return el('td', { text: own });
  const f = feedbackFor(texts, id, { includeDrafts: true });
  if (!f) return el('td', { class: 'status', text: 'Ei palautetekstiä: oppilas saa yleisen vihjeen.' });
  return el('td', {}, f.pupil, ' ', f.status === 'reviewed' ? null : el('span', { class: 'badge draft', text: 'luonnos' }));
}

function misconceptionLabel(id) {
  if (!id) return '–';
  const f = feedbackFor(texts, id, { includeDrafts: true });
  return f ? `${id} ${f.name}` : id;
}

function itemCard(item) {
  const box = el('input', { type: 'checkbox' });
  box.checked = selected.items.has(item.id);
  box.addEventListener('change', () => toggle(selected.items, item.id, box.checked));
  const tryUrl = `index.html?luonnokset=1&tehtava=${encodeURIComponent(item.id)}`;
  const head = el('div', { class: 'item-head' },
    el('label', {}, box, item.id),
    statusBadge(item.pupilReady),
    el('span', { text: `${item.gradeBand === '1-6' ? 'lk 1–6' : 'lk 7–9'}${item.grade ? ` (${item.grade}.)` : ''}` }),
    el('span', { text: item.goals.join(', ') }),
    item.level ? el('span', { text: `taso ${item.level}` }) : null,
    el('span', { text: item.file.split('/').pop() }),
    el('a', { href: tryUrl, target: '_blank', rel: 'noopener', text: 'Kokeile' }),
  );
  const body = [head, el('p', { class: 'stem', text: item.stem })];

  if (item.kind === 'entry') {
    body.push(el('p', { class: 'answer-line' }, 'Oikea vastaus: ', el('strong', { text: answerText(item) })));
    if (item.wrong.length) {
      const rows = item.wrong.map((w) =>
        el('tr', {}, el('td', { text: w.match }), el('td', { text: misconceptionLabel(w.misconception) }), feedbackCell(w.misconception, w.feedback)));
      body.push(el('table', { class: 'wrong' },
        el('thead', {}, el('tr', {}, el('th', { text: 'Väärä vastaus' }), el('th', { text: 'Virhekäsitys' }), el('th', { text: 'Palaute oppilaalle' }))),
        el('tbody', {}, ...rows)));
    }
  } else {
    body.push(el('ul', { class: 'opt-list' }, ...item.options.map((o) =>
      el('li', { class: o.correct ? 'right' : '' },
        `${o.correct ? '✓ ' : ''}${o.text}`,
        o.misconception ? el('span', { class: 'status', text: ` (${misconceptionLabel(o.misconception)})` }) : null))));
    const wrongOpts = item.options.filter((o) => !o.correct && o.misconception);
    if (wrongOpts.length) {
      body.push(el('table', { class: 'wrong' },
        el('thead', {}, el('tr', {}, el('th', { text: 'Väärä vaihtoehto' }), el('th', { text: 'Virhekäsitys' }), el('th', { text: 'Palaute oppilaalle' }))),
        el('tbody', {}, ...wrongOpts.map((o) =>
          el('tr', {}, el('td', { text: o.text }), el('td', { text: misconceptionLabel(o.misconception) }), feedbackCell(o.misconception, o.feedback))))));
    }
  }
  if (item.solution && item.solution.steps) {
    body.push(el('p', { class: 'status', text: `Ratkaisu: ${item.solution.steps.join(' → ')}` }));
  }
  return el('article', { class: 'card item' }, ...body);
}

function itemFilters() {
  const f = new FormData($('item-filters'));
  return Object.fromEntries(['status', 'band', 'goal', 'misconception', 'query'].map((k) => [k, f.get(k) || '']));
}

function currentItems() {
  return filterItems(items, itemFilters());
}

function renderItems() {
  const list = currentItems();
  const s = summarize(list);
  $('item-count').textContent = `Näytetään ${list.length} / ${items.length} tehtävää (${s.reviewed} tarkistettu, ${s.draft} luonnosta).`;
  $('item-list').replaceChildren(...list.slice(0, shownItems).map(itemCard));
  $('more-items').hidden = list.length <= shownItems;
  // Link for pupils: same topic filters, no drafts, no status or text search.
  const f = itemFilters();
  const q = paramsFromFilters({ goal: f.goal, band: f.band, misconception: f.misconception }).toString();
  const link = new URL(`index.html${q ? `?${q}` : ''}`, location.href).href;
  $('pupil-link').href = link;
  $('pupil-link').textContent = link;
}

function fillSelect(select, counts, label = (id) => id) {
  for (const id of sortIds(Object.keys(counts))) {
    select.append(el('option', { value: id, text: `${label(id)} (${counts[id]})` }));
  }
}

// -------------------------------------------------------------- texts ---

function textCard(id, entry) {
  const box = el('input', { type: 'checkbox' });
  box.checked = selected.texts.has(id);
  box.addEventListener('change', () => toggle(selected.texts, id, box.checked));
  const n = usage[id] || 0;
  return el('article', { class: 'card item' },
    el('div', { class: 'item-head' },
      el('label', {}, box, id),
      statusBadge(entry.status === 'reviewed'),
      el('span', { text: n ? `käytössä ${n} tehtävässä` : 'ei vielä tehtävissä' })),
    el('p', { class: 'stem', text: entry.name_fi }),
    el('p', { class: 'text-block' }, el('span', { class: 'label', text: 'Oppilaalle' }), entry.pupil),
    el('p', { class: 'text-block' }, el('span', { class: 'label', text: 'Opettajalle' }), entry.teacher),
    entry.applets && entry.applets.length
      ? el('p', { class: 'text-block' }, el('span', { class: 'label', text: 'Appletit' }),
        ...entry.applets.flatMap((a, i) => [i ? ', ' : '', el('a', { href: `../${a}`, target: '_blank', rel: 'noopener', text: a })]))
      : null);
}

function renderTexts() {
  const f = new FormData($('text-filters'));
  const status = f.get('status');
  const usedOnly = f.get('used') === 'on';
  const ids = sortIds(Object.keys(texts)).filter((id) => {
    const e = texts[id];
    if (status === 'draft' && e.status === 'reviewed') return false;
    if (status === 'reviewed' && e.status !== 'reviewed') return false;
    if (usedOnly && !usage[id]) return false;
    return true;
  });
  $('text-count').textContent = `Näytetään ${ids.length} / ${Object.keys(texts).length} palautetekstiä.`;
  $('text-list').replaceChildren(...ids.map((id) => textCard(id, texts[id])));
}

// -------------------------------------------------------------- print ---

function printSheet() {
  const list = currentItems();
  if (!list.length) return;
  const sheet = $('print');
  const tasks = el('ol', {}, ...list.map((item) =>
    el('li', {},
      item.stem,
      item.kind === 'choice'
        ? el('span', { class: 'line', text: item.options.map((o) => `☐ ${o.text}`).join('     ') })
        : el('span', { class: 'line', text: 'Vastaus: ____________________' }))));
  const key = el('div', { class: 'key' },
    el('h1', { text: 'Vastaukset' }),
    el('ol', {}, ...list.map((item) => el('li', { text: answerText(item) }))));
  sheet.replaceChildren(
    el('h1', { text: 'Harjoitus' }),
    el('p', { class: 'sheet-info', text: 'Nimi: ______________________      Päivämäärä: ____________' }),
    tasks, key);
  window.print();
}

// --------------------------------------------------------------- init ---

function selectTab(which) {
  for (const t of ['items', 'texts']) {
    const on = t === which;
    $(`tab-${t}`).setAttribute('aria-selected', String(on));
    $(`panel-${t}`).hidden = !on;
  }
}

async function init() {
  loadSelection();
  const base = new URL('data/', location.href);
  try {
    const [loaded, t] = await Promise.all([
      loadItems(new URL('manifest.json', base).href, { includeDrafts: true }),
      loadMisconceptions(new URL('misconceptions_fi.json', base).href),
    ]);
    items = loaded.items;
    texts = t;
    const notes = [];
    if (loaded.skipped.length) notes.push(`${loaded.skipped.length} tehtävää ohitettiin (tyyppiä ei vielä tueta).`);
    if (loaded.errors.length) notes.push(`${loaded.errors.length} tiedostoa ei saatu ladattua.`);
    $('load-status').textContent = notes.join(' ');
  } catch (e) {
    $('load-status').textContent = 'Tietojen lataaminen epäonnistui.';
    $('load-status').className = 'error';
    console.error(e);
    return;
  }

  const s = summarize(items);
  usage = s.byMisconception;
  fillSelect($('item-filters').elements.goal, s.byGoal);
  fillSelect($('item-filters').elements.misconception, s.byMisconception, (id) => {
    const f = feedbackFor(texts, id, { includeDrafts: true });
    return f && f.id === id ? `${id} ${f.name}` : id;
  });

  $('item-filters').addEventListener('input', () => {
    shownItems = PAGE;
    renderItems();
  });
  $('item-filters').addEventListener('submit', (e) => e.preventDefault());
  $('text-filters').addEventListener('input', renderTexts);
  $('more-items').addEventListener('click', () => {
    shownItems += PAGE;
    renderItems();
  });
  $('select-visible').addEventListener('click', () => {
    currentItems().forEach((i) => selected.items.add(i.id));
    saveSelection();
    updateSelectionBar();
    renderItems();
  });
  $('print-sheet').addEventListener('click', printSheet);
  $('copy-ids').addEventListener('click', copyIds);
  $('clear-selection').addEventListener('click', () => {
    selected.items.clear();
    selected.texts.clear();
    saveSelection();
    updateSelectionBar();
    renderItems();
    renderTexts();
  });
  $('tab-items').addEventListener('click', () => selectTab('items'));
  $('tab-texts').addEventListener('click', () => selectTab('texts'));

  renderItems();
  renderTexts();
  updateSelectionBar();
}

init();
