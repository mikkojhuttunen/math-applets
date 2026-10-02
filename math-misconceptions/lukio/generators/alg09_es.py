#!/usr/bin/env python3
"""ALG-09 ES (lukio level): square of a sum. Each item shows a worked solution with one line where the
middle term of a binomial square is dropped. Lines are checked by the verifier (all lines before the
error line equivalent, the error line not)."""
import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "alg09_es"
TID, CODE = "ALG-09", "ES"
X = sp.Symbol("x")
GENERIC = "(a + b)² on (a + b)(a + b), ja siinä on myös keskimmäinen tulo 2ab. Kokeile lukuarvoilla, esim. a = 1, b = 1."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, lines, err, etype, steps, final, params, fb="Oikein: binomin neliössä on aina keskimmäinen tulo."):
        items.append(base_item(TID, CODE, n, lops, ["G2"], syll, level, "none", prompt,
                               {"lines": lines, "error_line": err, "error_type": etype}, steps, final, fb,
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1 (MAB): yard with side x + 3, area 49
    a, area = 3, 49
    side = sp.sqrt(area)
    assert sp.solveset(sp.Eq((X + a) ** 2, area), X, sp.S.Reals) == sp.FiniteSet(-10, 4)
    add(start, ["MAB2.07"], "MAB", "P",
        f"Neliön muotoisen pihan sivu on x + {a} metriä ja pinta-ala {area} m². Oppilas ratkaisi x:n näin. Napauta rivi, jossa on virhe.",
        [f"(x + {a})² = {area}", f"x² + {a * a} = {area}", f"x² = {area - a * a}", f"x = √{area - a * a}"], 2, "square_of_sum_split",
        [f"Rivillä 2 summan (x + {a}) neliö on laskettu termeittäin: (x + {a})² ≠ x² + {a * a}.",
         f"Oikein: sivu on √{area} = {side}, joten x + {a} = {side} ja x = {side - a}."], f"x = {side - a}", {"a": a, "area": area})
    # 2 (MAA): ((2x + 6)/2)^2 - 9
    e = sp.expand(((2 * X + 6) / 2) ** 2 - 9)
    assert e == X**2 + 6 * X
    add(start + 1, ["MAA2.01"], "MAA", "T", "Oppilas sieventi lausekkeen ((2x + 6)/2)² − 9 näin. Napauta rivi, jossa on virhe.",
        ["((2x + 6)/2)² − 9", "(x + 3)² − 9", "x² + 9 − 9", "x²"], 3, "square_of_sum_split",
        ["Rivi 2 on oikein: (2x + 6)/2 = x + 3.", "Rivillä 3 puuttuu keskimmäinen tulo 2 · x · 3 = 6x.", "Oikein: (x + 3)² − 9 = x² + 6x + 9 − 9 = x² + 6x."],
        "x² + 6x", {"inner": "(2x+6)/2", "sub": 9})
    # 3 (MAA): 98^2 by (100 - 2)^2
    right, wrong = (100 - 2) ** 2, 100**2 - 2**2
    assert right == 9604 and wrong == 9996
    add(start + 2, ["MAA2.01"], "MAA", "T", "Oppilas laski 98² päässä näin. Napauta rivi, jossa on virhe.",
        ["98²", "(100 − 2)²", "100² − 2²", "9996"], 3, "square_of_difference_split",
        ["Rivillä 3 erotuksen neliö on laskettu termeittäin; keskimmäinen tulo −2 · 100 · 2 = −400 puuttuu.", "Oikein: 10000 − 400 + 4 = 9604."],
        str(right), {"n": 98}, "Oikein: erotuksen neliössä on keskimmäinen tulo. Tulos 9996 olisi lähes 100², vaikka 98 < 100.")
    # 4 (MAB): two years of 5 % growth
    r = sp.Rational(5, 100)
    assert (1 + r) ** 2 != 1 + r**2
    add(start + 3, ["MAB2.07"], "MAB", "T",
        "Hinta nousee kaksi vuotta peräkkäin 5 % vuodessa. Oppilas laski kokonaiskertoimen näin. Napauta rivi, jossa on virhe.",
        ["(1 + 0,05)²", "1² + 0,05²", "1,0025"], 2, "square_of_sum_split",
        ["Rivillä 2 summan (1 + 0,05) neliö on laskettu termeittäin; keskimmäinen tulo 2 · 0,05 = 0,1 puuttuu.", "Oikein: 1 + 0,1 + 0,0025 = 1,1025, eli hinta nousee 10,25 %."],
        "1,1025", {"rate": "5/100", "years": 2}, "Oikein: kasvukerroin on 1,05² = 1,1025.")
    # 5 (MAA): equation, hint to substitute
    assert sp.solveset(sp.Eq((X + 2) ** 2, X**2 + 20), X, sp.S.Reals) == sp.FiniteSet(4)
    add(start + 4, ["MAA2.01"], "MAA", "H",
        "Oppilas ratkaisi yhtälön (x + 2)² = x² + 20 näin. Napauta rivi, jossa on virhe. Vihje: sijoita x = 4 alkuperäiseen yhtälöön.",
        ["(x + 2)² = x² + 20", "x² + 4 = x² + 20", "4 = 20", "ei ratkaisua"], 2, "square_of_sum_split",
        ["Rivillä 2 puuttuu keskimmäinen tulo 4x.", "Oikein: x² + 4x + 4 = x² + 20, joten 4x = 16 ja x = 4. Tarkistus: 6² = 36 ja 4² + 20 = 36."],
        "x = 4", {"yhtalo": "(x+2)^2=x^2+20"}, "Oikein: sijoitus x = 4 antaa molemmille puolille 36, joten yhtälöllä on ratkaisu.")
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
