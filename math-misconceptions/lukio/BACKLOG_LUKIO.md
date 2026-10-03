# Math misconceptions, upper secondary (lukio): exercise-generation backlog

| | |
|---|---|
| Version | 2026-10-02 |
| Purpose | Work queue and progress tracker for exercises about documented misconceptions in lukio mathematics (MAY1, lyhyt MAB, pitkä MAA), linked to LOPS 2019 goal IDs |
| Built from | `data/curriculum/LOPS_2019_matematiikka_oppimistavoitteet.md` (goal IDs, levels), `data/misconceptions/lukio_misconceptions.md` (topics, typical wrong answers, evidence), `../math-misconceptions-7-9grades-backlog.md` (exercise types, per-run method, item rules; read only) |
| Status | **Framework only. No routine runs yet.** Generation starts when the tooling tasks in section 2 are done and a human sets `ROUTINE_ENABLED: yes`. |
| Runs completed | 12 |
| Last run | 2026-10-03 |
| Progress | 59 of 151 planned cells in phases 0–2 generated |

## 0. Framework in one page

The lukio pipeline copies the **7–9 design** (one topic × exercise-type matrix, one JSON file per cell, generators with fixed seeds, sympy verification), not the 1–6 design (batches of 20 per backlog row). Reasons:

1. Lukio items are mostly symbolic (expressions, derivatives, integrals, equations, solution sets). The 7–9 verifier already recomputes NE, ES, SO, FS, ME and RP with sympy; derivatives and antiderivatives are a small extension.
2. Lukio misconceptions are about procedures and concepts, so error spotting, step ordering and fill-the-step items (ES, SO, FS) fit them better than the numeric-entry batches of grades 1–6.
3. The matrix shows coverage per misconception and per module at a glance, which is what a teacher of a given module needs.

Differences from the 7–9 pipeline:

| | 7–9 | Lukio |
|---|---|---|
| Folder | `math-misconceptions/` | `math-misconceptions/lukio/` (own schema, scripts, generators, exercises) |
| Branch | `claude/exercises` | `claude/exercises-lukio` |
| Curriculum link | `ops` S-IDs, `t` T-goals, `grade` 7–9 | `lops` goal IDs (`MAA6.06`), `g` general goals G1–G8, `syllabus` (`MAA` / `MAB`), `tools` (`none` = A part, `cas` = B part) |
| Topic IDs | `ALG-01`, `EXT-03`, … | `LDER-02`, … plus carried-over 1–9 IDs (section 3.2) |
| Item IDs | `ALG-07-ES-001` | `LU-LDER-02-ES-001` (prefix keeps IDs unique in the shared practice-page manifest) |
| Levels | P/T/H/K = grades 5/7/8/9 | P/T/H/K = module grades 5–6/7/8/9–10, tied to YO A and B parts |
| Extra answer kinds | number, expression, set | also `antiderivative` (checked by differentiating), `periodic` (base solutions + period), `interval` (union of intervals), exact `rational` |

The 7–9 scripts are copied and adapted, not shared: the pipelines own disjoint files (see `CLAUDE.md`), and a shared script would let one routine break the other.

## 1. Instructions for the scheduled task (read first)

All paths are relative to `math-misconceptions/lukio/`. Edit only files inside this folder. Read `../math-misconceptions-7-9grades-backlog.md` and `../sources/` but never edit them.

### 1.1 Configuration (edit here)

```
ROUTINE_ENABLED: yes           # set to yes only when section 2 tasks L-T01..L-T05 are done
ACTIVE_PHASES:   0, 1, 2      # phases whose exercise types may be generated (legend, section 4)
TOPICS_PER_RUN:  3
TYPES_PER_TOPIC: 2
ITEMS_PER_TYPE:  5            # items per matrix cell (one parametrized template)
SYLLABUS_MIX:    2            # for topics marked MAA, MAB: at least this many of the items target MAB
LANGUAGE:        fi           # Finnish terms, decimal comma, U+2212 minus
BRANCH:          claude/exercises-lukio
```

### 1.2 What to do in each run

0. If `ROUTINE_ENABLED` is `no`, change nothing and report "lukio routine not enabled".
1. **Read** this file, the curriculum file and, for each selected topic, its row in `data/misconceptions/lukio_misconceptions.md` (for carried-over topics the row in `../sources/math_misconceptions_item_bank.xlsx`, or the 7–9 backlog section 3.2 for `EXT-`).
2. **Select.** Go through section 3 top to bottom (sorted: priority, then suggested year, then module). For each topic collect its `o` or `s` cells in section 5 whose type is in an active phase. Skip cells with two `Failed` rows in the log. Take the first `TOPICS_PER_RUN` topics with at least one such cell, and up to `TYPES_PER_TOPIC` types each, ordered by phase, then by column order.
3. **Generate** per selected type a parametrized template and `ITEMS_PER_TYPE` items:
   - write the generator as `generators/<template>.py` with a fixed seed; `provenance.template` is the file name without `.py`;
   - import the helpers in `generators/gen_common.py` (`base_item`, `mc_options`, `cli`, `frac`, `show`); `generators/example_ltri01_ne.py` is the model, and `tests/fixtures/good/` has a hand-written example of each phase 0–2 type;
   - answers are computed by code (sympy), never written by hand;
   - every distractor, near-miss or injected error carries a misconception ID as its tag;
   - items cover at least two levels of P / T / H / K and state the level and `tools`;
   - if the topic's syllabus is `MAA, MAB`, at least `SYLLABUS_MIX` items target MAB, with a MAB goal ID and MAB-level content (models and applications, no symbolic calculus beyond MAB8);
   - stems are new; never copy YTL exam tasks or textbook tasks (copyright), even when the marking notes inspired the topic.
4. **Write** the items to `exercises/<TopicID>/<TypeCode>.json` (wrapper as in the 7–9 backlog section 1.3, with `"schema_version": "lukio-1.0"`). Number from 001 without gaps.
5. **Update this file:** set the cells to `X`, append one log row per batch (section 6), increase "Runs completed", set "Last run", recompute "Progress". Nothing else.
6. **Verify** with `python scripts/verify.py --base HEAD --check-backlog`. It must print `VERIFY OK`. If a template cannot be fixed, delete its file, restore the cell, log `Failed` with the reason, and verify again.
7. **Never** edit or delete an existing item or an `X` cell, and never change sections 0–2.
8. **Stop condition:** no `o` cell left in active phases: change only "Last run" and report it.

### 1.3 Quality rules

- Topics with evidence `Limited`, or a source marked † in the catalogue, are generated, but the log row carries "evidence to be checked".
- Each topic needs at least one item that asks for a justification (G3) or a plausibility check (G4) before it counts as complete.
- Items marked `tools: none` must be solvable by hand in a few minutes; `cas` items may assume a CAS but must not be trivial with one (YTL rule: an answer from software alone is not enough in analysis tasks).
- Do not present the typical wrong answers as frequencies; most evidence is qualitative or from other countries.

## 2. Tasks before generation starts

These are done in manual sessions (Claude Code with the teacher), not by the routine. Mark them `done` here when finished.

