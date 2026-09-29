# Appletti-backlog

Tämä on ajastetun tehtävän työjono. Tehtävä ottaa jonosta aina pienimmän numeron aiheen, jonka Tila on `odottaa`.

Tilat: `odottaa` → `työn alla` → `valmis` → `hyväksytty` (asetat itse tarkistuksen jälkeen) tai `korjattava`.

Uuden aiheen lisääminen: kopioi alla oleva pohja listan loppuun, anna seuraava numero ja täytä kentät.

Pohja:

```
## NN Aiheen nimi
- Tila: odottaa
- Taso: yläkoulu 7-9 / lukio pitkä / lukio lyhyt
- Tavoite: mitä oppijan pitää ymmärtää appletin jälkeen
- Yleinen virhekäsitys: mitä appletin pitää haastaa
- Interaktio: mitä oppija saa muuttaa ja mitä hän näkee tapahtuvan
- Tiedosto:
- Valmistui:
- Huomiot:
```

---

## 01 Derivaatta tangentin kulmakertoimena
- Tila: valmis
- Taso: lukio pitkä
- Tavoite: derivaatta pisteessä on sekantin kulmakertoimen raja-arvo, kun pisteiden väli lähestyy nollaa
- Yleinen virhekäsitys: derivaatta on "funktion arvo" tai "funktion muutos" eikä muutosnopeus
- Interaktio: liukusäädin sekantin toiselle pisteelle (h → 0), funktion valinta, tangentti ja kulmakerroin näkyvät
- Tiedosto: lukio-pitka/derivaatta-sekantti-tangentti.html
- Valmistui: 2026-09-29
- Huomiot: Tarkistuslaskut (f(x) = x², x₀ = 1): h = 1 → (4 − 1)/1 = 3; h = 0,1 → (1,21 − 1)/0,1 = 2,1; h = 0,001 → 2,001; raja-arvo 2 = 2x₀. Toinen funktio (f(x) = x³ − 3x, x₀ = 2, f(2) = 2): h = 1 → (18 − 2)/1 = 16; h = 0,1 → 9,61; h = 0,001 → 9,006; f′(2) = 3·4 − 3 = 9. Ääritapaukset (x₀ = ±3, h = ±5 ja h = ±0,001, kaikki viisi funktiota, |x| pisteessä 0) testattu selaimessa 360 px leveällä näytöllä: ei konsolivirheitä eikä sivuttaisvieritystä; |x|:n derivaatta pisteessä 0 näytetään "ei määritelty". Tutki itse -vastaukset opettajalle: (1) sekantin kulmakerroin lähestyy tangentin kulmakerrointa f′(x₀); x²:lla sekantin kulmakerroin on 2x₀ + h. (2) Tangentti on vaakasuora kohdassa x₀ = 0, jolloin f′(0) = 0: funktion hetkellinen muutosnopeus on nolla (minimikohta), vaikka f(0) = 0 sattuu olemaan sama luku. Vertailuksi x³ − 3x:llä f′ = 0 kohdissa x = ±1, mutta f(±1) = ∓2. (3) Molemmilta puolilta saadaan sama raja-arvo kaikilla muilla funktioilla; |x|:llä pisteessä 0 oikealta +1 ja vasemmalta −1, joten derivaattaa ei ole. Tarkistettava: appletissa ei väitetä mitään opetussuunnitelman sisällöistä; opettajan kannattaa harkita, onko |x|-esimerkki sopiva lukion pitkän matematiikan kurssitasolle. Lisäksi tiedosto on testattu vain Chromiumilla, ei kosketuslaitteella.

