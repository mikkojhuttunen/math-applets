// Data for the test page (testaa.html). No DOM.

import { sortIds } from './filters.js';

// Which front-page section a goal band belongs to, by the section heading.
export function sectionKey(heading) {
  const h = (heading || '').toLowerCase();
  if (/1\s*[–-]\s*6/.test(h)) return '1-6';
  if (/7\s*[–-]\s*9/.test(h)) return '7-9';
  if (h.includes('lyhyt')) return 'lukio-lyhyt';
  if (h.includes('pitkä')) return 'lukio-pitka';
  return h;
}

const BAND_SECTION = { '1-2': '1-6', '3-6': '1-6', '7-9': '7-9' };
const SECTION_TITLES = { '1-6': 'Luokat 1–6', '7-9': 'Luokat 7–9' };

// Practice topics per goal band: { '1-2': [{ goal, items, reviewed }], ... }.
// goals: data/goals.json; items: all items, drafts included.
export function topicsByBand(items, goals) {
  const counts = new Map();
  for (const item of items) {
    for (const g of item.goals) {
      const c = counts.get(g) || { items: 0, reviewed: 0 };
      c.items++;
      if (item.pupilReady) c.reviewed++;
      counts.set(g, c);
    }
  }
  const out = {};
  for (const goal of sortIds([...counts.keys()])) {
    const band = (goals[goal] && goals[goal].band) || (goal.startsWith('S') ? '7-9' : '3-6');
    (out[band] = out[band] || []).push({ goal, ...counts.get(goal) });
  }
  return out;
}

// Front-page sections [{ heading, applets: [{ href, title }] }] merged with
// the practice topics. Every band with topics lands in its section, and a
// band whose section is missing on the front page still gets one.
export function buildLevels(sections, topics) {
  const levels = sections.map((s) => ({ key: sectionKey(s.heading), heading: s.heading, applets: s.applets, bands: [] }));
  for (const band of Object.keys(topics).sort()) {
    const key = BAND_SECTION[band] || band;
    let level = levels.find((l) => l.key === key);
    if (!level) {
      level = { key, heading: SECTION_TITLES[key] || key, applets: [], bands: [] };
      levels.push(level);
    }
    level.bands.push({ band, topics: topics[band] });
  }
  return levels;
}
