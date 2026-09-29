# math-applets

Interaktiiviset matematiikka-appletit, julkaistaan GitHub Pagesin kautta. Etusivu: index.html.

## Tuotantoputki

Kokonaisuus: aihelista → ajastettu Claude-tehtävä → valmis applet → sinun tarkistuksesi → GitHub Pages.

## Tiedostot

| Tiedosto | Tarkoitus |
|---|---|
| BACKLOG.md | Aihejono ja tilat |
| APPLET_SPEC.md | Tekniset ja pedagogiset vaatimukset |
| SCHEDULED_TASK_PROMPT.md | Ajastetun tehtävän ohje |
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

1. Vie tiedostot repon juureen (komennot erikseen).
2. Luo Coworkissa ajastettu tehtävä: kopioi ohje tiedostosta SCHEDULED_TASK_PROMPT.md ja anna tehtävälle pääsy paikalliseen repokansioon.
3. Aja tehtävä ensin käsin kerran ("Run now") ja tarkista tulos ennen kuin otat viikkoajastuksen käyttöön.
4. Aseta ajastus (suositus: viikoittain).

## Viikkorutiini

1. Avaa raportti ja applet selaimessa.
2. Käy läpi laatutarkistus (APPLET_SPEC.md) ja Huomiot-kentän tarkistuslaskut.
3. Aseta tilaksi `hyväksytty` tai `korjattava` (kirjoita korjaustoive Huomiot-kenttään; seuraava ajo ei korjaa sitä automaattisesti, pyydä korjaus chatissa).
4. Commit ja push.

## Rajoitukset, jotka kannattaa tietää

- Ajastettu tehtävä toimii vain siinä, mihin sillä on pääsy. Nykyisillä liittimillä (Drive, Kalenteri, Trello) se ei työnnä koodia GitHubiin, siksi push on aina sinun tehtäväsi.
- Paikalliseen kansioon kirjoittavat tehtävät saattavat vaatia, että Claude Desktop on käynnissä. Tarkista tämä ensimmäisellä ajolla.
- Tehtävät voivat pyytää lupia joka ajolla. Anna vain tarpeelliset oikeudet (yksi kansio).
- Tarkista aina laskut ja opetussuunnitelmasidonnaisuus itse; tehtävä ei korvaa asiantuntijatarkistusta.
- Jos tehtävän ohje muuttuu, muokkaa sitä myös SCHEDULED_TASK_PROMPT.md:hen, jotta versio pysyy repossa.
