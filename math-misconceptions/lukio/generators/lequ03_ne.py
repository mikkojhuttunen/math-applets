#!/usr/bin/env python3
"""LEQU-03 NE (lukio level): an inequality is multiplied by an expression of unknown sign.
Interval answers are computed with sympy; the wrong answer is the set obtained by assuming the
multiplier is positive."""
import sympy as sp

from gen_common import base_item, cli, frac

TEMPLATE = "lequ03_ne"
TID, CODE = "LEQU-03", "NE"
X = sp.Symbol("x", real=True)
GENERIC = "Epäyhtälön saa kertoa puolittain vain lausekkeella, jonka merkki tiedetään. Siirrä kaikki vasemmalle, sievennä yhdeksi murtolausekkeeksi ja tutki tekijöiden merkit."


def ivs(rel):
    s = sp.solve_univariate_inequality(rel, X, relational=False)
    parts = list(s.args) if isinstance(s, sp.Union) else ([] if s == sp.S.EmptySet else [s])
    parts.sort(key=lambda p: float(p.inf) if p.inf != -sp.oo else -1e18)
    out = []
    for p in parts:
        out.append({"lo": None if p.inf == -sp.oo else str(p.inf), "hi": None if p.sup == sp.oo else str(p.sup),
                    "lo_closed": bool((not p.left_open) and p.inf != -sp.oo), "hi_closed": bool((not p.right_open) and p.sup != sp.oo)})
    return out


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, g, level, prompt, ref_text, rel, wrong_text, wfb, steps, final, params, hint=None):
        ans = {"kind": "interval", "variable": "x", "reference": ref_text, "intervals": ivs(rel)}
        items.append(base_item(TID, CODE, n, ["MAA2.06", "MAA2.07"], [g], "MAA", level, "none", prompt,
                               {"answer": ans, "wrong": [{"match": wrong_text, "misconception": TID, "feedback": wfb}]},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    add(start, "G4", "T", "Ratkaise epäyhtälö 1/x > 3.", "1/x > 3", 1 / X > 3, "x < 1/3",
        "Kertoessasi x:llä oletit, että x > 0. Kokeile x = −1: 1/(−1) = −1, joka ei ole suurempi kuin 3.",
        ["Siirrä 3 vasemmalle: 1/x − 3 > 0, eli (1 − 3x)/x > 0.", "Osoittajan ja nimittäjän on oltava samanmerkkiset: 0 < x < 1/3."],
        "0 < x < 1/3", {"a": 1, "b": 3})
    add(start + 1, "G3", "T", "Ratkaise epäyhtälö 2/(x − 1) < 1.", "2/(x − 1) < 1", 2 / (X - 1) < 1, "x > 3",
        "Kertominen x − 1:llä käänsi suunnan vain kun x − 1 < 0. Tapaus x < 1 puuttuu: esimerkiksi x = 0 antaa 2/(−1) = −2 < 1.",
        ["Siirrä 1 vasemmalle: (3 − x)/(x − 1) < 0.", "Merkki on negatiivinen, kun osoittaja ja nimittäjä ovat erimerkkiset: x < 1 tai x > 3."],
        "x < 1 tai x > 3", {"a": 2, "b": 1})
    add(start + 2, "G4", "H", "Ratkaise epäyhtälö 4/x ≤ 1. Tarkista tulos sijoittamalla x = −2.", "4/x ≤ 1", 4 / X <= 1, "x ≥ 4",
        "Kun x < 0, 4/x on negatiivinen ja siten pienempi kuin 1. Esimerkiksi x = −2 antaa −2 ≤ 1.",
        ["Siirrä 1 vasemmalle: (4 − x)/x ≤ 0.", "Murtoluku on ei-positiivinen, kun x < 0 tai x ≥ 4 (x = 0 ei kelpaa).", "Tarkistus: x = −2 antaa 4/(−2) = −2 ≤ 1."],
        "x < 0 tai x ≥ 4", {"a": 4, "b": 1})
    add(start + 3, "G4", "H", "Ratkaise epäyhtälö 3/(x + 1) > 1.", "3/(x + 1) > 1", 3 / (X + 1) > 1, "x < 2",
        "Kertominen x + 1:llä on sallittu vain, kun x + 1 > 0. Silloin x > −1, ja ratkaisu on −1 < x < 2.",
        ["Siirrä 1 vasemmalle: (2 − x)/(x + 1) > 0.", "Osoittaja ja nimittäjä samanmerkkiset: −1 < x < 2."],
        "−1 < x < 2", {"a": 3, "b": 1})
    add(start + 4, "G3", "H", "Ratkaise epäyhtälö x/(x − 2) < 3.", "x/(x − 2) < 3", X / (X - 2) < 3, "x > 3",
        "Kertominen x − 2:lla antaa vain tapauksen x > 2. Tapaus x < 2 puuttuu: x = 0 antaa 0 < 3.",
        ["Siirrä 3 vasemmalle: (x − 3(x − 2))/(x − 2) < 0, eli (6 − 2x)/(x − 2) < 0.", "Merkit ovat erilaiset, kun x < 2 tai x > 3."],
        "x < 2 tai x > 3", {"a": 1, "b": 2, "c": 3})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
