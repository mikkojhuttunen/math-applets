#!/usr/bin/env python3
"""NUM-08 RP (lukio level): successive percentage changes. The pupil writes an equation whose only solution
is the true value. True values come from exact Fractions; the invalid examples add or subtract the
percentages instead of multiplying the growth factors."""
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "num08_rp"
TID, CODE = "NUM-08", "RP"
GENERIC = "Peräkkäiset prosenttimuutokset kerrotaan keskenään: jokainen lasketaan edellisen muutoksen jälkeisestä arvosta, ei alkuarvosta."


def payload(var, value, valid, invalid):
    assert value.denominator == 1
    return {"constraint": {"type": "solution_equals", "variable": var, "value": int(value)},
            "checks": {"valid": valid, "invalid": invalid}}


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, g, syll, level, prompt, pl, steps, final, params, fb):
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt, pl, steps, final, fb,
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    v = 200 * Fraction(3, 2) * Fraction(1, 2)
    assert v == 150
    add(start, ["MAY1.03", "MAB6.01"], ["G4", "G8"], "MAB", "P",
        "Takin hinta on 200 €. Hinta nousee 50 % ja laskee sen jälkeen 50 %. Merkitään p = lopullinen hinta euroina. Kirjoita yhtälö, jonka ainoa ratkaisu on p:n oikea arvo.",
        payload("p", v, ["p = 200*(3/2)*(1/2)", "p = 200*(3/2)*(50/100)"], ["p = 200*(1 + 1/2 − 1/2)", "p = 200"]),
        ["Nousun jälkeen hinta on 200 · 3/2 = 300 €.", "Lasku koskee korotettua hintaa: 300 · 1/2 = 150 €. Hinta ei palaa alkuarvoon 200 €."],
        "esim. p = 200 · 1,5 · 0,5 (p = 150)", {"price": 200, "p": [50, -50]},
        "Oikein: lasku lasketaan korotetusta hinnasta.")
    k = 100 * (Fraction(11, 10) * Fraction(6, 5) - 1)
    assert k == 32
    add(start + 1, ["MAY1.03", "MAB6.01"], ["G4", "G8"], "MAB", "T",
        "Vuokra nousee ensin 10 % ja sitten 20 %. Merkitään k = vuokran kokonaisnousu prosentteina alkuperäisestä. Kirjoita yhtälö, jonka ainoa ratkaisu on k:n oikea arvo.",
        payload("k", k, ["k = 100*((11/10)*(6/5) − 1)", "k = 100*((11/10)*(12/10) − 1)"], ["k = 10 + 20", "k = 100*(1/10 + 1/5)"]),
        ["Kasvukertoimet ovat 11/10 ja 6/5, joten kokonaiskerroin on 11/10 · 6/5 = 33/25 = 1,32.", "Nousu on 32 %, ei 10 % + 20 % = 30 %."],
        "esim. k = 100 · (1,1 · 1,2 − 1) (k = 32)", {"p": [10, 20]},
        "Oikein: prosenttimuutokset kertautuvat, joten kokonaisnousu on enemmän kuin prosenttien summa.")
    s = 100 * Fraction(4, 5) * Fraction(5, 4)
    assert s == 100
    add(start + 2, ["MAY1.03", "MAA9.03"], ["G4"], "MAA", "T",
        "Hinta laskee 20 % ja nousee sen jälkeen 25 %. Merkitään s = lopullinen hinta prosentteina alkuperäisestä hinnasta. Kirjoita yhtälö, jonka ainoa ratkaisu on s:n oikea arvo.",
        payload("s", s, ["s = 100*(4/5)*(5/4)", "s = 100*(80/100)*(125/100)"], ["s = 100 − 20 + 25", "s = 100*(1 − 1/5 + 1/4)"]),
        ["Alennuksen jälkeen hinta on 4/5 alkuhinnasta, korotus kertoo sen luvulla 5/4.", "4/5 · 5/4 = 1, joten hinta palaa täsmälleen alkuarvoon eli 100 %:iin. Laskeminen 100 − 20 + 25 antaisi 105 %."],
        "esim. s = 100 · 0,8 · 1,25 (s = 100)", {"p": [-20, 25]},
        "Oikein: kertoimet 0,8 ja 1,25 ovat toistensa käänteislukuja.")
    q = Fraction(11, 10)
    assert q * q == Fraction(121, 100)
    p = 100 * (q - 1)
    assert p == 10
    add(start + 3, ["MAY1.03", "MAA9.03"], ["G4", "G8"], "MAA", "H",
        "Hinta nousee kaksi vuotta peräkkäin saman prosenttimäärän p vuodessa, ja kokonaisnousu on 21 %. Kirjoita yhtälö, jonka ainoa ratkaisu on p:n oikea arvo (p > 0).",
        payload("p", p, ["p = 100*(sqrt(121/100) − 1)", "p = 100*(11/10 − 1)"], ["2*p = 21", "p = 21/2"]),
        ["Kasvukerroin q toteuttaa q² = 1,21, joten q = 1,1 ja p = 10.", "Jos 21 % jaettaisiin tasan, saataisiin 10,5 %, mutta kaksi 10,5 %:n nousua antaisi yli 22 %."],
        "esim. p = 100 · (√1,21 − 1) (p = 10)", {"total": 21, "years": 2},
        "Oikein: kertoimen neliö on 1,21, ei 1 + 2p/100.")
    d = 100 * (1 - 1 / Fraction(5, 4))
    assert d == 20
    add(start + 4, ["MAY1.03", "MAB6.01"], ["G4"], "MAB", "H",
        "Hinta nousee 25 %. Merkitään d = prosenttimäärä, jonka verran hinnan on sen jälkeen laskettava, jotta se palaa alkuperäiseksi. Kirjoita yhtälö, jonka ainoa ratkaisu on d:n oikea arvo.",
        payload("d", d, ["d = 100*(1 − 1/(5/4))", "d = 100*(1 − 4/5)"], ["d = 25", "d = 100*(1 − 3/4)"]),
        ["Korotettu hinta on 5/4 alkuhinnasta. Alkuhintaan palataan kertoimella 4/5.", "Lasku on siis 1 − 4/5 = 1/5 = 20 %. Lasku 25 % antaisi 5/4 · 3/4 = 15/16, eli hinta jäisi alkuhintaa pienemmäksi."],
        "esim. d = 100 · (1 − 4/5) (d = 20)", {"p": 25},
        "Oikein: lasku lasketaan korotetusta hinnasta, joten sen prosenttiosuus on pienempi kuin nousu.")
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
