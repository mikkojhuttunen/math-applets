#!/usr/bin/env python3
"""EXT-06 (sine read as a length; adjacent and opposite leg mixed up), type ES (error spotting). Lines are numeric
expressions built from Pythagorean triples (a opposite, b adjacent, h hypotenuse); lines before the error line are
equivalent to line 1 and the error line breaks equivalence. Injected errors: sine read as a length, adjacent leg used
for the sine, opposite leg used for the cosine, scaled numerator without the scaled hypotenuse."""
import random

from gen_common import base_item, cli

TEMPLATE = "ext06_es"
TID, CODE = "EXT-06", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = ("Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Sin α = vastainen kateetti / hypotenuusa, "
           "cos α = viereinen kateetti / hypotenuusa.")
GOOD = "Oikein: sini on vastainen kateetti jaettuna hypotenuusalla ja kosini viereinen kateetti jaettuna hypotenuusalla."
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15)]


def make_items(run, date, count=5, start=1):
    rng = random.Random(1721)
    items, seen = [], set()
    for k in range(count):
        a, b, h = rng.choice([t for t in TRIPLES if t not in seen])
        seen.add((a, b, h))
        assert a * a + b * b == h * h and a != b
        m = rng.choice([2, 3, 4])
        if k == 0:
            level, err = "T", 2
            intro = (f"Suorakulmaisessa kolmiossa kulman α vastainen kateetti on {a} cm ja hypotenuusa {h} cm. "
                     f"Oppilas laskee lausekkeen {m} · sin α arvoa. Rivi 1 on sijoitus.")
            lines = [f"{m} · {a}/{h}", f"{m} · {a}", f"{m * a}"]
            fix = f"Sini on suhdeluku {a}/{h}, ei sivun pituus {a}. Oikea rivi 2 on {m * a}/{h}."
            etype = "sine_as_length"
        elif k == 1:
            level, err = "T", 2
            intro = (f"Suorakulmaisessa kolmiossa kulman β vastainen kateetti on {b} cm, viereinen kateetti {a} cm ja "
                     f"hypotenuusa {h} cm. Oppilas laskee lausekkeen {m} · sin β arvoa. Rivi 1 on sijoitus.")
            lines = [f"{m} · {b}/{h}", f"{m} · {a}/{h}", f"{m * a}/{h}"]
            fix = f"Sinin osoittaja on vastainen kateetti {b}, ei viereinen {a}. Oikea rivi 2 on {m * b}/{h}."
            etype = "adjacent_for_opposite"
        elif k == 2:
            level, err = "T", 3
            intro = (f"Suorakulmaisessa kolmiossa kulman α viereinen kateetti on {b} cm, vastainen kateetti {a} cm ja "
                     f"hypotenuusa {h} cm. Oppilas laskee lausekkeen {m} · cos α arvoa. Rivi 1 on sijoitus.")
            lines = [f"{m} · {b}/{h}", f"{m * b}/{h}", f"{m * a}/{h}"]
            fix = f"Kosinin osoittaja on viereinen kateetti {b}, ei vastainen {a}. Oikea rivi 3 on {m * b}/{h}."
            etype = "opposite_for_adjacent"
        elif k == 3:
            level, err = "H", 3
            intro = (f"Suorakulmaisen kolmion sivut ovat {a} cm, {b} cm ja {h} cm, ja kulman α vastainen kateetti on "
                     f"{a} cm. Kolmio suurennetaan {m}-kertaiseksi. Oppilas laskee suurennetun kolmion sin α -arvon.")
            lines = [f"{m * a}/{m * h}", f"{m} · {a}/({m} · {h})", f"{m * a}/{h}"]
            fix = f"Myös hypotenuusa kasvaa {m}-kertaiseksi ({m * h}), joten sini ei muutu: {a}/{h}."
            etype = "scaled_numerator_only"
        else:
            level, err = "H", 2
            intro = (f"Tikkaat ovat {h} m pitkät ja ne yltävät {a} m korkeudelle seinällä. Oppilas laskee, paljonko "
                     f"hypotenuusa kertaa kulman sini on. Rivi 1 on sijoitus.")
            lines = [f"{h} · {a}/{h}", f"{h} · {b}/{h}", f"{b}"]
            fix = f"Vastainen kateetti on {a} m, joten sinin osoittajassa on {a}. Oikea tulos on {a}."
            etype = "adjacent_for_opposite"
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        items.append(base_item(TID, CODE, start + k, ["S5.10"], ["T17"], 9, level, f"{intro} {ASK}", payload,
                               [fix], f"Virhe on rivillä {err}", GOOD, TEMPLATE,
                               {"triple": [a, b, h], "m": m}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