## 02 Integraali pinta-alana (Riemannin summa)
- Tila: valmis
- Taso: lukio pitkä
- Tavoite: määrätty integraali on suorakaidesummien raja-arvo
- Yleinen virhekäsitys: integraali on pelkkä "derivoinnin käänteistoiminto" ilman pinta-alamerkitystä; negatiivinen pinta-ala
- Interaktio: suorakaiteiden lukumäärä, vasen/oikea/keskipiste, funktion valinta, summa vs. tarkka arvo
- Tiedosto: lukio-pitka/integraali-riemannin-summa.html
- Valmistui: 2026-09-29
- Huomiot: Tarkistuslaskut (f(x) = x², [0, 3], tarkka 9): n = 2, Δx = 1,5: vasen 1,5·(0 + 2,25) = 3,375; oikea 1,5·(2,25 + 9) = 16,875. n = 4, Δx = 0,75: vasen 0,75·(0 + 0,5625 + 2,25 + 5,0625) = 5,90625; keskipiste 0,75·(0,140625 + 1,265625 + 3,515625 + 6,890625) = 8,859375. Sovelluksen laskenta antoi samat arvot. Muut: sin x, [0, π], n = 1, keskipiste: π·sin(π/2) = π ≈ 3,1416 (tarkka 2, ylitys); 1/x, [1, 4], n = 200, keskipiste ≈ 1,38629 (tarkka ln 4 ≈ 1,38629); sin x, [0, 2π], n = 200, vasen ≈ 0 ja pinta-alat itseisarvoina ≈ 4. Ääritapaukset: n = 1 ja n = 200 kaikilla viidellä funktiolla ja kolmella tavalla, ei konsolivirheitä; 360 px leveällä näytöllä ei sivuttaisvieritystä (Chromium). Nollan lähellä oleva ero näytetään ilman miinusmerkkiä. Tutki itse -vastaukset opettajalle: (1) x²:lla vasen summa on aina liian pieni (funktio kasvava) ja kasvaa kohti arvoa 9 kun n kasvaa. (2) Oikea summa on liian suuri, keskipiste on tarkin, koska virheet vasemmalla ja oikealla puolella suorakaiteessa kumoavat suurelta osin toisensa (kaarevuus vaikuttaa vain toisen asteen termin kautta). (3) Summa lähestyy nollaa: positiivinen ja negatiivinen puoli ovat yhtä suuret; pinta-alat itseisarvoina yhteensä lähestyvät arvoa 4 (2 + 2). Tarkistettava: appletissa ei väitetä mitään opetussuunnitelman sisällöistä; tarkka arvo on kovakoodattu funktiokohtaisesti (ei laskettu numeerisesti). Riemannin summa -termin ja määritelmän sopivuus kurssitasolle (esim. onko keskipistesääntö kurssin sisältöä) on opettajan arvioitava. Testattu vain Chromiumilla, ei kosketuslaitteella.

## 03 Yksikköympyrä ja trigonometriset funktiot
- Tila: valmis
- Taso: lukio pitkä
- Tavoite: sin ja cos ovat yksikköympyrän pisteen koordinaatit; kuvaaja syntyy kulman kasvaessa
- Yleinen virhekäsitys: sin ja cos ovat vain suorakulmaisen kolmion sivusuhteita, eivät toimi yli 90°
- Interaktio: kulman vetäminen (aste/radiaani), pisteen koordinaatit ja kuvaaja rinnakkain
- Tiedosto: lukio-pitka/yksikkoympyra-sini-kosini.html
- Valmistui: 2026-09-29
- Huomiot: Tarkistuslaskut (sovelluksen lukemat vs. käsin): θ = 30° → cos = √3/2 ≈ 0,8660, sin = 1/2 = 0,5000; θ = 150° → cos = −0,8660, sin = 0,5000; θ = 210° → cos = −0,8660, sin = −0,5000; θ = 330° → cos = 0,8660, sin = −0,5000; θ = 390° antaa samat arvot kuin 30° (jaksollisuus). cos² + sin² = 1,0000 kaikilla. Ääritapaukset: θ = 0°, 90° ja 720° (cos 90° näytetään 0,0000 ilman miinusmerkkiä), radiaaninäkymä, sin/cos-valintojen poiskytkentä; ei konsolivirheitä; 360 px leveällä näytöllä (pinottu asettelu) ja 1000 px leveällä (vaalea ja tumma teema) ei sivuttaisvieritystä (Chromium). Tutki itse -vastaukset opettajalle: (1) Kulman kasvaessa 90°:sta 180°:een pisteen x-koordinaatti pienenee 0:sta arvoon −1 (cos θ negatiivinen) ja y-koordinaatti pienenee 1:stä 0:aan (sin θ pysyy positiivisena, toinen neljännes). (2) sin θ = 0,5 kulmilla 30° ja 150°: pisteet ovat samalla korkeudella, peilikuvat y-akselin suhteen (150° = 180° − 30°). cos θ = 0,5 kulmilla 60° ja 300°: pisteet samalla x-koordinaatilla, peilikuvat x-akselin suhteen (300° = 360° − 60°). (3) Kuvaajat toistuvat 360° välein (2π rad). Tarkistettava: appletissa ei väitetä mitään opetussuunnitelman sisällöistä; opettajan kannattaa arvioida, onko radiaani ja kulma-alue 0°–720° (ei negatiivisia kulmia) sopiva kurssitasolle. Radiaaniarvo näytetään desimaalilukuna, ei π:n monikertona (π:n monikerrat vain kuvaajan akselilla). Testattu vain Chromiumilla, ei kosketuslaitteella; ympyrän pisteen vetäminen testattu vain koodin tasolla ja pikavalinnoilla, ei oikealla kosketuksella.

