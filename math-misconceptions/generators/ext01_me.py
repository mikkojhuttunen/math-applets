#!/usr/bin/env python3
"""EXT-01 (negative base and square: -3² read as 9), type ME (multi-select equivalence). Expressions are numeric
(the variable x is only a schema placeholder); equivalence flags are checked by verify.py and every distractor
value is asserted to differ from the reference. Tagged distractors read -a² as (-a)² or the reverse."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "ext01_me"
TID, CODE = "EXT-01", "ME"
GOOD = "Oikein: −a² = −(a · a), mutta (−a)² = (−a) · (−a) = a²."
GENERIC = "Laske jokaisen vaihtoehdon arvo erikseen ja vertaa viitelausekkeeseen. Muista, että −a² ≠ (−a)²."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1203)
    items, seen = [], set()
    for k in range(count):
        ctx = ""
        if k == 0:
            a, b = rng.choice([(4, 10), (5, 30), (6, 40)])
            level, ref, val = "T", f"{MINUS}{a}² + {b}", -a * a + b
            eq = [f"{MINUS}({a} · {a}) + {b}", f"{b} {MINUS} {a}²", f"{num(-a * a)} + {b}"]
            bad = [(f"({MINUS}{a})² + {b}", TID, a * a + b), (f"{a}² + {b}", TID, a * a + b),
                   (f"{MINUS}{2 * a} + {b}", None, -2 * a + b)]
            steps = [f"{MINUS}{a}² = {MINUS}({a} · {a}) = {num(-a * a)}", f"{num(-a * a)} + {b} = {num(val)}"]
            params = {"a": a, "b": b}
        elif k == 1:
            a, c = rng.choice([(3, 4), (7, 5), (8, 6)])
            level, ref, val = "T", f"{MINUS}{a}² {MINUS} {c}", -a * a - c
            eq = [f"{MINUS}({a} · {a}) {MINUS} {c}", f"{MINUS}{c} {MINUS} {a}²", f"{num(-a * a - c)}"]
            bad = [(f"({MINUS}{a})² {MINUS} {c}", TID, a * a - c), (f"{a}² {MINUS} {c}", TID, a * a - c),
                   (f"{MINUS}{2 * a} {MINUS} {c}", None, -2 * a - c)]
            steps = [f"{MINUS}{a}² = {num(-a * a)}", f"{num(-a * a)} {MINUS} {c} = {num(val)}"]
            params = {"a": a, "c": c}
        elif k == 2:
            d, c = rng.choice([(2, 20), (3, 30), (4, 50)])
            level, ref, val = "T", f"({MINUS}{d})² + {c}", d * d + c
            eq = [f"{d}² + {c}", f"({MINUS}{d}) · ({MINUS}{d}) + {c}", f"{d} · {d} + {c}"]
            bad = [(f"{MINUS}{d}² + {c}", TID, -d * d + c), (f"{MINUS}({d} · {d}) + {c}", TID, -d * d + c),
                   (f"{MINUS}{2 * d} + {c}", None, -2 * d + c)]
            steps = [f"({MINUS}{d})² = ({MINUS}{d}) · ({MINUS}{d}) = {d * d}", f"{d * d} + {c} = {val}"]
            params = {"d": d, "c": c}
        elif k == 3:
            a, b = rng.choice([(3, 4), (2, 5), (4, 6)])
            level, ref, val = "H", f"{MINUS}{a}² + ({MINUS}{b})²", b * b - a * a
            eq = [f"{b}² {MINUS} {a}²", f"{MINUS}({a} · {a}) + ({MINUS}{b}) · ({MINUS}{b})", f"{num(b * b - a * a)}"]
            bad = [(f"{a}² + {b}²", TID, a * a + b * b), (f"{MINUS}{a}² {MINUS} {b}²", TID, -a * a - b * b),
                   (f"{a}² {MINUS} {b}²", None, a * a - b * b)]
            steps = [f"{MINUS}{a}² = {num(-a * a)}", f"({MINUS}{b})² = {b * b}", f"{num(-a * a)} + {b * b} = {num(val)}"]
            params = {"a": a, "b": b}
        else:
            a, c = rng.choice([(3, 20), (4, 30), (5, 40)])
            level, ref, val = "H", f"{c} {MINUS} {a}²", c - a * a
            ctx = (f"Pelissä pelaaja aloittaa {c} pisteellä ja menettää {a}² pistettä osuessaan miinaan. "
                   "Valitse kaikki lausekkeet, joiden arvo on pelaajan pisteet miinaan osumisen jälkeen. ")
            eq = [f"{c} {MINUS} ({a} · {a})", f"{c} {MINUS} ({MINUS}{a})²", f"{num(c - a * a)}"]
            bad = [(f"{c} + {a}²", TID, c + a * a), (f"{c} {MINUS} {2 * a}", None, c - 2 * a),
                   (f"({c} {MINUS} {a})²", None, (c - a) ** 2)]
            steps = [f"{a}² = {a * a}", f"{c} {MINUS} {a * a} = {val}"]
            params = {"a": a, "c": c}
        assert all(v != val for _, _, v in bad), "distractor equals reference"
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        prompt = ctx or f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref}."
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m, _ in bad]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": ["x"], "samples": [[1], [2], [3]], "options": options}
        items.append(base_item(TID, CODE, start + k, ["S2.01", "S2.11"], ["T10", "T11"], 7, level, prompt, payload,
                               steps, num(val), GOOD, TEMPLATE, params, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
