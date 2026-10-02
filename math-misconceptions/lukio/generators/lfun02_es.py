#!/usr/bin/env python3
"""LFUN-02 ES: linearity applied to every function. Each item shows a worked solution with
one injected line where a function (square, sine, root, logarithm) is split over a sum.
The numbers in every line are computed with sympy; the verifier checks that all lines
before the error line are equivalent and that the error line is not."""
import random

import sympy as sp

from gen_common import base_item, cli, num, show

TEMPLATE = "lfun02_es"
TID, CODE = "LFUN-02", "ES"
X = sp.Symbol("x")
GENERIC = "Funktio ei yleensä jaa summaa: f(a + b) on eri asia kuin f(a) + f(b). Kokeile lukuarvoilla."


def t(e):
    """Display text of a polynomial or expression: ², decimal comma, proper minus."""
    return show(e).replace(" · ", "").replace("^2", "²").replace("**2", "²")


def sq_equation(rng, n, lops, syll, level, ctx, date, run):
    a = rng.choice([2, 3, 4, 5])
    m = rng.choice([5, 6, 7])
    c = m * m
    true_sols = sorted(sp.solveset(sp.Eq((X + a) ** 2, c), X, sp.S.Reals), key=float)
    wrong_rhs = c - a * a
    wrong_sols = sorted(sp.solveset(sp.Eq(X**2, wrong_rhs), X, sp.S.Reals), key=float)
    lines = [f"(x + {a})² = {c}", f"x² + {a * a} = {c}", f"x² = {wrong_rhs}", f"x = √{wrong_rhs} tai x = −√{wrong_rhs}"]
    steps = [f"Rivillä 2 neliö on jaettu summan yli: (x + {a})² ≠ x² + {a * a}.",
             f"Oikein: (x + {a})² = x² + {2 * a}x + {a * a}, tai otetaan neliöjuuri: x + {a} = {m} tai x + {a} = −{m}."]
    final = f"x = {num(true_sols[1])} tai x = {num(true_sols[0])}"
    assert sorted(true_sols, key=float) == [-m - a, m - a]
    assert wrong_sols != true_sols
    return base_item(TID, CODE, n, [lops], ["G2"], syll, level, "none", ctx.format(a=a, c=c),
                     {"lines": lines, "error_line": 2, "error_type": "square_of_sum_split"}, steps, final,
                     "Oikein: summan neliö ei ole neliöiden summa, keskimmäinen tulo puuttuu.", TEMPLATE,
                     {"a": a, "m": m}, date, run, misconceptions=[TID, "ALG-09"], generic_wrong=GENERIC)


