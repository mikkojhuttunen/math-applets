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
3. The browser check passes: `NODE_PATH=$(npm root -g) node tools/browser_test.js` prints `BROWSER TEST OK` (no console errors, no requests to other origins, no `NaN`, no horizontal scroll). W13 turns it into a general page check and a CI workflow.
4. The ground rules above still hold.
5. `CHANGELOG.md` in this folder has a line for the change.

## Decisions

### WD1 Data kept on the device
- State: done (2026-09-30, recommendation accepted)
- Question: may the page remember progress (answered items, scores) in the browser's own storage?
- Why it matters: nothing would be sent anywhere, but `EXPERT_REVIEW_REQUIRED.md` says not to store data about grades 1-6 pupils until the sign-off, and "on the pupil's own device" is not clearly outside that.
- Recommendation: **no storage in v1.** A round keeps its score only while the page is open. Reopen after the expert review.

### WD2 Which items are shown
- State: done (2026-09-30, recommendation accepted)
- Question: all current items are `draft`. What does a pupil see?
- Recommendation: the practice page serves only `reviewed` (1-6) and `approved` (7-9) items. Drafts appear only in the teacher view (W10), marked `LUONNOS`. The repo is public, so drafts are not secret, just not offered to pupils. Until the teacher reviews some items, the demo shows the practice page in draft mode through the teacher view.

### WD3 Folder and URL
- State: done (2026-09-30, recommendation accepted)
- Recommendation: `harjoittele/` (URL `.../math-applets/harjoittele/`), practice page `index.html`, teacher view `opettaja.html`.

## Tasks

### W01 Skeleton
- State: done
- Needs: WD3
- What: `harjoittele/index.html` (start screen placeholder), `harjoittele/css/`, `harjoittele/js/` as ES modules (`<script type="module">`, no build step), `package.json` with `"type": "module"` and `"test": "node --test"`, `CHANGELOG.md`, `README.md` (how to run locally). Same look as the front page (`index.html` colours, light and dark).
- Test: one unit test that imports a module; page opens locally with no console errors.
- Done: 2026-09-30, v0.1.0
- Notes: `index.html` shows a placeholder until W06. `js/format.js` has `formatNumber()` for later pages; a helper that rewrote decimals in whole texts was dropped because it turned ids such as `A36.S2.04` into `A36.S2,04`, and the bank texts are already in Finnish format. Checked: `npm test` (2 tests), and Playwright against `python3 -m http.server` at 360 px width: status text rendered, no console errors, no requests to other origins, no horizontal scroll.

### W02 Data manifest
- State: done
- Needs: W01
- What: GitHub Pages cannot list folders, so the page needs a list of exercise files. `tools/build_manifest.js` reads `math-misconceptions/grades1-6/exercises/grades1-6/batch-*.json` and `math-misconceptions/exercises/*/*.json` (the 7-9 source files; `math-misconceptions/build/` is git-ignored and not published) and writes `harjoittele/data/manifest.json`: file paths, item counts by status, goal and misconception. A test fails when the manifest is out of date, so a new batch reminds whoever merges it to rebuild.
- Test: manifest from fixtures; staleness test against the real repo.
- Done: 2026-09-30, v0.2.0
- Notes: `tools/build_manifest.js` writes `data/manifest.json` (paths relative to `harjoittele/`, counts by status, goal and misconception; no timestamps, so it only changes when the banks change). `--check` exits 1 when stale. The 7-9 source files are wrappers `{schema_version, topic, type, items}`; their items carry Finnish feedback per wrong answer in `payload.wrong`, useful for W03/W06. Fixtures: 3 real 1-6 items (one set to `reviewed`) and 2 items from `generators/example_alg08_ne.py` (one set to `approved`). Current repo: 2 files, 40 items, all draft. 4 new tests, including one that fails when the manifest is out of date.

