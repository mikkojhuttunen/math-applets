# Generated exercises, grades 1–6

> **EXPERT REVIEW REQUIRED BEFORE USE WITH PUPILS. NOT LEGAL ADVICE.** These files are exercise *content* only. No data about pupils is stored here and none may be added. Do not put these items in front of pupils until a teacher has reviewed them and the sign-off in `docs/privacy/expert_review_signoff_template.md` is complete. See `EXPERT_REVIEW_REQUIRED.md`.

- One JSON array per file, named `batch-<date>-<time>.json`. Never edit an existing batch file from an automated run; add a new one.
- Every item is checked by `python tools/exercise_pipeline/verify_items.py "exercises/grades1-6/*.json"`.
- Automated runs write `"status": "draft"`. Only a human reviewer changes it to `"reviewed"` (then verify with `--allow-reviewed`).

## Item fields

| Field | Meaning |
|---|---|
| `id` | Unique, for example `A36.S2.04-sub-20261001-001` |
| `goal` | Goal id from `data/curriculum/OPS_1-6_oppimistavoitteet.md`, for example `A36.S2.04` |
| `level` | Grades 3–6: `P`, `T`, `H`, `K`. Grades 1–2: `V` (familiar) or `S` (new situation) |
| `type` | `numeric_entry` or `choice` |
| `stem_fi` | Task text in Finnish, decimal comma, at most 400 characters |
| `answer` | The correct answer as the pupil would type it |
| `answer_expr` | Plain arithmetic that code evaluates to check `answer`, for example `4/5 + 1/6` or `0.5 + 0.25` |
| `options` | For `choice`: the options, including the answer |
| `misconceptions` | Wrong answers a rule produces, tagged with the item bank id, for example `NUM-10a` |
| `workbook` | Item bank ids, for example `["NUM-10"]` |
| `source` | `template`, `generated` or `human` |
| `status` | `draft` (automated) or `reviewed` (human) |
| `notes` | Optional short note for the reviewer |

Any other field is rejected, which keeps personal data out.
