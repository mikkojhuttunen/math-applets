# Appletin vaatimukset

Ajastettu tehtävä ja jokainen käsin tehty applet noudattavat tätä. Vaatimukset on koottu valmiista appleteista 01–07 ja 09 (esim. `lukio-pitka/eksponentti-logaritmi.html`, `yla-aste-7-9/prosentti-kerroin.html`), jotka kelpaavat malliksi.

## 1. Tiedosto ja sijainti

- Yksi applet on yksi itsenäinen `.html`-tiedosto. Ei ulkoisia kirjastoja, CDN-linkkejä, fontteja, kuvia eikä build-vaihetta: CSS `<style>`-lohkossa, JavaScript `<script>`-lohkossa.
- Kansio backlogin Taso-kentän mukaan:

| Taso | Kansio |
|---|---|
| luokat 1-6 | `luokat-1-6/` |
| yläkoulu 7-9 | `yla-aste-7-9/` |
| lukio pitkä | `lukio-pitka/` |
| lukio lyhyt | `lukio-lyhyt/` |

- Tiedostonimi: pienet kirjaimet, sanat väliviivalla, ä → a, ö → o, å → a, ei välilyöntejä. Esim. `normaalijakauma-keskihajonta.html`.
- Kansioihin ei tehdä alikansioita.

## 2. Rakenne

Järjestys sivulla:

1. `<h1>` = backlogin aiheen nimi, sen alla yhden tai kahden virkkeen johdanto, joka kertoo ydinasian (Tavoite-kenttä).
2. Visualisointi (`<canvas>` tai `<svg>`), jolla on `role="img"` ja kuvaava `aria-label`. Selite (legend), jos värejä on useampi.
3. Säätimet: `<input type="range">` jokaisella näkyvä `<label>` ja elävä lukuarvo; pikavalintapainikkeet kiinnostaville tapauksille; `Nollaa`-painike.
4. Lukemat: tärkeimmät luvut ja laskun välivaiheet, jotka päivittyvät heti.
5. Tutki itse: 3–4 numeroitua kysymystä, jotka ohjaavat oppijan löytämään Tavoitteen ja törmäämään virhekäsitykseen. Vastaukset eivät näy sivulla (ne kirjataan backlogin Huomiot-kenttään opettajalle).
6. Varo virhekäsitystä -laatikko: Yleinen virhekäsitys -kentän virhekäsitys ja lyhyt selitys, miksi se on väärä ja miten appletista sen näkee.
7. `<footer>`: `Taso: … · Käsite: …`.

## 3. Tekninen toteutus

- `<html lang="fi">`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, `<title>` = aiheen nimi.
- Värit CSS-muuttujina `:root`-lohkossa ja tumma teema `@media (prefers-color-scheme:dark)` -lohkossa. Canvas piirretään uudelleen, kun teema vaihtuu (`matchMedia(...).addEventListener("change", draw)`), ja värit luetaan muuttujista, ei kovakoodata piirtokoodiin.
- Leveys: `main{max-width:…;margin:0 auto;padding:…}`, `box-sizing:border-box`. Ei sivuttaisvieritystä 360 px leveällä.
- Canvas skaalataan `devicePixelRatio`:lla ja piirretään uudelleen `resize`-tapahtumassa.
- Vedettävät pisteet Pointer Events -rajapinnalla (`pointerdown/move/up/cancel`, `setPointerCapture`), canvasissa `touch-action:none`. Jokaisen vedettävän suureen pitää olla säädettävissä myös liukusäätimellä.
- Liukusäätimien arvot kokonaislukuina ja jaetaan koodissa (esim. `value/10`), jotta tasa-arvovertailut (D = 0, kulma = 90°) ovat tarkkoja.
- JavaScript yhden `(function(){ "use strict"; … })();` -lohkon sisällä, ei globaaleja muuttujia, ei `localStorage`a, ei verkkopyyntöjä.
- Lukujen esitys: desimaalipilkku, oikea miinusmerkki (−, U+2212), ei "−0,00", määrittelemätön arvo tekstinä "ei määritelty". Sivulla ei saa koskaan näkyä `NaN`, `undefined` tai `Infinity`.
- Kielletyt tai reunatapaukset (esim. kantaluku a = 1, nollalla jakaminen, Δx = 0) käsitellään näkyvällä selittävällä viestillä, ei hiljaisella virheellä.

## 4. Pedagogiikka

- Yksi applet, yksi ydinidea (Tavoite-kenttä). Ei lisäominaisuuksia, joita backlogin Interaktio-kenttä ei pyydä.
- Virhekäsitys pitää pystyä näkemään appletissa: oppija voi säätää tilanteen, jossa väärä ajatus antaisi eri tuloksen kuin appletti näyttää.
- Appletissa ei väitetä mitään opetussuunnitelman sisällöistä (kurssikoodit vain `index.html`:n kuvauksessa).
- Merkinnät kuten suomalaisissa oppikirjoissa (esim. y = kx + b, log<sub>a</sub> x, puolipiste pisteen koordinaateissa (1; 2)).

## 5. Laatutarkistus ennen kuin tila on `valmis`

1. `node scripts/check_applet.js <tiedosto>` tulostaa `CHECK OK`. Skripti tarkistaa leveyksillä 360 px ja 1000 px, vaaleassa ja tummassa teemassa: konsolivirheet, sivuttaisvieritys, ulkoiset resurssit, `lang="fi"`, viewport, sekä jokaisen liukusäätimen ääripäät (ei NaN/undefined/Infinity).
2. Vähintään kaksi tarkistuslaskua käsin, eri parametreilla, ja sovelluksen lukemat vertailtu niihin.
3. Reunatapaukset (ääripäät, nolla, kielletyt arvot) kokeiltu ja kuvattu.
4. Vähintään yksi kuvakaappaus 360 px leveydeltä katsottu (`node scripts/check_applet.js --shots <kansio> <tiedosto>` tallentaa ne).
5. Tutki itse -kysymyksiin on vastaukset.

## 6. Huomiot-kentän sisältö

Kirjoita yhteen kappaleeseen samassa järjestyksessä kuin valmiissa aiheissa 01–06:

- **Tarkistuslaskut:** käsin lasketut arvot ja sovelluksen lukemat.
- **Ääritapaukset:** mitä kokeiltiin ja miten appletti käyttäytyi; `check_applet.js`-tulos; testiselain ja leveydet.
- **Parametrien alueet ja omat valinnat:** liukusäätimien välit ja askeleet.
- **Tutki itse -vastaukset opettajalle:** jokaiseen kysymykseen numeroitu vastaus.
- **Tarkistettava:** mikä jäi tarkistamatta tai on opettajan arvioitava (kurssitaso, rajaukset, kosketuslaitetestaus).

## 7. Julkaisu

Kun applet on valmis:

- Backlogin kohta: `Tila: valmis`, `Tiedosto`, `Valmistui` (VVVV-KK-PP), `Huomiot`.
- `INDEX.md`: uusi rivi loppuun muodossa `- [Nimi](kansio/tiedosto.html) - taso - VVVV-KK-PP`.
- `index.html`: uusi `<li>` oikean tason `<ul>`-listaan, muodossa `<li><a href="kansio/tiedosto.html">Nimi</a> <span>lyhyt aihe tai kurssikoodi</span></li>`.
