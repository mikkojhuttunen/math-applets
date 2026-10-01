#!/usr/bin/env python3
"""FUN-02 (slope-height confusion), type MC. Two distance-time lines are built so that the faster one is lower
before the crossing point; the speeds are computed from the tabulated points."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "fun02_mc"
TID, CODE = "FUN-02", "MC"
HEIGHT = ("Kuvaajan korkeus kertoo vain sen, kuinka pitkän matkan kohde on kulkenut. Nopeuden kertoo jyrkkyys: "
          "kuinka paljon matka kasvaa aikayksikössä.")


def coef(v):
    return "" if v == 1 else str(v)


def lines(rng):
    """Return (vF, cF, vS, cS, t0): the faster line starts lower and crosses the slower one at t0."""
    while True:
        vS = rng.randint(1, 4)
        vF = vS + rng.randint(1, 3)
        t0 = rng.randint(3, 5)
        cF = rng.randint(0, 3)
        cS = cF + (vF - vS) * t0
        if cS <= 40:
            return vF, cF, vS, cS, t0


def make_items(run, date, count=5, start=1):
    rng = random.Random(641)
    items = []
    for n in range(count):
        vF, cF, vS, cS, t0 = lines(rng)
        names = ["A", "B"]
        rng.shuffle(names)
        F, S = names  # F is faster
        pos = {F: (cF, vF), S: (cS, vS)}
        def pt(name, t):
            c, v = pos[name]
            return c + v * t
        q = 2
        assert pt(S, q) > pt(F, q) and pt(S, 0) > pt(F, 0)
        assert pt(F, t0) == pt(S, t0)
        if n in (0, 1, 2):
            level = "T"
            ctx = [("pyöräilijää", "km", "h", "Kaksi pyöräilijää"), ("juoksijaa", "km", "h", "Kaksi juoksijaa"),
                   ("vesisäiliötä", "l", "min", "Kaksi vesisäiliötä täyttyy letkuilla.")][n]
            unit, tu = ctx[1], ctx[2]
            what = "kulkee" if n < 2 else "täyttyy"
            head = (f"{ctx[3]} A ja B lähtevät samaan aikaan. Etäisyys lähtöpisteestä ({unit}) ajan ({tu}) funktiona:"
                    if n < 2 else f"{ctx[3]} Vettä on säiliöissä (l) ajan (min) funktiona:")
            tbl = f"A: t = 0 → {pt('A', 0)} {unit}, t = {q} → {pt('A', q)} {unit}. B: t = 0 → {pt('B', 0)} {unit}, t = {q} → {pt('B', q)} {unit}."
            ask = "Kumpi " + ("kulkee" if n < 2 else "täyttyy") + (" nopeammin?" if n != 1 else " hitaammin?")
            answer_name = F if n != 1 else S
            wrong_name = S if n != 1 else F
            prompt = f"{head} {tbl} Kuvaajat (aika–määrä) leikkaavat, kun t = {t0}. {ask}"
            ok = (f"{answer_name}", f"Oikein: {answer_name}:n määrä kasvaa {'nopeammin' if n != 1 else 'hitaammin'}. " +
                  f"A:n nopeus on {(pt('A', q) - pt('A', 0)) // q} ja B:n {(pt('B', q) - pt('B', 0)) // q} {unit}/{tu}.")
            wrongs = [(f"{wrong_name}", "FUN-02", HEIGHT), ("Yhtä nopeasti, koska kuvaajat leikkaavat.", None,
                      "Leikkauspiste kertoo vain, että määrät ovat yhtä suuret sillä hetkellä. Nopeus on kuvaajan jyrkkyys."),
                      ("Sitä ei voi päätellä annetuista tiedoista.", None, "Kahdesta pisteestä lasketaan muutos aikayksikköä kohti.")]
            steps = [f"A: ({pt('A', q)} − {pt('A', 0)}) / {q} = {(pt('A', q) - pt('A', 0)) // q} {unit}/{tu}",
                     f"B: ({pt('B', q)} − {pt('B', 0)}) / {q} = {(pt('B', q) - pt('B', 0)) // q} {unit}/{tu}"]
            final, params = ok[0], {"vF": vF, "cF": cF, "vS": vS, "cS": cS, "t0": t0, "faster": F, "q": q, "context": ctx[0]}
        elif n == 3:
            level = "H"
            prompt = (f"Kaksi juoksijaa: A:n matka (km) on s = {coef(pos['A'][1])}t + {pos['A'][0]} ja B:n matka s = {coef(pos['B'][1])}t + {pos['B'][0]}, missä t on aika tunteina. "
                      f"Kumpi juoksija on hetkellä t = 1 kauempana lähtöpisteestä ja kumpi juoksee nopeammin?")
            far = S if pt(S, 1) > pt(F, 1) else F
            assert far == S
            ok = (f"Kauempana on {S}, nopeammin juoksee {F}.", f"Oikein: {S}:n matka on t = 1 suurempi ({pt(S, 1)} km), mutta {F}:n nopeus on suurempi ({vF} km/h).")
            wrongs = [(f"{S} on kauempana ja myös juoksee nopeammin.", "FUN-02", HEIGHT),
                      (f"Kauempana on {F}, nopeammin juoksee {S}.", None, f"Tarkista luvut: t = 1 antaa {S}:lle {pt(S, 1)} km ja {F}:lle {pt(F, 1)} km."),
                      (f"{F} on kauempana ja myös juoksee nopeammin.", None, f"Tarkista luvut: t = 1 antaa {S}:lle {pt(S, 1)} km ja {F}:lle {pt(F, 1)} km.")]
            steps = [f"t = 1: {S} {pt(S, 1)} km, {F} {pt(F, 1)} km", f"Nopeudet (termin t kerroin): {S} {pos[S][1]} km/h, {F} {vF} km/h"]
            final, params = ok[0], {"vF": vF, "cF": cF, "vS": vS, "cS": cS, "faster": F, "q": 1}
        else:
            level = "H"
            prompt = (f"Kahden kohteen matka–aika-kuvaajat leikkaavat, kun t = {t0}. Ennen leikkauspistettä {S}:n kuvaaja on {F}:n kuvaajan yläpuolella. "
                      f"Mikä perustelu on oikea, kun kysytään, kumpi liikkuu nopeammin?")
            ok = (f"Ylempänä oleva {S} on kauempana, mutta nopeutta kuvaa jyrkkyys. {F}:n kuvaaja nousee jyrkemmin, joten {F} liikkuu nopeammin.",
                  "Oikein: korkeus on matka, jyrkkyys on nopeus.")
            wrongs = [(f"{S} liikkuu nopeammin, koska sen kuvaaja on ylempänä.", "FUN-02", HEIGHT),
                      (f"{F} liikkuu nopeammin, koska kuvaajat leikkaavat sen kohdalla.", None, "Leikkauspiste ei kerro nopeutta vaan sen, että matkat ovat yhtä suuret."),
                      ("Nopeus on sama, koska kuvaajat kohtaavat.", None, "Kuvaajat voivat leikata, vaikka jyrkkyydet ovat erilaiset.")]
            steps = [f"Korkeus = matka: {S} on kauempana kuin {F} ennen t = {t0}", f"Jyrkkyys = nopeus: {F} {vF}, {S} {vS}"]
            final, params = ok[0], {"vF": vF, "cF": cF, "vS": vS, "cS": cS, "t0": t0, "faster": F}
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + n, ["S4.07"], ["T8", "T15"], 9, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: matka–aika-kuvaajassa nopeus on jyrkkyys, ei korkeus.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