## 04 Paraabeli ja toisen asteen yhtälön juuret
- Tila: valmis
- Taso: lukio pitkä
- Tavoite: kertoimet a, b, c määräävät paraabelin muodon ja juurten määrän; diskriminantti
- Yleinen virhekäsitys: toisen asteen yhtälöllä on aina kaksi ratkaisua
- Interaktio: liukusäätimet a, b, c; juuret, huippu ja diskriminantti päivittyvät
- Tiedosto: lukio-pitka/paraabeli-toisen-asteen-juuret.html
- Valmistui: 2026-09-29
- Huomiot: Tarkistuslaskut: (1) a = 1, b = −2, c = −3: D = 4 + 12 = 16, juuret (2 ± 4)/2 = −1 ja 3, huippu (1; −4). Sovelluksen lukemat samat. (2) a = −3, b = 6, c = 6: D = 36 + 72 = 108, juuret 1 ∓ √108/6 ≈ −0,732 ja 2,732, huippu (1; 9). Sovelluksen lukemat samat. Lisäksi a = 1, b = −2, c = 1: D = 0, juuri x = 1, huippu (1; 0); a = 3, b = −6, c = 6: D = −36, ei reaalijuuria. D lasketaan kokonaislukuina (kertoimet kymmenesosina), joten D = 0 tunnistetaan tarkasti ilman liukulukuvirhettä. Ääritapaukset: a = 0 (suora: b ≠ 0 → yksi juuri −c/b; b = 0, c ≠ 0 → ei juuria; a = b = c = 0 → kaikki x), a = ±3 ja b, c = ±6 ääripäät; ei konsolivirheitä; 360 px ja 1000 px leveällä näytöllä ei sivuttaisvieritystä (Chromium, vain ohjelmallinen testaus, kuvakaappausta ei katsottu). Kertoimet a, b, c liikkuvat askelin 0,1 välillä a ∈ [−3; 3], b, c ∈ [−6; 6]; kuvaajan alue x ∈ [−8; 8], y ∈ [−10; 10]. Tutki itse -vastaukset opettajalle: (1) c:tä muuttamalla (a = 1, b = −2): D = 4 − 4c, joten kaksi juurta kun c < 1, yksi kun c = 1, ei juuria kun c > 1; paraabeli siirtyy ylös/alas. (2) Paraabeli koskettaa x-akselia kun D = 0, esim. a = 1, b = −2, c = 1; silloin huipun y-koordinaatti on 0 (huippu on x-akselilla) ja juuri on huipun x-koordinaatti −b/(2a). (3) a:n merkki kääntää paraabelin aukeamissuunnan (a > 0 ylös, a < 0 alas); D = b² − 4ac riippuu tulosta ac, joten juurten lukumäärä voi muuttua, kun a:n merkki vaihtuu, jos c ja b pidetään ennallaan (esim. b = 0, c = 4: a = 1 → D < 0, a = −1 → D > 0). Huom. tehtävänannon kysymys 3 on appletin tekstissä muotoiltu "mikä pysyy samana, kun D ei muutu"; D:n ollessa vakio juurten lukumäärä pysyy samana, mutta a:n merkin vaihto yleensä muuttaa D:tä, joten opettajan kannattaa ehkä tarkentaa kysymystä. Tarkistettava: appletissa ei väitetä mitään opetussuunnitelman sisällöistä; komplekslukuja ei käsitellä ("ei reaalijuuria"), opettajan on arvioitava sopiiko rajaus kurssitasolle. Juurten nimeäminen x₁ ≤ x₂ ja kaavan x = (−b ± √D)/2a käyttö ovat oma valinta. Testattu vain Chromiumilla, ei kosketuslaitteella; ei vedettävää kuvaajaa, vain liukusäätimet.

