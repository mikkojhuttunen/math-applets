#!/usr/bin/env python3
"""ALG-12 (subtraction of a negative number), type MC. The correct option is computed from the integers; the tagged
wrong option subtracts the absolute value (the result is smaller than the starting number, "subtracting makes smaller")."""
import random

from gen_common import MINUS, base_item, cli, mc_options, num

TEMPLATE = "alg12_mc"
TID, CODE = "ALG-12", "MC"
BAD = ("Negatiivisen luvun vähentäminen ei pienennä lukua. Vähentäminen on vastaluvun lisäämistä: "
       "a − (−b) = a + b.")
GOOD = "Oikein: negatiivisen luvun vähentäminen on sen vastaluvun lisäämistä, a − (−b) = a + b."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1201)
    items = []
    for k in range(count):
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        while b == a:
            b = rng.randint(2, 9)
        if k == 0:
            prompt, level = f"Laske {a} {MINUS} ({MINUS}{b}).", "T"
            good = a + b
            wr = [(a - b, TID, BAD), (-(a + b), None, "Tulos on väärän merkkinen: positiiviseen lukuun lisätään positiivinen luku."),
                  (a * b, None, "Tässä ei kerrota, vaan vähennetään.")]
            steps = [f"{a} {MINUS} ({MINUS}{b}) = {a} + {b} = {a + b}"]
        elif k == 1:
            prompt, level = f"Laske {MINUS}{a} {MINUS} ({MINUS}{b}).", "T"
            good = b - a
            wr = [(-(a + b), TID, BAD), (a + b, None, "Tarkista ensimmäisen luvun merkki."),
                  (a - b, None, "Tarkista tuloksen merkki.")]
            steps = [f"{MINUS}{a} {MINUS} ({MINUS}{b}) = {MINUS}{a} + {b} = {num(b - a)}"]
        elif k == 2:
            prompt, level = f"Lämpötila on {a} astetta. Mikä on lämpötilan ja lämpötilan {MINUS}{b} astetta erotus (ensimmäinen miinus toinen)?", "T"
            good = a + b
            wr = [(a - b, TID, BAD), (-(a + b), None, "Tulos on väärän merkkinen."), (b, None, "Tarkista laskutoimitus.")]
            steps = [f"{a} {MINUS} ({MINUS}{b}) = {a} + {b} = {a + b}"]
        elif k == 3:
            prompt = (f"Oppilas laskee {a} {MINUS} ({MINUS}{b}) = {a - b}, koska vähennyslasku pienentää lukua. "
                      f"Mikä väite on oikein?")
            level = "H"
            good = None
            correct = (f"Väite on väärin: {a} {MINUS} ({MINUS}{b}) = {a + b}", GOOD)
            wrongs = [(f"Väite on oikein: {a} {MINUS} ({MINUS}{b}) = {num(a - b)}", TID, BAD),
                      (f"Väite on väärin: {a} {MINUS} ({MINUS}{b}) = {num(-(a + b))}", None, "Tulos on väärän merkkinen."),
                      ("Laskua ei voi laskea", None, "Lasku voidaan laskea.")]
            steps = [f"{a} {MINUS} ({MINUS}{b}) = {a} + {b} = {a + b}", f"Tarkistus: {a + b} {MINUS} {a} = {b}"]
            final = f"{a} {MINUS} ({MINUS}{b}) = {a + b}"
        else:
            prompt = f"Miksi laskun {a} {MINUS} ({MINUS}{b}) tulos on suurempi kuin {a}?"
            level = "H"
            correct = ("Koska negatiivisen luvun vähentäminen on sen vastaluvun lisäämistä", GOOD)
            wrongs = [("Ei ole suurempi: vähentäminen pienentää lukua aina", TID, BAD),
                      (f"Koska {a} on aina suurempi kuin {b}", None, "Vertailu ei selitä tulosta; ratkaisevaa on vähennettävän luvun merkki."),
                      ("Koska kaksi miinusmerkkiä kumoaa toisensa vain kertolaskussa", None, "Vähennyslaskussa vähennettävän vastaluku lisätään.")]
            steps = [f"{a} {MINUS} ({MINUS}{b}) = {a} + {b} = {a + b} > {a}"]
            final = "Negatiivisen luvun vähentäminen on vastaluvun lisäämistä"
        if k < 3:
            correct = (num(good), GOOD)
            wrongs = [(num(w), t, f) for w, t, f in wr if w != good]
            final = num(good)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.01"], ["T10", "T11"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE,
                               {"a": a, "b": b, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
