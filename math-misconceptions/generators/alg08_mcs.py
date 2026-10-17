#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type MC select-all (a reverse problem).
The pupil ticks every equation whose solution is the given value. Correct equations keep the bracket or expand
it fully (5(x + 6) = 75, 5x + 30 = 75); wrong ones come from the same numbers, and the tagged ones multiply only
the first term of the bracket (5x + 6 = 75)."""
import random

from gen_common import MINUS, base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "alg08_mcs"
TID, CODE = "ALG-08", "MC"


def make_items(run, date, count=5, start=1):
    rng = random.Random(8305)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b, x = rng.randint(2, 6), rng.randint(2, 7), rng.randint(2, 9)
            cc = rng.randint(2, 5)
            if (a, b, x) not in seen and x > b:
                break
        seen.add((a, b, x))
        level = "T"
        if k == 0:
            c = a * (x + b)
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{a}(x + {b}) = {c}", f"{a}x + {a * b} = {c}"]
            invalid = [(f"{a}(x + {b}) = {c + a * b - b}", None), (f"{a}x + {b} = {c}", TID), (f"{a}x + {b} = {a * x + a * b}", TID)]
            steps = [f"Sijoitetaan x = {x}: {a}({x} + {b}) = {c}", f"{a}(x + {b}) = {c}"]
        elif k == 1:
            c = a * (x - b)
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{a}(x {MINUS} {b}) = {c}", f"{a}x {MINUS} {a * b} = {c}"]
            invalid = [(f"{a}(x {MINUS} {b}) = {c + a * b - b}", TID), (f"{a}x {MINUS} {b} = {c}", TID),
                       (f"{a}x {MINUS} {b} = {a * x - a * b}", TID)]
            steps = [f"Sijoitetaan x = {x}: {a}({x} {MINUS} {b}) = {c}", f"{a}(x {MINUS} {b}) = {c}"]
        elif k == 2:
            c = a * (x + b) + cc * x
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{a}(x + {b}) + {cc}x = {c}", f"{a + cc}x + {a * b} = {c}"]
            invalid = [(f"{a}x + {b} + {cc}x = {c}", TID), (f"{a + cc}x + {b} = {c}", TID), (f"{a}(x + {b}) + {cc}x = {c + 3 * a}", None)]
            steps = [f"Sijoitetaan x = {x}: {a}({x} + {b}) + {cc} · {x} = {c}", f"{a}(x + {b}) + {cc}x = {c}"]
        elif k == 3:
            level = "H"
            m = rng.randint(2, 4)
            c = a * (m * x + b)
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{a}({m}x + {b}) = {c}", f"{a * m}x + {a * b} = {c}"]
            invalid = [(f"{a * m}x + {b} = {c}", TID), (f"{a}({m}x + {b}) = {c + a * b - b}", None),
                       (f"{a * m}x + {b} = {a * m * x + a * b}", TID)]
            cc = m
            steps = [f"Sijoitetaan x = {x}: {a}({m} · {x} + {b}) = {c}", f"{a}({m}x + {b}) = {c}"]
        else:
            level = "H"
            c = a * (x + b)
            prompt = (f"Siivooja veloittaa {a} euroa tunnilta. Työ kestää x + {b} tuntia, ja koko työn hinta on {c} euroa. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu x = {x} on tuntimäärä ilman {b} tunnin lisäosaa.")
            valid = [f"{a}(x + {b}) = {c}", f"{a}x + {a * b} = {c}"]
            invalid = [(f"{a}x + {b} = {c}", TID), (f"{a}(x + {b}) = {a * x}", None), (f"{a}x + {b} = {a * x + a * b}", TID)]
            steps = [f"Hinta = tuntihinta · tunnit = {a}(x + {b})", f"{a}(x + {b}) = {c}"]
        invalid = list(dict.fromkeys(invalid))
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", x, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, "; ".join(pretty(e) for e in valid),
                               "Kun x:n paikalle sijoitetaan pyydetty luku, yhtälön molemmat puolet ovat yhtä suuret.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": cc, "x": x}, date, run,
                               generic_wrong="Sijoita x:n paikalle pyydetty luku ja laske molemmat puolet: ovatko ne yhtä suuret? Muista, että kerroin kertoo koko sulun."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
