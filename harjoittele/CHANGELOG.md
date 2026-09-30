# Changelog

`version` in `package.json` follows the same rules as the bot: MAJOR when a page changes behaviour or is removed, MINOR for a new page or feature, PATCH for fixes.

## 0.2.0 (2026-09-30)

- W02: `tools/build_manifest.js` and `data/manifest.json`, the list of exercise files for the pages. Run `node tools/build_manifest.js` after exercise batches change; `npm test` fails until you do.

## 0.1.0 (2026-09-30)

- W01: skeleton. `index.html` start page (Finnish, same colours as the front page, light and dark), `css/style.css`, ES modules in `js/` with no build step, `js/format.js` (decimal comma, U+2212 minus, empty text instead of `NaN`), `node:test` unit tests.
