#!/usr/bin/env python3
"""LEXP-03 NE: exponential growth judged as linear. Answers computed with sympy."""
import sympy as sp

from gen_common import base_item, cli, num

TEMPLATE = "lexp03_ne"
TID, CODE = "LEXP-03", "NE"
GENERIC = "Prosentuaalinen kasvu kertautuu: joka vuosi muutos lasketaan edellisen vuoden arvosta, ei alkuarvosta."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, g, tools, prompt, answer, wrong, wfb, steps, final, params):
        items.append(base_item(TID, CODE, n, lops, g, syll, level, tools, prompt,
                               {"answer": answer, "wrong": [{"match": wrong, "misconception": TID, "feedback": wfb}]},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: 3 % for 20 years, whole percent
    r, n = sp.Rational(3, 100), 20
    g = round(float(((1 + r) ** n - 1) * 100))
    add(start, ["MAB4.02"], "MAB", "T", ["G5"], "none",
        f"Hinta nousee {num(int(r * 100))} % vuodessa {n} vuotta. Kuinka monta prosenttia hinta on noussut yhteensä? Pyöristä kokonaisprosenttiin.",
        {"kind": "number", "value": g, "tolerance": 0.5, "unit": "%"}, int(r * 100 * n),
        "60 % olettaa saman euromääräisen nousun joka vuosi. Käytä kerrointa 1,03^20.",
        ["Vuosikerroin on 1,03.", f"1,03^{n} ≈ {num(round(float((1 + r) ** n), 2))}, joten nousu on noin {g} %."], f"{g} %",
        {"rate": str(r), "years": n})
    # 2: doubling time at 5 %, CAS tools
    r = sp.Rational(5, 100)
    t = round(float(sp.log(2) / sp.log(1 + r)))
    assert t == 14
    add(start + 1, ["MAB4.02"], "MAB", "H", ["G5"], "cas",
        f"Sijoituksen arvo kasvaa {num(int(r * 100))} % vuodessa. Kuinka monta vuotta kestää, kunnes arvo on kaksinkertainen? Pyöristä lähimpään kokonaislukuun.",
        {"kind": "number", "value": t, "tolerance": 0.5, "unit": "vuotta"}, int(100 / (r * 100)),
        "100 / 5 = 20 olettaa lineaarisen kasvun. Ratkaise yhtälö 1,05^t = 2.",
        ["1,05^t = 2.", f"t = ln 2 / ln 1,05 ≈ {num(round(float(sp.log(2) / sp.log(1 + r)), 1))}."], f"{t} vuotta", {"rate": str(r)})
    # 3: compound interest, MAA
    p, r, n = 1000, sp.Rational(2, 100), 5
    amount = round(float(p * (1 + r) ** n), 2)
    add(start + 2, ["MAA9.03"], "MAA", "T", ["G5"], "none",
        f"Talletat {num(p)} € tilille, jonka vuosikorko on {num(int(r * 100))} %. Korko liitetään pääomaan joka vuosi. Paljonko tilillä on {n} vuoden kuluttua (€)?",
        {"kind": "number", "value": amount, "tolerance": 0.01, "unit": "€"}, p + p * float(r) * n,
        "1100 € olettaa, että korkoa maksetaan vain alkupääomalle. Käytä kerrointa 1,02^5.",
        ["Vuosikerroin on 1,02.", f"{p} · 1,02^{n} = {num(amount)}."], f"{num(amount)} €", {"p": p, "rate": str(r), "years": n})
    # 4: doubling every 3 days
    n0, d, t = 10, 3, 12
    right = n0 * 2 ** (t // d)
    add(start + 3, ["MAA5.06"], "MAA", "P", ["G5"], "none",
        f"Tartuntojen määrä kaksinkertaistuu {d} päivän välein. Aluksi tartuntoja on {n0}. Montako tartuntaa on {t} päivän kuluttua?",
        {"kind": "number", "value": right}, n0 + n0 * (t // d),
        "Tämä lisää saman määrän joka jakso. Kaksinkertaistuminen kertoo määrän luvulla 2.",
        [f"{t} päivää on {t // d} kaksinkertaistumista.", f"{n0} · 2^{t // d} = {right}."], str(right), {"n0": n0, "d": d, "t": t})
    # 5: plausibility, 4 % for 10 years
    r, n = sp.Rational(4, 100), 10
    g = round(float(((1 + r) ** n - 1) * 100))
    assert g == 48
    add(start + 4, ["MAA9.03"], "MAA", "H", ["G4"], "none",
        f"Asunnon hinta nousee {num(int(r * 100))} % vuodessa. Kollega arvioi, että {n} vuodessa hinta nousee 40 %. Laske todellinen nousu prosentteina kokonaisprosentiksi pyöristettynä ja tarkista, onko arvio järkevä.",
        {"kind": "number", "value": g, "tolerance": 0.5, "unit": "%"}, 40,
        "40 % on lineaarinen arvio, 10 · 4 %. Kasvu kertautuu: käytä kerrointa 1,04^10.",
        ["Vuosikerroin on 1,04.", f"1,04^{n} ≈ {num(round(float((1 + r) ** n), 3))}, joten nousu on noin {g} %.", "Arvio 40 % on liian pieni."],
        f"{g} %", {"rate": str(r), "years": n})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