| # | Task | Output | Status |
|---|---|---|---|
| L-R01 | Read YTL "hyvän vastauksen piirteet" for lyhyt and pitkä 2019–2026 and list recurring errors per module. Needs network access to ylioppilastutkinto.fi. | `data/misconceptions/ytl_error_notes.md`; new or re-rated rows in the catalogue | todo |
| L-R02 | Check the curriculum file against ePerusteet (module contents, the † rows, MAB6/MAB7 names). Needs access to eperusteet.opintopolku.fi or oph.fi. | Curriculum file version 2 | done 2026-10-02: read from the ePerusteet API; all † resolved; MAB6 = Talousmatematiikan alkeet, MAB7 = Talousmatematiikka (same content as MAA9); MAA9.05 retired; 11 new IDs; change table in curriculum file section 8 |
| L-R03 | Evidence check of the catalogue as done for grades 1–6: trace each source, confirm the wrong answer, verify DOIs. Start with priority 1 topics. | Ratings and notes updated; bib entries without "unverified" | todo |
| L-R04 | Decide whether lukio rows go into the shared item bank workbook (owned by the 7–9 pipeline) or stay in the Markdown catalogue. | Decision in section 7 | todo |
| L-T01 | Schema `schema/item.schema.json`: copy of the 7–9 schema with the lukio `curriculum` block, ID patterns and answer kinds from section 0. | Schema | done 2026-10-02: `schema_version` `lukio-1.0`; `curriculum` = `lops`, `g`, `syllabus`, `level`, `tools`; IDs `LU-<Topic>-<Type>-nnn`; NE answer kinds `rational`, `antiderivative`, `periodic`, `interval` added; `e` reserved for Euler's number (variables a–d, f–z) |
| L-T02 | `scripts/verify.py`: copy of the 7–9 verifier; parse this backlog and the lukio curriculum file; add checks for `antiderivative`, `periodic`, `interval`, `rational`; check `syllabus` against the goal prefix. | Verifier | done 2026-10-02: also rejects retired goal IDs (MAA9.05), knows catalogue IDs as misconception tags, skips sample points outside the real domain. Structural and curriculum checks run on the empty bank (`VERIFY OK`); sympy checks of the new answer kinds probed 2026-10-02 with 38 throwaway items (good and bad per kind and per curriculum rule); two fixes: `ln|x|` was parsed as a product of letters, and d/dx ln|x| was not recognised as 1/x (variable now real). Known leniency: a reference ln(x) for 1/x passes because only x > 0 is evaluated. Fixtures for these go into L-T03 |
| L-T03 | `tests/run_tests.py` with good and bad fixtures for each new check; one hand-written seed item per phase 0–2 type (log rows `Seed`). | Tests, 7 seed items | done 2026-10-02: 13 good items (7 seeds + 6 for the answer kinds rational, antiderivative incl. ln\|x\|, periodic in degrees, interval incl. empty set), 31 bad fixtures, LOPS and catalogue file checks, backlog cross-check, `--base`; seeds live in `tests/fixtures/good/` and their cells are `s` (step 1.2.2 now selects `o` or `s`, as in 7–9) |
| L-T04 | `scripts/build_bank.py` for lukio (`build/bank.json`, `build/index.json` grouped by `by_lops`, `by_module`, `by_syllabus`, `by_misconception`, `by_type`). | Build script | done 2026-10-02: adapted copy of `../scripts/build_bank.py`; index also has `by_level`, `by_tools`, `by_g`, `by_topic`; flag `needs_cas` added; approved items only unless `--include-draft`; `build/` git-ignored by `lukio/.gitignore`; tests in `tests/run_tests.py` section 7 |
| L-T05 | `ROUTINE_PROMPT_LUKIO.md` (routine settings and prompt, as the 7–9 `ROUTINE_PROMPT.md`) and a test run with "Run now". | Prompt file, first branch commit | partly done 2026-10-02: prompt file, `generators/gen_common.py`, reference generator `generators/example_ltri01_ne.py` (tested); local dry run of the prompt with `ROUTINE_ENABLED: yes` on a throwaway branch (LFUN-02 MC, 5 items, 2 MAB) reached `VERIFY OK` and passing tests, nothing committed. Open: the teacher creates the routine and does the two "Run now" tests in `ROUTINE_PROMPT_LUKIO.md` section 1 |
| L-T06 | CI for lukio (unit tests and verify on pull requests touching `math-misconceptions/lukio/**`). | Workflow file; check with the site-publishing owner | todo |
| L-T07 | Ask the practice-page pipeline to read lukio items (new `lukio` format in `harjoittele/tools/build_manifest.js`). Request only; that pipeline makes the change. | Row in `harjoittele/BACKLOG_WEB.md` | todo |

Order: L-R02 and L-T01–L-T03 first (they block generation); L-R01 and L-R03 can run alongside the first generated batches, which stay `draft` anyway.

## 3. Topics (work queue)

Priority: 1 = evidence Strong, 2 = Moderate or carried over from 1–9, 3 = Limited. **LOPS main** is the goal the topic is primarily assessed under; **Syllabus** says which oppimäärä the items target; **Vk** is the suggested year of the main goal.

### 3.1 Topic table