### W03 Item loader
- State: done
- Needs: W02
- What: `js/items.js` fetches the files in the manifest and turns both formats into one internal shape: `{id, source, gradeBand, goal, type, stem, answer, options, misconceptionAnswers, feedback, status}`. The 1-6 format is described in `math-misconceptions/grades1-6/exercises/grades1-6/README.md`, the 7-9 format in `math-misconceptions/schema/item.schema.json`. Unsupported types and items that need a figure are skipped and counted, never shown broken.
- Test: fixtures of both formats, every real item loads or is counted as skipped.
- Done: 2026-09-30, v0.3.0
- Notes: `js/items.js`: `loadItems(manifestUrl, {includeDrafts})` returns `{items, skipped, errors}`. Supported now: 1-6 `numeric_entry` and `choice`, 7-9 `NE` (answer kinds number, set, expression) and `MC`. Skipped with a reason: other types, items with `prompt.figure`, duplicate ids, a choice answer that is not exactly one option, and drafts unless `includeDrafts` (WD2). A file that fails to load is reported and the rest still load. 1-6 answers stay as typed text (`{kind: 'typed'}`) for W04 to parse; 1-6 misconception answers have `feedback: null` until W05 supplies the texts, while 7-9 items bring their own Finnish feedback. 7 new tests, including all 40 real items. Browser check: `loadItems` in Chromium against `python3 -m http.server` gives 40 items with drafts, 0 without.

### W04 Answer checking
- State: done
- Needs: W01
- What: `js/answers.js`: normalise a typed answer (spaces, decimal comma or point, U+2212 or hyphen minus, fractions `3/4`, mixed numbers `1 1/2`, trailing units) and compare with the item's answer: `correct`, `wrong` or `unreadable`. Must agree with the Python checkers (`math-misconceptions` schema and backlog section 1.3; `grades1-6/tools/exercise_pipeline/verify_items.py`). Taken over from bot task B05.
- Test: table of inputs, plus every `answer` and every misconception answer in the real banks must parse.
- Done: 2026-09-30, v0.4.0
- Notes: `js/answers.js`: `checkAnswer(item, typed)` and `checkChoice(item, optionId)` return `{result, misconception, feedback, ambiguous}`, like `classify()` in `buggy_rules.py` (one matching stored wrong answer gives its misconception, two or more give `ambiguous`). Numbers are exact BigInt fractions; `parseNumber` gives the same result as `buggy_rules.parse_answer` on 24 shared inputs (checked by running both), and also accepts thousands spaces (`1 000`) and known units (`5 cm`, `12 €`, `90°`; a list, so `2x` is not read as 2). Sets accept `2; −3`, `2 tai −3`, `x = 2, x = −3` (comma needs a following space, since `2,5` is a decimal). Expressions: a small parser (implicit multiplication, `²`, `·`, `÷`, single-letter variables) compared at the item's samples plus the extra points of `verify.py`'s POOL; at least 3 valid points needed. 12 new tests, including every answer and stored wrong answer of the 40 real items and the example generator's 7-9 items.

### W05 Misconception feedback texts
- State: done
- Needs: W01
- What: `tools/build_misconceptions.py` turns the `Misconceptions` sheet of `math-misconceptions/sources/math_misconceptions_item_bank.xlsx` and the sub-variants in `grades1-6/tools/buggy_rules/buggy_rules.py` (for example `NUM-10a`) into `data/misconceptions_fi.json`: id → short Finnish feedback for the pupil (what went wrong, one hint, no full solution) and a note for the teacher. The xlsx descriptions are in English, so the Finnish texts are written here and marked `draft` until the teacher reviews them. Taken over from bot task B06.
- Test: every misconception id used in the banks has an entry.
- Done: 2026-09-30, v0.5.0
- Notes: Split in two files. `tools/extract_misconceptions.py` (standard library only, reads the xlsx as zip/XML) writes `data/misconceptions_source.json`: the English reference for 54 ids (42 from the xlsx sheet, 9 `EXT-` topics from section 3.2 of the 7-9 backlog, 3 sub-variants `NUM-10a`-`c` from `buggy_rules.RULES`). `data/misconceptions_fi.json` is written by hand: per id `name_fi`, `pupil` (what went wrong and one hint, never the answer, at most 220 characters), `teacher` (the typical error with the xlsx example, and a classroom idea), `applets` (existing applet paths) and `status: draft`. `js/misconceptions.js`: `feedbackFor()` falls back from a sub-variant to its parent and returns draft texts only with `includeDrafts`, like exercises under WD2. MEA-02 and EXT-07 describe the same error (noted in both teacher texts). Six new tests: same ids in both files, Finnish number format, lengths, applet paths exist, every misconception used by the banks has a text, source file up to date. **Teacher review needed:** set `status` to `reviewed` per entry; until then pupils see the general hint.

