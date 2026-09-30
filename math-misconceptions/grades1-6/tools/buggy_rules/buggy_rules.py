"""Buggy-rule item generation, classification and error spotting for FinnMath.

Covers two documented misconceptions from the item bank:
  NUM-10  smaller-from-larger subtraction (three variants, after Vermeulen et al. 2020)
  NUM-03  numerators and denominators added separately (natural number bias)
  NUM-12  larger denominator taken as the larger fraction

No dependencies beyond the standard library. All checking is deterministic.

EXPERT REVIEW REQUIRED. Logging pupils' answers or keeping per-pupil tallies is processing
of children's personal data. Do not use this code with real pupils in grades 1-6 until the
sign-off in docs/privacy/expert_review_signoff_template.md is complete. Use synthetic data.
"""
from __future__ import annotations

import json
import random
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from typing import Optional

# --------------------------------------------------------------------------
# Rule registry. Ids are stored with every item so responses can be counted.
# --------------------------------------------------------------------------
RULES = {
    "NUM-10a": "Smaller digit subtracted from larger; no regrouping",
    "NUM-10b": "Smaller from larger, and the next digit is also reduced by one",
    "NUM-10c": "Regrouping done in the column, but the next digit is not reduced",
    "NUM-03": "Numerators and denominators added separately",
    "NUM-12": "Larger denominator taken as the larger fraction",
}
SUB_RULES = ("NUM-10a", "NUM-10b", "NUM-10c")
MINUS = "\u2212"  # Finnish typography uses the true minus sign


# ==========================================================================
# 1. Multi-digit subtraction (column method)
# ==========================================================================
def _digits(n: int) -> list[int]:
    return [int(c) for c in reversed(str(n))]


def column_trace(minuend: int, subtrahend: int, rule: Optional[str] = None) -> list[dict]:
    """Column subtraction from the ones column upwards.

    rule=None is the correct procedure. Otherwise one of SUB_RULES changes what
    happens in a column where the top digit is smaller than the bottom digit.
    Borrowing across a zero is always done correctly, so it is never a source
    of the modelled bugs.
    """
    if minuend <= subtrahend:
        raise ValueError("minuend must be larger than subtrahend")
    top = _digits(minuend)
    bot = _digits(subtrahend)
    bot += [0] * (len(top) - len(bot))
    cols, borrow_in = [], 0
    for i, (t, b) in enumerate(zip(top, bot)):
        t_eff = t - borrow_in
        chain = t_eff < 0            # a zero that had to lend onward
        if chain:
            t_eff += 10
        borrow_out = 1 if chain else 0
        need = t_eff < b
        if not need:
            digit = t_eff - b
        else:
            digit = (b - t_eff) if rule in ("NUM-10a", "NUM-10b") else (t_eff + 10 - b)
            if rule in (None, "NUM-10b"):
                borrow_out = 1
        cols.append(dict(pos=i, t=t, b=b, borrow_in=borrow_in, t_eff=t_eff,
                         chain=chain, need=need, digit=digit, borrow_out=borrow_out))
        borrow_in = borrow_out
    return cols


def trace_value(cols: list[dict]) -> int:
    return int("".join(str(c["digit"]) for c in reversed(cols)))


def subtraction_answers(m: int, s: int) -> tuple[int, dict[str, int]]:
    correct = trace_value(column_trace(m, s))
    assert correct == m - s
    return correct, {r: trace_value(column_trace(m, s, r)) for r in SUB_RULES}


def is_diagnostic_subtraction(m: int, s: int) -> bool:
    """Item design constraints taken from Vermeulen et al. (2020).

    - the item needs at least one regrouping;
    - the subtrahend does not end in 8 or 9 (these invite compensation, 76 - 48 via 76 - 50);
    - the difference exceeds 10 (avoids subtraction by adding up);
    - the correct answer and the three bug answers are all different, so a correct
      answer cannot come from a bug by accident (82 - 27 fails this).
    """
    if m - s <= 10 or s % 10 in (8, 9):
        return False
    if not any(c["need"] for c in column_trace(m, s)):
        return False
    correct, bugs = subtraction_answers(m, s)
    vals = [correct, *bugs.values()]
    return len(set(vals)) == len(vals)


