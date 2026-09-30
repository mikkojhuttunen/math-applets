# Practice pages (harjoittele): backlog

Work queue for a static practice platform on GitHub Pages: pupils and teachers open a link, do exercises from this repo's exercise banks, and get feedback aimed at the misconception behind a wrong answer. It replaces the paused Telegram bot (`telegram-bot/BACKLOG_BOT.md`); the comparison that led here is summarised at the end of this file.

Published at `https://mikkojhuttunen.github.io/math-applets/harjoittele/` once merged into `main`.

## How to use this file

- Take the lowest-numbered task whose state is `todo` and whose `Needs` are all `done`. Do one task per session.
- States: `todo` → `in progress` → `done`. Decisions (`WD`) are made by the teacher; Claude sets them only to `proposed` with a recommendation.
- When a task is finished: fill `Done` and `Notes` (what was built, how it was tested), run the checks in "Definition of done", commit with a message like `Harjoittele W04: vastausten tarkistus`.
- Code lives only in `harjoittele/`. It reads the exercise pipelines' files but never edits them (see `CLAUDE.md`).

## Ground rules (from decisions D1-D2 of the bot backlog and `math-misconceptions/grades1-6/EXPERT_REVIEW_REQUIRED.md`)

- No server, no AI calls, no analytics, no cookies, no accounts.
- Nothing about pupils leaves the device. No requests to other sites: no CDN scripts, no web fonts, no embedded video. The pages may fetch only JSON files from this same site.
- User-facing text in Finnish, decimal comma, U+2212 minus sign, never `NaN` or `undefined` on screen.
- Works on a school Chromebook, an iPad, a phone and a classroom projector, with keyboard and touch.

## Definition of done (every W task)

1. `cd harjoittele && npm test` passes offline (unit tests with `node:test`, no dependencies).
2. The page works when served locally: `python3 -m http.server` from the repo root, then open `http://localhost:8000/harjoittele/`. (`file://` does not allow the data fetches.)
3. The browser check (from W13 on) passes: no console errors, no requests to other origins, Finnish number format.
4. The ground rules above still hold.
5. `CHANGELOG.md` in this folder has a line for the change.

## Decisions

### WD1 Data kept on the device
- State: proposed
- Question: may the page remember progress (answered items, scores) in the browser's own storage?
- Why it matters: nothing would be sent anywhere, but `EXPERT_REVIEW_REQUIRED.md` says not to store data about grades 1-6 pupils until the sign-off, and "on the pupil's own device" is not clearly outside that.
- Recommendation: **no storage in v1.** A round keeps its score only while the page is open. Reopen after the expert review.

### WD2 Which items are shown
- State: proposed
- Question: all current items are `draft`. What does a pupil see?
- Recommendation: the practice page serves only `reviewed` (1-6) and `approved` (7-9) items. Drafts appear only in the teacher view (W10), marked `LUONNOS`. The repo is public, so drafts are not secret, just not offered to pupils. Until the teacher reviews some items, the demo shows the practice page in draft mode through the teacher view.

### WD3 Folder and URL
- State: proposed
- Recommendation: `harjoittele/` (URL `.../math-applets/harjoittele/`), practice page `index.html`, teacher view `opettaja.html`.

## Tasks

### W01 Skeleton
- State: todo
- Needs: WD3
- What: `harjoittele/index.html` (start screen placeholder), `harjoittele/css/`, `harjoittele/js/` as ES modules (`<script type="module">`, no build step), `package.json` with `"type": "module"` and `"test": "node --test"`, `CHANGELOG.md`, `README.md` (how to run locally). Same look as the front page (`index.html` colours, light and dark).
- Test: one unit test that imports a module; page opens locally with no console errors.
- Done:
- Notes:

### W02 Data manifest
- State: todo
- Needs: W01
- What: GitHub Pages cannot list folders, so the page needs a list of exercise files. `tools/build_manifest.js` reads `math-misconceptions/grades1-6/exercises/grades1-6/batch-*.json` and `math-misconceptions/exercises/*/*.json` (the 7-9 source files; `math-misconceptions/build/` is git-ignored and not published) and writes `harjoittele/data/manifest.json`: file paths, item counts by status, goal and misconception. A test fails when the manifest is out of date, so a new batch reminds whoever merges it to rebuild.
- Test: manifest from fixtures; staleness test against the real repo.
- Done:
- Notes:

### W03 Item loader
- State: todo
- Needs: W02
- What: `js/items.js` fetches the files in the manifest and turns both formats into one internal shape: `{id, source, gradeBand, goal, type, stem, answer, options, misconceptionAnswers, feedback, status}`. The 1-6 format is described in `math-misconceptions/grades1-6/exercises/grades1-6/README.md`, the 7-9 format in `math-misconceptions/schema/item.schema.json`. Unsupported types and items that need a figure are skipped and counted, never shown broken.
- Test: fixtures of both formats, every real item loads or is counted as skipped.
- Done:
- Notes:

### W04 Answer checking
- State: todo
- Needs: W01
- What: `js/answers.js`: normalise a typed answer (spaces, decimal comma or point, U+2212 or hyphen minus, fractions `3/4`, mixed numbers `1 1/2`, trailing units) and compare with the item's answer: `correct`, `wrong` or `unreadable`. Must agree with the Python checkers (`math-misconceptions` schema and backlog section 1.3; `grades1-6/tools/exercise_pipeline/verify_items.py`). Taken over from bot task B05.
- Test: table of inputs, plus every `answer` and every misconception answer in the real banks must parse.
- Done:
- Notes:

