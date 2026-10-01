#!/usr/bin/env python3
"""NUM-03 (whole-number bias in fraction addition), type MC. Options are computed with Fraction from the same numbers."""
import random
from fractions import Fraction
from math import lcm

from gen_common import base_item, cli, mc_options

TEMPLATE = "num03_mc"
TID, CODE = "NUM-03", "MC"
BAD = ("Osoittajat ja nimittäjät eivät lasku erikseen yhteen. Muuta murtoluvut samannimisiksi ja laske vain osoittajat yhteen.")
SAME = "Samannimisten murtolukujen summassa nimittäjä pysyy samana: osat ovat samankokoisia."


def fr(f):
    return f"{f.numerator}/{f.denominator}"


def naive(a, b, c, d):
    return f"{a + c}/{b + d}"


def pick_unlike(rng):
    while True:
        b, d = rng.sample([2, 3, 4, 5, 6, 8], 2)
        if b % d == 0 or d % b == 0:
            continue
        a, c = rng.randint(1, b - 1), rng.randint(1, d - 1)
        s = Fraction(a, b) + Fraction(c, d)
        if s < 1 and Fraction(a + c, b + d) != s:
            return a, b, c, d


def make_items(run, date, count=5, start=1):
    rng = random.Random(501)
    items, seen = [], set()
    for k in range(count):
        if k == 0:  # equal denominators
            d = rng.choice([8, 10, 12])
            a, c = rng.sample(range(1, d // 2), 2)
            s = Fraction(a, d) + Fraction(c, d)
            prompt = f"Laske {a}/{d} + {c}/{d}."
            correct = (f"{fr(s)}" if s.denominator != d else f"{a + c}/{d}", "Oikein: nimittäjä pysyy samana ja osoittajat lasketaan yhteen.")
            ctext = f"{a + c}/{d}"
            correct = (ctext, correct[1])
            wrongs = [(f"{a + c}/{2 * d}", "NUM-03", BAD), (f"{a * c}/{d}", None, SAME),
                      (f"{a + c}/{d * d}", None, SAME)]
            steps = [f"{a}/{d} + {c}/{d} = ({a} + {c})/{d}", f"= {a + c}/{d}"]
            params, key, level = {"a": a, "c": c, "d": d}, (a, d, c, d), "T"
            final = ctext
        elif k in (1, 2):  # unlike denominators, plain and in context
            a, b, c, d = pick_unlike(rng)
            L = lcm(b, d)
            num = a * (L // b) + c * (L // d)
            s = Fraction(num, L)
            ctext = fr(s)
            if k == 1:
                prompt = f"Laske {a}/{b} + {c}/{d}."
            else:
                prompt = (f"Kakkuohjeessa tarvitaan {a}/{b} l maitoa ja {c}/{d} l kermaa. "
                          f"Kuinka monta litraa nestettä tarvitaan yhteensä?")
                ctext += " l"
            wr = naive(a, b, c, d)
            assert Fraction(a + c, b + d) != s
            correct = (ctext, f"Oikein: yhteinen nimittäjä on {L}, ja {a * (L // b)}/{L} + {c * (L // d)}/{L} = {num}/{L}.")
            unit = " l" if k == 2 else ""
            wrongs = [(wr + unit, "NUM-03", BAD), (f"{a * c}/{b * d}" + unit, None,
                      "Murtolukuja ei yhteenlaskussa kerrota keskenään. Muuta ne samannimisiksi."),
                      (f"{num}/{b + d}" + unit, None, "Nimittäjäksi ei kelpaa nimittäjien summa. Käytä yhteistä nimittäjää.")]
            wrongs = [w for w in wrongs if w[0] != ctext]
            steps = [f"{a}/{b} = {a * (L // b)}/{L}, {c}/{d} = {c * (L // d)}/{L}", f"{a * (L // b)}/{L} + {c * (L // d)}/{L} = {num}/{L}"]
            params, key, level = {"a": a, "b": b, "c": c, "d": d, "context": k == 2}, (a, b, c, d), "T"
            final = ctext
            if s.denominator != L:
                final = ctext
                correct = (ctext, correct[1])
        elif k == 3:  # estimate: is the sum over 1?
            while True:
                b, d = rng.sample([3, 4, 5, 6, 8], 2)
                a, c = rng.randint(b // 2 + 1, b - 1), rng.randint(d // 2 + 1, d - 1)
                s = Fraction(a, b) + Fraction(c, d)
                if s > 1 and Fraction(a + c, b + d) < 1 and b % d and d % b:
                    break
            prompt = f"Laske summa {a}/{b} + {c}/{d} arvioiden. Onko summa suurempi vai pienempi kuin 1?"
            correct = ("Suurempi kuin 1, koska kumpikin yhteenlaskettava on yli puoli", "Oikein: molemmat luvut ovat yli 1/2, joten summa on yli 1.")
            wrongs = [(f"Pienempi kuin 1, koska {a}/{b} + {c}/{d} = {a + c}/{b + d}", "NUM-03", BAD),
                      ("Täsmälleen 1", None, "Laske arvio: kumpi luku on suurempi kuin 1/2?"),
                      ("Sitä ei voi arvioida ilman laskemista", None, "Arvion voi tehdä vertaamalla lukuja puoleen.")]
            steps = [f"{a}/{b} > 1/2 ja {c}/{d} > 1/2", "Summa > 1/2 + 1/2 = 1"]
            params, key, level = {"a": a, "b": b, "c": c, "d": d, "estimate": True}, (a, b, c, d, "e"), "H"
            final = "Suurempi kuin 1"
        else:  # justify why a/b + c/d != (a+c)/(b+d)
            a, b, c, d = 1, 2, 1, 3
            while (a, b, c, d) in seen:
                a, b, c, d = rng.choice([(1, 2, 1, 4), (1, 3, 1, 4), (1, 2, 1, 5), (2, 3, 1, 4)])
            s = Fraction(a, b) + Fraction(c, d)
            prompt = (f"Oppilas laskee {a}/{b} + {c}/{d} = {a + c}/{b + d}. Miksi vastaus ei voi olla oikein? Valitse paras perustelu.")
            correct = (f"Yhteenlaskettavat ovat yhdessä {fr(s)}, mikä on eri kuin {a + c}/{b + d}; "
                       f"yhteenlaskettavat on ensin muutettava samannimisiksi",
                       "Oikein: summa on laskettava yhteisellä nimittäjällä.")
            assert s != Fraction(a + c, b + d)
            wrongs = [(f"{a + c}/{b + d} on oikea vastaus, koska osoittajat ja nimittäjät lasketaan yhteen", "NUM-03", BAD),
                      (f"Vastaus on oikein, koska {a} + {c} = {a + c} ja {b} + {d} = {b + d}", "NUM-03", BAD),
                      ("Murtolukuja ei voi laskea yhteen, jos nimittäjät ovat erilaiset", None,
                       "Erinimiset murtoluvut voi laskea yhteen, kun ne muutetaan samannimisiksi.")]
            steps = [f"Yhteinen nimittäjä {lcm(b, d)}: {a * (lcm(b, d) // b)}/{lcm(b, d)} + {c * (lcm(b, d) // d)}/{lcm(b, d)} = {fr(s)}",
                     f"{fr(s)} ≠ {a + c}/{b + d}"]
            params, key, level = {"a": a, "b": b, "c": c, "d": d, "justify": True}, (a, b, c, d, "j"), "H"
            final = "Summa on laskettava samannimisillä murtoluvuilla"
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.02"], ["T11"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: murtolukujen yhteenlaskussa osoittajat lasketaan yhteen samannimisinä.",
                               TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