| ID | Topic | Evidence | Prio | LOPS main | LOPS also | Syllabus | G | Vk | Notes |
|---|---|---|---|---|---|---|---|---|---|
| LFUN-02 | Linearity applied to every function | Strong | 1 | MAA2.01 | MAA5.03, MAA5.07, MAB2.07 | MAA, MAB | G2, G3 | 1 | Umbrella topic; tag LEXP-01 / LTRI-02 too when they apply |
| LVEC-01 | Length of a sum is the sum of lengths | Strong | 1 | MAA4.07 | MAA4.08 | MAA | G2, G4 | 1→2 | |
| LEXP-03 | Exponential growth judged as linear | Strong | 1 | MAB4.02 | MAA5.06, MAA9.03, MAB7.01 | MAA, MAB | G4, G5 | 1→2 | Good lyhyt starter |
| LLIM-01 | A limit cannot be reached | Strong | 1 | MAA6.01 | - | MAA | G2, G3 | 2 | Conceptual; mostly MC and later TF/EX |
| LLIM-02 | 0,999… is less than 1 | Strong | 1 | MAA6.01 | MAY1.01 | MAA, MAB | G3 | 2 | MAB items via MAY1.01 |
| LDER-04 | Graph of f′ read as graph of f | Strong | 1 | MAA6.08 | MAB8.03 | MAA, MAB | G2, G7 | 2 | Applet gap; GI needs the phase 3 front end |
| LPRB-06 | Order handled wrongly in counting | Strong | 1 | MAA8.03 | MAB5.07 | MAA, MAB | G4 | 2→3 | |
| LPRB-01 | Equiprobability bias | Strong | 1 | MAA8.04 | MAB5.06 | MAA, MAB | G2, G4 | 2→3 | |
| LPRB-04 | Representativeness | Strong | 1 | MAA8.04 | MAB5.06 | MAA, MAB | G3 | 2→3 | Related to 7–9 PRB-01 |
| LPRB-03 | Conjunction fallacy | Strong | 1 | MAA8.05 | MAB5.06 | MAA, MAB | G3 | 2→3 | |
| LFUN-01 | A function must be one formula | Strong | 1 | MAA12.01 | MAY1.07 | MAA, MAB | G2 | 3 | MAB items via MAY1.07 |
| LSTA-04 | Confidence interval read as a probability | Strong | 1 | MAB9.04 | - | MAB | G3, G8 | 3 | |
| ALG-09 | Square of a sum (carried over) | Strong | 2 | MAA2.01 | MAB2.07 | MAA, MAB | G2 | 1 | 1–9 workbook row; lukio-level items only |
| EXT-02 | Integer exponents (carried over) | Moderate | 2 | MAY1.04 | MAA5.05 | MAA, MAB | G2 | 1 | 7–9 seed row |
| NUM-08 | Successive percentage changes (carried over) | Strong | 2 | MAY1.03 | MAB6.01, MAA9.03 | MAA, MAB | G4, G8 | 1 | 1–9 workbook row |
| FUN-05 | Every linear function is proportional (carried over) | Moderate | 2 | MAY1.06 | MAB4.01 | MAA, MAB | G5 | 1 | 1–9 workbook row |
| EXT-04 | x² = a gives only the positive root (carried over) | Moderate | 2 | MAA2.04 | MAB2.04 | MAA, MAB | G4 | 1 | 7–9 seed row |
| LEQU-01 | Dividing by an expression that can be zero | Moderate | 2 | MAA2.05 | MAA2.04, MAB2.04 | MAA, MAB | G3, G4 | 1 | |
| LEQU-02 | Zero-product rule with a non-zero product | Moderate | 2 | MAA2.05 | - | MAA | G4 | 1 | |
| LEQU-03 | Inequality multiplied by an expression of unknown sign | Moderate | 2 | MAA2.06 | MAA2.07 | MAA | G3, G4 | 1 | Needs `interval` answers |
| LEQU-04 | Square root taken across an inequality | Moderate | 2 | MAA2.06 | - | MAA | G4 | 1 | Needs `interval` answers |
| LEQU-05 | Absolute value as "drop the minus" | Moderate | 2 | MAA4.06 | MAY1.02 | MAA | G4 | 1→2 | |
| LVEC-02 | A vector is tied to its position | Moderate | 2 | MAA4.07 | - | MAA | G2 | 1→2 | Mostly phase 3 (GI) |
| LVEC-03 | Dot product gives a vector | Moderate | 2 | MAA4.08 | MAA10.02 | MAA | G2 | 1→2 | |
| LTRI-03 | Radian not seen as a measure | Moderate | 2 | MAA5.01 | - | MAA | G2 | 2 | |
| LTRI-02 | Sine treated as a factor | Moderate | 2 | MAA5.03 | MAA6.07 | MAA | G2 | 2 | |
| LTRI-01 | Trigonometric equation has one solution | Moderate | 2 | MAA5.04 | - | MAA | G4 | 2 | Needs `periodic` answers |
| LEXP-02 | Fractional or negative exponent misread | Moderate | 2 | MAA5.05 | MAY1.04 | MAA, MAB | G2 | 2 | MAB items via MAY1.04 |
| LEXP-01 | Logarithm rules made linear | Moderate | 2 | MAA5.07 | MAB4.03 | MAA, MAB | G2 | 2 | |
| LLIM-03 | Limit is the function value | Moderate | 2 | MAA6.01 | MAA6.02 | MAA | G3 | 2 | Finnish YO evidence |
| LLIM-04 | Continuous means "no pen lift" on all of ℝ | Moderate | 2 | MAA6.02 | MAA12.02 | MAA | G2, G3 | 2 | |
| LDER-01 | Product and quotient rules made linear | Moderate | 2 | MAA6.05 | - | MAA | G2 | 2 | |
| LDER-02 | Chain rule: inner derivative omitted | Moderate | 2 | MAA6.06 | - | MAA | G2 | 2 | |
| LDER-03 | f′ = 0 always gives an extremum | Moderate | 2 | MAA6.08 | MAA6.09, MAB8.04 | MAA, MAB | G3, G4 | 2 | Finnish YO evidence |
| LINT-01 | Integration constant omitted | Moderate | 2 | MAA7.01 | - | MAA | G2 | 2 | Needs `antiderivative` answers |
| LINT-02 | Definite integral is always an area | Moderate | 2 | MAA7.04 | MAA7.03 | MAA | G3, G4 | 2 | |
| LSTA-03 | Standard deviation as bumpiness or range | Moderate | 2 | MAA8.01 | MAB5.02 | MAA, MAB | G4 | 2→3 | |
| LSTA-01 | Correlation shows causation | Moderate | 2 | MAA8.02 | MAB5.03 | MAA, MAB | G3, G8 | 2→3 | |
| LSTA-02 | r ≈ 0 means no relation; r is the slope | Moderate | 2 | MAA8.02 | MAB5.03 | MAA, MAB | G4 | 2→3 | |
| LPRB-02 | Confusion of the inverse | Moderate | 2 | MAA8.05 | - | MAA | G3, G4 | 2→3 | Conditional probability is not named in LOPS 2019 (MAA8 says only "laskusäännöt"); keep items within the multiplication rule or mark them as local extension |
| LFIN-01 | Compound interest computed as simple | Moderate | 2 | MAA9.03 | MAB7.01 | MAA, MAB | G5, G8 | 2→3 | |
| LLOG-01 | Implication confused with its converse | Moderate | 2 | MAA11.02 | MAA3.06 | MAA | G3 | 3 | |
| LDER-05 | Continuous implies differentiable | Moderate | 2 | MAA12.02 | MAA6.02 | MAA | G3 | 3 | Finnish sources |
| LGEO-01 | Sine law: ambiguous case missed | Limited | 3 | MAA3.03 | - | MAA | G4 | 1 | |
| LEXP-04 | Exponential equation solved by dividing by the base | Limited | 3 | MAA5.06 | MAB4.03 | MAA, MAB | G4 | 2 | |
| LTRI-04 | sin⁻¹ x read as 1/sin x | Limited | 3 | MAA5.04 | - | MAA | G2 | 2 | |
| LINT-03 | Integral taken factor by factor; power rule for n = −1 | Limited | 3 | MAA7.02 | MAA12.05 | MAA | G2 | 2 | |
| LFIN-02 | Nominal change taken as real change | Limited | 3 | MAB6.02 | - | MAB | G8 | 2 | Index is MAB6 only (MAA9.05 retired in curriculum v2) |
| LPRB-05 | Independent and mutually exclusive confused | Limited | 3 | MAA8.05 | - | MAA | G2 | 2→3 | |
| LFUN-03 | f⁻¹ read as 1/f | Limited | 3 | MAA12.04 | - | MAA | G2 | 3 | |

### 3.2 Carried-over topics

ALG-09, EXT-02, NUM-08, FUN-05 and EXT-04 are 1–9 rows. The lukio pipeline writes its own items for them (lukio goal IDs, lukio contexts and numbers, item IDs `LU-ALG-09-…`); it never edits the 7–9 items. Other carried-over rows (section 3 of the catalogue) can be added here later.

## 4. Legend

Cell codes in section 5: `o` planned, `s` seed only, `X` generated batch exists (see log), `-` not suitable.

Exercise types, tiers and phases are the same as in the 7–9 backlog section 2:

