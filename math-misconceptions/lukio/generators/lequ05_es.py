#!/usr/bin/env python3
"""LEQU-05 ES (lukio level): absolute value read as "drop the minus sign". Each item shows a
worked solution of an absolute value equation where the error line keeps only one case. The
lines before the error line are equivalent to line 1 and the error line is not (verifier
checks this with sympy); the roots in the solution steps are computed with sympy."""
import sympy as sp

from gen_common import base_item, cli, num

TEMPLATE = "lequ05_es"
TID, CODE = "LEQU-05", "ES"
X = sp.Symbol("x", real=True)
GENERIC = "Itseisarvo |a| on luvun a etäisyys nollasta. Yhtälö |f(x)| = a tarkoittaa f(x) = a tai f(x) = −a (kun a ≥ 0). Tarkista sijoittamalla."


def roots(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def txt(rs):
    return " tai ".join(f"x = {num(r)}" for r in rs) if rs else "ei ratkaisua"


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, level, prompt, lines, err, eq, steps, params):
        rs = roots(eq)
        final = txt(rs)
        items.append(base_item(TID, CODE, n, ["MAA4.06"], ["G4"], "MAA", level, "none", prompt,
                               {"lines": lines, "error_line": err, "error_type": "negative_case_dropped"},
                               steps + [f"Oikea ratkaisu: {final}."], final,
                               "Oikein: itseisarvoyhtälöllä on kaksi tapausta, positiivinen ja negatiivinen.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: |x - 3| = 5
    add(start, "T", "Oppilas ratkaisi yhtälön |x − 3| = 5 näin. Napauta rivi, jossa on virhe.",
        ["|x − 3| = 5", "x − 3 = 5", "x = 8"], 2, sp.Eq(sp.Abs(X - 3), 5),
        ["Rivillä 2 on otettu vain positiivinen tapaus x − 3 = 5.", "Myös x − 3 = −5 toteuttaa yhtälön, koska |−5| = 5."], {"a": 3, "b": 5})
    # 2: |x + 4| - 2 = 4
    add(start + 1, "T", "Oppilas ratkaisi yhtälön |x + 4| − 2 = 4 näin. Napauta rivi, jossa on virhe.",
        ["|x + 4| − 2 = 4", "|x + 4| = 6", "x + 4 = 6", "x = 2"], 3, sp.Eq(sp.Abs(X + 4) - 2, 4),
        ["Rivi 2 on oikein: lisätään 2 molemmille puolille.", "Rivillä 3 negatiivinen tapaus x + 4 = −6 on jäänyt pois."], {"a": 4, "c": 2, "d": 4})
    # 3: |x - 1| = |x + 5|, only same-sign case
    add(start + 2, "H", "Oppilas ratkaisi yhtälön |x − 1| = |x + 5| näin. Napauta rivi, jossa on virhe.",
        ["|x − 1| = |x + 5|", "x − 1 = x + 5", "−1 = 5", "ei ratkaisua"], 2, sp.Eq(sp.Abs(X - 1), sp.Abs(X + 5)),
        ["Rivillä 2 on otettu vain tapaus, jossa lausekkeet ovat yhtä suuret.", "Itseisarvot ovat yhtä suuret myös, kun lausekkeet ovat vastaluvut: x − 1 = −(x + 5)."], {"a": -1, "b": 5})
    # 4: |3x + 3| = 6, hint
    add(start + 3, "H", "Oppilas ratkaisi yhtälön |3x + 3| = 6 näin. Napauta rivi, jossa on virhe. Vihje: sijoita x = −3 alkuperäiseen yhtälöön.",
        ["|3x + 3| = 6", "|x + 1| = 2", "x + 1 = 2", "x = 1"], 3, sp.Eq(sp.Abs(3 * X + 3), 6),
        ["Rivi 2 on oikein: jaetaan 3:lla.", "Rivillä 3 on vain positiivinen tapaus.", "Tarkistus: x = −3 antaa |3 · (−3) + 3| = |−6| = 6, joten se on ratkaisu."], {"a": 3, "b": 3, "c": 6})
    # 5: |x - 4| + 5 = 2, no solutions; plausibility
    add(start + 4, "H", "Oppilas ratkaisi yhtälön |x − 4| + 5 = 2 näin. Napauta rivi, jossa on virhe. Vihje: voiko itseisarvo olla negatiivinen?",
        ["|x − 4| + 5 = 2", "|x − 4| = −3", "x − 4 = −3", "x = 1"], 3, sp.Eq(sp.Abs(X - 4) + 5, 2),
        ["Rivi 2 on oikein: vähennetään 5.", "Rivillä 3 itseisarvo on poistettu, vaikka sen arvo ei voi olla −3.",
         "Tarkistus: x = 1 antaa |1 − 4| + 5 = 8, ei 2."], {"a": -4, "c": 5, "d": 2})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
