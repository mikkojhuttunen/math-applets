// Loads the exercise files listed in data/manifest.json and turns the two
// bank formats into one shape the pages use:
//
// {
//   id, format: 'grades1-6' | 'grades7-9', gradeBand: '1-6' | '7-9',
//   grade (7-9 only, else null), level, goals: [], misconceptions: [],
//   status, pupilReady (reviewed / approved),
//   kind: 'entry' | 'choice', stem, hint,
//   answer (entry):  { kind: 'typed', value } for 1-6 text answers,
//                    { kind: 'number', value, tolerance, unit },
//                    { kind: 'set', values }, or
//                    { kind: 'expression', reference, variables, samples }
//   wrong (entry):   [{ match, misconception, feedback }]
//   options (choice): [{ id, text, correct, misconception, feedback }]
//   feedbackCorrect, solution: { steps, final } | null
// }
//
// Items the pages cannot show yet are skipped with a reason, never shown
// half-broken. Formats: math-misconceptions/grades1-6/exercises/grades1-6/README.md
// and math-misconceptions/schema/item.schema.json.

const PUPIL_READY = new Set(['reviewed', 'approved']);

function skip(reason) {
  return { skip: reason };
}

function misconceptionAnswers(raw) {
  return Object.entries(raw.misconceptions || {}).map(([id, v]) => ({
    match: v && v.answer !== undefined ? String(v.answer) : '',
    misconception: id,
    feedback: null,
  }));
}

export function normalize1to6(raw) {
  if (!raw || !raw.id) return skip('no id');
  const base = {
    id: raw.id,
    format: 'grades1-6',
    gradeBand: '1-6',
    grade: null,
    level: raw.level || null,
    goals: raw.goal ? [raw.goal] : [],
    misconceptions: raw.workbook || [],
    status: raw.status || 'unknown',
    pupilReady: PUPIL_READY.has(raw.status),
    stem: raw.stem_fi || '',
    hint: null,
    feedbackCorrect: null,
    solution: null,
  };
  if (!base.stem) return skip('no stem');
  if (raw.answer === undefined || raw.answer === null || raw.answer === '') return skip('no answer');

  if (raw.type === 'numeric_entry') {
    return { ...base, kind: 'entry', answer: { kind: 'typed', value: String(raw.answer) }, wrong: misconceptionAnswers(raw) };
  }
  if (raw.type === 'choice') {
    if (!Array.isArray(raw.options) || raw.options.length < 2) return skip('choice without options');
    const answer = String(raw.answer);
    const byAnswer = new Map(misconceptionAnswers(raw).map((w) => [w.match, w.misconception]));
    const letters = 'abcdefgh';
    const options = raw.options.map((text, i) => ({
      id: letters[i],
      text: String(text),
      correct: String(text) === answer,
      misconception: byAnswer.get(String(text)) || null,
      feedback: null,
    }));
    if (options.filter((o) => o.correct).length !== 1) return skip('answer is not exactly one of the options');
    return { ...base, kind: 'choice', options };
  }
  return skip(`type ${raw.type} not supported`);
}

export function normalize7to9(raw) {
  if (!raw || !raw.id) return skip('no id');
  const prompt = raw.prompt || {};
  if (prompt.figure) return skip('needs a figure');
  const payload = raw.payload || {};
  const base = {
    id: raw.id,
    format: 'grades7-9',
    gradeBand: '7-9',
    grade: (raw.curriculum && raw.curriculum.grade) || null,
    level: (raw.curriculum && raw.curriculum.level) || null,
    goals: (raw.curriculum && raw.curriculum.ops) || [],
    misconceptions: raw.misconceptions || [],
    status: raw.status || 'unknown',
    pupilReady: PUPIL_READY.has(raw.status),
    stem: prompt.text || '',
    hint: payload.input_hint || null,
    feedbackCorrect: (raw.feedback && raw.feedback.correct) || null,
    solution: raw.solution || null,
  };
  if (!base.stem) return skip('no stem');

  if (raw.type === 'NE') {
    const a = payload.answer;
    if (!a || !['number', 'set', 'expression'].includes(a.kind)) return skip('NE without a known answer kind');
    const wrong = (payload.wrong || []).map((w) => ({
      match: String(w.match),
      misconception: w.misconception || null,
      feedback: w.feedback || null,
    }));
    return { ...base, kind: 'entry', answer: a, wrong };
  }
  if (raw.type === 'MC') {
    const correct = new Set(payload.correct || []);
    const options = (payload.options || []).map((o) => ({
      id: o.id,
      text: o.text,
      correct: correct.has(o.id),
      misconception: o.misconception || null,
      feedback: o.feedback || null,
    }));
    if (options.length < 2 || options.filter((o) => o.correct).length !== 1) return skip('MC without exactly one correct option');
    return { ...base, kind: 'choice', options };
  }
  return skip(`type ${raw.type} not supported`);
}

export function itemsInFile(format, data) {
  if (format === 'grades1-6') return Array.isArray(data) ? data : [];
  return data && Array.isArray(data.items) ? data.items : [];
}

export function normalize(format, raw) {
  return format === 'grades1-6' ? normalize1to6(raw) : normalize7to9(raw);
}

async function fetchJson(fetchImpl, url) {
  const res = await fetchImpl(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// manifestUrl: absolute URL of data/manifest.json. File paths in the
// manifest are relative to harjoittele/, one level above data/.
// Returns { items, skipped: [{file, id, reason}], errors: [{file, message}] }.
// Drafts are included only when includeDrafts is true (teacher view).
export async function loadItems(manifestUrl, { fetchImpl = globalThis.fetch, includeDrafts = false } = {}) {
  const manifest = await fetchJson(fetchImpl, manifestUrl);
  const siteBase = new URL('../', manifestUrl);
  const items = [];
  const skipped = [];
  const errors = [];
  const seen = new Set();

  for (const file of manifest.files || []) {
    let data;
    try {
      data = await fetchJson(fetchImpl, new URL(file.path, siteBase).href);
    } catch (e) {
      errors.push({ file: file.path, message: e.message });
      continue;
    }
    for (const raw of itemsInFile(file.format, data)) {
      const item = normalize(file.format, raw);
      const id = raw && raw.id;
      if (item.skip) {
        skipped.push({ file: file.path, id, reason: item.skip });
      } else if (seen.has(item.id)) {
        skipped.push({ file: file.path, id, reason: 'duplicate id' });
      } else if (!item.pupilReady && !includeDrafts) {
        skipped.push({ file: file.path, id, reason: 'not reviewed' });
      } else {
        seen.add(item.id);
        items.push(item);
      }
    }
  }
  return { items, skipped, errors };
}
