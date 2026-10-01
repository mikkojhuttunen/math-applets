# Math misconceptions, grades 7-9: exercise-generation backlog

| | |
|---|---|
| Version | 2026-09-30 |
| Purpose | Work queue and progress tracker for auto-generating exercises about documented misconceptions, linked to the Finnish curriculum (OPS 7-9) goal IDs |
| Built from | `sources/math_misconceptions_item_bank.xlsx` (33 misconceptions), `../math-applets/math/OPS_7-9_oppimistavoitteet.md` (S-IDs, T-goals, levels), `sources/FinnMath_Exercise_Types_and_Learning_Analysis.docx` (exercise types, phases, item record) |
| Not available when built | `math_misconceptions_grades7-9_summary.docx` was not in the project. The xlsx was derived from it, so its content is covered through the xlsx. |
| Runs completed | 18 |
| Last run | 2026-10-01 |
| Progress | 95 of 227 planned cells generated |

## 1. Instructions for the scheduled task (read first)

All paths are relative to the folder `math-misconceptions/` of the repository. Edit only files inside this folder; the OPS goal file one level up is read only.

### 1.1 Configuration (edit here)

```
ACTIVE_PHASES:   0, 1, 2      # phases whose exercise types may be generated (see section 2)
TOPICS_PER_RUN:  3
TYPES_PER_TOPIC: 2
ITEMS_PER_TYPE:  5            # items written per matrix cell (one parametrized template)
LANGUAGE:        fi           # Finnish terms, decimal comma
BRANCH:          claude/exercises   # long-lived branch the routine pushes to; you merge into main
```

Defaults follow the "Recommended first version" in the exercise-types document: phases 0-2 need no interactive front-end and no LLM call per attempt. Add phase 3 when the interactive components exist and phase 4 once usage data shows where LLM feedback is needed.

### 1.2 What to do in each run

1. **Read** this file and the OPS goal file `../math-applets/math/OPS_7-9_oppimistavoitteet.md` (read only; it belongs to the applet pipeline). For each selected topic also read its row in `sources/math_misconceptions_item_bank.xlsx` (sheet `Misconceptions`: stem, correct answer, typical wrong answer, why students choose it). For `EXT-` topics use the seed table in section 3.2. Read the grade 5 / 7 / 8 / 9 criteria for the topic's T-goals in the OPS file (section 4).
2. **Select.** Go through section 3.1 top to bottom (already sorted: priority, then catalogue order). For each topic look at its row in section 4 and collect the cells marked `o` or `s` whose type belongs to an active phase. Skip cells that already have two `Failed` rows in the log (a human decides those). Take the first `TOPICS_PER_RUN` topics that have at least one such cell. Within a topic take up to `TYPES_PER_TOPIC` types, ordered by phase, then by column order in section 4.
3. **Generate** per selected type a parametrized template and `ITEMS_PER_TYPE` items:
   - write the generator as `generators/<template>.py` with a fixed random seed; `provenance.template` is the file name without `.py`;
   - the answer is computed by code, never written by hand;
   - every distractor, near-miss form or injected error carries the misconception ID (e.g. `ALG-08`) as its tag;
   - items cover at least two of the levels P / T / H / K (OPS section 6) and state the level;
   - the stem is the seed idea with new numbers and Finnish wording, not a copy of the xlsx stem; use everyday contexts (prices, recipes, map scales) where natural (T7).
4. **Write** the items to `exercises/<TopicID>/<TypeCode>.json` as described in section 1.3. Number the items 001 upward. Renumber before writing if you dropped an item.
5. **Update this file:** set the generated cells to `X`, append one row per batch to section 5 (Location = the json path), increase "Runs completed", set "Last run", recompute "Progress". Do not change anything else.
6. **Verify** with `python scripts/verify.py --base HEAD --check-backlog`. It must print `VERIFY OK`. Fix your new items until it does. If a template cannot be fixed, delete its new file, set its cell back to its previous code, add a log row with Status `Failed` and the reason, and run verify again.
7. **Never** overwrite, edit or delete an existing item or an `X` cell, and never change section 1. A finished cell is regenerated only if the user sets it back to `o`; the new items are then appended to the same file with numbering that continues.
8. **Stop condition:** if no `o` or `s` cell is left in the active phases, change nothing except "Last run" and report that the next phase should be enabled.

### 1.3 Item files and schema

One file per matrix cell: `exercises/<TopicID>/<TypeCode>.json`, for example `exercises/ALG-07/ES.json`. The file is a wrapper:

```json
{
  "schema_version": "1.0",
  "topic": "ALG-07",
  "type": "ES",
  "items": [ { ...item... }, { ...item... } ]
}
```

Each item follows `schema/item.schema.json`. Required fields: `schema_version`, `id`, `type`, `status`, `lang`, `curriculum` (`ops`, `t`, `grade`, `level`), `misconceptions`, `prompt`, `payload`, `solution`, `feedback`, `provenance`. Additional properties are not allowed.

| Rule | Value |
|---|---|
| Item ID | `<TopicID>-<TypeCode>-<nnn>`, e.g. `ALG-07-ES-001`; unique, numbered from 001 without gaps |
| Status | always `draft` for new items; only a human sets `approved` |
| `misconceptions` | must include the topic ID; more IDs only if a distractor targets another misconception |
| `curriculum.ops` | must include the topic's main S-ID; other entries only from its "OPS also" column |
| `curriculum.t` | only T-goals listed for the topic in section 3.1 |
| `provenance.verified` | `true` only if the answer was recomputed by code in the same run |
| Text | Finnish, decimal comma; an always-present plain Unicode version (`x²`, `√`); `latex` is optional |

Payload fields per type (details and limits in the schema):

| Type | `payload` |
|---|---|
| MC | `options[{id, text, misconception, feedback}]` (3-8), `correct[id]` |
| NE | `answer` (number / expression with `variables` and `samples` / set), `wrong[{match, misconception, feedback}]` |
| ES | `lines` (3-8), `error_line` (from 2), `error_type` |
| SO | `lines` in correct order, `accept` (`exact` or `dependency`) |
| FS | `lines`, `blank_index`, `answer` (expression, or equation with `solutions`) |
| ME | `reference`, `variables`, `samples`, `options[{id, text, equivalent, misconception}]` |
| RP | `constraint` (`solution_equals`), `checks{valid[], invalid[]}` |
| SC, MA, EST, GI, NL, EX, TF, PH | not yet specified; the schema accepts any object, so define the payload with the user before generating these types |

What `scripts/verify.py` checks: structure, curriculum links, and the algebra of NE, ES, SO, FS, ME and RP (answers, injected errors and distractors are recomputed with sympy). MC correctness is not machine-checked, so its generator must compute the options from the same numbers. Every new item is reviewed by a human before `approved`.

