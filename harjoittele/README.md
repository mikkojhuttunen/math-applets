# Harjoittele: practice pages

Static practice pages on GitHub Pages for the exercise banks in this repository. No server, no AI calls, no cookies, nothing stored or sent anywhere. Work queue and ground rules: `BACKLOG_WEB.md`.

## Layout

| Path | Role |
|---|---|
| `index.html` | Practice page (pupils); `?luonnokset=1` previews drafts |
| `css/style.css` | Shared styles, light and dark |
| `js/` | ES modules loaded directly by the browser, no build step |
| `data/manifest.json` | List of exercise files and counts, built by `tools/build_manifest.js` |
| `data/misconceptions_source.json` | English misconception catalogue, built by `tools/extract_misconceptions.py` |
| `data/misconceptions_fi.json` | Finnish feedback per misconception, written by hand |
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

Browser test (Chromium through Playwright, which is not a dependency of this folder):

```
cd harjoittele
NODE_PATH=$(npm root -g) node tools/browser_test.js
```

## Reviewing the Finnish feedback texts

Each entry in `data/misconceptions_fi.json` has `pupil` (shown after a wrong answer), `teacher` (teacher view) and `status`. Pupils see a text only when its `status` is `reviewed`; edit the text if needed and change `draft` to `reviewed`. Then run `npm test`.

When the item bank xlsx, the 7-9 backlog's EXT table or `buggy_rules.RULES` changes, run `python3 tools/extract_misconceptions.py`; the tests then list any id that still needs a Finnish text.

## When exercise batches change

```
cd harjoittele
node tools/build_manifest.js
npm test
```
