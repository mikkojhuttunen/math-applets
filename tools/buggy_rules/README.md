# FinnMath buggy rules (grades 3–6)

> **EXPERT REVIEW REQUIRED. NOT LEGAL ADVICE.** Logging pupils' answers or keeping a per-pupil tally of misconception rules is processing of children's personal data. Until the sign-off in `docs/privacy/expert_review_signoff_template.md` is complete, use this code only with synthetic data, and keep `Tally` disabled. See `EXPERT_REVIEW_REQUIRED.md`.

Generators, a classifier and error-spotting items for three misconceptions in the item bank (`math_misconceptions_item_bank.xlsx`):

| Rule id | Item bank id | What the student does | Example |
|---|---|---|---|
| NUM-10a | NUM-10 | Subtracts the smaller digit from the larger, no regrouping | 453 − 127 = 334 |
| NUM-10b | NUM-10 | Same, and also reduces the next digit by one | 453 − 127 = 324 |
| NUM-10c | NUM-10 | Regroups correctly but does not reduce the next digit | 453 − 127 = 336 |
| NUM-03 | NUM-03 | Adds numerators and denominators separately | 1/4 + 1/3 = 2/7 |
| NUM-12 | NUM-12 | Takes the larger denominator as the larger fraction | 1/8 > 1/4 |

The correct answer for 453 − 127 is 326.

## Files

- `buggy_rules.py`: everything, standard library only.
- `test_buggy_rules.py`: 18 tests. Run `python -m unittest test_buggy_rules -v`.
- `sample_items.json`: one of each item type, generated with `python buggy_rules.py`.

## How it works

**Item record.** Each generated item has `type`, `template`, `params`, the correct `answer`, the wrong answer each rule produces (`misconceptions`), and the item bank and curriculum ids (`workbook`, `curriculum`). This is the minimal record proposed in the exercise-types document.

**Classify.** `classify(item, answer)` returns `correct`, `matched` (one rule reproduces the answer), `ambiguous`, `unexplained` or `unparsed`. Answers may be `5/6`, `1 1/6`, `0,5`; equivalent fractions count as equal.

**Error spotting.** `make_subtraction_error_item` and `make_fraction_add_error_item` return a worked solution with one injected error and the faulty line index. `check_tap` returns the error tag the student missed, even for a wrong tap.

**Tally.** `Tally` flags a rule for a student only after it explains wrong answers on at least two different items.

## Design decisions and their sources

These come from Vermeulen et al. (2020), *Frontiers in Education* 5:537531, read in full (264 Dutch third-graders).

- **Three variants, not one.** The paper separates smaller-from-larger, smaller-from-larger with the next digit reduced, and regrouping without reducing the next digit. The tests reproduce its printed examples: 347 − 62 gives 325, 225 and 385; 43 − 17 gives 34, 24 and 36.
- **Item constraints.** `is_diagnostic_subtraction` requires a regrouping, a difference above 10, a subtrahend not ending in 8 or 9, and four different answers. The last rule matters: for 82 − 27 the second variant gives the correct 55, so a correct answer would not prove anything. The old item bank item 302 − 148 failed the "8 or 9" rule and was replaced by 453 − 127.
- **Typed answers for diagnosis.** In the paper, multiple-choice items produced a bridging-error rate of 0.277 against 0.115 for open items, so choice distractors overstate the error. Use `numeric_entry` to diagnose and keep `choice` items (NUM-12) for quick checks.
- **Minimum evidence.** The paper and the studies it cites (Hennessy, 1993) describe bugs as unstable. One matching answer proves little, hence `Tally(min_items=2)`. Raise it once real data exists.
- **Who to diagnose.** The paper reports, from a related unpublished study, that higher bridging-error rates went with higher mathematical ability. In its own data, the item type answered by weaker pupils (1000 − 70) drew other errors instead. An `unexplained` wrong answer is common and expected.

## Limits

- **Method.** The Finnish narration ("Lainattu kymmenen pois") assumes the regrouping ("borrowing") method. If your target schools teach another subtraction method, such as adding ten to both numbers, the variants and lines need adapting. A teacher should check the wording either way.
- **Unverified for Finland.** The variants are documented for Dutch third-graders and cited elsewhere as frequent across countries. I found no Finnish item-level data.
- **NUM-12 and the "larger numerator" rule.** Only the larger-denominator rule is implemented. The larger-numerator rule appears in a 2025 review that could not be trusted (see the Claude document).
- **Lowest terms.** `parse_answer` accepts equivalent fractions. If a task asks for lowest terms, add that check in the app.
- **Porting.** The logic is small enough to port to JavaScript. The app's expression checker (mathjs or sympy) is not needed for these item types.

## Adding a rule

1. Add the id to `RULES` and write a function that returns the wrong answer for given params.
2. Store the answer under `misconceptions` when generating the item.
3. Add a test that reproduces a published worked example, then a property test that `classify` recovers the rule.
4. Check that the wrong answer differs from the correct one for every generated item.
