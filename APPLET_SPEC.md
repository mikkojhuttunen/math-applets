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
- Värit CSS-muuttujina `:root`-lohkossa (pohjavärit kohdan 8 teema-lohkossa) ja tumma teema `@media (prefers-color-scheme:dark)` -lohkossa. Canvas piirretään uudelleen, kun teema vaihtuu (`matchMedia(...).addEventListener("change", draw)`), ja värit luetaan muuttujista, ei kovakoodata piirtokoodiin.
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


## 8. Oma teema

Opettajan omat värit, kuvat, äänet ja fontit kootaan kansioon `teema/` (ohje ja tiedostopaikat: `teema/README.md`). Applet pysyy silti itsenäisenä tiedostona (kohta 1): se ei lataa mitään `teema/`-kansiosta, vaan kopioi värien arvot itseensä.

- Pohjavärit kirjoitetaan omaan lohkoonsa merkkien `/* teema:alku */` ja `/* teema:loppu */` väliin, vaalea ja tumma teema molemmat. Nimet ovat aina samat, ja arvot otetaan `teema/teema.css`:n applettiosasta (`--a-bg` → `--bg` jne.):

```css
/* teema:alku */
:root{--bg:#fafafa;--card:#fff;--fg:#1c1e21;--muted:#5b6068;--line:#d0d4da;--grid:#e6e8ec;--acc:#1a5fb4;--warn:#fff4d6;--warnbd:#e0b040}
@media (prefers-color-scheme:dark){:root{--bg:#15171a;--card:#1e2126;--fg:#e8eaed;--muted:#a0a6ae;--line:#3a3f46;--grid:#2a2e34;--acc:#6ea8fe;--warn:#3a3218;--warnbd:#8a6d1c}}
/* teema:loppu */
:root{--exp:#1a5fb4;--log:#d9480f;--pt:#2b8a3e}
@media (prefers-color-scheme:dark){:root{--exp:#6ea8fe;--log:#ff922b;--pt:#69db7c}}
```

- Lohkon ulkopuolella vain appletin omat kuvaajavärit (käyrät, pisteet, alueet), omilla nimillään. Muualla CSS:ssä ja piirtokoodissa käytetään pohjaväreille vain näitä nimiä, ei kovakoodattuja arvoja, jotta teeman vaihto on lohkon korvaaminen.
- Kun `teema/teema.css`:n applettiosa muuttuu, lohko päivitetään kaikkiin appleteihin. Paikkamerkki: skriptiä `scripts/apply_theme.js` ei vielä ole; siihen asti lohko kopioidaan käsin. Lohkon ulkopuolelle ei kosketa.
- Kuvaajavärit tarkistetaan kontrastiltaan sekä `--card`- että tumman teeman `--card`-taustaa vasten.
- Ei ääniä: appletissa ei ole oikeita tai vääriä vastauksia. Äänet ovat vain harjoitussivuilla (`harjoittele/`).
- Ei omia fontteja eikä kuvia: ne rikkoisivat kohdan 1. Fontti on järjestelmän (`system-ui, …`).
- Ennen tätä kohtaa tehdyt appletit käyttävät osin muita nimiä (esim. `--bd`, `--box`). Ne siirretään teema-lohkoon omana tehtävänään, ei uuden appletin yhteydessä.
