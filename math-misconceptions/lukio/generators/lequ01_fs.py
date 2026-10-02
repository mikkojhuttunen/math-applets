#!/usr/bin/env python3
"""LEQU-01 FS (lukio level): dividing by an expression that can be zero. The blanked line is the
factoring step; the answer is an equation checked against the solution set."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "lequ01_fs"
TID, CODE = "LEQU-01", "FS"
X, T = sp.symbols("x t", real=True)
GENERIC = "Yhtälön molempia puolia saa jakaa vain lausekkeella, joka ei voi olla nolla. Siirrä muuten kaikki yhdelle puolelle ja tekijöi."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, g, level, prompt, lines, blank, eq, v, equivalents, steps, params):
        s = sorted(sp.solveset(eq, v, sp.S.Reals), key=float)
        final = lines[blank - 1]
        ans = {"kind": "equation", "reference": final, "variable": str(v), "solutions": [int(a) for a in s]}
        if equivalents:
            ans["equivalents"] = equivalents
        sol = " tai ".join(f"{v} = {show(a)}" for a in s)
        items.append(base_item(TID, CODE, n, lops, [g], syll, level, "none", prompt,
                               {"lines": lines, "blank_index": blank, "answer": ans}, steps + [f"{sol}."], final,
                               "Oikein: tekijöihin jakaminen säilyttää myös ratkaisun, jossa tekijä on 0.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    add(start, ["MAA2.05"], "MAA", "G4", "T", "Täydennä puuttuva rivi: ota yhteinen tekijä x.",
        ["x² = 7x", "x² − 7x = 0", "x(x − 7) = 0"], 3, sp.Eq(X ** 2, 7 * X), X, [],
        ["Siirrä 7x vasemmalle: x² − 7x = 0.", "Ota x yhteiseksi tekijäksi: x(x − 7) = 0."], {"a": 7})
    add(start + 1, ["MAB2.04"], "MAB", "G4", "T", "Täydennä puuttuva rivi: ota yhteinen tekijä 3x.",
        ["3x² = 12x", "3x² − 12x = 0", "3x(x − 4) = 0"], 3, sp.Eq(3 * X ** 2, 12 * X), X, [],
        ["Siirrä 12x vasemmalle: 3x² − 12x = 0.", "Ota 3x yhteiseksi tekijäksi: 3x(x − 4) = 0."], {"c": 3, "b": 12})
    add(start + 2, ["MAA2.05"], "MAA", "G4", "H", "Täydennä puuttuva rivi: ota yhteinen tekijä x.",
        ["x³ = 16x", "x³ − 16x = 0", "x(x² − 16) = 0", "x(x − 4)(x + 4) = 0"], 3, sp.Eq(X ** 3, 16 * X), X, [],
        ["Siirrä 16x vasemmalle: x³ − 16x = 0.", "Ota x yhteiseksi tekijäksi: x(x² − 16) = 0.", "Tekijöi erotus: x(x − 4)(x + 4) = 0."], {"n": 3, "a": 16})
    add(start + 3, ["MAB2.04"], "MAB", "G4", "H", "Täydennä puuttuva rivi: ota x yhteiseksi tekijäksi ennen sieventämistä.",
        ["x(x + 2) = 3x", "x(x + 2) − 3x = 0", "x(x + 2 − 3) = 0", "x(x − 1) = 0"], 3, sp.Eq(X * (X + 2), 3 * X), X, [],
        ["Siirrä 3x vasemmalle: x(x + 2) − 3x = 0.", "Ota x yhteiseksi tekijäksi: x(x + 2 − 3) = 0.", "Sievennä: x(x − 1) = 0."], {"a": 2, "b": 3})
    add(start + 4, ["MAA2.05", "MAA2.04"], "MAA", "G3", "H",
        "Täydennä puuttuva rivi: ota yhteinen tekijä x − 3 jakamatta sillä.",
        ["(x − 3)(x + 2) = 4(x − 3)", "(x − 3)(x + 2) − 4(x − 3) = 0", "(x − 3)(x + 2 − 4) = 0", "(x − 3)(x − 2) = 0"], 3,
        sp.Eq((X - 3) * (X + 2), 4 * (X - 3)), X, [],
        ["Siirrä oikea puoli vasemmalle, koska x − 3 voi olla nolla.", "Ota x − 3 yhteiseksi tekijäksi: (x − 3)(x + 2 − 4) = 0.", "Sievennä: (x − 3)(x − 2) = 0."], {"a": 3, "b": 2, "c": 4})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
