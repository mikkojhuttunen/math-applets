// Answer checking for the practice pages. Agrees with the Python checkers:
// numbers and fractions like buggy_rules.parse_answer (grades 1-6), and
// expressions compared at sample points like scripts/verify.py (grades 7-9).
//
// checkAnswer(item, typed) -> {
//   result: 'correct' | 'wrong' | 'unreadable',
//   misconception: id | null,   the one stored wrong answer the reply matches
//   feedback: text | null,      that wrong answer's feedback, if the item has one
//   ambiguous: boolean          the reply matches more than one stored wrong answer
// }

// ------------------------------------------------------------ fractions ---

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a;
}

function frac(n, d = 1n) {
  if (d === 0n) return null;
  if (d < 0n) [n, d] = [-n, -d];
  const g = gcd(n, d) || 1n;
  return { n: n / g, d: d / g };
}

function fracEqual(a, b) {
  return a.n === b.n && a.d === b.d;
}

function fracToNumber(f) {
  return Number(f.n) / Number(f.d);
}

function decimalToFrac(text) {
  const m = /^(\d*)(?:\.(\d+))?$/.exec(text);
  if (!m || (m[1] === '' && m[2] === undefined)) return null;
  const decimals = m[2] || '';
  return frac(BigInt((m[1] || '0') + decimals), 10n ** BigInt(decimals.length));
}

// Minus signs, spaces and decimal comma to one plain form.
function clean(text) {
  return String(text)
    .replace(/[−–—]/g, '-')
    .replace(/[  ]/g, ' ')
    .trim()
    .replace(/\s+/g, ' ');
}

// Units after the number: "5 cm", "12 €", "3,5 m²", "90°". Only known
// units, so "2x" is not read as 2. Not "%", which changes the value.
const TRAILING_UNIT = /\s*(?:mm|cm|dm|km|m|mg|g|kg|t|ml|cl|dl|l|s|min|h|e|snt|€|°)[²³]?\.?$/i;

// "7", "-3", "0,5", "0.5", "5/6", "1 1/6", "1 000" (thousands spaces),
// "5 cm". Returns an exact fraction or null.
export function parseNumber(text) {
  let t = clean(text).replace(TRAILING_UNIT, '').replace(/^\+/, '');
  let sign = 1n;
  if (t.startsWith('-')) {
    sign = -1n;
    t = t.slice(1).trim();
  }
  let m;
  if ((m = /^(\d+) (\d+)\/(\d+)$/.exec(t))) {
    const f = frac(BigInt(m[2]), BigInt(m[3]));
    return f && frac(sign * (BigInt(m[1]) * f.d + f.n), f.d);
  }
  if ((m = /^(\d+)\/(\d+)$/.exec(t))) {
    return frac(sign * BigInt(m[1]), BigInt(m[2]));
  }
  if (/^\d{1,3}( \d{3})+([.,]\d+)?$/.test(t)) t = t.replace(/ /g, '');
  const f = decimalToFrac(t.replace(',', '.'));
  return f && frac(sign * f.n, f.d);
}

// "2; −3", "2 tai −3", "x = 2, x = −3" (comma needs a space after it,
// since "2,5" is a decimal). Returns an array of fractions or null.
export function parseNumberList(text) {
  const parts = clean(text)
    .split(/\s*;\s*|\s+(?:tai|ja)\s+|,\s+/i)
    .map((p) => p.replace(/^[a-zA-Z]\s*=\s*/, ''))
    .filter((p) => p !== '');
  if (parts.length === 0) return null;
  const values = parts.map(parseNumber);
  return values.every(Boolean) ? values : null;
}

// ---------------------------------------------------------- expressions ---

function tokenize(text) {
  const src = clean(text)
    .replace(/[×·⋅]/g, '*')
    .replace(/÷/g, '/')
    .replace(/²/g, '^2')
    .replace(/³/g, '^3');
  const tokens = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === ' ') {
      i++;
    } else if (/[0-9]/.test(c)) {
      const m = /^\d+(?:[.,]\d+)?/.exec(src.slice(i));
      tokens.push({ t: 'num', v: Number(m[0].replace(',', '.')) });
      i += m[0].length;
    } else if (/[a-zA-Z]/.test(c)) {
      tokens.push({ t: 'var', v: c });
      i++;
    } else if ('+-*/^()'.includes(c)) {
      tokens.push({ t: c });
      i++;
    } else {
      return null;
    }
  }
  return tokens;
}

