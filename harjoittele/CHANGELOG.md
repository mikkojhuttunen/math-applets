# Changelog

`version` in `package.json` follows the same rules as the bot: MAJOR when a page changes behaviour or is removed, MINOR for a new page or feature, PATCH for fixes.

## 0.15.0 (2026-10-18)

- `tarkista.html`: review page for vetting draft items one at a time, with approve / fix / reject verdicts, a four-point checklist, results as a file per reviewer, and a merge tab for the collector (`js/review.js`, `js/review_page.js`). Page check and browser test cover it.
- Merge tab downloads the updated exercise files and manifest as one zip (`js/status_edit.js`, `js/zip.js`), identical to what `tools/set_status.js` writes.
- `tools/set_status.js`: sets items to `approved` (grades 7-9) or `reviewed` (grades 1-6) from a list of ids.
- Browser test: the pupil start page lists an item under each of its goals, so the topic counts are compared with the number of goal links, not with the number of items.

## 0.14.0 (2026-10-17)

- Number answers framed as a sentence: `answer_prefix`, the box and `answer.unit` on one line ("Hinta on [ ] euroa"); the input hint moves below the row. An answer typed with the item's own unit ("12 euroa") is accepted. The teacher view shows the prefix with the correct answer.
- Correct answers show "Oikein!" once, before the item's own feedback.

## 0.13.0 (2026-10-01)

- `testaa.html`: test page with every applet and practice topic per school level (`LIVE_BACKLOG.md` L03).

## 0.12.1 (2026-10-01)

- Manifest rebuilt: 143 files, 1010 items. Pupil titles for 33 more goals. Fix: column view only for a bare subtraction, not for a subtraction inside another question.

## 0.12.0 (2026-10-01)

- W12: link to the practice pages on the front page.
- W13: `tools/check_pages.js` page check with `--self-test`; GitHub Actions workflows `harjoittele` (tests, page check, browser test) and `harjoittele-content` (warns when `data/` needs rebuilding after exercise or curriculum changes).

## 0.11.0 (2026-10-01)

- W11: goal browser `tavoitteet.html`: 128 curriculum goals with exercises, practice links, applets and misconceptions; search and filters in the URL. `data/goal_applets.json`. Teacher links in the practice page footer.

## 0.10.0 (2026-10-01)

- W09: a wrong answer to a subtraction shows the sum in columns with the wrong columns marked; after the second try also the borrows and the correct row.

## 0.9.0 (2026-10-01)

- W08: start screen with topics; shareable links `?tavoite=`, `?luokat=`, `?virhe=`; pupil link in the teacher view; `data/goals.json` from the curriculum files (`tools/build_goals.js`) and pupil titles in `data/topics_fi.json`.

## 0.8.0 (2026-10-01)

- W07: choice options in random order with letters A, B, C ...; letter keys choose.

## 0.7.0 (2026-10-01)

- W10: teacher view `opettaja.html`: all items and feedback texts with filters, review checkboxes and a copy list of ids, "Kokeile" link, printable worksheet with answer key. Practice page accepts `?tehtava=<id>`.
- Manifest rebuilt for the new batches: 5 files, 100 items.

## 0.6.0 (2026-09-30)

- W06: practice round of five on `index.html`: number pad, two tries, misconception feedback, correct answer after the second try, summary. Draft preview with `?luonnokset=1`. `js/round.js`, `tools/browser_test.js`.

## 0.5.0 (2026-09-30)

- W05: Finnish feedback texts for 54 misconceptions (`data/misconceptions_fi.json`, all draft), English reference extracted from the item bank (`tools/extract_misconceptions.py`), lookup in `js/misconceptions.js`.

## 0.4.0 (2026-09-30)

- W04: `js/answers.js` checks typed answers (numbers, fractions, sets, expressions) and choices, and finds the misconception behind a stored wrong answer.

## 0.3.0 (2026-09-30)

- W03: `js/items.js` loads the files in the manifest and turns 1-6 and 7-9 items into one shape; drafts only for the teacher view.

## 0.2.0 (2026-09-30)

- W02: `tools/build_manifest.js` and `data/manifest.json`, the list of exercise files for the pages. Run `node tools/build_manifest.js` after exercise batches change; `npm test` fails until you do.

## 0.1.0 (2026-09-30)

- W01: skeleton. `index.html` start page (Finnish, same colours as the front page, light and dark), `css/style.css`, ES modules in `js/` with no build step, `js/format.js` (decimal comma, U+2212 minus, empty text instead of `NaN`), `node:test` unit tests.
