#!/usr/bin/env python3
"""LEXP-03 RP: exponential growth judged as linear. The pupil writes an equation whose only
solution is the true value (or growth factor, or time). True values are computed with sympy
from exact fractions; the invalid examples are the linear misreading of the same story."""
import random

import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "lexp03_rp"
TID, CODE = "LEXP-03", "RP"
GENERIC = "Eksponentiaalisessa kasvussa muutos kerrotaan joka jaksolla samalla kasvutekijällä; se ei ole sama lisäys joka jaksolla."


def payload(var, value, valid, invalid):
    return {"constraint": {"type": "solution_equals", "variable": var, "value": int(value)},
            "checks": {"valid": valid, "invalid": invalid}}


def make_items(run, date, count=5, start=1):
    items = []
    # 1 MAB bacteria doubling, n after 3 hours
    n0, h = 100, 3
    v = n0 * 2**h
    items.append(base_item(
        TID, CODE, start, ["MAB4.02"], ["G5"], "MAB", "P", "none",
        f"Bakteerien määrä kaksinkertaistuu joka tunti. Alussa niitä on {n0}. Merkitään n = bakteerien määrä {h} tunnin kuluttua. Kirjoita yhtälö, jonka ainoa ratkaisu on n:n oikea arvo.",
        payload("n", v, [f"n = {n0}*2^{h}", f"n = {n0}*2*2*2"], [f"n = {n0} + {n0}*{h}", f"n = {n0}*2*{h}"]),
        [f"Jokaisella tunnilla määrä kerrotaan kahdella: n = {n0} · 2³ = {v}.", f"Lisäys {n0} bakteeria tunnissa (yhteensä {n0 + n0 * h}) olisi lineaarista kasvua."],
        f"esim. n = {n0} · 2^{h} (n = {v})", "Oikein: määrä kerrotaan kasvutekijällä joka tunti.", TEMPLATE, {"n0": n0, "hours": h}, date, run,
        generic_wrong=GENERIC))

    # 2 MAB price growth 10 % per year, 2 years
    k0, y = 1000, 2
    q = sp.Rational(11, 10)
    v = k0 * q**y
    assert v == 1210
    items.append(base_item(
        TID, CODE, start + 1, ["MAB4.02", "MAB7.01"], ["G5"], "MAB", "T", "none",
        f"Talletus {k0} € kasvaa 10 % vuodessa korkoa korolle. Merkitään v = talletuksen arvo {y} vuoden kuluttua. Kirjoita yhtälö, jonka ainoa ratkaisu on v:n oikea arvo.",
        payload("v", v, [f"v = {k0}*(11/10)^{y}", f"v = {k0}*(11/10)*(11/10)"], [f"v = {k0}*(1 + {y}*1/10)", f"v = {k0}*(11/10)*{y}"]),
        [f"Kasvutekijä on 1 + 10/100 = 11/10, joten v = {k0} · (11/10)² = {v}.", f"Kahden vuoden 10 %:n lisäys {k0}:stä (yhteensä {k0 + 2 * k0 // 10}) unohtaa koron koron."],
        f"esim. v = {k0} · 1,1² (v = {v})", "Oikein: korko lasketaan joka vuosi edellisen vuoden arvosta.", TEMPLATE, {"k0": k0, "years": y}, date, run,
        generic_wrong=GENERIC))

    # 3 MAA growth factor from 8-fold in 3 years
    years, total = 3, 8
    qv = sp.Integer(total) ** sp.Rational(1, years)
    assert qv == 2
    items.append(base_item(
        TID, CODE, start + 2, ["MAA5.06"], ["G4"], "MAA", "T", "none",
        f"Kasvusto muuttuu {years} vuodessa {total}-kertaiseksi, ja kasvutekijä q on joka vuosi sama. Kirjoita yhtälö, jonka ainoa ratkaisu on q:n oikea arvo.",
        payload("q", qv, [f"q^{years} = {total}", f"q^{years} − {total} = 0"], [f"{years}*q = {total}", f"q = {total}^{years}"]),
        [f"Kolmen vuoden kasvutekijä on q · q · q = q³, joten q³ = {total}.", "Siis q = 2. Yhtälö 3q = 8 olisi lineaarinen malli."],
        f"esim. q^{years} = {total} (q = {qv})", "Oikein: kasvutekijät kerrotaan keskenään.", TEMPLATE, {"years": years, "total": total}, date, run,
        generic_wrong=GENERIC))

    # 4 MAA time until 32-fold, doubling every hour
    base, total = 2, 32
    tv = sp.log(total, base)
    assert tv == 5
    items.append(base_item(
        TID, CODE, start + 3, ["MAA5.06"], ["G4"], "MAA", "H", "none",
        f"Määrä kaksinkertaistuu joka tunti. Merkitään t = aika tunteina, jonka kuluttua määrä on {total}-kertainen alkuarvoon verrattuna. Kirjoita yhtälö, jonka ainoa ratkaisu on t:n oikea arvo.",
        payload("t", tv, [f"{base}^t = {total}", f"{base}^t = {base}^5"], [f"{base}*t = {total}", f"t = {total}"]),
        [f"Tunnin kuluttua tekijä on 2, t tunnin kuluttua 2^t. Yhtälö 2^t = {total} antaa t = 5.", f"Lineaarinen malli 2t = {total} antaisi t = 16, joka on liian pitkä aika."],
        f"esim. 2^t = {total} (t = 5)", "Oikein: viidessä tunnissa kerrotaan kahdella viisi kertaa.", TEMPLATE, {"base": base, "total": total}, date, run,
        generic_wrong=GENERIC))

    # 5 MAB value halves each year
    k0, y = 800, 3
    v = k0 * sp.Rational(1, 2) ** y
    assert v == 100
    items.append(base_item(
        TID, CODE, start + 4, ["MAB4.02"], ["G4"], "MAB", "H", "none",
        f"Koneen arvo laskee 50 % joka vuosi. Alussa arvo on {k0} €. Merkitään k = arvo {y} vuoden kuluttua. Kirjoita yhtälö, jonka ainoa ratkaisu on k:n oikea arvo, ja tarkista, ettei arvo ole negatiivinen.",
        payload("k", v, [f"k = {k0}*(1/2)^{y}", f"k = {k0}/2^{y}"], [f"k = {k0} − {y}*{k0 // 2}", f"k = {k0}/(2*{y})"]),
        [f"Arvo puolittuu joka vuosi: k = {k0} · (1/2)³ = {v}.", f"Vähennys {k0 // 2} € vuodessa antaisi {k0 - y * (k0 // 2)} €, mikä on mahdoton negatiivinen arvo."],
        f"esim. k = {k0} · (1/2)^{y} (k = {v})", "Oikein: arvo lähestyy nollaa mutta ei muutu negatiiviseksi.", TEMPLATE, {"k0": k0, "years": y}, date, run,
        generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
