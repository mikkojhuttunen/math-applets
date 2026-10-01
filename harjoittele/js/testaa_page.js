// Test page (testaa.html): applets from the front page and practice topics
// from the exercise banks, per school level.

import { loadItems } from './items.js';
import { topicTitle } from './filters.js';
import { topicsByBand, buildLevels } from './testhub.js';
import { el } from './dom.js';

const $ = (id) => document.getElementById(id);
const BAND_TITLES = { '1-2': 'Harjoitukset, luokat 1–2', '3-6': 'Harjoitukset, luokat 3–6', '7-9': 'Harjoitukset, luokat 7–9' };

async function json(url, key) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`HTTP ${r.status} ${url}`);
  return (await r.json())[key] || {};
}

// Sections of the front page: each <h2> with the links in the list after it.
async function frontPageSections() {
  const html = await (await fetch(new URL('../index.html', location.href))).text();
  const doc = new DOMParser().parseFromString(html, 'text/html');
  return [...doc.querySelectorAll('h2')].map((h) => {
    let list = h.nextElementSibling;
    while (list && list.tagName !== 'UL' && list.tagName !== 'H2') list = list.nextElementSibling;
    const links = list && list.tagName === 'UL' ? [...list.querySelectorAll('a[href]')] : [];
    return { heading: h.textContent.trim(), applets: links.map((a) => ({ href: a.getAttribute('href'), title: a.textContent.trim() })) };
  });
}

function topicLink(t, topics, goals) {
  const href = `index.html?tavoite=${encodeURIComponent(t.goal)}${t.reviewed ? '' : '&luonnokset=1'}`;
  const note = t.reviewed ? `${t.items} tehtävää, ${t.reviewed} tarkistettu` : `${t.items} tehtävää, luonnoksia`;
  return el('li', {}, el('a', { href, text: topicTitle(t.goal, topics, goals) }), ' ', el('span', { class: 'status', text: `${t.goal} · ${note}` }));
}

function render(levels, topics, goals) {
  const nodes = [];
  for (const level of levels) {
    const parts = [el('h2', { text: level.heading })];
    parts.push(el('h3', { class: 'area', text: 'Appletit' }));
    parts.push(level.applets.length
      ? el('ul', {}, ...level.applets.map((a) => el('li', {}, el('a', { href: `../${a.href}`, text: a.title }))))
      : el('p', { class: 'status', text: 'Ei vielä appletteja.' }));
    if (level.bands.length) {
      for (const { band, topics: list } of level.bands) {
        parts.push(el('h3', { class: 'area', text: BAND_TITLES[band] || `Harjoitukset ${band}` }));
        parts.push(el('ul', {}, ...list.map((t) => topicLink(t, topics, goals))));
      }
    } else {
      parts.push(el('h3', { class: 'area', text: 'Harjoitukset' }));
      parts.push(el('p', { class: 'status', text: 'Ei vielä harjoituksia.' }));
    }
    nodes.push(el('section', { class: 'card level' }, ...parts));
  }
  $('levels').replaceChildren(...nodes);
}

async function init() {
  const base = new URL('data/', location.href);
  try {
    const [loaded, goals, topics, sections] = await Promise.all([
      loadItems(new URL('manifest.json', base).href, { includeDrafts: true }),
      json(new URL('goals.json', base), 'goals'),
      json(new URL('topics_fi.json', base), 'topics').catch(() => ({})),
      frontPageSections().catch(() => []),
    ]);
    const levels = buildLevels(sections, topicsByBand(loaded.items, goals));
    render(levels, topics, goals);
    const applets = levels.reduce((n, l) => n + l.applets.length, 0);
    const skipped = loaded.skipped.length ? ` ${loaded.skipped.length} tehtävää on tyyppiä, jota harjoitussivu ei vielä näytä.` : '';
    $('status').textContent = `${applets} applettia ja ${loaded.items.length} harjoitustehtävää.${skipped}`;
  } catch (e) {
    $('status').textContent = 'Sivun lataaminen epäonnistui.';
    $('status').className = 'error';
    console.error(e);
  }
}

init();
