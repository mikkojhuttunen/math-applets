# Own theme: sounds, graphics, colours, fonts

Placeholder folder for the teacher's own look and sound. Nothing here is used by any page yet: the practice pages take it into use in task W15 (`harjoittele/BACKLOG_WEB.md`, needs decision WD4), and applets copy the colours as described in `APPLET_SPEC.md`, section 8.

How it works:

- `teema.json` lists every slot. `null` means "not in use": the page uses its built-in look and plays no sound for that slot. To use your own file, put it in the subfolder and write its path relative to this folder, e.g. `"oikein": "aanet/oikein.mp3"`.
- A page never requests a file whose slot is `null`, so an empty slot causes no 404 and no console error (the page checks fail on both).
- `teema.css` holds the colours and the font stack. The values in it now are the site's current defaults.
- Everything is served from this same site. No CDN, no web font services: the ground rules in `harjoittele/BACKLOG_WEB.md` forbid requests to other sites.
- Only files you made yourself or whose licence allows publishing on a public website (CC0, CC BY with the credit written below, SIL OFL for fonts). Add the source and licence of each file to the table at the end.

## Sounds (`aanet/`)

Used only on the practice pages (`harjoittele/`). Applets have no right or wrong answers, so they have no sounds.

| Slot | When it plays | Length |
|---|---|---|
| `klikkaus` | button or choice pressed | under 0,1 s |
| `oikein` | correct answer | 0,3–0,8 s |
| `vaarin` | wrong answer; gentle, not a buzzer | 0,3–0,6 s |
| `kierros_valmis` | round finished (fanfare) | 1,5–3 s |
| `vihje` | hint or feedback text opened | under 0,5 s |

- Format: MP3 (plays everywhere, including iPad Safari). Mono, 44,1 or 48 kHz, 96–128 kbps.
- Trim silence at the start; even 100 ms makes a click feel late.
- Normalise all files to the same loudness, about −16 LUFS, so the fanfare is not much louder than the click.
- Keep each file under 100 kB, the fanfare under 300 kB.
- Sounds are off by default (a classroom of 30 devices). The pupil turns them on with a button, or the teacher shares a link with `?aanet=1`. The choice is not remembered between visits (decision WD1: no storage).

## Pictures (`kuvat/`)

| Slot | Where | Size |
|---|---|---|
| `logo` | page header | height 48 px shown; SVG, or PNG/WebP 96 px high |
| `hahmo_neutraali` | start screen, during a round | about 160 × 160 px shown |
| `hahmo_oikein` | next to a correct answer | same |
| `hahmo_vaarin` | next to the feedback for a wrong answer; encouraging, not sad | same |
| `hahmo_juhla` | end of round | same |

- SVG preferred: sharp at every size, small. Raster: WebP or PNG at twice the shown size (320 × 320 px for a 160 px slot), transparent background.
- Must read on both the light and the dark background; test against the `--bg` values in `teema.css`.
- Designed for a 360 px wide phone first; lines thinner than 2 px disappear.
- Decoration must not push the question below the fold on a phone.

## Icons (`ikonit/`)

`aanet_paalla`, `aanet_pois`, `vihje`, `nollaa`, `seuraava`, `oikein`, `vaarin`.

- SVG, `viewBox="0 0 24 24"`, one colour drawn with `currentColor` (fill or stroke), no fixed colours, so the icon follows the text colour in light and dark theme.
- Every icon button also has a Finnish text label or `aria-label`; the icon alone is never the only cue.

## Fonts (`fontit/`)

| Slot | Use |
|---|---|
| `leipa` | body text, regular |
| `leipa_lihava` | body text, bold |
| `otsikko` | headings; leave `null` to use the body font |

- `.woff2` only, with a licence that allows web use (SIL OFL is the usual one).
- Must contain ä ö å Ä Ö Å and the maths characters the pages use: − (U+2212) × · ² ³ √ π Δ ∫ ≈ ≤ ≥ ½ □. Many fonts lack ∫, Δ or □: test before adding.
- Digits should be tabular (equal width), or column arithmetic will not line up.
- Fonts are for the practice pages and the front page only. Applets stay self-contained and use the system font (`APPLET_SPEC.md`, section 1).

## App icon (`sovelluskuvake`)

For the browser tab and a phone home screen: `favicon` (SVG, or 32 × 32 PNG), `kuvake_192` and `kuvake_512` (PNG), `kuvake_maskable` (512 × 512 PNG with everything important inside the central 80 % circle).

## Colours (`teema.css`)

- Two sets, light and dark; both are required.
- Site part: the variable names already used by `index.html` and `harjoittele/css/style.css`.
- Applet part (`--a-*`): base colours only. Each applet copies these values into its own theme block under the names in the comments (`APPLET_SPEC.md`, section 8). Graph colours (curves, points) stay in each applet.
- Contrast: text on `--bg` and `--card` at least 4,5:1; never rely on `--ok` and `--bad` alone: a correct or wrong answer is always also shown with a sign or text, for colour-blind pupils.

## Sources and licences

| File | Author / source | Licence |
|---|---|---|
| | | |
