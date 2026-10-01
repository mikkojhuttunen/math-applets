# Changelog

`version` in `package.json` follows the same rules as the bot: MAJOR when a page changes behaviour or is removed, MINOR for a new page or feature, PATCH for fixes.

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
