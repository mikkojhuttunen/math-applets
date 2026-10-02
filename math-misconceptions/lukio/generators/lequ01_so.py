#!/usr/bin/env python3
"""LEQU-01 SO (lukio level): dividing by an expression that can be zero. The lines are ordered steps
that move everything to one side and factor instead of dividing; all lines are equivalent equations."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "lequ01_so"
TID, CODE = "LEQU-01", "SO"
X, T = sp.symbols("x t", real=True)
GENERIC = "Yhtälön molempia puolia saa jakaa vain lausekkeella, joka ei voi olla nolla. Siirrä muuten kaikki yhdelle puolelle ja tekijöi."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, g, level, prompt, lines, eq, v, steps, params):
        s = sorted(sp.solveset(eq, v, sp.S.Reals), key=float)
        final = " tai ".join(f"{v} = {show(a)}" for a in s)
        items.append(base_item(TID, CODE, n, lops, [g], syll, level, "none", prompt, {"lines": lines, "accept": "exact"},
                               steps + [f"{final}."], final, "Oikein: ensin toinen puoli nollaksi ja sitten tekijöihin, ei jakamista.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    add(start, ["MAA2.05"], "MAA", "G4", "T", "Järjestä rivit niin, että ne ratkaisevat yhtälön x² = 5x oikein ilman jakamista x:llä.",
        ["x² = 5x", "x² − 5x = 0", "x(x − 5) = 0"], sp.Eq(X ** 2, 5 * X), X,
        ["Siirrä 5x vasemmalle, jotta ratkaisu x = 0 ei katoa.", "Ota x yhteiseksi tekijäksi."], {"a": 5})
    add(start + 1, ["MAB2.04"], "MAB", "G4", "T", "Kappaleen korkeus on 2t² = 8t jollain hetkellä t. Järjestä rivit niin, että ne ratkaisevat yhtälön oikein ilman jakamista t:llä.",
        ["2t² = 8t", "2t² − 8t = 0", "2t(t − 4) = 0"], sp.Eq(2 * T ** 2, 8 * T), T,
        ["Siirrä 8t vasemmalle.", "Ota 2t yhteiseksi tekijäksi."], {"c": 2, "b": 8})
    add(start + 2, ["MAA2.05"], "MAA", "G4", "H", "Järjestä rivit niin, että ne ratkaisevat yhtälön x³ = 9x oikein ilman jakamista x:llä.",
        ["x³ = 9x", "x³ − 9x = 0", "x(x² − 9) = 0", "x(x − 3)(x + 3) = 0"], sp.Eq(X ** 3, 9 * X), X,
        ["Siirrä 9x vasemmalle.", "Ota x yhteiseksi tekijäksi.", "Tekijöi erotus x² − 9."], {"n": 3, "a": 9})
    add(start + 3, ["MAB2.04"], "MAB", "G4", "H", "Järjestä rivit niin, että ne ratkaisevat yhtälön x(x + 2) = 3x oikein ilman jakamista x:llä.",
        ["x(x + 2) = 3x", "x(x + 2) − 3x = 0", "x(x + 2 − 3) = 0", "x(x − 1) = 0"], sp.Eq(X * (X + 2), 3 * X), X,
        ["Siirrä 3x vasemmalle.", "Ota x yhteiseksi tekijäksi.", "Sievennä sulkeet."], {"a": 2, "b": 3})
    add(start + 4, ["MAA2.05", "MAA2.04"], "MAA", "G3", "H",
        "Yhtälössä (x − 2)(x + 1) = 5(x − 2) on tekijä x − 2 kummallakin puolella. Järjestä rivit niin, että ratkaisu ei jaa tekijällä x − 2.",
        ["(x − 2)(x + 1) = 5(x − 2)", "(x − 2)(x + 1) − 5(x − 2) = 0", "(x − 2)(x + 1 − 5) = 0", "(x − 2)(x − 4) = 0"],
        sp.Eq((X - 2) * (X + 1), 5 * (X - 2)), X,
        ["Siirrä oikea puoli vasemmalle, koska x − 2 voi olla nolla.", "Ota x − 2 yhteiseksi tekijäksi ja sievennä."], {"a": 2, "b": 1, "c": 5})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
