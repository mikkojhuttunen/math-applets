# math-applets

Interactive maths applets for Finnish schools (grades 1-9 and upper secondary), published with GitHub Pages from `main`. User-facing text is Finnish.

## Pipelines, disjoint files

| Pipeline | Files it owns | Instructions | Branch its routine pushes to |
|---|---|---|---|
| Applets | `BACKLOG.md`, `INDEX.md`, `index.html`, level folders | `APPLET_SPEC.md`, `SCHEDULED_TASK_PROMPT.md` | `claude/applets` |
| Misconception exercises, grades 7-9 | `math-misconceptions/` except `grades1-6/` | `math-misconceptions/README.md`, `math-misconceptions/ROUTINE_PROMPT.md` | `claude/exercises` |
| Exercises, grades 1-6 | `math-misconceptions/grades1-6/` | `math-misconceptions/grades1-6/ROUTINE_PROMPT_1-6.md`, `math-misconceptions/grades1-6/EXPERT_REVIEW_REQUIRED.md` | `claude/exercises-1-6` |
| Practice pages | `harjoittele/` | `harjoittele/BACKLOG_WEB.md` | no routine; manual sessions |
| Demo site | `demo/` | `demo/README.md` | no routine; manual sessions |
| Site publishing | `LIVE_BACKLOG.md`, `TESTING.md`, `.nojekyll`, `.github/workflows/pages-live.yml` | `LIVE_BACKLOG.md` | no routine; manual sessions |
| Telegram bot (paused) | `telegram-bot/` | `telegram-bot/BACKLOG_BOT.md`, `telegram-bot/BOT_ANALYSIS.md` | no routine; paused at B01 |

Work on one pipeline never edits another's files. The practice pages, the demo site and the bot read the other pipelines' files read-only. `math-applets/math/OPS_7-9_oppimistavoitteet.md` is shared read-only reference (curriculum goals S1-S6). The grades 1-6 pipeline reads `math-misconceptions/sources/` (item bank) read-only; its own curriculum goals are in `math-misconceptions/grades1-6/data/curriculum/OPS_1-6_oppimistavoitteet.md`.

## Layout

- `luokat-1-6/`, `yla-aste-7-9/`, `lukio-pitka/`, `lukio-lyhyt/`: one self-contained `.html` per applet, no subfolders, no build step, no external resources.
- `scripts/check_applet.js`: automated applet check; run `node scripts/check_applet.js <file.html>` and expect `CHECK OK`.
- Some older applets (English titles, e.g. `lukio-pitka/Vector_addition.html`) were imported from another repo and predate `APPLET_SPEC.md`; they do not pass the checker and are not backlog items. Do not use them as style references.

## Applet work

- Follow `APPLET_SPEC.md`. Style references: `lukio-pitka/eksponentti-logaritmi.html`, `yla-aste-7-9/prosentti-kerroin.html`.
- Backlog states: `odottaa` → `työn alla` → `valmis` → `hyväksytty` / `korjattava`. Only the teacher sets `hyväksytty` and `korjattava`.
- A finished applet also needs its backlog fields (Tiedosto, Valmistui, Huomiot with hand calculations and Tutki itse answers), a row in `INDEX.md` and an `<li>` in `index.html`.
- Numbers on pages: decimal comma, U+2212 minus sign, never `NaN`/`undefined`.

## Exercise work

- Grades 7-9: follow `math-misconceptions/README.md`. Run `python tests/run_tests.py` and `python scripts/verify.py` from `math-misconceptions/` before committing.
- Grades 1-6: follow `math-misconceptions/grades1-6/ROUTINE_PROMPT_1-6.md`. From `math-misconceptions/grades1-6/` run `python -m unittest discover -s tools/buggy_rules`, `python -m unittest discover -s tools/exercise_pipeline` and `python tools/exercise_pipeline/verify_items.py "exercises/grades1-6/*.json"` before committing. Batches go in `exercises/grades1-6/` inside that folder, never in `math-misconceptions/exercises/`, which the 7-9 scripts read. No pupil data, ever; see `EXPERT_REVIEW_REQUIRED.md`.

## Git

- Merge `claude/*` branches into `main` with a merge commit, never squash: the routines merge `main` back every run.
- Commit messages in Finnish for applet work, following existing history (e.g. `Lisää applet 07: ...`).
