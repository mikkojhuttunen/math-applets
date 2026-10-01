// Column (allekkain) layout for whole-number subtraction, used to show a
// pupil where their answer differs from the correct one (W09).
//
// parseSubtraction("Laske 453 − 127.") -> { a: 453, b: 127 } or null
// columnLayout(453, 127, "334") -> {
//   width,                    number of digit columns
//   top, bottom,              digits right-aligned, '' where empty
//   given, correct,           the pupil's answer and the correct difference
//   carry,                    per column, the top value actually used in the
//                             correct method when borrowing changed it
//                             (for example '13', or '9' across a zero), else ''
//   wrong                     column indexes where given and correct differ
// }
// Column index 0 is the leftmost column.

export function parseSubtraction(stem) {
  // Only a bare subtraction ("Laske 453 − 127."), not one inside an
  // equation or another question such as "9 − 3 = □ + 5" or "y = 8 − 3x".
  const m = /^\s*(?:Laske\s+)?(\d+)\s*[−\-–]\s*(\d+)\s*[.=]?\s*$/.exec(stem || '');
  if (!m) return null;
  const a = Number(m[1]);
  const b = Number(m[2]);
  if (!Number.isSafeInteger(a) || !Number.isSafeInteger(b) || a < b) return null;
  return { a, b };
}

function digits(n, width) {
  const s = String(n);
  return Array.from({ length: width }, (_, i) => {
    const j = i - (width - s.length);
    return j >= 0 ? s[j] : '';
  });
}

export function columnLayout(a, b, givenText) {
  const given = String(givenText ?? '').trim();
  if (!/^\d+$/.test(given)) return null;
  const correctValue = a - b;
  const width = Math.max(String(a).length, String(b).length, given.length);
  const top = digits(a, width);
  const bottom = digits(b, width);
  const correct = digits(correctValue, width);
  const givenDigits = digits(Number(given), width);

  // Correct column method from the ones column leftwards.
  const carry = Array(width).fill('');
  let borrowIn = 0;
  for (let i = width - 1; i >= 0; i--) {
    const t = Number(top[i] || 0);
    const d = Number(bottom[i] || 0);
    let used = t - borrowIn;
    let borrowOut = 0;
    if (used < d) {
      used += 10;
      borrowOut = 1;
    }
    if (top[i] !== '' && used !== t) carry[i] = String(used);
    borrowIn = borrowOut;
  }

  const wrong = [];
  for (let i = 0; i < width; i++) if (givenDigits[i] !== correct[i]) wrong.push(i);
  return { width, top, bottom, given: givenDigits, correct, carry, wrong };
}
