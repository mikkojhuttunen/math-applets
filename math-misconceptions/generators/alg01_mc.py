#!/usr/bin/env python3
"""ALG-01 (letter read as an object label), type MC.

Numbers come from a fixed seed; every option text is built from the same numbers.
Usage: python generators/alg01_mc.py --run 1 --date 2026-09-30 --write
"""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "alg01_mc"
TID, CODE = "ALG-01", "MC"
# (A partitive, B partitive, A price label, B price label, unit)
CTX = [
    ("omenaa", "päärynää", "omenan", "päärynän", "senttiä"),
    ("pullaa", "pirtelöä", "pullan", "pirtelön", "euroa"),
    ("vihkoa", "kynää", "vihon", "kynän", "euroa"),
    ("elokuvalippua", "karkkipussia", "elokuvalipun", "karkkipussin", "euroa"),
    ("tarraa", "korttia", "tarran", "kortin", "senttiä"),
]
BAD = "Kirjain luetaan tavaran nimeksi. Kirjain on kuitenkin luku: se kertoo, montako kappaletta ostetaan."


def make_items(run, date, count=5, start=1):
    rng = random.Random(101)
    items = []
    for k in range(count):
        ca, cb, la, lb, unit = CTX[k]
        pa, pb = rng.randint(2, 9), rng.randint(2, 9)
        while pb == pa:
            pb = rng.randint(2, 9)
        x, y = ("a", "p") if k % 2 == 0 else ("m", "n")
        expr = f"{pa}{x} + {pb}{y}"
        intro = (f"{la.capitalize()} hinta on {pa} {unit} ja {lb} hinta {pb} {unit}. "
                 f"Ostetaan {x} kpl ({ca}) ja {y} kpl ({cb}).")
        params = {"pa": pa, "pb": pb, "vars": [x, y], "context": k + 1}
        if k < 3:
            level = "T"
            prompt = f"{intro} Mitä lauseke {expr} kertoo?"
            options, cid = mc_options(rng, (f"Ostosten yhteishinnan ({unit})", "Oikein: lauseke on yhteishinta."), [
                (f"{pa} {ca} ja {pb} {cb}", "ALG-01", BAD),
                ("Ostettujen tuotteiden yhteismäärän", None, f"Lauseke kertoo hinnan, ei kappalemäärää: {pa}{x} on {x} tuotteen hinta."),
                ("Yhden kappaleen hinnan molemmista tuotteista", None,
                 f"Yhden kappaleen hinta olisi {pa} + {pb}, ilman kirjaimia."),
            ])
            steps = [f"{pa}{x}: {x} kappaletta, hinta {pa} {unit} kappaleelta, yhteensä {pa} · {x} {unit}",
                     f"{pb}{y}: {y} kappaletta, hinta {pb} {unit} kappaleelta, yhteensä {pb} · {y} {unit}",
                     f"Summa {expr} on koko ostoksen hinta"]
            final = f"Yhteishinta ({unit})"
        elif k == 3:
            level = "H"
            prompt = f"{intro} Mitä kirjain {x} tarkoittaa lausekkeessa {expr}?"
            options, cid = mc_options(rng, ("Ensimmäisen tuotteen kappalemäärää, eli lukua", "Oikein: kirjain on lukumäärä."), [
                ("Ensimmäistä tuotetta itseään, esinettä", "ALG-01", BAD),
                ("Ensimmäisen tuotteen hintaa", None, f"Hinta on jo annettu: {pa} {unit}. Kirjain on määrä."),
                ("Molempien tuotteiden yhteishintaa", None, "Yhteishinta on koko lauseke, ei yksi kirjain."),
            ])
            steps = [f"Hinta {pa} {unit} on annettu lukuna", f"Kertoimena {x} on se, montako kappaletta ostetaan",
                     f"Siksi {x} on luku (kappalemäärä), ei esine"]
            final = "Kappalemäärää, eli lukua"
        else:
            level = "H"
            prompt = (f"{intro} Aino sanoo: \"Lauseke {expr} tarkoittaa {pa} {ca} ja {pb} {cb}.\" "
                      "Miksi väite on virheellinen?")
            options, cid = mc_options(rng, ("Kirjaimet ovat lukuja (määriä), joten lauseke on hinta eikä tuotteiden lista",
                                            "Oikein: kirjain edustaa lukua."), [
                ("Väite on oikein: kirjain voi lyhentää tuotteen nimeä", "ALG-01", BAD),
                ("Lausekkeesta puuttuu yhtäsuuruusmerkki", None, "Lauseke ei tarvitse yhtäsuuruusmerkkiä."),
                ("Kerroin ja kirjain pitäisi kirjoittaa toisin päin", None, f"{pa}{x} ja {x}·{pa} ovat sama asia."),
            ])
            steps = [f"{x} ja {y} ovat määriä eli lukuja", f"{pa}{x} = {pa} · {x} on hinta {unit}",
                     "Lauseke on lasku, ei luettelo esineistä"]
            final = "Kirjaimet ovat lukuja, joten lauseke kertoo hinnan"
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T4", "T15"] if k == 4 else ["T7", "T15"], 7,
                               level, prompt, payload, steps, final,
                               "Oikein: kirjain kertoo määrän, luku hinnan, ja lauseke on hinta.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