def make_subtraction_item(rng: random.Random, ndig_m: int = 3, ndig_s: int = 3) -> dict:
    if ndig_s > ndig_m:
        raise ValueError("subtrahend cannot have more digits than the minuend")
    lo_m, hi_m = 10 ** (ndig_m - 1), 10 ** ndig_m - 1
    lo_s, hi_s = 10 ** (ndig_s - 1), 10 ** ndig_s - 1
    while True:
        m, s = rng.randint(lo_m, hi_m), rng.randint(lo_s, hi_s)
        if m > s and is_diagnostic_subtraction(m, s):
            break
    correct, bugs = subtraction_answers(m, s)
    return {
        "type": "numeric_entry",
        "template": "sub_multidigit_v1",
        "params": {"minuend": m, "subtrahend": s},
        "stem_fi": f"Laske {m} {MINUS} {s}.",
        "answer": str(correct),
        "misconceptions": {r: {"answer": str(v)} for r, v in bugs.items()},
        "workbook": ["NUM-10"],
        "curriculum": ["A36.S2.04"],
    }


# ---- error spotting ------------------------------------------------------
_COLNAMES = ["Ykk\u00f6set", "Kymmenet", "Sadat", "Tuhannet"]


def _lines_fi(cols: list[dict]) -> list[str]:
    out = []
    for c in cols:
        t, b, d, te = c["t"], c["b"], c["digit"], c["t_eff"]
        pre = ""
        if c["borrow_in"]:
            pre = (f"{t} {MINUS} 1 ei onnistu, lainataan: {t + 10} {MINUS} 1 = {te}. " if c["chain"]
                   else f"Lainattu kymmenen pois: {t} {MINUS} 1 = {te}. ")
        if not c["need"]:
            main = f"{te} {MINUS} {b} = {d}."
        elif c["digit"] == b - te:      # reversed subtraction (rules a and b)
            main = f"{b} {MINUS} {te} = {d}."
        else:
            main = f"{te} {MINUS} {b} ei onnistu, lainataan: {te + 10} {MINUS} {b} = {d}."
        out.append(f"{_COLNAMES[c['pos']]}: {pre}{main}")
    out.append(f"Vastaus: {trace_value(cols)}.")
    return out


def make_subtraction_error_item(m: int, s: int, rule: str) -> dict:
    """Worked solution with one injected error; the student taps the faulty line."""
    good = _lines_fi(column_trace(m, s))
    bad = _lines_fi(column_trace(m, s, rule))
    faulty = next(i for i, (g, x) in enumerate(zip(good, bad)) if g != x)
    return {
        "type": "error_spotting",
        "template": "sub_multidigit_err_v1",
        "params": {"minuend": m, "subtrahend": s, "rule": rule},
        "stem_fi": f"Napauta rivi, jossa on virhe. Tehtävä: {m} {MINUS} {s}.",
        "lines_fi": bad,
        "solution_lines_fi": good,
        "faulty_line": faulty,
        "error_tag": rule,
        "workbook": ["NUM-10"],
        "curriculum": ["A36.S2.04"],
    }


# ==========================================================================
# 2. Fractions
# ==========================================================================
def _frac(a: int, b: int) -> str:
    return f"{a}/{b}"


def make_fraction_add_item(rng: random.Random) -> dict:
    while True:
        b, d = rng.randint(2, 9), rng.randint(2, 9)
        a, c = rng.randint(1, b - 1), rng.randint(1, d - 1)
        if b == d:
            continue
        correct = Fraction(a, b) + Fraction(c, d)
        bug = Fraction(a + c, b + d)
        if bug != correct and correct < 2:
            break
    return {
        "type": "numeric_entry",
        "template": "frac_add_v1",
        "params": {"a": a, "b": b, "c": c, "d": d},
        "stem_fi": f"Laske {_frac(a, b)} + {_frac(c, d)}. Vastaa murtolukuna.",
        "answer": str(correct),
        "misconceptions": {"NUM-03": {"answer": str(bug)}},
        "workbook": ["NUM-03"],
        "curriculum": ["A36.S2.12"],
    }


def make_fraction_add_error_item(rng: random.Random) -> dict:
    item = make_fraction_add_item(rng)
    a, b, c, d = (item["params"][k] for k in "abcd")
    lcm = b * d // _gcd(b, d)
    x, y = a * lcm // b, c * lcm // d
    good = [f"{_frac(a, b)} + {_frac(c, d)}",
            f"= {_frac(x, lcm)} + {_frac(y, lcm)}",
            f"= {Fraction(a, b) + Fraction(c, d)}"]
    bad = [good[0],
           f"= ({a} + {c})/({b} + {d})",
           f"= {Fraction(a + c, b + d)}"]
    return {
        "type": "error_spotting",
        "template": "frac_add_err_v1",
        "params": item["params"],
        "stem_fi": "Napauta rivi, jossa on virhe.",
        "lines_fi": bad,
        "solution_lines_fi": good,
        "faulty_line": 1,
        "error_tag": "NUM-03",
        "workbook": ["NUM-03"],
        "curriculum": ["A36.S2.12"],
    }


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def make_fraction_compare_item(rng: random.Random) -> dict:
    """Unit fractions: which is larger? Choice item, kept for quick checks only."""
    b, d = rng.sample(range(2, 13), 2)
    options = [f"1/{b}", f"1/{d}"]
    correct = 0 if b < d else 1
    return {
        "type": "choice",
        "template": "frac_compare_unit_v1",
        "params": {"b": b, "d": d},
        "stem_fi": f"Kumpi on suurempi, {options[0]} vai {options[1]}?",
        "options": options,
        "answer": options[correct],
        "misconceptions": {"NUM-12": {"answer": options[1 - correct]}},
        "workbook": ["NUM-12"],
        "curriculum": ["A36.S2.11"],
    }