// Parses into a function vars -> number. Implicit multiplication: "2x",
// "3(x + 1)", "x(x + 1)", "(x + 1)(x − 1)". Single-letter variables only.
export function parseExpression(text) {
  const tokens = tokenize(text);
  if (!tokens || tokens.length === 0) return null;
  let pos = 0;
  const peek = () => tokens[pos];
  const take = (t) => (peek() && peek().t === t ? tokens[pos++] : null);

  function expr() {
    let left = term();
    for (;;) {
      if (take('+')) {
        const a = left, b = term();
        left = (v) => a(v) + b(v);
      } else if (take('-')) {
        const a = left, b = term();
        left = (v) => a(v) - b(v);
      } else return left;
    }
  }
  function term() {
    let left = unary();
    for (;;) {
      if (take('*')) {
        const a = left, b = unary();
        left = (v) => a(v) * b(v);
      } else if (take('/')) {
        const a = left, b = unary();
        left = (v) => a(v) / b(v);
      } else if (peek() && (peek().t === 'var' || peek().t === '(')) {
        const a = left, b = power();
        left = (v) => a(v) * b(v);
      } else return left;
    }
  }
  function unary() {
    if (take('-')) {
      const a = unary();
      return (v) => -a(v);
    }
    if (take('+')) return unary();
    return power();
  }
  function power() {
    const base = primary();
    if (take('^')) {
      const exp = unary();
      return (v) => Math.pow(base(v), exp(v));
    }
    return base;
  }
  function primary() {
    const tok = tokens[pos++];
    if (!tok) throw new Error('end');
    if (tok.t === 'num') return () => tok.v;
    if (tok.t === 'var') {
      return (v) => {
        if (!(tok.v in v)) throw new Error(`unknown ${tok.v}`);
        return v[tok.v];
      };
    }
    if (tok.t === '(') {
      const inner = expr();
      if (!take(')')) throw new Error('missing )');
      return inner;
    }
    throw new Error(`unexpected ${tok.t}`);
  }

  try {
    const fn = expr();
    if (pos !== tokens.length) return null;
    return fn;
  } catch {
    return null;
  }
}

// Extra points besides the item's own samples, as in verify.py's POOL.
const EXTRA_POINTS = [-3, -2, -1, 2, 3, 5, 7, 0.5, -5 / 3];

function samplePoints(answer) {
  const vars = answer.variables || [];
  const points = (answer.samples || []).map((s) => Object.fromEntries(vars.map((v, i) => [v, s[i]])));
  EXTRA_POINTS.forEach((_, i) => {
    points.push(Object.fromEntries(vars.map((v, j) => [v, EXTRA_POINTS[(i + 4 * j) % EXTRA_POINTS.length]])));
  });
  return points;
}

function sameExpression(f, g, points) {
  let valid = 0;
  for (const p of points) {
    let a, b;
    try {
      a = f(p);
      b = g(p);
    } catch {
      return false; // uses a letter the answer does not have
    }
    if (!Number.isFinite(a) || !Number.isFinite(b)) continue;
    if (Math.abs(a - b) > 1e-9 * Math.max(1, Math.abs(a), Math.abs(b))) return false;
    valid++;
  }
  return valid >= 3;
}

// -------------------------------------------------------------- checking ---

function comparer(answer) {
  switch (answer.kind) {
    case 'typed': {
      const expected = parseNumber(answer.value);
      return { parse: parseNumber, equal: (x) => expected !== null && fracEqual(x, expected), same: fracEqual };
    }
    case 'number': {
      const tol = Math.max(answer.tolerance || 0, 1e-9);
      return {
        parse: parseNumber,
        equal: (x) => Math.abs(fracToNumber(x) - answer.value) <= tol,
        same: (x, y) => Math.abs(fracToNumber(x) - fracToNumber(y)) <= tol,
      };
    }
    case 'set': {
      const key = (list) => [...new Set(list.map((f) => `${f.n}/${f.d}`))].sort().join(' ');
      const expected = key(answer.values.map((v) => parseNumber(String(v))));
      return { parse: parseNumberList, equal: (x) => key(x) === expected, same: (x, y) => key(x) === key(y) };
    }
    case 'expression': {
      const points = samplePoints(answer);
      const ref = parseExpression(answer.reference);
      return {
        parse: parseExpression,
        equal: (x) => ref !== null && sameExpression(x, ref, points),
        same: (x, y) => sameExpression(x, y, points),
      };
    }
    default:
      return null;
  }
}

export function checkAnswer(item, typed) {
  const none = { misconception: null, feedback: null, ambiguous: false };
  const cmp = item && item.answer && comparer(item.answer);
  const value = cmp && String(typed || '').trim() ? cmp.parse(typed) : null;
  if (!value) return { result: 'unreadable', ...none };
  if (cmp.equal(value)) return { result: 'correct', ...none };

  const hits = (item.wrong || []).filter((w) => {
    const m = cmp.parse(w.match);
    return m && cmp.same(value, m);
  });
  if (hits.length === 1) {
    return { result: 'wrong', misconception: hits[0].misconception, feedback: hits[0].feedback, ambiguous: false };
  }
  return { result: 'wrong', misconception: null, feedback: null, ambiguous: hits.length > 1 };
}

// Choice items: the tapped option decides.
export function checkChoice(item, optionId) {
  const opt = (item.options || []).find((o) => o.id === optionId);
  if (!opt) return { result: 'unreadable', misconception: null, feedback: null, ambiguous: false };
  if (opt.correct) return { result: 'correct', misconception: null, feedback: null, ambiguous: false };
  return { result: 'wrong', misconception: opt.misconception, feedback: opt.feedback || null, ambiguous: false };
}
