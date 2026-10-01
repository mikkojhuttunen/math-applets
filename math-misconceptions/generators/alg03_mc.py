#!/usr/bin/env python3
"""ALG-03 (value from alphabet position), type MC. The solution is computed from the equation; the tagged wrong
option is the letter's position in the alphabet. Letters are chosen so that the position differs from the solution."""
import random

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "alg03_mc"
TID, CODE = "ALG-03", "MC"
BAD = ("Kirjaimen paikka aakkosissa ei vaikuta sen arvoon. Kirjain on tuntematon luku, jonka arvo ratkaistaan "
       "yhtälöstä.")
GOOD = "Oikein: kirjaimen arvo ratkaistaan yhtälöstä, ei aakkospaikasta."
LETTERS = "kmnptwyd"


def pos(ch):
    return ord(ch) - 96


def make_items(run, date, count=5, start=1):
    rng = random.Random(301)
    items, used = [], set()
    for k in range(count):
        while True:
            ch = rng.choice(LETTERS)
            if ch not in used:
                break
        used.add(ch)
        p = pos(ch)
        v = rng.choice([x for x in range(3, 13) if x != p])
        if k == 0:
            c = rng.choice([4, 5, 7, 8])
            prompt = f"{ch} + {c} = {v + c}. Mikä on {ch}?"
            correct = (str(v), f"Oikein: {v + c} {chr(8722)} {c} = {v}.")
            wrongs = [(str(p), TID, BAD), (str(v + 2 * c), None, f"Luku {c} on vähennettävä, ei lisättävä."),
                      (str(v + c), None, "Tämä on yhtälön oikea puoli, ei ratkaisu.")]
            steps = [f"{ch} + {c} = {v + c}", f"{ch} = {v + c} {chr(8722)} {c} = {v}"]
            final, level = str(v), "T"
        elif k == 1:
            c = rng.choice([2, 3, 4])
            prompt = f"{c}{ch} = {c * v}. Mikä on {ch}?"
            correct = (str(v), f"Oikein: {c * v} ÷ {c} = {v}.")
            wrongs = [(str(p), TID, BAD), (str(c * v * c), None, f"Kerroin {c} on jaettava pois, ei kerrottava."),
                      (str(c * v - c), None, f"Termi {c}{ch} tarkoittaa tuloa {c} · {ch}.")]
            steps = [f"{c}{ch} = {c * v}", f"{ch} = {c * v} ÷ {c} = {v}"]
            final, level = str(v), "T"
        elif k == 2:
            c = rng.choice([3, 4, 6])
            prompt = f"{ch} {chr(8722)} {c} = {v - c}. Mikä on {ch}?"
            correct = (str(v), f"Oikein: {v - c} + {c} = {v}.")
            wrongs = [(str(p), TID, BAD), (num(v - 2 * c), None, f"Luku {c} on lisättävä, ei vähennettävä."),
                      (num(c - (v - c)), None, "Tarkista vastauksen merkki.")]
            steps = [f"{ch} {chr(8722)} {c} = {v - c}", f"{ch} = {v - c} + {c} = {v}"]
            final, level = str(v), "T"
        elif k == 3:
            q = ch
            prompt = (f"Oppilas ratkaisee yhtälön {q} + 3 = {v + 3} ja kirjoittaa: ”{q} = {p}, koska {q} on aakkosten "
                      f"{p}. kirjain.” Mikä väite on oikein?")
            correct = (f"Väite on väärin: yhtälöstä saadaan {q} = {v}", GOOD)
            wrongs = [(f"Väite on oikein: {q} = {p}, koska kirjaimen paikka aakkosissa on sen arvo", TID, BAD),
                      (f"Väite on väärin: yhtälöstä saadaan {q} = {v + 6}", None, "Luku 3 on vähennettävä, ei lisättävä."),
                      ("Yhtälöllä ei ole ratkaisua", None, "Yhtälö on ratkaistavissa.")]
            steps = [f"{q} + 3 = {v + 3}", f"{q} = {v + 3} {chr(8722)} 3 = {v}", f"Tarkistus: {v} + 3 = {v + 3}"]
            final, level = f"{q} = {v}", "H"
        else:
            prompt = (f"Miksi yhtälössä {ch} + 2 = {v + 2} kirjaimen {ch} arvoa ei voi päätellä sen paikasta aakkosissa?")
            correct = ("Kirjain on tuntematon luku, jonka arvon määrää yhtälö, ei kirjaimen paikka aakkosissa", GOOD)
            wrongs = [(f"Sen voi päätellä: {ch} on aakkosten {p}. kirjain, joten {ch} = {p}", TID, BAD),
                      ("Siksi, että kirjaimet vaihtavat paikkaa aakkosissa", None, "Aakkosjärjestys ei liity kirjaimen arvoon."),
                      (f"Siksi, että {ch}:n arvo on aina {v + 2}", None, f"Luku {v + 2} on yhtälön oikea puoli, ei kirjaimen arvo.")]
            steps = [f"{ch} + 2 = {v + 2}", f"{ch} = {v}, eli arvo saadaan laskemalla yhtälöstä"]
            final, level = "Arvo ratkaistaan yhtälöstä", "H"
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T14", "T15"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE,
                               {"letter": ch, "position": p, "value": v, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