# ==========================================================================
# 3. Answer parsing and classification
# ==========================================================================
def parse_answer(text: str) -> Optional[Fraction]:
    """Accepts 7, 5/6, 1 1/6, 0,5 and 0.5. Returns None if unreadable.
    Equivalent forms (10/12 for 5/6) compare equal; the app may add a
    'lowest terms' requirement on top of this if the task asks for it."""
    t = str(text).strip().replace("\u2212", "-").replace(",", ".")
    try:
        if " " in t and "/" in t:
            whole, frac = t.split(None, 1)
            n, d = frac.split("/")
            sign = -1 if whole.startswith("-") else 1
            return sign * (abs(Fraction(int(whole))) + Fraction(int(n), int(d)))
        if "/" in t:
            n, d = t.split("/")
            return Fraction(int(n), int(d))
        return Fraction(Decimal(t))
    except (ValueError, ZeroDivisionError, InvalidOperation):
        return None


def classify(item: dict, raw_answer: str) -> dict:
    """Compare a typed or chosen answer with the correct one and every stored bug answer.

    status: correct | matched | ambiguous | unexplained | unparsed
    """
    if item["type"] == "choice":
        if raw_answer == item["answer"]:
            return {"status": "correct", "rules": []}
        hits = [r for r, v in item["misconceptions"].items() if v["answer"] == raw_answer]
        return {"status": "matched" if hits else "unexplained", "rules": hits}
    val = parse_answer(raw_answer)
    if val is None:
        return {"status": "unparsed", "rules": []}
    if val == parse_answer(item["answer"]):
        return {"status": "correct", "rules": []}
    hits = [r for r, v in item["misconceptions"].items() if val == parse_answer(v["answer"])]
    if len(hits) == 1:
        return {"status": "matched", "rules": hits}
    return {"status": "ambiguous" if hits else "unexplained", "rules": hits}


def check_tap(item: dict, tapped_line: int) -> dict:
    """Error spotting: a wrong tap still says which error the student did not notice."""
    if tapped_line == item["faulty_line"]:
        return {"correct": True, "missed_error_tag": None, "tap_kind": "hit"}
    kind = "before_error" if tapped_line < item["faulty_line"] else "after_error"
    return {"correct": False, "missed_error_tag": item["error_tag"], "tap_kind": kind}


# ==========================================================================
# 4. Per-student tally with a minimum-evidence guard
# ==========================================================================
class Tally:
    """Counts matched rules per student. A rule is flagged only when it explains wrong
    answers on at least `min_items` different items. Bugs are known to be unstable
    (Hennessy, 1993; Vermeulen et al., 2020), so one match proves little.

    EXPERT REVIEW REQUIRED: a per-pupil tally is a profile of a child. Keep it disabled for
    real pupils in grades 1-6 until the privacy sign-off is complete."""

    def __init__(self, min_items: int = 2):
        self.min_items = min_items
        self._items: dict[str, set[str]] = {}
        self.wrong_unexplained = 0

    def add(self, item_id: str, result: dict) -> None:
        if result["status"] == "matched":
            for r in result["rules"]:
                self._items.setdefault(r, set()).add(item_id)
        elif result["status"] in ("unexplained", "ambiguous"):
            self.wrong_unexplained += 1

    def flags(self) -> list[str]:
        return sorted(r for r, ids in self._items.items() if len(ids) >= self.min_items)

    def counts(self) -> dict[str, int]:
        return {r: len(ids) for r, ids in self._items.items()}


# ==========================================================================
# Demo: python buggy_rules.py > sample_items.json
# ==========================================================================
def demo(seed: int = 7) -> dict:
    rng = random.Random(seed)
    m, s = 453, 127
    return {
        "numeric_entry_subtraction": [make_subtraction_item(rng) for _ in range(3)],
        "numeric_entry_fraction_add": [make_fraction_add_item(rng) for _ in range(3)],
        "error_spotting_subtraction": [make_subtraction_error_item(m, s, r) for r in SUB_RULES],
        "error_spotting_fraction_add": [make_fraction_add_error_item(rng)],
        "choice_fraction_compare": [make_fraction_compare_item(rng) for _ in range(2)],
    }


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
