#!/usr/bin/env python3
"""LEQU-02 FS (lukio level): zero-product rule. The blanked line is the step that makes the right side
0 (or factors the result); the answer is an equation checked against the solution set."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "lequ02_fs"
TID, CODE = "LEQU-02", "FS"
X = sp.Symbol("x", real=True)
GENERIC = "Tulon nollasääntöä voi käyttää vasta, kun toisella puolella on 0. Siirrä ensin kaikki vasemmalle ja tekijöi."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, g, level, prompt, lines, blank, eq, steps, params):
        s = sorted(sp.solveset(eq, X, sp.S.Reals), key=float)
        final = lines[blank - 1]
        ans = {"kind": "equation", "reference": final, "variable": "x", "solutions": [int(a) for a in s]}
        sol = " tai ".join(f"x = {show(a)}" for a in s)
        items.append(base_item(TID, CODE, n, ["MAA2.05"], [g], "MAA", level, "none", prompt,
                               {"lines": lines, "blank_index": blank, "answer": ans}, steps + [f"{sol}."], final,
                               "Oikein: nyt toisella puolella on 0 ja tulon nollasääntöä voi käyttää.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    add(start, "G4", "T", "Täydennä puuttuva rivi: siirrä oikea puoli vasemmalle, jotta tulo voidaan tulkita nollaksi.",
        ["(x − 5)(x + 1) = 7", "x² − 4x − 5 = 7", "x² − 4x − 12 = 0", "(x − 6)(x + 2) = 0"], 3,
        sp.Eq((X - 5) * (X + 1), 7), ["Kerro auki: x² − 4x − 5 = 7.", "Siirrä 7 vasemmalle: x² − 4x − 12 = 0."], {"a": -5, "b": 1, "k": 7})
    add(start + 1, "G4", "T", "Täydennä puuttuva rivi: tekijöi vasen puoli.",
        ["x(x + 2) = 8", "x² + 2x = 8", "x² + 2x − 8 = 0", "(x + 4)(x − 2) = 0"], 4,
        sp.Eq(X * (X + 2), 8), ["Kerro auki ja siirrä 8 vasemmalle: x² + 2x − 8 = 0.", "Tekijöi: (x + 4)(x − 2) = 0."], {"a": 2, "k": 8})
    add(start + 2, "G4", "H", "Täydennä puuttuva rivi: tekijöi vasen puoli, jotta nollasääntöä voi käyttää.",
        ["(x + 2)(x − 4) = 16", "x² − 2x − 8 = 16", "x² − 2x − 24 = 0", "(x − 6)(x + 4) = 0"], 4,
        sp.Eq((X + 2) * (X - 4), 16), ["Kerro auki: x² − 2x − 8 = 16.", "Siirrä 16 vasemmalle: x² − 2x − 24 = 0.", "Tekijöi: (x − 6)(x + 4) = 0."], {"a": 2, "b": -4, "k": 16})
    add(start + 3, "G4", "H", "Täydennä puuttuva rivi: tekijöi vasen puoli.",
        ["(x + 1)(x + 4) = 10", "x² + 5x + 4 = 10", "x² + 5x − 6 = 0", "(x + 6)(x − 1) = 0"], 4,
        sp.Eq((X + 1) * (X + 4), 10), ["Kerro auki: x² + 5x + 4 = 10.", "Siirrä 10 vasemmalle: x² + 5x − 6 = 0.", "Tekijöi: (x + 6)(x − 1) = 0."], {"a": 1, "b": 4, "k": 10})
    add(start + 4, "G4", "H", "Täydennä puuttuva rivi. Perustele itsellesi, miksi 20:n siirtäminen vasemmalle on välttämätöntä ennen tekijöihin jakoa.",
        ["(x − 2)(x − 3) = 20", "x² − 5x + 6 = 20", "x² − 5x − 14 = 0", "(x − 7)(x + 2) = 0"], 3,
        sp.Eq((X - 2) * (X - 3), 20), ["Kerro auki: x² − 5x + 6 = 20.", "Siirrä 20 vasemmalle: x² − 5x − 14 = 0.", "Tekijöi: (x − 7)(x + 2) = 0."], {"a": -2, "b": -3, "k": 20})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
