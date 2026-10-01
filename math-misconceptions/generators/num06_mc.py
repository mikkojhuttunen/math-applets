#!/usr/bin/env python3
"""NUM-06 (no number between 0,3 and 0,4), type MC. Midpoints are computed with Decimal and checked to lie strictly between."""
import random
from decimal import Decimal

from gen_common import base_item, cli, mc_options
from gen_decimal import fmt as _fmt

TEMPLATE = "num06_mc"
TID, CODE = "NUM-06", "MC"
BAD = ("Desimaalilukujen välistä löytyy aina uusia lukuja: lisää desimaali tai laske keskiarvo "
       "(0,3 ja 0,4 välissä ovat esimerkiksi 0,35 ja 0,305).")


def fmt(d):
    return _fmt(d.normalize() if d != 0 else d)


def mid(a, b):
    m = (a + b) / 2
    assert a < m < b
    return m


def make_items(run, date, count=5, start=1):
    rng = random.Random(701)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a = Decimal(rng.randint(1, 8)) / 10
            b = a + Decimal("0.1")
            m = mid(a, b)
            prompt = f"Montako lukua on lukujen {fmt(a)} ja {fmt(b)} välissä?"
            correct = ("Äärettömän monta", f"Oikein: esimerkiksi {fmt(m)}, {fmt(a + Decimal('0.01'))} ja {fmt(a + Decimal('0.001'))} ovat välissä, ja uusia löytyy aina.")
            wrongs = [("Ei yhtään", "NUM-06", BAD), (f"Vain yksi, {fmt(m)}", "NUM-06", BAD),
                      ("Yhdeksän", "NUM-06", BAD)]
            steps = [f"Keskiarvo ({fmt(a)} + {fmt(b)}) / 2 = {fmt(m)} on välissä", "Samalla tavalla löytyy aina uusi luku"]
            final, params, key, level = "Äärettömän monta", {"a": fmt(a), "b": fmt(b)}, (a, b, "n"), "T"
        elif k == 1:
            a = Decimal(rng.randint(10, 80)) / 10 + Decimal("0.05") * 0
            a = Decimal(rng.randint(11, 59)) / 10
            b = a + Decimal("0.1")
            m = mid(a, b)
            outs = [a - Decimal("0.1"), b + Decimal("0.1"), a]
            prompt = f"Mikä seuraavista luvuista on lukujen {fmt(a)} ja {fmt(b)} välissä?"
            correct = (fmt(m), f"Oikein: {fmt(a)} < {fmt(m)} < {fmt(b)}.")
            wrongs = [(fmt(outs[0]), None, f"Luku {fmt(outs[0])} on pienempi kuin {fmt(a)}."),
                      (fmt(outs[1]), None, f"Luku {fmt(outs[1])} on suurempi kuin {fmt(b)}."),
                      (f"Mikään ei ole, koska {fmt(a)} ja {fmt(b)} ovat peräkkäiset luvut", "NUM-06", BAD)]
            steps = [f"({fmt(a)} + {fmt(b)}) / 2 = {fmt(m)}", f"{fmt(a)} < {fmt(m)} < {fmt(b)}"]
            final, params, key, level = fmt(m), {"a": fmt(a), "b": fmt(b)}, (a, b, "m"), "T"
        elif k == 2:
            a = Decimal(rng.randint(40, 90)) / 10 + Decimal("0.0")
            a = Decimal(rng.randint(41, 49)) / 10
            b = a + Decimal("0.1")
            m = mid(a, b)
            prompt = (f"Kaksi lankaa on {fmt(a)} cm ja {fmt(b)} cm pitkiä. Voiko olla lankaa, jonka pituus on näiden välissä?")
            correct = (f"Voi, esimerkiksi {fmt(m)} cm, ja tällaisia pituuksia on äärettömän monta", f"Oikein: {fmt(a)} < {fmt(m)} < {fmt(b)}.")
            wrongs = [(f"Ei voi, koska {fmt(a)} ja {fmt(b)} ovat peräkkäiset luvut", "NUM-06", BAD),
                      (f"Voi, mutta vain yksi, {fmt(m)} cm", "NUM-06", BAD),
                      ("Voi vain, jos pituus mitataan millimetrin tarkkuudella", None, "Pituuksia on välissä aina, vaikka mittaustarkkuus rajoittaisi mittaamista.")]
            steps = [f"({fmt(a)} + {fmt(b)}) / 2 = {fmt(m)}"]
            final, params, key, level = "Voi", {"a": fmt(a), "b": fmt(b), "context": "lanka"}, (a, b, "c"), "T"
        elif k == 3:
            b = Decimal(rng.randint(2, 9)) / 10
            prompt = f"Mikä on suurin luku, joka on pienempi kuin {fmt(b)}?"
            n1 = b - Decimal("0.01")
            n2 = b - Decimal("0.001")
            correct = ("Sellaista ei ole, koska lukua lähempänä " + fmt(b) + " voi aina löytää", "Oikein: jos luku on pienempi kuin " + fmt(b) + ", sen ja " + fmt(b) + " väliltä löytyy suurempi.")
            wrongs = [(fmt(n1), "NUM-06", BAD), (fmt(n2), "NUM-06", BAD),
                      (fmt(b - Decimal("0.1")), "NUM-06", BAD)]
            assert n1 < b and n2 < b
            steps = [f"{fmt(n2)} < {fmt((n2 + b) / 2)} < {fmt(b)}", "Aina löytyy suurempi luku"]
            final, params, key, level = "Sellaista lukua ei ole", {"b": fmt(b)}, (b, "s"), "H"
        else:
            a = Decimal(rng.randint(1, 8)) / 10
            b = a + Decimal("0.1")
            prompt = f"Miten voit löytää aina uuden luvun lukujen {fmt(a)} ja {fmt(b)} väliltä? Valitse paras tapa."
            correct = ("Lasketaan lukujen keskiarvo", "Oikein: keskiarvo on aina lukujen välissä.")
            m = mid(a, b)
            wrongs = [(f"Lisätään lukuun {fmt(a)} pienin mahdollinen desimaali, joten välissä ei ole lukuja", "NUM-06", BAD),
                      (f"Lisätään luvut yhteen: {fmt(a)} + {fmt(b)} = {fmt(a + b)}", None, "Summa ei ole välissä: se on suurempi kuin pienempi luku ja usein suurempi kuin molemmat."),
                      ("Sellaista lukua ei löydy, koska luvut ovat peräkkäiset", "NUM-06", BAD)]
            steps = [f"({fmt(a)} + {fmt(b)}) / 2 = {fmt(m)}", f"{fmt(a)} < {fmt(m)} < {fmt(b)}"]
            final, params, key, level = "Keskiarvo", {"a": fmt(a), "b": fmt(b), "justify": True}, (a, b, "j"), "H"
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.08"], ["T12"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: kahden luvun välissä on aina äärettömän monta lukua.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
