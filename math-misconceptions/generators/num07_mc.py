#!/usr/bin/env python3
"""NUM-07 (wrong base in reverse percentage), type MC. All values are computed with Decimal arithmetic from the
original amount; the typical wrong answer takes the percentage of the new (given) amount."""
import random
from decimal import Decimal

from gen_common import base_item, cli, mc_options
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)


TEMPLATE = "num07_mc"
TID, CODE = "NUM-07", "MC"
BAD = ("Prosentti on laskettu uudesta määrästä, mutta muutos tapahtui alkuperäisestä määrästä. "
       "Alkuperäinen määrä on se 100 %, josta muutos lasketaan.")
GOOD = "Oikein: muutosprosentti lasketaan alkuperäisestä määrästä, joten uusi määrä on 100 % ± muutos."


def make_items(run, date, count=5, start=1):
    rng = random.Random(807)
    items, seen = [], set()
    for k in range(count):
        while True:
            orig = Decimal(rng.choice([40, 60, 80, 120, 160, 200, 240]))
            p = Decimal(rng.choice([10, 20, 25, 50])) if k != 1 else Decimal(rng.choice([10, 20, 25]))
            if (orig, p) not in seen:
                break
        seen.add((orig, p))
        up, down = orig * (1 + p / 100), orig * (1 - p / 100)
        if k == 0:
            new = up
            prompt = (f"Pelin hinta nousi {fmt(p)} % ja on nyt {fmt(new)} €. Mikä hinta oli ennen korotusta?")
            correct = (f"{fmt(orig)} €", f"Oikein: {fmt(orig)} · {fmt(1 + p / 100)} = {fmt(new)}.")
            wrongs = [(f"{fmt(new * (1 - p / 100))} €", "NUM-07", BAD),
                      (f"{fmt(new * (1 + p / 100))} €", None, "Tämä olisi hinta, jos nykyinen hinta nousisi vielä kerran."),
                      (f"{fmt(new - p)} €", None, f"{fmt(p)} % ei tarkoita {fmt(p)} euroa.")]
            steps = [f"Vanha hinta on 100 %, uusi {fmt(100 + p)} %", f"{fmt(new)} ÷ {fmt(1 + p / 100)} = {fmt(orig)}"]
            final, level = f"{fmt(orig)} €", "T"
        elif k == 1:
            new = down
            prompt = f"Takin hinta aleni {fmt(p)} % ja se maksaa nyt {fmt(new)} €. Mikä oli takin hinta ennen alennusta?"
            correct = (f"{fmt(orig)} €", f"Oikein: {fmt(orig)} · {fmt(1 - p / 100)} = {fmt(new)}.")
            wrongs = [(f"{fmt(new * (1 + p / 100))} €", "NUM-07", BAD),
                      (f"{fmt(new * (1 - p / 100))} €", None, "Tämä olisi hinta, jos nykyinen hinta alenisi vielä kerran."),
                      (f"{fmt(new + p)} €", None, f"{fmt(p)} % ei tarkoita {fmt(p)} euroa.")]
            steps = [f"Vanha hinta on 100 %, uusi {fmt(100 - p)} %", f"{fmt(new)} ÷ {fmt(1 - p / 100)} = {fmt(orig)}"]
            final, level = f"{fmt(orig)} €", "T"
        elif k == 2:
            new = up
            prompt = (f"Luokan oppilasmäärä kasvoi {fmt(p)} % ja on nyt {fmt(new)}. "
                      f"Kuinka monta oppilasta lisää luokkaan tuli?")
            gain = new - orig
            correct = (f"{fmt(gain)}", f"Oikein: alkuperäinen määrä oli {fmt(orig)}, ja kasvu on {fmt(new)} {chr(8722)} {fmt(orig)} = {fmt(gain)}.")
            wrongs = [(f"{fmt(new * p / 100)}", "NUM-07", BAD),
                      (f"{fmt(orig)}", None, "Tämä on alkuperäinen määrä, ei lisäys."),
                      (f"{fmt(p)}", None, f"{fmt(p)} on prosenttiluku, ei oppilaiden määrä.")]
            steps = [f"{fmt(new)} ÷ {fmt(1 + p / 100)} = {fmt(orig)}", f"{fmt(new)} {chr(8722)} {fmt(orig)} = {fmt(gain)}"]
            final, level = fmt(gain), "T"
        elif k == 3:
            new = up
            wrong_old = new - new * p / 100
            prompt = (f"Palkka nousi {fmt(p)} % ja on nyt {fmt(new)} €/kk. Oppilas laskee vanhaksi palkaksi "
                      f"{fmt(new)} {chr(8722)} {fmt(p)} % · {fmt(new)} = {fmt(wrong_old)} €. Mikä väite on oikein?")
            correct = (f"Lasku on väärin: vanha palkka on {fmt(orig)} €, koska {fmt(orig)} · {fmt(1 + p / 100)} = {fmt(new)}", GOOD)
            wrongs = [(f"Lasku on oikein: {fmt(wrong_old)} € on vanha palkka", "NUM-07", BAD),
                      (f"Lasku on väärin: vanha palkka on {fmt(new * (1 + p / 100))} €", None, "Tämä olisi palkka, jos nykyinen palkka nousisi vielä kerran."),
                      ("Vanhaa palkkaa ei voi laskea, jos ei tiedä korotuksen euromäärää", None, "Prosentin ja uuden määrän avulla alkuperäisen voi laskea.")]
            steps = [f"{fmt(wrong_old)} · {fmt(1 + p / 100)} = {fmt(wrong_old * (1 + p / 100))} ≠ {fmt(new)}",
                     f"{fmt(new)} ÷ {fmt(1 + p / 100)} = {fmt(orig)}"]
            final, level = f"{fmt(orig)} €", "H"
        else:
            prompt = (f"Hinta nousi {fmt(p)} %. Miksi vanhaa hintaa ei saa laskemalla uudesta hinnasta {fmt(p)} % pois?")
            correct = (f"Koska {fmt(p)} % on laskettu vanhasta hinnasta, ja uusi hinta on suurempi, joten {fmt(p)} % uudesta hinnasta on liian suuri",
                       GOOD)
            wrongs = [(f"Se on aina oikein, koska nousu ja lasku {fmt(p)} % kumoavat toisensa", "NUM-07", BAD),
                      ("Siksi, että prosentteja ei saa vähentää hinnasta lainkaan", None, "Prosentteja voi käyttää, kunhan perusarvo on oikea."),
                      (f"Siksi, että vanha hinta on aina {fmt(p)} euroa pienempi", None, f"{fmt(p)} % ei tarkoita {fmt(p)} euroa.")]
            steps = [f"Uusi hinta = {fmt(1 + p / 100)} · vanha hinta", f"Vanha hinta = uusi hinta ÷ {fmt(1 + p / 100)}"]
            final, level = "Perusarvo on vanha hinta, ei uusi", "H"
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE,
                               {"orig": fmt(orig), "percent": fmt(p), "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
