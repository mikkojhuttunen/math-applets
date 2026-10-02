#!/usr/bin/env python3
"""Verify the lukio exercise bank.

Copied from ../../scripts/verify.py (7-9) and adapted as BACKLOG_LUKIO.md
section 0 describes. Checks, in this order:
  1. Wrapper and item structure against schema/item.schema.json
  2. Curriculum links against the BACKLOG_LUKIO.md topic table and the
     LOPS 2019 goal file: goal IDs exist and are not retired, belong to the
     topic, and match the item's syllabus (MAA items: MAA or MAY1 goals,
     MAB items: MAB or MAY1 goals); G-goals belong to the topic
  3. Algebra: recomputes answers, injected errors and distractors with sympy
     (NE, ES, SO, FS, ME, RP), including the lukio answer kinds rational,
     antiderivative (checked by differentiating), periodic (base solutions
     plus period) and interval (union of intervals). MC and other types are
     checked structurally only.
  4. --base REF:      existing items must be unchanged; new items must be draft
  5. --check-backlog: matrix cells in the backlog must agree with the files

Notation: e is Euler's number and never a variable; ln is the natural
logarithm, lg the base-10 logarithm; log without a base is read as ln.
Exit code 0 and the last line "VERIFY OK ..." mean the bank is consistent.
Usage (run from math-misconceptions/lukio/):
  python scripts/verify.py --base HEAD --check-backlog
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr, standard_transformations, implicit_multiplication_application)
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    sys.exit(f"Missing dependency: {exc}. Run: pip install -r ../requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = "BACKLOG_LUKIO.md"
LOPS_FILE = Path("data") / "curriculum" / "LOPS_2019_matematiikka_oppimistavoitteet.md"
CATALOGUE = Path("data") / "misconceptions" / "lukio_misconceptions.md"
SCHEMA_VERSION = "lukio-1.0"
ID_PREFIX = "LU-"
TYPE_CODES = ["MC", "NE", "ES", "SO", "FS", "ME", "RP", "SC", "MA", "EST", "GI", "NL", "EX", "TF", "PH"]
CHECKED_TYPES = {"MC", "NE", "ES", "SO", "FS", "ME", "RP"}
LOCAL = {c: sp.Symbol(c) for c in "abcdfghijklmnopqrstuvwxyz"}
LOCAL.update({c: sp.Symbol(c) for c in "CDK"})
LOCAL.update({"e": sp.E, "pi": sp.pi, "ln": sp.log, "log": sp.log, "lg": lambda x: sp.log(x, 10),
              "exp": sp.exp, "sqrt": sp.sqrt, "Abs": sp.Abs, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
              "asin": sp.asin, "acos": sp.acos, "atan": sp.atan})
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
POOL = [sp.Rational(v) for v in (-3, -2, -1, 2, 3, 5, 7, 4, 9)] + [
    sp.Rational(1, 2), sp.Rational(-5, 3), sp.Rational(3, 2), sp.Rational(11, 3), sp.Rational(6, 5)]


class Unsupported(Exception):
    """A line or expression the checker cannot interpret (reported as a warning)."""


# ----------------------------------------------------------------- parsing
def norm(s):
    s = s.strip()
    s = re.sub(r"\|([^|]+)\|", r"Abs(\1)", s)
    for a, b in (("−", "-"), ("–", "-"), ("—", "-"), ("×", "*"), ("·", "*"), ("÷", "/"), ("π", "pi"),
                 ("½", "(1/2)"), ("²", "**2"), ("³", "**3"), ("^", "**"), ("≤", "<="), ("≥", ">="), ("°", "")):
        s = s.replace(a, b)
    s = re.sub(r"√\(", "sqrt(", s)
    s = re.sub(r"√([0-9]+|[a-z])", r"sqrt(\1)", s)
    return re.sub(r"(?<=\d),(?=\d)", ".", s)  # decimal comma -> point


def parse(text):
    try:
        return parse_expr(norm(str(text)), local_dict=dict(LOCAL), transformations=TRANSFORMS)
    except Exception as exc:
        raise Unsupported(f"cannot parse '{text}': {exc}")


def parse_line(text):
    """Return ('ex', expr) | ('eq', lhs-rhs) | ('ineq', relational)."""
    t = re.sub(r"^\s*=\s*", "", norm(text))  # step-ordering lines may start with "="
    m = re.search(r"<=|>=|<|>", t)
    if m:
        l, r = t.split(m.group(0), 1)
        rel = {"<": sp.Lt, ">": sp.Gt, "<=": sp.Le, ">=": sp.Ge}[m.group(0)]
        return "ineq", rel(parse(l), parse(r), evaluate=False)
    if t.count("=") > 1:
        raise Unsupported(f"more than one '=' in '{text}'")
    if "=" in t:
        l, r = t.split("=")
        return "eq", parse(l) - parse(r)
    return "ex", parse(t)


def solset(kind, e):
    syms = e.free_symbols
    if not syms:
        truth = bool(e == 0) if kind == "eq" else bool(e)
        return sp.S.Reals if truth else sp.S.EmptySet
    if len(syms) > 1:
        raise Unsupported("more than one unknown")
    return sp.solveset(e, next(iter(syms)), sp.S.Reals)


def numeric_equal(ea, eb):
    syms = sorted(ea.free_symbols | eb.free_symbols, key=str)
    valid = 0
    for i in range(len(POOL)):
        point = {s: POOL[(i + 4 * j) % len(POOL)] for j, s in enumerate(syms)}
        try:
            va, vb = ea.subs(point), eb.subs(point)
            if any(v.has(sp.zoo, sp.nan, sp.oo, -sp.oo) for v in (va, vb)):
                continue
            ca, cb = complex(sp.N(va, 30)), complex(sp.N(vb, 30))
            if abs(ca.imag) > 1e-12 or abs(cb.imag) > 1e-12:
                continue  # outside the real domain (logarithm, root)
            if abs(ca - cb) > 1e-9 * max(1.0, abs(ca)):
                return False
            valid += 1
        except (TypeError, ZeroDivisionError):
            continue
    return valid >= 4


def exact(value):
    """Exact sympy number from a JSON number or a string such as 'pi/6'."""
    v = sp.nsimplify(value) if isinstance(value, (int, float)) else parse(value)
    if v.free_symbols:
        raise Unsupported(f"'{value}' is not a number")
    return v


def close(a, b):
    return abs(complex(sp.N(a - b, 30))) < 1e-9


def same(a, b):
    ka, ea = parse_line(a)
    kb, eb = parse_line(b)
    if ka != kb:
        return False
    return numeric_equal(ea, eb) if ka == "ex" else solset(ka, ea) == solset(kb, eb)


def finite_at(expr, variables, samples):
    for sample in samples:
        if len(sample) != len(variables):
            return f"sample {sample} does not match variables {variables}"
        value = expr.subs({sp.Symbol(v): sp.nsimplify(x) for v, x in zip(variables, sample)})
        if value.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
            return f"reference is undefined at sample {sample}"
    return None


# ------------------------------------------------- backlog / LOPS data
def table_rows(text, header_start):
    """Cells of the Markdown table whose header line starts with header_start."""
    rows, active = [], False
    for line in text.splitlines():
        if line.startswith(header_start):
            active = True
            continue
        if not active:
            continue
        if not line.startswith("|"):
            break
        if set(line.replace("|", "").strip()) <= set("-: "):
            continue
        rows.append([x.strip() for x in line.strip().strip("|").split("|")])
    return rows


def split_list(s):
    return [x.strip() for x in s.split(",") if x.strip() and x.strip() != "-"]


def parse_topics(text):
    """Topic table of BACKLOG_LUKIO.md section 3.1."""
    topics = {}
    for c in table_rows(text, "| ID | Topic | Evidence"):
        if len(c) >= 9:
            topics[c[0]] = {"main": c[4], "also": split_list(c[5]), "syllabus": split_list(c[6]),
                            "g": split_list(c[7]), "vk": c[8]}
    return topics


def parse_lops(text):
    """Goal IDs, retired goal IDs and G-goal IDs of the LOPS 2019 goal file."""
    goals, retired = set(), set()
    for gid, desc in re.findall(r"^\| ((?:MAY1|MAA\d{1,2}|MAB\d)\.\d\d) \| ([^|]*)\|", text, re.M):
        (retired if desc.strip().startswith("*poistettu") else goals).add(gid)
    gs = set(re.findall(r"^\| (G[1-8]) \|", text, re.M))
    return goals, retired, gs


def parse_catalogue(text):
    """Misconception IDs of the lukio catalogue, including carried-over 1-9 rows."""
    return set(re.findall(r"^\| ([A-Z]{3,4}-\d{2}) \|", text, re.M))


def goal_syllabus(gid):
    """'MAY' for the common module, otherwise 'MAA' or 'MAB'."""
    return gid[:3]


def parse_matrix(text):
    codes, rows, active = [], {}, False
    for line in text.splitlines():
        if line.startswith("| ID | MC |"):
            codes = [x.strip() for x in line.strip().strip("|").split("|")][1:]
            active = True
            continue
        if not active:
            continue
        if not line.startswith("|"):
            break
        if set(line.replace("|", "").strip()) <= set("-: "):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        rows[c[0]] = dict(zip(codes, c[1:]))
    return codes, rows


# ----------------------------------------------------------- type checks
def check_MC(it, tid, topics):
    errs, warns = [], []
    p = it["payload"]
    ids = [o["id"] for o in p["options"]]
    if len(set(ids)) != len(ids):
        errs.append("duplicate option ids")
    if p["correct"][0] not in ids:
        errs.append("correct id is not among the options")
    texts = [o["text"].strip().lower() for o in p["options"]]
    if len(set(texts)) != len(texts):
        errs.append("two options have the same text")
    wrong = [o for o in p["options"] if o["id"] != p["correct"][0]]
    for o in p["options"]:
        if o["id"] == p["correct"][0] and o["misconception"] is not None:
            errs.append("the correct option must have misconception null")
        if o["misconception"] and o["misconception"] not in topics:
            errs.append(f"option {o['id']}: unknown misconception {o['misconception']}")
    if not any(o["misconception"] == tid for o in wrong):
        errs.append(f"no wrong option is tagged with the topic misconception {tid}")
    if any(o["misconception"] is None for o in wrong):
        warns.append("some wrong options carry no misconception tag")
    warns.append("MC correctness is not machine-checked; rely on the generator script and review")
    return errs, warns


def check_rational(a, wrong):
    errs, warns = [], []
    value = sp.Rational(a["value"])
    if str(value) != a["value"].lstrip("+"):
        errs.append(f"rational value '{a['value']}' is not in lowest terms (expected {value})")
    for w in wrong:
        m = str(w["match"])
        try:
            wv = exact(m)
        except Unsupported:
            continue
        if close(wv, value):
            if re.search(r"\d[.,]\d", m):
                warns.append(f"wrong answer '{m}' is the decimal form of the correct value; tag it as a form error, not a misconception")
            else:
                errs.append(f"wrong answer '{m}' equals the correct value")
    return errs, warns


def check_antiderivative(a, wrong):
    errs = []
    x, c = sp.Symbol(a["variable"]), sp.Symbol(a["constant"])
    f, F = parse(a["integrand"]), parse(a["reference"])
    if c not in F.free_symbols:
        errs.append(f"reference '{a['reference']}' does not contain the constant {a['constant']}")
    if not numeric_equal(sp.diff(F, x), f):
        errs.append(f"the derivative of the reference is not the integrand '{a['integrand']}'")
    problem = finite_at(F.subs(c, 0), [a["variable"]], a["samples"])
    if problem:
        errs.append(problem)
    for w in wrong:
        W = parse(str(w["match"]))
        if c in W.free_symbols and numeric_equal(sp.diff(W, x), f):
            errs.append(f"wrong answer '{w['match']}' is a correct antiderivative with the constant")
    return errs


def periodic_base(a):
    """(equation in the item's unit, period, sorted base values) for a periodic answer."""
    x = sp.Symbol(a["variable"])
    kind, e = parse_line(a["reference"])
    if kind != "eq":
        raise Unsupported("answer kind 'periodic' needs an equation")
    if a["unit"] == "deg":
        e = e.subs(x, x * sp.pi / 180)
    return x, e, exact(a["period"]), [exact(v) for v in a["base"]]


def check_periodic(a, wrong):
    errs = []
    x, e, period, base = periodic_base(a)
    if not period.is_positive:
        return [f"period {a['period']} must be positive"]
    for v in base:
        if not (v >= 0 and v < period):
            errs.append(f"base solution {v} is not in [0, {period})")
        elif not close(e.subs(x, v), 0):
            errs.append(f"base solution {v} does not satisfy the equation")
    if len(set(base)) != len(base):
        errs.append("base solutions repeat")
    if not numeric_equal(e.subs(x, x + period), e):
        errs.append(f"{a['period']} is not a period of the equation")
    found = sp.solveset(e, x, sp.Interval.Ropen(0, period))
    if not isinstance(found, sp.FiniteSet):
        raise Unsupported(f"cannot list the solutions of '{a['reference']}' in one period")
    missing = [v for v in found if not any(close(v, b) for b in base)]
    if missing:
        errs.append(f"base solutions miss {sorted(missing, key=float)} in [0, {period})")
    return errs


def interval_set(a):
    parts = []
    for iv in a["intervals"]:
        lo = -sp.oo if iv["lo"] is None else exact(iv["lo"])
        hi = sp.oo if iv["hi"] is None else exact(iv["hi"])
        parts.append(sp.Interval(lo, hi, not iv["lo_closed"] or lo == -sp.oo, not iv["hi_closed"] or hi == sp.oo))
    return parts


def same_set(s1, s2):
    return sp.Complement(s1, s2) == sp.S.EmptySet and sp.Complement(s2, s1) == sp.S.EmptySet


def check_interval(a, wrong):
    errs = []
    kind, rel = parse_line(a["reference"])
    if kind != "ineq":
        return ["answer kind 'interval' needs an inequality"]
    parts = interval_set(a)
    for i, iv in enumerate(parts, 1):
        if iv == sp.S.EmptySet:
            errs.append(f"interval {i} is empty")
    if errs:
        return errs
    for i in range(1, len(parts)):
        if parts[i - 1].sup > parts[i].inf or (parts[i - 1].sup == parts[i].inf and
                                               parts[i - 1].contains(parts[i].inf) and parts[i].contains(parts[i].inf)):
            errs.append(f"intervals {i} and {i + 1} overlap or are out of order")
    declared = sp.Union(*parts) if parts else sp.S.EmptySet
    if not same_set(solset(kind, rel), declared):
        errs.append(f"intervals do not match the solution set {solset(kind, rel)} of '{a['reference']}'")
    for w in wrong:
        try:
            wk, we = parse_line(str(w["match"]))
        except Unsupported:
            continue
        if wk == "ineq" and same_set(solset(wk, we), declared):
            errs.append(f"wrong answer '{w['match']}' has the correct solution set")
    return errs


def check_NE(it, tid, topics):
    errs, warns = [], []
    p = it["payload"]
    a = p["answer"]
    if a["kind"] == "expression":
        ref = parse(a["reference"])
        problem = finite_at(ref, a["variables"], a["samples"])
        if problem:
            errs.append(problem)
        for w in p["wrong"]:
            if numeric_equal(ref, parse(str(w["match"]))):
                errs.append(f"wrong answer '{w['match']}' is actually equivalent to the reference")
    elif a["kind"] == "number":
        tol = max(a.get("tolerance", 0), 1e-9)
        for w in p["wrong"]:
            if abs(float(parse(str(w["match"]))) - a["value"]) <= tol:
                errs.append(f"wrong answer '{w['match']}' equals the correct value")
    elif a["kind"] == "set":
        for w in p["wrong"]:
            if float(parse(str(w["match"]))) in a["values"]:
                errs.append(f"wrong answer '{w['match']}' is one of the correct values")
    elif a["kind"] == "rational":
        e2, w2 = check_rational(a, p["wrong"])
        errs += e2
        warns += w2
    elif a["kind"] == "antiderivative":
        errs += check_antiderivative(a, p["wrong"])
    elif a["kind"] == "periodic":
        errs += check_periodic(a, p["wrong"])
        if p["wrong"]:
            warns.append("wrong answers of a periodic answer are matched as text, not checked")
    else:  # interval
        errs += check_interval(a, p["wrong"])
    for w in p["wrong"]:
        if w["misconception"] and w["misconception"] not in topics:
            errs.append(f"unknown misconception {w['misconception']} in wrong list")
    if not any(w["misconception"] == tid for w in p["wrong"]):
        errs.append(f"no wrong answer is tagged with the topic misconception {tid}")
    return errs, warns


def check_ES(it, tid, topics):
    errs = []
    lines, e = it["payload"]["lines"], it["payload"]["error_line"]
    if e > len(lines):
        return [f"error_line {e} is beyond the last line ({len(lines)})"], []
    for i in range(1, e - 1):
        if not same(lines[0], lines[i]):
            errs.append(f"line {i + 1} is not equivalent to line 1 but comes before the error line")
    if same(lines[e - 2], lines[e - 1]):
        errs.append(f"line {e} is equivalent to line {e - 1}: no error was injected")
    return errs, []


def check_SO(it, tid, topics):
    errs = []
    p = it["payload"]
    lines = p["lines"]
    if len(set(lines)) != len(lines):
        errs.append("two lines are identical")
    for i in range(1, len(lines)):
        if not same(lines[0], lines[i]):
            errs.append(f"line {i + 1} is not equivalent to line 1")
    if p["accept"] == "dependency":
        deps = p.get("dependencies")
        if not deps:
            errs.append("accept = dependency needs a dependencies list")
        else:
            for a, b in deps:
                if a > len(lines) or b > len(lines):
                    errs.append(f"dependency ({a}, {b}) points beyond the last line")
    return errs, []


def check_FS(it, tid, topics):
    errs = []
    p = it["payload"]
    lines, b, ans = p["lines"], p["blank_index"], p["answer"]
    if b > len(lines):
        return [f"blank_index {b} is beyond the last line"], []
    for i in range(1, len(lines)):
        if not same(lines[0], lines[i]):
            errs.append(f"line {i + 1} is not equivalent to line 1")
    if ans["kind"] == "expression":
        if not same(ans["reference"], lines[b - 1]):
            errs.append("answer.reference is not equivalent to the blanked line")
        problem = finite_at(parse(ans["reference"]), ans["variables"], ans["samples"])
        if problem:
            errs.append(problem)
    else:
        kind, e = parse_line(ans["reference"])
        if kind == "ex":
            errs.append("answer kind 'equation' needs an equation or inequality")
        elif solset(kind, e) != sp.FiniteSet(*[sp.nsimplify(x) for x in ans["solutions"]]):
            errs.append("answer.solutions does not match the solution set of answer.reference")
        if not same(ans["reference"], lines[b - 1]):
            errs.append("answer.reference is not equivalent to the blanked line")
        for alt in ans.get("equivalents", []):
            if not same(alt, ans["reference"]):
                errs.append(f"equivalent '{alt}' is not equivalent to the reference")
    return errs, []


def check_ME(it, tid, topics):
    errs = []
    p = it["payload"]
    ref = parse(p["reference"])
    problem = finite_at(ref, p["variables"], p["samples"])
    if problem:
        errs.append(problem)
    flags = []
    for o in p["options"]:
        actual = numeric_equal(ref, parse(o["text"]))
        flags.append(actual)
        if actual != o["equivalent"]:
            errs.append(f"option {o['id']} '{o['text']}': equivalent flag is {o['equivalent']} but the algebra says {actual}")
        if o["equivalent"] and o["misconception"] is not None:
            errs.append(f"option {o['id']} is equivalent but carries a misconception tag")
        if o["misconception"] and o["misconception"] not in topics:
            errs.append(f"option {o['id']}: unknown misconception {o['misconception']}")
    if all(flags) or not any(flags):
        errs.append("options must include at least one equivalent and one non-equivalent expression")
    if not any(o["misconception"] == tid for o in p["options"] if not o["equivalent"]):
        errs.append(f"no non-equivalent option is tagged with the topic misconception {tid}")
    return errs, []


def check_RP(it, tid, topics):
    errs = []
    p = it["payload"]
    target = sp.FiniteSet(sp.nsimplify(p["constraint"]["value"]))
    for label, wanted in (("valid", True), ("invalid", False)):
        for line in p["checks"][label]:
            kind, e = parse_line(line)
            if kind != "eq":
                errs.append(f"checks.{label} entry '{line}' is not an equation")
            elif (solset(kind, e) == target) != wanted:
                errs.append(f"checks.{label} entry '{line}' does not behave as {label} for the constraint")
    return errs, []


CHECKERS = {"MC": check_MC, "NE": check_NE, "ES": check_ES, "SO": check_SO,
            "FS": check_FS, "ME": check_ME, "RP": check_RP}


# ------------------------------------------------------------- item level
def verify_item(item, tid, code, ctx):
    errs, warns = [], []
    schema_errs = sorted(ctx["validator"].iter_errors(item), key=lambda e: list(e.path))
    if schema_errs:
        for e in schema_errs[:6]:
            errs.append(f"schema: {'/'.join(str(x) for x in e.path) or '(item)'}: {e.message[:160]}")
        return errs, warns

    if not item["id"].startswith(f"{ID_PREFIX}{tid}-{code}-"):
        errs.append(f"id {item['id']} does not match file {tid}/{code}.json")
    if item["type"] != code:
        errs.append(f"type {item['type']} does not match file name {code}.json")
    if tid not in item["misconceptions"]:
        errs.append(f"misconceptions must include the topic id {tid}")
    for m in item["misconceptions"]:
        if m not in ctx["known"]:
            errs.append(f"unknown misconception id {m}")
    if len(item["id"].encode()) > 48:
        errs.append("id is too long for a Telegram callback_data payload")
    if not item["provenance"]["verified"]:
        errs.append("provenance.verified is false: only code-verified items may be committed")

    row = ctx["topics"].get(tid)
    if row:
        cur = item["curriculum"]
        syl = cur["syllabus"]
        allowed = {row["main"], *row["also"]}
        if syl not in row["syllabus"]:
            errs.append(f"syllabus {syl} is not listed for topic {tid} (allowed: {row['syllabus']})")
        for g in cur["lops"]:
            if g not in allowed:
                errs.append(f"goal {g} is not linked to topic {tid} in the backlog (allowed: {sorted(allowed)})")
            if g in ctx["retired"]:
                errs.append(f"goal {g} is retired in the LOPS file")
            elif ctx["goals"] and g not in ctx["goals"]:
                errs.append(f"goal {g} does not exist in the LOPS file")
            if goal_syllabus(g) not in ("MAY", syl):
                errs.append(f"goal {g} belongs to the other syllabus than {syl}")
        if goal_syllabus(row["main"]) in ("MAY", syl) and row["main"] not in cur["lops"]:
            errs.append(f"curriculum.lops must include the main goal {row['main']} for a {syl} item")
        for g in cur["g"]:
            if g not in row["g"]:
                errs.append(f"G-goal {g} is not linked to topic {tid} (allowed: {row['g']})")
            if ctx["g_ids"] and g not in ctx["g_ids"]:
                errs.append(f"G-goal {g} does not exist in the LOPS file")

    tmpl = ROOT / "generators" / f"{item['provenance']['template']}.py"
    if not tmpl.exists():
        warns.append(f"generator generators/{tmpl.name} not found (template not reproducible)")

    if code in CHECKERS:
        try:
            e2, w2 = CHECKERS[code](item, tid, ctx["known"])
            errs += e2
            warns += w2
        except Unsupported as exc:
            warns.append(f"algebra not checked: {exc}")
    else:
        warns.append(f"type {code}: structural check only")
    return errs, warns


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def run_git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def check_base(ref, exdir, current):
    errs, warns = [], []
    probe = run_git("rev-parse", "--verify", "--quiet", ref)
    if probe.returncode != 0:
        return errs, [f"--base {ref}: ref not found, immutability check skipped"]
    listing = run_git("ls-tree", "-r", "--name-only", ref, "--", "exercises")
    for rel in [x for x in listing.stdout.splitlines() if x.endswith(".json")]:
        shown = run_git("show", f"{ref}:./{rel}")
        if shown.returncode != 0:
            continue
        base_items = {i["id"]: i for i in json.loads(shown.stdout)["items"]}
        cur_items = current.get(rel)
        if cur_items is None:
            errs.append(f"{rel}: file existed at {ref} but is gone now")
            continue
        for iid, old in base_items.items():
            if iid not in cur_items:
                errs.append(f"{rel}: item {iid} was removed")
            elif cur_items[iid] != old:
                errs.append(f"{rel}: existing item {iid} was modified")
    for rel, items in current.items():
        shown = run_git("show", f"{ref}:./{rel}")
        known = set()
        if shown.returncode == 0:
            known = {i["id"] for i in json.loads(shown.stdout)["items"]}
        for iid, it in items.items():
            if iid not in known and it.get("status") != "draft":
                errs.append(f"{rel}: new item {iid} has status '{it.get('status')}', must be draft")
    return errs, warns


def check_backlog(exdir, text, files_with_items):
    errs = []
    codes, rows = parse_matrix(text)
    if not rows:
        return ["could not find the coverage matrix in the backlog"]
    for tid, cells in rows.items():
        for code in codes:
            has = (tid, code) in files_with_items
            val = cells.get(code, "-")
            if val == "X" and not has:
                errs.append(f"backlog marks {tid} {code} as X but no items exist")
            if val != "X" and has:
                errs.append(f"{tid}/{code}.json has items but the backlog cell is '{val}' (expected X)")
    for tid, code in files_with_items:
        if tid not in rows:
            errs.append(f"{tid}/{code}.json: topic is not in the backlog matrix")
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exercises", default=str(ROOT / "exercises"), help="folder with <Topic>/<Type>.json")
    ap.add_argument("--backlog", default=str(ROOT / BACKLOG))
    ap.add_argument("--lops", default=str(ROOT / LOPS_FILE), help="LOPS 2019 goal file")
    ap.add_argument("--catalogue", default=str(ROOT / CATALOGUE), help="lukio misconception catalogue")
    ap.add_argument("--base", help="git ref; existing items must be unchanged, new ones draft")
    ap.add_argument("--check-backlog", action="store_true", help="matrix cells must match the files")
    args = ap.parse_args()

    exdir = Path(args.exercises)
    backlog_path = Path(args.backlog)
    if not backlog_path.exists():
        sys.exit(f"VERIFY FAILED: backlog not found at {backlog_path}")
    backlog_text = backlog_path.read_text(encoding="utf-8")
    topics = parse_topics(backlog_text)
    if not topics:
        sys.exit("VERIFY FAILED: could not read the topic table from the backlog")
    lops_path = Path(args.lops)
    if not lops_path.exists():
        sys.exit(f"VERIFY FAILED: LOPS goal file not found at {lops_path}")
    goals, retired, g_ids = parse_lops(lops_path.read_text(encoding="utf-8"))
    if not goals:
        sys.exit("VERIFY FAILED: could not read goal IDs from the LOPS file")
    warnings = []
    known = set(topics)
    cat_path = Path(args.catalogue)
    if cat_path.exists():
        known |= parse_catalogue(cat_path.read_text(encoding="utf-8"))
    else:
        warnings.append("misconception catalogue not found: only backlog topic IDs are known")
    errors = []
    for tid, row in topics.items():
        for g in [row["main"], *row["also"]]:
            if g in retired or g not in goals:
                errors.append(f"backlog topic {tid}: goal {g} is {'retired' if g in retired else 'not'} in the LOPS file")
    schema = load_json(ROOT / "schema" / "item.schema.json")
    ctx = {"topics": topics, "known": known, "goals": goals, "retired": retired, "g_ids": g_ids,
           "validator": Draft202012Validator(schema)}

    current, with_items, n_items = {}, set(), 0
    for path in sorted(exdir.glob("*/*.json")):
        tid, code = path.parent.name, path.stem
        label = f"{tid}/{code}.json"
        if code not in TYPE_CODES:
            errors.append(f"{label}: unknown type code")
            continue
        if tid not in topics:
            errors.append(f"{label}: topic is not in the backlog")
        try:
            doc = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: invalid JSON ({exc})")
            continue
        if not isinstance(doc, dict) or set(doc) != {"schema_version", "topic", "type", "items"}:
            errors.append(f"{label}: wrapper must have exactly schema_version, topic, type, items")
            continue
        if doc["schema_version"] != SCHEMA_VERSION or doc["topic"] != tid or doc["type"] != code:
            errors.append(f"{label}: wrapper values do not match the path")
        if not doc["items"]:
            errors.append(f"{label}: empty items list (delete the file instead)")
            continue
        seen, prompts, nums = set(), set(), []
        for item in doc["items"]:
            iid = item.get("id", "?") if isinstance(item, dict) else "?"
            if iid in seen:
                errors.append(f"{label}: duplicate id {iid}")
            seen.add(iid)
            e, w = verify_item(item, tid, code, ctx)
            errors += [f"{label} {iid}: {m}" for m in e]
            warnings += [f"{label} {iid}: {m}" for m in w]
            key = json.dumps([item.get("prompt"), item.get("payload")], sort_keys=True)
            if key in prompts:
                errors.append(f"{label} {iid}: identical to another item in the file")
            prompts.add(key)
            m = re.search(r"-(\d{3})$", iid)
            if m:
                nums.append(int(m.group(1)))
        if nums and sorted(nums) != list(range(1, max(nums) + 1)):
            warnings.append(f"{label}: item numbers have gaps: {sorted(nums)}")
        n_items += len(doc["items"])
        current[f"exercises/{tid}/{code}.json"] = {i["id"]: i for i in doc["items"] if isinstance(i, dict) and "id" in i}
        with_items.add((tid, code))

    if args.base and Path(exdir).resolve() == (ROOT / "exercises").resolve():
        e, w = check_base(args.base, exdir, current)
        errors += e
        warnings += w
    if args.check_backlog:
        errors += check_backlog(exdir, backlog_text, with_items)

    uniq = list(dict.fromkeys(warnings))
    for w in uniq:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"VERIFY FAILED: {len(errors)} error(s), {len(uniq)} warning(s)")
        sys.exit(1)
    print(f"VERIFY OK: {n_items} item(s) in {len(with_items)} file(s), {len(uniq)} warning(s)")


if __name__ == "__main__":
    main()
