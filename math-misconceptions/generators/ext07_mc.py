#!/usr/bin/env python3
"""EXT-07 (area unit conversion: 1 m² = 100 cm²), type MC. Options are computed from the exact area factor
(1 m² = 10 000 cm²); the tagged distractor uses the length factor 100."""
import random
from decimal import Decimal

from gen_common import base_item, cli, mc_options

TEMPLATE = "ext07_mc"
TID, CODE = "EXT-07", "MC"
BAD = ("Pinta-alayksiköiden muuntokerroin on pituusyksikön kerroin toiseen potenssiin: "
       "1 m² = 1 m · 1 m = 100 cm · 100 cm = 10 000 cm².")
GOOD = "Oikein: 1 m² = 10 000 cm², koska 1 m = 100 cm ja 100 · 100 = 10 000."


def big(n):
    return f"{int(n):,}".replace(",", " ")


def d(x):
    return format(Decimal(x).normalize(), "f").replace(".", ",")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1808)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n = rng.choice([1, 2, 3])
            level = "T"
            prompt = f"Mikä on {n} m² neliösenttimetreinä?"
            ans = n * 10_000
            correct = (f"{big(ans)} cm²", GOOD)
            wrongs = [(f"{big(n * 100)} cm²", TID, BAD), (f"{big(n * 1000)} cm²", None, "Kerroin 1 000 ei ole oikea: 1 m² = 100 cm · 100 cm."),
                      (f"{big(n * 100_000)} cm²", None, "Kerroin on liian suuri: 1 m² = 100 cm · 100 cm = 10 000 cm².")]
            steps = [f"1 m² = 100 cm · 100 cm = 10 000 cm²", f"{n} · 10 000 = {big(ans)}"]
            params = {"n": n}
        elif k == 1:
            n = rng.choice([4, 5, 6])
            level = "T"
            prompt = f"Matto on {n} m² suuri. Mikä on sen pinta-ala neliösenttimetreinä?"
            ans = n * 10_000
            correct = (f"{big(ans)} cm²", GOOD)
            wrongs = [(f"{big(n * 100)} cm²", TID, BAD), (f"{big(n * 1000)} cm²", None, "Kerroin 1 000 ei ole oikea: 1 m² = 100 cm · 100 cm."),
                      (f"{big(n * 10)} cm²", None, "Kerroin on liian pieni: 1 m² = 10 000 cm².")]
            steps = ["1 m² = 10 000 cm²", f"{n} · 10 000 = {big(ans)}"]
            params = {"n": n}
        elif k == 2:
            n = rng.choice([3, 5, 7])
            level = "T"
            prompt = f"Mikä on {big(n * 10_000)} cm² neliömetreinä?"
            correct = (f"{n} m²", "Oikein: 10 000 cm² = 1 m², joten jaetaan luvulla 10 000.")
            wrongs = [(f"{big(n * 100)} m²", TID, BAD), (f"{d(Decimal(n) / 10)} m²", None, "Jaettiin liian pienellä luvulla: 1 m² on 10 000 cm²."),
                      (f"{big(n * 10)} m²", None, "Suunta on väärä: neliömetri on suurempi yksikkö kuin neliösenttimetri.")]
            steps = ["10 000 cm² = 1 m²", f"{big(n * 10_000)} ÷ 10 000 = {n}"]
            params = {"cm2": n * 10_000}
            ans = n
        elif k == 3:
            level = "H"
            prompt = ("Oppilas sanoo: \"1 m = 100 cm, joten 1 m² = 100 cm².\" Mikä perustelu osoittaa, että "
                      "päätelmä on virheellinen?")
            correct = ("Neliö, jonka sivu on 1 m, on 100 cm · 100 cm = 10 000 cm²", GOOD)
            wrongs = [("Päätelmä on oikea, koska 1 m = 100 cm", TID, BAD),
                      ("Päätelmä on virheellinen, koska 1 m² = 1 000 cm²", None, "Pinta-alassa on kaksi ulottuvuutta, joten kerroin on 100 · 100 = 10 000, ei 1 000."),
                      ("Päätelmä on virheellinen, koska 1 m on 10 cm", None, "1 m = 100 cm on oikein. Virhe on siinä, että pinta-alassa kerroin otetaan kahdesti.")]
            steps = ["1 m² = 1 m · 1 m = 100 cm · 100 cm = 10 000 cm²"]
            params = {}
            ans = None
        else:
            n = rng.choice([0.5, 1.5])
            level = "H"
            cm2 = rng.choice([3_000, 4_000]) if n == 0.5 else 12_000
            big_cm2 = int(Decimal(str(n)) * 10_000)
            assert big_cm2 > cm2
            prompt = f"Kumpi on suurempi: {d(n)} m² vai {big(cm2)} cm²?"
            correct = (f"{d(n)} m² on suurempi, koska se on {big(big_cm2)} cm²",
                       f"Oikein: {d(n)} m² = {big(big_cm2)} cm² > {big(cm2)} cm².")
            wrongs = [(f"{big(cm2)} cm² on suurempi, koska {d(n)} m² on vain {d(Decimal(str(n)) * 100)} cm²", TID, BAD),
                      ("Ne ovat yhtä suuret", None, f"{d(n)} m² = {big(big_cm2)} cm², joka ei ole {big(cm2)} cm²."),
                      (f"{big(cm2)} cm² on suurempi, koska luku {big(cm2)} on suurempi kuin {d(n)}", None,
                       "Lukuja ei voi verrata ennen kuin yksiköt on muunnettu samaksi.")]
            steps = [f"{d(n)} m² = {d(n)} · 10 000 cm² = {big(big_cm2)} cm²", f"{big(big_cm2)} > {big(cm2)}"]
            params = {"m2": n, "cm2": cm2}
            ans = None
        assert (k, str(params)) not in seen
        seen.add((k, str(params)))
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S5.14"], ["T18"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, correct[0], GOOD, TEMPLATE,
                               params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
