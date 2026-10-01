# Backlog: exercises for grades 1–6

> **EXPERT REVIEW REQUIRED BEFORE USE WITH PUPILS.** This backlog is for preparing exercise content with synthetic data only. See `EXPERT_REVIEW_REQUIRED.md`.

An automated run takes the first row whose status is `todo` or `in progress` and whose `have` is below `target`, and adds at most 20 items. `hold` rows are never touched. Statuses are changed by a human, except that a run may change `todo` to `in progress` and `in progress` to `done`, and update `have`.

| # | Goal | Item bank id | Type and how it is checked | Target | Have | Status | Notes |
|---|---|---|---|---|---|---|---|
| 1 | A36.S2.04 | NUM-10 | numeric_entry, `from_buggy_rules.py` (template `sub_multidigit_v1`) | 40 | 40 | done | Use only items where `is_diagnostic_subtraction` holds. Wrong answers NUM-10a/b/c. |
| 2 | A36.S2.12 | NUM-03 | numeric_entry, `from_buggy_rules.py` (template `frac_add_v1`) | 40 | 40 | done | Answer as a fraction. |
| 3 | A36.S2.11 | NUM-12 | choice, `from_buggy_rules.py` (template `frac_compare_unit_v1`) | 20 | 20 | done | Choice items overstate errors; keep for quick checks. |
| 4 | A12.S2.08 | ALG-06, ALG-13 | numeric_entry with `answer_expr`, or choice true/false | 30 | 30 | done | For example `8 + 4 = □ + 5` (answer 7, expr `8 + 4 - 5`); `8 = 5 + 3` true or false. |
| 5 | A12.S2.06 | NUM-09 | numeric_entry with `answer_expr` | 30 | 30 | done | Value of a digit in a number, for example 706 gives 700 (expr `7 * 100`). |
| 6 | A36.S2.01 | NUM-13 | numeric_entry with `answer_expr` | 20 | 20 | done | Multiplying by 10 with decimals, for example `3,5 × 10` gives 35. Wrong answer 3,50. |
| 7 | A36.S2.14 | NUM-11 | numeric_entry with `answer_expr` | 20 | 20 | done | Multiplier below 1, for example price of 0,5 m at 4 € per m. Wrong answer from division. |
| 8 | A36.S4.09 | MEA-01 | numeric_entry with `answer_expr` | 20 | 20 | done | Covering a rectangle with unit squares, rows times columns. Wrong answer from adding. |
| 9 | A12.S2.08 | none | numeric_entry with `answer_expr` | 60 | 60 | done | Addition and subtraction within 20, no misconception tags. |
| 10 | A12.S2.09 | none | numeric_entry with `answer_expr` | 60 | 60 | done | Addition and subtraction within 100. |
| 11 | A12.S2.12 | none | numeric_entry with `answer_expr` | 60 | 60 | done | Multiplication tables 1–5 and 10. |
| 12 | A36.S4.04 | GEO-03 | choice | 10 | 0 | hold | Evidence Limited in the item bank. A human decides whether to proceed. |
| 13 | A36.S4.11 | MEA-02 | numeric_entry with `answer_expr` | 10 | 0 | hold | No study found for the misconception. Do not generate until a human decides. |

## Revisions requested by the teacher (manual session, not for the routine)

The routine never edits existing batch files. These reviewed items match the language rules in `ROUTINE_PROMPT_1-6.md` (section **Language and style**, from the review of 2026-10-01) and should be revised in a manual session after the teacher confirms the wording. Suggestions follow the teacher's own corrections; change only `stem_fi`.

| Item | Now | Suggestion | Rule |
|---|---|---|---|
| A12.S2.08-add20-20261001-0721-012 | Hänen veljensä uimasi 6 minuuttia vähemmän. | Hänen veljensä ui 6 minuuttia vähemmän. | verb form (error) |
| A12.S2.09-addsub100-20261001-0820-012 | Lainaan lähti 37 kirjaa. | Kirjastosta lainattiin 37 kirjaa. | wording |
| A12.S2.12-kertotaulu-20261001-1122-011 | Pöydässä on 3 lautasta. … Montako omenaa on yhteensä? | Pöydällä on 3 lautasta. … Montako omenaa lautasilla on yhteensä? | place, question |
| A12.S2.12-kertotaulu-20261001-1122-012 | Montako pullaa on yhteensä? | Montako pullaa pusseissa on yhteensä? | question |
| A12.S2.12-kertotaulu-20261001-1122-015 | Aino piirtää 3 riviä tähtiä. | Aino piirtää tähtiä kolmeen riviin. | rows |
| A12.S2.12-kertotaulu-20261001-1122-018 | Kukkamaassa on 2 riviä tulppaaneja. … Montako tulppaania on yhteensä? | Kukkamaassa on tulppaaneja kahdessa rivissä. Kummassakin rivissä on 8 tulppaania. Montako tulppaania kukkamaassa on yhteensä? | rows, question |
| A12.S2.12-kertotaulu-20261001-1122-019 | Montako sivua hän lukee 6 päivässä? | Montako sivua hän on lukenut 6 päivässä? | tense |
| A12.S2.12-kertotaulu-20261001-1122-020 | Montako tarraa on yhteensä? | Montako tarraa vihkossa on yhteensä? | question |
| A12.S2.12-kertotaulu-20261001-1322-014 | Sanni jakaa pöydälle 7 lautasta. Jokaiselle tulee 2 korttia. | Sanni laittaa pöydälle 7 lautasta ja jokaiselle lautaselle 2 korttia. | unclear |
| A12.S2.12-kertotaulu-20261001-1322-017 | Montako purkkia on yhteensä? | Montako purkkia hyllyillä on yhteensä? | question |
| A12.S2.12-kertotaulu-20261001-1322-018 | Oskari tekee 4 pinoa kortteja. … Montako korttia on yhteensä? | Oskari tekee korteista neljä pinoa. … Montako korttia pinoissa on yhteensä? | rows, question |
| A12.S2.12-kertotaulu-20261001-1322-020 | Montako lintua on yhteensä? | Montako lintua oksilla on yhteensä? | question |
| A12.S2.08-add20-20261001-0721-018 | Montako nallea on yhteensä? | Montako nallea tuolilla ja hyllyllä on yhteensä? | question |
| A36.S4.09-cover-20261001-0421-001 | Ruutuja on 3 riviä, … Montako ruutua on yhteensä? | Ruudut ovat kolmessa rivissä, … Montako ruutua suorakulmion peittämiseen tarvitaan? | rows, question |
| A36.S4.09-cover-20261001-0421-002 | Laattoja on 4 riviä, | Laatat ovat neljässä rivissä, | rows |
| A36.S4.09-cover-20261001-0421-005 | Ruutuja on 6 riviä | Ruudut ovat kuudessa rivissä, | rows |
| A36.S4.09-cover-20261001-0421-006 | Montako kolon paikkaa kennossa on? | Montako koloa kennossa on? | wording |
| A36.S4.09-cover-20261001-0421-018 | Montako ruutua on yhteensä? | Montako ruutua suorakulmion peittämiseen tarvitaan? | question |
| A36.S4.09-cover-20261001-0421-019 | Ruutuja on 15 riviä | Ruudut ovat 15 rivissä, | rows |

Items the teacher already corrected on 2026-10-01 (for reference): 0921-018, 1122-012, 1122-014, 1222-013, 1222-016, 1222-018, 1222-019, 1322-013, 1322-015 (batch ids `A12.S2.09-addsub100-20261001-…` and `A12.S2.12-kertotaulu-20261001-…`).
