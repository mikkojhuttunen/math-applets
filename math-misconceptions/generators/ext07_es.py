#!/usr/bin/env python3
"""EXT-07 (area unit conversion: 1 m² = 100 cm²), type ES (error spotting). Lines are numeric expressions; lines
before the error line are equivalent to line 1 and the error line uses the length factor (100 or 1 000) instead of
its square, which breaks equivalence."""
import random

from gen_common import base_item, cli

TEMPLATE = "ext07_es"
TID, CODE = "EXT-07", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = "Pinta-alan muuntokerroin on pituuden kertoimen neliö: 1 m² = 100 cm · 100 cm = 10 000 cm². Tarkista rivi kerrallaan."
GOOD = "Oikein: pinta-alayksiköiden muuntokerroin on pituusyksikön kertoimen neliö."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1808)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n = rng.choice([2, 3, 4, 6, 7])
            intro = f"Oppilas muuntaa {n} m² neliösenttimetreiksi. Rivit ovat lukuja ilman yksikköä."
            lines = [f"{n} · 100 · 100", f"{n} · 100", f"{n * 100}"]
            err, level, params = 2, "T", {"n": n}
            fix = f"1 m² = 100 · 100 cm² = 10 000 cm². Oikea rivi 2 on {n} · 10 000 = {n * 10000}."
        elif k == 1:
            n = rng.choice([2, 3, 5, 8])
            intro = f"Oppilas muuntaa {n * 10000} cm² neliömetreiksi. Rivit ovat lukuja ilman yksikköä."
            lines = [f"{n * 10000} / (100 · 100)", f"{n * 10000} / 10000", f"{n * 10000} / 100"]
            err, level, params = 3, "T", {"n": n}
            fix = f"10 000 cm² = 1 m², joten jaetaan luvulla 10 000. Oikea tulos on {n}."
        elif k == 2:
            n = rng.choice([2, 3, 5])
            intro = f"Oppilas muuntaa {n} km² neliömetreiksi. Rivit ovat lukuja ilman yksikköä."
            lines = [f"{n} · 1000 · 1000", f"{n} · 1000000", f"{n} · 1000"]
            err, level, params = 3, "T", {"n": n}
            fix = f"1 km² = 1 000 · 1 000 m² = 1 000 000 m². Oikea tulos on {n * 1000000}."
        elif k == 3:
            w, l, t = rng.choice([(4, 5, 20), (3, 5, 25), (4, 6, 30)])
            intro = (f"Lattian mitat ovat {w} m ja {l} m ja laatan sivu on {t} cm. Oppilas laskee, montako laattaa "
                     f"tarvitaan. Rivit ovat lukuja ilman yksikköä.")
            lines = [f"{w * l} · 10000 / ({t} · {t})", f"{w * l * 10000} / {t * t}", f"{w * l * 100} / {t * t}"]
            err, level, params = 3, "H", {"w": w, "l": l, "t": t}
            fix = f"Lattia on {w * l} m² = {w * l * 10000} cm², ei {w * l * 100} cm². Oikea tulos on {w * l * 10000 // (t * t)}."
        else:
            n, c = rng.choice([(3, 4000), (2, 5000), (5, 8000)])
            intro = (f"Huoneen lattia on {n} m² ja matto peittää {c} cm². Oppilas laskee, montako neliösenttimetriä "
                     f"jää peittämättä. Rivit ovat lukuja ilman yksikköä.")
            lines = [f"{n} · 10000 − {c}", f"{n * 10000} − {c}", f"{n * 100} − {c}"]
            err, level, params = 3, "H", {"n": n, "c": c}
            fix = f"{n} m² = {n * 10000} cm², ei {n * 100} cm². Oikea tulos on {n * 10000 - c}."
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"lines": lines, "error_line": err, "error_type": "length_factor_for_area"}
        items.append(base_item(TID, CODE, start + k, ["S5.14"], ["T18"], 7, level, f"{intro} {ASK}", payload,
                               [fix], f"Virhe on rivillä {err}", GOOD, TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
