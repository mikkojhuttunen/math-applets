#!/usr/bin/env python3
"""ALG-07 (sign errors and one-sided operations), type MC select-all (a reverse problem).
The pupil ticks every equation whose solution is the given value. Correct equations balance at that value
(also with the sides swapped); wrong ones come from the same numbers. The tagged ones are what a pupil who
solves with a sign slip (moving +b across as +b) or a one-sided operation (subtracting b on one side only)
would accept as having that solution."""
import random

from gen_common import MINUS, base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "alg07_mcs"
TID, CODE = "ALG-07", "MC"


def make_items(run, date, count=5, start=1):
    rng = random.Random(8204)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b, x = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 9)
            if (a, b, x) not in seen:
                break
        seen.add((a, b, x))
        level, e = "T", 0
        if k == 0:
            c = a * x + b
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{a}x + {b} = {c}", f"{c} = {a}x + {b}"]
            invalid = [(f"{a}x + {b} = {c + 2 * b}", None), (f"{a}x + {b} = {a * x}", TID), (f"{a}x + {b} = {c - 2 * b}", TID)]
            steps = [f"Sijoitetaan x = {x}: {a} · {x} + {b} = {c}", f"{a}x + {b} = {c}"]
        elif k == 1:
            c = a * x - b
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{a}x {MINUS} {b} = {c}", f"{c} = {a}x {MINUS} {b}"]
            invalid = [(f"{a}x {MINUS} {b} = {c + 2 * b}", TID), (f"{a}x {MINUS} {b} = {a * x}", TID), (f"{a}x {MINUS} {b} = {c - 2 * b}", None)]
            steps = [f"Sijoitetaan x = {x}: {a} · {x} {MINUS} {b} = {c}", f"{a}x {MINUS} {b} = {c}"]
        elif k == 2:
            c = b + a * x
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{b} + {a}x = {c}", f"{c} = {b} + {a}x"]
            invalid = [(f"{b} + {a}x = {c + 2 * b}", None), (f"{b} + {a}x = {a * x}", TID), (f"{b} + {a}x = {c - 2 * b}", TID)]
            steps = [f"Sijoitetaan x = {x}: {b} + {a} · {x} = {c}", f"{b} + {a}x = {c}"]
        elif k == 3:
            level = "H"
            a = max(a, 5)
            e = rng.randint(2, a - 2)
            d = b + (a - e) * x
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}."
            valid = [f"{a}x + {b} = {e}x + {d}", f"{e}x + {d} = {a}x + {b}"]
            invalid = [(f"{a}x + {b} = {e}x + {d + 2 * b}", None), (f"{a}x + {b} = {e}x + {d - 2 * b}", TID),
                       (f"{a}x + {b} = {e}x + {d + b}", None)]
            c = d
            steps = [f"Molemmat puolet saavat saman arvon, kun x = {x}: {a} · {x} + {b} = {a * x + b}",
                     f"Oikea puoli: {e} · {x} + {d} = {e * x + d}, joten {a}x + {b} = {e}x + {d} kelpaa"]
        else:
            level = "H"
            c = b + a * x
            prompt = (f"Taksin lähtömaksu on {b} euroa ja kilometrihinta {a} euroa. Matkan hinta oli {c} euroa. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu x = {x} on ajettujen kilometrien määrä.")
            valid = [f"{b} + {a}x = {c}", f"{a}x + {b} = {c}", f"{a}x = {c} {MINUS} {b}"]
            invalid = [(f"{a}x {MINUS} {b} = {c}", TID), (f"{a}x = {c} + {b}", TID), (f"{a}x + {b} = {a * x}", TID)]
            steps = [f"Hinta = lähtömaksu + kilometrit · {a}", f"{b} + {a}x = {c}"]
            e = 0
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", x, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps, "; ".join(pretty(e) for e in valid),
                               "Kun x:n paikalle sijoitetaan pyydetty luku, yhtälön molemmat puolet ovat yhtä suuret.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "e": e, "x": x}, date, run,
                               generic_wrong="Sijoita x:n paikalle pyydetty luku ja laske molemmat puolet: ovatko ne yhtä suuret?"))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
