#!/usr/bin/env python3
"""NUM-07 (wrong base in reverse percentage), type NE. Answers come from Decimal arithmetic; the typical wrong
answer applies the percentage to the new (given) amount."""
import random
from decimal import Decimal

from gen_common import base_item, cli
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)


TEMPLATE = "num07_ne"
TID, CODE = "NUM-07", "NE"
BAD = ("Prosentti on laskettava alkuperäisestä määrästä, ei annetusta uudesta määrästä. "
       "Alkuperäinen määrä on 100 %, ja uusi määrä on 100 % ± muutos.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(808)
    items, seen = [], set()
    for k in range(count):
        while True:
            orig = Decimal(rng.choice([40, 60, 80, 120, 160, 200, 240, 500]))
            p = Decimal(rng.choice([10, 20, 25])) if k in (1, 4) else Decimal(rng.choice([10, 20, 25, 50]))
            if k == 3:
                orig = Decimal(rng.choice([500, 600, 800]))
                p = Decimal(rng.choice([8, 10, 12, 20]))
            if (orig, p) not in seen:
                break
        seen.add((orig, p))
        up, down = orig * (1 + p / 100), orig * (1 - p / 100)
        if k == 0:
            new = up
            ans, wrong = orig, [new * (1 - p / 100)]
            prompt = f"Polkupyörän hinta nousi {fmt(p)} % ja on nyt {fmt(new)} €. Mikä hinta oli ennen nousua? Kirjoita hinta euroina."
            steps = [f"{fmt(new)} € on {fmt(100 + p)} % vanhasta hinnasta", f"{fmt(new)} ÷ {fmt(1 + p / 100)} = {fmt(orig)}"]
            level = "T"
        elif k == 1:
            new = down
            ans, wrong = orig, [new * (1 + p / 100)]
            prompt = f"Kengät maksavat alennuksen {fmt(p)} % jälkeen {fmt(new)} €. Mikä oli hinta ennen alennusta? Kirjoita hinta euroina."
            steps = [f"{fmt(new)} € on {fmt(100 - p)} % vanhasta hinnasta", f"{fmt(new)} ÷ {fmt(1 - p / 100)} = {fmt(orig)}"]
            level = "T"
        elif k == 2:
            new = down
            ans, wrong = orig - new, [new * p / 100]
            prompt = f"Reppu maksaa {fmt(p)} %:n alennuksen jälkeen {fmt(new)} €. Montako euroa alennus oli?"
            steps = [f"{fmt(new)} ÷ {fmt(1 - p / 100)} = {fmt(orig)}", f"{fmt(orig)} {chr(8722)} {fmt(new)} = {fmt(orig - new)}"]
            level = "T"
        elif k == 3:
            new = up
            ans, wrong = new - orig, [new * p / 100]
            prompt = f"Vuokra nousi {fmt(p)} % ja on nyt {fmt(new)} €/kk. Kuinka monta euroa vuokra nousi kuukaudessa?"
            steps = [f"{fmt(new)} ÷ {fmt(1 + p / 100)} = {fmt(orig)}", f"{fmt(new)} {chr(8722)} {fmt(orig)} = {fmt(new - orig)}"]
            level = "H"
        else:
            new = down
            prompt = (f"Jäätelön hinta aleni {fmt(p)} %. Nyt se maksaa {fmt(new / 20)} €. "
                      f"Mikä oli hinta ennen alennusta euroina?")
            ans, wrong = orig / 20, [new / 20 * (1 + p / 100)]
            steps = [f"{fmt(new / 20)} € on {fmt(100 - p)} % vanhasta hinnasta", f"{fmt(new / 20)} ÷ {fmt(1 - p / 100)} = {fmt(ans)}"]
            level = "H"
        assert all(w != ans for w in wrong)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, prompt, payload, steps, fmt(ans),
                               "Oikein: perusarvona on alkuperäinen määrä, ja uusi määrä on 100 % ± muutos.", TEMPLATE,
                               {"orig": fmt(orig), "percent": fmt(p), "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
