#!/usr/bin/env python3
"""ALG-04 (conjoining terms), type MC. Fixed seed, options computed from the numbers."""
import random

from gen_common import MINUS, base_item, cli, mc_options

TEMPLATE = "alg04_mc"
TID, CODE = "ALG-04", "MC"
OP = "Plusmerkki ei pyydä yhdistämään kaikkea yhdeksi termiksi. Eri muotoisia termejä (luku ja x-termi) ei voi laskea yhteen."


def make_items(run, date, count=5, start=1):
    rng = random.Random(311)
    items = []
    for k in range(count):
        a, b, c = rng.randint(2, 7), rng.randint(3, 9), rng.randint(2, 6)
        while c == a:
            c = rng.randint(2, 6)
        if k == 0:
            level = "T"
            prompt = f"Sievennä lauseke {a}x + {b}."
            options, cid = mc_options(rng, (f"{a}x + {b}", f"Oikein: {a}x ja {b} ovat eri muotoisia termejä, joten lauseke on jo sievin."), [
                (f"{a + b}x", TID, OP),
                (f"{a * b}x", TID, OP),
                (f"{a + b}", None, f"Kirjain ei katoa: {a}x ei ole sama kuin {a}."),
            ])
            steps = [f"{a}x on x-termi, {b} on vakiotermi", "Eri muotoisia termejä ei voi yhdistää", f"{a}x + {b}"]
            final = f"{a}x + {b}"
        elif k == 1:
            level = "T"
            prompt = f"Sievennä lauseke {a}x + {b} + {c}x."
            options, cid = mc_options(rng, (f"{a + c}x + {b}", "Oikein: vain x-termit voi laskea yhteen."), [
                (f"{a + b + c}x", TID, OP),
                (f"{a + c + b}", None, "Kirjain x ei saa kadota: x-termit pysyvät x-termeinä."),
                (f"{a * c}x + {b}", None, f"Samanlaiset termit lasketaan yhteen, ei kerrota: {a}x + {c}x."),
            ])
            steps = [f"x-termit: {a}x + {c}x = {a + c}x", f"Vakiotermi: {b}", f"{a + c}x + {b}"]
            final = f"{a + c}x + {b}"
        elif k == 2:
            level = "T"
            d = rng.randint(2, 5)
            prompt = f"Mikä lauseke on sama kuin {b} + {a}y {MINUS} {d}?"
            rest = f"+ {b - d}" if b >= d else f"{MINUS} {d - b}"
            options, cid = mc_options(rng, (f"{a}y {rest}", "Oikein: luvut yhdistetään keskenään, y-termi pysyy omana termin."), [
                (f"{a + b - d}y", TID, OP),
                (f"{a}y {MINUS} {b + d}", None, "Tarkista vakiotermien merkit: +" + str(b) + f" ja {MINUS}{d}."),
                (f"{a * b - d}y", TID, OP),
            ])
            steps = [f"Luvut: {b} {MINUS} {d} = {str(b - d).replace(chr(45), MINUS)}", f"y-termi: {a}y", f"{a}y {rest}"]
            final = f"{a}y {rest}"
        elif k == 3:
            level = "H"
            x = 2
            prompt = (f"Oppilas sieventää lausekkeen {a}x + {b} muotoon {a + b}x. Mikä perustelu osoittaa, että sieventäminen on väärin?")
            options, cid = mc_options(rng, (f"Kun x = {x}, {a}x + {b} = {a * x + b}, mutta {a + b}x = {(a + b) * x}", "Oikein: lausekkeiden arvot eroavat, joten ne eivät ole sama lauseke."), [
                (f"Sieventäminen on oikein, koska plusmerkki pyytää laskemaan kaiken yhteen", TID, OP),
                (f"Väärin, koska vastauksessa ei saa olla kirjainta", None, "Kirjain saa olla vastauksessa, kun alkuperäisessäkin on kirjain."),
                (f"Väärin, koska luvut pitäisi kertoa keskenään", None, "Kertominen ei kuulu tehtävään."),
            ])
            steps = [f"x = {x}: {a}x + {b} = {a * x + b}", f"x = {x}: {a + b}x = {(a + b) * x}", "Arvot eroavat, joten lausekkeet eivät ole samat"]
            final = "Sijoituksella nähdään, että lausekkeet eroavat"
        else:
            level = "H"
            price = rng.randint(6, 12)
            base = 2 * price + c
            wrong_val = (2 + c) * price
            prompt = (f"Pizza maksaa x euroa ja juoma {c} euroa. Kaksi pizzaa ja yksi juoma maksaa 2x + {c} euroa. "
                      f"Matti sanoo hinnan olevan {2 + c}x euroa. Mikä on oikea hinta euroina, kun x = {price}?")
            options, cid = mc_options(rng, (str(base), "Oikein: 2x + " + str(c) + " ei ole sama kuin " + str(2 + c) + "x."), [
                (str(wrong_val), TID, OP),
                (str(2 * (price + c)), None, "Juoma ostetaan vain kerran, ei kahta."),
                (str(price + c), None, "Pizzoja on kaksi."),
            ])
            steps = [f"2x + {c} = 2 · {price} + {c}", f"= {2 * price} + {c}", f"= {base}"]
            final = str(base)
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, final,
                               "Oikein: eri muotoisia termejä ei voi yhdistää yhdeksi termiksi.", TEMPLATE,
                               {"a": a, "b": b, "c": c}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