### 1.4 Quality rules

- The xlsx states that the wrong answers are the most typical option, not a measured majority. Do not present frequencies to students.
- Topics with evidence `Limited` or a note "check full text" are generated, but the log entry carries the note so the reviewer sees it.
- Before a topic is treated as complete for the active phases, at least one item should ask the student to justify (T4) or check plausibility (T6). If none exists, add an `MC` with a "why" option, or `TF` / `EX` if phase 4 is active.
- Do not copy item text from third-party datasets (Eedi, Otero et al.) without checking their licences.

## 2. Legend

**Cell codes in section 4:** `o` planned, `s` seed example only (hand-written, still to be generated as a batch), `X` generated batch exists (see log), `-` not suitable for this misconception.

| Code | Exercise type | Tier | Checked by | Phase |
|---|---|---|---|---|
| MC | Multiple choice (misconception-tagged distractors) | - | Option tag | 0 |
| NE | Numeric or expression entry | 1 | Symbolic checker (mathjs / sympy) | 1 |
| ES | Error spotting | 1 | Injected error location | 1 |
| SO | Step ordering | 1 | Stored sequence | 1 |
| FS | Fill in the missing step | 1 | Equivalence to removed line | 2 |
| ME | Multi-select equivalence | 1 | Symbolic comparison | 2 |
| RP | Reverse problem | 1 | Substitution | 2 |
| SC | Sorting or classifying | 1 | Category label per item | 3 |
| MA | Matching | 1 | Stored pairs | 3 |
| EST | Estimation | 2 | Tolerance band | 3 |
| GI | Graph interaction | 2 | Geometric tolerance | 3 |
| NL | Number line and inequalities | 2 | Solution-set comparison | 3 |
| EX | Explain in your own words | 3 | LLM feedback | 4 |
| TF | True or false with justification | 3 | LLM feedback | 4 |
| PH | Photo of handwritten work | 3 | LLM feedback | 4 |

