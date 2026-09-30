"""Deterministic checks for generated grades 1-6 exercise items. Standard library only.

Usage:
    python tools/exercise_pipeline/verify_items.py exercises/grades1-6/*.json
Exit code 0 = every item passed, 1 = at least one problem.

Why this exists: an LLM must never be the judge of its own answer key. Every item carries
an `answer_expr` that code evaluates, and the answer has to match it exactly.

The checker also blocks anything that looks like pupil data. Exercises are content only.
EXPERT REVIEW REQUIRED before any pupil uses them: see EXPERT_REVIEW_REQUIRED.md.
"""
from __future__ import annotations

import ast
import glob
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "buggy_rules"))
from buggy_rules import parse_answer  # noqa: E402

DEFAULT_OPS = os.path.join(HERE, "..", "..", "data", "curriculum", "OPS_1-6_oppimistavoitteet.md")

ALLOWED_KEYS = {"id", "goal", "level", "type", "stem_fi", "answer", "answer_expr", "options",
                "misconceptions", "workbook", "source", "status", "notes"}
REQUIRED_KEYS = {"id", "goal", "level", "type", "stem_fi", "answer", "source", "status"}
TYPES = {"numeric_entry", "choice"}
LEVELS = {"A36": {"P", "T", "H", "K"}, "A12": {"V", "S"}}
TAG = re.compile(r"^[A-Z]{3}-\d{2}[a-z]?$")
GOAL = re.compile(r"\bA(?:12|36)\.S\d\.\d{2}\b")
DECIMAL_POINT = re.compile(r"(?<![\d/.])\d+\.\d+(?![\d/.])")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
HETU = re.compile(r"\b\d{6}[-+A-FU-Y]\d{3}[0-9A-Y]\b")
URL = re.compile(r"https?://", re.I)


# ---------------------------------------------------------------- safe arithmetic
def eval_expr(expr: str) -> Fraction:
    """Evaluate + - * / ** on numbers only. Anything else raises ValueError."""
    if len(expr) > 200:
        raise ValueError("expression too long")

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            return Fraction(str(n.value))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add):
                return a + b
            if isinstance(n.op, ast.Sub):
                return a - b
            if isinstance(n.op, ast.Mult):
                return a * b
            if isinstance(n.op, ast.Div):
                if b == 0:
                    raise ValueError("division by zero")
                return a / b
            if isinstance(n.op, ast.Pow) and b.denominator == 1 and 0 <= b <= 6:
                return a ** int(b)
        raise ValueError("expression uses something other than plain arithmetic")

    try:
        return ev(ast.parse(expr.strip(), mode="eval"))
    except SyntaxError as e:
        raise ValueError(f"cannot parse expression: {e.msg}") from e


def load_goals(ops_path: str = DEFAULT_OPS) -> set[str]:
    with open(ops_path, encoding="utf-8") as f:
        return set(GOAL.findall(f.read()))


# ---------------------------------------------------------------- checks
def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


