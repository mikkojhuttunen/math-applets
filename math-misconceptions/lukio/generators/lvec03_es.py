#!/usr/bin/env python3
"""LVEC-03 ES (lukio level): the dot product gives a vector. Each item shows a worked solution
where the component products are not added into one number (or the second component is dropped
in a perpendicularity equation). Every line is computed with sympy; the verifier checks that the
lines before the error line are equivalent and that the error line is not."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "lvec03_es"
TID, CODE = "LVEC-03", "ES"
GENERIC = "Pistetulo a · b = a₁b₁ + a₂b₂ on yksi luku. Komponenttien tulot lasketaan yhteen, ne eivät jää erillisiksi."


def pt(p):
    return f"({show(p[0])}, {show(p[1])})"


def par(v):
    return f"({show(v)})" if v < 0 else show(v)


def make_items(run, date, count=5, start=1):
    items = []
    K = sp.Symbol("k")

    def add(n, level, prompt, lines, error_line, steps, final, params):
        items.append(base_item(TID, CODE, n, ["MAA4.08"], ["G2"], "MAA", level, "none", prompt,
                               {"lines": lines, "error_line": error_line, "error_type": "dot_product_as_vector"},
                               steps, final, "Oikein: pistetulo on komponenttitulojen summa.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: components multiplied, then the products multiplied together
    a, b = sp.Matrix([2, 3]), sp.Matrix([4, 1])
    p1, p2 = a[0] * b[0], a[1] * b[1]
    d = a.dot(b)
    assert p1 * p2 != d
    add(start, "P", f"Oppilas laski pistetulon a · b, kun a = {pt(a)} ja b = {pt(b)}. Napauta rivi, jossa on virhe.",
        [f"{a[0]} · {b[0]} + {a[1]} · {b[1]}", f"{p1} · {p2}", f"{p1 * p2}"], 2,
        [f"Rivillä 2 komponenttitulot {p1} ja {p2} on kerrottu keskenään. Ne lasketaan yhteen.", f"Oikein: {p1} + {p2} = {d}."],
        show(d), {"a": [2, 3], "b": [4, 1]})
    # 2: perpendicular, second component dropped
    a, b = sp.Matrix([K, 3]), sp.Matrix([6, -2])
    sol = sp.solve(sp.Eq(a.dot(b), 0), K)
    assert sol == [1]
    add(start + 1, "T", f"Vektorit a = (k, 3) ja b = {pt(b)} ovat kohtisuorassa. Oppilas ratkaisi k:n näin. Napauta rivi, jossa on virhe.",
        [f"6k + 3 · ({show(b[1])}) = 0", "6k = 0", "k = 0"], 2,
        ["Rivillä 2 termi 3 · (−2) = −6 on pudotettu pois, ikään kuin pistetulo olisi vektori (6k, −6), jonka vain ensimmäinen komponentti pitäisi nollata.",
         "Oikein: 6k − 6 = 0, joten k = 1."], "k = 1", {"b": [6, -2]})
    # 3: same idea, error on line 3
    a, b = sp.Matrix([K, 3]), sp.Matrix([4, -2])
    sol = sp.solve(sp.Eq(a.dot(b), 0), K)
    assert sol == [sp.Rational(3, 2)]
    add(start + 2, "T", f"Vektorit a = (k, 3) ja b = {pt(b)} ovat kohtisuorassa. Oppilas ratkaisi k:n näin. Napauta rivi, jossa on virhe.",
        [f"4k + 3 · ({show(b[1])}) = 0", "4k − 6 = 0", "4k = 0", "k = 0"], 3,
        ["Rivillä 3 luku −6 on pudotettu pois, vaikka pistetulo on yksi luku 4k − 6 ja koko luvun pitää olla nolla.",
         "Oikein: 4k = 6, joten k = 3/2."], "k = 3/2", {"b": [4, -2]})
    # 4: components multiplied but not added
    a, b = sp.Matrix([1, 2]), sp.Matrix([3, -1])
    d = a.dot(b)
    assert d == 1
    add(start + 3, "H", f"Oppilas laski pistetulon a · b, kun a = {pt(a)} ja b = {pt(b)}. Napauta rivi, jossa on virhe.",
        [f"1 · 3 + 2 · ({show(b[1])})", "3 · (−2)", "−6"], 2,
        ["Rivillä 2 komponenttitulot 3 ja −2 on kerrottu keskenään. Pistetulossa ne lasketaan yhteen.", "Oikein: 3 + (−2) = 1."],
        show(d), {"a": [1, 2], "b": [3, -1]})
    # 5: a . a, the squares multiplied instead of added; hint says the result is one number
    a = sp.Matrix([-2, 5])
    d = a.dot(a)
    assert d == 29 and a[0] ** 2 * a[1] ** 2 != d
    add(start + 4, "H", f"Oppilas laski pistetulon a · a, kun a = {pt(a)}. Napauta rivi, jossa on virhe. Vihje: a · a on sama kuin |a|².",
        ["(−2)^2 + 5^2", "4 + 25", "4 · 25", "100"], 3,
        ["Rivillä 3 komponenttien neliöt 4 ja 25 on kerrottu keskenään. Ne lasketaan yhteen.",
         f"Oikein: 4 + 25 = {d}, ja tämä on |a|²."], show(d), {"a": [-2, 5]})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
