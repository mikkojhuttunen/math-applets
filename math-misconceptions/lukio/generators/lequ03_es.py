#!/usr/bin/env python3
"""LEQU-03 ES (lukio level): an inequality is multiplied by an expression of unknown sign. The
error line multiplies (or drops the denominator) as if it were positive; the verifier checks that
the lines before it are equivalent to line 1 and the error line is not. Correct solution sets
are computed with sympy."""
import sympy as sp

from gen_common import base_item, cli, frac

TEMPLATE = "lequ03_es"
TID, CODE = "LEQU-03", "ES"
X = sp.Symbol("x", real=True)
GENERIC = "Epäyhtälön saa kertoa puolittain vain lausekkeella, jonka merkki tiedetään. Siirrä kaikki vasemmalle, sievennä yhdeksi murtolausekkeeksi ja tutki merkit."


def fmt(rel):
    """Solution set of an inequality in x as Finnish text."""
    s = sp.solve_univariate_inequality(rel, X, relational=False)
    parts = list(s.args) if isinstance(s, sp.Union) else [s]
    parts.sort(key=lambda p: float(p.inf) if p.inf != -sp.oo else -1e18)
    out = []
    for p in parts:
        lo, hi = p.inf, p.sup
        if lo == -sp.oo:
            out.append(f"x {'≤' if not p.right_open else '<'} {frac(hi)}")
        elif hi == sp.oo:
            out.append(f"x {'≥' if not p.left_open else '>'} {frac(lo)}")
        else:
            out.append(f"{frac(lo)} {'<' if p.left_open else '≤'} x {'<' if p.right_open else '≤'} {frac(hi)}")
    return " tai ".join(out)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, g, level, prompt, lines, err, rel, expect, steps, params):
        final = fmt(rel)
        assert final == expect, (final, expect)
        items.append(base_item(TID, CODE, n, ["MAA2.06", "MAA2.07"], [g], "MAA", level, "none", prompt,
                               {"lines": lines, "error_line": err, "error_type": "multiply_unknown_sign"},
                               steps + [f"Oikea ratkaisu: {final}."], final,
                               "Oikein: kertominen on sallittu vain, kun tekijän merkki tiedetään.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    add(start, "G4", "T", "Oppilas ratkaisi epäyhtälön 3/x < 1 näin. Napauta rivi, jossa on virhe.",
        ["3/x < 1", "3 < x", "x > 3"], 2, 3 / X < 1, "x < 0 tai x > 3",
        ["Rivillä 2 on kerrottu x:llä, vaikka x:n merkkiä ei tiedetä. Jos x < 0, suunta kääntyy.",
         "Esimerkiksi x = −1 toteuttaa alkuperäisen epäyhtälön (3/(−1) = −3 < 1), mutta ei riviä 3."], {"a": 3, "b": 1})
    add(start + 1, "G4", "T", "Oppilas ratkaisi epäyhtälön 4/(x − 2) > 1 näin. Napauta rivi, jossa on virhe.",
        ["4/(x − 2) > 1", "4 > x − 2", "x < 6"], 2, 4 / (X - 2) > 1, "2 < x < 6",
        ["Rivillä 2 on kerrottu lausekkeella x − 2, joka voi olla negatiivinen.",
         "Kerto on sallittu vain, kun x − 2 > 0, eli x > 2; silloin saadaan 2 < x < 6."], {"a": 4, "b": 2, "c": 1})
    add(start + 2, "G4", "H", "Oppilas ratkaisi epäyhtälön 1/x > −2 näin. Napauta rivi, jossa on virhe. Vihje: sijoita x = −1 alkuperäiseen epäyhtälöön ja riviin 3.",
        ["1/x > −2", "1 > −2x", "x > −1/2"], 2, 1 / X > -2, "x < −1/2 tai x > 0",
        ["Rivillä 2 on kerrottu x:llä oletuksella x > 0.",
         "Tarkistus: x = −1 antaa 1/(−1) = −1 > −2, joten x = −1 on ratkaisu, mutta −1 > −1/2 on epätosi."], {"a": 1, "b": -2})
    add(start + 3, "G3", "H", "Oppilas ratkaisi epäyhtälön (x + 1)/x < 2 näin. Napauta rivi, jossa on virhe.",
        ["(x + 1)/x < 2", "(1 − x)/x < 0", "x + 1 < 2x", "x > 1"], 3, (X + 1) / X < 2, "x < 0 tai x > 1",
        ["Rivi 2 on oikein: (x + 1)/x − 2 = (1 − x)/x.",
         "Rivillä 3 kerrotaan x:llä ilman tietoa sen merkistä. Murtoluku on negatiivinen myös, kun x < 0 ja 1 − x > 0."], {"a": 1, "b": 1, "c": 2})
    add(start + 4, "G4", "H", "Oppilas ratkaisi epäyhtälön 3/(x + 2) < 1 näin. Napauta rivi, jossa on virhe.",
        ["3/(x + 2) < 1", "(1 − x)/(x + 2) < 0", "1 − x < 0", "x > 1"], 3, 3 / (X + 2) < 1, "x < −2 tai x > 1",
        ["Rivi 2 on oikein: 3/(x + 2) − 1 = (1 − x)/(x + 2).",
         "Rivillä 3 nimittäjä on jätetty pois, vaikka murtoluku on negatiivinen myös, kun x + 2 < 0 ja 1 − x > 0.",
         "Tarkistus: x = −3 antaa 3/(−1) = −3 < 1, mutta −3 > 1 on epätosi."], {"a": 3, "b": 2, "c": 1})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
