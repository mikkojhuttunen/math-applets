#!/usr/bin/env python3
"""EXT-04 ES (lukio level): x^2 = a gives only the positive root. Each worked solution drops the
negative root on its last line; the verifier checks that the error line is not equivalent to the line before."""
import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "ext04_es"
TID, CODE = "EXT-04", "ES"
X = sp.Symbol("x", real=True)
GENERIC = "Yhtälöllä x² = a on kaksi ratkaisua, kun a > 0: x = √a ja x = −√a. Tarkista sijoittamalla."


def roots(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, lines, err, steps, final, params, fb="Oikein: myös vastaluku toteuttaa yhtälön."):
        items.append(base_item(TID, CODE, n, lops, ["G4"], syll, level, "none", prompt,
                               {"lines": lines, "error_line": err, "error_type": "positive_root_only"}, steps, final, fb,
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    r = roots(sp.Eq(X ** 2, 81))
    assert r == [-9, 9]
    add(start, ["MAA2.04"], "MAA", "T", "Oppilas ratkaisi yhtälön x² = 81 näin. Napauta rivi, jossa on virhe.",
        ["x² = 81", "x² − 81 = 0", "(x − 9)(x + 9) = 0", "x − 9 = 0"], 4,
        ["Rivillä 4 on jäänyt pois tekijä x + 9, josta saadaan ratkaisu x = −9.", "Oikein: x = 9 tai x = −9."], "x = 9 tai x = −9", {"a": 81})
    r = roots(sp.Eq(X ** 2 - 9, 0))
    assert r == [-3, 3]
    add(start + 1, ["MAB2.04"], "MAB", "T", "Oppilas etsi paraabelin y = x² − 9 nollakohdat näin. Napauta rivi, jossa on virhe.",
        ["x² − 9 = 0", "x² = 9", "x = 3"], 3,
        ["Rivillä 3 on otettu vain positiivinen neliöjuuri. Myös (−3)² = 9.", "Oikein: paraabeli leikkaa x-akselin kohdissa x = −3 ja x = 3."], "x = −3 tai x = 3", {"c": -9})
    r = roots(sp.Eq((X - 2) ** 2, 9))
    assert r == [-1, 5]
    add(start + 2, ["MAA2.04"], "MAA", "H", "Oppilas ratkaisi yhtälön (x − 2)² = 9 näin. Napauta rivi, jossa on virhe.",
        ["(x − 2)² = 9", "x − 2 = 3", "x = 5"], 2,
        ["Rivillä 2 on otettu vain positiivinen neliöjuuri: myös x − 2 = −3 toteuttaa yhtälön.", "Oikein: x = 5 tai x = −1."], "x = 5 tai x = −1", {"shift": 2, "a": 9})
    r = roots(sp.Eq(2 * X ** 2, 50))
    assert r == [-5, 5]
    add(start + 3, ["MAB2.04"], "MAB", "H", "Kuvaajan y = 2x² pisteet, joissa y = 50, löytyy ratkaisemalla yhtälö 2x² = 50. Oppilas ratkaisi sen näin. Napauta rivi, jossa on virhe.",
        ["2x² = 50", "x² = 25", "x = 5"], 3,
        ["Rivillä 3 on otettu vain positiivinen neliöjuuri. Kuvaajalla on kaksi pistettä, joiden y-koordinaatti on 50.", "Oikein: x = 5 tai x = −5."], "x = 5 tai x = −5", {"c": 2, "a": 50})
    r = roots(sp.Eq(X ** 2 + 5, 30))
    assert r == [-5, 5]
    add(start + 4, ["MAA2.04"], "MAA", "H", "Oppilas ratkaisi yhtälön x² + 5 = 30 näin. Napauta rivi, jossa on virhe. Vihje: sijoita x = −5 alkuperäiseen yhtälöön.",
        ["x² + 5 = 30", "x² = 25", "x = 5"], 3,
        ["Rivillä 3 on otettu vain positiivinen neliöjuuri.", "Tarkistus: (−5)² + 5 = 30, joten myös x = −5 on ratkaisu."], "x = 5 tai x = −5", {"c": 5, "a": 30},
        "Oikein: sijoitus x = −5 antaa 25 + 5 = 30, joten −5 on myös ratkaisu.")
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
