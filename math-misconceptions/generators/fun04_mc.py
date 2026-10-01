#!/usr/bin/env python3
"""FUN-04 (a function must have a formula or change), type MC. A constant relation is a function: every x gives
exactly one y. Numbers in the options come from the same parameters as the stem."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "fun04_mc"
TID, CODE = "FUN-04", "MC"
BAD = ("Funktion määritelmä vaatii vain, että jokaista x:n arvoa vastaa täsmälleen yksi y:n arvo. "
       "Arvon ei tarvitse muuttua eikä lausekkeessa tarvitse olla x:ää.")
GOOD = "Oikein: funktiossa jokaista x:n arvoa vastaa täsmälleen yksi y:n arvo, vaikka se olisi aina sama."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1251)
    items = []
    for k in range(count):
        if k == 0:
            c = rng.choice([3, 5, 7, 9])
            prompt = f"Onko y = {c} funktio, kun x voi olla mikä tahansa luku?"
            correct = (f"On, koska jokaista x:n arvoa vastaa täsmälleen yksi y:n arvo, nimittäin {c}", GOOD)
            wrongs = [("Ei ole, koska y ei muutu x:n mukana", TID, BAD),
                      ("Ei ole, koska lausekkeessa ei ole x:ää", TID, BAD),
                      (f"On, mutta vain jos x = {c}", None, "Funktio on määritelty kaikille x:n arvoille, ei vain yhdelle.")]
            steps = [f"Kun x = 1, y = {c}; kun x = 2, y = {c}", f"Jokaista x:n arvoa vastaa täsmälleen yksi y:n arvo {c}"]
            final, level, params = "On funktio", "T", {"c": c, "form": k}
        elif k == 1:
            fee = rng.choice([9, 12, 15, 20])
            prompt = (f"Kuntosalin kuukausimaksu on {fee} € riippumatta siitä, kuinka monta kertaa käyt salilla. "
                      "Onko kuukausimaksu käyntikertojen funktio?")
            correct = (f"On: jokaista käyntikertojen määrää vastaa täsmälleen yksi maksu, {fee} €", GOOD)
            wrongs = [("Ei ole, koska maksu ei muutu käyntikertojen mukana", TID, BAD),
                      ("Ei ole, koska käyntikertoja ei voi laskea lausekkeeseen", None, "Käyntikertojen määrä on funktion muuttuja, vaikka maksu ei siitä riipu."),
                      ("On vain, jos käyntikertoja on yli 10", None, "Funktio on määritelty kaikilla käyntikertamäärillä.")]
            steps = [f"0 käyntiä: {fee} €, 10 käyntiä: {fee} €", "Jokaista määrää vastaa yksi maksu, joten kyseessä on funktio"]
            final, level, params = "On funktio", "T", {"fee": fee, "form": k}
        elif k == 2:
            c, x0 = rng.choice([(7, 3), (4, 10), (6, 5)])
            prompt = f"Funktio on f(x) = {c}. Mikä on f({x0})?"
            correct = (str(c), GOOD)
            wrongs = [("Sitä ei voi laskea, koska lausekkeessa ei ole x:ää", TID, BAD),
                      (str(c * x0), None, f"Funktion arvo ei riipu x:stä: f(x) on aina {c}."),
                      (str(x0), None, f"f({x0}) ei ole {x0}, vaan lausekkeen arvo {c}.")]
            steps = [f"f(x) = {c} kaikilla x:n arvoilla", f"f({x0}) = {c}"]
            final, level, params = str(c), "T", {"c": c, "x0": x0, "form": k}
        elif k == 3:
            c = rng.choice([2, 3, 4])
            prompt = f"Funktion kuvaaja on vaakasuora suora y = {c}. Mitä siitä voi päätellä?"
            correct = (f"Se on funktion kuvaaja: jokaisella x:llä on täsmälleen yksi y:n arvo, {c}", GOOD)
            wrongs = [("Se ei ole funktion kuvaaja, koska y ei muutu", TID, BAD),
                      ("Se on funktion kuvaaja vain, jos suora nousee", None, "Funktion ei tarvitse olla nouseva."),
                      ("Se ei ole funktion kuvaaja, koska se on suora eikä käyrä", None, "Suora voi olla funktion kuvaaja.")]
            steps = ["Pystysuora suora leikkaa kuvaajan täsmälleen kerran jokaisella x:llä", "Siis kyseessä on funktio"]
            final, level, params = "Funktion kuvaaja", "H", {"c": c, "form": k}
        else:
            c = rng.choice([4, 5, 8])
            prompt = (f"Oppilas väittää: \"y = {c} ei ole funktio, koska siinä ei ole x:ää eikä y muutu.\" "
                      "Mikä väitteen perustelussa on virheellistä?")
            correct = ("Funktio vaatii vain, että jokaista x:n arvoa vastaa täsmälleen yksi y; muuttuminen ei ole vaatimus", GOOD)
            wrongs = [("Mikään, väite on oikein", TID, BAD),
                      ("Se, että y on kokonaisluku", None, "Funktion arvon laji ei ratkaise sitä, onko kyseessä funktio."),
                      ("Se, että funktiossa pitää olla kaksi muuttujaa", None, "Funktiossa on yksi riippumaton muuttuja.")]
            steps = ["Funktion määritelmä: jokaista x:ää vastaa täsmälleen yksi y", f"y = {c} täyttää määritelmän"]
            final, level, params = "Muuttuminen ei ole funktion vaatimus", "H", {"c": c, "form": k}
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S4.04"], ["T15"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
