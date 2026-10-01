#!/usr/bin/env python3
"""EXT-05 (Pythagorean theorem assumed to hold for every triangle), type MC. The squares and sums in the option
texts are computed from the side lengths; a triangle is right-angled exactly when a² + b² = c² for its longest
side c, and this is decided by code before the options are written."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "ext05_mc"
TID, CODE = "EXT-05", "MC"
BAD = ("Pythagoraan lause koskee vain suorakulmaista kolmiota. Muissa kolmioissa summa a² + b² ei yleensä ole c². "
       "Kokeile laskea neliöt ja vertaa.")
GOOD = "Oikein: Pythagoraan lause pätee vain suorakulmaisessa kolmiossa, ja käänteislause kertoo, milloin kulma on suora."


def is_right(a, b, c):
    s = sorted([a, b, c])
    return s[0] ** 2 + s[1] ** 2 == s[2] ** 2


def make_items(run, date, count=5, start=1):
    rng = random.Random(1505)
    items, seen = [], set()
    for k in range(count):
        if k in (0, 2):
            a, b, c = rng.choice([(5, 6, 8), (4, 5, 6), (7, 8, 10)]) if k == 0 else rng.choice([(3, 4, 6), (6, 7, 9)])
            assert not is_right(a, b, c)
            level = "T"
            ctx = "" if k == 0 else "Pellon sivut ovat "
            if k == 0:
                prompt = f"Kolmion sivut ovat {a}, {b} ja {c}. Onko kolmio suorakulmainen?"
            else:
                prompt = f"{ctx}{a} m, {b} m ja {c} m. Onko pellon nurkka suora?"
            s, t = a * a + b * b, c * c
            correct = (f"Ei, koska {a}² + {b}² = {s}, mutta {c}² = {t}", GOOD)
            wrongs = [(f"Kyllä, koska kolmiossa aina {a}² + {b}² = {c}²", TID, BAD),
                      (f"Kyllä, koska {a} + {b} > {c}", None,
                       "Epäyhtälö a + b > c kertoo vain, että kolmio on olemassa, ei sitä, onko kulma suora."),
                      ("Sitä ei voi päätellä sivujen pituuksista, vaan kulma pitää mitata", None,
                       "Käänteislauseella kulman voi päätellä sivuista: vertaa neliöiden summaa.")]
            steps = [f"{a}² + {b}² = {s}", f"{c}² = {t}", f"{s} ≠ {t}, joten kolmio ei ole suorakulmainen"]
            final = correct[0]
            params = {"a": a, "b": b, "c": c}
        elif k == 1:
            a, b = rng.choice([(6, 8), (5, 12)])
            h = int((a * a + b * b) ** 0.5)
            assert h * h == a * a + b * b
            level = "T"
            prompt = (f"Kolmiossa ABC sivut AC = {a} ja BC = {b}, ja kulma C on 60°. Oppilas laskee "
                      f"AB = √({a}² + {b}²) = {h}. Mikä on oikein?")
            correct = ("Lasku ei kelpaa, koska kulma C ei ole suora kulma", GOOD)
            wrongs = [(f"Lasku on oikein, koska a² + b² = c² pätee kaikissa kolmioissa, AB = {h}", TID, BAD),
                      (f"Oikea tulos on AB = {a + b}", None, "Kolmion sivun pituus ei ole kahden sivun summa."),
                      (f"Oikea tulos on AB = {b - a}", None, "Kolmion sivun pituus ei ole kahden sivun erotus.")]
            steps = ["Pythagoraan lause koskee vain suorakulmaista kolmiota",
                     "Kulma C on 60°, ei 90°, joten laskua ei voi käyttää"]
            final = correct[0]
            params = {"a": a, "b": b, "angle": 60}
        elif k == 3:
            a, b, c = rng.choice([(6, 7, 9), (5, 6, 7)])
            s, t = a * a + b * b, c * c
            assert s > t
            level = "H"
            prompt = (f"Kolmion sivut ovat {a}, {b} ja {c}. Lasketaan {a}² + {b}² = {s} ja {c}² = {t}. "
                      "Mitä tästä voi päätellä?")
            correct = ("Luvut eivät ole yhtä suuret, joten kolmio ei ole suorakulmainen", GOOD)
            wrongs = [(f"Luvut {s} ja {t} ovat lähellä toisiaan, joten kolmio on suorakulmainen", TID, BAD),
                      (f"Kolmio on suorakulmainen, koska {s} > {t}", TID, BAD),
                      (f"Kolmiota ei ole olemassa, koska {s} ≠ {t}", None,
                       "Kolmio on olemassa, kun kaksi lyhyempää sivua on yhteensä pisintä pidempi.")]
            steps = [f"{s} ≠ {t}", "Käänteislauseen mukaan kolmio on suorakulmainen vain, jos luvut ovat yhtä suuret"]
            final = correct[0]
            params = {"a": a, "b": b, "c": c}
        else:
            level = "H"
            a, b, c = 2, 3, 4
            assert not is_right(a, b, c)
            prompt = ("Oppilas väittää: \"Pythagoraan lause a² + b² = c² pätee jokaisessa kolmiossa.\" "
                      "Mikä esimerkki osoittaa väitteen vääräksi?")
            correct = (f"Kolmio, jonka sivut ovat {a}, {b} ja {c}, koska {a}² + {b}² = {a * a + b * b} ≠ {c * c}", GOOD)
            wrongs = [("Kolmio, jonka sivut ovat 3, 4 ja 5, koska 3² + 4² = 5²", TID,
                       "Tämä kolmio on suorakulmainen, joten se ei osoita väitettä vääräksi."),
                      ("Kolmio, jonka sivut ovat 6, 8 ja 10, koska 6² + 8² = 10²", TID,
                       "Tämä kolmio on suorakulmainen, joten se ei osoita väitettä vääräksi.")]
            steps = [f"{a}² + {b}² = {a * a + b * b}", f"{c}² = {c * c}", "Luvut eivät ole yhtä suuret, joten väite ei pidä"]
            final = correct[0]
            params = {"a": a, "b": b, "c": c, "variant": "counterexample"}
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S5.09"], ["T17"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