## 05 Suoran yhtälö ja kulmakerroin
- Tila: valmis
- Taso: yläkoulu 7-9
- Tavoite: y = kx + b, k on muutosnopeus ja b leikkauspiste
- Yleinen virhekäsitys: k ja b sekoittuvat; negatiivinen kulmakerroin
- Interaktio: liukusäätimet k ja b, kaksi vedettävää pistettä, kulmakolmio
- Tiedosto: yla-aste-7-9/suoran-yhtalo.html
- Valmistui: 2026-09-29
- Huomiot: Tarkistuslaskut: (1) k = 2, b = 1, A: x = −2, B: x = 1 → A(−2; −3), B(1; 3), Δx = 3, Δy = 6, Δy/Δx = 2 = k; yhtälö "y = 2x + 1". (2) k = −1,5, b = −2, A: x = −3, B: x = 2 → A(−3; 2,5), B(2; −5), Δx = 5, Δy = −7,5, Δy/Δx = −1,5 = k; yhtälö "y = −1,5x − 2". Sovelluksen lukemat samat. Lisäksi k = 5, b = −5, x = ±6 (Δx = 12, Δy = 60) ja k = 1, b = 0 → "y = x". Ääritapaukset: k = 0 (vaakasuora, yhtälö "y = 3", Δy = 0), b = 0 ("y = kx"), k = ±1 (näytetään "x" ja "−x"), A ja B samassa x:ssä (Δx = 0 → k:ta ei lasketa, näytetään ohje), k ja b ääripäissä ±5, pisteen vetäminen hiirellä; ei konsolivirheitä; 360 px ja 1000 px leveällä näytöllä ei sivuttaisvieritystä (Chromium, kuvakaappaus katsottu 360 px). Pisteet A ja B siirtyvät vain suoraa pitkin (x askelin 0,5), joten kulmakerroin ei muutu vetämällä; vihreä piste y-akselilla muuttaa b:tä (askel 0,1). Tutki itse -vastaukset opettajalle: (1) b = 2, k muuttuu: suora kiertyy pisteen (0; 2) ympäri, joten leikkauspiste y-akselilla pysyy samana (2) ja jyrkkyys muuttuu. (2) k = 1, b muuttuu: suora siirtyy ylös/alas yhdensuuntaisena, jyrkkyys (k = 1) ei muutu. (3) Pisteiden etäisyyden muuttaminen muuttaa Δx:ää ja Δy:tä mutta ei niiden suhdetta k = Δy/Δx. (4) Negatiivisella k:lla suora laskee oikealle mentäessä (y pienenee x:n kasvaessa); k = 0: vaakasuora suora y = b. Tarkistettava: appletissa ei väitetä mitään opetussuunnitelman sisällöistä; opettajan on arvioitava, onko kulmakertoimen Δy/Δx-merkintä ja suoran yhtälö y = kx + b oikeassa kohdassa yläkoulun kurssia. Kun piste A on kohdassa x = 0, se on vihreän b-pisteen päällä ja vetäminen tarttuu b-pisteeseen (vihreä on päällimmäisenä). Pystysuoraa suoraa (x = vakio) ei käsitellä. Testattu vain Chromiumilla, ei kosketuslaitteella.

