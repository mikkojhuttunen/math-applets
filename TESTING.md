# Testing the site on a laptop

Two ways: the published site on GitHub Pages, or a local copy on your own laptop. Both show the same pages.

## A. Published site (after Pages is enabled, see `LIVE_BACKLOG.md` T2)

| What | Address |
|---|---|
| Test page: everything per school level | https://mikkojhuttunen.github.io/math-applets/harjoittele/testaa.html |
| Front page and applets | https://mikkojhuttunen.github.io/math-applets/ |
| Exercises, draft preview | https://mikkojhuttunen.github.io/math-applets/harjoittele/?luonnokset=1 |
| Teacher view | https://mikkojhuttunen.github.io/math-applets/harjoittele/opettaja.html |
| Curriculum goals with exercises | https://mikkojhuttunen.github.io/math-applets/harjoittele/tavoitteet.html?sisalto=1 |

All exercises are still drafts, so pupils' view (`harjoittele/` without `?luonnokset=1`) says there is nothing to practise yet.

## B. Local copy, no GitHub needed

Needs Python 3 (preinstalled on macOS and most Linux; on Windows install it from python.org or the Microsoft Store).

```
git clone https://github.com/mikkojhuttunen/math-applets.git
cd math-applets
python3 -m http.server 8000
```

On Windows use `py -m http.server 8000` instead of the last line. Then open http://localhost:8000/ in the browser. Stop the server with Ctrl+C.

Without git: on the GitHub page of the repository choose Code → Download ZIP, unzip it, and start the server in the unzipped folder.

The same addresses as in table A work with `http://localhost:8000/` in place of `https://mikkojhuttunen.github.io/math-applets/`, for example http://localhost:8000/harjoittele/testaa.html.

Why a server: the applets are single files and also open with a double click, but the practice pages load exercise files, and browsers block that for pages opened straight from the disk (`file://`).

## What to try

- Applets: each level on the front page; drag the sliders, check that numbers use a decimal comma and the − sign.
- Exercises: on the start screen pick a topic from each grade band, answer one right, one with a typical wrong answer (the teacher view lists them) and one with something unreadable such as `abc`.
- Teacher view: filters, Kokeile links, Tulosta moniste (print preview).
- On a narrow window (or the browser's phone view) nothing should need sideways scrolling.

Write down what is wrong and where; that becomes the next tasks.
