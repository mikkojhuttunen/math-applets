#!/usr/bin/env python3
"""EXT-02 (integer exponents: 2³ = 6, a⁰ = 0, 2⁻¹ = -2), type ME (multi-select equivalence). Expressions are
numeric (the variable x is only a schema placeholder) and written with ^ for the exponent; equivalence flags are
checked by verify.py and every distractor value is asserted to differ from the reference. Tagged distractors read
the power as a product, a⁰ as 0 and a negative exponent as a negative number."""
import random
from fractions import Fraction

from gen_common import MINUS, base_item, cli

TEMPLATE = "ext02_me"
TID, CODE = "EXT-02", "ME"
GOOD = "Oikein: potenssi on toistettu kertolasku, a^0 = 1 ja a^(−n) = 1/a^n."
GENERIC = "Laske jokaisen vaihtoehdon arvo erikseen ja vertaa viitelausekkeeseen. Muista: a^0 = 1 ja a^(−n) = 1/a^n."


def show(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1206)
    items, seen = [], set()
    for k in range(count):
        ctx = ""
        if k == 0:
            a, c = rng.choice([(3, 4), (2, 6), (5, 3)])
            n = 3
            level, ref, val = "T", f"{a}^{n} + {c}", Fraction(a ** n + c)
            eq = [f"{' · '.join([str(a)] * n)} + {c}", f"{c} + {a}^{n}", f"{a ** n + c}"]
            bad = [(f"{a} · {n} + {c}", Fraction(a * n + c)), (f"{a} + {n} + {c}", Fraction(a + n + c)),
                   (f"{a ** (n - 1)} + {c}", Fraction(a ** (n - 1) + c))]
            tags = [TID, TID, None]
            steps = [f"{a}^{n} = {' · '.join([str(a)] * n)} = {a ** n}", f"{a ** n} + {c} = {a ** n + c}"]
            params = {"a": a, "c": c}
        elif k == 1:
            a, b, c = rng.choice([(7, 3, 4), (5, 2, 6), (9, 4, 1)])
            level, ref, val = "T", f"{b} · {a}^0 + {c}", Fraction(b + c)
            eq = [f"{b} · 1 + {c}", f"{b + c}", f"{c} + {b} · {a}^0"]
            bad = [(f"{b} · 0 + {c}", Fraction(c)), (f"{b} · {a} + {c}", Fraction(a * b + c)),
                   (f"{a}^0 + {c}", Fraction(1 + c))]
            tags = [TID, None, None]
            steps = [f"{a}^0 = 1", f"{b} · 1 + {c} = {b + c}"]
            params = {"a": a, "b": b, "c": c}
        elif k == 2:
            a, b = rng.choice([(2, 10), (4, 12), (5, 20)])
            level, ref, val = "T", f"{a}^({MINUS}1) + {b}", Fraction(1, a) + b
            eq = [f"1/{a} + {b}", f"{b} + 1/{a}", f"{b} + {a}^({MINUS}1)"]
            bad = [(f"{MINUS}{a} + {b}", Fraction(b - a)), (f"{MINUS}1/{a} + {b}", b - Fraction(1, a)),
                   (f"{a} + {b}", Fraction(a + b))]
            tags = [TID, TID, None]
            steps = [f"{a}^({MINUS}1) = 1/{a}", f"1/{a} + {b} = {show(val)}"]
            params = {"a": a, "b": b}
        elif k == 3:
            a = rng.choice([2, 3, 5])
            level, ref, val = "H", f"{a}^0 + {a}^({MINUS}2)", 1 + Fraction(1, a * a)
            eq = [f"1 + 1/{a}^2", f"1/{a}^2 + 1", f"{a}^({MINUS}2) + 1"]
            bad = [(f"0 + 1/{a}^2", Fraction(1, a * a)), (f"1 {MINUS} {a}^2", Fraction(1 - a * a)),
                   (f"1 + {a}^2", Fraction(1 + a * a))]
            tags = [TID, TID, None]
            steps = [f"{a}^0 = 1", f"{a}^({MINUS}2) = 1/{a}^2 = 1/{a * a}", f"1 + 1/{a * a} = {show(val)}"]
            params = {"a": a}
        else:
            a, n = rng.choice([(2, 3), (3, 2), (5, 2)])
            level, ref, val = "H", f"{a}^{n} · {a}^0 · {a}^({MINUS}1)", Fraction(a ** n, a)
            ctx = "Valitse kaikki lausekkeet, joiden arvo on sama kuin tulon arvo. "
            eq = [f"{a}^{n - 1}", f"{a ** n} · 1 · 1/{a}", f"{a ** (n - 1)}"]
            bad = [(f"{a ** n} · 0 · {MINUS}{a}", Fraction(0)), (f"{a * n} · 1 · {MINUS}{a}", Fraction(-a * a * n)),
                   (f"{a ** n} · 1 · {a}", Fraction(a ** (n + 1)))]
            tags = [TID, TID, None]
            steps = [f"{a}^0 = 1", f"{a}^({MINUS}1) = 1/{a}", f"{a ** n} · 1 · 1/{a} = {show(val)}"]
            params = {"a": a, "n": n}
        assert all(v != val for _, v in bad), "distractor equals reference"
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        prompt = ctx or f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref}."
        opts = [(t, True, None) for t in eq] + [(t, False, m) for (t, _), m in zip(bad, tags)]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": ["x"], "samples": [[1], [2], [3]], "options": options}
        items.append(base_item(TID, CODE, start + k, ["S2.11"], ["T10", "T11"], 8, level, prompt, payload,
                               steps, show(val), GOOD, TEMPLATE, params, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
