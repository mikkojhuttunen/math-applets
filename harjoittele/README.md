# Harjoittele: practice pages

Static practice pages on GitHub Pages for the exercise banks in this repository. No server, no AI calls, no cookies, nothing stored or sent anywhere. Work queue and ground rules: `BACKLOG_WEB.md`.

## Layout

| Path | Role |
|---|---|
| `index.html` | Practice page: start screen, then rounds. Links: `?tavoite=A36.S2.04`, `?luokat=1-6`, `?virhe=NUM-10`; `?tehtava=<id>` one item; `?luonnokset=1` previews drafts |
| `opettaja.html` | Teacher view: all items and feedback texts, review selection, printable worksheet |
| `tarkista.html` | Review page: draft items one at a time with verdicts (approve, fix, reject), results as a file per reviewer, and a merge tab for the collector. Filters in the URL: `?lk=7-9&aihe=ALG-04&tyyppi=valinta&kaikki=1` |
| `testaa.html` | Test page: applets and practice topics per school level, draft previews |
| `tavoitteet.html` | Goal browser: curriculum goals with exercises, practice links and applets (`?haku=`, `?luokat=`) |
| `css/style.css` | Shared styles, light and dark |
| `js/` | ES modules loaded directly by the browser, no build step |
| `data/manifest.json` | List of exercise files and counts, built by `tools/build_manifest.js` |
| `data/misconceptions_source.json` | English misconception catalogue, built by `tools/extract_misconceptions.py` |
| `data/misconceptions_fi.json` | Finnish feedback per misconception, written by hand |
| `data/goals.json` | Curriculum goals of grades 1-9, built by `tools/build_goals.js` |
| `data/topics_fi.json` | Pupil-facing topic titles per goal, written by hand |
| `data/goal_applets.json` | Applets per goal, written by hand; add a line when a new applet covers a goal |
| `tools/` | Build scripts run with Node before committing |
| `test/` | Unit tests (`node:test`), no dependencies |

## Run locally

The pages fetch data files, which browsers block on `file://`, so serve the repo root:

```
cd harjoittele
npm test
cd ..
python3 -m http.server 8000
```

Then open `http://localhost:8000/harjoittele/`. All exercises are drafts for now, so use `http://localhost:8000/harjoittele/?luonnokset=1` to try a round.

Browser checks (Chromium through Playwright, which is not a dependency of this folder; use a globally installed Playwright with `NODE_PATH`, or `npm install --no-save playwright@1.56.1`):

```
cd harjoittele
NODE_PATH=$(npm root -g) node tools/check_pages.js --self-test
NODE_PATH=$(npm root -g) node tools/check_pages.js
NODE_PATH=$(npm root -g) node tools/browser_test.js
```

`check_pages.js` sweeps every page for errors, requests to other sites, Finnish number format and phone width; `browser_test.js` clicks through a round, the teacher view and the goal browser.

## Continuous integration

- `.github/workflows/harjoittele.yml`: on pull requests and pushes to `main` touching `harjoittele/` or the front page, runs `npm test`, the page check (with its self-test) and the browser test.
- `.github/workflows/harjoittele-content.yml`: on pull requests changing exercise batches, curriculum goals or misconception sources, warns if `harjoittele/data/` needs rebuilding. It never fails, because those pull requests come from other pipelines.

## Reviewing exercises with colleagues

1. Share a link to `tarkista.html`, optionally with a filter that splits the work (`?lk=7-9&aihe=ALG-04`, `?lk=1-6`). Each reviewer writes a name, goes through the items, and presses "Lataa tiedostoksi". Verdicts stay in the browser (localStorage) until the reviewer clears them; the page sends nothing anywhere.
2. The collector opens the "Yhdistä" tab, adds the reviewers' files (and optionally their own verdicts) and chooses how many approvals are needed. The tab lists the items that are ready, the conflicts and the comments on items to fix.
3. "Lataa päivitetyt tiedostot (.zip)" downloads the exercise files with the ready items set to `approved` (grades 7-9) or `reviewed` (grades 1-6), plus the updated `data/manifest.json`, with paths from the repository root. Run `git pull`, unzip over the repository (`unzip -o`), check `git status --short`, then commit and push. The files are fetched from the published site, so everything must be pushed first. Grades 1-6 also need the sign-off in `EXPERT_REVIEW_REQUIRED.md`.
4. Alternative from a list of ids: `node tools/set_status.js hyvaksytyt-<date>.txt` (use `--dry` first), then `node tools/build_manifest.js` and `npm test`. Both routes use `js/status_edit.js` and give identical files.

Item types the pupil pages cannot show yet (ES, RP, ME, FS, SO in grades 7-9) are not in the review page either. `review/` keeps id lists of items that have been checked by hand.

## Reviewing exercises and feedback texts (old way)

Open `opettaja.html`, tick what you approve and press "Kopioi tunnisteet". The copied list says which file each id is in and which `status` value to set: `reviewed` for grades 1-6 items and feedback texts, `approved` for grades 7-9 items. Edit the files, then run `node tools/build_manifest.js` and `npm test` here. The grades 1-6 verifier accepts reviewed items only with `--allow-reviewed` (see `math-misconceptions/grades1-6/exercises/grades1-6/README.md`).

## Reviewing the Finnish feedback texts

Each entry in `data/misconceptions_fi.json` has `pupil` (shown after a wrong answer), `teacher` (teacher view) and `status`. Pupils see a text only when its `status` is `reviewed`; edit the text if needed and change `draft` to `reviewed`. Then run `npm test`.

When the item bank xlsx, the 7-9 backlog's EXT table or `buggy_rules.RULES` changes, run `python3 tools/extract_misconceptions.py`; the tests then list any id that still needs a Finnish text.

## When exercise batches change

```
cd harjoittele
node tools/build_manifest.js
npm test
```

If a batch uses a goal that has no title yet, the tests say so: add it to `data/topics_fi.json`. If a curriculum goal file changes, run `node tools/build_goals.js`.