## 06 Pythagoraan lause
- Tila: valmis
- Taso: yläkoulu 7-9
- Tavoite: neliöiden pinta-alat kateeteilla ja hypotenuusalla toteuttavat a² + b² = c²
- Yleinen virhekäsitys: lause pätee kaikille kolmioille
- Interaktio: kateettien pituudet, neliöt piirtyvät sivuille, kulman muuttaminen näyttää milloin yhtälö ei päde
- Tiedosto: yla-aste-7-9/pythagoras-neliot.html
- Valmistui: 2026-09-29
- Huomiot: Tarkistuslaskut (sovelluksen lukemat vs. käsin): (1) a = 3, b = 4, C = 90° → a² = 9, b² = 16, summa 25, c² = 25, c = 5. (2) a = 5, b = 8, C = 90° → 25 + 64 = 89 = c², c ≈ 9,43. Kulma ≠ 90° (kosinilause c² = a² + b² − 2ab·cos C): a = 5, b = 8, C = 60° → 89 − 40 = 49, c = 7 (a² + b² suurempi, erotus −40); C = 120° → 89 + 40 = 129, c ≈ 11,36 (c² suurempi, erotus +40). Ääritapaukset: a = b = 1, C = 30° → c² ≈ 0,27; a = b = 8, C = 150° → c² ≈ 238,85; ei konsolivirheitä; 360 px ja 1000 px leveällä näytöllä sekä vaaleassa että tummassa teemassa ei sivuttaisvieritystä (Chromium, kuvakaappaus katsottu 360 px). Sivut a ja b ovat välillä 1,0–8,0 (askel 0,1), kulma C välillä 30°–150° (askel 1°). Kolmion ja neliöiden mittakaava on kiinteä, joten neliöiden koko vastaa oikeita pituuksia säätäessä. Suora kulma tunnistetaan täsmälleen C = 90° (ei liukulukuvertailua). Tutki itse -vastaukset opettajalle: (1) Kun C = 90°, a² + b² = c² kaikilla a:n ja b:n arvoilla; neliöiden pinta-alojen summa täsmää aina. (2) Kun C < 90°, c² on pienempi kuin a² + b² (kolmio "sulkeutuu" nopeammin); kun C > 90°, c² on suurempi kuin a² + b². (3) Yhtälö a² + b² = c² pätee vain kulmalla C = 90°, koska c² = a² + b² − 2ab·cos C ja ab > 0, joten 2ab·cos C = 0 vain kun cos C = 0. Useampaa kulmaa ei löydy. Tarkistettava: appletissa ei väitetä mitään opetussuunnitelman sisällöistä; opettajan on arvioitava, onko kulman muuttaminen ja "ei suora kulma" -vertailu sopivassa kohdassa yläkoulun kurssia (kosinilausetta appletissa ei mainita, se on vain taustalaskenta). Kulma-alue 30°–150° on oma valinta. Pythagoraan lauseen käänteislause (jos a² + b² = c², kolmio on suorakulmainen) ei ole erikseen esillä. Testattu vain Chromiumilla, ei kosketuslaitteella; ei vedettäviä pisteitä, vain liukusäätimet.

## 07 Eksponenttifunktio ja logaritmi käänteisfunktioina
- Tila: odottaa
- Taso: lukio pitkä
- Tavoite: a^x ja log_a x ovat peilikuvia suoran y = x suhteen
- Yleinen virhekäsitys: logaritmi on "vain laskusääntö"; kantaluvun vaikutus
- Interaktio: kantaluvun a valinta, pisteen vetäminen ja peilikuva
- Tiedosto:
- Valmistui:
- Huomiot:

## 08 Normaalijakauma ja keskihajonta
- Tila: odottaa
- Taso: lukio pitkä
- Tavoite: keskiarvo siirtää, keskihajonta levittää; alueen todennäköisyys pinta-alana
- Yleinen virhekäsitys: keskihajonta on "keskimääräinen virhe" tai sama kuin vaihteluväli
- Interaktio: μ ja σ, valittava väli ja sen todennäköisyys, 68-95-99,7 -säännön korostus
- Tiedosto:
- Valmistui:
- Huomiot:

## 09 Prosenttilaskenta ja kerroin
- Tila: odottaa
- Taso: yläkoulu 7-9
- Tavoite: prosentin muutos kertoimena; peräkkäiset muutokset
- Yleinen virhekäsitys: +20 % ja sitten -20 % palauttaa alkuarvon
- Interaktio: alkuarvo ja muutokset liukusäätimillä, palkkikaavio ja kerroin näkyvät
- Tiedosto:
- Valmistui:
- Huomiot:

## 10 Vektorien summa ja komponentit
- Tila: odottaa
- Taso: lukio pitkä
- Tavoite: vektorin summa komponenteittain ja geometrisesti (kärki-häntä)
- Yleinen virhekäsitys: vektorien pituudet lasketaan yhteen sellaisenaan
- Interaktio: kahden vektorin vetäminen, summavektori ja komponentit, pituus ja suunta
- Tiedosto:
- Valmistui:
- Huomiot:
