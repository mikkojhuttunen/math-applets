#!/usr/bin/env python3
"""LEQU-05 MC (lukio level): absolute value read as "drop the minus sign". Correct options are
computed with sympy; distractors carry misconception tags."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "lequ05_mc"
TID, CODE = "LEQU-05", "MC"
X = sp.Symbol("x", real=True)
GENERIC = "Itseisarvo |a| on luvun a etäisyys nollasta. Yhtälö |f(x)| = a tarkoittaa f(x) = a tai f(x) = −a (kun a ≥ 0)."


def roots(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def txt(rs):
    return " tai ".join(f"x = {num(r)}" for r in rs) if rs else "ei ratkaisua"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1205)
    items = []

    def add(n, level, prompt, correct, wrongs, steps, final, params, lops=None):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops or ["MAA4.06"], ["G4"], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: |x - 3| = 5
    r = roots(sp.Eq(sp.Abs(X - 3), 5))
    assert [int(a) for a in r] == [-2, 8]
    add(start, "T", "Ratkaise yhtälö |x − 3| = 5.",
        (txt(r), "Oikein: x − 3 = 5 tai x − 3 = −5."),
        [(txt([r[1]]), TID, "Itseisarvo ei vain poista miinusmerkkiä: myös x − 3 = −5 toteuttaa yhtälön, koska |−5| = 5."),
         (txt([-r[1], -r[0]]), None, "Tarkista sijoittamalla: |2 − 3| = 1, ei 5."),
         (txt([r[1], 2]), None, "x = 2 antaa |2 − 3| = 1, ei 5. Negatiivinen tapaus on x − 3 = −5.")],
        ["x − 3 = 5, joten x = 8.", "x − 3 = −5, joten x = −2."], txt(r), {"a": 3, "b": 5})
    # 2: |x| = -4
    assert roots(sp.Eq(sp.Abs(X), -4)) == []
    add(start + 1, "T", "Kuinka monta ratkaisua yhtälöllä |x| = −4 on?",
        ("Ei yhtään, koska itseisarvo ei ole koskaan negatiivinen.", "Oikein."),
        [("Yksi: x = 4, koska itseisarvo poistaa miinusmerkin.", TID, "Itseisarvo |x| on aina ≥ 0, joten se ei voi olla −4. Sijoita x = 4: |4| = 4, ei −4."),
         ("Kaksi: x = 4 ja x = −4.", TID, "Sijoita: |4| = 4 ja |−4| = 4, kumpikaan ei ole −4."),
         ("Yksi: x = −4.", None, "Sijoita: |−4| = 4, ei −4.")],
        ["|x| ≥ 0 kaikilla x.", "Negatiivinen oikea puoli −4 ei voi olla itseisarvo."], "Ei yhtään ratkaisua", {"a": -4})
    # 3: |2x - 1| = 7
    r = roots(sp.Eq(sp.Abs(2 * X - 1), 7))
    assert [int(a) for a in r] == [-3, 4]
    add(start + 2, "H", "Ratkaise yhtälö |2x − 1| = 7.",
        (txt(r), "Oikein: 2x − 1 = 7 tai 2x − 1 = −7."),
        [(txt([r[1]]), TID, "Myös 2x − 1 = −7 on mahdollinen: x = −3, ja |2 · (−3) − 1| = 7."),
         (txt([-r[1], -r[0]]), None, "Sijoita x = −4: |2 · (−4) − 1| = 9, ei 7."),
         (txt([r[1], 3]), None, "x = 3 antaa |5| = 5, ei 7. Negatiivinen tapaus 2x − 1 = −7 antaa x = −3.")],
        ["2x − 1 = 7, joten x = 4.", "2x − 1 = −7, joten x = −3."], txt(r), {"a": 2, "b": -1, "c": 7})
    # 4: |x| = -x holds exactly for x <= 0
    s = sp.solveset(sp.Eq(sp.Abs(X), -X), X, sp.S.Reals)
    assert s == sp.Interval(-sp.oo, 0)
    add(start + 3, "H", "Milloin yhtälö |x| = −x pätee? Perustele valintasi.",
        ("Kun x ≤ 0, koska silloin −x ≥ 0 on x:n vastaluku ja sama kuin |x|.", "Oikein: esimerkiksi |−3| = 3 = −(−3)."),
        [("Ei koskaan, koska itseisarvo poistaa miinusmerkin eikä siis voi olla −x.", TID, "|−3| = 3 ja −(−3) = 3, joten yhtälö pätee, kun x on negatiivinen."),
         ("Kun x ≥ 0, koska silloin |x| = x.", None, "Kun x > 0, −x on negatiivinen ja |x| positiivinen. Yhtälö pätee vain x = 0 tässä joukossa."),
         ("Kun x < 0, mutta ei kun x = 0.", None, "Myös x = 0 toteuttaa yhtälön: |0| = 0 = −0.")],
        ["Jos x ≥ 0, |x| = x, ja yhtälö x = −x antaa x = 0.", "Jos x < 0, |x| = −x aina.", "Siis yhtälö pätee, kun x ≤ 0."],
        "x ≤ 0", {}, lops=["MAA4.06", "MAY1.02"])
    # 5: |x - 2| = |x + 4|
    r = roots(sp.Eq(sp.Abs(X - 2), sp.Abs(X + 4)))
    assert r == [-1]
    add(start + 4, "H", "Ratkaise yhtälö |x − 2| = |x + 4|.",
        (txt(r), "Oikein: x − 2 = −(x + 4) antaa x = −1."),
        [("Ei ratkaisua, koska x − 2 = x + 4 on mahdoton.", TID, "Itseisarvot ovat yhtä suuret myös, kun lausekkeet ovat toistensa vastalukuja: x − 2 = −(x + 4)."),
         ("x = 3", None, "Sijoita: |3 − 2| = 1, mutta |3 + 4| = 7."),
         ("x = 1", None, "Sijoita: |1 − 2| = 1, mutta |1 + 4| = 5.")],
        ["x − 2 = x + 4 on mahdoton.", "x − 2 = −(x + 4), joten 2x = −2 ja x = −1."], txt(r), {"a": -2, "b": 4})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
