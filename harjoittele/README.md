# Harjoittele: practice pages

Static practice pages on GitHub Pages for the exercise banks in this repository. No server, no AI calls, no cookies, nothing stored or sent anywhere. Work queue and ground rules: `BACKLOG_WEB.md`.

## Layout

| Path | Role |
|---|---|
| `index.html` | Practice page (pupils) |
| `css/style.css` | Shared styles, light and dark |
| `js/` | ES modules loaded directly by the browser, no build step |
| `test/` | Unit tests (`node:test`), no dependencies |

## Run locally

The pages fetch data files, which browsers block on `file://`, so serve the repo root:

```
cd harjoittele
npm test
cd ..
python3 -m http.server 8000
```

Then open `http://localhost:8000/harjoittele/`.
