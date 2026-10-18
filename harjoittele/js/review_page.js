// Review page (tarkista.html). A reviewer goes through the draft items one
// by one; the collector merges the reviewers' files. Nothing leaves the
// browser: verdicts are kept in localStorage and exported as a file by the
// reviewer, and the page never changes the exercise files itself.

import { loadItems } from './items.js';
import { loadMisconceptions, feedbackFor } from './misconceptions.js';
import { answerText } from './round.js';
import { el } from './dom.js';
import * as R from './review.js';
import { editStatus, updateManifest, serializeManifest, STATUS_FOR_BAND } from './status_edit.js';
import { makeZip } from './zip.js';

const STORE_KEY = 'harjoittele.tarkista.v1';
const $ = (id) => document.getElementById(id);

let items = [];
let itemsById = {};
let texts = {};
let bankSize = 0;
let queue = [];
let fullQueue = [];
let index = 0;
let store = { reviewer: '', verdicts: {} };
let storageWorks = true;
let filters = { band: '', topic: '', kind: '', all: false };
let draft = { checks: {}, comment: '' };
let problem = '';
const mergeFiles = [];

// ------------------------------------------------------------- storage ---

function loadStore() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
    const verdicts = {};
    for (const [id, v] of Object.entries(raw.verdicts || {})) {
      if (v && R.VERDICTS.includes(v.verdict)) verdicts[id] = { verdict: v.verdict, comment: String(v.comment || '') };
    }
    store = { reviewer: R.cleanName(raw.reviewer), verdicts };
  } catch {
    /* no stored work, or storage unavailable */
  }
}

function saveStore() {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify(store));
  } catch {
    storageWorks = false;
  }
}

// -------------------------------------------------------------- helpers ---

function bandLabel(item) {
  return `lk ${item.gradeBand === '1-6' ? '1–6' : '7–9'}${item.grade ? ` (${item.grade}.)` : ''}`;
}

function misconceptionLabel(id) {
  if (!id) return '–';
  const f = feedbackFor(texts, id, { includeDrafts: true });
  return f ? `${id} ${f.name}` : id;
}

function wrongFeedback(w) {
  if (w.feedback) return w.feedback;
  const f = feedbackFor(texts, w.misconception, { includeDrafts: true });
  return f ? f.pupil : 'Ei palautetekstiä: oppilas saa yleisen vihjeen.';
}