| Phase | Types |
|---|---|
| 0 | MC multiple choice with tagged distractors |
| 1 | NE numeric or expression entry, ES error spotting, SO step ordering |
| 2 | FS fill in the missing step, ME multi-select equivalence, RP reverse problem |
| 3 | SC sorting, MA matching, EST estimation, GI graph interaction, NL number line and intervals |
| 4 | EX explain, TF true or false with justification, PH photo of handwritten work |

## 5. Exercise-type coverage matrix

Same row order as section 3.1. Planned cells in phases 0–2: 151.

| ID | MC | NE | ES | SO | FS | ME | RP | SC | MA | EST | GI | NL | EX | TF | PH |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| LFUN-02 | X | X | X | - | - | X | - | o | - | - | - | - | - | o | - |
| LVEC-01 | X | X | - | - | - | - | X | - | - | o | o | - | - | - | - |
| LEXP-03 | X | X | - | - | - | - | X | - | - | o | o | - | o | - | - |
| LLIM-01 | X | - | - | - | - | - | - | - | - | - | - | - | o | o | - |
| LLIM-02 | X | - | - | - | - | - | - | - | - | - | - | - | o | o | - |
| LDER-04 | X | - | - | - | - | - | - | - | o | - | o | - | o | - | - |
| LPRB-06 | X | X | X | - | - | - | X | - | - | - | - | - | - | - | - |
| LPRB-01 | s | X | X | - | - | - | X | - | - | - | - | - | - | - | - |
| LPRB-04 | X | X | - | - | - | - | - | - | - | - | - | - | - | o | - |
| LPRB-03 | X | X | - | - | - | - | - | - | - | - | - | - | - | o | - |
| LFUN-01 | X | - | - | - | - | - | - | o | - | - | o | - | o | o | - |
| LSTA-04 | X | - | - | - | - | - | - | - | - | - | - | - | o | o | - |
| ALG-09 | X | X | X | - | X | X | - | - | - | - | - | - | - | - | - |
| EXT-02 | X | X | X | - | - | X | - | - | - | - | - | - | - | - | - |
| NUM-08 | X | X | - | - | - | - | X | - | - | o | - | - | - | - | - |
| FUN-05 | X | X | - | - | - | - | - | - | - | - | o | - | - | o | - |
| EXT-04 | X | X | X | - | - | - | - | - | - | - | - | o | - | - | - |
| LEQU-01 | X | X | s | X | X | - | s | - | - | - | - | - | - | - | o |
| LEQU-02 | X | X | X | s | X | - | - | - | - | - | - | - | - | - | o |
| LEQU-03 | X | X | X | - | o | - | - | - | - | - | - | o | - | - | o |
| LEQU-04 | X | X | X | - | - | - | - | - | - | - | - | o | - | - | - |
| LEQU-05 | X | X | o | - | - | - | o | - | - | - | - | o | - | - | - |
| LVEC-02 | o | - | - | - | - | - | - | - | - | - | o | - | - | o | - |
| LVEC-03 | o | o | o | - | - | - | - | - | - | - | - | - | - | - | - |
| LTRI-03 | o | o | - | - | - | - | - | - | o | o | - | - | - | - | - |
| LTRI-02 | o | - | o | - | - | o | - | - | - | - | - | - | - | o | - |
| LTRI-01 | o | s | o | o | o | - | - | - | - | - | o | - | - | - | o |
| LEXP-02 | o | o | o | - | - | o | - | - | - | - | - | - | - | - | - |
| LEXP-01 | o | o | o | - | o | s | - | - | - | - | - | - | - | - | - |
| LLIM-03 | o | o | o | - | - | - | - | - | - | - | o | - | - | - | - |
| LLIM-04 | o | - | - | - | - | - | - | o | - | - | - | - | - | o | - |
| LDER-01 | o | o | o | o | o | o | - | - | - | - | - | - | - | - | o |
| LDER-02 | o | o | o | - | o | o | - | - | - | - | - | - | - | - | o |
| LDER-03 | o | o | o | o | - | - | - | - | - | - | o | - | - | - | o |
| LINT-01 | o | o | o | - | - | o | - | - | - | - | - | - | - | - | - |
| LINT-02 | o | o | o | o | o | - | - | - | - | - | o | - | - | - | o |
| LSTA-03 | o | o | - | - | - | - | - | o | - | o | - | - | - | - | - |
| LSTA-01 | o | - | - | - | - | - | - | - | - | - | - | - | o | o | - |
| LSTA-02 | o | - | - | - | - | - | - | o | - | o | o | - | - | - | - |
| LPRB-02 | o | o | o | o | - | - | - | - | - | - | - | - | o | - | - |
| LFIN-01 | o | o | o | - | - | - | o | - | - | o | - | - | - | - | - |
| LLOG-01 | o | - | - | - | - | - | - | o | - | - | - | - | o | o | - |
| LDER-05 | o | - | o | - | - | - | - | - | - | - | - | - | - | o | - |
| LGEO-01 | o | o | o | - | - | - | - | - | - | - | o | - | - | - | - |
| LEXP-04 | o | o | o | - | s | - | - | - | - | - | - | - | - | - | - |
| LTRI-04 | o | o | - | - | - | - | - | - | - | - | - | - | - | - | - |
| LINT-03 | o | o | o | - | - | - | - | - | - | - | - | - | - | - | - |
| LFIN-02 | o | o | - | - | - | - | - | - | - | - | - | - | - | - | - |
| LPRB-05 | o | o | - | - | - | - | - | o | - | - | - | - | - | o | - |
| LFUN-03 | o | o | - | - | - | - | o | - | - | - | - | - | - | - | - |

## 6. Generation log

One row per generated batch, newest at the bottom. Level is P / T / H / K; Tools is `none` or `cas`.

