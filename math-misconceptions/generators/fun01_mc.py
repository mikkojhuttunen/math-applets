#!/usr/bin/env python3
"""FUN-01 (graph as picture), type MC. Situations are given as value tables; the correct graph description
(rising / constant / falling) is computed from the numbers, the distractor reads the graph as the shape of the route."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "fun01_mc"
TID, CODE = "FUN-01", "MC"
BAD = ("Kuvaaja ei ole kuva tiestä tai reitistä. Vaaka-akselilla on aika, ja kuvaaja näyttää, miten pystyakselin suure "
       "muuttuu ajan kuluessa.")
GOOD = "Oikein: kuvaajan muoto riippuu siitä, miten suure muuttuu ajan funktiona, ei tilanteen ulkonäöstä."


def trend(a, b):
    return "kasvaa" if b > a else "pienenee" if b < a else "pysyy samana"


def make_items(run, date, count=5, start=1):
    rng = random.Random(3319)
    items = []
    for k in range(count):
        if k == 0:
            v0 = rng.randint(5, 12)
            v1 = v0 + rng.randint(12, 20)
            v2 = rng.randint(6, v0 + 4)
            assert trend(v0, v1) == "kasvaa" and trend(v1, v1) == "pysyy samana" and trend(v1, v2) == "pienenee"
            prompt = (f"Pyöräilijä ajaa ensin alas mäkeä, sitten tasaista tietä ja lopuksi ylös mäkeä. Hänen nopeutensa on "
                      f"mäen alussa {v0} km/h, tasaisen tien alussa ja lopussa {v1} km/h ja ylämäen lopussa {v2} km/h. "
                      "Millainen nopeus–aika-kuvaaja sopii tilanteeseen?")
            ok = (f"Nopeus kasvaa ({v0} → {v1} km/h), pysyy vakiona ({v1} km/h) ja pienenee ({v1} → {v2} km/h)",
                  "Oikein: nopeus muuttuu juuri näin, ja kuvaajan muoto seuraa nopeuden muutosta.")
            wrongs = [("Kuvaaja laskee, on vaakasuora ja nousee, kuten tien muoto: alas, tasaista, ylös", TID, BAD),
                      (f"Nopeus pysyy koko ajan {v1} km/h", None, f"Nopeus on {v0} km/h mäen alussa ja {v2} km/h lopussa."),
                      ("Nopeus pienenee koko ajan", None, f"Alamäessä nopeus kasvaa ({v0} → {v1} km/h).")]
            level, params = "T", {"v0": v0, "v1": v1, "v2": v2}
            steps = [f"Alamäki: {v0} → {v1}, nopeus kasvaa", f"Tasainen tie: {v1}, pysyy samana", f"Ylämäki: {v1} → {v2}, nopeus pienenee"]
            final = ok[0]
        elif k == 1:
            v = rng.randint(12, 24)
            ts = [0, 1, 2, 3]
            ss = [v * t for t in ts]
            assert all(ss[i + 1] > ss[i] for i in range(3))
            prompt = (f"Pyöräilijä ajaa {v} km/h tasaista vauhtia tietä, joka kulkee ensin ylämäkeen, sitten tasaisena ja lopuksi alamäkeen. "
                      f"Kuvaajassa vaaka-akselilla on aika (h) ja pystyakselilla kuljettu matka (km). Matka on 0, {ss[1]}, {ss[2]} ja {ss[3]} km, "
                      "kun aikaa on kulunut 0, 1, 2 ja 3 h. Millainen kuvaaja on?")
            ok = (f"Suoraan nouseva kuvaaja: matka kasvaa {v} km joka tunti", "Oikein: tasainen vauhti antaa suoran, vaikka tie nousisi ja laskisi.")
            wrongs = [("Kuvaaja nousee, on vaakasuora ja laskee, kuten tien profiili", TID, BAD),
                      ("Kuvaaja on vaakasuora, koska tie on suurimmaksi osaksi tasainen", TID, BAD),
                      (f"Kuvaaja laskee, koska matka pienenee", None, f"Matka kasvaa: {ss[1]}, {ss[2]}, {ss[3]} km.")]
            level, params = "T", {"v": v}
            steps = [f"s = {v}t", f"Matkat {ss[0]}, {ss[1]}, {ss[2]}, {ss[3]} km: kasvaa tasaisesti"]
            final = ok[0]
        elif k == 2:
            d = rng.randint(2, 6) * 100
            m = rng.randint(3, 8)
            prompt = (f"Pekka kävelee kotoa kauppaan, ja matka–aika-kuvaajassa vaaka-akseli on aika (min) ja pystyakseli matka kotoa (m). "
                      f"Kaupan edessä hän seisoo {m} minuuttia {d} m:n päässä kotoa. Miltä tämä aikaväli näyttää kuvaajassa?")
            ok = (f"Vaakasuora jana korkeudella {d} m: matka ei muutu {m} minuuttiin", "Oikein: paikallaan seisominen on vaakasuora jana.")
            wrongs = [("Pystysuora jana, koska Pekka seisoo pystyssä", TID, BAD),
                      ("Nouseva jana, koska hän on kaupan edessä", None, "Matka kotoa ei kasva, kun hän seisoo paikallaan."),
                      ("Laskeva jana, koska hän on pysähtynyt", None, "Matka kotoa pysyy samana.")]
            level, params = "T", {"d": d, "m": m}
            steps = [f"{m} min ajan matka on {d} m", "Matka ei muutu: vaakasuora jana"]
            final = ok[0]
        elif k == 3:
            a = rng.randint(1, 3) * 100
            b = a + rng.randint(1, 3) * 100
            c = b
            e = c + rng.randint(1, 3) * 100
            ss = [0, a, b, c, e]
            flat = [i for i in range(4) if ss[i] == ss[i + 1]]
            assert len(flat) == 1
            t0, t1 = flat[0], flat[0] + 1
            prompt = (f"Matka–aika-taulukko (aika minuutteina, matka metreinä): 0 min: 0, 1 min: {a}, 2 min: {b}, 3 min: {c}, 4 min: {e}. "
                      f"Kuvaaja on vaakasuora aikavälillä {t0}–{t1} min. Mitä kävelijä tällä välillä tekee?")
            ok = ("Seisoo paikallaan, koska matka ei muutu", "Oikein: vaakasuora osa tarkoittaa, että suure ei muutu.")
            wrongs = [("Kävelee tasaista tietä, koska kuvaaja on tasainen", TID, BAD),
                      ("Kävelee kovinta vauhtia, koska kuvaaja on pitkä", None, "Vauhti näkyy kuvaajan jyrkkyydestä."),
                      ("Kävelee takaisin kotia kohti", None, "Matka kotoa ei pienene.")]
            level, params = "H", {"s": ss}
            steps = [f"{t0}–{t1} min: matka {ss[t0]} → {ss[t1]} m", "Matka ei muutu: kävelijä seisoo"]
            final = ok[0]
        else:
            v = rng.randint(4, 9)
            prompt = (f"Oppilas sanoo: \"Matka–aika-kuvaaja, jossa kuljetaan {v} m/s, on kuva siitä, miltä reitti näyttää.\" "
                      "Mikä on paras vastaus?")
            ok = (f"Ei ole: kuvaaja s = {v}t näyttää, miten matka kasvaa ajan kuluessa, ja reitti voi olla mutkainen tai mäkinen",
                  GOOD)
            wrongs = [("On: kuvaajan muoto kertoo, onko reitti suora, mäkinen vai mutkainen", TID, BAD),
                      ("On: jos reitti kääntyy, myös kuvaaja kääntyy samaan suuntaan", TID, BAD),
                      (f"Ei ole, koska nopeus {v} m/s ei voi näkyä kuvaajassa", None, "Nopeus näkyy kuvaajan jyrkkyytenä.")]
            level, params = "H", {"v": v}
            steps = [f"s = {v}t", "Vaaka-akseli on aika, ei paikka"]
            final = ok[0]
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S4.07"], ["T8", "T15"], 9, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
