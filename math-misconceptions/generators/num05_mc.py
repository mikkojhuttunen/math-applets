#!/usr/bin/env python3
"""NUM-05 (division always makes smaller), type MC. Quotients are computed with Decimal arithmetic."""
import random
from decimal import Decimal

from gen_common import base_item, cli, mc_options
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)


TEMPLATE = "num05_mc"
TID, CODE = "NUM-05", "MC"
BAD = ("Jakolasku ei aina pienennä. Kun jakaja on pienempi kuin 1, osamäärä on suurempi kuin jaettava "
       "(esimerkiksi 8 ÷ 0,5 = 16, koska luvussa 8 on 16 puolikasta).")


def make_items(run, date, count=5, start=1):
    rng = random.Random(701)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n, f = rng.choice([8, 12, 20, 15]), Decimal(rng.choice(["0.5", "0.25", "0.4", "0.2"]))
            q = n / f
            assert q > n
            prompt = f"Onko osamäärä {n} ÷ {fmt(f)} suurempi vai pienempi kuin {n}?"
            correct = (f"Suurempi kuin {n}", f"Oikein: {n} ÷ {fmt(f)} = {fmt(q)}, ja {fmt(q)} > {n}.")
            wrongs = [(f"Pienempi kuin {n}", "NUM-05", BAD), (f"Yhtä suuri kuin {n}", None, f"Jakaja {fmt(f)} ei ole 1, joten osamäärä ei ole {n}."),
                      ("Sitä ei voi tietää laskematta", None, "Jakaja on pienempi kuin 1, joten osamäärän suunnan voi päätellä.")]
            steps = [f"{fmt(f)} < 1", f"{n} ÷ {fmt(f)} = {fmt(q)} > {n}"]
            final, params, key, level = f"Suurempi kuin {n}", {"divisor": fmt(f), "n": n}, (n, f, "a"), "T"
        elif k == 1:
            n, f = rng.choice([3, 4, 6]), Decimal(rng.choice(["0.5", "0.25", "0.2"]))
            q = n / f
            prompt = (f"Nauhaa on {n} metriä. Siitä leikataan {fmt(f)} metrin pituisia pätkiä. "
                      f"Montako pätkää nauhasta saadaan verrattuna lukuun {n}?")
            correct = (f"{fmt(q)} pätkää, eli enemmän kuin {n}", f"Oikein: {n} ÷ {fmt(f)} = {fmt(q)}.")
            wrongs = [(f"Alle {n} pätkää, koska jakaminen pienentää luvun", "NUM-05", BAD),
                      (f"Tasan {n} pätkää", None, f"Pätkä on lyhyempi kuin 1 metri, joten pätkiä tulee enemmän kuin {n}."),
                      (f"{fmt(n * f)} pätkää", None, "Tämä on kertolasku. Pätkien määrä saadaan jakamalla pituus pätkän pituudella.")]
            steps = [f"{n} ÷ {fmt(f)} = {fmt(q)}", f"{fmt(q)} > {n}"]
            final, params, key, level = f"{fmt(q)} pätkää", {"n": n, "piece": fmt(f)}, (n, f, "b"), "T"
        elif k == 2:
            n = rng.choice([20, 30, 40])
            small = Decimal(rng.choice(["0.4", "0.5", "0.8"]))
            bigs = rng.sample([2, 4, 5], 3)
            prompt = f"Mikä seuraavista osamääristä on suurempi kuin {n}?"
            assert n / small > n and all(Decimal(n) / b < n for b in bigs)
            correct = (f"{n} ÷ {fmt(small)}", f"Oikein: {n} ÷ {fmt(small)} = {fmt(n / small)} > {n}.")
            wrongs = [(f"{n} ÷ {b}", None, f"Jakaja {b} > 1, joten osamäärä {fmt(Decimal(n) / b)} on pienempi kuin {n}.") for b in bigs[:2]]
            wrongs.append((f"Mikään osamäärä ei ole suurempi kuin {n}, koska jakolasku pienentää", "NUM-05", BAD))
            steps = [f"{fmt(small)} < 1, joten {n} ÷ {fmt(small)} > {n}"]
            final, params, key, level = f"{n} ÷ {fmt(small)}", {"n": n, "small": fmt(small), "bigs": bigs[:2]}, (n, small, "c"), "T"
        elif k == 3:
            n, f = rng.choice([6, 9, 12]), Decimal(rng.choice(["0.3", "0.6", "0.4"]))
            q = n / f
            assert q > n
            prompt = (f"Oppilas laskee {n} ÷ {fmt(f)} = {fmt(q)} ja sanoo: \"Jakolasku pienentää, joten tuloksen piti olla alle {n}. "
                      f"Laskin väärin.\" Mikä väite on oikein?")
            correct = (f"Lasku on oikein: jakaja {fmt(f)} on pienempi kuin 1, joten osamäärä {fmt(q)} on suurempi kuin {n}",
                       "Oikein: osamäärä on suurempi kuin jaettava, kun jakaja on alle 1.")
            wrongs = [(f"Lasku on väärin: osamäärän pitää olla pienempi kuin {n}", "NUM-05", BAD),
                      (f"Lasku on väärin: oikea osamäärä on {fmt(n * f)}", None, "Tämä on tulo. Tarkista, mitä lasketaan: jaetaanko vai kerrotaanko?"),
                      ("Osamäärää ei voi tarkistaa arvioimalla", None, "Arvion voi tehdä vertaamalla jakajaa lukuun 1.")]
            steps = [f"{fmt(f)} < 1", f"{n} ÷ {fmt(f)} = {fmt(q)} > {n}"]
            final, params, key, level = fmt(q), {"n": n, "divisor": fmt(f)}, (n, f, "d"), "H"
        else:
            n = rng.choice([3, 6, 9])
            q = Decimal(n) / Decimal("0.25")
            prompt = f"Mikä on oikea perustelu sille, että {n} ÷ 0,25 on suurempi kuin {n}?"
            correct = (f"Luvussa {n} on {fmt(q)} neljännestä, joten {n} ÷ 0,25 = {fmt(q)}", "Oikein: jakaminen luvulla 0,25 kysyy, montako neljännestä mahtuu lukuun.")
            wrongs = [(f"Se ei ole suurempi, koska jakolasku pienentää aina", "NUM-05", BAD),
                      (f"Se on suurempi, koska 0,25 on pienempi kuin {n}", None, "Perustelu ei riitä: ratkaisevaa on, että jakaja on pienempi kuin 1."),
                      (f"Se on yhtä suuri, koska 0,25 on vain desimaalimerkintä", None, "0,25 on neljäsosa, ei ykkönen.")]
            steps = ["0,25 = 1/4", f"{n} ÷ 0,25 = {n} · 4 = {fmt(q)}"]
            final, params, key, level = fmt(q), {"n": n, "justify": True}, (n, "e"), "H"
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.03", "S2.06"], ["T11"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: jakaja alle 1 suurentaa osamäärää.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
