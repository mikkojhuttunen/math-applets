#!/usr/bin/env python3
"""GEO-01 (prototype-bound concept of triangle), type MC. Triangles are given by coordinates, angles or side lengths;
whether they are triangles (non-collinear vertices, angle sum, triangle inequality) is decided by code."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "geo01_mc"
TID, CODE = "GEO-01", "MC"
BAD = ("Kolmio on suljettu kuvio, jolla on kolme suoraa sivua. Kuvion asento, symmetria tai sivujen pituudet "
       "eivät vaikuta siihen, onko se kolmio.")
GOOD = "Oikein: kolme suoraa sivua ja suljettu kuvio riittävät, kuvio saa olla vinossa ja epäsymmetrinen."


def area2(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def pts_text(ps):
    return ", ".join(f"{n}({x}, {y})" for n, (x, y) in zip("ABC", ps))


def tilted_scalene(rng):
    """Three lattice points: non-collinear, all sides different, no right angle, no horizontal or vertical side."""
    while True:
        ps = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(3)]
        a2 = area2(*ps)
        if a2 == 0:
            continue
        sq = sorted([d2(ps[0], ps[1]), d2(ps[1], ps[2]), d2(ps[0], ps[2])])
        if len(set(sq)) < 3 or sq[0] + sq[1] == sq[2]:
            continue
        if any(ps[i][0] == ps[j][0] or ps[i][1] == ps[j][1] for i in range(3) for j in range(i + 1, 3)):
            continue
        return ps, a2


def collinear(rng):
    while True:
        x, y = rng.randint(0, 3), rng.randint(0, 3)
        dx, dy = rng.randint(1, 3), rng.randint(1, 3)
        ps = [(x, y), (x + dx, y + dy), (x + 2 * dx, y + 2 * dy)]
        if area2(*ps) == 0:
            return ps


def obtuse_angles(rng):
    while True:
        a = rng.randint(101, 140)
        b = rng.randint(15, 180 - a - 15)
        c = 180 - a - b
        if c > 0 and len({a, b, c}) == 3:
            return a, b, c


def scalene_sides(rng):
    while True:
        s = sorted(rng.sample(range(3, 15), 3))
        if s[0] + s[1] > s[2]:
            return s


def half(n2):
    return f"{n2 // 2},5" if n2 % 2 else str(n2 // 2)


def make_items(run, date, count=5, start=1):
    rng = random.Random(1701)
    items = []
    for k in range(count):
        if k == 0:
            ps, a2 = tilted_scalene(rng)
            assert a2 > 0
            prompt = (f"Koordinaatistoon piirretään kuvio, jonka kärjet ovat {pts_text(ps)}. Pisteet yhdistetään janoilla. "
                      "Onko syntyvä kuvio kolmio?")
            ok = (f"Kyllä: pisteet eivät ole samalla suoralla, ja kuvion ala on {half(a2)} ruutua",
                  "Oikein: kolme pistettä, jotka eivät ole samalla suoralla, määräävät kolmion, vaikka se olisi vinossa.")
            wrongs = [("Ei, koska kolmion täytyy olla symmetrinen", TID, BAD),
                      ("Ei, koska yksikään sivu ei ole vaakasuora ja kolmion pohjan pitää olla alhaalla", TID, BAD),
                      ("Kyllä, mutta vain jos kaikki sivut ovat yhtä pitkät", None, "Kolmion sivut saavat olla eri pituisia.")]
            level, params = "T", {"points": ps, "twice_area": a2}
            steps = [f"Kärjet {pts_text(ps)}", f"Pisteet eivät ole samalla suoralla: ala {half(a2)} > 0", "Kuvio on kolmio"]
            final = ok[0]
        elif k == 1:
            a, b, c = obtuse_angles(rng)
            assert a + b + c == 180
            prompt = (f"Kuviolla on kolme suoraa sivua ja sen kulmat ovat {a}°, {b}° ja {c}°. "
                      "Onko kuvio kolmio?")
            ok = (f"Kyllä: kulmien summa on {a} + {b} + {c} = 180°",
                  "Oikein: kolmion yksi kulma saa olla tylppä, kunhan kulmien summa on 180°.")
            wrongs = [(f"Ei, koska kolmiossa kaikkien kulmien pitää olla teräviä ja {a}° on tylppä", TID, BAD),
                      ("Ei, koska kolmion kulmat ovat aina yhtä suuret", TID, BAD),
                      ("Kyllä, koska kulmien summa on 360°", None, f"Kulmien summa on {a} + {b} + {c} = 180°.")]
            level, params = "T", {"angles": [a, b, c]}
            steps = [f"{a} + {b} + {c} = 180", "Kulmasumma on kolmion kulmasumma"]
            final = ok[0]
        elif k == 2:
            a, b, c = scalene_sides(rng)
            assert a + b > c
            prompt = (f"Kukkapenkin reunat ovat suoria ja niiden pituudet ovat {a} m, {b} m ja {c} m. "
                      "Onko penkin muoto kolmio?")
            ok = (f"Kyllä: {a} + {b} = {a + b} > {c}, joten sivuista saa kolmion, vaikka ne ovat eri pituisia",
                  "Oikein: kolmion sivut saavat olla eri pituisia, kunhan kaksi lyhintä sivua on yhteensä pidempiä kuin pisin.")
            wrongs = [("Ei, koska kolmion kaikkien sivujen pitää olla yhtä pitkät", TID, BAD),
                      ("Ei, koska oikea kolmio on tasakylkinen", TID, BAD),
                      (f"Ei, koska {a} + {b} < {c}", None, f"{a} + {b} = {a + b}, mikä on suurempi kuin {c}.")]
            level, params = "T", {"sides": [a, b, c]}
            steps = [f"{a} + {b} = {a + b} > {c}", "Sivuista voi muodostaa kolmion"]
            final = ok[0]
        elif k == 3:
            line = collinear(rng)
            tri = [tilted_scalene(rng)[0] for _ in range(3)]
            prompt = ("Mikä seuraavista pistejoukoista EI muodosta kolmiota, kun pisteet yhdistetään janoilla?")
            ok = (f"{pts_text(line)}", f"Oikein: pisteet ovat samalla suoralla (ala 0), joten kolmiota ei synny.")
            wrongs = [(pts_text(t), TID, "Nämä pisteet eivät ole samalla suoralla, joten ne muodostavat kolmion, vaikka se näyttää vinolta.")
                      for t in tri]
            wrongs = [(t, m, f) for t, m, f in wrongs]
            seen = {w[0] for w in wrongs} | {ok[0]}
            if len(seen) < 4:   # identical random triples: redraw deterministically
                tri = []
                while len(tri) < 3:
                    t = tilted_scalene(rng)[0]
                    if pts_text(t) not in {pts_text(x) for x in tri}:
                        tri.append(t)
                wrongs = [(pts_text(t), TID, "Nämä pisteet eivät ole samalla suoralla, joten ne muodostavat kolmion, vaikka se näyttää vinolta.") for t in tri]
            level, params = "H", {"collinear": line, "triangles": tri}
            steps = [f"{pts_text(line)}: ala 0", "Muut pistejoukot antavat ala > 0"]
            final = ok[0]
        else:
            ps, a2 = tilted_scalene(rng)
            prompt = (f"Kuvion kärjet ovat {pts_text(ps)}. Oppilas sanoo: \"Tämä ei ole oikea kolmio, koska se on vinossa.\" "
                      "Miten asiaa kannattaa perustella?")
            ok = (f"Kolmio on kolmio, kun kolme suoraa sivua sulkee kuvion. Tässä ala on {half(a2)} ruutua, joten pisteet eivät ole samalla suoralla",
                  GOOD)
            wrongs = [("Oppilas on oikeassa: kolmion pitää olla symmetrinen ja pohjan vaakasuora", TID, BAD),
                      ("Oppilas on oikeassa, koska kolmioksi kutsutaan vain tasasivuista kuviota", TID, BAD),
                      ("Kuvio on kolmio vain, jos sitä kierretään niin, että yksi sivu on vaakasuora", TID, BAD)]
            level, params = "H", {"points": ps, "twice_area": a2}
            steps = [f"Kärjet {pts_text(ps)}", f"Ala {half(a2)} > 0", "Asento ei vaikuta kolmion käsitteeseen"]
            final = ok[0]
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S5.03"], ["T16"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
