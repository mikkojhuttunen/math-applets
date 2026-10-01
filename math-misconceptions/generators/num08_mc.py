#!/usr/bin/env python3
"""NUM-08 (successive percentage changes), type MC. Results are computed with Fraction; the tagged wrong option
assumes that a rise and a fall of the same percentage cancel."""
import random
from fractions import Fraction

from gen_common import base_item, cli, mc_options

TEMPLATE = "num08_mc"
TID, CODE = "NUM-08", "MC"
BAD = ("Prosentit eivät kumoa toisiaan: jälkimmäinen prosentti lasketaan muuttuneesta arvosta, ei alkuperäisestä. "
       "Esimerkiksi +10 % ja −10 % antaa 1,10 · 0,90 = 0,99.")
GOOD = "Oikein: muutoskertoimet kerrotaan keskenään, esimerkiksi 1,10 · 0,90 = 0,99."


def fmt(x):
    """Fraction or int as Finnish decimal text."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = f"{float(x):.4f}".rstrip("0").rstrip(".")
    assert Fraction(s) == x, "not a short decimal"
    return s.replace(".", ",")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1221)
    items = []
    for k in range(count):
        if k == 0:
            p = rng.choice([10, 20, 30])
            f = (1 + Fraction(p, 100)) * (1 - Fraction(p, 100))
            prompt = (f"Verkkokaupan kävijämäärä kasvaa {p} % ja laskee sen jälkeen {p} %. "
                      "Alkutilanteeseen verrattuna kävijämäärä on:")
            correct = (f"Pienempi: {fmt(f * 100)} % alkuarvosta", GOOD)
            wrongs = [("Sama kuin alussa", TID, BAD), (f"Suurempi kuin alussa", None, "Lasku on suurempi kuin nousu, koska se kohdistuu suurempaan arvoon."),
                      (f"Pienempi: {2 * p} % alkuarvosta", None, "Prosentteja ei lasketa yhteen tai kerrota luvulla kaksi.")]
            steps = [f"1,{p // 10} · 0,{10 - p // 10} = {fmt(f)}", f"{fmt(f * 100)} % alkuarvosta"]
            level, params = "T", {"p": p, "form": k}
            final = f"{fmt(f * 100)} % alkuarvosta"
        elif k == 1:
            price, q = rng.choice([(80, 25), (200, 10), (50, 20), (150, 20)])
            up = price * (1 + Fraction(q, 100))
            fin = up * (1 - Fraction(q, 100))
            assert fin.denominator == 1 and fin != price
            prompt = (f"Takin hinta on {price} €. Hintaa korotetaan {q} %, ja korotettua hintaa alennetaan sen jälkeen {q} %. "
                      "Mikä on lopullinen hinta?")
            correct = (f"{fmt(fin)} €", GOOD)
            wrongs = [(f"{price} €", TID, BAD), (f"{fmt(up)} €", None, "Tämä on hinta korotuksen jälkeen, alennus puuttuu."),
                      (f"{fmt(price * (1 - Fraction(2 * q, 100)))} €", None, "Alennus lasketaan korotetusta hinnasta, ei alkuperäisestä.")]
            steps = [f"{price} · {fmt(1 + Fraction(q, 100))} = {fmt(up)}", f"{fmt(up)} · {fmt(1 - Fraction(q, 100))} = {fmt(fin)}"]
            level, params = "T", {"price": price, "q": q, "form": k}
            final = f"{fmt(fin)} €"
        elif k == 2:
            p = rng.choice([20, 25, 40])
            f = (1 - Fraction(p, 100)) * (1 + Fraction(p, 100))
            prompt = (f"Puhelimen hinta laskee {p} % ja nousee sen jälkeen {p} %. "
                      "Alkuperäiseen hintaan verrattuna lopullinen hinta on:")
            correct = (f"Pienempi: {fmt(f * 100)} % alkuperäisestä", GOOD)
            wrongs = [("Sama kuin alkuperäinen", TID, BAD), ("Suurempi kuin alkuperäinen", None, "Nousu kohdistuu pienentyneeseen hintaan, joten se on pienempi muutos euroina kuin lasku."),
                      (f"Pienempi: {100 - 2 * p} % alkuperäisestä", None, "Prosentteja ei lasketa yhteen.")]
            steps = [f"{fmt(1 - Fraction(p, 100))} · {fmt(1 + Fraction(p, 100))} = {fmt(f)}", f"{fmt(f * 100)} % alkuperäisestä"]
            level, params = "T", {"p": p, "form": k}
            final = f"{fmt(f * 100)} % alkuperäisestä"
        elif k == 3:
            p = rng.choice([10, 20, 30])
            f = (1 + Fraction(p, 100)) * (1 - Fraction(p, 100))
            prompt = (f"Aino korottaa tuotteen hintaa {p} % ja alentaa sitten {p} %. Eero alentaa saman tuotteen hintaa {p} % ja "
                      f"korottaa sitten {p} %. Kummallakin on sama alkuhinta. Mikä väite on oikein?")
            correct = (f"Lopulliset hinnat ovat yhtä suuret, ja kumpikin on {fmt(f * 100)} % alkuhinnasta", GOOD)
            wrongs = [("Lopulliset hinnat ovat yhtä suuret ja yhtä suuret kuin alkuhinta", TID, BAD),
                      ("Ainon lopullinen hinta on suurempi", None, "Kertolasku ei riipu järjestyksestä: 1,10 · 0,90 = 0,90 · 1,10."),
                      ("Eeron lopullinen hinta on suurempi", None, "Kertolasku ei riipu järjestyksestä: 1,10 · 0,90 = 0,90 · 1,10.")]
            steps = [f"Aino: {fmt(1 + Fraction(p, 100))} · {fmt(1 - Fraction(p, 100))} = {fmt(f)}",
                     f"Eero: {fmt(1 - Fraction(p, 100))} · {fmt(1 + Fraction(p, 100))} = {fmt(f)}"]
            level, params = "H", {"p": p, "form": k}
            final = "Yhtä suuret, " + f"{fmt(f * 100)} % alkuhinnasta"
        else:
            p = rng.choice([20, 30, 50])
            prompt = f"Miksi hinta ei palaa alkuperäiseen, kun sitä korotetaan {p} % ja alennetaan sen jälkeen {p} %?"
            correct = ("Koska alennus lasketaan korotetusta hinnasta, joka on suurempi kuin alkuperäinen", GOOD)
            wrongs = [("Hinta palaa alkuperäiseen, koska prosentit ovat yhtä suuret", TID, BAD),
                      (f"Koska {p} % on aina {p} euroa", None, "Prosentti on osuus, ei kiinteä eurosumma; sen suuruus riippuu siitä, mistä arvosta se lasketaan."),
                      ("Koska prosentteja ei voi laskea peräkkäin", None, "Prosentit voidaan laskea peräkkäin kertomalla muutoskertoimet.")]
            f = (1 + Fraction(p, 100)) * (1 - Fraction(p, 100))
            steps = [f"{fmt(1 + Fraction(p, 100))} · {fmt(1 - Fraction(p, 100))} = {fmt(f)} ≠ 1"]
            level, params = "H", {"p": p, "form": k}
            final = "Alennus lasketaan suuremmasta arvosta"
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
