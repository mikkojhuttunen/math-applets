#!/usr/bin/env python3
"""LEQU-04 ES (lukio level): the square root is taken across a quadratic inequality (x^2 < a
gives x < sqrt(a)). The error line drops the absolute value; the lines before it are equivalent
to line 1 and the error line is not. Correct solution sets are computed with sympy."""
import sympy as sp

from gen_common import base_item, cli, frac

TEMPLATE = "lequ04_es"
TID, CODE = "LEQU-04", "ES"
X = sp.Symbol("x", real=True)
GENERIC = "Neliöjuuri ei säilytä epäyhtälöä näin: √(x²) = |x|. Ratkaise |x| < a tai siirrä kaikki vasemmalle ja tekijöi."


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

    def add(n, level, prompt, lines, err, rel, expect, steps, params):
        final = fmt(rel)
        assert final == expect, (final, expect)
        items.append(base_item(TID, CODE, n, ["MAA2.06"], ["G4"], "MAA", level, "none", prompt,
                               {"lines": lines, "error_line": err, "error_type": "root_across_inequality"},
                               steps + [f"Oikea ratkaisu: {final}."], final,
                               "Oikein: neliöjuuresta tulee itseisarvo, √(x²) = |x|.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    add(start, "T", "Oppilas ratkaisi epäyhtälön x² < 16 näin. Napauta rivi, jossa on virhe.",
        ["x² < 16", "√(x²) < √16", "x < 4"], 3, X ** 2 < 16, "−4 < x < 4",
        ["Rivi 2 on oikein, mutta √(x²) = |x|, ei x.", "Rivillä 3 itseisarvo on pudotettu. Esimerkiksi x = −5 toteuttaa rivin 3, mutta (−5)² = 25 > 16."], {"a": 16})
    add(start + 1, "T", "Oppilas ratkaisi epäyhtälön x² > 36 näin. Napauta rivi, jossa on virhe.",
        ["x² > 36", "x² − 36 > 0", "(x − 6)(x + 6) > 0", "x > 6"], 4, X ** 2 > 36, "x < −6 tai x > 6",
        ["Rivit 2 ja 3 ovat oikein. Tulo on positiivinen, kun tekijät ovat samanmerkkiset.", "Rivillä 4 toinen tapaus x < −6 puuttuu: x = −7 antaa 49 > 36."], {"a": 36})
    add(start + 2, "H", "Oppilas ratkaisi epäyhtälön (x + 1)² ≤ 9 näin. Napauta rivi, jossa on virhe.",
        ["(x + 1)² ≤ 9", "|x + 1| ≤ 3", "x + 1 ≤ 3", "x ≤ 2"], 3, (X + 1) ** 2 <= 9, "−4 ≤ x ≤ 2",
        ["Rivi 2 on oikein: √((x + 1)²) = |x + 1|.", "Rivillä 3 itseisarvo on pudotettu; oikein −3 ≤ x + 1 ≤ 3."], {"shift": 1, "a": 9})
    add(start + 3, "H", "Oppilas ratkaisi epäyhtälön 4x² < 25 näin. Napauta rivi, jossa on virhe. Vihje: sijoita x = −3 alkuperäiseen epäyhtälöön ja riviin 3.",
        ["4x² < 25", "x² < 25/4", "x < 5/2"], 3, 4 * X ** 2 < 25, "−5/2 < x < 5/2",
        ["Rivi 2 on oikein: jaetaan 4:llä.", "Rivillä 3 on otettu neliöjuuri ilman itseisarvoa.",
         "Tarkistus: x = −3 toteuttaa rivin 3, mutta 4 · 9 = 36 > 25."], {"c": 4, "a": 25})
    add(start + 4, "H", "Oppilas ratkaisi epäyhtälön x² + 2 > 11 näin. Napauta rivi, jossa on virhe.",
        ["x² + 2 > 11", "x² > 9", "x > 3"], 3, X ** 2 + 2 > 11, "x < −3 tai x > 3",
        ["Rivi 2 on oikein: vähennetään 2.", "Rivillä 3 ratkaisu x < −3 puuttuu: x = −4 antaa 18 > 11."], {"c": 2, "a": 11})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