### W06 Practice round, typed answers
- State: done
- Needs: W03, W04, W05, WD1, WD2
- What: the practice page: a round of 5 items, a large answer field with an on-screen number pad for tablets, "Tarkista" button. A wrong answer that matches one of the item's misconception answers shows that misconception's feedback; any other wrong answer gets a general hint and a second try; after the second try the correct answer is shown. Summary at the end ("4/5 oikein") with "Uusi kierros". Nothing stored (WD1).
- Test: browser test of a full round, including a misconception answer, an unreadable answer and the summary.
- Done: 2026-09-30, v0.6.0
- Notes: `js/round.js` (pure, unit-tested) runs a round of 5: unreadable answers do not use a try; the first wrong answer shows the item's own feedback (7-9), else the misconception text from W05, else a general hint; the second wrong answer reveals the correct answer (and `solution.steps` when present); summary counts correct and first-try answers. Choice items already work through the same flow (buttons; a wrongly chosen option is disabled), so W07 only has to add shuffling and keyboard checks. `js/main.js` renders it: large answer field, on-screen number pad (0-9, `,`, `−`, `/`, space, delete, clear; `x ( ) +` added for expression answers; pad taps keep the cursor), Enter submits, feedback directly under the field so it stays visible on a 375 × 667 phone, `aria-live` feedback. DOM built with `textContent` only. Nothing stored. **Draft preview** `?luonnokset=1` (WD2): drafts and draft feedback texts, a yellow LUONNOS banner, item id and misconception id shown; without it pupils currently see "no reviewed exercises yet". Bug found by the browser test and fixed: after the second wrong answer `current()` returned null and the reveal crashed. Tests: 9 unit tests for the round; `tools/browser_test.js` (Playwright, run separately) plays a full draft round in Chromium at 360 px: unreadable answer, misconception answer, reveal, number-pad input with delete, Enter, summary 4/5, new round; plus pupil view, no console errors, no foreign requests, no NaN, no horizontal scroll, `lang="fi"`. Screenshots checked in light and dark.

### W07 Choice items
- State: done
- Needs: W06
- What: `choice` (1-6) and `MC`, `TF` (7-9) items as large buttons in shuffled order; wrong options mapped to misconception feedback like W06.
- Test: shuffled order still grades right; keyboard selection works.
- Done: 2026-10-01, v0.8.0
- Notes: Grading and feedback for choice items were already in W06. Added `presentOptions()` in `js/round.js`: options in a new random order each time, lettered A, B, C ... on large buttons; the letter keys choose an option when no text field has focus; a wrongly chosen option is disabled. 1 new unit test (shuffled order grades by id, the item itself is not changed); browser test chooses the wrong option by click and the right one by its letter key. Real choice items now in the banks: 20 `A36.S2.11` comparisons (`NUM-12`).

