# Publishing the site: backlog

Work queue for getting the whole site live on GitHub Pages and testable on a laptop: applets and exercises of every school level, from one address. Practice-page features have their own queue in `harjoittele/BACKLOG_WEB.md`; this file is about publishing, testing and what is still missing for a demo.

## How to use this file

- Teacher steps (`T`) are done by the teacher in GitHub or on the laptop. Claude tasks (`L`) are done one at a time, lowest number first, when their `Needs` are done.
- States: `todo` → `in progress` → `done`; `needs OK` = touches another pipeline's files (see `CLAUDE.md`) and waits for the teacher's approval.
- Claude cannot open `*.github.io` from its environment, so anything about the live site is checked by the teacher or by a GitHub Actions workflow (L02).

## Where things stand (2026-10-01)

| | State |
|---|---|
| GitHub Pages | **Not enabled** (repository setting `has_pages: false`). Nothing is live. |
| If enabled from `main` today | The front page and all 20 applets would work: no file uses Jekyll/Liquid syntax and every front-page link resolves. The practice pages on `main` are still at W03 and show only a placeholder. |
| Branch `claude/keen-hopper-75z03v` | Practice pages W01-W13: start screen, rounds with feedback, teacher view, goal browser, checks and CI. Not yet merged. |
| Exercises | 1010 items, all `draft`. The practice page can show 740 (grades 1-6: 400, grades 7-9: 340) on 36 curriculum goals. 270 grades 7-9 items are of five types it cannot show yet: ES 75, RP 60, FS 55, ME 45, SO 35. |
| Applets | 20 on the front page. 9 pass `scripts/check_applet.js`; 11 fail (mostly applets imported in English before `APPLET_SPEC.md`). |
| Speed | Every practice page load fetches all 143 exercise files. Fine on a laptop, slow on a phone. |

## Teacher steps

### T1 Merge the branch into `main`
- State: todo
- `git fetch origin`, `git checkout main`, `git pull origin main`, `git merge --no-ff origin/claude/keen-hopper-75z03v`, `git push origin main`. The push starts the `harjoittele` workflow; check it under Actions.

### T2 Enable GitHub Pages
- State: todo
- Needs: T1
- GitHub → repository → Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch **main**, folder **/ (root)** → Save. After a minute or two the site is at `https://mikkojhuttunen.github.io/math-applets/`. Every later push to `main` republishes it.

### T3 Test on the laptop
- State: todo
- Needs: T2 (or L04 for a local copy)
- Start from the test page (L03) or from these addresses:
  - front page and applets: `https://mikkojhuttunen.github.io/math-applets/`
  - exercises, draft preview: `https://mikkojhuttunen.github.io/math-applets/harjoittele/?luonnokset=1`
  - teacher view: `https://mikkojhuttunen.github.io/math-applets/harjoittele/opettaja.html`
  - curriculum goals: `https://mikkojhuttunen.github.io/math-applets/harjoittele/tavoitteet.html?sisalto=1`
- Note what is wrong per page; the findings become new tasks here or in the pipeline backlogs.

### T4 Review a first set of exercises
- State: todo
- Pupils see only reviewed items (decision WD2). For a demo without the preview link, review for example one topic per grade band in the teacher view, copy the ids, set `status` in the JSON files and run `node tools/build_manifest.js` in `harjoittele/`.

## Claude tasks

### L01 Publish files as they are (`.nojekyll`)
- State: done (2026-10-01)
- What: an empty `.nojekyll` file at the repository root, so GitHub Pages skips Jekyll. Today nothing breaks the Jekyll build, but the routines write Markdown backlogs every hour, and a single `{{` or `{%` in any of them would make Liquid fail the whole site build. Without Jekyll, Markdown files are served as plain text instead of rendered pages, which no page relies on, and publishing is quicker.
- Notes: Empty `.nojekyll` added at the root. Checked beforehand that no page depends on Jekyll (no front matter, no Liquid, no `_` folders the site needs).

