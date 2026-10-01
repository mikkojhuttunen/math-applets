"""Helpers shared by the EXT-08 generators (not a template itself): data lists and exact medians."""
from fractions import Fraction


def median(vals):
    s = sorted(vals)
    n = len(s)
    return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def written_middle(vals):
    """What a pupil gets by reading the middle of the list without sorting it."""
    n = len(vals)
    return Fraction(vals[n // 2]) if n % 2 else Fraction(vals[n // 2 - 1] + vals[n // 2], 2)


def mean(vals):
    return Fraction(sum(vals), len(vals))


def dec(f):
    """Decimal comma text of a terminating fraction."""
    f = Fraction(f)
    assert f.denominator in (1, 2, 4, 5, 8, 10, 20, 25), f
    s = f"{float(f):.10f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def pick_list(rng, n, lo=2, hi=30, want_mean=False):
    """Random unsorted list of n distinct values where the written middle differs from the median
    (and, with want_mean, the mean is a terminating decimal different from the median)."""
    while True:
        vals = rng.sample(range(lo, hi), n)
        if vals == sorted(vals) or vals == sorted(vals, reverse=True):
            continue
        md, wm, mn = median(vals), written_middle(vals), mean(vals)
        if md == wm:
            continue
        if md.denominator not in (1, 2) or wm.denominator not in (1, 2):
            continue
        if want_mean and (mn == md or mn == wm or mn.denominator not in (1, 2, 4, 5, 10)):
            continue
        return vals


def txt(vals):
    return ", ".join(str(v) for v in vals)