### W08 Start screen and shareable links
- State: done
- Needs: W06
- What: choose grade band, then topic (curriculum goal) or misconception, showing only choices that have items. Every choice is also a URL parameter (`?tavoite=A36.S2.04`, `?luokat=3-6`, `?virhe=NUM-10`) so a teacher can share one link or QR code for a lesson.
- Test: each parameter, a parameter with no items gives a Finnish message.
- Done: 2026-10-01, v0.9.0
- Notes: Start screen "Valitse aihe": goals that have items, grouped by grade band, with item counts, plus "Kaikki aiheet sekaisin". Topic names for pupils come from the hand-written `data/topics_fi.json` (3 titles now: A36.S2.04 "Yhteen- ja vähennyslasku allekkain", A36.S2.11 "Murtolukujen vertailu", A36.S2.12 "Murtolukujen yhteenlasku"; teacher may reword), falling back to the curriculum text. A test fails when a bank uses a goal with no title, as a reminder. URL parameters `?tavoite=`, `?luokat=`, `?virhe=` (combinable, `luonnokset=1` kept), set with `history.pushState`, so links are shareable and Back returns to the start screen; a choice with no items says so. The round shows the topic and a "Vaihda aihe" link; the summary has "Uusi kierros" and "Vaihda aihe". The teacher view shows the pupil link for its current goal / band / misconception filters. To support this, `tools/build_goals.js` builds `data/goals.json` (128 goals from section 3 of both curriculum files, with area and 7-9 grade), which is also the data W11 needs. `js/teacher_logic.js` renamed `js/filters.js` (shared). 6 new unit tests; browser test covers the start screen, topic link, URL, items all on the chosen goal, Back, an unknown goal, and the pupil link.

### W09 Visual feedback for column arithmetic
- State: done
- Needs: W06
- What: for the subtraction misconceptions (`NUM-10a`, `NUM-10b`, `NUM-10c`), show the pupil's answer and the correct one in columns and highlight the column where they differ. Pattern for later visual feedback on other misconceptions, and for links to matching applets.
- Test: rendering for each sub-variant with the real batch items.
- Done: 2026-10-01, v0.10.0
- Notes: `js/columns.js` (pure): `parseSubtraction()` reads `Laske A − B.` stems, `columnLayout()` right-aligns the digits, works out the correct column method (including borrowing across a zero) and lists the columns where the pupil's answer differs. On the practice page, any wrong whole-number answer to a subtraction item (not only stored misconception answers) shows the sum in columns: after the first try only the pupil's row with the wrong columns in red (no correct digits, so the second try is still theirs); after the second try also the borrow marks above the top row and the correct row in green. With 453 − 127 the three NUM-10 variants mark different columns: 10a tens and ones, 10b ones, 10c tens. Single-item mode now shows the topic name instead of the id. 6 new unit tests, including every stored wrong answer of the 40 real subtraction items; the browser test checks the marked columns on the first try and the correct row and borrows after the second. Addition and other operations are not covered yet: the parser only accepts subtraction.

