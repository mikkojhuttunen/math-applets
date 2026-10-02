#!/usr/bin/env python3
"""LVEC-01 RP: the length of a sum of vectors is not the sum of lengths.
The pupil writes an equation for s = |a + b|^2 whose only solution is the true value.
The true value is computed with sympy from the vector data; the invalid examples are the
misreading |a + b| = |a| + |b| (squared) and the plain sum of lengths."""
import random

import sympy as sp

from gen_common import base_item, cli, num

TEMPLATE = "lvec01_rp"
TID, CODE = "LVEC-01", "RP"
GENERIC = "Vektorien summan pituus ei yleensä ole pituuksien summa. Laske summavektorin komponenteista tai käytä pistetuloa."


def payload(var, value, valid, invalid):
    return {"constraint": {"type": "solution_equals", "variable": var, "value": int(value)},
            "checks": {"valid": valid, "invalid": invalid}}


def make_items(run, date, count=5, start=1):
    rng = random.Random(4101)
    items = []

    # 1 perpendicular, lengths given
    p, q = rng.choice([(3, 4), (5, 12)])
    v = p * p + q * q
    items.append(base_item(
        TID, CODE, start, ["MAA4.07"], ["G2"], "MAA", "P", "none",
        f"Vektorit a ja b ovat kohtisuorassa, |a| = {p} ja |b| = {q}. Merkitään s = |a + b|². Kirjoita yhtälö, jonka ainoa ratkaisu on s:n oikea arvo.",
        payload("s", v, [f"s = {p}^2 + {q}^2", f"s − {p * p} = {q * q}"], [f"s = ({p} + {q})^2", f"s = {p} + {q}"]),
        [f"Kohtisuorassa olevien vektorien summalle pätee Pythagoras: |a + b|² = |a|² + |b|² = {p * p} + {q * q} = {v}."],
        f"esim. s = {p}² + {q}² (s = {v})", "Oikein: kohtisuorilla vektoreilla pituuksien neliöt lasketaan yhteen.", TEMPLATE,
        {"p": p, "q": q}, date, run, generic_wrong=GENERIC))

    # 2 context: walking east and north, d = squared distance
    e_, n_ = 6, 8
    v = e_**2 + n_**2
    items.append(base_item(
        TID, CODE, start + 1, ["MAA4.07"], ["G4"], "MAA", "T", "none",
        f"Robotti ajaa {e_} m itään ja sitten {n_} m pohjoiseen. Merkitään d = (etäisyys lähtöpisteestä)². Kirjoita yhtälö, jonka ainoa ratkaisu on d:n oikea arvo.",
        payload("d", v, [f"d = {e_}^2 + {n_}^2", f"d = {v}"], [f"d = ({e_} + {n_})^2", f"d = {e_} + {n_}"]),
        [f"Siirtymät ovat kohtisuorassa: d = {e_}² + {n_}² = {v}.", f"Etäisyys on √{v} = {int(sp.sqrt(v))} m, ei {e_ + n_} m."],
        f"esim. d = {e_}² + {n_}² (d = {v})", "Oikein: etäisyys on pituuksien summaa lyhyempi, koska suunta muuttuu.", TEMPLATE,
        {"east": e_, "north": n_}, date, run, generic_wrong=GENERIC))

    # 3 components, perpendicular check by dot product
    a, b = sp.Matrix([1, 2]), sp.Matrix([2, -1])
    assert a.dot(b) == 0
    s = a + b
    v = s.dot(s)
    la, lb = a.dot(a), b.dot(b)
    items.append(base_item(
        TID, CODE, start + 2, ["MAA4.07"], ["G2"], "MAA", "T", "none",
        "Vektorit a = (1, 2) ja b = (2, −1). Merkitään w = |a + b|². Kirjoita yhtälö, jonka ainoa ratkaisu on w:n oikea arvo.",
        payload("w", v, [f"w = {s[0]}^2 + {s[1]}^2", f"w = {la} + {lb}"], [f"w = (sqrt({la}) + sqrt({lb}))^2", f"w = 2*sqrt({la})"]),
        [f"a + b = ({s[0]}, {s[1]}), joten |a + b|² = {s[0]}² + {s[1]}² = {v}.",
         f"Pituuksien summan neliö olisi (√{la} + √{lb})² = {sp.expand((sp.sqrt(la) + sp.sqrt(lb)) ** 2)}, eli eri luku."],
        f"esim. w = {s[0]}² + {s[1]}² (w = {v})", "Oikein: lasketaan summavektorin komponenteista.", TEMPLATE,
        {"a": [1, 2], "b": [2, -1]}, date, run, generic_wrong=GENERIC))

    # 4 angle 60 degrees
    p, q = 3, 5
    c = sp.cos(sp.pi / 3)
    v = p * p + q * q + 2 * p * q * c
    assert v == 49
    items.append(base_item(
        TID, CODE, start + 3, ["MAA4.07", "MAA4.08"], ["G4"], "MAA", "H", "none",
        f"Vektorien a ja b välinen kulma on 60°, |a| = {p} ja |b| = {q}. Merkitään s = |a + b|². Kirjoita yhtälö, jonka ainoa ratkaisu on s:n oikea arvo.",
        payload("s", v, [f"s = {p}^2 + {q}^2 + 2*{p}*{q}*cos(pi/3)", f"s = {int(v)}"], [f"s = ({p} + {q})^2", f"s = {p}^2 + {q}^2"]),
        [f"|a + b|² = |a|² + |b|² + 2 a·b, ja a·b = {p}·{q}·cos 60° = {sp.Rational(p * q, 2)}.", f"Siis s = {p * p} + {q * q} + {p * q} = {int(v)}, ja |a + b| = 7."],
        f"esim. s = {p}² + {q}² + 2·{p}·{q}·cos 60° (s = {int(v)})", "Oikein: kulma otetaan huomioon pistetulon kautta. Pituus 7 on pienempi kuin 3 + 5 = 8.", TEMPLATE,
        {"p": p, "q": q, "angle_deg": 60}, date, run, generic_wrong=GENERIC))

    # 5 opposite vectors
    a, b = sp.Matrix([3, 4]), sp.Matrix([-3, -4])
    s = a + b
    v = s.dot(s)
    assert v == 0
    items.append(base_item(
        TID, CODE, start + 4, ["MAA4.07"], ["G2"], "MAA", "H", "none",
        "Vektorit a = (3, 4) ja b = (−3, −4). Merkitään t = |a + b|². Kirjoita yhtälö, jonka ainoa ratkaisu on t:n oikea arvo, ja mieti, miksi tulos on järkevä.",
        payload("t", v, ["t = (3 − 3)^2 + (4 − 4)^2", "t = 0"], ["t = (5 + 5)^2", "t = 5 + 5"]),
        ["Summavektori on (3 − 3, 4 − 4) = (0, 0), joten t = 0.", "Vektorit ovat vastakkaiset ja yhtä pitkät, joten ne kumoavat toisensa; pituuksien summa 5 + 5 = 10 ei kerro mitään summavektorin pituudesta."],
        "esim. t = (3 − 3)² + (4 − 4)² (t = 0)", "Oikein: vastakkaiset vektorit kumoavat toisensa, summan pituus on 0.", TEMPLATE,
        {"a": [3, 4], "b": [-3, -4]}, date, run, generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
