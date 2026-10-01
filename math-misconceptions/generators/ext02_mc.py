#!/usr/bin/env python3
"""EXT-02 (integer exponents: 2³ = 6, a⁰ = 0, 2⁻¹ = -2), type MC. Values are computed with Python integers and
Fractions; the tagged distractors are the power read as a product, a⁰ read as 0 and a negative exponent read as a
negative number."""
import random
from fractions import Fraction

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "ext02_mc"
TID, CODE = "EXT-02", "MC"
SUP = {1: "¹", 2: "²", 3: "³", 4: "⁴"}


def sup(n):
    """Exponent as plain Unicode superscript text."""
    return num(n).replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("0", "⁰") \
        if n >= 0 else "⁻" + sup(-n)


def frac(a, n):
    """a^-n as a fraction text 1/a^n."""
    return f"1/{a ** n}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1203)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a, n = rng.choice([(2, 3), (3, 3), (4, 3), (5, 3), (2, 4)])
            prompt = f"Mikä on potenssin {a}{sup(n)} arvo?"
            bad = ("Potenssi on toistettu kertolasku: " f"{a}{sup(n)} = " + " · ".join([str(a)] * n) + f" = {a ** n}. "
                   f"Kantalukua ei kerrota eksponentilla.")
            correct = (str(a ** n), f"Oikein: {a}{sup(n)} = " + " · ".join([str(a)] * n) + f" = {a ** n}.")
            wrongs = [(str(a * n), "EXT-02", bad), (str(a + n), None, f"Tämä on {a} + {n}. Potenssi on tulo, ei summa."),
                      (str(a ** (n + 1)), None, f"Tämä on {a}{sup(n + 1)}: kertoja on yksi liikaa. Potenssissa {a}{sup(n)} kerrotaan {n} kertaa luvulla {a}.")]
            steps = [" · ".join([str(a)] * n) + f" = {a ** n}"]
            final, params, level = str(a ** n), {"a": a, "n": n}, "T"
        elif k == 1:
            a = rng.choice([3, 5, 7, 9])
            prompt = f"Mikä on potenssin {a}⁰ arvo?"
            bad = (f"Nollas potenssi ei ole nolla. Kun eksponentti pienenee yhdellä, tulo jaetaan luvulla {a}: "
                   f"{a}¹ = {a}, {a}⁰ = {a} ÷ {a} = 1.")
            correct = ("1", f"Oikein: jokaisen nollasta eroavan luvun nollas potenssi on 1, joten {a}⁰ = 1.")
            wrongs = [("0", "EXT-02", bad), (str(a), None, f"Tämä on {a}¹. Eksponentti 0 ei jätä kantalukua sellaisenaan."),
                      (num(-1), None, "Nollas potenssi ei ole negatiivinen: a⁰ = 1.")]
            steps = [f"{a}¹ = {a}", f"{a}⁰ = {a} ÷ {a} = 1"]
            final, params, level = "1", {"a": a}, "T"
        elif k == 2:
            a, n = rng.choice([(2, 2), (2, 3), (3, 2), (5, 2), (3, 3)])
            prompt = f"Mikä on potenssin {a}⁻{SUP[n]} arvo?"
            bad = (f"Negatiivinen eksponentti ei tee tuloksesta negatiivista. Se tarkoittaa käänteislukua: "
                   f"{a}⁻{SUP[n]} = 1/{a}{SUP[n]} = {frac(a, n)}.")
            correct = (frac(a, n), f"Oikein: {a}⁻{SUP[n]} = 1/{a}{SUP[n]} = {frac(a, n)}.")
            wrongs = [(num(-a ** n), "EXT-02", bad), (num(-a * n), None, f"Tämä on −{a} · {n}. Potenssi ei ole tulo."),
                      (str(a ** n), None, f"Tämä on {a}{SUP[n]}: negatiivinen eksponentti kääntää luvun käänteisluvuksi.")]
            steps = [f"{a}⁻{SUP[n]} = 1/{a}{SUP[n]}", f"= {frac(a, n)}"]
            final, params, level = frac(a, n), {"a": a, "n": n}, "T"
        elif k == 3:
            a = rng.choice([3, 4, 5, 6])
            prompt = "Mikä seuraavista väitteistä on oikein?"
            correct = (f"{a}⁰ = 1 ja {a}⁻² = 1/{a * a}", "Oikein: nollas potenssi on 1 ja negatiivinen eksponentti tarkoittaa käänteislukua.")
            wrongs = [(f"{a}⁰ = 0 ja {a}⁻² = {num(-2 * a)}", "EXT-02",
                       f"Nollas potenssi on 1, ei 0. Lisäksi {a}⁻² = 1/{a}² = 1/{a * a}, eikä se ole negatiivinen."),
                      (f"{a}⁰ = 1 ja {a}⁻² = {num(-a * a)}", "EXT-02", f"Negatiivinen eksponentti ei tee luvusta negatiivista: {a}⁻² = 1/{a * a}."),
                      (f"{a}⁰ = 0 ja {a}⁻² = 1/{a * a}", "EXT-02", f"Nollas potenssi on 1, ei 0: {a}⁰ = {a} ÷ {a} = 1.")]
            steps = [f"{a}⁰ = {a} ÷ {a} = 1", f"{a}⁻² = 1/{a}² = 1/{a * a}"]
            final, params, level = f"{a}⁰ = 1 ja {a}⁻² = 1/{a * a}", {"a": a}, "H"
        else:
            a = rng.choice([2, 5, 10])
            prompt = f"Mikä perustelu on oikea sille, että {a}⁰ = 1?"
            correct = (f"Kun eksponentti pienenee yhdellä, tulo jaetaan luvulla {a}: {a}² = {a * a}, {a}¹ = {a}, {a}⁰ = {a} ÷ {a} = 1",
                       "Oikein: potenssit muodostavat jonon, jossa jokaisella askeleella jaetaan kantaluvulla.")
            wrongs = [(f"Nollas potenssi tarkoittaa, että lukua {a} ei kerrota kertaakaan, joten tulos on 0", "EXT-02",
                       "Kertojia ei ole, mutta tyhjä tulo on 1, ei 0. Jonosta nähdään: a¹ ÷ a = a⁰ = 1."),
                      (f"Se on sopimus, joka ei liity muihin potensseihin: {a}⁰ voisi olla mikä tahansa luku", None,
                       "Arvo 1 seuraa potenssien laskusäännöistä: a¹ ÷ a = a⁰ = 1."),
                      (f"Koska {a} ÷ {a} = 0", None, f"{a} ÷ {a} = 1, ei 0: luku jaettuna itsellään on 1.")]
            steps = [f"{a}² = {a * a}", f"{a}¹ = {a}", f"{a}⁰ = {a} ÷ {a} = 1"]
            final, params, level = f"Jonossa jaetaan kantaluvulla: {a}⁰ = {a} ÷ {a} = 1", {"a": a, "justify": True}, "H"
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.11"], ["T10", "T11"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: potenssi on toistettu kertolasku, a⁰ = 1 ja negatiivinen eksponentti tarkoittaa käänteislukua.",
                               TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
