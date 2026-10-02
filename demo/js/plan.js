// Demo site logic without the DOM: the plan (levels, seasons, topics),
// which exercises belong to a topic, the season of a date and the
// address (hash) of each screen. Unit-tested in test/plan.test.js.

import { normalize7to9 } from '../../harjoittele/js/items.js';

// Lukio demo items use the grades 7-9 item shape plus `set`. An answer
// may also be { kind: 'typed', value: '1/36' } (exact, shown as written),
// which the 7-9 loader does not take, so it is swapped in afterwards.
export function normalizeLukio(data) {
  const items = [];
  for (const raw of (data && data.items) || []) {
    const answer = raw.payload && raw.payload.answer;
    const typed = answer && answer.kind === 'typed' ? answer : null;
    const item = normalize7to9(typed ? { ...raw, payload: { ...raw.payload, answer: { kind: 'number', value: 0 } } } : raw);
    if (item.skip) continue;
    if (typed) item.answer = { kind: 'typed', value: String(typed.value) };
    items.push({ ...item, format: 'demo', gradeBand: 'lukio', set: raw.set });
  }
  return items;
}

export function topicItems(topic, bank, lukio) {
  if (topic.set) return lukio.filter((i) => i.set === topic.set);
  return bank.filter((i) => i.goals.includes(topic.goal) && (!topic.grade || i.grade === topic.grade));
}

// Autumn term from August, winter from December, spring from March.
export function seasonOf(date = new Date()) {
  const m = date.getMonth() + 1;
  if (m >= 3 && m <= 6) return 'kevat';
  if (m === 12 || m <= 2) return 'talvi';
  return 'syksy';
}

// '#7-9/talvi/2' -> { level: '7-9', season: 'talvi', topic: 2 }.
// Unknown parts are dropped, so a stale link falls back to a valid screen.
export function parseHash(hash, plan) {
  const [levelId, seasonId, topicNo] = decodeURIComponent(String(hash || '').replace(/^#\/?/, '')).split('/');
  const level = plan.levels.find((l) => l.id === levelId);
  if (!level) return {};
  const season = plan.seasons.find((s) => s.id === seasonId);
  if (!season) return { level: level.id };
  const topics = level.seasons[season.id] || [];
  const n = Number(topicNo);
  if (topicNo === undefined || !Number.isInteger(n) || n < 0 || n >= topics.length) return { level: level.id, season: season.id };
  return { level: level.id, season: season.id, topic: n };
}

export function hashFor({ level, season, topic } = {}) {
  if (!level) return '#';
  if (!season) return `#${level}`;
  if (topic === undefined || topic === null) return `#${level}/${season}`;
  return `#${level}/${season}/${topic}`;
}

// Every topic of the plan with its exercise count; used by the tests and
// the page check so that no button leads to an empty topic.
export function planCounts(plan, bank, lukio) {
  const rows = [];
  for (const level of plan.levels) {
    for (const season of plan.seasons) {
      (level.seasons[season.id] || []).forEach((topic, i) => {
        rows.push({ level: level.id, season: season.id, topic: i, title: topic.title, count: topicItems(topic, bank, lukio).length });
      });
    }
  }
  return rows;
}
