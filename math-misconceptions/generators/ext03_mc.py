#!/usr/bin/env python3
"""EXT-03 (inequality sign not reversed when multiplying or dividing by a negative number), type MC. The solution
of each inequality is computed with integers and checked by brute force over an integer window; the tagged
distractor keeps the inequality sign unchanged."""
import random

from gen_common import base_item, cli, lin, mc_options, num

TEMPLATE = "ext03_mc"
TID, CODE = "EXT-03", "MC"
FLIP = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
HOLDS = {">": lambda u, v: u > v, "<": lambda u, v: u < v, "≥": lambda u, v: u >= v, "≤": lambda u, v: u <= v}
BAD = ("Kun epäyhtälö kerrotaan tai jaetaan negatiivisella luvulla, epäyhtälömerkin suunta kääntyy. "
       "Tarkista sijoittamalla: väitetyn ratkaisun luku ei toteuta alkuperäistä epäyhtälöä.")
GOOD = "Oikein: negatiivisella luvulla kerrottaessa tai jaettaessa epäyhtälömerkin suunta kääntyy."


def ineq(p, q, rel, rhs, var="x"):
    return f"{lin(p, q).replace('x', var)} {rel} {num(rhs)}"


def solve(p, q, rel, rhs):
    """p x + q rel rhs with p < 0, (rhs - q) divisible by p: (flipped rel, boundary), brute-force checked."""
    assert p < 0 and (rhs - q) % p == 0
    srel, r = FLIP[rel], (rhs - q) // p
    for x in range(-40, 41):
        orig = HOLDS[rel](p * x + q, rhs)
        assert orig == HOLDS[srel](x, r)
        if x != r:
            assert orig != HOLDS[rel](x, r)  # keeping the sign gives a different set
    return srel, r


def make_items(run, date, count=5, start=1):
    rng = random.Random(1301)
    items, seen = [], set()
    for k in range(count):
        var, justify = "x", False
        if k == 0:
            a, r = rng.choice([(2, -3), (3, -4), (5, -2)])
            p, q, rel, rhs, level = -a, 0, ">", -a * r, "T"
            prompt = f"Ratkaise epäyhtälö {ineq(p, q, rel, rhs)}."
            params = {"a": a, "rhs": rhs}
        elif k == 1:
            a, r = rng.choice([(2, 4), (4, 3), (3, 5)])
            p, q, rel, rhs, level = -a, 0, "≤", -a * r, "T"
            prompt = f"Ratkaise epäyhtälö {ineq(p, q, rel, rhs)}."
            params = {"a": a, "rhs": rhs}
        elif k == 2:
            t0, a, lim = rng.choice([(5, 3, -4), (8, 2, -2), (10, 5, -5)])
            p, q, rel, rhs, level, var = -a, t0, "<", lim, "T", "t"
            prompt = (f"Lämpötila on aluksi {t0} °C ja laskee {a} astetta tunnissa, joten t tunnin kuluttua se on "
                      f"{lin(p, q).replace('x', 't')} °C. Millä t:n arvoilla lämpötila on alle {num(lim)} °C?")
            params = {"t0": t0, "a": a, "lim": lim}
        elif k == 3:
            c, a, rhs = rng.choice([(5, 2, -1), (7, 3, 1), (1, 4, -7)])
            p, q, rel, level = -a, c, ">", "H"
            prompt = f"Ratkaise epäyhtälö {ineq(p, q, rel, rhs)}."
            params = {"c": c, "a": a, "rhs": rhs}
        else:
            a, r = rng.choice([(2, -3), (4, 2), (3, -5)])
            p, q, rel, rhs, level, justify = -a, 0, ">", -a * r, "H", True
            params = {"a": a, "rhs": rhs, "justify": True}
        srel, rr = solve(p, q, rel, rhs)
        sol_text = f"{var} {srel} {num(rr)}"
        wrong_text = f"{var} {rel} {num(rr)}"
        if justify:
            xt = rr + 1
            prompt = (f"Oppilas väittää, että epäyhtälön {ineq(p, q, rel, rhs)} ratkaisu on {wrong_text}. "
                      "Mikä perustelu osoittaa, että väite on väärä?")
            correct = (f"Luku x = {num(xt)} toteuttaa väitteen, mutta {num(p * xt)} ei ole {rel} {num(rhs)}; "
                       f"negatiivisella luvulla jaettaessa merkki kääntyy, ja oikea ratkaisu on {sol_text}",
                       "Oikein: sijoittamalla huomaa, että merkin suunta täytyy kääntää.")
            wrongs = [("Väite on oikein, koska jakaminen ei muuta epäyhtälömerkin suuntaa", TID, BAD),
                      (f"Väite on väärä, koska raja-arvo on {num(-rr)} eikä {num(rr)}", None,
                       f"Raja-arvo {num(rr)} on oikein. Virhe on merkin suunnassa."),
                      ("Väite on väärä, koska epäyhtälöä ei saa jakaa negatiivisella luvulla", None,
                       "Negatiivisella luvulla saa jakaa, mutta merkin suunta kääntyy.")]
            steps = [f"Kokeillaan x = {num(xt)}: {num(p)} · ({num(xt)}) = {num(p * xt)}",
                     f"{num(p * xt)} ei ole {rel} {num(rhs)}", f"Oikea ratkaisu: {sol_text}"]
        else:
            correct = (sol_text, GOOD)
            wrongs = [(wrong_text, TID, BAD),
                      (f"{var} {srel} {num(-rr)}", None, f"Tarkista raja-arvo: se on {num(rr)}."),
                      (f"{var} {rel} {num(-rr)}", None, f"Tarkista raja-arvo: se on {num(rr)}.")]
            steps = ([f"{lin(p, 0).replace('x', var)} {rel} {num(rhs - q)}"] if q else []) + \
                    [f"Jaetaan luvulla {num(p)}, ja merkki kääntyy: {sol_text}"]
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S3.07"], ["T14"], 9, level, prompt,
                               {"options": options, "correct": [cid]}, steps, sol_text, GOOD, TEMPLATE, params,
                               date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