| Date | Topic | Type | Item IDs | Levels | Tools | LOPS ID | Location | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-02 | LPRB-01 | MC | LU-LPRB-01-MC-001 | P | none | MAB5.06 | tests/fixtures/good/LPRB-01/MC.json | Seed | Hand-written (L-T03), also a test fixture; Two dice: is sum 7 or sum 12 more likely; MAB item |
| 2026-10-02 | LTRI-01 | NE | LU-LTRI-01-NE-001 | T | none | MAA5.04 | tests/fixtures/good/LTRI-01/NE.json | Seed | Hand-written (L-T03), also a test fixture; sin x = 1/2, all solutions in radians; answer kind periodic |
| 2026-10-02 | LEQU-01 | ES | LU-LEQU-01-ES-001 | T | none | MAA2.05 | tests/fixtures/good/LEQU-01/ES.json | Seed | Hand-written (L-T03), also a test fixture; x³ = 4x divided by x, root 0 lost |
| 2026-10-02 | LEQU-02 | SO | LU-LEQU-02-SO-001 | T | none | MAA2.05 | tests/fixtures/good/LEQU-02/SO.json | Seed | Hand-written (L-T03), also a test fixture; Order the steps of (x − 2)(x − 3) = 6: zero-product rule only after the right side is 0 |
| 2026-10-02 | LEXP-04 | FS | LU-LEXP-04-FS-001 | P | none | MAB4.03 | tests/fixtures/good/LEXP-04/FS.json | Seed | Hand-written (L-T03), also a test fixture; 3 · 2^x = 48, missing line 2^x = 2^4; MAB item |
| 2026-10-02 | LEXP-01 | ME | LU-LEXP-01-ME-001 | T | none | MAA5.07 | tests/fixtures/good/LEXP-01/ME.json | Seed | Hand-written (L-T03), also a test fixture; Which equal lg x + lg y; distractors lg(x + y), lg x · lg y |
| 2026-10-02 | LEQU-01 | RP | LU-LEQU-01-RP-001 | H | none | MAA2.05 | tests/fixtures/good/LEQU-01/RP.json | Seed | Hand-written (L-T03), also a test fixture; Quadratic equation whose only solution is x = 3; x² = 3x listed as invalid |
| 2026-10-02 | LFUN-02 | MC | LU-LFUN-02-MC-001…005 | P, T, H | none | MAA2.01, MAA5.03, MAA5.07, MAB2.07 | exercises/LFUN-02/MC.json | Draft | Run 1; (x + a)², sin(a + b), lg a + lg b; 2 MAB items; items 004 and 005 are justification or plausibility checks |
| 2026-10-02 | LFUN-02 | NE | LU-LFUN-02-NE-001…005 | P, T, H | none | MAA2.01, MAA5.03, MAB2.07 | exercises/LFUN-02/NE.json | Draft | Run 1; √(a² + b²), expanding squares (expression), sin(π/6 + π/3) plausibility; 2 MAB items |
| 2026-10-02 | LVEC-01 | MC | LU-LVEC-01-MC-001…005 | P, T, H | none | MAA4.07 | exercises/LVEC-01/MC.json | Draft | Run 1; perpendicular and general sums, equality condition, possible lengths |
| 2026-10-02 | LVEC-01 | NE | LU-LVEC-01-NE-001…005 | P, T, H | none | MAA4.07 | exercises/LVEC-01/NE.json | Draft | Run 1; coordinates, boat and current, opposite vectors, minimum length |
| 2026-10-02 | LEXP-03 | MC | LU-LEXP-03-MC-001…005 | P, T, H | none | MAB4.02, MAB7.01, MAA5.06 | exercises/LEXP-03/MC.json | Draft | Run 1; 3 % for 20 years, doubling time, bacteria, 50 % for 4 years, investment estimate; 3 MAB items |
| 2026-10-02 | LEXP-03 | NE | LU-LEXP-03-NE-001…005 | P, T, H | none, cas | MAB4.02, MAA5.06, MAA9.03 | exercises/LEXP-03/NE.json | Draft | Run 1; item 002 is cas (doubling time at 5 %); 2 MAB items |
| 2026-10-02 | LFUN-02 | ES | LU-LFUN-02-ES-001…005 | P, T, H | none | MAB2.07, MAA2.01, MAA5.03, MAA5.07 | exercises/LFUN-02/ES.json | Draft | Run 2; square of a sum split (equation and expression, 2 MAB items), sin(π/6 + π/3), √(x² + 9) = 5, ln(2x) + ln(3x); item 003 has a plausibility hint |
| 2026-10-02 | LFUN-02 | ME | LU-LFUN-02-ME-001…005 | P, T, H | none | MAB2.07, MAA2.01, MAA5.03, MAA5.07 | exercises/LFUN-02/ME.json | Draft | Run 2; (x + 4)², (3x − 2)² (2 MAB items), sin 2x, √(x² + y²), ln(xy²) |
| 2026-10-02 | LVEC-01 | RP | LU-LVEC-01-RP-001…005 | P, T, H | none | MAA4.07, MAA4.08 | exercises/LVEC-01/RP.json | Draft | Run 2; equation for s = \|a + b\|² (perpendicular, robot, components, 60°, opposite vectors) |
| 2026-10-02 | LEXP-03 | RP | LU-LEXP-03-RP-001…005 | P, T, H | none | MAB4.02, MAB7.01, MAA5.06 | exercises/LEXP-03/RP.json | Draft | Run 2; doubling bacteria, 10 % interest, growth factor, doubling time, halving value; 3 MAB items; exact fractions used instead of decimals so the verifier can compare solutions |
| 2026-10-02 | LLIM-01 | MC | LU-LLIM-01-MC-001…005 | P, T, H, K | none | MAA6.01 | exercises/LLIM-01/MC.json | Draft | Run 3; constant function, removable discontinuity, polynomial limit by substitution, 4/x as x grows, sin x / x justification; MAA only |
| 2026-10-02 | LLIM-02 | MC | LU-LLIM-02-MC-001…005 | P, T, H, K | none | MAA6.01, MAY1.01 | exercises/LLIM-02/MC.json | Draft | Run 3; 0,999… = 1, 3 · 1/3, 10x − x trick, 0,777… as fraction, plausibility via midpoint; 3 MAB items via MAY1.01 |
| 2026-10-02 | LDER-04 | MC | LU-LDER-04-MC-001…005 | P, T, H, K | none | MAA6.08, MAB8.03 | exercises/LDER-04/MC.json | Draft | Run 3; sign of f′, maximum of f from f′, plant growth speed, f′ < 0 is not f < 0, justification at x = 3; 2 MAB items |
| 2026-10-02 | LPRB-06 | MC | LU-LPRB-06-MC-001…005 | P, T | none | MAA8.03, MAB5.07 | exercises/LPRB-06/MC.json | Draft | Run 4; committee 3 of 8, pizza toppings (MAB), medals (order matters), handshakes (MAB), justification of dividing by 3!; 2 MAB items |
| 2026-10-02 | LPRB-06 | NE | LU-LPRB-06-NE-001…005 | P, T, H | none, cas | MAA8.03, MAB5.07 | exercises/LPRB-06/NE.json | Draft | Run 4; 3 of 10, 4 of 12 (MAB), medals, boys and girls with product principle, plausibility 5 of 15 (cas); 1 MAB item |
| 2026-10-02 | LPRB-01 | MC | - | - | - | - | - | Failed | Run 4; the seed cell stays `s` (tests require it) and the seed already uses ID LU-LPRB-01-MC-001, so a generated batch would collide; no file kept |
| 2026-10-02 | LPRB-01 | NE | LU-LPRB-01-NE-001…005 | P, T, H | none | MAA8.04, MAB5.06 | exercises/LPRB-01/NE.json | Draft | Run 4; sum 9, one head of two (MAB), two heads of three, sum at most 4 (MAB), at least one six with plausibility check; answers rational; 2 MAB items |
| 2026-10-02 | LPRB-04 | MC | LU-LPRB-04-MC-001…005 | P, T, H | none | MAA8.04, MAB5.06 | exercises/LPRB-04/MC.json | Draft | Run 4; coin sequences, lotto rows (MAB), dice sequences, sequence vs event (MAB), family justification (MAB); evidence † for the source (kahneman1972subjective), evidence to be checked; 3 MAB items |
| 2026-10-02 | LPRB-04 | NE | LU-LPRB-04-NE-001…005 | P, T, H | none | MAA8.04, MAB5.06 | exercises/LPRB-04/NE.json | Draft | Run 4; count of more likely sequences, P of a sequence (MAB), ratio of sequences, sequence vs event (MAB), lotto row count; evidence to be checked; 2 MAB items |
| 2026-10-02 | LPRB-06 | ES | LU-LPRB-06-ES-001…005 | P, T, H | none | MAA8.03, MAB5.07 | exercises/LPRB-06/ES.json | Draft | Run 5; division by k! forgotten (3 of 8, 2 boys of 6 and 1 girl of 5), divided although order matters (medals), divided by k instead of k! (pizza, MAB), handshakes with plausibility hint (MAB); 2 MAB items |
| 2026-10-02 | LPRB-06 | RP | LU-LPRB-06-RP-001…005 | P, T, H | none | MAA8.03, MAB5.07 | exercises/LPRB-06/RP.json | Draft | Run 5; equation for k: 3 of 8, 2 toppings of 6 (MAB), medals (order matters), 4 of 9, handshakes (MAB); 2 MAB items |
| 2026-10-02 | LPRB-01 | MC | - | - | - | - | - | Skipped | Run 5; not selected: the cell stays `s` and the seed already uses ID LU-LPRB-01-MC-001, so a batch would collide again (see Run 4 Failed row); ES and RP generated instead |
| 2026-10-02 | LPRB-01 | ES | LU-LPRB-01-ES-001…005 | T, P, H | none | MAA8.04, MAB5.06 | exercises/LPRB-01/ES.json | Draft | Run 5; sums 9 or 10, at least one head of two (MAB), two heads of three, sum at most 3 (MAB), five and six in either order with a hint; 2 MAB items |
| 2026-10-02 | LPRB-01 | RP | LU-LPRB-01-RP-001…005 | P, T, H | none | MAA8.04, MAB5.06 | exercises/LPRB-01/RP.json | Draft | Run 5; equation for p with coin sequences (at least one head of 2 and of 3, exactly 2 of 3, exactly 1 of 4, all alike with justification of why 1/2 fails); probabilities exact in binary; 3 MAB items |
| 2026-10-02 | LPRB-03 | MC | LU-LPRB-03-MC-001…005 | P, T, H | none | MAA8.05, MAB5.06 | exercises/LPRB-03/MC.json | Draft | Run 5; prime vs prime and even, two free throws (MAB), club subset (MAB), possible P(A and B) when P(A) = 0,30, library justification (G3); 2 MAB items |
| 2026-10-02 | LPRB-03 | NE | LU-LPRB-03-NE-001…005 | P, T, H | none | MAA8.05, MAB5.06 | exercises/LPRB-03/NE.json | Draft | Run 5; even and greater than 3, red ace (MAB), first and third coin heads (MAB), independent product, sum 7 with first die 3 and plausibility of an estimate; answers rational; 2 MAB items |
| 2026-10-02 | LFUN-01 | MC | LU-LFUN-01-MC-001…005 | P, T, H | none | MAY1.07, MAA12.01 | exercises/LFUN-01/MC.json | Draft | Run 6; constant rule, piecewise f(3), table with equal values, parking tariff, \|x\| justification; 3 MAB items via MAY1.07; verifier allows only G2 for this topic, so item 005 is a justification in content but tagged G2 |
| 2026-10-02 | LSTA-04 | MC | LU-LSTA-04-MC-001…005 | P, T, H | none, cas | MAB9.04 | exercises/LSTA-04/MC.json | Draft | Run 6; meaning of 95 %, margin of error (cas), sample size 100→400, 40 intervals, can true support be 50 %; all MAB; items 001, 004, 005 are justification or plausibility checks |
| 2026-10-02 | ALG-09 | MC | LU-ALG-09-MC-001…005 | P, T, H | none | MAA2.01, MAB2.07 | exercises/ALG-09/MC.json | Draft | Run 6; (x − 6)², (2x + 5)² − (2x − 5)², extended plot (MAB), a² + b² from a + b and ab (MAB), counterexample justification; 2 MAB items; carried over from 1–9 |
| 2026-10-02 | ALG-09 | NE | LU-ALG-09-NE-001…005 | P, T, H | none | MAA2.01, MAB2.07 | exercises/ALG-09/NE.json | Draft | Run 6; (x − 8)² expression, 47² by (50 − 3)², area increase (MAB), a² + b² (MAB), (a + b)² − (a² + b²) at a = 3, b = 4; 2 MAB items |
| 2026-10-02 | ALG-09 | ES | LU-ALG-09-ES-001…005 | P, T, H | none | MAB2.07, MAA2.01 | exercises/ALG-09/ES.json | Draft | Run 7; yard area (MAB), ((2x + 6)/2)² − 9, 98² as (100 − 2)², two years of 5 % growth (MAB), equation (x + 2)² = x² + 20 with a substitution hint; 2 MAB items |
| 2026-10-02 | ALG-09 | FS | LU-ALG-09-FS-001…005 | P, T, H | none | MAA2.01, MAB2.07 | exercises/ALG-09/FS.json | Draft | Run 7; binomial square as a product, (2x − 3)², (1 + 0,04)² (MAB), equation with the square opened, area increase (MAB); 2 MAB items |
| 2026-10-02 | EXT-02 | MC | LU-EXT-02-MC-001…005 | P, T, H | none | MAY1.04, MAA5.05 | exercises/EXT-02/MC.json | Draft | Run 7; 2⁻³, 3⁰ + 2⁻², 10⁻² m in cm (MAB), 4 · 10⁻³ (MAB), justification of a⁰ = 1; MAB items via MAY1.04; evidence not yet checked (catalogue rating Moderate); verifier allows only G2 for this topic, so item 005 is a justification in content but tagged G2 |
| 2026-10-02 | EXT-02 | NE | LU-EXT-02-NE-001…005 | P, T, H | none | MAY1.04, MAA5.05 | exercises/EXT-02/NE.json | Draft | Run 7; 2⁻³, 5⁰ + 3⁻², 4 · 10⁻² (MAB), (2/3)⁻², N(−3) for bacteria (MAB); answers rational or number; MAB items via MAY1.04 |
| 2026-10-02 | NUM-08 | MC | LU-NUM-08-MC-001…005 | P, T, H | none | MAY1.03, MAA9.03, MAB6.01 | exercises/NUM-08/MC.json | Draft | Run 7; +20 % then −20 %, price 50 € +30 % −30 % (MAB), +10 % and +20 % (MAB), −10 % for three years, plausibility check of undoing +25 % (MAB); 3 MAB items |
| 2026-10-02 | NUM-08 | NE | LU-NUM-08-NE-001…005 | P, T, H | none | MAY1.03, MAA9.03, MAB6.01 | exercises/NUM-08/NE.json | Draft | Run 7; 80 € +15 % −15 %, two 10 % rises (MAB), two 20 % cuts (MAB), +3 % for three years, undoing +20 % (MAB); 3 MAB items |
| 2026-10-02 | EXT-02 | ES | LU-EXT-02-ES-001…005 | P, T, H | none | MAY1.04, MAA5.05 | exercises/EXT-02/ES.json | Draft | Run 8; 5⁰ + 5⁻¹ (a⁰ = 0), 4⁻² as 4 · (−2), 3 · 10⁻² as negative (MAB), (2⁻¹)⁻² with exponents added, N(−2) for bacteria with plausibility hint (MAB); 2 MAB items; evidence not yet checked (catalogue rating Moderate); verifier allows only G2 for this topic |
| 2026-10-02 | EXT-02 | ME | LU-EXT-02-ME-001…005 | P, T, H | none | MAY1.04, MAA5.05 | exercises/EXT-02/ME.json | Draft | Run 8; x⁻², x⁰ + x⁻¹, 2 · 10⁻ˣ (MAB), (x⁻¹)⁻², 500 · 2⁻ˣ (MAB); 2 MAB items; evidence not yet checked |
| 2026-10-02 | ALG-09 | ME | LU-ALG-09-ME-001…005 | P, T, H | none | MAA2.01, MAB2.07 | exercises/ALG-09/ME.json | Draft | Run 8; (x + 5)², (2x − 3)² (MAB), (x + y)² − (x − y)², (x + 1/x)², (a + b)² − a² (MAB); 2 MAB items |
| 2026-10-02 | NUM-08 | RP | LU-NUM-08-RP-001…005 | P, T, H | none | MAY1.03, MAB6.01, MAA9.03 | exercises/NUM-08/RP.json | Draft | Run 8; equation for p, k, s, p, d: +50 % −50 % (MAB), +10 % and +20 % (MAB), −20 % then +25 %, equal yearly rise giving 21 %, undoing +25 % (MAB); 3 MAB items |
| 2026-10-02 | FUN-05 | MC | LU-FUN-05-MC-001…005 | P, T, H | none | MAY1.06, MAB4.01 | exercises/FUN-05/MC.json | Draft | Run 9; taxi 10 km, bike rental (MAB), proportional function, table y = 3x + 4 (MAB), counterexample f(2x) ≠ 2f(x) as justification; 2 MAB items; evidence Limited in the catalogue, evidence to be checked; verifier allows only G5 for this topic, so item 005 is a justification in content but tagged G5 |
| 2026-10-02 | FUN-05 | NE | LU-FUN-05-NE-001…005 | P, T, H | none | MAY1.06, MAB4.01 | exercises/FUN-05/NE.json | Draft | Run 9; f(10) from f(5), phone plan (MAB), gym fee (MAB), f(6) from two points, tank with plausibility check of an estimate; 2 MAB items; evidence to be checked |
| 2026-10-02 | EXT-04 | MC | LU-EXT-04-MC-001…005 | T, H | none | MAA2.04, MAB2.04 | exercises/EXT-04/MC.json | Draft | Run 9; x² = 49, tile area 2,25 (MAB), (x − 2)² = 9, 2x² = 50 (MAB), justification why x = 8 for x² = 64 is incomplete; 2 MAB items; evidence not yet checked; only G4 allowed for this topic |
| 2026-10-02 | EXT-04 | NE | LU-EXT-04-NE-001…005 | T, H | none | MAA2.04, MAB2.04 | exercises/EXT-04/NE.json | Draft | Run 9; negative root of x² = 121, 3x² = 75 (MAB), smaller root of (x − 1)² = 16, number of roots (MAB), sum of roots with plausibility check; 2 MAB items; evidence not yet checked |
| 2026-10-02 | LEQU-01 | MC | LU-LEQU-01-MC-001…005 | T, H | none | MAA2.05, MAA2.04, MAB2.04 | exercises/LEQU-01/MC.json | Draft | Run 9; x² = 3x, ball height 12t − 3t² (MAB), x³ = 4x, x(x − 5) = 2x (MAB), justification why dividing by x − 1 is an error (G3); 2 MAB items; source † (vaiyavutjamai2006effects), evidence to be checked |
| 2026-10-02 | LEQU-01 | NE | LU-LEQU-01-NE-001…005 | T, H | none | MAA2.05, MAA2.04, MAB2.04 | exercises/LEQU-01/NE.json | Draft | Run 9; smaller root of x² = 7x, number of roots of 6x² = 18x (MAB), x³ = 9x, product of roots of x(x + 4) = 3x (MAB), sum of roots with plausibility check; 2 MAB items; evidence to be checked |
| 2026-10-02 | LEQU-01 | ES, RP | - | - | - | - | - | Skipped | Run 9; not selected: the seed cells `s` already use IDs LU-LEQU-01-ES-001 and LU-LEQU-01-RP-001, so a batch would collide; MC and NE generated instead |
| 2026-10-02 | LPRB-01 | MC | - | - | - | - | - | Skipped | Run 9; not selected: seed ID collision as in Run 4 and Run 5 |
| 2026-10-02 | EXT-04 | ES | LU-EXT-04-ES-001…005 | T, H | none | MAA2.04, MAB2.04 | exercises/EXT-04/ES.json | Draft | Run 10; x² = 81, nollakohdat of y = x² − 9 (MAB), (x − 2)² = 9, 2x² = 50 (MAB), x² + 5 = 30 with a substitution hint; the negative root is dropped on the error line; 2 MAB items; evidence not yet checked |
| 2026-10-02 | LEQU-01 | SO | LU-LEQU-01-SO-001…005 | T, H | none | MAA2.05, MAB2.04, MAA2.04 | exercises/LEQU-01/SO.json | Draft | Run 10; order the steps without dividing: x² = 5x, 2t² = 8t (MAB), x³ = 9x, x(x + 2) = 3x (MAB), common factor x − 2 (G3); 2 MAB items; source † (vaiyavutjamai2006effects), evidence to be checked |
| 2026-10-02 | LEQU-01 | FS | LU-LEQU-01-FS-001…005 | T, H | none | MAA2.05, MAB2.04, MAA2.04 | exercises/LEQU-01/FS.json | Draft | Run 10; blank is the factoring line: x² = 7x, 3x² = 12x (MAB), x³ = 16x, x(x + 2) = 3x (MAB), common factor x − 3 (G3); 2 MAB items; evidence to be checked |
| 2026-10-02 | LEQU-02 | MC | LU-LEQU-02-MC-001…005 | T, H | none | MAA2.05 | exercises/LEQU-02/MC.json | Draft | Run 10; (x − 2)(x − 3) = 6, x(x + 4) = 5, (2x − 1)(x + 3) = 4, substitution check of x = 13 or 14 (justification), which equation allows the rule directly; MAA only |
| 2026-10-02 | LEQU-02 | NE | LU-LEQU-02-NE-001…005 | T, H | none | MAA2.05 | exercises/LEQU-02/NE.json | Draft | Run 10; larger root of (x − 3)(x − 4) = 12, smaller root of x(x − 5) = 14, larger root of (x + 1)(x − 2) = 10, sum of roots of x(x − 6) = 16, sum of roots of (x − 3)(x + 2) = −6 with a substitution check; MAA only |
| 2026-10-03 | LEQU-02 | ES | LU-LEQU-02-ES-001…005 | T, H | none | MAA2.05 | exercises/LEQU-02/ES.json | Draft | Run 11; (x − 4)(x + 1) = 6, x(x + 3) = 10, x² − 4x = 12 with the error on line 3, (x + 2)(x + 3) = 12 with substitution hint, x(x − 1)(x − 2) = 6; MAA only; evidence Moderate, source vaiyavutjamai2006effects |
| 2026-10-03 | LEQU-02 | FS | LU-LEQU-02-FS-001…005 | T, H | none | MAA2.05 | exercises/LEQU-02/FS.json | Draft | Run 11; blank is moving the right side to 0 or the factoring line: (x − 5)(x + 1) = 7, x(x + 2) = 8, (x + 2)(x − 4) = 16, (x + 1)(x + 4) = 10, (x − 2)(x − 3) = 20; MAA only |
| 2026-10-03 | LEQU-02 | SO | - | - | - | - | - | Skipped | Run 11; not selected: the seed cell `s` already uses ID LU-LEQU-02-SO-001, so a batch would collide; ES and FS generated instead |
| 2026-10-03 | LEQU-03 | MC | LU-LEQU-03-MC-001…005 | T, H | none | MAA2.06, MAA2.07 | exercises/LEQU-03/MC.json | Draft | Run 11; 5/x > 2, −6/x < 3, justification why multiplying 1/x < 2 by x is incomplete (G3), plausibility check of x < 4 for 4/x > 1, 6/(x² + 1) > 1 where multiplying is allowed; MAA only; source † (tsamir2004consistencies), evidence to be checked |
| 2026-10-03 | LEQU-03 | NE | LU-LEQU-03-NE-001…005 | T, H | none | MAA2.06, MAA2.07 | exercises/LEQU-03/NE.json | Draft | Run 11; interval answers for 1/x > 3, 2/(x − 1) < 1, 4/x ≤ 1 with check at x = −2, 3/(x + 1) > 1, x/(x − 2) < 3; MAA only; source † (tsamir2004consistencies), evidence to be checked |
| 2026-10-03 | LEQU-04 | MC | LU-LEQU-04-MC-001…005 | T, H | none | MAA2.06 | exercises/LEQU-04/MC.json | Draft | Run 11; x² < 16, x² > 49, (x + 2)² ≤ 9, test number that exposes x < 3 for x² < 9, justification via √(x²) = \|x\| (G4 only allowed); MAA only; source † (tsamir2004consistencies), evidence to be checked |
| 2026-10-03 | LEQU-04 | NE | LU-LEQU-04-NE-001…005 | T, H | none | MAA2.06 | exercises/LEQU-04/NE.json | Draft | Run 11; interval answers for x² < 4, x² > 9, x² ≤ 25 with check at x = −4, (x − 1)² < 4, 2x² ≥ 18; MAA only; source † (tsamir2004consistencies), evidence to be checked |
| 2026-10-03 | LEQU-03 | ES | LU-LEQU-03-ES-001…005 | T, H | none | MAA2.06, MAA2.07 | exercises/LEQU-03/ES.json | Draft | Run 12; 3/x < 1, 4/(x − 2) > 1, 1/x > −2 with a substitution hint, (x + 1)/x < 2 and 3/(x + 2) < 1 with the error on line 3 (G3 on item 004); MAA only; source † (tsamir2004consistencies), evidence to be checked |
| 2026-10-03 | LEQU-03 | FS | - | - | - | - | - | Failed | Run 12; the verifier's FS check accepts only equations with finite solution sets or expression answers, so a blank line that is an inequality cannot be checked (scripts/ is not editable by the routine); no file kept, cell stays `o` |
| 2026-10-03 | LEQU-04 | ES | LU-LEQU-04-ES-001…005 | T, H | none | MAA2.06 | exercises/LEQU-04/ES.json | Draft | Run 12; x² < 16 with √(x²) written out, x² > 36 by factoring, (x + 1)² ≤ 9, 4x² < 25 with a substitution hint, x² + 2 > 11; the dropped absolute value or lost branch is the error; MAA only; source † (tsamir2004consistencies), evidence to be checked |
| 2026-10-03 | LEQU-05 | MC | LU-LEQU-05-MC-001…005 | T, H | none | MAA4.06, MAY1.02 | exercises/LEQU-05/MC.json | Draft | Run 12; \|x − 3\| = 5, \|x\| = −4 (no solutions), \|2x − 1\| = 7, when \|x\| = −x holds (justification, MAY1.02), \|x − 2\| = \|x + 4\|; MAA only; evidence Moderate, source almog2012absolute |
| 2026-10-03 | LEQU-05 | NE | LU-LEQU-05-NE-001…005 | T, H | none | MAA4.06 | exercises/LEQU-05/NE.json | Draft | Run 12; smaller root of \|x − 3\| = 5, number of roots of \|2x − 1\| = 7, sum of roots of \|x + 4\| = 6, smaller root of \|3x − 2\| = \|x + 6\|, number of roots of \|x − 1\| = −2 with a substitution check; MAA only |

