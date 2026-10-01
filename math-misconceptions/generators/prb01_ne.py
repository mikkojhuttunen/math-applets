#!/usr/bin/env python3
"""PRB-01 (recency, gambler's fallacy), type NE. Answers are computed with Fraction; the typical wrong
answer is the value the \"it is due\" or \"it balances out\" belief gives."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "prb01_ne"
TID, CODE = "PRB-01", "NE"
BAD = ("Aiemmat tulokset eivät vaikuta seuraavaan: reilulla kolikolla, nopalla tai pyöräkkeellä ei ole muistia. "
       "Todennäköisyys on joka kerralla sama.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(902)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n = rng.choice([3, 4, 5])
            ans = Fraction(1, 2) * 100
            wrong = [100 * (1 - Fraction(1, 2) ** n)]
            prompt = (f"Reilua kolikkoa on heitetty {n} kertaa, ja joka kerta on tullut kruuna. "
                      "Kuinka monta prosenttia on todennäköisyys, että seuraavalla heitolla tulee klaava?")
            steps = ["Heitot ovat riippumattomia", "P(klaava) = 1/2 = 50 %"]
            params = {"streak": n}
        elif k == 1:
            m = rng.choice([9, 12, 15])
            ans = Fraction(6)
            wrong = [Fraction(1)]
            prompt = (f"Reilua noppaa on heitetty {m} kertaa, eikä kuutosta ole tullut kertaakaan. "
                      "Seuraavalla heitolla kuutosen todennäköisyys on 1/☐. Kirjoita nimittäjä.")
            steps = ["Heitot ovat riippumattomia", "P(6) = 1/6"]
            params = {"rolls": m}
        elif k == 2:
            s = rng.choice([10, 20, 5])
            ans = Fraction(100, s)
            wrong = [Fraction(100)]
            prompt = (f"Pyörässä on {s} yhtä suurta sektoria, ja niistä yksi on sininen. "
                      f"Pyörä on pyöräytetty {s - 1} kertaa, eikä sininen ole tullut kertaakaan. "
                      "Kuinka monta prosenttia on todennäköisyys, että seuraavalla pyöräytyksellä tulee sininen?")
            steps = [f"P(sininen) = 1/{s}", f"1/{s} = {100 / s:g} %".replace(".", ",")]
            params = {"sectors": s}
        elif k == 3:
            tosses = rng.choice([100, 80, 60])
            streak = rng.choice([6, 8, 10])
            rest = tosses - streak
            ans = Fraction(rest, 2)
            wrong = [Fraction(tosses, 2) - streak]
            prompt = (f"Reilua kolikkoa heitetään yhteensä {tosses} kertaa. Ensimmäisistä {streak} heitosta "
                      f"jokainen on kruuna. Montako kruunaa odotetaan tulevan jäljellä olevista {rest} heitosta?")
            steps = [f"Jäljellä on {rest} heittoa", "Jokaisella heitolla P(kruuna) = 1/2", f"{rest} · 1/2 = {rest // 2}"]
            params = {"tosses": tosses, "streak": streak}
        else:
            n = rng.choice([4, 5, 6])
            ans = Fraction(50)
            wrong = [100 * Fraction(1, 2) ** (n + 1)]
            prompt = (f"Reilulla kolikolla on tullut {n} klaavaa peräkkäin. Kuinka monta prosenttia on todennäköisyys, "
                      "että myös seuraava heitto on klaava?")
            steps = ["Heitot ovat riippumattomia", "P(klaava) = 1/2 = 50 %"]
            params = {"streak": n, "same_side": True}
        assert all(w != ans for w in wrong) and ans.denominator == 1 or k == 0
        key = str(params) + str(k)
        assert key not in seen
        seen.add(key)
        fa = lambda x: float(x)
        payload = {"answer": {"kind": "number", "value": fa(ans)},
                   "wrong": [{"match": fa(w), "misconception": "PRB-01", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        final = str(int(ans))
        items.append(base_item(TID, CODE, start + k, ["S6.06"], ["T19"], 9, "T" if k < 3 else "H", prompt,
                               payload, steps, final, "Oikein: satunnaisilla toistoilla ei ole muistia.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
