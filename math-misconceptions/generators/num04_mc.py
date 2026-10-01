#!/usr/bin/env python3
"""NUM-04 (multiplication always makes bigger), type MC. Comparisons are decided by Decimal arithmetic."""
import random
from decimal import Decimal

from gen_common import base_item, cli, mc_options
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)

TEMPLATE = "num04_mc"
TID, CODE = "NUM-04", "MC"
BAD = ("Kertolasku ei aina suurenna. Kun kerrotaan luvulla, joka on pienempi kuin 1, tulo on pienempi kuin toinen tekijä "
       "(esimerkiksi 0,5 × 8 on puolet luvusta 8).")


def make_items(run, date, count=5, start=1):
    rng = random.Random(601)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            f, n = Decimal(rng.choice(["0.5", "0.25", "0.4", "0.6"])), rng.choice([8, 12, 20, 15])
            p = f * n
            assert p < n
            prompt = f"Onko tulo {fmt(f)} × {n} suurempi vai pienempi kuin {n}?"
            correct = (f"Pienempi kuin {n}", f"Oikein: {fmt(f)} × {n} = {fmt(p)}, ja {fmt(p)} < {n}.")
            wrongs = [(f"Suurempi kuin {n}", "NUM-04", BAD), (f"Yhtä suuri kuin {n}", None, f"Kerroin {fmt(f)} ei ole 1, joten tulo ei ole {n}."),
                      ("Sitä ei voi tietää laskematta", None, "Kerroin on pienempi kuin 1, joten tuloksen suunnan voi päätellä.")]
            steps = [f"{fmt(f)} < 1", f"{fmt(f)} × {n} = {fmt(p)} < {n}"]
            final, params, key, level = f"Pienempi kuin {n}", {"factor": fmt(f), "n": n}, (f, n), "T"
        elif k == 1:
            price = rng.choice([20, 40, 60, 80])
            f = Decimal(rng.choice(["0.8", "0.75", "0.9", "0.6"]))
            new = f * price
            assert new < price
            prompt = (f"Takin hinta on {price} €. Alennuksessa hinta lasketaan kertolaskulla {fmt(f)} × {price}. "
                      f"Miten uusi hinta eroaa vanhasta?")
            correct = (f"Uusi hinta ({fmt(new)} €) on pienempi, koska kerroin {fmt(f)} on alle 1",
                       f"Oikein: {fmt(f)} × {price} = {fmt(new)}.")
            wrongs = [(f"Uusi hinta on suurempi, koska kertolasku suurentaa luvun", "NUM-04", BAD),
                      ("Uusi hinta on sama kuin vanha", None, "Kerroin ei ole 1, joten hinta muuttuu."),
                      (f"Uusi hinta on {fmt(f * price * 10)} €, koska kerroin luetaan kokonaislukuna", None,
                       "Kerroin on desimaaliluku: " + fmt(f) + " on pienempi kuin 1.")]
            steps = [f"{fmt(f)} × {price} = {fmt(new)}", f"{fmt(new)} < {price}"]
            final, params, key, level = f"{fmt(new)} €", {"factor": fmt(f), "price": price}, (f, price, "a"), "T"
        elif k == 2:
            n = rng.choice([30, 40, 50])
            small = Decimal(rng.choice(["0.4", "0.7", "0.9"]))
            bigs = rng.sample([Decimal(x) for x in ["1.2", "1.5", "2", "3"]], 3)
            prompt = f"Mikä seuraavista tuloista on pienempi kuin {n}?"
            cands = [small] + bigs
            assert [x * n < n for x in cands] == [True, False, False, False]
            correct = (f"{fmt(small)} × {n}", f"Oikein: {fmt(small)} × {n} = {fmt(small * n)} < {n}.")
            wrongs = [(f"{fmt(b)} × {n}", None, f"Kerroin {fmt(b)} > 1, joten tulo on suurempi kuin {n}.") for b in bigs[:2]]
            wrongs.append((f"Mikään tulo ei ole pienempi kuin {n}, koska kertolasku suurentaa", "NUM-04", BAD))
            steps = [f"{fmt(small)} < 1, joten {fmt(small)} × {n} < {n}"]
            final, params, key, level = f"{fmt(small)} × {n}", {"small": fmt(small), "n": n, "bigs": [fmt(b) for b in bigs[:2]]}, (small, n, "b"), "T"
        elif k == 3:
            f = Decimal(rng.choice(["0.6", "0.8", "0.35"]))
            n = rng.choice([25, 40, 20])
            p = f * n
            prompt = (f"Oppilas laskee {fmt(f)} × {n} = {fmt(p)} ja sanoo: \"Tulon piti olla suurempi kuin {n}, joten laskin väärin.\" "
                      f"Mikä väite on oikein?")
            correct = (f"Lasku on oikein: {fmt(f)} on pienempi kuin 1, joten tulo {fmt(p)} on pienempi kuin {n}",
                       "Oikein: tulo on pienempi kuin toinen tekijä, kun kerroin on alle 1.")
            wrongs = [(f"Lasku on väärin: tulon pitää olla suurempi kuin {n}", "NUM-04", BAD),
                      (f"Lasku on väärin: oikea tulo on {fmt(p * 10)}", None, "Laske uudelleen: desimaalipilkun paikka pitää tarkistaa."),
                      ("Tuloa ei voi tarkistaa arvioimalla", None, "Arvion voi tehdä vertaamalla kerrointa lukuun 1.")]
            assert p < n
            steps = [f"{fmt(f)} < 1", f"{fmt(f)} × {n} = {fmt(p)} < {n}"]
            final, params, key, level = f"{fmt(p)}", {"factor": fmt(f), "n": n}, (f, n, "c"), "H"
        else:
            b = rng.choice([4, 6, 10])
            prompt = (f"Mikä on oikea perustelu sille, että 0,25 × {b} on pienempi kuin {b}?")
            q = Decimal("0.25") * b
            correct = (f"0,25 × {b} on neljäsosa luvusta {b}, eli {fmt(q)}", "Oikein: kertominen luvulla 0,25 ottaa neljäsosan.")
            wrongs = [(f"Se ei ole pienempi, koska kertolasku suurentaa aina", "NUM-04", BAD),
                      (f"Se on pienempi, koska 0,25 on pienempi kuin {b}", None,
                       "Perustelu ei riitä: ratkaisevaa on, että kerroin on pienempi kuin 1."),
                      (f"Se on yhtä suuri, koska 0,25 on vain desimaalimerkintä", None,
                       "0,25 on neljäsosa, ei ykkönen.")]
            steps = [f"0,25 = 1/4", f"0,25 × {b} = {fmt(q)} = {b} / 4"]
            final, params, key, level = f"{fmt(q)}", {"b": b, "justify": True}, (b, "d"), "H"
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.03", "S2.06"], ["T11"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: kerroin alle 1 pienentää tuloa.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
