#!/usr/bin/env python3
"""LFUN-01 MC: a function must be one formula (constant, piecewise, table, tariff).
Values are computed with sympy / plain Python; the distractor tagged LFUN-01 rejects a rule for lacking one formula."""
import math
import random

import sympy as sp

from gen_common import base_item, cli, mc_options

TEMPLATE = "lfun01_mc"
TID, CODE = "LFUN-01", "MC"
X = sp.Symbol("x")
GENERIC = "Funktio on sääntö, joka liittää jokaiseen lähtöarvoon täsmälleen yhden arvon. Kaavojen määrä tai kaavan muoto ei ratkaise."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1201)
    items = []
    # 1: constant rule (MAB)
    c = 5
    f = sp.Lambda(X, sp.Integer(c))
    assert all(f(v) == c for v in (-2, 0, 7))
    opts, cid = mc_options(
        rng, ("On funktio: jokaista x:n arvoa vastaa täsmälleen yksi arvo, nimittäin 5", "Oikein: vakiofunktion kuvaaja on vaakasuora suora."),
        [("Ei ole funktio, koska säännössä ei esiinny muuttujaa x", "LFUN-01", "Funktion ei tarvitse käyttää x:ää. Riittää, että jokaiselle x:lle tulee yksi arvo."),
         ("On funktio vain, jos arvo muuttuu, kun x muuttuu", "LFUN-01", "Muuttumattomuus ei estä funktiota: f(−2) = f(0) = f(7) = 5 on sallittua.")])
    items.append(base_item(TID, CODE, start, ["MAY1.07"], ["G2"], "MAB", "P", "none",
                           f"Sääntö on: jokaista lukua x vastaa luku {c}. Onko tämä sääntö funktio?",
                           {"options": opts, "correct": [cid]},
                           [f"Jokaiselle x:lle tulee täsmälleen yksi arvo, {c}.", "Siis sääntö on funktio (vakiofunktio)."], "On funktio", "Oikein.",
                           TEMPLATE, {"c": c}, date, run, generic_wrong=GENERIC))
    # 2: piecewise value (MAA)
    f = sp.Piecewise((2 * X, X < 3), (X + 4, True))
    val, other = f.subs(X, 3), 2 * 3
    assert val == 7 and other != val
    opts, cid = mc_options(
        rng, (str(val), "Oikein: x = 3 ei ole alle 3, joten käytetään kaavaa x + 4."),
        [(str(other), None, "Ehto on x < 3, joten x = 3 kuuluu toiseen kaavaan."),
         ("f(3) ei ole määritelty, koska kaavoja on kaksi", "LFUN-01", "Paloittain määritelty funktio on funktio: jokaista x:ää varten ehto valitsee täsmälleen yhden kaavan.")])
    items.append(base_item(TID, CODE, start + 1, ["MAA12.01"], ["G2"], "MAA", "T", "none",
                           "Funktio f määritellään: f(x) = 2x, kun x < 3, ja f(x) = x + 4, kun x ≥ 3. Mikä on f(3)?",
                           {"options": opts, "correct": [cid]},
                           ["Ehto x < 3 ei päde, kun x = 3.", "f(3) = 3 + 4 = 7."], "7", "Oikein.", TEMPLATE, {"a": 3}, date, run, generic_wrong=GENERIC))
    # 3: table with equal outputs (MAB)
    xs, ys = [1, 2, 3, 4], [7, 7, 7, 7]
    assert len(set(xs)) == len(xs)
    opts, cid = mc_options(
        rng, ("Kyllä: jokaista x:n arvoa vastaa täsmälleen yksi y:n arvo", "Oikein: samat y-arvot eri x:ille ovat sallittuja."),
        [("Ei: y ei muutu, joten y ei voi olla funktio", "LFUN-01", "Funktio saa antaa saman arvon monelle x:lle. Kielletty on vain se, että yhdelle x:lle tulee kaksi arvoa."),
         ("Ei: taulukossa ei ole kaavaa", "LFUN-01", "Funktion ei tarvitse olla annettu kaavalla; taulukkokin määrittelee funktion.")])
    items.append(base_item(TID, CODE, start + 2, ["MAY1.07"], ["G2"], "MAB", "T", "none",
                           "Taulukossa on x:n arvot 1, 2, 3 ja 4 sekä niitä vastaavat y:n arvot 7, 7, 7 ja 7. Onko y funktio x:n suhteen?",
                           {"options": opts, "correct": [cid]},
                           ["Jokaista x:ää vastaa täsmälleen yksi y.", "Kaikki y-arvot ovat samat, mikä on sallittua."], "Kyllä", "Oikein.",
                           TEMPLATE, {"xs": xs, "ys": ys}, date, run, generic_wrong=GENERIC))
    # 4: tariff, computed value (MAB)
    def fee(h):
        return 2 * min(h, 3) + 1 * max(h - 3, 0)
    started = math.ceil(4.5)
    right = fee(started)
    wrong_all = 2 * started
    assert right == 8 and wrong_all == 10
    opts, cid = mc_options(
        rng, (f"{right} €", "Oikein: 3 h · 2 € + 2 h · 1 € = 8 €."),
        [(f"{wrong_all} €", None, "Kolmen ensimmäisen tunnin jälkeen hinta on 1 € alkavalta tunnilta."),
         ("Hintaa ei voi laskea, koska se ei noudata yhtä kaavaa", "LFUN-01", "Kaksiosainen hinnoittelu on paloittain määritelty funktio. Pysäköintiaika määrää hinnan yksikäsitteisesti.")])
    items.append(base_item(TID, CODE, start + 3, ["MAY1.07"], ["G2"], "MAB", "T", "none",
                           "Pysäköinti maksaa 2 € jokaiselta alkavalta tunnilta kolmen ensimmäisen tunnin ajalta ja sen jälkeen 1 € jokaiselta alkavalta tunnilta. Paljonko 4,5 tunnin pysäköinti maksaa?",
                           {"options": opts, "correct": [cid]},
                           ["4,5 tuntia on 5 alkavaa tuntia.", "3 · 2 € + 2 · 1 € = 8 €."], f"{right} €", "Oikein.",
                           TEMPLATE, {"hours": 4.5}, date, run, generic_wrong=GENERIC))
    # 5: justification, |x| (MAA)
    g = sp.Piecewise((X, X >= 0), (-X, True))
    assert all(g.subs(X, v) == abs(v) for v in (-3, 0, 4))
    opts, cid = mc_options(
        rng, ("Funktio vaatii vain, että jokaista x:ää vastaa täsmälleen yksi arvo. Kaava saa olla paloittainen, ja |x| täyttää ehdon.", "Oikein."),
        [("Väite pitää paikkansa: funktiolla täytyy olla yksi kaava koko määrittelyjoukossa", "LFUN-01", "Yhden kaavan vaatimus ei kuulu funktion määritelmään."),
         ("|x| on funktio vain, jos sen kuvaaja on suora", "LFUN-01", "Kuvaajan muodolla ei ole tekemistä funktion määritelmän kanssa.")])
    items.append(base_item(TID, CODE, start + 4, ["MAA12.01"], ["G2"], "MAA", "H", "none",
                           "Oppilas väittää: ”f(x) = |x| ei ole funktio, koska sille tarvitaan kaksi kaavaa: x ja −x.” Mikä seuraavista on oikea perustelu väitteen arviointiin?",
                           {"options": opts, "correct": [cid]},
                           ["Esim. |−3| = 3, |0| = 0, |4| = 4: jokaiselle x:lle tulee yksi arvo.", "Kaavojen määrä ei vaikuta funktion määritelmään."],
                           "Väite on väärä: |x| on funktio", "Oikein.", TEMPLATE, {"f": "abs"}, date, run, generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