### W05 Misconception feedback texts
- State: todo
- Needs: W01
- What: `tools/build_misconceptions.py` turns the `Misconceptions` sheet of `math-misconceptions/sources/math_misconceptions_item_bank.xlsx` and the sub-variants in `grades1-6/tools/buggy_rules/buggy_rules.py` (for example `NUM-10a`) into `data/misconceptions_fi.json`: id → short Finnish feedback for the pupil (what went wrong, one hint, no full solution) and a note for the teacher. The xlsx descriptions are in English, so the Finnish texts are written here and marked `draft` until the teacher reviews them. Taken over from bot task B06.
- Test: every misconception id used in the banks has an entry.
- Done:
- Notes:

### W06 Practice round, typed answers
- State: todo
- Needs: W03, W04, W05, WD1, WD2
- What: the practice page: a round of 5 items, a large answer field with an on-screen number pad for tablets, "Tarkista" button. A wrong answer that matches one of the item's misconception answers shows that misconception's feedback; any other wrong answer gets a general hint and a second try; after the second try the correct answer is shown. Summary at the end ("4/5 oikein") with "Uusi kierros". Nothing stored (WD1).
- Test: browser test of a full round, including a misconception answer, an unreadable answer and the summary.
- Done:
- Notes:

### W07 Choice items
- State: todo
- Needs: W06
- What: `choice` (1-6) and `MC`, `TF` (7-9) items as large buttons in shuffled order; wrong options mapped to misconception feedback like W06.
- Test: shuffled order still grades right; keyboard selection works.
- Done:
- Notes:

### W08 Start screen and shareable links
- State: todo
- Needs: W06
- What: choose grade band, then topic (curriculum goal) or misconception, showing only choices that have items. Every choice is also a URL parameter (`?tavoite=A36.S2.04`, `?luokat=3-6`, `?virhe=NUM-10`) so a teacher can share one link or QR code for a lesson.
- Test: each parameter, a parameter with no items gives a Finnish message.
- Done:
- Notes:

### W09 Visual feedback for column arithmetic
- State: todo
- Needs: W06
- What: for the subtraction misconceptions (`NUM-10a`, `NUM-10b`, `NUM-10c`), show the pupil's answer and the correct one in columns and highlight the column where they differ. Pattern for later visual feedback on other misconceptions, and for links to matching applets.
- Test: rendering for each sub-variant with the real batch items.
- Done:
- Notes:

### W10 Teacher view
- State: todo
- Needs: W03
- What: `opettaja.html`: all items including drafts (`LUONNOS` badge), filter by status, goal and misconception, each item with its answer, misconception answers and feedback. "Kokeile" opens that item on the practice page. A print layout for a worksheet with an answer key on a separate page. The page does not change item status; it lists the ids to mark reviewed in the JSON.
- Test: counts match the manifest; print stylesheet hides controls.
- Done:
- Notes:

### W11 Goal browser
- State: todo
- Needs: W03
- What: the curriculum goals of both OPS files (`math-misconceptions/grades1-6/data/curriculum/OPS_1-6_oppimistavoitteet.md`, `math-applets/math/OPS_7-9_oppimistavoitteet.md`) as a searchable list: each goal with its exercise count and a practice link. Goals are read at build time into `data/goals.json` by a tool like W02. Taken over from bot task B04.
- Test: exact id and text search, goal with no items.
- Done:
- Notes:

### W12 Link from the front page
- State: todo
- Needs: W06
- What: one link to `harjoittele/` in the root `index.html`. That file belongs to the applets pipeline, so this is done only with the teacher's OK, in its own commit, touching nothing else.
- Done:
- Notes:

### W13 Automated page check
- State: todo
- Needs: W06
- What: `tools/check_pages.js` with Playwright (Chromium is preinstalled in the Claude environment): opens each page, fails on console errors, requests to other origins, `NaN`/`undefined` on screen, a decimal point in shown numbers, missing `lang="fi"`, or horizontal scrolling at 360 px width. Plus a GitHub Actions workflow `.github/workflows/harjoittele.yml` running the unit tests and this check on pull requests that touch `harjoittele/`.
- Test: the check itself fails on a deliberately broken fixture page.
- Done:
- Notes:

### W14 Demo release v1.0
- State: todo
- Needs: W07, W08, W10, W12, W13
- What: `README.md` section for teachers in Finnish (how to share a link, what is and is not stored), a QR code image for the practice page, version 1.0.0 in `CHANGELOG.md`.
- Done:
- Notes:

## Later

- **W20 Progress on the device** (needs WD1 reopened after the expert review): remember finished items in `localStorage` on that device only, with a clear "Tyhjennä" button.
- **W21 Offline use**: a service worker so a class can practise without a network after the first visit.
- **W22 Class results for the teacher**: only with a separate privacy decision; needs a backend and would store pupil data, so it is outside the ground rules above.

## Why a web page instead of the Telegram bot (2026-09-30)

| | Telegram bot | Web page on GitHub Pages |
|---|---|---|
| Hosting | Server needed (Railway, webhook, secrets, redeploys) | None; publishing from `main` already runs |
| Who can use it | Needs a Telegram account; minimum age and school practice keep pupils out | Any browser, no account; link or QR in Classroom, Peda.net, Wilma |
| Interaction | Text and buttons, maths as Unicode only | Full HTML: number pad, column layouts, links to applets |
| Privacy | Telegram ids are personal data | Can be built to send nothing anywhere |
| Content updates | Redeploy | Merge to `main` |
| What it cannot do | Nothing blocks it, but it cannot reach pupils | No push messages or reminders; no class results without a backend; answers visible in page source (fine for practice, not for tests) |

## Log

| Date | Task | Result |
|---|---|---|
| 2026-09-30 | backlog | Created; Telegram bot paused at B01 |