def check_item(item: dict, goals: set[str], allow_reviewed: bool = False) -> list[str]:
    """Return a list of problems (empty list = item passes)."""
    p: list[str] = []
    if not isinstance(item, dict):
        return ["item is not an object"]
    extra = set(item) - ALLOWED_KEYS
    if extra:
        p.append(f"unknown fields (only content fields are allowed): {sorted(extra)}")
    missing = REQUIRED_KEYS - set(item)
    if missing:
        p.append(f"missing fields: {sorted(missing)}")
        return p
    if item["type"] not in TYPES:
        p.append(f"type must be one of {sorted(TYPES)}")
    goal = item["goal"]
    if goal not in goals:
        p.append(f"goal {goal!r} is not in the OPS_1-6 file")
    else:
        if item["level"] not in LEVELS[goal[:3]]:
            p.append(f"level {item['level']!r} not valid for {goal[:3]} (allowed {sorted(LEVELS[goal[:3]])})")
    if item["status"] != "draft" and not allow_reviewed:
        p.append("status must be 'draft'; only a human reviewer sets 'reviewed'")
    if item["source"] not in {"generated", "template", "human"}:
        p.append("source must be generated, template or human")
    stem = item["stem_fi"]
    if not isinstance(stem, str) or not stem.strip() or len(stem) > 400:
        p.append("stem_fi must be a non-empty string of at most 400 characters")
    else:
        if DECIMAL_POINT.search(stem):
            p.append("stem uses a decimal point; use a decimal comma")
    for s in _strings(item):
        if EMAIL.search(s) or HETU.search(s) or URL.search(s):
            p.append("text contains an email address, personal identity code or link")
            break
    for t in item.get("workbook", []):
        if not TAG.match(t):
            p.append(f"workbook id {t!r} is not like NUM-10")

    correct = None
    if item["type"] == "numeric_entry":
        expr = item.get("answer_expr")
        if not expr:
            p.append("numeric_entry needs answer_expr")
        else:
            try:
                value = eval_expr(expr)
                correct = parse_answer(item["answer"])
                if correct is None:
                    p.append(f"answer {item['answer']!r} cannot be read as a number")
                elif correct != value:
                    p.append(f"answer {item['answer']!r} does not equal answer_expr {expr!r} = {value}")
            except ValueError as e:
                p.append(f"answer_expr problem: {e}")
    elif item["type"] == "choice":
        opts = item.get("options")
        if not isinstance(opts, list) or len(opts) < 2 or len(set(opts)) != len(opts):
            p.append("choice needs at least two different options")
        elif item["answer"] not in opts:
            p.append("answer is not one of the options")

    for tag, m in (item.get("misconceptions") or {}).items():
        if not TAG.match(tag):
            p.append(f"misconception tag {tag!r} is not like NUM-10a")
            continue
        if not isinstance(m, dict) or "answer" not in m:
            p.append(f"misconception {tag} needs an answer")
            continue
        if item["type"] == "choice":
            if m["answer"] not in (item.get("options") or []) or m["answer"] == item["answer"]:
                p.append(f"misconception {tag}: wrong answer must be a different option")
        else:
            wrong = parse_answer(m["answer"])
            if wrong is None:
                p.append(f"misconception {tag}: answer cannot be read as a number")
            elif correct is not None and wrong == correct:
                p.append(f"misconception {tag}: wrong answer equals the correct answer")
            if m.get("answer_expr"):
                try:
                    if wrong is not None and eval_expr(m["answer_expr"]) != wrong:
                        p.append(f"misconception {tag}: answer does not equal its answer_expr")
                except ValueError as e:
                    p.append(f"misconception {tag}: answer_expr problem: {e}")
    return p


def check_files(paths: list[str], goals: set[str], allow_reviewed: bool = False) -> dict[str, list[str]]:
    problems: dict[str, list[str]] = {}
    seen_ids: dict[str, str] = {}
    seen_stems: dict[str, str] = {}
    for path in paths:
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            problems[path] = [f"cannot read file: {e}"]
            continue
        if not isinstance(data, list):
            problems[path] = ["file must contain a JSON array of items"]
            continue
        for i, item in enumerate(data):
            label = f"{path}[{i}] {item.get('id', '?') if isinstance(item, dict) else '?'}"
            errs = check_item(item, goals, allow_reviewed)
            if isinstance(item, dict) and "id" in item:
                if item["id"] in seen_ids:
                    errs.append(f"duplicate id (also in {seen_ids[item['id']]})")
                seen_ids[item["id"]] = path
                stem = re.sub(r"\s+", " ", str(item.get("stem_fi", ""))).strip().lower()
                if stem in seen_stems and seen_stems[stem] != item["id"]:
                    errs.append(f"duplicate stem (also {seen_stems[stem]})")
                seen_stems[stem] = item["id"]
            if errs:
                problems[label] = errs
    return problems


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    allow_reviewed = "--allow-reviewed" in argv
    ops = DEFAULT_OPS
    for a in argv:
        if a.startswith("--ops="):
            ops = a.split("=", 1)[1]
    paths = sorted({p for a in args for p in (glob.glob(a) or [a])})
    if not paths:
        print("no files given")
        return 1
    problems = check_files(paths, load_goals(ops), allow_reviewed)
    for label, errs in problems.items():
        print(f"FAIL {label}")
        for e in errs:
            print(f"     - {e}")
    print(f"{len(paths)} file(s) checked; {'no problems' if not problems else str(len(problems)) + ' item(s)/file(s) with problems'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
