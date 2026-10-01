#!/usr/bin/env python3
"""NUM-08 (successive percentage changes), type NE. Answers are computed with Fraction; the tagged wrong answer
treats a rise and a fall of the same percentage as cancelling (or subtracts the percentages directly)."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "num08_ne"
TID, CODE = "NUM-08", "NE"
BAD = ("Prosentit eivät kumoa toisiaan: jälkimmäinen prosentti lasketaan muuttuneesta arvosta, ei alkuperäisestä. "
       "Käytä muutoskertoimia, esimerkiksi 1,10 · 0,90 = 0,99.")
GOOD = "Oikein: muutoskertoimet kerrotaan keskenään, esimerkiksi 1,10 · 0,90 = 0,99."


def val(x):
    x = Fraction(x)
    return int(x) if x.denominator == 1 else float(x)


def make_items(run, date, count=5, start=1):
    rng = random.Random(1222)
    items = []
    for k in range(count):
        if k == 0:
            p = rng.choice([10, 20, 30, 40])
            f = (1 + Fraction(p, 100)) * (1 - Fraction(p, 100))
            ans, wrong = f * 100, [Fraction(100)]
            prompt = (f"Hinta nousee {p} % ja laskee sen jälkeen {p} %. Kuinka monta prosenttia alkuperäisestä hinnasta "
                      "lopullinen hinta on?")
            steps = [f"(1 + {p}/100) · (1 − {p}/100) = {float(f)}".replace(".", ","), f"Lopullinen hinta on {val(ans)} % alkuperäisestä".replace(".", ",")]
            level, params = "T", {"p": p, "form": k}
        elif k == 1:
            price, q = rng.choice([(80, 25), (200, 10), (50, 20), (150, 20)])
            ans = price * (1 + Fraction(q, 100)) * (1 - Fraction(q, 100))
            assert ans.denominator == 1 and ans != price
            wrong = [Fraction(price)]
            prompt = (f"Takin hinta on {price} €. Hintaa korotetaan {q} %, ja korotettua hintaa alennetaan sen jälkeen {q} %. "
                      "Mikä on lopullinen hinta euroina?")
            steps = [f"{price} · (1 + {q}/100) · (1 − {q}/100) = {val(ans)}"]
            level, params = "T", {"price": price, "q": q, "form": k}
        elif k == 2:
            n, q = rng.choice([(400, 25), (500, 20), (1000, 30)])
            ans = n * (1 - Fraction(q, 100)) * (1 + Fraction(q, 100))
            assert ans.denominator == 1 and ans != n
            wrong = [Fraction(n)]
            prompt = (f"Verkkokaupassa on {n} kävijää päivässä. Kävijämäärä laskee {q} % ja kasvaa sen jälkeen {q} %. "
                      "Kuinka monta kävijää päivässä on lopuksi?")
            steps = [f"{n} · (1 − {q}/100) · (1 + {q}/100) = {val(ans)}"]
            level, params = "T", {"n": n, "q": q, "form": k}
        elif k == 3:
            p = rng.choice([10, 20, 30, 40])
            f = (1 - Fraction(p, 100)) * (1 + Fraction(p, 100))
            ans, wrong = (1 - f) * 100, [Fraction(0)]
            prompt = (f"Hinta laskee {p} % ja nousee sen jälkeen {p} %. Kuinka monta prosenttiyksikköä lopullinen hinta on "
                      "alkuperäistä hintaa pienempi?")
            steps = [f"(1 − {p}/100) · (1 + {p}/100) = {float(f)}".replace(".", ","), f"100 % − {val(f * 100)} % = {val(ans)} prosenttiyksikköä".replace(".", ",")]
            level, params = "H", {"p": p, "form": k}
        else:
            p = rng.choice([25, 100, 150, 300])
            ans, wrong = Fraction(100 * p, 100 + p), [Fraction(p)]
            prompt = (f"Hinta nousee {p} %. Kuinka monta prosenttia korotetun hinnan pitää sen jälkeen laskea, jotta "
                      "hinta palaa alkuperäiseksi?")
            steps = [f"(1 + {p}/100) · (1 − x/100) = 1", f"x = {val(ans)}"]
            level, params = "H", {"p": p, "form": k}
            assert Fraction(ans) != Fraction(p) and Fraction(ans).denominator == 1
        wrong = [w for w in dict.fromkeys(wrong) if w != ans]
        payload = {"answer": {"kind": "number", "value": val(ans)},
                   "wrong": [{"match": val(w), "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, prompt, payload, steps,
                               str(val(ans)).replace(".", ","), GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