### L02 Check the live site after each publish
- State: todo
- Needs: T2
- What: `tools/check_pages.js` gets a `--base <url>` option to check the live site instead of a local copy; a workflow `.github/workflows/pages-live.yml` runs it after each GitHub Pages deployment (and by hand) and fails if a page is missing, broken or breaks the rules. Also checks that every front-page link answers.

### L03 Test page for all school levels
- State: todo
- What: `harjoittele/testaa.html`, one page for a tester on a laptop: per school level (luokat 1-2, 3-6, 7-9, lukio pitkä, lukio lyhyt) the applets (read from the front page) and the practice topics with item counts and draft-preview links, plus links to the teacher view and the goal browser, and a short checklist of what to try. Linked from the practice page footer.

### L04 Run the site on the laptop without GitHub
- State: done (2026-10-01)
- What: `TESTING.md` at the root: clone or download the repository, start `python3 -m http.server 8000` (or `py -m http.server 8000` on Windows) in its folder and open `http://localhost:8000/`. Explains why opening the files directly (`file://`) works for applets but not for the practice pages. Includes the test addresses of T3 for `localhost`.
- Notes: `TESTING.md`: published addresses, local copy with `git clone` or Download ZIP and `python3 -m http.server 8000` (`py -m http.server 8000` on Windows), why `file://` is not enough for the practice pages, and what to try.

### L05 Faster loading of exercises
- State: todo
- What: `tools/build_manifest.js` also writes `harjoittele/data/items.json`, one file with every item the pages can show, so a page makes one request instead of 143. Measure load time before and after on the throttled "Fast 3G" profile; keep the per-file loading as a fallback.

### L06-L10 The five grades 7-9 item types the practice page cannot show
- State: todo (one task each; 270 items in total)
- L06 `ES` error spotting (75 items): solution lines shown, the pupil taps the first wrong line.
- L07 `RP` (60): payload `constraint` and `checks{valid, invalid}`; read the schema and an item first, then design the interaction with the teacher.
- L08 `FS` fill in a step (55): one line of a solution is blank; typed answer checked like an expression or equation.
- L09 `ME` matching equivalent expressions (45): choose every expression equivalent to the reference.
- L10 `SO` step ordering (35): put solution lines in order (buttons up/down, works with keyboard and touch).
- Each one: loader support in `js/items.js`, checking in `js/answers.js` that agrees with `math-misconceptions/scripts/verify.py`, rendering, unit and browser tests, and the teacher view card.

### L11 Applets that fail the applet check
- State: needs OK (applets pipeline)
- What: 11 applets fail `node scripts/check_applet.js`: `yla-aste-7-9/` heita-sikaa, kolikko-ja-noppa, kustannusvertailu, prosenttimuutos, sekoitusongelma, trig-explorer; `lukio-pitka/` Vector_addition, complex-plane-explorer, derivative_visualizer, integral-speed-distance; `lukio-lyhyt/` makeishinnoittelu, pokerikasien-todennakoisyydet. Report what fails in each, then the teacher decides per applet: fix, translate, or mark as "vanha" on the front page.

### L12 Remove the stray copies at the repository root
- State: needs OK (grades 1-6 pipeline)
- What: `BACKLOG_1-6.md`, `EXPERT_REVIEW_REQUIRED.md`, `ROUTINE_PROMPT_1-6.md`, `data/`, `docs/`, `exercises/`, `tools/` and `math-applets/yla-aste-7-9/` at the root are older copies of grades 1-6 files and applets. They are published too, and `.github/workflows/verify-exercises.yml` checks them instead of `math-misconceptions/grades1-6/`, so the real batches are not verified on pull requests. Point the workflow at `math-misconceptions/grades1-6/` and delete the copies, after checking nothing reads them.

### L13 Practice links on the front page per level
- State: needs OK (applets pipeline)
- Needs: L03
- What: under each level heading of the root `index.html`, one line linking to that level's practice topics, so a visitor finds exercises next to the applets.

## Log

| Date | Task | Result |
|---|---|---|
| 2026-10-01 | backlog | Created. Pages not enabled; `main` would publish the front page and applets; branch not merged; 740 of 1010 items showable |
| 2026-10-01 | L01, L04 | `.nojekyll`; `TESTING.md` |
