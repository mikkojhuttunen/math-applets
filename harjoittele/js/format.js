// Number formatting for pages: decimal comma, U+2212 minus sign.
// Returns '' for anything that is not a finite number, so NaN or
// undefined never reach the screen.

const MINUS = '−';

export function formatNumber(value, maxDecimals = 6) {
  if (typeof value !== 'number' || !Number.isFinite(value)) return '';
  const rounded = Number(value.toFixed(maxDecimals));
  const text = Math.abs(rounded).toString().replace('.', ',');
  return rounded < 0 ? MINUS + text : text;
}

