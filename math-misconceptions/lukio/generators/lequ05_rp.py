#!/usr/bin/env python3
"""LEQU-05 RP (lukio level): absolute value read as "drop the minus sign". The pupil writes an
absolute value equation whose only solution is a given x. A pupil who drops the negative case
believes |x - a| = b has one solution; the invalid examples are such equations with two roots.
Valid and invalid examples are checked against the solution set by the verifier."""
from gen_common import base_item, cli

TEMPLATE = "lequ05_rp"
TID, CODE = "LEQU-05", "RP"
GENERIC = "Yhtälö |f(x)| = a, a > 0, antaa kaksi ratkaisua: f(x) = a ja f(x) = −a. Yksi ratkaisu syntyy, kun |f(x)| = 0 tai kun kaksi tapausta antaa saman luvun."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, level, prompt, value, valid, invalid, steps, final, params):
        items.append(base_item(TID, CODE, n, ["MAA4.06"], ["G4"], "MAA", level, "none", prompt,
                               {"constraint": {"type": "solution_equals", "variable": "x", "value": value},
                                "checks": {"valid": valid, "invalid": invalid}},
                               steps, final, "Oikein: yhtälöllä on täsmälleen tämä yksi ratkaisu.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: only solution x = 8
    add(start, "T", "Kirjoita itseisarvoyhtälö, jonka ainoa ratkaisu on x = 8.", 8,
        ["|x − 8| = 0", "|2x − 16| = 0", "|x| = |x − 16|"],
        ["|x − 3| = 5", "|x + 2| = 10", "|x − 8| = 1"],
        ["Itseisarvo on 0 vain, kun lauseke on 0: |x − 8| = 0 antaa x = 8.",
         "Yhtälö |x − 3| = 5 antaa x = 8 mutta myös x = −2."],
        "esim. |x − 8| = 0", {"x0": 8})
    # 2: only solution x = 2
    add(start + 1, "T", "Kirjoita itseisarvoyhtälö, jonka ainoa ratkaisu on x = 2.", 2,
        ["|x − 2| = 0", "|3x − 6| = 0", "|x| = |x − 4|"],
        ["|x + 4| = 6", "|x − 1| = 1", "|2x − 1| = 3"],
        ["Kun oikea puoli on 0, kaksi tapausta yhtyvät: x − 2 = 0.", "Yhtälöt |x + 4| = 6 ja |2x − 1| = 3 antavat 2 ja toisen ratkaisun, joten niillä on kaksi ratkaisua."],
        "esim. |x − 2| = 0", {"x0": 2})
    # 3: only solution x = -3
    add(start + 2, "H", "Kirjoita itseisarvoyhtälö, jonka ainoa ratkaisu on x = −3.", -3,
        ["|x + 3| = 0", "|2x + 6| = 0", "|x| = |x + 6|"],
        ["|x − 5| = 8", "|x + 3| = 2", "|2x + 1| = 5"],
        ["|x + 3| = 0 antaa x = −3.", "|x − 5| = 8 antaa x = 13 ja x = −3, joten ratkaisuja on kaksi."],
        "esim. |x + 3| = 0", {"x0": -3})
    # 4: only solution x = 5, different form
    add(start + 3, "H", "Kirjoita itseisarvoyhtälö, jonka ainoa ratkaisu on x = 5. Yhtälön ei saa olla muotoa |x − 5| = 0.", 5,
        ["|2x − 10| = 0", "|x| = |x − 10|", "|x − 1| = |x − 9|"],
        ["|x − 1| = 4", "|x − 3| = 2", "|x + 2| = 7"],
        ["Kun |a| = |b|, joko a = b tai a = −b. Yhtälössä |x| = |x − 10| tapaus x = x − 10 on mahdoton ja x = −(x − 10) antaa x = 5.",
         "Yhtälö |x − 1| = 4 antaa x = 5 ja x = −3."],
        "esim. |x| = |x − 10|", {"x0": 5})
    # 5: only solution x = 4, plausibility check
    add(start + 4, "H", "Kirjoita itseisarvoyhtälö, jonka ainoa ratkaisu on x = 4. Tarkista sijoittamalla, että yhtälö toteutuu, kun x = 4.", 4,
        ["|x − 4| = 0", "|x − 1| = |x − 7|", "|5x − 20| = 0"],
        ["|x − 4| = 3", "|x − 1| = 3", "|x + 2| = 6"],
        ["Esimerkki |x − 1| = |x − 7|: x − 1 = x − 7 on mahdoton ja x − 1 = −(x − 7) antaa x = 4.",
         "Tarkistus: |4 − 1| = 3 ja |4 − 7| = 3."],
        "esim. |x − 1| = |x − 7|", {"x0": 4})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
