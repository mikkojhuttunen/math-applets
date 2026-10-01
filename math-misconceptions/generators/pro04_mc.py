#!/usr/bin/env python3
"""PRO-04 (larger perimeter means larger area), type MC. A long thin rectangle always has the larger perimeter and the
smaller area than the compared square or compact rectangle; all numbers are computed from the side lengths."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "pro04_mc"
TID, CODE = "PRO-04", "MC"
BAD = ("Piirin kasvaminen ei tarkoita pinta-alan kasvamista. Ohut ja pitkä suorakulmio voi olla pienempi alaltaan "
       "kuin pienempipiirinen, mutta tasaisempi kuvio.")
GOOD = "Oikein: suurempi piiri ei takaa suurempaa alaa, vaan ala lasketaan sivujen tulona."


def thin_and_square(rng):
    """Return (w, h, s) with thin rectangle w x h, square side s: P_rect > P_square but A_rect < A_square."""
    while True:
        h = rng.randint(1, 2)
        w = rng.randint(8, 16)
        s = rng.randint(4, 7)
        if 2 * (w + h) > 4 * s and w * h < s * s:
            return w, h, s


def make_items(run, date, count=5, start=1):
    rng = random.Random(841)
    items = []
    for k in range(count):
        w, h, s = thin_and_square(rng)
        pr, ps, ar, as_ = 2 * (w + h), 4 * s, w * h, s * s
        if k == 0:
            level = "T"
            prompt = f"Suorakulmion sivut ovat {w} cm ja {h} cm. Neliön sivu on {s} cm. Kummalla kuviolla on suurempi pinta-ala?"
            ok = (f"Neliöllä: sen ala on {as_} cm² ja suorakulmion {ar} cm²", f"Oikein: {s} · {s} = {as_} cm² ja {w} · {h} = {ar} cm².")
            wrongs = [(f"Suorakulmiolla, koska sen piiri on {pr} cm ja neliön {ps} cm", TID, BAD),
                      ("Kuvioilla on sama ala", None, f"Alat ovat {ar} cm² ja {as_} cm²."),
                      ("Sitä ei voi tietää, koska muodot ovat erilaiset", None, "Pinta-alat voi laskea ja verrata.")]
            steps = [f"Suorakulmion ala {w} · {h} = {ar} cm², piiri {pr} cm", f"Neliön ala {s} · {s} = {as_} cm², piiri {ps} cm"]
            final, params = ok[0], {"w": w, "h": h, "s": s}
        elif k == 1:
            level = "T"
            prompt = (f"Huone A on {w} m × {h} m ja huone B on {s} m × {s} m. Huoneen A lattian reunalistaa kuluu enemmän. "
                      "Onko huoneen A lattiapinta-ala silloin suurempi?")
            ok = (f"Ei: huoneen A ala on {ar} m² ja huoneen B {as_} m²", f"Oikein: A:n piiri on suurempi ({pr} m > {ps} m), mutta ala pienempi.")
            wrongs = [("Kyllä, koska sen piiri on suurempi", TID, BAD),
                      ("Kyllä, koska reunalistaa kuluu enemmän ja ala on silloin aina suurempi", TID, BAD),
                      (f"Ei: huoneiden alat ovat yhtä suuret, {ar} m²", None, f"Huoneen B ala on {as_} m².")]
            steps = [f"A: piiri {pr} m, ala {ar} m²", f"B: piiri {ps} m, ala {as_} m²"]
            final, params = ok[0], {"w": w, "h": h, "s": s}
        elif k == 2:
            level = "T"
            prompt = (f"Oppilas väittää: \"Jos kuvion piiri on suurempi, myös sen pinta-ala on suurempi.\" "
                      f"Vertaa suorakulmiota {w} cm × {h} cm ja neliötä {s} cm × {s} cm. Mikä väite on oikein?")
            ok = (f"Väite on väärä: suorakulmion piiri on {pr} cm > {ps} cm, mutta ala {ar} cm² < {as_} cm²", GOOD)
            wrongs = [("Väite on oikea: suurempi piiri tarkoittaa aina suurempaa alaa", TID, BAD),
                      (f"Väite on oikea, koska suorakulmion pidempi sivu on {w} cm", TID, BAD),
                      ("Väite on väärä, koska piiri ja ala eivät liity toisiinsa mitenkään", None, "Piiri ja ala molemmat riippuvat sivuista, mutta eri tavalla.")]
            steps = [f"Suorakulmio: piiri {pr} cm, ala {ar} cm²", f"Neliö: piiri {ps} cm, ala {as_} cm²"]
            final, params = ok[0], {"w": w, "h": h, "s": s}
        elif k == 3:
            level = "H"
            prompt = (f"Kaksi pellon aitausta: suorakulmio {w} m × {h} m ja neliö {s} m × {s} m. Aitausten sisälle kylvetään ruohoa. "
                      "Kummassa aitauksessa on enemmän ruohoa ja kummassa kuluu enemmän aitaa?")
            ok = (f"Ruohoa on enemmän neliössä, aitaa kuluu enemmän suorakulmioon", f"Oikein: neliön ala {as_} m² > {ar} m², suorakulmion piiri {pr} m > {ps} m.")
            wrongs = [("Suorakulmiossa on enemmän ruohoa ja siihen kuluu enemmän aitaa", TID, BAD),
                      ("Neliössä on enemmän ruohoa ja siihen kuluu enemmän aitaa", None, f"Neliön piiri on {ps} m, suorakulmion {pr} m."),
                      ("Aitausten ruohomäärät ja aitamäärät ovat samat", None, "Sekä alat että piirit eroavat.")]
            steps = [f"Suorakulmio: piiri {pr} m, ala {ar} m²", f"Neliö: piiri {ps} m, ala {as_} m²"]
            final, params = ok[0], {"w": w, "h": h, "s": s}
        else:
            level = "H"
            prompt = "Miksi kuvion piirin kasvattaminen ei välttämättä kasvata sen pinta-alaa?"
            ok = (f"Ala riippuu sivujen tulosta: esimerkiksi {w} × {h} (piiri {pr}, ala {ar}) on ohut, kun taas {s} × {s} (piiri {ps}) on alaltaan suurempi, {as_}", GOOD)
            wrongs = [("Piiri ja ala kasvavat aina yhtä aikaa, joten kasvattaminen aina kasvattaa alaa", TID, BAD),
                      ("Pinta-alaan vaikuttaa vain kuvion korkeus", None, "Ala riippuu molemmista sivumitoista."),
                      ("Piiri mitataan neliösenteissä, joten sitä ei voi verrata alaan", None, "Piiri mitataan pituusyksiköissä; syy on muussa.")]
            steps = [f"{w} × {h}: piiri {pr}, ala {ar}", f"{s} × {s}: piiri {ps}, ala {as_}"]
            final, params = ok[0], {"w": w, "h": h, "s": s}
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S5.07"], ["T18"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
