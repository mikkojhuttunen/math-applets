#!/usr/bin/env python3
"""FUN-05 (every linear function is proportional), type MC. Options are computed from the same a, b as the stem;
the tagged option assumes that doubling x doubles y."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "fun05_mc"
TID, CODE = "FUN-05", "MC"
BAD = ("Suora ei välttämättä ole suoraan verrannollisuus. Vain suora y = ax, joka kulkee origon kautta, kaksinkertaistaa "
       "y:n, kun x kaksinkertaistuu. Tarkista laskemalla arvot.")
GOOD = "Oikein: y = ax + b on suoraan verrannollinen vain, kun b = 0. Muuten x:n kaksinkertaistaminen ei kaksinkertaista y:tä."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1261)
    items = []
    for k in range(count):
        if k == 0:
            a, b = rng.choice([(2, 3), (3, 4), (4, 2)])
            y1, y2 = a + b, 2 * a + b
            prompt = f"Funktio on y = {a}x + {b}. Kun x kaksinkertaistuu arvosta 1 arvoon 2, kaksinkertaistuuko myös y?"
            correct = (f"Ei: y muuttuu arvosta {y1} arvoon {y2}, eikä {y2} ole {2 * y1}", GOOD)
            wrongs = [("Kyllä, koska kuvaaja on suora", TID, BAD),
                      ("Kyllä, koska x ja y kasvavat yhtä aikaa", TID, BAD),
                      (f"Ei: y pienenee arvosta {y1} arvoon {y2}", None, f"Arvo kasvaa, {y1} → {y2}.")]
            steps = [f"x = 1: y = {a} + {b} = {y1}", f"x = 2: y = {2 * a} + {b} = {y2}", f"2 · {y1} = {2 * y1} ≠ {y2}"]
            final, level, params = "Ei kaksinkertaistu", "T", {"a": a, "b": b, "form": k}
        elif k == 1:
            a, b = rng.choice([(2, 3), (3, 1), (5, 2)])
            ys = [a * x + b for x in (1, 2, 3)]
            ratio = f"{ys[1] / 2:g}".replace(".", ",")
            prompt = (f"Taulukossa x = 1, 2, 3 ja y = {ys[0]}, {ys[1]}, {ys[2]}. Taulukon arvot ovat suoralta. "
                      "Onko y suoraan verrannollinen x:ään?")
            correct = (f"Ei: suhde y/x ei ole vakio ({ys[0]}/1 = {ys[0]}, mutta {ys[1]}/2 = {ratio})", GOOD)
            wrongs = [("Kyllä, koska arvot ovat suoralta", TID, BAD),
                      ("Kyllä, koska y kasvaa kun x kasvaa", TID, BAD),
                      ("Ei, koska arvot eivät ole suoralta", None, "Arvot ovat suoralta: erotukset ovat yhtä suuret.")]
            steps = [f"y/x: {ys[0]}/1 = {ys[0]}, {ys[1]}/2 = {ratio}", "Suhde ei ole vakio"]
            final, level, params = "Ei ole", "T", {"a": a, "b": b, "form": k}
        elif k == 2:
            a, b = rng.choice([(2, 4), (3, 5), (4, 6)])
            n = rng.choice([3, 4, 5])
            price_n, price_2n = a * n + b, a * 2 * n + b
            prompt = (f"Taksimatkan hinta on {b} € + {a} € jokaiselta kilometriltä. {n} km:n matka maksaa {price_n} €. "
                      f"Mitä {2 * n} km:n matka maksaa?")
            correct = (f"{price_2n} €", GOOD)
            wrongs = [(f"{2 * price_n} €", TID, BAD), (f"{price_2n + a} €", None, f"Matka on {2 * n} km, ei {2 * n + 1} km."),
                      (f"{a * 2 * n} €", None, "Aloitusmaksu pitää myös lisätä.")]
            steps = [f"{b} + {a} · {2 * n} = {price_2n}", f"2 · {price_n} = {2 * price_n} ei kelpaa, koska aloitusmaksu on mukana vain kerran"]
            final, level, params = f"{price_2n} €", "T", {"a": a, "b": b, "n": n, "form": k}
        elif k == 3:
            a = rng.choice([3, 4, 5])
            b = rng.choice([1, 2])
            prompt = "Minkä funktion arvo kaksinkertaistuu aina, kun x kaksinkertaistuu?"
            correct = (f"y = {a}x", GOOD)
            wrongs = [(f"y = {a}x + {b}", TID, BAD), (f"y = x + {a}", TID, BAD), (f"y = {a} − x".replace("-", "−"), None, "y pienenee x:n kasvaessa.")]
            steps = [f"y = {a}x: y(2x) = {a} · 2x = 2 · {a}x", f"y = {a}x + {b}: y(2x) = {2 * a}x + {b} ≠ 2 · ({a}x + {b})"]
            final, level, params = f"y = {a}x", "H", {"a": a, "b": b, "form": k}
        else:
            a, b = rng.choice([(2, 3), (3, 2), (4, 1)])
            prompt = (f"Oppilas väittää: \"Funktio y = {a}x + {b} on suora, joten se on suoraan verrannollisuus.\" "
                      "Mikä on vastaesimerkki?")
            correct = (f"Kun x = 1, y = {a + b}; kun x = 2, y = {2 * a + b}. Arvo {2 * a + b} ei ole kaksinkertainen arvoon {a + b} verrattuna", GOOD)
            wrongs = [("Ei vastaesimerkkiä, väite on oikein", TID, BAD),
                      ("Kun x = 0, y = 0", None, f"Kun x = 0, y = {b}, eikä 0."),
                      (f"Kun x = 1, y = {a}", None, f"Kun x = 1, y = {a + b}.")]
            steps = [f"x = 1: y = {a + b}", f"x = 2: y = {2 * a + b}", f"2 · {a + b} = {2 * (a + b)} ≠ {2 * a + b}"]
            final, level, params = "Suora ei kulje origon kautta", "H", {"a": a, "b": b, "form": k}
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S4.03"], ["T14", "T15"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
