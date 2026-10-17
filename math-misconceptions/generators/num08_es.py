#!/usr/bin/env python3
"""NUM-08 (successive percentage changes), type ES. Lines are numeric expressions: lines before the error line are
equivalent to line 1 and the error line breaks equivalence (both checked by verify.py). The injected error treats a rise
and a fall as cancelling, adds the percentages, or takes the second percentage of the original amount."""
import random
from fractions import Fraction

from gen_common import MINUS, base_item, cli

TEMPLATE = "num08_es"
TID, CODE = "NUM-08", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = ("Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Peräkkäiset prosenttimuutokset "
           "kerrotaan muutoskertoimilla; jälkimmäinen prosentti lasketaan jo muuttuneesta arvosta.")


def d(x):
    """Fraction as decimal text with a decimal comma."""
    return f"{float(x):g}".replace(".", ",")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1241)
    items, seen = [], set()
    for k in range(count):
        P = rng.choice([80, 200, 400, 500])
        p = rng.choice([10, 20, 25])
        pf = Fraction(p, 100)
        up, down = 1 + pf, 1 - pf
        level, err = "T", 3
        if k == 0:
            intro = f"Tuotteen hinta on {P} €. Hinta nousee {p} % ja laskee sen jälkeen {p} %. Oppilas laskee lopullisen hinnan rivi riviltä. "
            lines = [f"{P} · (1 + {d(pf)}) · (1 {MINUS} {d(pf)})", f"{P} · {d(up)} · {d(down)}", f"{P} · 1", f"{P}"]
            etype = "cancel_percentages"
            fix = (f"Muutoskertoimet ovat {d(up)} ja {d(down)}, ja niiden tulo on {d(up * down)}, ei 1. "
                   f"Oikea lopullinen hinta on {d(P * up * down)} €.")
        elif k == 1:
            intro = f"Tuotteen hinta on {P} €. Hinta laskee {p} % ja nousee sen jälkeen {p} %. Oppilas laskee lopullisen hinnan rivi riviltä. "
            amt = P * pf
            lines = [f"{P} · (1 {MINUS} {d(pf)}) · (1 + {d(pf)})", f"{P} · {d(down)} · {d(up)}",
                     f"{P} {MINUS} {d(amt)} + {d(amt)}", f"{P}"]
            etype = "cancel_percentages"
            fix = (f"Nousu lasketaan jo alentuneesta hinnasta {d(P * down)} €, joten nousun määrä ei ole {d(amt)} €. "
                   f"Oikea lopullinen hinta on {d(P * up * down)} €.")
        elif k == 2:
            Q = P * up
            amt = P * pf
            intro = (f"Tuotteen hinta on {P} €. Hinta nousee {p} % ja korotettua hintaa alennetaan sen jälkeen {p} %. "
                     "Oppilas laskee lopullisen hinnan rivi riviltä. ")
            lines = [f"{P} · {d(up)} · {d(down)}", f"{d(Q)} · {d(down)}", f"{d(Q)} {MINUS} {d(amt)}", f"{d(Q - amt)}"]
            etype = "wrong_base"
            fix = (f"Alennus lasketaan korotetusta hinnasta {d(Q)} €: {d(Q)} · {d(down)} = {d(Q * down)}. "
                   f"Alennus on siis {d(Q * pf)} €, ei {d(amt)} €.")
        elif k == 3:
            level = "H"
            a = rng.choice([10, 20, 30])
            af = Fraction(a, 100)
            intro = (f"Kaupungin asukasluku on {P * 100} ja se kasvaa kaksi vuotta peräkkäin {a} % vuodessa. "
                     "Oppilas laskee asukasluvun kahden vuoden jälkeen rivi riviltä. ")
            lines = [f"{P * 100} · (1 + {d(af)}) · (1 + {d(af)})", f"{P * 100} · {d(1 + af)} · {d(1 + af)}",
                     f"{P * 100} · {d(1 + 2 * af)}", f"{d(P * 100 * (1 + 2 * af))}"]
            etype = "add_percentages"
            fix = (f"Kahden {a} %:n kasvun yhteinen muutoskerroin on {d(1 + af)} · {d(1 + af)} = {d((1 + af) ** 2)}, "
                   f"ei {d(1 + 2 * af)}. Toinen kasvu lasketaan jo kasvaneesta luvusta.")
            p = a
        else:
            level = "H"
            a, b = rng.choice([(10, 20), (20, 30), (10, 40), (20, 25)])
            af, bf = Fraction(a, 100), Fraction(b, 100)
            intro = (f"Takin hinta on {P} €. Alennus on ensin {a} % ja kassalla vielä {b} % alennetusta hinnasta. "
                     "Oppilas laskee lopullisen hinnan rivi riviltä. ")
            lines = [f"{P} · (1 {MINUS} {d(af)}) · (1 {MINUS} {d(bf)})", f"{P} · {d(1 - af)} · {d(1 - bf)}",
                     f"{P} · (1 {MINUS} {d(af + bf)})", f"{d(P * (1 - af - bf))}"]
            etype = "add_percentages"
            fix = (f"Alennukset eivät summaudu: {d(1 - af)} · {d(1 - bf)} = {d((1 - af) * (1 - bf))}, "
                   f"ei {d(1 - af - bf)}. Oikea hinta on {d(P * (1 - af) * (1 - bf))} €.")
            p = [a, b]
        key = (k, P, str(p))
        assert key not in seen
        seen.add(key)
        params = {"P": P, "p": p, "form": k}
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        final = f"Virhe on rivillä {err}"
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, intro + ASK, payload,
                               [fix], final,
                               "Oikein: peräkkäiset prosenttimuutokset kerrotaan muutoskertoimilla, koska jälkimmäinen lasketaan muuttuneesta arvosta.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
