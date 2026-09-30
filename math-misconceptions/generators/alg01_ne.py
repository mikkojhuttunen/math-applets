#!/usr/bin/env python3
"""ALG-01 (letter read as an object label), type NE (number entry).

Evaluate a price expression 'pa·x + pb·y' for given values; the label reading
gives the sum of the coefficients. All numbers computed, fixed seed.
"""
import random

from gen_common import base_item, cli

TEMPLATE = "alg01_ne"
TID, CODE = "ALG-01", "NE"
# (noun A partitive, noun B partitive, letter A, letter B, unit)
CTX = [
    ("pulla", "pirtelö", "p", "k", "euroa"),
    ("vihko", "kynä", "v", "k", "euroa"),
    ("elokuvalippu", "karkkipussi", "l", "p", "euroa"),
    ("tarra", "kortti", "t", "k", "euroa"),
    ("omena", "banaani", "o", "b", "euroa"),
]


def make_items(run, date, count=5, start=1):
    rng = random.Random(102)
    items = []
    for k in range(count):
        na, nb, la, lb, unit = CTX[k]
        ca, cb = rng.randint(2, 5), rng.randint(2, 5)
        while cb == ca:
            cb = rng.randint(2, 5)
        va, vb = rng.randint(2, 4), rng.randint(2, 4)
        while vb == va:
            vb = rng.randint(2, 4)
        value = ca * va + cb * vb
        labels = ca + cb            # label reading: 'ca apples + cb pears'
        swapped = ca * vb + cb * va  # coefficients paired with the wrong letter
        if k < 3:
            level, pay = "T", 0
            prompt = (f"Kaupassa {na} maksaa {ca} euroa ja {nb} {cb} euroa. Ostetaan {la} kpl ensimmäistä ja {lb} kpl toista tuotetta, "
                      f"jolloin hinta euroina on {ca}{la} + {cb}{lb}. Laske hinta, kun {la} = {va} ja {lb} = {vb}.")
            answer = value
            wrong = [(labels, "ALG-01", f"Kirjaimet ovat lukuja, ei esineiden nimiä. Sijoita {la} = {va} ja {lb} = {vb}: {ca} · {va} + {cb} · {vb}."),
                     (swapped, None, f"Tarkista, kumpi kirjain kuuluu kummankin luvun perään: {ca}{la} ja {cb}{lb}.")]
            steps = [f"{ca}{la} + {cb}{lb} = {ca} · {va} + {cb} · {vb}", f"= {ca * va} + {cb * vb}", f"= {value}"]
        else:
            level, pay = "H", 20 + 5 * k
            prompt = (f"Kaupassa {na} maksaa {ca} euroa ja {nb} {cb} euroa. Kun ostetaan {la} kpl ensimmäistä ja {lb} kpl toista tuotetta, "
                      f"hinta euroina on {ca}{la} + {cb}{lb}. Ostetaan {va} kpl ensimmäistä ja {vb} kpl toista, ja maksetaan {pay} euron setelillä. "
                      "Paljonko vaihtorahaa saadaan euroina?")
            answer = pay - value
            wrong = [(pay - labels, "ALG-01", "Kirjaimet ovat lukuja (kappalemääriä), ei esineiden nimiä. Laske hinta: " + f"{ca} · {va} + {cb} · {vb}."),
                     (value, None, "Tämä on ostosten hinta. Vaihtoraha on maksettu summa miinus hinta.")]
            steps = [f"Hinta: {ca} · {va} + {cb} · {vb} = {value}", f"Vaihtoraha: {pay} {chr(0x2212)} {value} = {answer}"]
        assert answer > 0 and all(w[0] != answer for w in wrong)
        assert len({w[0] for w in wrong}) == len(wrong)
        payload = {"answer": {"kind": "number", "value": answer},
                   "wrong": [{"match": w, "misconception": m, "feedback": f} for w, m, f in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T15", "T7"], 7, level, prompt, payload,
                               steps, str(answer), "Oikein: sijoita luvut kirjainten paikalle ja laske.",
                               TEMPLATE, {"ca": ca, "cb": cb, "va": va, "vb": vb, "pay": pay}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
