#!/usr/bin/env python3
"""LEQU-02 ES (lukio level): zero-product rule used when the product is not zero. The error line sets
a factor equal to the non-zero value; the verifier checks it is not equivalent to the line before."""
from gen_common import base_item, cli

TEMPLATE = "lequ02_es"
TID, CODE = "LEQU-02", "ES"
GENERIC = "Tulon nollasääntö toimii vain, kun tulo on 0. Siirrä ensin kaikki vasemmalle ja tekijöi."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, g, level, prompt, lines, err, steps, final, params):
        items.append(base_item(TID, CODE, n, ["MAA2.05"], [g], "MAA", level, "none", prompt,
                               {"lines": lines, "error_line": err, "error_type": "zero_product_nonzero"}, steps, final,
                               "Oikein: tulon nollasääntö ei päde, kun tulo on muu kuin 0.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    add(start, "G4", "T", "Oppilas ratkaisi yhtälön (x − 4)(x + 1) = 6 näin. Napauta rivi, jossa on virhe.",
        ["(x − 4)(x + 1) = 6", "x − 4 = 6", "x = 10"], 2,
        ["Rivillä 2 on käytetty nollasääntöä, vaikka tulo on 6. Tulo 6 saadaan monella tavalla.", "Oikein: x² − 3x − 4 = 6, x² − 3x − 10 = 0, (x − 5)(x + 2) = 0, x = 5 tai x = −2."],
        "x = 5 tai x = −2", {"a": -4, "b": 1, "k": 6})
    add(start + 1, "G4", "T", "Oppilas ratkaisi yhtälön x(x + 3) = 10 näin. Napauta rivi, jossa on virhe.",
        ["x(x + 3) = 10", "x + 3 = 10", "x = 7"], 2,
        ["Rivillä 2 on jätetty tekijä x pois, vaikka tulo on 10.", "Oikein: x² + 3x − 10 = 0, (x + 5)(x − 2) = 0, x = −5 tai x = 2."],
        "x = −5 tai x = 2", {"a": 3, "k": 10})
    add(start + 2, "G4", "H", "Oppilas ratkaisi yhtälön x² − 4x = 12 näin. Napauta rivi, jossa on virhe.",
        ["x² − 4x = 12", "x(x − 4) = 12", "x − 4 = 12"], 3,
        ["Rivi 2 on oikein, mutta rivillä 3 nollasääntöä on käytetty, vaikka tulo on 12.", "Oikein: x² − 4x − 12 = 0, (x − 6)(x + 2) = 0, x = 6 tai x = −2."],
        "x = 6 tai x = −2", {"b": -4, "k": 12})
    add(start + 3, "G4", "H", "Oppilas ratkaisi yhtälön (x + 2)(x + 3) = 12 näin. Napauta rivi, jossa on virhe. Vihje: sijoita x = 10 alkuperäiseen yhtälöön.",
        ["(x + 2)(x + 3) = 12", "x + 2 = 12", "x = 10"], 2,
        ["Rivillä 2 nollasääntöä on käytetty, vaikka tulo on 12.", "Tarkistus: (10 + 2)(10 + 3) = 156 ≠ 12.", "Oikein: x² + 5x − 6 = 0, (x + 6)(x − 1) = 0, x = −6 tai x = 1."],
        "x = −6 tai x = 1", {"a": 2, "b": 3, "k": 12},)
    add(start + 4, "G4", "H", "Oppilas ratkaisi yhtälön x(x − 1)(x − 2) = 6 näin. Napauta rivi, jossa on virhe.",
        ["x(x − 1)(x − 2) = 6", "x − 1 = 6", "x = 7"], 2,
        ["Rivillä 2 nollasääntöä on käytetty kolmen tekijän tuloon, joka on 6, ei 0.", "Tarkistus: 7 · 6 · 5 = 210 ≠ 6.", "Oikein: yhtälön ratkaisu on x = 3, sillä 3 · 2 · 1 = 6."],
        "x = 3", {"k": 6})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
