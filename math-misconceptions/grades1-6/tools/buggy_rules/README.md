# Buggy rules (grades 1–6)

> **EXPERT REVIEW REQUIRED BEFORE USE WITH PUPILS. NOT LEGAL ADVICE.** Content preparation with synthetic data only. The per-pupil `Tally` class stays disabled until the sign-off in `docs/privacy/expert_review_signoff_template.md` is complete. See `EXPERT_REVIEW_REQUIRED.md`.

`buggy_rules.py` models documented misconceptions as procedures, so the wrong answer a misconception produces is computed by code, not guessed. Standard library only.

## Rules

| Id | Rule | Item bank row |
|---|---|---|
| `NUM-10a` | Smaller digit subtracted from larger; no regrouping | NUM-10 |
| `NUM-10b` | Smaller from larger, and the next digit is also reduced by one | NUM-10 |
| `NUM-10c` | Regrouping done in the column, but the next digit is not reduced | NUM-10 |
| `NUM-03` | Numerators and denominators added separately | NUM-03 |
| `NUM-12` | Larger denominator taken as the larger fraction | NUM-12 |

The three NUM-10 variants follow Vermeulen et al. (2020). Example: 453 − 127 gives 326 correctly, 334 (a), 324 (b) and 336 (c).

## Templates

| Template | Function | Type | Goal |
|---|---|---|---|
| `sub_multidigit_v1` | `make_subtraction_item(rng, ndig_m, ndig_s)` | numeric_entry | A36.S2.04 |
| `sub_multidigit_err_v1` | `make_subtraction_error_item(m, s, rule)` | error_spotting | A36.S2.04 |
| `frac_add_v1` | `make_fraction_add_item(rng)` | numeric_entry | A36.S2.12 |
| `frac_add_err_v1` | `make_fraction_add_error_item(rng)` | error_spotting | A36.S2.12 |
| `frac_compare_unit_v1` | `make_fraction_compare_item(rng)` | choice | A36.S2.11 |

`tools/exercise_pipeline/from_buggy_rules.py` uses the three numeric_entry and choice templates. The error-spotting templates are not in the item schema of `exercises/grades1-6/README.md` yet, so the verifier rejects them.

**Subtraction items are diagnostic.** `is_diagnostic_subtraction(m, s)` accepts a pair only if it needs at least one regrouping, the subtrahend does not end in 8 or 9 (these invite compensation), the difference is over 10 (avoids adding up), and the correct answer and the three bug answers are all different. `make_subtraction_item` draws until a pair passes.

**Fraction addition** uses different denominators 2–9, keeps the correct sum below 2, and skips pairs where the bug answer happens to be correct.

**Unit-fraction comparison** is a choice item. Multiple-choice distractors raise error rates, so keep these for quick checks, not diagnosis.

## Checking answers

- `parse_answer(text)` reads `7`, `5/6`, `1 1/6`, `0,5`, `0.5` and the minus sign U+2212. Equivalent forms compare equal (`10/12` equals `5/6`). Returns `None` if unreadable.
- `classify(item, answer)` returns `correct`, `matched` (one rule explains the answer), `ambiguous` (several rules do), `unexplained` or `unparsed`.
- `check_tap(item, line)` scores an error-spotting tap and says whether it fell before or after the faulty line.
- `Tally(min_items=2)` flags a rule only when it explains wrong answers on at least two different items, because bugs are unstable (Hennessy, 1993). **It is a profile of a child: keep it off for real pupils until sign-off.**

## Run

From the pipeline root (`math-misconceptions/grades1-6/`):

```bash
python tools/buggy_rules/buggy_rules.py
```

prints a demo set of every template as JSON.

Limits: the rules reproduce answers described in the literature. They do not show that a pupil who gives such an answer holds the misconception, and they cover only the five rules above. A teacher must review every item.