## 7. Coverage and decisions to confirm

### 7.1 Topics per module (main goal or "also")

| Module | Topics |
|---|---|
| MAY1 | EXT-02, NUM-08, FUN-05, LLIM-02, LFUN-01, LEXP-02, LEQU-05 |
| MAA2 | LFUN-02, ALG-09, EXT-04, LEQU-01, LEQU-02, LEQU-03, LEQU-04 |
| MAA3 | LGEO-01, LLOG-01 |
| MAA4 | LVEC-01, LVEC-02, LVEC-03, LEQU-05 |
| MAA5 | LTRI-01, LTRI-02, LTRI-03, LTRI-04, LEXP-01, LEXP-02, LEXP-03, LEXP-04, LFUN-02 |
| MAA6 | LLIM-01, LLIM-02, LLIM-03, LLIM-04, LDER-01, LDER-02, LDER-03, LDER-04, LDER-05, LTRI-02 |
| MAA7 | LINT-01, LINT-02, LINT-03 |
| MAA8 | LSTA-01, LSTA-02, LSTA-03, LPRB-01 … LPRB-06 |
| MAA9 | LEXP-03, LFIN-01, LFIN-02, NUM-08 |
| MAA10 | LVEC-03 |
| MAA11 | LLOG-01 |
| MAA12 | LFUN-01, LFUN-03, LDER-05, LLIM-04, LINT-03 |
| MAB2 | LFUN-02, ALG-09, EXT-04, LEQU-01 |
| MAB3 | none yet (7–9 PRO-01, PRO-02 fit MAB3.01) |
| MAB4 | LEXP-03, LEXP-01, LEXP-04, FUN-05 |
| MAB5 | LSTA-01, LSTA-02, LSTA-03, LPRB-01, LPRB-03, LPRB-04, LPRB-06 |
| MAB6, MAB7 | NUM-08, LFIN-01, LFIN-02, LEXP-03 |
| MAB8 | LDER-03, LDER-04 |
| MAB9 | LSTA-04 |

Gaps: MAB3, MAA3, MAA10 and MAB9 beyond confidence intervals. L-R01 (YTL notes) is the most likely source of topics for them.

### 7.2 Decisions to confirm

1. **Design.** 7–9 matrix design with forked tooling (section 0), not 1–6 batches. Alternative: generalise the 7–9 scripts with a `--profile lukio` option, which needs the 7–9 pipeline's agreement because it edits its files.
2. **IDs.** `L`-prefixed topic IDs and `LU-` item IDs (section 0).
3. **Syllabus split.** One topic, items for both syllabi (`SYLLABUS_MIX`), rather than separate MAA and MAB topics.
4. **Carried-over topics.** Five 1–9 rows get lukio items (section 3.2). Others are only cross-referenced.
5. **Order.** Evidence first, then year. Alternative: follow the module order of one school year so a teacher gets complete modules sooner.
6. **Copyright.** YTL tasks and textbook tasks are used only as inspiration for topics, never as stems.