function downloadText(name, data, type = 'text/plain') {
  const isText = typeof data === 'string';
  const url = URL.createObjectURL(new Blob([data], { type: isText ? `${type};charset=utf-8` : type }));
  const a = el('a', { href: url, download: name });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function copyText(text, message, fallbackId, messageId) {
  try {
    await navigator.clipboard.writeText(text);
    $(messageId).textContent = message;
    $(fallbackId).hidden = true;
  } catch {
    const ta = $(fallbackId);
    ta.value = text;
    ta.hidden = false;
    ta.select();
  }
}

// ----------------------------------------------------------- card view ---

function resetDraft() {
  const item = queue[index];
  const v = item && store.verdicts[item.id];
  draft = { checks: v && v.verdict === 'approve' ? Object.fromEntries(R.CHECKS.map((c) => [c.id, true])) : {}, comment: v ? v.comment : '' };
  problem = '';
}

function itemBody(item) {
  const body = [];
  body.push(el('p', { class: 'stem', text: item.stem }));
  if (item.hint) body.push(el('p', { class: 'status', text: `Oppilaalle näkyvä ohje: ${item.hint}` }));
  if (item.kind === 'entry') {
    body.push(el('p', { class: 'answer-line' }, 'Oikea vastaus: ', item.answerPrefix ? `${item.answerPrefix} ` : '', el('strong', { text: answerText(item) })));
    if (item.wrong.length) {
      body.push(el('table', { class: 'wrong' },
        el('thead', {}, el('tr', {}, el('th', { text: 'Väärä vastaus' }), el('th', { text: 'Virhekäsitys' }), el('th', { text: 'Palaute oppilaalle' }))),
        el('tbody', {}, ...item.wrong.map((w) =>
          el('tr', {}, el('td', { text: w.match }), el('td', { text: misconceptionLabel(w.misconception) }), el('td', { text: wrongFeedback(w) }))))));
    }
  } else {
    body.push(el('ul', { class: 'opt-list' }, ...item.options.map((o) =>
      el('li', { class: o.correct ? 'right' : '' },
        `${o.correct ? '✓ ' : ''}${o.text}`,
        o.misconception ? el('span', { class: 'opt-fb', text: `Virhekäsitys: ${misconceptionLabel(o.misconception)}` }) : null,
        o.feedback ? el('span', { class: 'opt-fb', text: `Palaute: ${o.feedback}` }) : null))));
  }
  if (item.feedbackCorrect) body.push(el('p', { class: 'status', text: `Palaute oikeasta vastauksesta: ${item.feedbackCorrect}` }));
  if (item.solution && item.solution.steps) {
    body.push(el('p', { class: 'status', text: `Ratkaisu: ${item.solution.steps.join(' → ')}${item.solution.final ? ` (vastaus: ${item.solution.final})` : ''}` }));
  }
  return body;
}

function renderCard() {
  const area = $('card-area');
  if (!items.length) return area.replaceChildren();
  if (!queue.length) {
    const none = fullQueue.length === 0;
    return area.replaceChildren(el('div', { class: 'card review-card' },
      el('p', { text: none ? 'Tällä rajauksella ei ole luonnostehtäviä.' : 'Kaikki rajauksen tehtävät on arvioitu. Kiitos! Tallenna tulokset tiedostoksi alla.' }),
      none ? null : el('button', { type: 'button', onclick: () => { $('setup').elements.mode.value = 'all'; applyFilters(); } }, 'Käy arvioidut uudelleen läpi')));
  }
  if (index >= queue.length) {
    return area.replaceChildren(el('div', { class: 'card review-card' },
      el('p', { text: 'Jono on käyty läpi. Tallenna tulokset tiedostoksi alla ja lähetä ne kokoajalle.' }),
      el('button', { type: 'button', onclick: () => { index = queue.length - 1; resetDraft(); render(); } }, 'Takaisin viimeiseen tehtävään')));
  }

  const item = queue[index];
  const saved = store.verdicts[item.id];
  const head = el('div', { class: 'item-head' },
    el('strong', { text: item.id }),
    el('span', { text: bandLabel(item) }),
    el('span', { text: item.goals.join(', ') }),
    item.level ? el('span', { text: `taso ${item.level}` }) : null,
    saved ? el('span', { class: `verdict-mark ${saved.verdict}`, text: { approve: 'HYVÄKSYTTY', fix: 'KORJATTAVA', reject: 'HYLÄTTY' }[saved.verdict] }) : null,
    el('a', { href: `index.html?luonnokset=1&tehtava=${encodeURIComponent(item.id)}`, target: '_blank', rel: 'noopener', text: 'Kokeile oppilaana' }));

  const checks = el('fieldset', { class: 'checks' }, el('legend', { text: 'Tarkistukset (kaikki vaaditaan hyväksymiseen)' }),
    ...R.CHECKS.map((c, i) => {
      const box = el('input', { type: 'checkbox', id: `check-${c.id}` });
      box.checked = Boolean(draft.checks[c.id]);
      box.addEventListener('change', () => { draft.checks[c.id] = box.checked; });
      return el('label', {}, box, `${i + 1}. ${c.text}`);
    }));

  const comment = el('textarea', { id: 'comment', maxlength: R.MAX_COMMENT, placeholder: 'Esimerkiksi: vaihtoehto C on myös oikein, kun x on 0' });
  comment.value = draft.comment;
  comment.addEventListener('input', () => { draft.comment = comment.value; });

  const verdictButton = (verdict, label, cls) => el('button', { type: 'button', class: cls, onclick: () => decide(verdict) }, label);
  const card = el('article', { class: 'card review-card' },
    head,
    ...itemBody(item),
    checks,
    el('label', { class: 'comment-label', for: 'comment', text: 'Kommentti (pakollinen, jos korjattava tai hylätty)' }),
    comment,
    el('p', { class: 'problem', id: 'problem', role: 'alert', text: problem }),
    el('div', { class: 'verdict-buttons' },
      verdictButton('approve', 'Hyväksy (A)', 'approve'),
      verdictButton('fix', 'Korjattava (K)', 'fix'),
      verdictButton('reject', 'Hylkää (H)', 'reject')),
    el('div', { class: 'nav-row' },
      el('button', { type: 'button', onclick: () => go(-1), disabled: index === 0 }, '← Edellinen'),
      el('span', { class: 'status', text: `Tehtävä ${index + 1} / ${queue.length}` }),
      el('button', { type: 'button', onclick: () => go(1) }, 'Seuraava →')));
  if (index === 0) card.querySelector('.nav-row button').disabled = true;
  area.replaceChildren(card);
}

// ------------------------------------------------------------- actions ---

function decide(verdict) {
  const item = queue[index];
  if (!item) return;
  const text = R.verdictProblem(verdict, draft.comment, draft.checks);
  if (text) {
    problem = text;
    const p = $('problem');
    if (p) p.textContent = text;
    return;
  }
  store.verdicts = R.setVerdict(store.verdicts, item.id, verdict, draft.comment);
  saveStore();
  go(1);
}

function go(delta) {
  index = Math.max(0, Math.min(queue.length, index + delta));
  resetDraft();
  render();
  window.scrollTo({ top: 0 });
}

function renderProgress() {
  const p = R.progress(fullQueue, store.verdicts);
  $('progress').max = Math.max(1, p.total);
  $('progress').value = p.judged;
  $('progress-text').textContent = p.total
    ? `Arvioitu ${p.judged} / ${p.total} · hyväksytty ${p.approve} · korjattavia ${p.fix} · hylättyjä ${p.reject}`
    : 'Ei tehtäviä tällä rajauksella.';
}

function renderStoreText() {
  const n = Object.keys(store.verdicts).length;
  $('store-text').textContent = `Arvioita yhteensä ${n}.${storageWorks ? ' Ne säilyvät tässä selaimessa.' : ' Selaimen muisti ei ole käytössä: tallenna tiedosto ennen sivun sulkemista.'}`;
}

function render() {
  renderProgress();
  renderCard();
  renderStoreText();
}

// ------------------------------------------------------------- filters ---

function currentSearch() {
  return R.searchFromParams(filters);
}

function applyFilters() {
  const f = $('setup').elements;
  filters = { band: f.band.value, topic: f.topic.value, kind: f.kind.value, all: f.mode.value === 'all' };
  history.replaceState(null, '', `${location.pathname}${currentSearch()}`);
  const link = $('share-link');
  link.href = `${location.origin}${location.pathname}${currentSearch()}`;
  link.textContent = link.href;
  fullQueue = R.buildQueue(items, { ...filters, unjudged: false });
  queue = R.buildQueue(items, { ...filters, unjudged: !filters.all }, store.verdicts);
  index = 0;
  resetDraft();
  render();
}

function fillTopics(selected) {
  const counts = new Map();
  for (const item of items) {
    if (item.pupilReady) continue;
    const t = R.topicOf(item);
    counts.set(t, (counts.get(t) || 0) + 1);
  }
  const select = $('setup').elements.topic;
  const topics = [...counts.keys()];
  if (selected && !counts.has(selected)) topics.push(selected);
  for (const t of R.sortItems(topics.map((id) => ({ id }))).map((x) => x.id)) {
    select.append(el('option', { value: t, text: counts.has(t) ? `${t} (${counts.get(t)})` : t }));
  }
}

// --------------------------------------------------------------- export ---

function resultsFile() {
  return R.buildReviewFile({ reviewer: store.reviewer, verdicts: store.verdicts, bankSize });
}

function needName() {
  if (store.reviewer) return false;
  $('export-message').textContent = 'Kirjoita ensin nimesi lomakkeen ylälaitaan.';
  $('setup').elements.reviewer.focus();
  return true;
}

function downloadResults() {
  if (needName()) return;
  if (!Object.keys(store.verdicts).length) {
    $('export-message').textContent = 'Ei vielä arvioita tallennettavaksi.';
    return;
  }
  downloadText(R.reviewFileName(store.reviewer), `${JSON.stringify(resultsFile(), null, 2)}\n`, 'application/json');
  $('export-message').textContent = 'Tiedosto ladattu. Lähetä se kokoajalle.';
}

function copyResults() {
  if (needName()) return;
  copyText(`${JSON.stringify(resultsFile(), null, 2)}\n`, 'Tulokset kopioitu leikepöydälle.', 'copy-fallback', 'export-message');
}

async function importOwn(event) {
  const file = event.target.files[0];
  event.target.value = '';
  if (!file) return;
  const parsed = R.parseReviewFile(await file.text());
  if (!parsed.ok) {
    $('export-message').textContent = parsed.error;
    return;
  }
  let added = 0;
  for (const v of parsed.file.verdicts) {
    if (!store.verdicts[v.id]) added++;
    store.verdicts = R.setVerdict(store.verdicts, v.id, v.verdict, v.comment);
  }
  if (!store.reviewer) store.reviewer = parsed.file.reviewer;
  $('setup').elements.reviewer.value = store.reviewer;
  saveStore();
  $('export-message').textContent = `Tuotu ${parsed.file.verdicts.length} arviota (${added} uutta).`;
  applyFilters();
}

function clearAll() {
  if (!Object.keys(store.verdicts).length) return;
  if (!window.confirm('Poistetaanko kaikki arviot tästä selaimesta? Tallenna tiedosto ensin, jos haluat säilyttää ne.')) return;
  store.verdicts = {};
  saveStore();
  $('export-message').textContent = 'Arviot poistettu.';
  applyFilters();
}

// ---------------------------------------------------------------- merge ---

// Builds a zip of the exercise files with the ready items set to approved
// (grades 7-9) or reviewed (grades 1-6), plus the updated manifest, with
// paths relative to the repository root. The files are fetched from the
// published site, so they match the repository only if everything has been
// pushed.
async function downloadUpdateZip(readyRows, fileName) {
  const message = $('merge-message');
  message.textContent = 'Haetaan tiedostoja…';
  try {
    const base = new URL('./', location.href);
    const byFile = new Map();
    for (const row of readyRows) {
      const item = itemsById[row.id];
      if (!byFile.has(item.file)) byFile.set(item.file, []);
      byFile.get(item.file).push(item);
    }
    const entries = [];
    const changes = [];
    for (const [file, list] of byFile) {
      const res = await fetch(new URL(file, base));
      if (!res.ok) throw new Error(`Tiedostoa ${file} ei saatu ladattua (${res.status}).`);
      let text = await res.text();
      for (const item of list) {
        const r = editStatus(text, item.id, item.gradeBand);
        if (r.result === 'missing') throw new Error(`Tunnistetta ${item.id} ei löytynyt tiedostosta ${file}.`);
        if (r.result === 'changed') {
          text = r.text;
          changes.push({ path: file, from: r.from, to: STATUS_FOR_BAND[item.gradeBand] });
        }
      }
      entries.push({ name: file.replace(/^\.\.\//, ''), text });
    }
    const res = await fetch(new URL('data/manifest.json', base));
    if (!res.ok) throw new Error('Tiedostoa manifest.json ei saatu ladattua.');
    const manifest = updateManifest(JSON.parse(await res.text()), changes);
    entries.push({ name: 'harjoittele/data/manifest.json', text: serializeManifest(manifest) });
    downloadText(fileName, makeZip(entries), 'application/zip');
    message.textContent = `Ladattu ${fileName}: ${changes.length} tehtävää, ${entries.length - 1} tehtävätiedostoa ja manifest.`;
  } catch (e) {
    message.textContent = `Päivitystiedostoa ei saatu tehtyä: ${e.message}`;
    console.error(e);
  }
}

function renderMerge() {
  const list = $('merge-files-list');
  list.replaceChildren(...mergeFiles.map((f, i) => el('li', {},
    el('span', { text: `${f.reviewer}: ${f.verdicts.length} arviota${f.created ? `, ${f.created}` : ''}${f.name ? ` (${f.name})` : ''}` }),
    el('button', { type: 'button', onclick: () => { mergeFiles.splice(i, 1); renderMerge(); } }, 'Poista'))));
  const result = $('merge-result');
  if (!mergeFiles.length) return result.replaceChildren();

  const minApprovals = Number($('min-approvals').value) || 1;
  const merged = R.mergeReviews(mergeFiles, { itemsById, minApprovals });
  const c = R.countOutcomes(merged.rows);
  const notes = [];
  const sizes = new Set(mergeFiles.map((f) => f.bankItems).filter(Boolean));
  if (sizes.size > 1 || (sizes.size === 1 && !sizes.has(bankSize))) notes.push('Osa tiedostoista on tehty eri tehtävämäärällä kuin nykyinen pankki. Tarkista, ettei tunnisteita puutu.');
  if (c.unknown) notes.push(`${c.unknown} tunnistetta ei löydy nykyisestä pankista, ne ohitetaan.`);
  if (c.already) notes.push(`${c.already} tehtävää on jo hyväksytty, ne ohitetaan.`);
  const untouched = items.filter((i) => !i.pupilReady && !merged.rows.some((r) => r.id === i.id)).length;

  const summary = el('p', {}, `Tarkastajia ${merged.people.length} (${merged.people.join(', ')}). Valmiita hyväksyttäväksi ${c.ready}, odottaa lisää hyväksyntöjä ${c.waiting}, ristiriitaisia ${c.conflict}, korjattavia ${c.fix}, hylättyjä ${c.reject}. Kukaan ei ole arvioinut ${untouched} luonnosta.`);

  const ready = merged.rows.filter((r) => r.outcome === 'ready' && r.known && !r.alreadyApproved);
  const attention = merged.rows.filter((r) => ['conflict', 'fix', 'reject'].includes(r.outcome) && r.known && !r.alreadyApproved);
  const waiting = merged.rows.filter((r) => r.outcome === 'waiting' && r.known && !r.alreadyApproved);
  const fileDate = new Date().toISOString().slice(0, 10);
  const zipName = `tehtavapaivitys-${fileDate}.zip`;

  const readyBlock = el('details', { class: 'merge-block', open: true },
    el('summary', { text: `Valmiit hyväksyttäväksi (${ready.length})` }),
    el('div', { class: 'toolbar' },
      el('button', { type: 'button', onclick: () => downloadText(`hyvaksytyt-${fileDate}.txt`, R.approvedText(merged.rows)) }, 'Lataa tunnisteet (.txt)'),
      el('button', { type: 'button', onclick: () => copyText(R.approvedText(merged.rows), 'Tunnisteet kopioitu.', 'merge-fallback', 'merge-message') }, 'Kopioi tunnisteet')),
    el('p', { class: 'status', text: 'Helpoin tapa: lataa päivitetyt tiedostot, pura ne tehtäväkansion päälle ja tee commit. Tiedostot haetaan julkaistulta sivustolta, joten aja ensin git pull.' }),
    el('div', { class: 'toolbar' },
      el('button', { type: 'button', class: 'primary', disabled: ready.length === 0, onclick: () => downloadUpdateZip(ready, zipName) }, 'Lataa päivitetyt tiedostot (.zip)')),
    el('code', { class: 'command', text: `cd math-applets\ngit pull\nunzip -o ~/Downloads/${zipName}\ngit status --short\ngit add math-misconceptions harjoittele/data/manifest.json\ngit commit -m "Hyväksy tarkistetut tehtävät"\ngit push origin main` }),
    el('details', { class: 'help' }, el('summary', { text: 'Vaihtoehto: tunnistelista ja komentorivityökalu' }),
      el('p', { class: 'status' }, 'Jos tehtävätiedostoihin on tehty muutoksia, joita ei ole vielä julkaistu, käytä tätä: lataa tunnistelista ja aja ',
        el('code', { class: 'command', text: `cd harjoittele\nnode tools/set_status.js hyvaksytyt-${fileDate}.txt\nnode tools/build_manifest.js\nnpm test` }))),
    el('ul', {}, ...ready.map((r) => el('li', { text: r.id }))));

  const attentionBlock = el('details', { class: 'merge-block', open: true },
    el('summary', { text: `Korjattavat, hylätyt ja ristiriitaiset (${attention.length})` }),
    el('div', { class: 'toolbar' },
      el('button', { type: 'button', onclick: () => downloadText(`korjattavat-${fileDate}.txt`, R.fixesText(merged.rows, itemsById)) }, 'Lataa kommentit (.txt)')),
    ...attention.map((r) => el('div', { class: 'merge-row' },
      el('strong', { text: `${r.id} ` }), el('span', { class: 'status', text: r.outcome === 'conflict' ? '(ristiriita)' : r.outcome === 'reject' ? '(hylätty)' : '(korjattava)' }),
      el('div', { text: itemsById[r.id].stem }),
      ...r.judgments.map((j) => el('span', { class: 'who', text: `${j.reviewer}: ${{ approve: 'hyväksyy', fix: 'korjattava', reject: 'hylkää' }[j.verdict]}${j.comment ? ` – ${j.comment}` : ''}` })))));

  const waitingBlock = waiting.length
    ? el('details', { class: 'merge-block' }, el('summary', { text: `Odottaa lisää hyväksyntöjä (${waiting.length})` }), el('ul', {}, ...waiting.map((r) => el('li', { text: `${r.id} (${r.approve} / ${minApprovals})` }))))
    : null;

  result.replaceChildren(summary, ...notes.map((n) => el('p', { class: 'error', text: n })), readyBlock, attentionBlock, waitingBlock,
    el('textarea', { id: 'merge-fallback', readonly: true, hidden: true, 'aria-label': 'Tunnisteet tekstinä' }));
}

async function addMergeFiles(event) {
  const files = [...event.target.files];
  event.target.value = '';
  const problems = [];
  for (const file of files) {
    const parsed = R.parseReviewFile(await file.text());
    if (parsed.ok) mergeFiles.push({ ...parsed.file, name: file.name });
    else problems.push(`${file.name}: ${parsed.error}`);
  }
  $('merge-message').textContent = problems.join(' ');
  renderMerge();
}

function addOwn() {
  if (!store.reviewer) {
    $('merge-message').textContent = 'Kirjoita nimesi Tarkista-välilehdelle ensin.';
    return;
  }
  const own = resultsFile();
  const copy = { reviewer: own.reviewer, created: own.created, bankItems: own.bank.items, verdicts: own.verdicts, name: 'omat arviot' };
  const at = mergeFiles.findIndex((f) => f.name === 'omat arviot');
  if (at >= 0) mergeFiles.splice(at, 1, copy);
  else mergeFiles.push(copy);
  $('merge-message').textContent = '';
  renderMerge();
}

// ----------------------------------------------------------------- tabs ---

function selectTab(name) {
  for (const t of ['review', 'merge']) {
    $(`tab-${t}`).setAttribute('aria-selected', String(t === name));
    $(`panel-${t}`).hidden = t !== name;
  }
  if (name === 'merge') renderMerge();
}

function onKey(event) {
  if (event.ctrlKey || event.metaKey || event.altKey) return;
  if ($('panel-review').hidden || !queue[index]) return;
  const tag = event.target.tagName;
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
  const key = event.key.toLowerCase();
  const map = { a: () => decide('approve'), k: () => decide('fix'), h: () => decide('reject'), arrowright: () => go(1), arrowleft: () => go(-1) };
  if (map[key]) {
    event.preventDefault();
    map[key]();
  } else if (/^[1-4]$/.test(key)) {
    const box = $(`check-${R.CHECKS[Number(key) - 1].id}`);
    box.checked = !box.checked;
    box.dispatchEvent(new Event('change'));
  }
}

// ----------------------------------------------------------------- init ---

async function init() {
  loadStore();
  const form = $('setup').elements;
  form.reviewer.value = store.reviewer;
  $('setup').addEventListener('submit', (e) => e.preventDefault());
  $('tab-review').addEventListener('click', () => selectTab('review'));
  $('tab-merge').addEventListener('click', () => selectTab('merge'));
  document.addEventListener('keydown', onKey);
  $('download').addEventListener('click', downloadResults);
  $('copy-results').addEventListener('click', copyResults);
  $('import-own').addEventListener('change', importOwn);
  $('clear-all').addEventListener('click', clearAll);
  $('merge-files').addEventListener('change', addMergeFiles);
  $('add-own').addEventListener('click', addOwn);
  $('min-approvals').addEventListener('change', renderMerge);
  form.reviewer.addEventListener('input', () => {
    store.reviewer = R.cleanName(form.reviewer.value);
    saveStore();
  });

  try {
    const base = new URL('data/', location.href);
    const [loaded, t] = await Promise.all([
      loadItems(new URL('manifest.json', base).href, { includeDrafts: true }),
      loadMisconceptions(new URL('misconceptions_fi.json', base).href).catch(() => ({})),
    ]);
    items = loaded.items;
    texts = t;
    bankSize = items.length;
    itemsById = Object.fromEntries(items.map((i) => [i.id, i]));
    const notes = [];
    if (loaded.skipped.length) notes.push(`${loaded.skipped.length} tehtävää ohitettiin, koska tehtävätyyppiä ei vielä tueta; ne eivät näy oppilaillekaan.`);
    if (loaded.errors.length) notes.push(`${loaded.errors.length} tiedostoa ei saatu ladattua.`);
    $('load-status').textContent = notes.join(' ');
  } catch (e) {
    $('load-status').textContent = 'Tietojen lataaminen epäonnistui.';
    $('load-status').className = 'error';
    console.error(e);
    return;
  }

  const fromUrl = R.paramsFromSearch(location.search);
  fillTopics(fromUrl.topic);
  form.band.value = fromUrl.band;
  form.topic.value = fromUrl.topic;
  form.kind.value = fromUrl.kind;
  form.mode.value = fromUrl.all ? 'all' : 'unjudged';
  $('setup').addEventListener('change', (e) => { if (e.target.name !== 'reviewer') applyFilters(); });
  applyFilters();
}

init();
