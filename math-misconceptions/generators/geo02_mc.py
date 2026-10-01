#!/usr/bin/env python3
"""GEO-02 (a square is not a rectangle), type MC. Rectangle = four right angles (opposite sides then equal);
whether a given figure satisfies this is decided by code from its sides and angles."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "geo02_mc"
TID, CODE = "GEO-02", "MC"
BAD = ("Neliö on suorakulmion erikoistapaus: sillä on kaikki suorakulmion ominaisuudet (neljä suoraa kulmaa) "
       "ja lisäksi sivut ovat yhtä pitkät.")
GOOD = "Oikein: jokainen neliö on myös suorakulmio, koska siinä on neljä suoraa kulmaa."


def is_rectangle(sides, angles):
    return all(x == 90 for x in angles) and sides[0] == sides[2] and sides[1] == sides[3]


def make_items(run, date, count=5, start=1):
    rng = random.Random(2113)
    items = []
    for k in range(count):
        s = rng.randint(3, 12)
        sq = ([s] * 4, [90] * 4)
        assert is_rectangle(*sq)
        if k == 0:
            prompt = f"Neliön sivu on {s} cm ja sen kaikki kulmat ovat 90°. Onko tämä neliö myös suorakulmio?"
            ok = (f"Kyllä: kulmat ovat 90° ja vastakkaiset sivut ovat yhtä pitkät ({s} cm ja {s} cm)",
                  GOOD)
            wrongs = [("Ei, koska suorakulmion sivujen pitää olla eri pituisia", TID, BAD),
                      ("Ei, koska neliö ja suorakulmio ovat eri kuviot", TID, BAD),
                      ("Kyllä, mutta vain jos sivu on yli 10 cm", None, "Sivun pituus ei vaikuta luokitteluun.")]
            level, steps = "T", [f"Kulmat 90°, sivut {s}, {s}, {s}, {s}", "Suorakulmion ehdot täyttyvät"]
            params = {"s": s}
        elif k == 1:
            prompt = (f"Neliönmuotoisen ikkunan sivu on {s} dm. Lasimestari valmistaa suorakulmion muotoisia laseja. "
                      "Voiko ikkunaan käyttää suorakulmion muotoista lasia?")
            ok = (f"Kyllä: neliö on suorakulmio, jonka molemmat sivut ovat {s} dm",
                  GOOD)
            wrongs = [("Ei, koska neliö ei ole suorakulmio", TID, BAD),
                      ("Ei, koska suorakulmiossa leveys ja korkeus ovat aina eri suuret", TID, BAD),
                      ("Kyllä, mutta lasin ala on silloin eri kuin neliön ala", None, f"Ala on sama, {s} · {s} = {s * s} dm².")]
            level, steps = "T", [f"{s} dm × {s} dm", "Leveys ja korkeus saavat olla yhtä suuret"]
            params = {"s": s}
        elif k == 2:
            prompt = (f"Suorakulmion ala on leveys · korkeus. Neliön sivu on {s} cm. Mikä on neliön ala, "
                      "kun käytät suorakulmion pinta-alan kaavaa?")
            ok = (f"{s} · {s} = {s * s} cm²", GOOD)
            wrongs = [("Kaava ei päde neliöön, koska neliö ei ole suorakulmio", TID, BAD),
                      (f"4 · {s} = {4 * s} cm²", None, f"Tämä on neliön piiri, ei ala.")]
            wrongs.append((f"{s} + {s} = {2 * s} cm²", None, "Ala saadaan kertomalla, ei laskemalla yhteen."))
            level, steps = "T", [f"Leveys {s} cm, korkeus {s} cm", f"{s} · {s} = {s * s}"]
            params = {"s": s}
        elif k == 3:
            prompt = (f"Kuvion kaikki sivut ovat {s} cm ja kaikki kulmat ovat 90°. Mitkä nimet sopivat kuviolle?")
            ok = ("Sekä neliö että suorakulmio", GOOD)
            wrongs = [("Vain neliö, koska neliö ei ole suorakulmio", TID, BAD),
                      ("Vain suorakulmio, koska sivut eivät ole eri pituisia", TID, BAD),
                      ("Ei kumpikaan", None, "Kulmat ovat 90° ja sivut yhtä pitkät, joten molemmat sopivat.")]
            level, steps = "H", ["Neljä suoraa kulmaa: suorakulmio", "Neljä yhtä pitkää sivua: neliö"]
            params = {"s": s}
        else:
            w = s + rng.randint(2, 5)
            assert not is_rectangle([w, s, w, s], [90] * 4) is False
            prompt = (f"Mikä väite on oikein? Verrataan neliötä (sivu {s} cm) ja suorakulmiota, jonka sivut ovat {w} cm ja {s} cm.")
            ok = ("Jokainen neliö on suorakulmio, mutta kaikki suorakulmiot eivät ole neliöitä", GOOD)
            wrongs = [("Neliö ei ole suorakulmio, koska sen sivut ovat yhtä pitkät", TID, BAD),
                      ("Jokainen suorakulmio on neliö, koska molemmissa on neljä suoraa kulmaa", None,
                       f"Suorakulmion {w} cm × {s} cm sivut eivät ole yhtä pitkät."),
                      ("Neliö ja suorakulmio ovat täysin erilaisia kuvioita, joilla ei ole yhteisiä ominaisuuksia", TID, BAD)]
            level, steps = "H", [f"{s} × {s} täyttää suorakulmion ehdot", f"{w} × {s} ei täytä neliön ehtoa"]
            params = {"s": s, "w": w}
        final = ok[0]
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S5.03"], ["T16"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
