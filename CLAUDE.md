# math-applets

Interactive maths applets for Finnish schools (grades 1-9 and upper secondary), published with GitHub Pages from `main`. User-facing text is Finnish.

## Two pipelines, disjoint files

| Pipeline | Files it owns | Instructions | Branch its routine pushes to |
|---|---|---|---|
| Applets | `BACKLOG.md`, `INDEX.md`, `index.html`, level folders | `APPLET_SPEC.md`, `SCHEDULED_TASK_PROMPT.md` | `claude/applets` |
| Misconception exercises | `math-misconceptions/` | `math-misconceptions/README.md`, `math-misconceptions/ROUTINE_PROMPT.md` | `claude/exercises` |

Work on one pipeline never edits the other's files. `math-applets/math/OPS_7-9_oppimistavoitteet.md` is shared read-only reference (curriculum goals S1-S6).

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

Follow `math-misconceptions/README.md`. Run `python tests/run_tests.py` and `python scripts/verify.py` from `math-misconceptions/` before committing.

## Git

- Merge `claude/*` branches into `main` with a merge commit, never squash: the routines merge `main` back every run.
- Commit messages in Finnish for applet work, following existing history (e.g. `Lisää applet 07: ...`).
