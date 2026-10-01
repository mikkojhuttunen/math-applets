#!/usr/bin/env python3
"""EXT-08 (mean taken as the "typical value"; median read from unsorted data), type NE. Medians and means are
computed with exact fractions after sorting; the tagged wrong answers are the middle of the list as written and,
where it differs, the mean."""
import random

from ext08_common import dec, mean, median, pick_list, txt, written_middle
from gen_common import base_item, cli

TEMPLATE = "ext08_ne"
TID, CODE = "EXT-08", "NE"
BAD = ("Mediaani ei ole listan keskimmäinen luku sellaisenaan. Järjestä luvut ensin pienimmästä suurimpaan ja "
       "valitse sitten keskimmäinen (parillisella määrällä kahden keskimmäisen keskiarvo).")
GOOD = "Oikein: luvut järjestetään ensin, ja mediaani on keskimmäinen arvo."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1801)
    items = []
    for k in range(count):
        if k == 0:
            vals = pick_list(rng, 5, 2, 20, want_mean=True)
            level = "T"
            prompt = f"Oppilaat saivat kokeesta pisteet {txt(vals)}. Mikä on pisteiden mediaani?"
            wrong = [written_middle(vals), mean(vals)]
        elif k == 1:
            vals = pick_list(rng, 7, 1, 30)
            level = "T"
            prompt = f"Seitsemän päivän lämpötilat olivat {txt(vals)} astetta. Mikä on lämpötilojen mediaani?"
            wrong = [written_middle(vals)]
        elif k == 2:
            vals = pick_list(rng, 6, 3, 40)
            level = "T"
            prompt = f"Kuuden kävelylenkin pituudet olivat {txt(vals)} minuuttia. Mikä on pituuksien mediaani?"
            wrong = [written_middle(vals)]
        elif k == 3:
            base = pick_list(rng, 5, 5, 25)
            new = rng.choice([v for v in range(26, 40) if v not in base])
            vals = base + [new]
            level = "H"
            assert median(vals) != written_middle(vals)
            prompt = (f"Viiden oppilaan lukemat kirjat ovat {txt(base)}. Kuudes oppilas on lukenut {new} kirjaa. "
                      f"Mikä on kaikkien kuuden oppilaan lukemien kirjojen mediaani?")
            wrong = [written_middle(vals)]
        else:
            n = 7
            while True:
                vals = pick_list(rng, n, 10, 30)
                big = max(vals) * 8
                data = [v for v in vals if v != max(vals)] + [big]
                rng.shuffle(data)
                if median(data) != written_middle(data) and median(data) == median(vals) \
                        and mean(data).denominator in (1, 2, 4, 5, 10) and mean(data) != median(data):
                    break
            level = "H"
            prompt = (f"Seitsemän työntekijän kuukausipalkat ovat {txt(data)} (luvut ovat satoja euroja). "
                      f"Mikä on mediaanipalkka sadoissa euroissa?")
            vals = data
            wrong = [written_middle(data), mean(data)]
        ans = median(vals)
        wrong = [w for w in dict.fromkeys(wrong) if w != ans]
        assert wrong
        srt = sorted(vals)
        steps = [f"Järjestys: {txt(srt)}"]
        steps.append(f"Keskimmäinen arvo on {dec(ans)}" if len(vals) % 2 else
                     f"Kaksi keskimmäistä ovat {srt[len(srt) // 2 - 1]} ja {srt[len(srt) // 2]}, niiden keskiarvo on {dec(ans)}")
        payload = {"answer": {"kind": "number", "value": float(ans), "tolerance": 0},
                   "wrong": [{"match": float(w), "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku" + (" desimaalipilkulla" if ans.denominator != 1 else "")}
        items.append(base_item(TID, CODE, start + k, ["S6.02", "S6.03"], ["T19"], 7, level, prompt, payload, steps,
                               dec(ans), GOOD, TEMPLATE, {"values": vals}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
