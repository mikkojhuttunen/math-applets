#!/usr/bin/env python3
"""EXT-08 (mean taken as the "typical value"; median read from unsorted data), type SO (step ordering). The task is the
difference mean - median of an unsorted list; every line has the same value as line 1 and the lines are listed in the
correct order. The median is stated in the prompt so the ordering focuses on keeping mean and median apart."""
import random

from ext08_common import dec, mean, median, pick_list, txt
from gen_common import MINUS, base_item, cli

TEMPLATE = "ext08_so"
TID, CODE = "EXT-08", "SO"
ASK = "Järjestä rivit oikeaan järjestykseen niin, että keskiarvon ja mediaanin erotus ratkeaa vaihe vaiheelta."
GOOD = "Oikein: keskiarvo ja mediaani ovat eri asioita; keskiarvo lasketaan kaikista arvoista, mediaani on järjestetyn listan keskimmäinen."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1812)
    items = []
    for k in range(count):
        n = (5, 5, 7, 6, 6)[k]
        while True:
            vals = pick_list(rng, n, 1, 40, want_mean=True)
            med, mn = median(vals), mean(vals)
            if mn > med and mn.denominator in (1, 2, 4, 5, 10) and (mn - med).denominator in (1, 2, 4, 5, 10):
                break
        total = sum(vals)
        terms = " + ".join(str(v) for v in vals)
        diff = mn - med
        lines = [f"({terms}) / {n} {MINUS} {dec(med)}", f"{total} / {n} {MINUS} {dec(med)}",
                 f"{dec(mn)} {MINUS} {dec(med)}", f"{dec(diff)}"]
        ctx = [
            f"Koepisteet ovat {txt(vals)}. Mediaani on {dec(med)}. ",
            f"Lukemat kirjat ovat {txt(vals)}. Mediaani on {dec(med)}. ",
            f"Päivälämpötilat ovat {txt(vals)} astetta. Mediaani on {dec(med)}. ",
            f"Lenkkien pituudet ovat {txt(vals)} minuuttia. Mediaani on {dec(med)}. ",
            f"Viikon myynnit ovat {txt(vals)} kappaletta. Mediaani on {dec(med)}. ",
        ][k]
        level = "T" if k < 3 else "H"
        steps = [f"Keskiarvo on summa jaettuna lukujen määrällä: {total} / {n} = {dec(mn)}",
                 f"Mediaani on {dec(med)}, joten erotus on {dec(mn)} {MINUS} {dec(med)} = {dec(diff)}"]
        items.append(base_item(TID, CODE, start + k, ["S6.02", "S6.03"], ["T19"], 7, level, ctx + ASK,
                               {"lines": lines, "accept": "exact"}, steps,
                               f"{dec(mn)} {MINUS} {dec(med)} = {dec(diff)}", GOOD, TEMPLATE,
                               {"values": vals, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
