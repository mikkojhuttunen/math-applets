#!/usr/bin/env python3
"""PRO-03 (same perimeter means same area), type RP. The wanted side x is found from equal perimeters; the invalid
equations equate the areas instead (the misconception) or reuse a side. verify.py checks their solution sets."""
import random

from gen_common import base_item, cli

TEMPLATE = "pro03_rp"
TID, CODE = "PRO-03", "RP"
GENERIC = "Sama piiri ei tarkoita samaa alaa. Piiri on sivujen summa 2 · (pituus + leveys); sijoita x ja tarkista."
GOOD = "Oikein: samat piirit antavat yhtälön sivujen summalle, ei alan yhtäsuuruudelle."


def make_items(run, date, count=5, start=1):
    rng = random.Random(8330)
    items, seen = [], set()
    for k in range(count):
        while True:
            s = rng.randint(4, 9)
            a = rng.randint(1, s - 1)
            if (s, a) not in seen:
                break
        seen.add((s, a))
        b = 2 * s - a
        level = "T"
        if k == 0:
            prompt = (f"Neliön sivu on {s} cm. Suorakulmion yksi sivu on {a} cm, ja sen piiri on yhtä suuri kuin neliön piiri. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {b} on suorakulmion toinen sivu (cm).")
            valid = [f"2 * ({a} + x) = {4 * s}", f"{a} + x = {2 * s}"]
            invalid = [f"{a} * x = {s * s}", f"x = {s}", f"{a} + x = {4 * s}"]
            steps = [f"Neliön piiri 4 · {s} = {4 * s} cm", f"Suorakulmion piiri 2 · ({a} + x) = {4 * s}", f"x = {2 * s} {chr(8722)} {a} = {b}"]
        elif k == 1:
            c, d = a, 2 * s - a
            e = rng.randint(1, s - 1)
            while e == a:
                e = rng.randint(1, s - 1)
            f = 2 * s - e
            prompt = (f"Suorakulmion A sivut ovat {c} cm ja {d} cm. Suorakulmion B piiri on sama kuin A:n, ja sen yksi sivu on {e} cm. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {f} on B:n toinen sivu (cm).")
            valid = [f"2 * ({e} + x) = 2 * ({c} + {d})", f"{e} + x = {c + d}"]
            invalid = [f"{e} * x = {c * d}", f"x = {d}", f"{e} + x = {2 * (c + d)}"]
            steps = [f"A:n piiri 2 · ({c} + {d}) = {2 * (c + d)} cm", f"B:n piiri 2 · ({e} + x) = {2 * (c + d)}", f"x = {c + d} {chr(8722)} {e} = {f}"]
            a, b = e, f
        elif k == 2:
            prompt = (f"Neliön muotoisen laidunkarsinan aita on {4 * s} m pitkä. Sama aita riittää suorakulmion muotoiseen karsinaan, jonka leveys on {a} m. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {b} on karsinan pituus (m).")
            valid = [f"2 * ({a} + x) = {4 * s}", f"2 * {a} + 2 * x = {4 * s}"]
            invalid = [f"{a} * x = {s * s}", f"x = {s}", f"2 * {a} + x = {4 * s}"]
            steps = [f"Aidan pituus on karsinan piiri: 2 · ({a} + x) = {4 * s}", f"{a} + x = {2 * s}", f"x = {b}"]
        elif k == 3:
            level = "H"
            a = rng.choice([x for x in range(2, 9) if x != s and (x + 2 * s) % 2 == 0])
            b = 2 * s - a
            prompt = (f"Nauha on kierretty suorakulmion ympäri, jonka sivut ovat {a} cm ja {b} cm. Nauha avataan ja siitä muotoillaan neliö. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {s} on neliön sivu (cm).")
            valid = [f"4 * x = 2 * ({a} + {b})", f"x = ({a} + {b}) / 2"]
            invalid = [f"x * x = {a * b}", f"x = {a * b}", f"4 * x = {a * b}"]
            steps = [f"Nauhan pituus on suorakulmion piiri 2 · ({a} + {b}) = {2 * (a + b)} cm", f"4x = {2 * (a + b)}", f"x = {s}"]
            assert a != b
        else:
            level = "H"
            prompt = (f"Kaksi lasten leikkialuetta on rajattu yhtä pitkällä köydellä. Neliön muotoisen alueen sivu on {s} m, "
                      f"ja suorakulmion muotoisen alueen lyhyempi sivu on {a} m. Pidempi sivu on x m. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {b} kertoo pidemmän sivun.")
            valid = [f"2 * ({a} + x) = 4 * {s}", f"2 * x = 4 * {s} {chr(8722)} 2 * {a}"]
            invalid = [f"{a} * x = {s} * {s}", f"x = {s} + {a}", f"x + {a} = 4 * {s}"]
            steps = [f"Köyden pituus 4 · {s} = {4 * s} m", f"2 · ({a} + x) = {4 * s}", f"x = {b}"]
        value = b if k != 3 else s
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": value},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S5.07"], ["T18"], 7, level, prompt, payload, steps, f"x = {value}",
                               GOOD, TEMPLATE, {"s": s, "a": a, "b": b, "form": k}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
