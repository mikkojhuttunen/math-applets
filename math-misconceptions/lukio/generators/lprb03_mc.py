#!/usr/bin/env python3
"""LPRB-03 MC: conjunction fallacy (P(A and B) judged larger than P(A)). Probabilities of the
dice and number examples are computed by enumeration; the distractor ranks the more detailed
event higher."""
import random
from fractions import Fraction

from gen_common import base_item, cli, frac, mc_options

TEMPLATE = "lprb03_mc"
TID, CODE = "LPRB-03", "MC"
GENERIC = "Tapahtuma ”A ja B” on aina osa tapahtumaa A, joten sen todennäköisyys ei voi olla suurempi kuin P(A). Tarkempi kuvaus ei tee tapahtumasta todennäköisempää."


def make_items(run, date, count=5, start=1):
    rng = random.Random(8203)
    items = []

    def add(n, lops, syll, level, g, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: die: prime vs prime and even
    prime = {x for x in range(1, 7) if x in (2, 3, 5)}
    both = {x for x in prime if x % 2 == 0}
    pa, pb = Fraction(len(prime), 6), Fraction(len(both), 6)
    assert pb < pa
    add(start, ["MAA8.05"], "MAA", "P", ["G3"],
        "Noppaa heitetään kerran. Kumpi on todennäköisempää: A) tulos on alkuluku, vai B) tulos on alkuluku ja parillinen?",
        (f"A, todennäköisyys {frac(pa)} (B:n todennäköisyys on {frac(pb)})", "Oikein: B:hen kuuluu vain tulos 2, A:han kuuluu tulokset 2, 3 ja 5."),
        [("B, koska se kertoo tuloksesta enemmän", TID, "Tarkempi kuvaus ei lisää todennäköisyyttä: tapahtuma B on osa tapahtumaa A."),
         ("Yhtä todennäköisiä, koska 2 on alkuluku", None, "Tulokset 3 ja 5 kuuluvat vain tapahtumaan A, joten A on todennäköisempi.")],
        ["A: tulokset 2, 3, 5 → 3/6.", "B: tulos 2 → 1/6.", "B on osa A:ta, joten P(B) ≤ P(A)."], "A", {"event": "prime"})

    # 2: free throws
    p_first = Fraction(6, 10)
    add(start + 1, ["MAB5.06"], "MAB", "T", ["G3"],
        "Koripalloilija onnistuu vapaaheitoissa 60 prosentin todennäköisyydellä. Kumpi on todennäköisempää: A) ensimmäinen heitto menee sisään, vai B) kaksi ensimmäistä heittoa menevät molemmat sisään?",
        ("A on todennäköisempää", "Oikein: P(A) = 0,6, mutta P(B) = 0,6 · 0,6 = 0,36 on pienempi."),
        [("B on todennäköisempää, koska pelaaja on hyvä heittäjä", TID, "Molemmat heitot sisään on osa tilannetta ”ensimmäinen sisään”, joten sen todennäköisyys on pienempi."),
         ("Yhtä todennäköisiä, koska heitot ovat samanlaisia", None, "Toisenkin heiton pitää onnistua, mikä pienentää todennäköisyyttä.")],
        ["P(A) = 0,6.", "P(B) = 0,6 · 0,6 = 0,36.", "0,36 < 0,6."], "A", {"p": "0.6"})

    # 3: club, general principle
    add(start + 2, ["MAB5.06"], "MAB", "T", ["G3"],
        "Kerhosta arvotaan yksi jäsen. Tapahtuma A: jäsen on tyttö. Tapahtuma B: jäsen on tyttö ja pelaa jalkapalloa. Mikä väite on aina tosi?",
        ("P(B) ≤ P(A)", "Oikein: jokainen B:hen kuuluva jäsen kuuluu myös A:han."),
        [("P(B) > P(A), koska B on tarkempi kuvaus", TID, "Tarkempi kuvaus rajaa joukkoa pienemmäksi, ei suuremmaksi."),
         ("P(B) = P(A)", None, "Näin on vain, jos kaikki kerhon tytöt pelaavat jalkapalloa. Aina tosi väite on P(B) ≤ P(A).")],
        ["B-joukko on A-joukon osajoukko.", "Osajoukon todennäköisyys ei ole suurempi."], "P(B) ≤ P(A)", {"setting": "club"})

    # 4: numbers
    add(start + 3, ["MAA8.05"], "MAA", "T", ["G3"],
        "Tapahtuman A todennäköisyys on 0,30. Mikä seuraavista voi olla tapahtuman ”A ja B” todennäköisyys?",
        ("0,25", "Oikein: se on enintään P(A) = 0,30."),
        [("0,35", TID, "”A ja B” on osa A:ta, joten sen todennäköisyys ei ylitä lukua 0,30."),
         ("0,50", TID, "”A ja B” on osa A:ta, joten sen todennäköisyys ei ylitä lukua 0,30.")],
        ["P(A ja B) ≤ P(A) = 0,30.", "Vain 0,25 on enintään 0,30."], "0,25", {"p_a": "0.30"})

    # 5: justification, G3
    add(start + 4, ["MAA8.05"], "MAA", "H", ["G3"],
        "Aino lukee paljon, käy kirjastossa viikoittain ja pitää hiljaisuudesta. Kumpi on todennäköisempää: A) Aino on kirjastovirkailija, vai B) Aino on kirjastovirkailija ja kirjoittaa blogia? Valitse paras perustelu vastaukselle.",
        ("A on todennäköisempää, koska jokainen B:n täyttävä henkilö täyttää myös A:n", "Oikein: B on A:n osajoukko, joten P(B) ≤ P(A) riippumatta Ainon kuvauksesta."),
        [("B on todennäköisempää, koska kuvaus sopii Ainoon paremmin", TID, "Kuvauksen sopivuus ei muuta joukkojen kokoja: B on osa A:ta."),
         ("B on todennäköisempää, koska bloggaaminen sopii kirjalliseen ihmiseen", TID, "Lisäehto voi vain pienentää todennäköisyyttä, ei suurentaa."),
         ("Ei voi sanoa, koska Ainosta ei tiedetä tarpeeksi", None, "Vertailu onnistuu ilman lisätietoa: osajoukko ei ole todennäköisempi kuin kokonaisuus.")],
        ["B-joukko on A-joukon osajoukko.", "Siksi P(B) ≤ P(A)."], "A, koska B on A:n osajoukko", {"setting": "library"})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