def sq_expression(rng, n, lops, syll, level, ctx, date, run):
    p, q = rng.choice([(2, 3), (3, 2), (2, 5)])
    sub = q * q
    right = sp.expand((p * X + q) ** 2 - sub)
    mid = sp.expand(p * p * X**2 + sub - sub)
    assert right != mid
    lines = [f"({p}x + {q})² − {sub}", f"{p * p}x² + {sub} − {sub}", f"{t(mid)}"]
    steps = [f"Rivillä 2 summan ({p}x + {q}) neliö on laskettu termeittäin.",
             f"Oikein: ({p}x + {q})² = {t(sp.expand((p * X + q) ** 2))}, joten tulos on {t(right)}."]
    return base_item(TID, CODE, n, [lops], ["G2"], syll, level, "none", ctx.format(p=p, q=q, sub=sub),
                     {"lines": lines, "error_line": 2, "error_type": "square_of_sum_split"}, steps, t(right),
                     "Oikein: binomin neliössä on aina keskimmäinen tulo.", TEMPLATE, {"p": p, "q": q},
                     date, run, misconceptions=[TID, "ALG-09"], generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(2202)
    items = [
        sq_equation(rng, start, "MAB2.07", "MAB", "P",
                    "Neliön muotoisen pihan sivu on x + {a} metriä ja pinta-ala {c} m². Oppilas ratkaisi sivun x näin. Napauta rivi, jossa on virhe.",
                    date, run),
        sq_expression(rng, start + 1, "MAB2.07", "MAB", "T",
                      "Laatan sivun pituus on {p}x + {q} metriä. Sen pinta-alasta vähennetään {sub} m². Oppilas sieventi lausekkeen näin. Napauta rivi, jossa on virhe.",
                      date, run),
    ]
    # sin(a + b) as sin a + sin b
    a, b = sp.pi / 6, sp.pi / 3
    right = sp.simplify(sp.sin(a + b))
    wrong = sp.simplify(sp.sin(a) + sp.sin(b))
    assert right == 1 and wrong != right
    items.append(base_item(
        TID, CODE, start + 2, ["MAA2.01", "MAA5.03"], ["G3"], "MAA", "T", "none",
        "Oppilas laski sin(π/6 + π/3) tarkan arvon näin. Napauta rivi, jossa on virhe. Vihje: sinin arvo ei ylitä lukua 1.",
        {"lines": ["sin(π/6 + π/3)", "sin(π/6) + sin(π/3)", "1/2 + √3/2"], "error_line": 2, "error_type": "sine_of_sum_split"},
        ["Rivillä 2 sini on jaettu summan yli, vaikka se ei ole lineaarinen.", "Oikein: π/6 + π/3 = π/2, ja sin(π/2) = 1."],
        "1", "Oikein: sini ei jaa summaa. Tulos 1/2 + √3/2 ≈ 1,37 olisi myös suurempi kuin 1.",
        TEMPLATE, {"a": "pi/6", "b": "pi/3"}, date, run, misconceptions=[TID, "LTRI-02"], generic_wrong=GENERIC))
    # square root of a sum
    # sqrt(x^2 + 9) = 5 -> x = +-4: the wrong line splits the root
    sols = sorted(sp.solveset(sp.Eq(sp.sqrt(X**2 + 9), 5), X, sp.S.Reals), key=float)
    assert sols == [-4, 4]
    items.append(base_item(
        TID, CODE, start + 3, ["MAA2.01"], ["G2"], "MAA", "H", "none",
        "Oppilas ratkaisi yhtälön √(x² + 9) = 5 näin. Napauta rivi, jossa on virhe.",
        {"lines": ["√(x² + 9) = 5", "x + 3 = 5", "x = 2"], "error_line": 2, "error_type": "root_of_sum_split"},
        ["Rivillä 2 neliöjuuri on jaettu summan yli: √(x² + 9) ≠ x + 3.",
         "Oikein: korotetaan neliöön, x² + 9 = 25, joten x² = 16 ja x = 4 tai x = −4."],
        "x = 4 tai x = −4", "Oikein: neliöjuuri ei jaa summaa. Tarkista sijoittamalla: √(2² + 9) = √13 ≠ 5.",
        TEMPLATE, {"root": "sqrt(x^2+9)=5"}, date, run, misconceptions=[TID], generic_wrong=GENERIC))
    # logarithm of a product
    p, q = 2, 3
    xp = sp.Symbol("x", positive=True)
    assert sp.simplify(sp.expand_log(sp.log(p * xp) + sp.log(q * xp) - sp.log(p * q * xp**2), force=True)) == 0
    assert sp.simplify(sp.log(p * xp + q * xp) - sp.log(p * xp) - sp.log(q * xp)) != 0
    items.append(base_item(
        TID, CODE, start + 4, ["MAA2.01", "MAA5.07"], ["G2"], "MAA", "H", "none",
        "Oppilas sieventi lausekkeen ln(2x) + ln(3x), kun x > 0. Napauta rivi, jossa on virhe.",
        {"lines": ["ln(2x) + ln(3x)", "ln(2x + 3x)", "ln(5x)"], "error_line": 2, "error_type": "log_sum_as_log_of_sum"},
        ["Rivillä 2 logaritmien summa on muutettu summan logaritmiksi. Logaritmien summa on tulon logaritmi.",
         "Oikein: ln(2x) + ln(3x) = ln(2x · 3x) = ln(6x²)."],
        "ln(6x²)", "Oikein: ln a + ln b = ln(ab), ei ln(a + b).", TEMPLATE, {"p": p, "q": q}, date, run,
        misconceptions=[TID, "LEXP-01"], generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
