#!/usr/bin/env python3
"""LTRI-02 ES (lukio level): sine treated as a factor that can be split. Each item shows a worked
solution with one line where the coefficient of the argument is moved in front of sin. The verifier
checks that the lines before the error line are equivalent and that the error line is not."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "ltri02_es"
TID, CODE = "LTRI-02", "ES"
GENERIC = "Sini ei ole tekijä, jonka voi jakaa: sin kx ≠ k sin x. Käytä kaksoiskulmakaavaa tai kokeile lukuarvolla."
X = sp.Symbol("x")


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, level, prompt, lines, error_line, steps, final, params):
        items.append(base_item(TID, CODE, n, ["MAA5.03"], ["G2"], "MAA", level, "none", prompt,
                               {"lines": lines, "error_line": error_line, "error_type": "sine_coefficient_pulled_out"},
                               steps, final, "Oikein: kerroin sinin sisällä ei siirry sinin eteen.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: sin 2x / sin x
    r = sp.simplify(sp.expand_trig(sp.sin(2 * X)) / sp.sin(X))
    assert sp.simplify(r - 2 * sp.cos(X)) == 0
    add(start, "T", "Oppilas sieventi lausekkeen sin 2x / sin x. Napauta rivi, jossa on virhe.",
        ["sin(2x)/sin(x)", "2 sin(x)/sin(x)", "2"], 2,
        ["Rivillä 2 kerroin 2 on siirretty sinin eteen: sin 2x ≠ 2 sin x.", "Oikein: sin 2x = 2 sin x cos x, joten osamäärä on 2 cos x."],
        "2cos(x)", {"expr": "sin(2x)/sin(x)"})
    # 2: value at x = pi/6
    x0 = sp.pi / 6
    v = sp.simplify(sp.sin(2 * x0))
    w = 2 * sp.sin(x0)
    assert v == sp.sqrt(3) / 2 and w == 1
    add(start + 1, "P", "Oppilas laski sin 2x:n arvon, kun x = π/6. Napauta rivi, jossa on virhe.",
        ["sin(2 · π/6)", "2 sin(π/6)", "2 · 1/2", "1"], 2,
        ["Rivillä 2 kerroin 2 on siirretty sinin eteen. Sinin sisällä oleva kulma on 2 · π/6 = π/3.", "Oikein: sin(π/3) = √3/2."],
        show(v), {"x": "pi/6"})
    # 3: sin 2x + 2 sin x
    e = sp.expand_trig(sp.sin(2 * X)) + 2 * sp.sin(X)
    assert sp.simplify(e - 2 * sp.sin(X) * (sp.cos(X) + 1)) == 0
    add(start + 2, "T", "Oppilas sieventi lausekkeen sin 2x + 2 sin x. Napauta rivi, jossa on virhe.",
        ["sin(2x) + 2 sin(x)", "2 sin(x) + 2 sin(x)", "4 sin(x)"], 2,
        ["Rivillä 2 sin 2x on korvattu lausekkeella 2 sin x.", "Oikein: sin 2x + 2 sin x = 2 sin x cos x + 2 sin x = 2 sin x (cos x + 1)."],
        "2sin(x)(cos(x)+1)", {})
    # 4: sin 3x / sin x
    r = sp.simplify(sp.expand_trig(sp.sin(3 * X)) / sp.sin(X))
    assert sp.simplify(r - (3 - 4 * sp.sin(X) ** 2)) == 0
    add(start + 3, "H", "Oppilas sieventi lausekkeen sin 3x / sin x. Napauta rivi, jossa on virhe.",
        ["sin(3x)/sin(x)", "3 sin(x)/sin(x)", "3"], 2,
        ["Rivillä 2 kerroin 3 on siirretty sinin eteen: sin 3x ≠ 3 sin x.", "Oikein: sin 3x = 3 sin x − 4 sin³ x, joten osamäärä on 3 − 4 sin² x."],
        "3 − 4sin(x)^2", {})
    # 5: sin 2x with sin x = 0.8, cos x = 0.6; hint on size
    d = sp.Rational(2) * sp.Rational(4, 5) * sp.Rational(3, 5)
    assert d == sp.Rational(24, 25) and 2 * sp.Rational(4, 5) > 1
    add(start + 4, "H", "Kulmalle x pätee sin x = 0,8 ja cos x = 0,6. Oppilas laski sin 2x:n näin. Napauta rivi, jossa on virhe. Vihje: sinin arvo ei voi ylittää lukua 1.",
        ["sin(2x)", "2 sin(x)", "2 · 0,8", "1,6"], 2,
        ["Rivillä 2 kerroin 2 on siirretty sinin eteen. Tulos 1,6 on suurempi kuin 1, joten se ei voi olla sinin arvo.",
         "Oikein: sin 2x = 2 sin x cos x = 2 · 0,8 · 0,6 = 0,96."], show(0.96), {"sin": 0.8, "cos": 0.6})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
