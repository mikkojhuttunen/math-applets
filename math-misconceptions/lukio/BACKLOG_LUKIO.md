# Math misconceptions, upper secondary (lukio): exercise-generation backlog

| | |
|---|---|
| Version | 2026-10-02 |
| Purpose | Work queue and progress tracker for exercises about documented misconceptions in lukio mathematics (MAY1, lyhyt MAB, pitkä MAA), linked to LOPS 2019 goal IDs |
| Built from | `data/curriculum/LOPS_2019_matematiikka_oppimistavoitteet.md` (goal IDs, levels), `data/misconceptions/lukio_misconceptions.md` (topics, typical wrong answers, evidence), `../math-misconceptions-7-9grades-backlog.md` (exercise types, per-run method, item rules; read only) |
| Status | **Framework only. No routine runs yet.** Generation starts when the tooling tasks in section 2 are done and a human sets `ROUTINE_ENABLED: yes`. |
| Runs completed | 0 |
| Last run | - |
| Progress | 0 of 151 planned cells in phases 0–2 generated |

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
ROUTINE_ENABLED: no           # set to yes only when section 2 tasks L-T01..L-T05 are done
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
2. **Select.** Go through section 3 top to bottom (sorted: priority, then suggested year, then module). For each topic collect its `o` cells in section 5 whose type is in an active phase. Skip cells with two `Failed` rows in the log. Take the first `TOPICS_PER_RUN` topics with at least one such cell, and up to `TYPES_PER_TOPIC` types each, ordered by phase, then by column order.
3. **Generate** per selected type a parametrized template and `ITEMS_PER_TYPE` items:
   - write the generator as `generators/<template>.py` with a fixed seed; `provenance.template` is the file name without `.py`;
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
| L-T02 | `scripts/verify.py`: copy of the 7–9 verifier; parse this backlog and the lukio curriculum file; add checks for `antiderivative`, `periodic`, `interval`, `rational`; check `syllabus` against the goal prefix. | Verifier | done 2026-10-02: also rejects retired goal IDs (MAA9.05), knows catalogue IDs as misconception tags, skips sample points outside the real domain. Structural and curriculum checks run on the empty bank (`VERIFY OK`); the sympy checks of the new answer kinds were not run (sympy not installable in that session) and get their first run in L-T03 |
| L-T03 | `tests/run_tests.py` with good and bad fixtures for each new check; one hand-written seed item per phase 0–2 type (log rows `Seed`). | Tests, 7 seed items | todo |
| L-T04 | `scripts/build_bank.py` for lukio (`build/bank.json`, `build/index.json` grouped by `by_lops`, `by_module`, `by_syllabus`, `by_misconception`, `by_type`). | Build script | todo |
| L-T05 | `ROUTINE_PROMPT_LUKIO.md` (routine settings and prompt, as the 7–9 `ROUTINE_PROMPT.md`) and a test run with "Run now". | Prompt file, first branch commit | todo |
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
| LFUN-02 | o | o | o | - | - | o | - | o | - | - | - | - | - | o | - |
| LVEC-01 | o | o | - | - | - | - | o | - | - | o | o | - | - | - | - |
| LEXP-03 | o | o | - | - | - | - | o | - | - | o | o | - | o | - | - |
| LLIM-01 | o | - | - | - | - | - | - | - | - | - | - | - | o | o | - |
| LLIM-02 | o | - | - | - | - | - | - | - | - | - | - | - | o | o | - |
| LDER-04 | o | - | - | - | - | - | - | - | o | - | o | - | o | - | - |
| LPRB-06 | o | o | o | - | - | - | o | - | - | - | - | - | - | - | - |
| LPRB-01 | o | o | o | - | - | - | o | - | - | - | - | - | - | - | - |
| LPRB-04 | o | o | - | - | - | - | - | - | - | - | - | - | - | o | - |
| LPRB-03 | o | o | - | - | - | - | - | - | - | - | - | - | - | o | - |
| LFUN-01 | o | - | - | - | - | - | - | o | - | - | o | - | o | o | - |
| LSTA-04 | o | - | - | - | - | - | - | - | - | - | - | - | o | o | - |
| ALG-09 | o | o | o | - | o | o | - | - | - | - | - | - | - | - | - |
| EXT-02 | o | o | o | - | - | o | - | - | - | - | - | - | - | - | - |
| NUM-08 | o | o | - | - | - | - | o | - | - | o | - | - | - | - | - |
| FUN-05 | o | o | - | - | - | - | - | - | - | - | o | - | - | o | - |
| EXT-04 | o | o | o | - | - | - | - | - | - | - | - | o | - | - | - |
| LEQU-01 | o | o | o | o | o | - | o | - | - | - | - | - | - | - | o |
| LEQU-02 | o | o | o | o | o | - | - | - | - | - | - | - | - | - | o |
| LEQU-03 | o | o | o | - | o | - | - | - | - | - | - | o | - | - | o |
| LEQU-04 | o | o | o | - | - | - | - | - | - | - | - | o | - | - | - |
| LEQU-05 | o | o | o | - | - | - | o | - | - | - | - | o | - | - | - |
| LVEC-02 | o | - | - | - | - | - | - | - | - | - | o | - | - | o | - |
| LVEC-03 | o | o | o | - | - | - | - | - | - | - | - | - | - | - | - |
| LTRI-03 | o | o | - | - | - | - | - | - | o | o | - | - | - | - | - |
| LTRI-02 | o | - | o | - | - | o | - | - | - | - | - | - | - | o | - |
| LTRI-01 | o | o | o | o | o | - | - | - | - | - | o | - | - | - | o |
| LEXP-02 | o | o | o | - | - | o | - | - | - | - | - | - | - | - | - |
| LEXP-01 | o | o | o | - | o | o | - | - | - | - | - | - | - | - | - |
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
| LEXP-04 | o | o | o | - | o | - | - | - | - | - | - | - | - | - | - |
| LTRI-04 | o | o | - | - | - | - | - | - | - | - | - | - | - | - | - |
| LINT-03 | o | o | o | - | - | - | - | - | - | - | - | - | - | - | - |
| LFIN-02 | o | o | - | - | - | - | - | - | - | - | - | - | - | - | - |
| LPRB-05 | o | o | - | - | - | - | - | o | - | - | - | - | - | o | - |
| LFUN-03 | o | o | - | - | - | - | o | - | - | - | - | - | - | - | - |

## 6. Generation log

One row per generated batch, newest at the bottom. Level is P / T / H / K; Tools is `none` or `cas`.

| Date | Topic | Type | Item IDs | Levels | Tools | LOPS ID | Location | Status | Note |
|---|---|---|---|---|---|---|---|---|---|

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
