# math-applets

Interaktiiviset matematiikka-appletit, julkaistaan GitHub Pagesin kautta. Etusivu: index.html.

## Tuotantoputki

Kokonaisuus: aihelista (BACKLOG.md) → ajastettu Claude Code -rutiini pilvessä → valmis applet haarassa `claude/applets` → sinun tarkistuksesi pull requestissa → `main` → GitHub Pages.

Tehtäväpankilla (`math-misconceptions/`) on oma rutiininsa ja haaransa `claude/exercises`, ks. `math-misconceptions/ROUTINE_PROMPT.md`.

## Tiedostot

| Tiedosto | Tarkoitus |
|---|---|
| BACKLOG.md | Aihejono ja tilat |
| APPLET_SPEC.md | Tekniset ja pedagogiset vaatimukset |
| SCHEDULED_TASK_PROMPT.md | Rutiinin käyttöönotto ja ohje (prompt) |
| CLAUDE.md | Repon käytännöt, jotka jokainen Claude Code -istunto lukee |
| scripts/check_applet.js | Appletin automaattinen tarkistus (`node scripts/check_applet.js <tiedosto>`) |
| <taso>/<nimi>.html | Valmiit appletit tasokohtaisissa kansioissa |
| INDEX.md | Luettelo valmiista |
| index.html | GitHub Pages -etusivu |

## Kansiorakenne

Appletit on jaettu oppimäärän mukaan neljään kansioon. Kansioiden sisällä ei ole alikansioita: yksi applet on yksi .html-tiedosto.

```
/
  index.html
  INDEX.md
  BACKLOG.md
  luokat-1-6/
  yla-aste-7-9/
  lukio-pitka/
  lukio-lyhyt/
```

## Käyttöönotto

1. Yhdistä GitHub osoitteessa claude.ai/code (Claude GitHub App repolle `mikkojhuttunen/math-applets`).
2. Luo rutiini osoitteessa claude.ai/code/routines tiedoston SCHEDULED_TASK_PROMPT.md kohdan 1 taulukon mukaan ja kopioi prompt sen kohdasta 2.
3. Kytke rutiini pois päältä, aja se kerran käsin ("Run now") ja tarkista tulos haarassa `claude/applets`.
4. Kytke ajastus päälle (aloita: kerran päivässä, yksi applet per ajo).

## Viikkorutiini

1. Avaa pull request `claude/applets` → `main`.
2. Avaa appletit selaimessa, käy läpi laatutarkistus (APPLET_SPEC.md) ja Huomiot-kentän tarkistuslaskut.
3. Yhdistä pull request valinnalla "Create a merge commit" (ei squash).
4. Aseta `main`-haarassa tilaksi `hyväksytty` tai `korjattava` (kirjoita korjaustoive Huomiot-kenttään; rutiini ei korjaa sitä, pyydä korjaus Claude Code -istunnossa).

## Rajoitukset, jotka kannattaa tietää

- Rutiini työntää vain haaraan `claude/applets`, ei koskaan `main`-haaraan. Mikään ei julkaistu GitHub Pagesissa ennen kuin yhdistät.
- Rutiini käyttää tilauksesi käyttökiintiötä. Tarkista kulutus ensimmäisten ajojen jälkeen.
- Tarkista aina laskut ja opetussuunnitelmasidonnaisuus itse; rutiini ei korvaa asiantuntijatarkistusta.
- Jos rutiinin ohje muuttuu, muokkaa sitä myös SCHEDULED_TASK_PROMPT.md:hen, jotta versio pysyy repossa.
