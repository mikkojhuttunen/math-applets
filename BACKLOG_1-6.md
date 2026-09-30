# Backlog: exercises for grades 1–6

> **EXPERT REVIEW REQUIRED BEFORE USE WITH PUPILS.** This backlog is for preparing exercise content with synthetic data only. See `EXPERT_REVIEW_REQUIRED.md`.

An automated run takes the first row whose status is `todo` or `in progress` and whose `have` is below `target`, and adds at most 20 items. `hold` rows are never touched. Statuses are changed by a human, except that a run may change `todo` to `in progress` and `in progress` to `done`, and update `have`.

| # | Goal | Item bank id | Type and how it is checked | Target | Have | Status | Notes |
|---|---|---|---|---|---|---|---|
| 1 | A36.S2.04 | NUM-10 | numeric_entry, `from_buggy_rules.py` (template `sub_multidigit_v1`) | 40 | 4 | in progress | Use only items where `is_diagnostic_subtraction` holds. Wrong answers NUM-10a/b/c. |
| 2 | A36.S2.12 | NUM-03 | numeric_entry, `from_buggy_rules.py` (template `frac_add_v1`) | 40 | 4 | in progress | Answer as a fraction. |
| 3 | A36.S2.11 | NUM-12 | choice, `from_buggy_rules.py` (template `frac_compare_unit_v1`) | 20 | 4 | in progress | Choice items overstate errors; keep for quick checks. |
| 4 | A12.S2.08 | ALG-06, ALG-13 | numeric_entry with `answer_expr`, or choice true/false | 30 | 0 | todo | For example `8 + 4 = □ + 5` (answer 7, expr `8 + 4 - 5`); `8 = 5 + 3` true or false. |
| 5 | A12.S2.06 | NUM-09 | numeric_entry with `answer_expr` | 30 | 0 | todo | Value of a digit in a number, for example 706 gives 700 (expr `7 * 100`). |
| 6 | A36.S2.01 | NUM-13 | numeric_entry with `answer_expr` | 20 | 0 | todo | Multiplying by 10 with decimals, for example `3,5 × 10` gives 35. Wrong answer 3,50. |
| 7 | A36.S2.14 | NUM-11 | numeric_entry with `answer_expr` | 20 | 0 | todo | Multiplier below 1, for example price of 0,5 m at 4 € per m. Wrong answer from division. |
| 8 | A36.S4.09 | MEA-01 | numeric_entry with `answer_expr` | 20 | 0 | todo | Covering a rectangle with unit squares, rows times columns. Wrong answer from adding. |
| 9 | A12.S2.08 | none | numeric_entry with `answer_expr` | 60 | 0 | todo | Addition and subtraction within 20, no misconception tags. |
| 10 | A12.S2.09 | none | numeric_entry with `answer_expr` | 60 | 0 | todo | Addition and subtraction within 100. |
| 11 | A12.S2.12 | none | numeric_entry with `answer_expr` | 60 | 0 | todo | Multiplication tables 1–5 and 10. |
| 12 | A36.S4.04 | GEO-03 | choice | 10 | 0 | hold | Evidence Limited in the item bank. A human decides whether to proceed. |
| 13 | A36.S4.11 | MEA-02 | numeric_entry with `answer_expr` | 10 | 0 | hold | No study found for the misconception. Do not generate until a human decides. |
