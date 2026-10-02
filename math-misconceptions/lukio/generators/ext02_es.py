#!/usr/bin/env python3
"""EXT-02 ES (lukio level): integer exponents. Each item shows a worked solution with one line where an
exponent rule is misapplied (a^0 = 0, a^-n read as a product or a negative number, exponents added in a
power of a power). Lines are checked by the verifier (lines before the error line equivalent, the error
line not)."""
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "ext02_es"
TID, CODE = "EXT-02", "ES"
GENERIC = "a⁰ = 1, a⁻ⁿ = 1/aⁿ ja (aᵐ)ⁿ = aᵐⁿ. Kokeile pienellä luvulla, esim. 2⁻¹ = 1/2."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, lines, err, etype, steps, final, params, fb="Oikein: negatiivinen eksponentti ja nollas potenssi noudattavat omia sääntöjään."):
        items.append(base_item(TID, CODE, n, lops, ["G2"], syll, level, "none", prompt,
                               {"lines": lines, "error_line": err, "error_type": etype}, steps, final, fb,
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    v = Fraction(5) ** 0 + Fraction(5) ** -1
    assert v == Fraction(6, 5)
    add(start, ["MAY1.04", "MAA5.05"], "MAA", "P",
        "Oppilas laski lausekkeen 5⁰ + 5⁻¹ arvon näin. Napauta rivi, jossa on virhe.",
        ["5^0 + 5^(−1)", "0 + 1/5", "1/5"], 2, "zero_power_as_zero",
        ["Rivillä 2 on kirjoitettu 5⁰ = 0, mutta mikä tahansa nollasta eroava luku potenssiin 0 on 1.", "Oikein: 1 + 1/5 = 6/5."],
        "6/5", {"expr": "5^0+5^-1"})
    v = Fraction(4) ** -2
    assert v == Fraction(1, 16)
    add(start + 1, ["MAY1.04", "MAA5.05"], "MAA", "T",
        "Oppilas laski potenssin 4⁻² arvon näin. Napauta rivi, jossa on virhe.",
        ["4^(−2)", "4 · (−2)", "−8"], 2, "negative_exponent_as_product",
        ["Rivillä 2 potenssi on laskettu kertolaskuna eksponentin kanssa, mutta 4⁻² ei ole 4 · (−2).", "Oikein: 4⁻² = 1/4² = 1/16."],
        "1/16", {"a": 4, "n": -2})
    add(start + 2, ["MAY1.04"], "MAB", "T",
        "Lääkeannos on 3 · 10⁻² grammaa. Oppilas muutti sen lausekkeen arvoksi näin. Napauta rivi, jossa on virhe.",
        ["3 · 10^(−2)", "3 · (−100)", "−300"], 2, "negative_exponent_as_negative",
        ["Rivillä 2 on kirjoitettu 10⁻² = −100, mutta negatiivinen eksponentti tarkoittaa käänteislukua: 10⁻² = 1/100.", "Oikein: 3 · 1/100 = 0,03 grammaa. Annos ei voi olla negatiivinen."],
        "0,03", {"c": 3, "n": -2}, "Oikein: 10⁻² = 0,01, joten annos on 0,03 g.")
    v = Fraction(2) ** 2
    add(start + 3, ["MAY1.04", "MAA5.05"], "MAA", "H",
        "Oppilas sieventi lausekkeen (2⁻¹)⁻² näin. Napauta rivi, jossa on virhe.",
        ["(2^(−1))^(−2)", "2^(−1 − 2)", "2^(−3)", "1/8"], 2, "power_of_power_added",
        ["Rivillä 2 potenssin potenssissa eksponentit on laskettu yhteen, vaikka ne kerrotaan: (aᵐ)ⁿ = aᵐⁿ.", "Oikein: 2^((−1) · (−2)) = 2² = 4."],
        str(v), {"expr": "(2^-1)^-2"}, "Oikein: eksponentit kerrotaan keskenään, joten tulos on 4.")
    v = Fraction(500) * Fraction(2) ** -2
    assert v == 125
    add(start + 4, ["MAY1.04"], "MAB", "H",
        "Bakteerien määrä on N(t) = 500 · 2^t, missä t on aika tunteina. Oppilas laski määrän kaksi tuntia ennen hetkeä t = 0 näin. Napauta rivi, jossa on virhe. Vihje: voiko bakteerien määrä olla negatiivinen?",
        ["500 · 2^(−2)", "500 · (−4)", "−2000"], 2, "negative_exponent_as_negative",
        ["Rivillä 2 on kirjoitettu 2⁻² = −4. Määrä ei voi olla negatiivinen, ja 2⁻² = 1/4.", "Oikein: 500 · 1/4 = 125."],
        "125", {"n0": 500, "t": -2}, "Oikein: 500 · 2⁻² = 125 bakteeria.")
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