Phases follow the exercise-types document (1: NE, ES, SO; 2: FS, ME, RP; 3: SC, MA, GI, NL; 4: EX, PH). Two placements are mine: MC is phase 0 (always available), and EST (Tier 2, not in the document's phase table) is placed in phase 3. TF (Tier 3) is placed in phase 4.

## 3. Topics (work queue)

### 3.1 Topic table

Priority: 1 = evidence Strong, 2 = Moderate or curriculum-derived (`EXT`), 3 = Limited. **OPS main** is the S-ID the topic is primarily assessed under; **OPS also** lists related S-IDs. **T** is the union of the linked T-goals. **Lk** is the suggested grade of the main S-ID (a proposal, see the OPS file section 0).

| ID | Topic | Evidence | Prio | OPS main | OPS also | T | Lk | Notes |
|---|---|---|---|---|---|---|---|---|
| ALG-01 | Letter as object (label) | Strong | 1 | S3.01 | S1.04 | T4, T7, T15 | 7 |  |
| ALG-06 | Operational reading of '=' | Strong | 1 | S3.05 | - | T14 | 7→8 | Applet gap (OPS §7): equation as a balance. |
| ALG-10 | Reversal error | Strong | 1 | S1.04 | S3.05 | T4, T7, T14 | 7→9 |  |
| NUM-01 | Longer decimal is larger | Strong | 1 | S2.06 | S2.08 | T11, T12 | 7 | OPS §6 files this under S2.06; S2.08 covers ordering on the number line. |
| NUM-02 | Shorter decimal is larger | Strong | 1 | S2.06 | S2.08 | T11, T12 | 7 | See NUM-01. |
| NUM-03 | Whole-number bias in fraction addition | Strong | 1 | S2.02 | - | T11 | 7 | Seed item has equal denominators; also cover unlike denominators (S2.02, OPS §6: 1/2 + 1/3). |
| NUM-04 | Multiplication always makes bigger | Strong | 1 | S2.03 | S2.06 | T11 | 7 | Applet gap (OPS §7): fraction division as areas. |
| NUM-06 | No number between 0,3 and 0,4 | Strong | 1 | S2.08 | - | T12 | 8 |  |
| PRO-01 | Illusion of linearity: area | Strong | 1 | S5.05 | S5.07 | T16, T18 | 8 | Applet gap (OPS §7): similarity and scale (k, k², k³). Same k² idea as OPS §6 (S5.05). |
| PRO-02 | Illusion of linearity: volume | Strong | 1 | S5.05 | S5.13 | T16, T18 | 8 | Applet gap (OPS §7): similarity and scale (k, k², k³). |
| FUN-02 | Slope–height confusion | Strong | 1 | S4.07 | S4.05 | T8, T15 | 9 |  |
| ALG-02 | X | Moderate | 2 | S3.01 | - | T15 | X | Evidence rests on a study with unverified authors; check before use. |
| ALG-04 | X | X | 2 | S3.02 | - | T14 | 7 |  |
| ALG-05 | X | X | 2 | S3.01 | - | T15 | 7 |  |
| ALG-07 | Sign errors and one-sided operations | Moderate | 2 | S3.05 | - | T14 | 7→8 | Applet gap (OPS §7): equation as a balance. Hand-written ES seed exists. |
| ALG-08 | Distributive law applied to one term | Moderate | 2 | S3.02 | S3.04 | T14 | 7 | Hand-written seeds exist (SO prototype, ME example). |
| ALG-09 | Square of a sum | Moderate | 2 | S3.04 | S3.03 | T14 | 8 |  |
| ALG-11 | Minus sign not distributed | Moderate | 2 | S3.02 | S2.01 | T10, T11, T14 | 7 |  |
| NUM-05 | Division always makes smaller | Moderate | 2 | S2.03 | S2.06 | T11 | 7 | Applet gap (OPS §7): fraction division as areas. |
| NUM-07 | Wrong base in reverse percentage | Moderate | 2 | S2.10 | - | T13 | 8 | Applet exists: prosentti-kerroin. |
| PRO-03 | Same perimeter means same area | Moderate | 2 | S5.07 | - | T18 | 7→9 |  |
| PRO-04 | Larger perimeter means larger area | Moderate | 2 | S5.07 | - | T18 | 7→9 |  |
| GEO-01 | Prototype-bound concept of triangle | Moderate | 2 | S5.03 | S5.01 | T16 | 7 |  |
| GEO-02 | A square is not a rectangle | Moderate | 2 | S5.03 | - | T16 | 7 |  |
| FUN-01 | Graph as picture | Moderate | 2 | S4.07 | S4.02 | T8, T15 | 9 |  |
| PRB-01 | Recency (gambler's fallacy) | Moderate | 2 | S6.06 | - | T19 | 9 | Applet gap (OPS §7): classical vs statistical probability. |
| PRB-02 | More black marbles means higher chance | Moderate | 2 | S6.06 | S2.02 | T11, T19 | 9 | Applet gap (OPS §7): classical vs statistical probability. |
| EXT-01 | Negative base and square: -3² read as 9 | Not assessed | 2 | S2.01 | S2.11 | T10, T11 | 7 | Applet gap (OPS §7): negatives on the number line. From OPS §6; literature evidence not yet checked. |
| EXT-02 | Integer exponents: 2³ = 6, a⁰ = 0, 2⁻¹ = -2 | Not assessed | 2 | S2.11 | - | T10, T11 | 8 | From OPS §6; literature evidence not yet checked. |
| EXT-03 | Inequality sign not reversed when multiplying or dividing by a negative number | Not assessed | 2 | S3.07 | - | T14 | 9 | From OPS §6; literature evidence not yet checked. |
| EXT-04 | x² = 9 gives only x = 3 | Not assessed | 2 | S3.08 | - | T14 | 9 | From OPS §6; literature evidence not yet checked. |
| EXT-05 | Pythagorean theorem assumed to hold for every triangle | Not assessed | 2 | S5.09 | - | T17 | 8 | Applet exists: pythagoras-neliot. From OPS §6; literature evidence not yet checked. |
| EXT-06 | Sine read as a length; adjacent and opposite leg mixed up | Not assessed | 2 | S5.10 | - | T17 | 9 | Applet gap (OPS §7): trigonometry in a right triangle. From OPS §6; literature evidence not yet checked. |
| EXT-07 | Area unit conversion: 1 m² = 100 cm² | Not assessed | 2 | S5.14 | - | T18 | 7→9 | From OPS §6; literature evidence not yet checked. |
| EXT-08 | Mean taken as the "typical value"; median read from unsorted data | Not assessed | 2 | S6.02 | S6.03 | T19 | 7 | Applet gap (OPS §7): mean vs median. From OPS §6; literature evidence not yet checked. |
| EXT-09 | Slope and intercept confused; steeper line means larger y | Not assessed | 2 | S4.05 | - | T15 | 8→9 | Applet exists: suoran-yhtalo. From OPS §6; literature evidence not yet checked. |
| ALG-03 | Value from alphabet position | Limited | 3 | S3.01 | S3.05 | T14, T15 | 7 | Limited evidence; check full text before relying on it. |
| ALG-12 | Subtraction of a negative number | Limited | 3 | S2.01 | - | T10, T11 | 7 | Applet gap (OPS §7): negatives on the number line. Limited evidence. |
| NUM-08 | Successive percentage changes | Limited | 3 | S2.10 | - | T13 | 8 | Applet exists: prosentti-kerroin. Limited evidence; also OPS §6 (+20 % then -20 %). |
| FUN-03 | Slope confused with visual steepness | Limited | 3 | S4.05 | - | T15 | 8→9 | Applet exists: suoran-yhtalo. Limited evidence. |
| FUN-04 | Function must have a formula or change | Limited | 3 | S4.04 | - | T15 | 8 | Limited evidence. |
| FUN-05 | Every linear function is proportional | Limited | 3 | S4.03 | S4.05 | T14, T15 | 8 | Limited evidence. |

### 3.2 Seeds for the `EXT` topics

These nine topics come from the misconception list in the OPS file (section 6) and have no row in the xlsx yet. Literature evidence has not been checked; add them to the xlsx once sources are found.

| ID | Topic | OPS main | Typical wrong answer | Correct |
|---|---|---|---|---|
| EXT-01 | Negative base and square: -3² read as 9 | S2.01 | -3² = 9 | -3² = -9 (and (-3)² = 9) |
| EXT-02 | Integer exponents: 2³ = 6, a⁰ = 0, 2⁻¹ = -2 | S2.11 | 2³ = 6; a⁰ = 0; 2⁻¹ = -2 | 2³ = 8; a⁰ = 1; 2⁻¹ = 1/2 |
| EXT-03 | Inequality sign not reversed when multiplying or dividing by a negative number | S3.07 | -2x > 6 gives x > -3 | x < -3 |
| EXT-04 | x² = 9 gives only x = 3 | S3.08 | x = 3 | x = 3 or x = -3 |
| EXT-05 | Pythagorean theorem assumed to hold for every triangle | S5.09 | applies a² + b² = c² to a triangle without a right angle | only right triangles; the converse is a test for a right angle |
| EXT-06 | Sine read as a length; adjacent and opposite leg mixed up | S5.10 | sin α = adjacent / hypotenuse, or sin α given in cm | sin α = opposite / hypotenuse, a dimensionless ratio |
| EXT-07 | Area unit conversion: 1 m² = 100 cm² | S5.14 | 1 m² = 100 cm² | 1 m² = 10 000 cm² |
| EXT-08 | Mean taken as the "typical value"; median read from unsorted data | S6.02 | median of 7, 2, 9, 4, 5 is 9 (middle of the list as written) | sort first: 2, 4, 5, 7, 9, so the median is 5 |
| EXT-09 | Slope and intercept confused; steeper line means larger y | S4.05 | for y = 3x + 1 the intercept is 3 | slope 3, intercept 1 |

## 4. Exercise-type coverage matrix

Same row order as section 3.1. Columns are in phase order.

| ID | MC | NE | ES | SO | FS | ME | RP | SC | MA | EST | GI | NL | EX | TF | PH |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ALG-01 | X | X | - | - | - | - | - | - | o | - | - | - | o | o | - |
| ALG-06 | X | X | X | - | - | - | X | o | - | - | - | - | - | o | - |
| ALG-10 | X | - | - | - | - | - | X | - | o | - | - | - | o | - | - |
| NUM-01 | X | X | - | - | - | - | - | o | - | - | - | o | o | - | - |
| NUM-02 | X | X | - | - | - | - | - | o | - | - | - | o | o | - | - |
| NUM-03 | X | X | X | - | X | X | - | - | - | o | - | - | - | - | - |
| NUM-04 | X | X | - | - | - | - | X | o | - | o | - | - | - | o | - |
| NUM-06 | X | - | - | - | - | - | X | - | - | - | - | o | o | o | - |
| PRO-01 | X | X | - | - | - | - | - | - | o | o | o | - | - | o | - |
| PRO-02 | X | X | - | - | - | - | - | - | o | o | o | - | - | o | - |
| FUN-02 | X | X | - | - | - | - | - | - | - | - | o | - | o | - | - |
| ALG-02 | X | - | - | - | - | - | X | - | - | - | - | - | o | o | - |
| ALG-04 | X | X | X | - | - | X | - | o | - | - | - | - | - | - | - |
| ALG-05 | X | X | - | - | - | X | - | - | - | - | - | - | - | - | - |
| ALG-07 | X | X | X | X | X | - | X | - | - | - | - | - | o | - | o |
| ALG-08 | X | X | X | X | X | X | X | - | - | - | - | - | - | - | - |
| ALG-09 | X | X | X | X | X | X | - | - | - | - | - | - | - | - | o |
| ALG-11 | X | X | X | X | X | X | - | - | - | - | - | - | - | - | - |
| NUM-05 | X | X | - | - | - | - | X | o | - | o | - | - | - | o | - |
| NUM-07 | X | X | X | X | X | - | - | - | - | o | - | - | o | - | o |
| PRO-03 | X | X | - | - | - | - | X | - | - | - | o | - | o | o | - |
| PRO-04 | X | X | - | - | - | - | X | - | - | - | o | - | o | o | - |
| GEO-01 | X | - | - | - | - | - | - | o | - | - | - | - | o | o | - |
| GEO-02 | X | - | - | - | - | - | - | o | - | - | - | - | o | o | - |
| FUN-01 | X | - | - | - | - | - | - | - | o | - | o | - | o | - | - |
| PRB-01 | X | X | - | - | - | - | - | - | - | - | - | - | o | o | - |
| PRB-02 | X | X | - | - | - | - | X | o | - | - | - | - | o | - | - |
| EXT-01 | X | X | X | - | X | X | - | - | - | - | - | - | - | - | - |
| EXT-02 | X | X | X | - | X | o | - | - | - | - | - | - | - | - | - |
| EXT-03 | X | X | o | o | o | - | - | - | - | - | - | o | o | - | o |
| EXT-04 | o | o | o | - | o | o | o | - | - | - | - | - | - | - | o |
| EXT-05 | o | o | - | - | - | - | - | o | - | - | - | - | o | o | - |
| EXT-06 | o | o | o | - | o | - | - | o | o | o | - | - | - | - | - |
| EXT-07 | o | o | o | - | - | - | - | - | o | o | - | - | - | - | - |
| EXT-08 | o | o | o | o | o | - | o | - | - | - | - | - | o | o | - |
| EXT-09 | o | o | - | - | - | - | o | o | o | - | o | - | - | - | - |
| ALG-03 | o | o | - | - | - | - | - | - | - | - | - | - | - | o | - |
| ALG-12 | o | o | o | - | - | o | - | - | - | - | - | - | - | - | - |
| NUM-08 | o | o | o | - | - | - | - | - | - | o | - | - | o | o | - |
| FUN-03 | o | o | - | - | - | - | - | - | - | - | o | - | - | o | - |
| FUN-04 | o | - | - | - | - | - | - | o | - | - | - | - | o | o | - |
| FUN-05 | o | o | - | - | - | - | - | o | o | - | - | - | - | o | - |

## 5. Generation log

One row per generated batch, newest at the bottom. Level is P / T / H / K (OPS section 6).

| Date | Topic | Type | Item IDs | Levels | OPS ID | Location | Status | Note |
|---|---|---|---|---|---|---|---|---|
| 2026-09-20 | ALG-07 | ES | (seed) | - | S3.05 | docx appendix | Seed | Tap the faulty line in 5 - 2x = 11; error: sign slip when dividing by a negative number |
| 2026-09-20 | ALG-08 | SO | (seed) | - | S3.02 | docx appendix, [prototype](https://claude.ai/artifact/BngH5P3L9yDcG1NPPx3JEu) | Seed | Order lines to simplify 2(x + 3) + 4x - 5; prototype has a generator |
| 2026-09-20 | ALG-08 | ME | (seed) | - | S3.02 | docx appendix | Seed | Which expressions equal 3(x - 2); distractors tagged |
| 2026-09-20 | - | NE | (seed) | - | S2.10 | docx appendix | Seed | Jacket 80 € +15 %. Fits no topic exactly; NUM-07 and NUM-08 are the closest. Not counted in section 4 |
| 2026-09-30 | ALG-01 | MC | ALG-01-MC-001..005 | T, T, T, H, H | S3.01 | exercises/ALG-01/MC.json | Draft | Strong; item 5 asks for a justification (no T4 link for this topic) |
| 2026-09-30 | ALG-01 | NE | ALG-01-NE-001..005 | T, T, T, H, H | S3.01 | exercises/ALG-01/NE.json | Draft | Strong |
| 2026-09-30 | ALG-06 | MC | ALG-06-MC-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-06/MC.json | Draft | Strong |
| 2026-09-30 | ALG-06 | NE | ALG-06-NE-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-06/NE.json | Draft | Strong |
| 2026-09-30 | ALG-10 | MC | ALG-10-MC-001..005 | T, T, T, H, H | S1.04 (S3.05) | exercises/ALG-10/MC.json | Draft | Strong |
| 2026-09-30 | ALG-10 | RP | ALG-10-RP-001..005 | T, T, T, H, K | S1.04 (S3.05) | exercises/ALG-10/RP.json | Draft | Strong |
| 2026-09-30 | ALG-06 | ES | ALG-06-ES-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-06/ES.json | Draft | Strong |
| 2026-09-30 | ALG-06 | RP | ALG-06-RP-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-06/RP.json | Draft | Strong |
| 2026-09-30 | NUM-01 | MC | NUM-01-MC-001..005 | T, T, T, H, H | S2.06 (S2.08) | exercises/NUM-01/MC.json | Draft | Strong; item 5 asks for a justification (no T4 link for this topic) |
| 2026-09-30 | NUM-01 | NE | NUM-01-NE-001..005 | T, T, T, H, H | S2.06 (S2.08) | exercises/NUM-01/NE.json | Draft | Strong |
| 2026-09-30 | NUM-02 | MC | NUM-02-MC-001..005 | T, T, T, H, H | S2.06 (S2.08) | exercises/NUM-02/MC.json | Draft | Strong; item 5 asks for a justification (no T4 link for this topic) |
| 2026-09-30 | NUM-02 | NE | NUM-02-NE-001..005 | T, T, T, H, H | S2.06 (S2.08) | exercises/NUM-02/NE.json | Draft | Strong |
| 2026-09-30 | NUM-03 | MC | NUM-03-MC-001..005 | T, T, T, H, H | S2.02 | exercises/NUM-03/MC.json | Draft | Strong; unlike denominators covered; item 5 asks for a justification |
| 2026-09-30 | NUM-03 | NE | NUM-03-NE-001..005 | T, T, T, H, H | S2.02 | exercises/NUM-03/NE.json | Draft | Strong; answers are numerators or denominators (integers) |
| 2026-09-30 | NUM-04 | MC | NUM-04-MC-001..005 | T, T, T, H, H | S2.03 (S2.06) | exercises/NUM-04/MC.json | Draft | Strong; item 5 asks for a justification |
| 2026-09-30 | NUM-04 | NE | NUM-04-NE-001..005 | T, T, T, H, H | S2.03 (S2.06) | exercises/NUM-04/NE.json | Draft | Strong |
| 2026-09-30 | NUM-06 | MC | NUM-06-MC-001..005 | T, T, T, H, H | S2.08 | exercises/NUM-06/MC.json | Draft | Strong; item 5 asks for a method justification |
| 2026-09-30 | NUM-06 | RP | NUM-06-RP-001..005 | T, T, T, H, H | S2.08 | exercises/NUM-06/RP.json | Draft | Strong |
| 2026-09-30 | NUM-03 | ES | NUM-03-ES-001..005 | T, T, T, H, H | S2.02 | exercises/NUM-03/ES.json | Draft | Strong; unlike denominators covered |
| 2026-09-30 | NUM-03 | FS | NUM-03-FS-001..005 | T, T, T, H, H | S2.02 | exercises/NUM-03/FS.json | Draft | Strong; answer is a numeric expression (variable x is only a schema placeholder) |
| 2026-09-30 | NUM-04 | RP | NUM-04-RP-001..005 | T, T, T, H, H | S2.03 (S2.06) | exercises/NUM-04/RP.json | Draft | Strong |
| 2026-09-30 | PRO-01 | MC | PRO-01-MC-001..005 | T, T, T, H, H | S5.05 | exercises/PRO-01/MC.json | Draft | Strong; item 5 asks for a justification |
| 2026-09-30 | PRO-01 | NE | PRO-01-NE-001..005 | T, T, T, H, H | S5.05 | exercises/PRO-01/NE.json | Draft | Strong |
| 2026-09-30 | NUM-03 | ME | NUM-03-ME-001..005 | T, T, T, H, H | S2.02 | exercises/NUM-03/ME.json | Draft | Strong; unlike denominators; expressions are numeric (variable x is only a schema placeholder) |
| 2026-09-30 | PRO-02 | MC | PRO-02-MC-001..005 | T, T, T, H, H | S5.05 | exercises/PRO-02/MC.json | Draft | Strong; item 5 asks for a justification |
| 2026-09-30 | PRO-02 | NE | PRO-02-NE-001..005 | T, T, T, H, H | S5.05 | exercises/PRO-02/NE.json | Draft | Strong |
| 2026-09-30 | FUN-02 | MC | FUN-02-MC-001..005 | T, T, T, H, H | S4.07 | exercises/FUN-02/MC.json | Draft | Strong; graphs described by value tables and equations (no figure); item 5 asks for a justification |
| 2026-09-30 | FUN-02 | NE | FUN-02-NE-001..005 | T, T, T, H, H | S4.07 | exercises/FUN-02/NE.json | Draft | Strong; speed from two graph points |
| 2026-09-30 | ALG-02 | MC | ALG-02-MC-001..005 | T, T, T, H, H | S3.01 | exercises/ALG-02/MC.json | Draft | Moderate; evidence rests on a study with unverified authors (check before use); item 4 asks for a justification |
| 2026-09-30 | ALG-02 | RP | ALG-02-RP-001..005 | T, T, T, H, H | S3.01 | exercises/ALG-02/RP.json | Draft | Moderate; evidence rests on a study with unverified authors (check before use); second letter given in words, equation written for x |
| 2026-09-30 | ALG-04 | MC | ALG-04-MC-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-04/MC.json | Draft | Moderate; item 4 asks for a justification (substitution check) |
| 2026-09-30 | ALG-04 | NE | ALG-04-NE-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-04/NE.json | Draft | Moderate |
| 2026-09-30 | ALG-05 | MC | ALG-05-MC-001..005 | T, T, T, H, H | S3.01 | exercises/ALG-05/MC.json | Draft | Moderate; item 4 asks for a justification |
| 2026-09-30 | ALG-05 | NE | ALG-05-NE-001..005 | T, T, T, H, H | S3.01 | exercises/ALG-05/NE.json | Draft | Moderate |
| 2026-10-01 | ALG-04 | ES | ALG-04-ES-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-04/ES.json | Draft | Moderate; expression lines, error merges unlike terms into one x-term |
| 2026-10-01 | ALG-04 | ME | ALG-04-ME-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-04/ME.json | Draft | Moderate |
| 2026-10-01 | ALG-05 | ME | ALG-05-ME-001..005 | T, T, T, H, H | S3.01 | exercises/ALG-05/ME.json | Draft | Moderate; place-value distractors such as 10c + n tagged ALG-05 |
| 2026-10-01 | ALG-07 | MC | ALG-07-MC-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-07/MC.json | Draft | Moderate; item 5 asks to identify the error in a step (justification) |
| 2026-10-01 | ALG-07 | NE | ALG-07-NE-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-07/NE.json | Draft | Moderate |
| 2026-10-01 | ALG-07 | ES | ALG-07-ES-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-07/ES.json | Draft | Moderate; sign not changed when moving a term, and one-sided division (item 3) |
| 2026-10-01 | ALG-07 | SO | ALG-07-SO-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-07/SO.json | Draft | Moderate; exact order, all lines equivalent to line 1 |
| 2026-10-01 | ALG-08 | MC | ALG-08-MC-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-08/MC.json | Draft | Moderate; item 5 asks to check a claim by substitution (justification) |
| 2026-10-01 | ALG-08 | NE | ALG-08-NE-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-08/NE.json | Draft | Moderate |
| 2026-10-01 | ALG-09 | MC | ALG-09-MC-001..005 | T, T, T, H, H | S3.04 (S3.03) | exercises/ALG-09/MC.json | Draft | Moderate; item 5 asks to check a claim by substitution (justification) |
| 2026-10-01 | ALG-09 | NE | ALG-09-NE-001..005 | T, T, T, H, H | S3.04 (S3.03) | exercises/ALG-09/NE.json | Draft | Moderate |
| 2026-10-01 | ALG-07 | FS | ALG-07-FS-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-07/FS.json | Draft | Moderate; blanked line is an equation (answer kind equation) |
| 2026-10-01 | ALG-07 | RP | ALG-07-RP-001..005 | T, T, T, H, H | S3.05 | exercises/ALG-07/RP.json | Draft | Moderate; invalid equations are sign-slip or one-sided results |
| 2026-10-01 | ALG-08 | ES | ALG-08-ES-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-08/ES.json | Draft | Moderate; error: only the first bracket term is multiplied |
| 2026-10-01 | ALG-08 | SO | ALG-08-SO-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-08/SO.json | Draft | Moderate; exact order, all lines equivalent to line 1 |
| 2026-10-01 | ALG-09 | ES | ALG-09-ES-001..005 | T, T, T, H, H | S3.04 (S3.03) | exercises/ALG-09/ES.json | Draft | Moderate; error: (a + b)² = a² + b² or dropped cross term |
| 2026-10-01 | ALG-09 | SO | ALG-09-SO-001..005 | T, T, T, H, H | S3.04 (S3.03) | exercises/ALG-09/SO.json | Draft | Moderate; exact order, all lines equivalent to line 1 |
| 2026-10-01 | ALG-08 | FS | ALG-08-FS-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-08/FS.json | Draft | Moderate; blanked line is an expression, answer accepted by equivalence |
| 2026-10-01 | ALG-08 | ME | ALG-08-ME-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-08/ME.json | Draft | Moderate; distractors multiply only one term of the bracket; item 2 sign distractor tagged ALG-11 |
| 2026-10-01 | ALG-09 | FS | ALG-09-FS-001..005 | T, T, T, H, H | S3.04 (S3.03) | exercises/ALG-09/FS.json | Draft | Moderate; blanked line is an expression, answer accepted by equivalence |
| 2026-10-01 | ALG-09 | ME | ALG-09-ME-001..005 | T, T, T, H, H | S3.04 (S3.03) | exercises/ALG-09/ME.json | Draft | Moderate; distractors distribute the power over the sum or lose the cross term |
| 2026-10-01 | ALG-11 | MC | ALG-11-MC-001..005 | T, T, T, H, H | S3.02 (S2.01) | exercises/ALG-11/MC.json | Draft | Moderate; item 5 asks to check a claim by substitution (justification) |
| 2026-10-01 | ALG-11 | NE | ALG-11-NE-001..005 | T, T, T, H, H | S3.02 (S2.01) | exercises/ALG-11/NE.json | Draft | Moderate |
| 2026-10-01 | ALG-08 | RP | ALG-08-RP-001..005 | T, T, T, H, H | S3.02 | exercises/ALG-08/RP.json | Draft | Moderate; invalid equations multiply only the first bracket term |
| 2026-10-01 | ALG-11 | ES | ALG-11-ES-001..005 | T, T, T, H, H | S3.02 (S2.01) | exercises/ALG-11/ES.json | Draft | Moderate; error: minus before a bracket changes only the first term's sign |
| 2026-10-01 | ALG-11 | SO | ALG-11-SO-001..005 | T, T, T, H, H | S3.02 (S2.01) | exercises/ALG-11/SO.json | Draft | Moderate; exact order, all lines equivalent to line 1 |
| 2026-10-01 | NUM-05 | MC | NUM-05-MC-001..005 | T, T, T, H, H | S2.03 (S2.06) | exercises/NUM-05/MC.json | Draft | Moderate; item 5 asks for a justification; xlsx row not read (openpyxl not in requirements), seed from backlog section 3.1 |
| 2026-10-01 | NUM-05 | NE | NUM-05-NE-001..005 | T, T, T, H, H | S2.03 (S2.06) | exercises/NUM-05/NE.json | Draft | Moderate; wrong answer is the product with the divisor |
| 2026-10-01 | ALG-11 | FS | ALG-11-FS-001..005 | T, T, T, H, H | S3.02 (S2.01) | exercises/ALG-11/FS.json | Draft | Moderate; blanked line is an expression, answer accepted by equivalence |
| 2026-10-01 | ALG-11 | ME | ALG-11-ME-001..005 | T, T, T, H, H | S3.02 (S2.01) | exercises/ALG-11/ME.json | Draft | Moderate; distractors leave a bracket term's sign unchanged |
| 2026-10-01 | NUM-05 | RP | NUM-05-RP-001..005 | T, T, T, H, H | S2.03 (S2.06) | exercises/NUM-05/RP.json | Draft | Moderate; invalid equations multiply instead of divide |
| 2026-10-01 | NUM-07 | MC | NUM-07-MC-001..005 | T, T, T, H, H | S2.10 | exercises/NUM-07/MC.json | Draft | Moderate; item 5 asks for a justification; xlsx row read via zip (openpyxl not in requirements) |
| 2026-10-01 | NUM-07 | NE | NUM-07-NE-001..005 | T, T, T, H, H | S2.10 | exercises/NUM-07/NE.json | Draft | Moderate; wrong answer is the percentage taken of the new amount |
| 2026-10-01 | NUM-07 | ES | NUM-07-ES-001..005 | T, T, T, H, H | S2.10 | exercises/NUM-07/ES.json | Draft | Moderate; lines are equations for the original amount x; error: percentage taken of the new amount or wrong factor |
| 2026-10-01 | NUM-07 | SO | NUM-07-SO-001..005 | T, T, T, H, H | S2.10 | exercises/NUM-07/SO.json | Draft | Moderate; exact order, all lines equivalent to line 1 |
| 2026-10-01 | PRO-03 | MC | PRO-03-MC-001..005 | T, T, T, H, H | S5.07 | exercises/PRO-03/MC.json | Draft | Moderate; item 5 asks for a justification; xlsx row read via zip (openpyxl not in requirements) |
| 2026-10-01 | PRO-03 | NE | PRO-03-NE-001..005 | T, T, T, H, H | S5.07 | exercises/PRO-03/NE.json | Draft | Moderate; wrong entry repeats the area of the other equal-perimeter shape |
| 2026-10-01 | PRO-04 | MC | PRO-04-MC-001..005 | T, T, T, H, H | S5.07 | exercises/PRO-04/MC.json | Draft | Moderate; item 5 asks for a justification |
| 2026-10-01 | PRO-04 | NE | PRO-04-NE-001..005 | T, T, T, H, H | S5.07 | exercises/PRO-04/NE.json | Draft | Moderate; wrong entry is the area or perimeter of the shape with the larger perimeter |
| 2026-10-01 | NUM-07 | FS | NUM-07-FS-001..005 | T, T, T, H, H | S2.10 | exercises/NUM-07/FS.json | Draft | Moderate; blanked line is an equation (answer kind equation); percentages written as hundredths so the checker compares exact rationals |
| 2026-10-01 | PRO-03 | RP | PRO-03-RP-001..005 | T, T, T, H, H | S5.07 | exercises/PRO-03/RP.json | Draft | Moderate; invalid equations equate the areas instead of the perimeters |
| 2026-10-01 | PRO-04 | RP | PRO-04-RP-001..005 | T, T, T, H, H | S5.07 | exercises/PRO-04/RP.json | Draft | Moderate; equal areas with a larger perimeter; invalid equations equate the perimeters |
| 2026-10-01 | GEO-01 | MC | GEO-01-MC-001..005 | T, T, T, H, H | S5.03 | exercises/GEO-01/MC.json | Draft | Moderate; triangles given by coordinates, angles or sides (no figure); item 5 asks for a justification |
| 2026-10-01 | GEO-02 | MC | GEO-02-MC-001..005 | T, T, T, H, H | S5.03 | exercises/GEO-02/MC.json | Draft | Moderate; item 5 asks to judge a class-inclusion claim (justification) |
| 2026-10-01 | FUN-01 | MC | FUN-01-MC-001..005 | T, T, T, H, H | S4.07 | exercises/FUN-01/MC.json | Draft | Moderate; graphs described by value tables and verbal trends (no figure); item 5 asks for a justification |
| 2026-10-01 | PRB-01 | MC | PRB-01-MC-001..005 | T, T, T, H, H | S6.06 | exercises/PRB-01/MC.json | Draft | Moderate; item 5 asks for a justification (independence); xlsx row read via zip (openpyxl not in requirements) |
| 2026-10-01 | PRB-01 | NE | PRB-01-NE-001..005 | T, T, T, H, H | S6.06 | exercises/PRB-01/NE.json | Draft | Moderate; wrong answers follow the "it is due" or "it balances out" belief |
| 2026-10-01 | PRB-02 | MC | PRB-02-MC-001..005 | T, T, T, H, H | S6.06 (S2.02) | exercises/PRB-02/MC.json | Draft | Moderate; item 5 asks for a justification (proportion, not count) |
| 2026-10-01 | PRB-02 | NE | PRB-02-NE-001..005 | T, T, T, H, H | S6.06 (S2.02) | exercises/PRB-02/NE.json | Draft | Moderate; wrong answer is the count of marbles instead of the proportion |
| 2026-10-01 | EXT-01 | MC | EXT-01-MC-001..005 | T, T, T, H, H | S2.01 (S2.11) | exercises/EXT-01/MC.json | Draft | Not assessed; literature evidence not yet checked; item 5 asks for a justification |
| 2026-10-01 | EXT-01 | NE | EXT-01-NE-001..005 | T, T, T, H, H | S2.01 (S2.11) | exercises/EXT-01/NE.json | Draft | Not assessed; literature evidence not yet checked; wrong answer reads −a² as (−a)² |
| 2026-10-01 | PRB-02 | RP | PRB-02-RP-001..005 | T, T, T, H, H | S6.06 (S2.02) | exercises/PRB-02/RP.json | Draft | Moderate; invalid equations use the count of black marbles instead of the proportion |
| 2026-10-01 | EXT-01 | ES | EXT-01-ES-001..005 | T, T, T, H, H | S2.01 (S2.11) | exercises/EXT-01/ES.json | Draft | Not assessed; literature evidence not yet checked; error: −a² read as a² |
| 2026-10-01 | EXT-01 | FS | EXT-01-FS-001..005 | T, T, T, H, H | S2.01 (S2.11) | exercises/EXT-01/FS.json | Draft | Not assessed; literature evidence not yet checked; blanked line is a numeric expression (variable x is only a schema placeholder) |
| 2026-10-01 | EXT-02 | MC | EXT-02-MC-001..005 | T, T, T, H, H | S2.11 | exercises/EXT-02/MC.json | Draft | Not assessed; literature evidence not yet checked; item 5 asks for a justification of a⁰ = 1 |
| 2026-10-01 | EXT-02 | NE | EXT-02-NE-001..005 | T, T, T, H, H | S2.11 | exercises/EXT-02/NE.json | Draft | Not assessed; literature evidence not yet checked; wrong answers read the power as a product, a⁰ as 0 and a⁻ⁿ as negative |
| 2026-10-01 | EXT-01 | ME | EXT-01-ME-001..005 | T, T, T, H, H | S2.01 (S2.11) | exercises/EXT-01/ME.json | Draft | Not assessed; literature evidence not yet checked; expressions are numeric (variable x is only a schema placeholder); distractors read −a² as (−a)² or the reverse |
| 2026-10-01 | EXT-02 | ES | EXT-02-ES-001..005 | T, T, T, H, H | S2.11 | exercises/EXT-02/ES.json | Draft | Not assessed; literature evidence not yet checked; exponents written with ^ so the checker can parse them; errors: power read as a product, a^0 = 0, a^(−n) negative |
| 2026-10-01 | EXT-02 | FS | EXT-02-FS-001..005 | T, T, T, H, H | S2.11 | exercises/EXT-02/FS.json | Draft | Not assessed; literature evidence not yet checked; blanked line is a numeric expression with ^ exponents (variable x is only a schema placeholder) |
| 2026-10-01 | EXT-03 | MC | EXT-03-MC-001..005 | T, T, T, H, H | S3.07 | exercises/EXT-03/MC.json | Draft | Not assessed; literature evidence not yet checked; item 5 asks for a justification by substitution |
| 2026-10-01 | EXT-03 | NE | EXT-03-NE-001..005 | T, T, T, H, H | S3.07 | exercises/EXT-03/NE.json | Draft | Not assessed; literature evidence not yet checked; answer is the number of integers in a window satisfying the inequality, wrong answer is the count with the sign not reversed |

## 6. Curriculum coverage

### 6.1 Topics per OPS goal (S-ID)

Main = the topic has this S-ID as its main goal; also = secondary link.

| S-ID | Oppilas osaa... | Lk | Main | Also |
|---|---|---|---|---|
| S1.04 | tulkita ja tuottaa matemaattista tekstiä (sanallinen tehtävä ↔ matemaattinen malli) | 7→9 | ALG-10 | ALG-01 |
| S2.01 | laskea peruslaskutoimituksia negatiivisilla luvuilla; laskujärjestys | 7 | ALG-12, EXT-01 | ALG-11 |
| S2.02 | laskea murtolukujen yhteen- ja vähennyslaskuja (samannimiset → erinimiset) | 7 | NUM-03 | PRB-02 |
| S2.03 | kertoa ja jakaa murtoluvun kokonaisluvulla ja murtoluvulla | 7 | NUM-04, NUM-05 | - |
| S2.06 | laskea desimaaliluvuilla sujuvasti | 7 | NUM-01, NUM-02 | NUM-04, NUM-05 |
| S2.08 | kuvata lukujoukot (luonnolliset, kokonais-, rationaali-, reaaliluvut), tunnistaa irrationaaliluvun, sijoittaa luvut lukusuoralle ja suuruusjärjestykseen | 8 | NUM-06 | NUM-01, NUM-02 |
| S2.10 | laskea muuttuneen arvon, perusarvon sekä muutos- ja vertailuprosentin; erottaa prosentin ja prosenttiyksikön | 8 | NUM-07, NUM-08 | - |
| S2.11 | laskea potensseilla, kun eksponentti on kokonaisluku (myös 0 ja negatiivinen) | 8 | EXT-02 | EXT-01 |
| S3.01 | käyttää muuttujaa ja laskea lausekkeen arvon | 7 | ALG-01, ALG-02, ALG-03, ALG-05 | - |
| S3.02 | muodostaa lausekkeita ja sieventää niitä (samanmuotoiset termit) | 7 | ALG-04, ALG-08, ALG-11 | - |
| S3.03 | sieventää potenssilausekkeita | 8 | - | ALG-09 |
| S3.04 | tunnistaa polynomin; laskea polynomien yhteen-, vähennys- ja kertolaskuja | 8 | ALG-09 | ALG-08 |
| S3.05 | muodostaa ja ratkaista ensimmäisen asteen yhtälön; perustella yhtäsuuruuden säilymisen | 7→8 | ALG-06, ALG-07 | ALG-03, ALG-10 |
| S3.07 | ratkaista ensimmäisen asteen epäyhtälön | 9 | EXT-03 | - |
| S3.08 | ratkaista vaillinaisen toisen asteen yhtälön (ax² + c = 0, ax² + bx = 0) | 9 | EXT-04 | - |
| S4.02 | kuvata riippuvuuksia graafisesti ja algebrallisesti (taulukko ↔ kuvaaja ↔ lauseke) | 8 | - | FUN-01 |
| S4.03 | tunnistaa ja käyttää suoraan ja kääntäen verrannollisuutta | 8 | FUN-05 | - |
| S4.04 | selittää funktion käsitteen ja laskea funktion arvon | 8 | FUN-04 | - |
| S4.05 | piirtää suoran; tulkita kulmakertoimen ja vakiotermin; tunnistaa nouseva/laskeva suora yhtälöstä | 8→9 | FUN-03, EXT-09 | FUN-02, FUN-05 |
| S4.07 | tulkita kuvaajia: funktion kasvaminen ja väheneminen | 9 | FUN-01, FUN-02 | - |
| S5.01 | käyttää käsitteitä piste, jana, suora, puolisuora, viiva ja kulma; nimetä kulmat | 7 | - | GEO-01 |
| S5.03 | tunnistaa ja nimetä monikulmioita ja niiden ominaisuuksia | 7 | GEO-01, GEO-02 | - |
| S5.05 | tunnistaa yhtenevät ja yhdenmuotoiset kuviot, löytää vastinosat, käyttää verrantoa ja mittakaavaa | 8 | PRO-01, PRO-02 | - |
| S5.07 | laskea monikulmioiden piirejä ja pinta-aloja (myös moniosaiset kuviot) | 7→9 | PRO-03, PRO-04 | PRO-01 |
| S5.09 | käyttää Pythagoraan lausetta ja sen käänteislausetta | 8 | EXT-05 | - |
| S5.10 | käyttää trigonometrisia funktioita (sin, cos, tan) suorakulmaisessa kolmiossa; nimetä viereinen ja vastainen kateetti | 9 | EXT-06 | - |
| S5.13 | laskea pallon, lieriön ja kartion (sekä särmiön ja pyramidin) pinta-alat, vaipan alat ja tilavuudet | 9 | - | PRO-02 |
| S5.14 | muuntaa pituus-, pinta-ala- ja tilavuusyksiköitä sekä vetomittoja (l, dl, cl, ml) | 7→9 | EXT-07 | - |
| S6.02 | laskea keskiarvon ja määrittää tyyppiarvon | 7 | EXT-08 | - |
| S6.03 | määrittää frekvenssin, suhteellisen frekvenssin ja mediaanin | 7 | - | EXT-08 |
| S6.06 | laskea klassisia todennäköisyyksiä | 9 | PRB-01, PRB-02 | - |

### 6.2 Topics per T-goal

| T | Count of topics |
|---|---|
| T4 | 2 |
| T7 | 2 |
| T8 | 2 |
| T10 | 4 |
| T11 | 10 |
| T12 | 3 |
| T13 | 2 |
| T14 | 11 |
| T15 | 10 |
| T16 | 4 |
| T17 | 2 |
| T18 | 5 |
| T19 | 3 |

T14 (unknown and equation solving) and T11 (rational-number arithmetic) carry the most topics, then T15 (variable, function, graphs). No topic links to T1-T3, T5, T6, T9 or T20: these are process goals or programming. T4 and T6 are handled through the item-design rules in section 1.4, not through topics.

### 6.3 OPS goals with no misconception topic yet

Not every goal needs a misconception exercise. The content goals below are the candidates for the next literature search:

- **S2.07** (7→9): erottaa tarkan arvon ja likiarvon; pyöristää annettuun ja oikeaan tarkkuuteen
- **S2.09** (7): selittää prosentin käsitteen; laskea prosenttiosuuden ja prosenttiluvun osoittaman määrän kokonaisuudesta
- **S2.12** (8): käyttää neliöjuurta laskutoimituksissa
- **S3.06** (8): käyttää verrantoa tehtävien ratkaisussa
- **S3.09** (9): ratkaista yhtälöparin graafisesti ja algebrallisesti; ymmärtää ratkaisun geometrisen merkityksen
- **S3.10** (7→8): tutkia ja muodostaa lukujonoja (sääntö, n:s jäsen)
- **S5.02** (7): tutkia suoriin ja kulmiin liittyviä ominaisuuksia (ristikulmat, vieruskulmat, kolmion kulmien summa)
- **S5.04** (7): piirtää suoran ja pisteen suhteen symmetrisiä kuvioita
- **S5.08** (8): laskea ympyrän kehän ja pinta-alan, kaaren pituuden ja sektorin pinta-alan
- **S5.11** (9): käyttää kehä- ja keskuskulmaa; tuntea Thaleen lauseen
- **S6.04** (9): kuvata hajontaa (vaihteluväli; hajonnan käsite)
- **S6.07** (9): määrittää tilastollisen todennäköisyyden ja verrata sitä klassiseen

Without a topic and not listed as a candidate: S1.01, S1.02, S1.03, S1.05, S1.06, S1.07, S1.08, S1.09, S2.04, S2.05, S2.13, S4.01, S4.06, S4.08, S5.06, S5.12, S6.01, S6.05. Most are goals under S1 (thinking skills) and construction/computation goals where no documented misconception has been catalogued.

## 7. Mapping decisions to confirm

- **Grade levels** come from the suggested grade split in the OPS file, which follows common textbook sequencing, not the national core curriculum. Change the mapping if the local curriculum differs.
- **NUM-01 and NUM-02** (decimal comparison) are mapped to S2.06 because the OPS file lists this error there. S2.08 (ordering numbers, number line) is the better fit for a number-line item; it is kept as a secondary link.
- **ALG-08** (2(x + 3)) is mapped to S3.02 (grade 7 simplification) with S3.04 (polynomial multiplication) as secondary. **ALG-09** ((a + b)²) is mapped to S3.04, secondary S3.03.
- **FUN-01 and FUN-02** are mapped to S4.07 (interpreting graphs, grade 9). The same ideas appear in S4.02 and S4.05 from grade 8; the seed items could be used a year earlier.
- **T-goal criteria** in the OPS file are summaries, not the official wording. Check them against the OPH table before quoting them to students.
- **Phase for MC, EST and TF** is my placement (section 2). Change it there if you prefer another order.
