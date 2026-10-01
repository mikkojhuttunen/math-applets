#!/usr/bin/env python3
"""PRO-03 (same perimeter means same area), type MC. Options are computed from the side lengths of rectangles with
equal perimeter."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "pro03_mc"
TID, CODE = "PRO-03", "MC"
BAD = ("Piiri kertoo vain reunan pituuden. Pinta-ala riippuu siitä, miten pituus jakautuu sivuille: "
       "samalla piirillä ala voi olla eri suuri.")
GOOD = "Oikein: sama piiri ei takaa samaa alaa, vaan ala lasketaan sivujen tulona."


def pair(rng, half, lo=1):
    a = rng.randint(lo, half // 2 - 1)
    return a, half - a


def make_items(run, date, count=5, start=1):
    rng = random.Random(831)
    items = []
    for k in range(count):
        if k == 0:
            level = "T"
            while True:
                a, b = rng.randint(2, 9), rng.randint(2, 12)
                if a != b and (a + b) % 2 == 0:
                    break
            s = (a + b) // 2
            prompt = f"Suorakulmion sivut ovat {a} cm ja {b} cm. Neliön piiri on yhtä suuri kuin suorakulmion piiri. Mitä voit sanoa pinta-aloista?"
            ok = (f"Neliön ala on {s * s} cm² ja suorakulmion {a * b} cm², joten alat eivät ole samat",
                  f"Oikein: neliön sivu on {2 * (a + b)} / 4 = {s} cm, ja ala {s}² = {s * s} cm².")
            wrongs = [("Alat ovat samat, koska piirit ovat samat", TID, BAD),
                      (f"Suorakulmion ala on suurempi, koska sen sivut ovat {a} cm ja {b} cm", None, f"Neliön ala on {s * s} cm², suurempi kuin {a * b} cm²."),
                      ("Pinta-aloja ei voi verrata, koska kuviot ovat eri muotoisia", None, "Pinta-alat voi aina laskea ja verrata.")]
            steps = [f"Piiri 2 · ({a} + {b}) = {2 * (a + b)} cm", f"Neliön sivu {s} cm, ala {s * s} cm²", f"Suorakulmion ala {a} · {b} = {a * b} cm²"]
            final, params = ok[0], {"a": a, "b": b}
        elif k == 1:
            level = "T"
            half = rng.choice([10, 12, 14, 16, 18])
            a, b = pair(rng, half, 2)
            s = half // 2
            prompt = (f"Kaksi aitausta tehdään {2 * half} metrin pituisesta aidasta: toinen on suorakulmio {a} m × {b} m ja toinen neliö. "
                      "Kumpaan mahtuu enemmän ruohoa?")
            ok = (f"Neliöön: sen ala on {s * s} m² ja suorakulmion {a * b} m²", f"Oikein: {s} · {s} = {s * s} m² on enemmän kuin {a} · {b} = {a * b} m².")
            wrongs = [("Molempiin yhtä paljon, koska aita on yhtä pitkä", TID, BAD),
                      (f"Suorakulmioon, koska sen pidempi sivu on {b} m", None, "Pidempi sivu ei yksin ratkaise alaa."),
                      ("Sitä ei voi tietää ilman piirrosta", None, "Alat saadaan laskemalla sivujen tulot.")]
            steps = [f"Neliön sivu {2 * half} / 4 = {s} m", f"Neliön ala {s * s} m², suorakulmion ala {a * b} m²"]
            final, params = ok[0], {"perimeter": 2 * half, "a": a, "b": b}
        elif k == 2:
            level = "T"
            half = rng.choice([12, 14, 16, 18])
            a, b = pair(rng, half, 1)
            c, d = pair(rng, half, a + 1)
            prompt = (f"Oppilas väittää: \"Suorakulmioiden piirit ovat molemmat {2 * half} cm, joten niiden alat ovat samat.\" "
                      f"Suorakulmioiden sivut ovat {a} cm × {b} cm ja {c} cm × {d} cm. Mikä väite on oikein?")
            ok = (f"Väite on väärä: alat ovat {a * b} cm² ja {c * d} cm²", f"Oikein: {a} · {b} = {a * b} ja {c} · {d} = {c * d}.")
            wrongs = [("Väite on oikea, koska piirit ovat samat", TID, BAD),
                      ("Väite on oikea, jos kuviot ovat suorakulmioita", TID, BAD),
                      ("Väite on väärä, koska piirit eivät ole samat", None, f"Molempien piiri on 2 · {half} = {2 * half} cm.")]
            steps = [f"Piirit: 2 · ({a} + {b}) = {2 * half} ja 2 · ({c} + {d}) = {2 * half}", f"Alat {a * b} cm² ja {c * d} cm²"]
            final, params = ok[0], {"a": a, "b": b, "c": c, "d": d}
        elif k == 3:
            level = "H"
            half = rng.choice([12, 16, 20])
            s = half // 2
            d1, d2 = rng.sample(range(1, s), 2)
            prompt = f"Pellon ympärille on käytettävissä {2 * half} m aitaa. Minkä mittaisen suorakulmion muotoisen pellon ala on suurin?"
            ok = (f"{s} m × {s} m", f"Oikein: ala {s * s} m² on suurempi kuin muiden vaihtoehtojen alat.")
            wrongs = [(f"{s - d1} m × {s + d1} m", None, f"Ala {(s - d1) * (s + d1)} m² on pienempi kuin {s * s} m²."),
                      (f"{s - d2} m × {s + d2} m", None, f"Ala {(s - d2) * (s + d2)} m² on pienempi kuin {s * s} m²."),
                      ("Kaikkien alat ovat yhtä suuret, koska aita on yhtä pitkä", TID, BAD)]
            steps = [f"Sivujen summa on {half} m", f"{s} · {s} = {s * s}, {s - d1} · {s + d1} = {(s - d1) * (s + d1)}, {s - d2} · {s + d2} = {(s - d2) * (s + d2)}"]
            final, params = ok[0], {"perimeter": 2 * half, "d1": d1, "d2": d2}
        else:
            level = "H"
            half = rng.choice([10, 12, 14])
            a, b = pair(rng, half, 1)
            s = half // 2
            prompt = "Miksi kahdella kuviolla voi olla sama piiri mutta eri pinta-ala?"
            ok = (f"Piiri kertoo vain reunan pituuden, ala riippuu sivujen suhteesta: esimerkiksi {a} × {b} ja {s} × {s} ovat samaa piiriä mutta alat ovat {a * b} ja {s * s}",
                  GOOD)
            wrongs = [("Se ei ole mahdollista, koska sama piiri tarkoittaa samaa alaa", TID, BAD),
                      ("Se on mahdollista vain, jos toinen kuvio on ympyrä", None, "Eri alat voivat olla jo suorakulmioilla."),
                      ("Se on mahdollista vain, jos piiri on pariton luku", None, "Piirin parillisuus ei vaikuta asiaan.")]
            steps = [f"Piiri {2 * half}: {a} × {b} antaa alan {a * b}", f"Neliö {s} × {s} antaa alan {s * s}"]
            final, params = ok[0], {"a": a, "b": b}
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S5.07"], ["T18"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
