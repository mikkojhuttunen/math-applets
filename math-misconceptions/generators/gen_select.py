"""Multi-select MC built from equations (not a template itself): the pupil ticks every equation whose solution
is the given value. Reverse problems (RP) are posed this way. Each option gets feedback from substituting the
value, so the pupil sees why an equation does or does not fit; verify.py re-solves every option (payload.check).

Scoring (done by the apps, documented in the backlog): a select-all item is worth 2 points,
max(0, 2 · (ticked correct / all correct − ticked wrong / all wrong)). Ticking every option gives 0."""
import random
import re

import sympy as sp
from sympy.parsing.sympy_parser import implicit_multiplication_application, parse_expr, standard_transformations

MINUS = "−"
_LOCAL = {c: sp.Symbol(c) for c in "abcdefghijklmnopqrstuvwxyz"}
_TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def pretty(eq):
    """Pupil-facing form of an equation written with ASCII operators: '·' for '*', '÷' for a spaced '/',
    and a proper minus sign. Unspaced fractions such as 1/4 stay as they are."""
    s = eq.replace(" * ", " · ").replace(" / ", " ÷ ").replace(" - ", f" {MINUS} ")
    return re.sub(r"(^|[(= ])-(?=[\dx(])", rf"\1{MINUS}", s)


def _parse(text):
    s = text
    for a, b in ((MINUS, "-"), ("·", "*"), ("÷", "/"), ("²", "**2"), ("³", "**3")):
        s = s.replace(a, b)
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)
    left, right = s.split("=")
    # Decimals become exact fractions, so 0,35 compares equal to 7/20.
    t = lambda x: sp.nsimplify(parse_expr(x, local_dict=dict(_LOCAL), transformations=_TRANSFORMS), rational=True)
    return t(left), t(right)


def num(q):
    """Exact number as Finnish text: decimal comma for terminating decimals, otherwise a fraction."""
    q = sp.nsimplify(q)
    sign = MINUS if q < 0 else ""
    q = abs(q)
    if q.is_Integer:
        return f"{sign}{q}"
    p, d = q.as_numer_denom()
    k = d
    for f in (2, 5):
        while k % f == 0:
            k //= f
    if k == 1:
        return sign + f"{float(q):.10f}".rstrip("0").replace(".", ",")
    return f"{sign}{p}/{d}"


def feedback(text, var, value):
    """Why the equation does or does not have exactly the solution var = value."""
    left, right = _parse(text)
    x, v = sp.Symbol(var), sp.nsimplify(value)
    lv, rv = sp.nsimplify(left.subs(x, v)), sp.nsimplify(right.subs(x, v))
    sols = sp.solveset(left - right, x, sp.S.Reals)
    if lv != rv:
        return f"Kun sijoitat {var} = {num(v)}, vasen puoli on {num(lv)} mutta oikea puoli {num(rv)}."
    if sols == sp.FiniteSet(v):
        return f"Kun sijoitat {var} = {num(v)}, molemmat puolet ovat {num(lv)}."
    others = sorted(s for s in sols if s != v) if isinstance(sols, sp.FiniteSet) else []
    if others:
        return (f"{var} = {num(v)} toteuttaa yhtälön, mutta niin toteuttaa myös "
                + " ja ".join(f"{var} = {num(s)}" for s in others) + ".")
    return f"{var} = {num(v)} toteuttaa yhtälön, mutta niin toteuttaa moni muukin luku."


def select_all(seed, var, value, valid, invalid):
    """valid: equations whose only solution is var = value; invalid: [(equation, misconception id or None)].
    Returns the MC payload with the options in a fixed shuffled order (seeded by `seed`, so the shuffle does not
    touch the generator's own random stream)."""
    pool = [(pretty(e), None, True) for e in valid] + [(pretty(e), m, False) for e, m in invalid]
    assert len({t for t, _, _ in pool}) == len(pool), "duplicate option texts"
    assert 2 <= len(valid) and 2 <= len(invalid) and len(pool) <= 8
    random.Random(seed).shuffle(pool)
    options, correct = [], []
    for i, (t, m, ok) in enumerate(pool):
        oid = "abcdefgh"[i]
        options.append({"id": oid, "text": t, "misconception": m, "feedback": feedback(t, var, value)})
        if ok:
            correct.append(oid)
    return {"options": options, "correct": correct, "select": "all",
            "check": {"type": "solution_equals", "variable": var, "value": value}}
