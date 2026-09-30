"""Shared helpers for the decimal-comparison generators (NUM-01, NUM-02); not a template itself."""
from decimal import Decimal

# (intro with {a} {b}, question, unit) for "which is larger" items
CTX = [
    ("Pituushypyssä kaksi hyppyä mitattiin tuloksiksi {a} m ja {b} m.", "Kumpi hyppy oli pidempi?", "m"),
    ("Kahden pussin painot ovat {a} kg ja {b} kg.", "Kumpi pussi on painavampi?", "kg"),
    ("Kahdessa pullossa on mehua {a} l ja {b} l.", "Kummassa pullossa on enemmän mehua?", "l"),
    ("Kaksi lankakerää on mitattu: toisessa on {a} m ja toisessa {b} m lankaa.", "Kummassa kerässä on enemmän lankaa?", "m"),
    ("Kahden kasvin pituudet ovat {a} m ja {b} m.", "Kumpi kasvi on pidempi?", "m"),
]
CTX3 = [
    ("Kolmen pussin painot ovat {a} kg, {b} kg ja {c} kg.", "Mikä on painavimman pussin paino?", "kg"),
    ("Kolmen hypyn tulokset ovat {a} m, {b} m ja {c} m.", "Mikä on pisin tulos?", "m"),
    ("Kolmessa pullossa on mehua {a} l, {b} l ja {c} l.", "Paljonko mehua on eniten sisältävässä pullossa?", "l"),
]
CTX4 = [
    ("Viiden metrin mittaisessa hyppysarjassa tulokset olivat {a} m, {b} m, {c} m ja {d} m.", "Mikä oli pisin tulos?", "m"),
    ("Neljän pakkauksen painot ovat {a} kg, {b} kg, {c} kg ja {d} kg.", "Mikä on painavimman pakkauksen paino?", "kg"),
    ("Neljän ämpärin tilavuudet ovat {a} l, {b} l, {c} l ja {d} l.", "Mikä on suurin tilavuus?", "l"),
]


def dec(s):
    return Decimal(s)


def fmt(d):
    """Decimal as Finnish text: decimal comma, no exponent."""
    return format(d, "f").replace(".", ",")


def digits(d):
    return -d.as_tuple().exponent


def hundredths(whole, n):
    """whole + n/100 with n in 1..99 (n%10 != 0 gives two decimals)."""
    return Decimal(whole) + Decimal(n) / 100


def tenths(whole, d):
    return Decimal(whole) + Decimal(d) / 10
