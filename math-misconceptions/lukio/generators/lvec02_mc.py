#!/usr/bin/env python3
"""LVEC-02 MC (lukio level): a vector is tied to its position. A vector is a free displacement:
two arrows with the same components are the same vector wherever they start. Correct answers
are computed from coordinates with sympy; distractors carry the misconception tag."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "lvec02_mc"
TID, CODE = "LVEC-02", "MC"
GENERIC = "Vektori kuvaa siirtymän: sen määräävät suunta ja pituus eli komponentit, ei alkupiste. Samat komponentit tarkoittavat samaa vektoria."


def pt(p):
    return f"({show(p[0])}, {show(p[1])})"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1402)
    items = []

    def add(n, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, ["MAA4.07"], ["G2"], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: same components, different starting points
    a, p, q = sp.Matrix([2, 3]), (0, 0), (4, 1)
    end2 = (q[0] + a[0], q[1] + a[1])
    add(start, "P",
        f"Vektori a = {pt(a)} piirretään origosta. Vektori b = {pt(a)} piirretään pisteestä {pt(q)}. Ovatko a ja b sama vektori?",
        ("Ovat, koska niillä on samat komponentit eli sama pituus ja suunta.", "Oikein: vektori ei riipu alkupisteestä."),
        [("Eivät, koska ne alkavat eri pisteistä.", TID, "Alkupiste ei kuulu vektoriin. Vektorin määräävät komponentit, ja ne ovat samat."),
         ("Eivät, koska ne päättyvät eri pisteisiin.", TID, f"Loppupiste riippuu alkupisteestä: b päättyy pisteeseen {pt(end2)}. Vektori kuvaa siirtymän, ei paikkaa."),
         ("Ovat vain, jos ne päättyvät samaan pisteeseen.", None, "Ehto ei ole tarpeen. Samat komponentit riittävät.")],
        ["Molempien komponentit ovat (2, 3).", "Samat komponentit tarkoittavat samaa siirtymää, joten vektorit ovat samat."],
        "Ovat sama vektori", {"a": [2, 3], "start_b": list(q)})
    # 2: end point of a vector from a given start
    a, A = sp.Matrix([3, 1]), (1, 2)
    B = (A[0] + a[0], A[1] + a[1])
    add(start + 1, "T",
        f"Vektori a = {pt(a)} piirretään pisteestä A = {pt(A)}. Mihin pisteeseen sen kärki osuu?",
        (pt(B), f"Oikein: {pt(A)} + {pt(a)} = {pt(B)}."),
        [(pt(a), TID, "Vektorin komponentit eivät ole kärkipisteen koordinaatit, ellei vektori alku ole origossa."),
         (pt((A[0] - a[0], A[1] - a[1])), None, "Vektori lisätään alkupisteen koordinaatteihin, ei vähennetä."),
         (pt((A[0] * a[0], A[1] * a[1])), None, "Siirtymä lisätään alkupisteeseen, ei kerrota.")],
        [f"Kärki = alkupiste + vektori = {pt(A)} + {pt(a)}.", f"Kärki on {pt(B)}."], pt(B), {"a": [3, 1], "A": list(A)})
    # 3: sum of vectors drawn from different points
    a, b, qb = sp.Matrix([2, 0]), sp.Matrix([0, 3]), (5, 5)
    s = a + b
    endb = (qb[0] + b[0], qb[1] + b[1])
    wrong1 = (a[0] + endb[0], a[1] + endb[1])
    add(start + 2, "T",
        f"Vektori a = {pt(a)} piirretään origosta ja vektori b = {pt(b)} pisteestä {pt(qb)}. Mikä on a + b?",
        (pt(s), "Oikein: summa lasketaan komponenteista."),
        [(pt(wrong1), TID, f"Tässä a:han on lisätty vektorin b kärkipisteen {pt(endb)} koordinaatit. Vektorin b komponentit ovat {pt(b)}, riippumatta mistä se piirretään."),
         (pt(endb), TID, "Tämä on vektorin b kärkipiste, ei summa. Vektorin b alkupiste ei vaikuta sen komponentteihin."),
         (pt((a[0] * b[0], a[1] * b[1])), None, "Vektorit lasketaan yhteen komponenteittain, ei kerrota.")],
        [f"a + b = {pt(a)} + {pt(b)} = {pt(s)}.", "Alkupisteet eivät vaikuta summaan."], pt(s), {"a": [2, 0], "b": [0, 3], "start_b": list(qb)})
    # 4: vectors AB and CD from point coordinates
    A, B, C, D = (1, 1), (4, 5), (3, 0), (6, 4)
    AB = sp.Matrix([B[0] - A[0], B[1] - A[1]])
    CD = sp.Matrix([D[0] - C[0], D[1] - C[1]])
    assert AB == CD
    add(start + 3, "H",
        f"Pisteet ovat A = {pt(A)}, B = {pt(B)}, C = {pt(C)} ja D = {pt(D)}. Ovatko vektorit AB ja CD yhtä suuret?",
        (f"Ovat, koska molempien komponentit ovat {pt(AB)}.", "Oikein: vektorin määrää siirtymä, ei alku- ja loppupiste."),
        [("Eivät, koska alku- ja loppupisteet ovat eri.", TID, f"Eri pisteet eivät tee vektoreista erilaisia. AB = {pt(AB)} ja CD = {pt(CD)}."),
         (f"Ne ovat yhtä pitkät mutta eri vektorit, koska ne sijaitsevat eri kohdissa.", TID, "Vektori ei sijaitse missään. Samat komponentit tarkoittavat samaa vektoria, jolloin myös suunta on sama."),
         ("Eivät, koska CD on pidempi.", None, f"Tarkista pituudet: |AB| = |CD| = {sp.sqrt(AB.dot(AB))}.")],
        [f"AB = B − A = {pt(AB)}.", f"CD = D − C = {pt(CD)}.", "Komponentit ovat samat, joten vektorit ovat yhtä suuret."],
        "Ovat yhtä suuret", {"A": list(A), "B": list(B), "C": list(C), "D": list(D)})
    # 5: displacement order, justification
    east, north = 3, 4
    add(start + 4, "H",
        f"Anna kulkee {east} km itään ja sitten {north} km pohjoiseen. Eero lähtee samasta paikasta ja kulkee ensin {north} km pohjoiseen ja sitten {east} km itään. Onko heidän kokonaissiirtymänsä sama vektori? Valitse perustelu.",
        (f"On, koska molemmilla siirtymä on ({east}, {north}) riippumatta reitistä ja välipisteistä.", "Oikein: a + b = b + a."),
        [("Ei ole, koska he kulkevat eri pisteiden kautta.", TID, "Reitti ja välipisteet eivät kuulu kokonaissiirtymään. Vektorin summa a + b on sama kuin b + a."),
         ("Ei ole, koska kokonaissiirtymän täytyy alkaa eri paikasta.", TID, "Siirtymä ei riipu alkupisteestä: molemmat alkavat samasta paikasta, ja silloinkin vektori määräytyisi komponenteista."),
         (f"On vain, jos kulkureitti on yhtä pitkä, {east + north} km.", None, "Pituus ei yksin ratkaise: vektorien yhtäsuuruus vaatii samat komponentit.")],
        [f"Siirtymät ovat ({east}, 0) ja (0, {north}).", f"Summa on ({east}, {north}) kummassakin järjestyksessä.", "Vektorien yhteenlasku on vaihdannainen."],
        "On sama vektori", {"east": east, "north": north})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
