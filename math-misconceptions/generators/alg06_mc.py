#!/usr/bin/env python3
"""ALG-06 (operational reading of '='), type MC. Fixed seed, options computed from the numbers."""
import random

from gen_common import MINUS, base_item, cli, mc_options

TEMPLATE = "alg06_mc"
TID, CODE = "ALG-06", "MC"
OP = "Yhtäsuuruusmerkki ei tarkoita 'laske tulos tähän'. Se kertoo, että molemmat puolet ovat yhtä suuret."


def make_items(run, date, count=5, start=1):
    rng = random.Random(201)
    items = []
    for k in range(count):
        a, b, c = rng.randint(3, 9), rng.randint(3, 9), rng.randint(2, 7)
        while len({a, b, c}) < 3:
            a, b, c = rng.randint(3, 9), rng.randint(3, 9), rng.randint(2, 7)
        s = a + b
        if k < 3:
            level = "T"
            blank_left = k == 2
            prompt = (f"Mikä luku kuuluu laatikkoon? {c} + □ = {a} + {b}" if blank_left else
                      f"Mikä luku kuuluu laatikkoon? {a} + {b} = □ + {c}")
            ans = s - c
            cand = [(s, "ALG-06", OP), (s + c, "ALG-06", OP), (abs(a - c), None, "Tarkista: molempien puolten summan on oltava sama.")]
            if blank_left:
                steps = [f"Oikea puoli: {a} + {b} = {s}", f"{c} + □ = {s}", f"□ = {s} {MINUS} {c} = {ans}"]
            else:
                steps = [f"Vasen puoli: {a} + {b} = {s}", f"□ + {c} = {s}", f"□ = {s} {MINUS} {c} = {ans}"]
            options, cid = mc_options(rng, (str(ans), "Oikein: puolten on oltava yhtä suuret."),
                                      [(str(v), m, f) for v, m, f in cand if v != ans])
            final = str(ans)
        elif k == 3:
            level = "H"
            d = rng.randint(2, 6)
            t = s + d
            prompt = f"Oppilas kirjoittaa: {a} + {b} = {s} + {d} = {t}. Miksi merkintä on virheellinen?"
            options, cid = mc_options(rng, (f"{a} + {b} ei ole yhtä suuri kuin {t}, vaikka merkintä väittää niin", "Oikein: jokaisen '=' molempien puolten on oltava yhtä suuret."), [
                ("Merkintä on oikein: tulos kirjoitetaan aina yhtäsuuruusmerkin jälkeen", "ALG-06", OP),
                (f"Luvun {s} pitäisi olla suluissa", None, "Sulut eivät korjaa ongelmaa: väite on epätosi."),
                ("Yhtäsuuruusmerkkiä ei saa käyttää kahdesti", None, "Merkkiä saa käyttää monta kertaa, jos jokainen väite on tosi."),
            ])
            steps = [f"{a} + {b} = {s} on tosi", f"{s} + {d} = {t} on tosi", f"Ketjusta seuraisi {a} + {b} = {t}, mutta {s} ≠ {t}"]
            final = "Jokaisen yhtäsuuruusmerkin molempien puolten on oltava yhtä suuret"
        else:
            level = "H"
            prompt = (f"Vaa'an vasemmassa kupissa on {a} kg:n ja {b} kg:n painot ja oikeassa kupissa {c} kg:n paino. "
                      f"Paljonko oikeaan kuppiin on lisättävä, jotta vaaka on tasapainossa? ({a} + {b} = {c} + □)")
            ans = s - c
            options, cid = mc_options(rng, (f"{ans} kg", "Oikein: molempien kuppien painojen on oltava yhtä suuret."), [
                (f"{s} kg", "ALG-06", OP),
                (f"{s + c} kg", "ALG-06", OP),
                (f"{c} kg", None, "Oikean kupin paino on jo annettu; kysytään lisäystä."),
            ])
            steps = [f"Vasen kuppi: {a} + {b} = {s} kg", f"Oikea kuppi: {c} + □ = {s}", f"□ = {s} {MINUS} {c} = {ans}"]
            final = f"{ans} kg"
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps, final,
                               "Oikein: yhtäsuuruusmerkki kertoo, että puolet ovat yhtä suuret.", TEMPLATE,
                               {"a": a, "b": b, "c": c}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