### W10 Teacher view
- State: done
- Needs: W03
- What: `opettaja.html`: all items including drafts (`LUONNOS` badge), filter by status, goal and misconception, each item with its answer, misconception answers and feedback. "Kokeile" opens that item on the practice page. A print layout for a worksheet with an answer key on a separate page. The page does not change item status; it lists the ids to mark reviewed in the JSON.
- Test: counts match the manifest; print stylesheet hides controls.
- Done: 2026-10-01, v0.7.0
- Notes: Done before W07-W09 at the teacher's request, to make reviewing easier. `opettaja.html` + `js/teacher.js` (DOM) + `js/teacher_logic.js` (filtering and counts, unit-tested). Tab **Tehtävät**: filters by status, grade band, goal, misconception (including sub-variants and their parents) and free text; each card shows id, status badge, goal, level, source file, correct answer, every stored wrong answer or wrong option with its misconception name and the pupil feedback (draft texts marked), and a **Kokeile** link that opens the item alone on the practice page (`index.html?luonnokset=1&tehtava=<id>`, added to `js/main.js`). Tab **Palautetekstit**: the 54 Finnish texts with pupil and teacher text, applet links and how many items use each. **Review**: checkboxes on items and texts, "Valitse näkyvät", and "Kopioi tunnisteet", which copies the ids grouped by file with the status value to set (`reviewed` for 1-6 and texts, `approved` for 7-9); a text box appears if the clipboard is blocked. The page never edits the JSON. Selections are kept in this browser's `localStorage` (teacher's own work, not pupil data) until cleared. **Print**: "Tulosta moniste" prints the filtered items as a worksheet (name and date lines, answer lines, tick boxes for choices) with the answer key on a new page. Shared `js/dom.js`. `loadItems` now adds `file` to each item. Fixes found by the browser test: `[hidden]` did not hide elements with their own `display` (global rule added); long misconception names in the filter made the page 531 px wide at 360 px (filters now shrink). Browser test rewritten to be deterministic now that the banks have 100 items and choice items: single typed item (unreadable, misconception, reveal), single choice item, a full random round answered correctly (one item through the number pad), and the teacher view (count, filters, card content, selection, copy list, selection kept after reload, clearing, feedback tab, print sheet). Screenshots checked: desktop, 375 px phone, print layout.

### W11 Goal browser
- State: done
- Needs: W03
- What: the curriculum goals of both OPS files (`math-misconceptions/grades1-6/data/curriculum/OPS_1-6_oppimistavoitteet.md`, `math-applets/math/OPS_7-9_oppimistavoitteet.md`) as a searchable list: each goal with its exercise count and a practice link. Goals are read at build time into `data/goals.json` by a tool like W02. Taken over from bot task B04.
- Test: exact id and text search, goal with no items.
- Done: 2026-10-01, v0.11.0
- Notes: `tavoitteet.html` + `js/goals_page.js` (DOM) + `js/goals_view.js` (rows, search, grouping; unit-tested). All 128 goals of `data/goals.json` (built in W08) grouped by grade band (1-2, 3-6, 7-9) and content area. Each goal: id, 7-9 grade, "Oppilas osaa …" text, exercise count with how many are reviewed, the pupil topic title when there is one, a practice link (`index.html?tavoite=`) when reviewed items exist or a draft preview link when only drafts exist, related applets, and the misconceptions its items cover. Search by exact id (shows just that goal) or by word in id, text or area; band filter; "only goals with exercises or applets" (9 goals now). Filters are in the URL (`?haku=`, `?luokat=`, `?sisalto=1`). Applets per goal come from the new hand-written `data/goal_applets.json` (7 goals, 9 applets), based on section 7 of the 7-9 curriculum file and the front page's topic lines; `pythagoras-neliot`, listed there, does not exist and is left out. A test checks that every goal and applet in it exists. Applet names are read from the front page's own links, so they follow `index.html`. Links to the goal browser from the teacher view and from the practice page footer ("Opettajalle: …"). 5 new unit tests; the browser test checks the full list, exact id search, practice link, URL, band filter and an applet link, at 360 px.

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
| 2026-09-30 | WD1-WD3 | Accepted: no storage in v1, pupils see reviewed items only, folder `harjoittele/` |
| 2026-09-30 | W01 | Skeleton, v0.1.0 |
| 2026-09-30 | W02 | Manifest, v0.2.0: 2 files, 40 draft items |
| 2026-09-30 | W03 | Item loader, v0.3.0: 40 items load, all draft |
| 2026-09-30 | W04 | Answer checking, v0.4.0: agrees with parse_answer on 24 inputs |
| 2026-09-30 | W05 | Finnish texts for 54 misconceptions, all draft, v0.5.0 |
| 2026-09-30 | W06 | Practice round with number pad, draft preview, v0.6.0; browser test OK |
| 2026-10-01 | merge | `main` merged in: 3 new grades 1-6 batches (A36.S2.11 choice, A36.S2.12 fractions); manifest rebuilt, 100 items, all load and grade correctly |
| 2026-10-01 | W10 | Teacher view, v0.7.0; browser test OK |
| 2026-10-01 | W07 | Choice items shuffled and lettered, letter keys, v0.8.0 |
| 2026-10-01 | W08 | Start screen, shareable topic links, goals.json, v0.9.0 |
| 2026-10-01 | W09 | Subtraction in columns after a wrong answer, v0.10.0 |
| 2026-10-01 | W11 | Goal browser tavoitteet.html, v0.11.0 |
