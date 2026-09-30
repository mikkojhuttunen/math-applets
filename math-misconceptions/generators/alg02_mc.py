#!/usr/bin/env python3
"""ALG-02 (different letters must differ in value), type MC. Fixed seed, options computed from the numbers."""
import random

from gen_common import MINUS, base_item, cli, mc_options

TEMPLATE = "alg02_mc"
TID, CODE = "ALG-02", "MC"
OP = "Eri kirjaimet voivat tarkoittaa samaa lukua. Kirjain on vain paikan pitäjä, ei luvun nimi."
PAIRS = [("a", "b"), ("m", "n"), ("c", "d"), ("p", "q"), ("s", "t")]


def make_items(run, date, count=5, start=1):
    rng = random.Random(301)
    items = []
    for k in range(count):
        u, w = PAIRS[k]
        h = rng.randint(3, 9)
        s = 2 * h
        if k == 0:
            level = "T"
            prompt = f"Luvuille {u} ja {w} pätee {u} + {w} = {s}. Voiko olla {u} = {w}?"
            options, cid = mc_options(rng, (f"Voi: {u} = {h} ja {w} = {h}", "Oikein: eri kirjaimet saavat olla sama luku."), [
                (f"Ei voi, koska {u} ja {w} ovat eri kirjaimia", TID, OP),
                (f"Voi vain, jos {u} = {s} ja {w} = 0", None, f"Silloin {u} ≠ {w}. Kokeile lukuja, jotka ovat yhtä suuret."),
                (f"Ei voi, koska {u} + {w} ei ole {s}", None, f"Tarkista: {h} + {h} = {s}."),
            ])
            steps = [f"Kokeillaan {u} = {h} ja {w} = {h}", f"{h} + {h} = {s}", f"Ehto {u} + {w} = {s} toteutuu, joten {u} = {w} on mahdollinen"]
            final = f"Voi: {u} = {w} = {h}"
        elif k == 1:
            level = "T"
            prompt = f"Luvuille {u} ja {w} pätee {u} · {w} = {h * h}. Mikä väite on tosi?"
            options, cid = mc_options(rng, (f"{u} = {h} ja {w} = {h} on mahdollinen", "Oikein: kirjaimilla saa olla sama arvo."), [
                (f"{u} ja {w} eivät voi olla yhtä suuret", TID, OP),
                (f"{u} ja {w} ovat aina {h}", None, f"Muitakin pareja on, esimerkiksi {u} = 1 ja {w} = {h * h}."),
                (f"Ehto ei voi toteutua, koska {h * h} ei ole tulo", None, f"Tarkista: {h} · {h} = {h * h}."),
            ])
            steps = [f"{h} · {h} = {h * h}", f"Siis {u} = {h}, {w} = {h} sopii ehtoon"]
            final = f"{u} = {w} = {h} on mahdollinen"
        elif k == 2:
            level = "T"
            ca, cb = rng.randint(2, 5), rng.randint(2, 5)
            while cb == ca:
                cb = rng.randint(2, 5)
            value = ca * h + cb * h
            prompt = f"Laske lausekkeen {ca}{u} + {cb}{w} arvo, kun {u} = {h} ja {w} = {h}."
            options, cid = mc_options(rng, (str(value), "Oikein: sijoita kummankin kirjaimen paikalle luku."), [
                ("Ei voi laskea, koska kirjainten arvot ovat samat", TID, OP),
                (str(ca * h + cb), None, f"Kirjaimen {w} paikalle sijoitetaan {h}, ja sillä kerrotaan {cb}."),
                (str(ca * cb * h), None, "Kertoimet kerrotaan kirjaimen arvolla, ei keskenään."),
            ])
            steps = [f"{ca}{u} + {cb}{w} = {ca} · {h} + {cb} · {h}", f"= {ca * h} + {cb * h}", f"= {value}"]
            final = str(value)
        elif k == 3:
            level = "H"
            prompt = (f"Ville sanoo: 'Yhtälön {u} + {w} = {s} ratkaisu {u} = {h}, {w} = {h} ei kelpaa, "
                      f"koska eri kirjaimet tarkoittavat eri lukuja.' Mikä on oikea perustelu?")
            options, cid = mc_options(rng, (f"Ratkaisu kelpaa: {h} + {h} = {s}, ja kirjaimet saavat olla yhtä suuret", "Oikein: yhtälön toteuttavat kaikki luvut, joilla ehto pätee."), [
                ("Ville on oikeassa: eri kirjaimilla on aina eri arvot", TID, OP),
                (f"Ratkaisu ei kelpaa, koska {h} ei ole {s}", None, f"Kirjainten summa on {h} + {h} = {s}."),
                ("Ville on oikeassa, koska ratkaisuja on vain yksi", None, "Ratkaisuja on monta, esimerkiksi myös eri lukuparit."),
            ])
            steps = [f"Sijoitus: {h} + {h} = {s}", "Yhtälö toteutuu", "Mikään sääntö ei vaadi eri kirjaimille eri arvoja"]
            final = "Eri kirjaimet saavat olla sama luku"
        else:
            level = "H"
            age = rng.randint(6, 12)
            prompt = (f"Kaksoset ovat {age}-vuotiaita. Aino on {u} vuotta ja Eetu {w} vuotta. "
                      f"Mikä väite on tosi?")
            options, cid = mc_options(rng, (f"{u} = {w} = {age}, vaikka kirjaimet ovat eri", "Oikein: samaa lukua voi merkitä kahdella kirjaimella."), [
                (f"Koska kirjaimet ovat {u} ja {w}, ikien täytyy olla eri", TID, OP),
                (f"{u} + {w} = {age}", None, f"Yhteenlasku olisi {age} + {age} = {2 * age}."),
                (f"{u} = {age} mutta {w} = {age} {MINUS} 1", None, "Kaksosilla on sama ikä."),
            ])
            steps = [f"Aino: {u} = {age}", f"Eetu: {w} = {age}", "Kirjaimet ovat eri, arvot samat"]
            final = f"{u} = {w} = {age}"
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T15"], 7, level, prompt, payload, steps, final,
                               "Oikein: eri kirjaimet saavat tarkoittaa samaa lukua.", TEMPLATE,
                               {"h": h, "pair": [u, w]}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
