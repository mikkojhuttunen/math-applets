#!/usr/bin/env python3
"""PRB-01 (recency, gambler's fallacy), type MC. Probabilities are computed with Fraction."""
import random
from fractions import Fraction

from gen_common import base_item, cli, mc_options

TEMPLATE = "prb01_mc"
TID, CODE = "PRB-01", "MC"
BAD = ("Aiemmat tulokset eivät vaikuta seuraavaan: reilulla kolikolla tai nopalla ei ole muistia. "
       "Lyhyessä sarjassa mikään tulos ei ole \"vuorossa\".")


def fr(f):
    return f"{f.numerator}/{f.denominator}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(901)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n = rng.choice([4, 5, 6, 7])
            side, other = rng.choice([("kruuna", "klaava"), ("klaava", "kruuna")])
            p = Fraction(1, 2)
            prompt = (f"Reilua kolikkoa on heitetty {n} kertaa, ja joka kerta on tullut {side}. "
                      f"Mikä on todennäköisyys, että seuraavalla heitolla tulee {other}?")
            correct = (fr(p), f"Oikein: jokaisella heitolla todennäköisyys on {fr(p)} riippumatta aiemmista.")
            wrongs = [(f"Suurempi kuin {fr(p)}, koska {other} on jo \"vuorossa\"", "PRB-01", BAD),
                      (f"Pienempi kuin {fr(p)}, koska sarja jatkuu samana", None,
                       "Sarja ei jatku sen enempää kuin katkeaakaan: heitot ovat toisistaan riippumattomia."),
                      ("Sitä ei voi tietää", None, "Reilun kolikon todennäköisyys tunnetaan: se on 1/2.")]
            steps = [f"Heitot ovat riippumattomia", f"P({other}) = {fr(p)}"]
            final, params, level = fr(p), {"streak": n}, "T"
        elif k == 1:
            m = rng.choice([8, 10, 12, 15])
            p = Fraction(1, 6)
            prompt = (f"Reilua noppaa on heitetty {m} kertaa, eikä kuutosta ole tullut kertaakaan. "
                      "Mitä voidaan sanoa seuraavasta heitosta?")
            correct = (f"Kuutosen todennäköisyys on edelleen {fr(p)}", f"Oikein: nopalla ei ole muistia, todennäköisyys on joka heitolla {fr(p)}.")
            wrongs = [(f"Kuutosen todennäköisyys on nyt suurempi kuin {fr(p)}, koska kuutonen on myöhässä", "PRB-01", BAD),
                      (f"Kuutosen todennäköisyys on nyt pienempi kuin {fr(p)}", None, "Noppa ei \"kyllästy\" kuutoseen: todennäköisyys ei muutu."),
                      ("Kuutonen tulee varmasti seuraavalla heitolla", "PRB-01", BAD)]
            steps = ["Heitot ovat riippumattomia", f"P(6) = {fr(p)}"]
            final, params, level = f"{fr(p)}", {"rolls": m}, "T"
        elif k == 2:
            w = rng.choice([15, 20, 25, 30])
            prompt = (f"Lotossa numero 7 ei ole tullut arvonnassa {w} viikkoon. "
                      "Mikä väite seuraavasta arvonnasta on oikein?")
            correct = ("Numero 7 on yhtä todennäköinen kuin mikä tahansa muu numero",
                       "Oikein: arvonta ei muista aiempia kierroksia, joten jokaisella numerolla on sama todennäköisyys.")
            wrongs = [("Numero 7 on nyt todennäköisempi kuin muut, koska se on myöhässä", "PRB-01", BAD),
                      ("Numero 7 on nyt epätodennäköisempi kuin muut", None, "Arvonta ei suosi eikä karta numeroa 7."),
                      ("Numero 7 ei voi tulla, koska se ei ole tullut pitkään aikaan", None, "Jokainen numero voi tulla milloin tahansa.")]
            steps = ["Arvonnat ovat riippumattomia", "Jokaisen numeron todennäköisyys on sama"]
            final, params, level = "Yhtä todennäköinen kuin muut", {"weeks": w}, "T"
        elif k == 3:
            n = rng.choice([5, 6])
            prompt = (f"Aino ja Eetu heittävät reilua kolikkoa. Kolikko on antanut {n} klaavaa peräkkäin. "
                      "Aino sanoo: \"Nyt kruuna on todennäköisempi, koska tulokset tasoittuvat.\" "
                      "Eetu sanoo: \"Kruuna ja klaava ovat yhtä todennäköisiä.\" Kumpi on oikeassa?")
            correct = ("Eetu: todennäköisyys on 1/2 kummallekin", "Oikein: tasoittuminen tapahtuu vasta pitkässä sarjassa eikä korjaa yksittäistä heittoa.")
            wrongs = [("Aino: kruuna on todennäköisempi", "PRB-01", BAD),
                      ("Kumpikaan ei ole oikeassa, klaava on todennäköisempi", None, "Aiemmat heitot eivät muuta kolikon todennäköisyyksiä."),
                      ("Aino, mutta vain jos heittoja on vähintään 10", "PRB-01", BAD)]
            steps = ["Heitot ovat riippumattomia", "P(kruuna) = P(klaava) = 1/2"]
            final, params, level = "Eetu", {"streak": n}, "H"
        else:
            n = rng.choice([6, 7, 8])
            prompt = (f"Reilulla kolikolla on tullut {n} kruunaa peräkkäin. Mikä perustelu on oikea sille, "
                      "että seuraavalla heitolla klaavan todennäköisyys on 1/2?")
            correct = ("Kolikolla ei ole muistia, joten jokainen heitto on riippumaton aiemmista",
                       "Oikein: riippumattomuus on ratkaiseva perustelu.")
            wrongs = [("Pitkässä sarjassa kruunia ja klaavoja tulee yhtä paljon, joten klaava on vuorossa", "PRB-01", BAD),
                      ("Vaihtoehtoja on kaksi, joten todennäköisyys on aina 1/2", None,
                       "Kaksi vaihtoehtoa ei riitä: esimerkiksi epäreilulla kolikolla todennäköisyydet eivät ole 1/2."),
                      ("Kruuna on tullut jo monta kertaa, joten se on todennäköisempi", None, "Aiemmat heitot eivät muuta todennäköisyyttä.")]
            steps = ["Heitot ovat riippumattomia", "P(klaava) = 1/2 joka heitolla"]
            final, params, level = "Kolikolla ei ole muistia", {"streak": n, "justify": True}, "H"
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S6.06"], ["T19"], 9, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: satunnaisilla toistoilla ei ole muistia.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
