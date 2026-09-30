# Exercise pipeline (grades 1–6)

> **EXPERT REVIEW REQUIRED BEFORE USE WITH PUPILS. NOT LEGAL ADVICE.** Content preparation with synthetic data only. See `EXPERT_REVIEW_REQUIRED.md`.

| File | Purpose |
|---|---|
| `verify_items.py` | Checks every item: answer key recomputed from `answer_expr`, goal id exists, level fits the grade band, decimal comma, wrong answers differ from the right one, status is `draft`, no personal data fields, no duplicates |
| `from_buggy_rules.py` | Writes a batch from the `tools/buggy_rules` templates (subtraction, fraction addition, unit-fraction comparison) |
| `test_verify_items.py` | 14 tests |

From the repository root:

```bash
python -m unittest discover -s tools/exercise_pipeline
python tools/exercise_pipeline/from_buggy_rules.py --n 12 --seed 20261001 --stamp 20261001 \
    --out exercises/grades1-6/batch-20261001-0600.json
python tools/exercise_pipeline/verify_items.py "exercises/grades1-6/*.json"
```

`from_buggy_rules.py` skips any stem that already exists in `exercises/grades1-6/*.json` (change with `--avoid-glob`), so a later batch never repeats an earlier task.

`answer_expr` accepts numbers with `+ - * /` and `**` (exponent 0–6). Nothing else is evaluated, so a malformed or hostile expression is rejected, not run.

Limits: the verifier checks arithmetic, format and safety. It cannot judge whether a task is good teaching, clear for a seven-year-old, or free of a second reading. A teacher must review every item.
