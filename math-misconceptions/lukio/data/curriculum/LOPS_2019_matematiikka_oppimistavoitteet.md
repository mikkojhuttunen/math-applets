# Matematiikka, lukio (LOPS 2019): oppimistavoitteet tehtävien ja applettien laatimiseen

Tämä tiedosto on lukion vastine tiedostoille `OPS_1-6_oppimistavoitteet.md` ja `OPS_7-9_oppimistavoitteet.md`. Se kattaa lukion matematiikan yhteisen moduulin (MAY1), lyhyen oppimäärän (MAB) ja pitkän oppimäärän (MAA). Jokaisella oppimistavoitteella on pysyvä tunniste (esim. `MAA6.06`), johon tehtävät, appletit, virhekäsitykset ja backlog-merkinnät voivat viitata.

Versio: 2 (2026-10-02). Tarkistettu ePerusteista (tehtävä L-R02). Muutokset versioon 1 (2026-10-01): luku 8.

## 0. Lähteet ja luotettavuus

| Osa | Lähde | Luotettavuus |
|---|---|---|
| Moduulirakenne, moduulien nimet ja laajuudet (op), pakollinen / valtakunnallinen valinnainen | Lukion opetussuunnitelman perusteet 2019 (OPH-2263-2019), luku 6.6 Matematiikka, ePerusteet (peruste 6828810, oppiaine 6831746; julkaisu 22.5.2026, muutosmääräys voimassa 15.4.2026 alkaen), luettu ePerusteiden rajapinnasta 2.10.2026 | **Sanatarkka virallinen lähde.** |
| Moduulien tavoitteet ja keskeiset sisällöt (luku 3) | Sama | Jokainen rivi palautuu moduulin tavoitteeseen tai keskeiseen sisältöön. Kohdat, joita perusteet eivät nimeä mutta jotka on pidetty esimerkkeinä, on merkitty "esim.". |
| Oppiaineen yleiset tavoitteet G1–G8 (luku 2) | Sama, matematiikan yleiset tavoitteet (8 luettelokohtaa) ja laaja-alainen osaaminen | **Tiivistetty ja numeroitu tätä tiedostoa varten.** Perusteissa tavoitteet ovat luettelona ilman tunnisteita; vastaavuus sarakkeessa "Perusteet". |
| Atomiset oppimistavoitteet (luku 3) | Pilkottu moduulin tavoitteista ja keskeisistä sisällöistä | Tunnisteet ovat tämän tiedoston omia. |
| Arviointi ja tasot (luku 4) | LOPS 2019, matematiikan arviointiteksti ja yleinen arviointiluku; ylioppilastutkintolautakunnan (YTL) "hyvän vastauksen piirteet" | Perusteissa ei ole matematiikan arvosanakriteerejä (tarkistettu). Tasot P/T/H/K on johdettu YO-kokeen rakenteesta. |
| Vuosikurssijako (luku 5) | **Ehdotus.** Perusteet eivät jaa moduuleja vuosikursseille; jaon tekee lukion oma OPS. | Tarkistettava paikallisesta OPS:sta |

## 1. Havainnot lähteistä

1. **Rakenne poikkeaa perusopetuksesta.** Lukion matematiikassa ei ole numeroituja T-tavoitteita eikä sisältöalueita S1–S6. Perusteet antavat oppiaineen yleiset tavoitteet ja jokaiselle moduulille omat tavoitteet ja keskeiset sisällöt. Tunnisteet on siksi muodostettu moduulikoodista: `MAY1.03`, `MAB4.02`, `MAA6.06`.
2. **Yhteinen alku.** MAY1 Luvut ja yhtälöt (2 op) kuuluu molempiin oppimääriin (perusteissa "Matematiikan yhteinen opintokokonaisuus"). Se kertaa ja syventää yläkoulun lukukäsitettä, murtolukuja, potenssia, verrannollisuutta, funktiota ja yhtälöä, joten yläkoulun virhekäsitykset (7–9-tiedoston `S2.01`, `S2.10`, `S2.11`, `S3.02`, `S3.08`, `S4.05`) jatkuvat siinä suoraan.
3. **Moduulin numero ei kerro sisältöä oppimäärien välillä.** MAB3 ja MAA3 ovat molemmat geometriaa, mutta MAB5 on tilastoja ja MAA5 trigonometriaa, eksponenttia ja logaritmia. Tunnisteet ovat siksi aina oppimääräkohtaisia.
4. **Talousmatematiikka.** Lyhyessä oppimäärässä on kaksi 1 op:n moduulia: **MAB6 Talousmatematiikan alkeet** (suhteellinen osuus, indeksi, yksinkertainen korko, verotus, valuutat) ja **MAB7 Talousmatematiikka**. Pitkässä on yksi, **MAA9 Talousmatematiikka** (1 op). MAB7:n ja MAA9:n tavoitteet ja sisällöt ovat perusteissa sanasta sanaan samat (lukujonot ja summat, koronkorko, nykyarvo ja diskonttaus, talletukset ja lainat, mallit). Indeksi, verotus ja valuutat kuuluvat vain MAB6:een.
5. **Oppimäärän vaihto.** Perusteiden hyväksilukutaulukko pitkästä lyhyeen: MAA2 → MAB2, MAA3 → MAB3, MAA6 → MAB8, MAA8 → MAB5, MAA9 → MAB7. Se kertoo, mitkä moduulit perusteet katsovat sisällöltään vastaaviksi.
6. **Analyysi lyhyessä oppimäärässä on valinnaista.** Derivaatta on lyhyessä vain valtakunnallisessa valinnaisessa moduulissa MAB8. Normaalijakauma on lyhyessä valinnaisessa moduulissa MAB9 ja pitkässä valinnaisessa MAA12. Luottamusväli ja virhemarginaali ovat vain MAB9:ssä; pitkän oppimäärän valtakunnallisissa moduuleissa niitä ei ole.
7. **Kompleksiluvut eivät kuulu LOPS 2019:n valtakunnallisiin moduuleihin.** Applet `lukio-pitka/complex-plane-explorer.html` ei siksi linkity mihinkään tunnisteeseen (paikallinen syventävä sisältö).
8. **Ohjelmistot ovat osa jokaista moduulia.** Jokaisen moduulin tavoitteissa on ohjelmistojen käyttö (MAA11:ssä ohjelmointi). YO-kokeessa on A-osa ilman laskinohjelmistoja ja B-osa niiden kanssa. Tehtävään kannattaa merkitä, onko se tarkoitettu ratkaistavaksi ilman apuvälineitä.
9. **Perusteiden rajaukset.** Perusteet rajaavat: MAY1:n potenssiyhtälö asteluvuilla 2 ja 3; MAA2:n potenssiyhtälö positiivisella kokonaislukueksponentilla; MAA4:n itseisarvoyhtälöt muotoa \|f(x)\| = a tai \|f(x)\| = \|g(x)\| (ei epäyhtälöitä); MAA5:n trigonometriset yhtälöt muotoa sin f(x) = a tai sin f(x) = sin g(x); MAA6:n trigonometristen funktioiden derivaatoista vain sini ja kosini; MAA3:n kappaleista suora lieriö, suora kartio ja pallo.

## 2. Oppiaineen yleiset tavoitteet G1–G8 (tiivistetty)

Sarake **Perusteet** viittaa perusteiden yleisten tavoitteiden luettelon kohtiin 1–8 (L = laaja-alaisen osaamisen teksti).

| ID | Tavoite (opiskelija…) | Perusteet | Vastaa 7–9:n tavoitetta |
|---|---|---|---|
| G1 | luottaa omiin kykyihinsä ja työskentelee pitkäjänteisesti matematiikan parissa, myös yhdessä toisten kanssa | 1, L | T1, T2 |
| G2 | seuraa matemaattista esitystä ja ilmaisee matemaattista ajattelua täsmällisesti suullisesti ja kirjallisesti, käyttää symboleja ja käsitteitä oikein | 5 | T4 |
| G3 | tekee otaksumia, perustelee ja arvioi perustelujen pätevyyttä ja tulosten yleistettävyyttä; erottaa esimerkin yleisestä perustelusta | 4, 5 | T4, T5 |
| G4 | ratkaisee ongelmia kokeillen ja tutkien, käyttää erilaisia ratkaisustrategioita ja arvioi ratkaisun mielekkyyttä | 6, 7 | T5, T6 |
| G5 | mallintaa yhteiskunnan, talouden ja luonnon ilmiöitä ja käytännön ongelmia matemaattisesti ja arvioi mallin hyvyyttä ja rajoituksia | 2, 6 | T7 |
| G6 | käyttää tarkoituksenmukaisia menetelmiä, ohjelmistoja ja tietolähteitä ja ymmärtää, ettei ohjelmiston tulos yksin riitä osoittamaan, todistamaan tai perustelemaan väitettä | 8 | T9, T20 |
| G7 | näkee yhteyksiä matematiikan osa-alueiden välillä ja matematiikan ja muiden tieteiden välillä; siirtyy esitysmuodosta toiseen | L | T3, T7 |
| G8 | ymmärtää matematiikan merkityksen kulttuurissa ja yhteiskunnassa ja pohjana jatko-opinnoille | 2, 3, L | T7, T8 |

## 3. Atomiset oppimistavoitteet moduuleittain

Sarakkeet: **ID** (käytä viitteenä), **Opiskelija osaa…**, **Vk** = ehdotettu vuosikurssi (1 / 2 / 3), **G** = liittyvät yleiset tavoitteet. Moduulien nimet, laajuudet ja asemat ovat perusteiden mukaiset. Poistettuja tunnisteita ei käytetä uudelleen.

### 3.1 Yhteinen moduuli

#### MAY1 Luvut ja yhtälöt (2 op, pakollinen molemmissa oppimäärissä)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAY1.01 | lukujoukot N, Z, Q ja R sekä niiden suhteet; rationaali- ja irrationaaliluvun ero | 1 | G2 |
| MAY1.02 | peruslaskutoimitukset ja laskujärjestyksen; vastaluku, käänteisluku ja itseisarvo | 1 | G2 |
| MAY1.03 | prosenttilaskennan: prosenttiosuus, muutos- ja vertailuprosentti, prosenttiyksikkö | 1 | G5, G8 |
| MAY1.04 | potenssin laskusäännöt kokonaislukueksponentilla | 1 | G2 |
| MAY1.05 | neliö- ja kuutiojuuren | 1 | G2 |
| MAY1.06 | suoraan ja kääntäen verrannollisuuden ja verrannon ongelmanratkaisussa | 1 | G4, G5 |
| MAY1.07 | funktion käsitteen, kuvaajan piirtämisen (myös ohjelmistolla) ja kuvaajan tulkinnan, esim. arvo ja nollakohta | 1 | G2, G5, G6 |
| MAY1.08 | ensimmäisen asteen yhtälön ratkaisemisen ja ratkaisun tarkistamisen | 1 | G4 |
| MAY1.09 | yhtälöparin ratkaisemisen | 1 | G4 |
| MAY1.10 | potenssifunktion ja potenssiyhtälön asteluvuilla 2 ja 3 (x² = a, x³ = a) | 1 | G4 |
| MAY1.11 | murtolukujen laskutoimitukset | 1 | G2 |

### 3.2 Pitkä oppimäärä (MAA)

#### MAA2 Funktiot ja yhtälöt 1 (3 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA2.01 | polynomien yhteen-, vähennys- ja kertolaskun sekä binomikaavat (summan neliö, summan ja erotuksen tulo) | 1 | G2 |
| MAA2.02 | polynomin jakamisen tekijöihin; polynomifunktion nollakohtien ja polynomin tekijöiden yhteyden | 1 | G2, G7 |
| MAA2.03 | polynomifunktion ominaisuudet ja kuvaajan, esim. paraabelin huippu ja nollakohdat | 1 | G2, G5 |
| MAA2.04 | toisen asteen yhtälön: vajaat yhtälöt, ratkaisukaava ja diskriminantti | 1 | G4 |
| MAA2.05 | korkeamman asteen polynomiyhtälön ratkaisemisen tulon nollasäännöllä | 1 | G4 |
| MAA2.06 | yksinkertaisen polynomiepäyhtälön ratkaisemisen, esim. merkkikaavion avulla | 1 | G3, G4 |
| MAA2.07 | rationaali- ja juurifunktion ominaisuudet ja rationaali- ja juuriyhtälön ratkaisemisen | 1 | G4, G5 |
| MAA2.08 | potenssifunktion ja potenssiyhtälön, kun eksponentti on positiivinen kokonaisluku | 1 | G4 |

#### MAA3 Geometria (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA3.01 | kuvioiden ja kappaleiden yhdenmuotoisuuden; pinta-alojen ja tilavuuksien suhteet k² ja k³ | 1 | G3, G5 |
| MAA3.02 | suorakulmaisen kolmion trigonometrian ja Pythagoraan lauseen | 1 | G4 |
| MAA3.03 | sini- ja kosinilauseen sekä kolmion pinta-alan ½ab sin γ | 1 | G4 |
| MAA3.04 | ympyrän, sen osien ja siihen liittyvien suorien geometrian, esim. kehä- ja keskuskulma, kaari, sektori, tangentti | 1 | G3 |
| MAA3.05 | suoraan lieriöön (myös särmiö), suoraan kartioon (myös pyramidi) ja palloon liittyvät pituudet, pinta-alat ja tilavuudet | 1 | G5 |
| MAA3.06 | geometristen lauseiden muotoilemisen, perustelemisen ja käyttämisen; havaintojen, oletusten ja johtopäätösten erottamisen | 1 | G3 |
| MAA3.07 | monikulmioihin liittyvien pituuksien, kulmien ja pinta-alojen laskemisen | 1 | G4 |

#### MAA4 Analyyttinen geometria ja vektorit (3 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA4.01 | käyrän yhtälön käsitteen: piste on käyrällä, jos se toteuttaa yhtälön | 1→2 | G2, G7 |
| MAA4.02 | suoran yhtälön (ratkaistu ja yleinen muoto); suorien yhdensuuntaisuuden ja kohtisuoruuden | 1→2 | G2 |
| MAA4.03 | pisteiden etäisyyden ja pisteen etäisyyden suorasta | 1→2 | G4 |
| MAA4.04 | ympyrän ja paraabelin yhtälön | 1→2 | G7 |
| MAA4.05 | yhtälöryhmän ratkaisemisen | 1→2 | G4 |
| MAA4.06 | itseisarvoyhtälön muotoa \|f(x)\| = a tai \|f(x)\| = \|g(x)\| | 1→2 | G4 |
| MAA4.07 | vektorin käsitteen ja perusominaisuudet; tason vektorien yhteen- ja vähennyslaskun ja luvulla kertomisen | 1→2 | G2 |
| MAA4.08 | tason vektorin koordinaattiesityksen ja pituuden; tason vektorien pistetulon ja välisen kulman | 1→2 | G2 |
| MAA4.09 | tasogeometrian ongelmien ratkaisemisen vektoreilla | 1→2 | G3, G4 |

#### MAA5 Funktiot ja yhtälöt 2 (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA5.01 | suunnatun kulman ja radiaanin | 2 | G2 |
| MAA5.02 | yksikköympyrän; sinin ja kosinin määritelmän ja symmetrioiden tutkimisen sen avulla | 2 | G2, G7 |
| MAA5.03 | sini- ja kosinifunktion kuvaajineen, symmetria- ja jaksollisuusominaisuuksineen | 2 | G2 |
| MAA5.04 | sini- ja kosiniyhtälön muotoa sin f(x) = a tai sin f(x) = sin g(x) ratkaisemisen (kaikki ratkaisut) | 2 | G4 |
| MAA5.05 | murtopotenssin ja sen yhteyden juureen | 2 | G2 |
| MAA5.06 | eksponenttifunktion ominaisuudet ja eksponenttiyhtälön | 2 | G4, G5 |
| MAA5.07 | logaritmin, logaritmin laskusäännöt, logaritmifunktion ja logaritmiyhtälön | 2 | G4 |
| MAA5.08 | yhteyden sin² x + cos² x = 1 soveltamisen | 2 | G3 |

#### MAA6 Derivaatta (3 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA6.01 | funktion raja-arvon havainnollisesti | 2 | G2, G3 |
| MAA6.02 | funktion jatkuvuuden havainnollisesti | 2 | G2, G3 |
| MAA6.03 | derivaatan tulkinnan funktion muutosnopeutena, esim. erotusosamäärän raja-arvo ja tangentin kulmakerroin | 2 | G2, G7 |
| MAA6.04 | polynomifunktion derivoinnin ja derivointisäännöt | 2 | G2 |
| MAA6.05 | tulon ja osamäärän derivaatan; rationaalifunktion derivaatan | 2 | G2 |
| MAA6.06 | yhdistetyn funktion derivaatan | 2 | G2 |
| MAA6.07 | juurifunktion, sini- ja kosinifunktion sekä eksponentti- ja logaritmifunktion derivaatat | 2 | G2 |
| MAA6.08 | funktion kulun tutkimisen derivaatan avulla (kulkukaavio, monotonisuus, ääriarvot) | 2 | G3, G4 |
| MAA6.09 | suurimman ja pienimmän arvon suljetulla välillä ja ääriarvosovellukset | 2 | G4, G5 |

#### MAA7 Integraalilaskenta (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA7.01 | integraalifunktion ja integroimisvakion | 2 | G2 |
| MAA7.02 | tärkeimpien alkeisfunktioiden integraalifunktiot | 2 | G2 |
| MAA7.03 | määrätyn integraalin ja sen yhteyden pinta-alaan; laskemisen integraalifunktion avulla | 2 | G3, G7 |
| MAA7.04 | pinta-alan laskemisen määrätyllä integraalilla (käyrän ja x-akselin välissä, kahden käyrän välissä) | 2 | G4 |
| MAA7.05 | tilavuuden laskemisen määrätyllä integraalilla, esim. pyörähdyskappale | 2 | G4 |
| MAA7.06 | integraalilaskennan sovellukset, esim. muutosnopeudesta kokonaismuutokseen | 2 | G5, G7 |
| MAA7.07 | määrätyn integraalin numeerisen laskemisen suorakaidesäännöllä | 2 | G4, G6 |

#### MAA8 Tilastot ja todennäköisyys (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA8.01 | diskreetin tilastollisen jakauman havainnollistamisen ja tunnusluvut: keskiluvut (keskiarvo, moodi, mediaani) ja keskihajonta | 2→3 | G5, G6 |
| MAA8.02 | kahden muuttujan yhteisjakauman havainnollistamisen, korrelaatiokertoimen ja lineaarisen regression | 2→3 | G5, G8 |
| MAA8.03 | kombinatoriikan: permutaatiot ja kombinaatiot, esim. tuloperiaate | 2→3 | G4 |
| MAA8.04 | klassisen ja tilastollisen todennäköisyyden | 2→3 | G2 |
| MAA8.05 | todennäköisyyden laskusäännöt, esim. komplementti, yhteen- ja kertolaskusääntö | 2→3 | G3, G4 |
| MAA8.06 | diskreetin todennäköisyysjakauman ja sen odotusarvon määrittämisen ja tulkinnan | 2→3 | G5 |
| MAA8.07 | binomijakauman | 2→3 | G5 |

#### MAA9 Talousmatematiikka (1 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA9.01 | aritmeettisen ja geometrisen lukujonon | 2→3 | G2 |
| MAA9.02 | aritmeettisen ja geometrisen lukujonon summan | 2→3 | G4 |
| MAA9.03 | koronkoron, talletukset ja säästämisen | 2→3 | G5, G8 |
| MAA9.04 | lainojen laskemisen, esim. annuiteetti ja tasalyhennys | 2→3 | G5, G8 |
| MAA9.05 | *poistettu versiossa 2: verotus, indeksi ja valuutat eivät kuulu MAA9:ään; ks. MAB6.02, MAB6.04, MAB6.05* | | |
| MAA9.06 | nykyarvon ja diskonttauksen | 2→3 | G5, G8 |
| MAA9.07 | lukujonoja ja summia hyödyntävät taloudelliset mallit: resurssien riittävyys, talouden suunnittelu, yrittäjyys ja kannattavuus; mallien rajoitukset | 2→3 | G5, G8 |

#### MAA10 3D-geometria (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA10.01 | vektoriesityksen kolmiulotteisessa koordinaatistossa | 3 | G2 |
| MAA10.02 | piste- ja ristitulon | 3 | G2 |
| MAA10.03 | pisteen, suoran ja tason avaruudessa | 3 | G7 |
| MAA10.04 | kulmat avaruudessa | 3 | G4 |
| MAA10.05 | yhden muuttujan differentiaali- ja integraalilaskennan sovelluksia avaruusgeometriassa, esim. ääriarvosovellukset | 3 | G7 |
| MAA10.06 | kahden muuttujan funktion ja pinnan avaruudessa | 3 | G7 |

#### MAA11 Algoritmit ja lukuteoria (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA11.01 | algoritmisen ajattelun peruskäsitteet (peräkkäisyys, valinta, toisto) ja vuokaavion; yksinkertaisten algoritmien, lajittelualgoritmien tai yhtälön numeerisen ratkaisun algoritmin ohjelmoinnin | 3 | G6 |
| MAA11.02 | konnektiivit ja totuusarvot | 3 | G3 |
| MAA11.03 | kokonaislukujen jaollisuuden ja jakoyhtälön | 3 | G3 |
| MAA11.04 | kongruenssin | 3 | G3 |
| MAA11.05 | Eukleideen algoritmin, aritmetiikan peruslauseen ja alkulukujen ominaisuuksia | 3 | G3, G6 |

#### MAA12 Analyysi ja jatkuva jakauma (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA12.01 | paloittain määritellyn funktion | 3 | G2 |
| MAA12.02 | funktion jatkuvuuden ja derivoituvuuden tutkimisen | 3 | G3 |
| MAA12.03 | jatkuvien ja derivoituvien funktioiden yleisiä ominaisuuksia | 3 | G3 |
| MAA12.04 | aidosti monotonisen funktion käänteisfunktion muodostamisen ja tutkimisen | 3 | G2, G7 |
| MAA12.05 | integraalilaskennan täydentävät taidot ja epäoleelliset integraalit | 3 | G2 |
| MAA12.06 | jatkuvan todennäköisyysjakauman; normaalijakauman ja normittamisen | 3 | G5 |
| MAA12.07 | funktioiden raja-arvot äärettömyydessä | 3 | G2, G3 |

### 3.3 Lyhyt oppimäärä (MAB)

#### MAB2 Lausekkeet ja yhtälöt (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB2.01 | muotoilla ongelman yhtälöksi sekä tulkita ja arvioida ratkaisun | 1 | G4, G5 |
| MAB2.02 | ratkaista yhtälön käsin ja ohjelmistolla | 1 | G4, G6 |
| MAB2.03 | toisen asteen polynomifunktion ja sen kuvaajan, myös ohjelmistolla | 1 | G2, G6 |
| MAB2.04 | toisen asteen yhtälön ratkaisemisen | 1 | G4 |
| MAB2.05 | aritmeettisen lukujonon ja summan | 1 | G5 |
| MAB2.06 | geometrisen lukujonon ja summan | 1 | G5 |
| MAB2.07 | muodostaa lausekkeita annettuihin ongelmiin ja käsitellä niitä yhtälöitä ratkaistessa (sieventäminen ei ole perusteissa erillinen sisältö) | 1 | G2 |

#### MAB3 Geometria (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB3.01 | kuvioiden yhdenmuotoisuuden, esim. mittakaava | 1 | G5 |
| MAB3.02 | suorakulmaisen kolmion trigonometrian | 1 | G4 |
| MAB3.03 | Pythagoraan lauseen ja sen käänteislauseen | 1 | G3 |
| MAB3.04 | kuvioiden ja kappaleiden pinta-alat ja tilavuudet | 1 | G5 |
| MAB3.05 | geometrian menetelmien käytön tasokoordinaatistossa | 1 | G7 |

#### MAB4 Matemaattisia malleja (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB4.01 | lineaarisen mallin soveltamisen; kulmakerroin muutosnopeutena | 1→2 | G5 |
| MAB4.02 | eksponentiaalisen mallin soveltamisen | 1→2 | G5 |
| MAB4.03 | eksponenttiyhtälön ratkaisemisen (perusteet mainitsevat ohjelmiston; logaritmia ei nimetä) | 1→2 | G4, G6 |
| MAB4.04 | ennusteiden tekemisen ja mallin hyvyyden ja käyttökelpoisuuden arvioinnin | 1→2 | G4, G5 |
| MAB4.05 | polynomi- ja eksponenttifunktion ominaisuuksien tutkimisen ja polynomiyhtälön ratkaisemisen ohjelmistolla sovelluksissa | 1→2 | G5, G6 |

#### MAB5 Tilastot ja todennäköisyys (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB5.01 | tilastoaineiston havainnollistamisen taulukoin ja diagrammein; datan haun ja käsittelyn ohjelmistolla | 2 | G5, G6 |
| MAB5.02 | tunnuslukujen määrittämisen, esim. keskiarvo, mediaani, moodi, keskihajonta | 2 | G5 |
| MAB5.03 | regression ja korrelaation käsitteet | 2 | G5, G8 |
| MAB5.04 | havainnon ja poikkeavan havainnon | 2 | G4 |
| MAB5.05 | ennusteiden tekemisen aineiston perusteella | 2 | G5 |
| MAB5.06 | todennäköisyyden käsitteen, yhteen- ja kertolaskusäännön ja todennäköisyyslaskennan malleja | 2 | G2, G4 |
| MAB5.07 | kombinaatiot ja tuloperiaatteen | 2 | G4 |

#### MAB6 Talousmatematiikan alkeet (1 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB6.01 | suhteellisen osuuden, vertailun ja muutoksen laskemisen (prosenttilaskennan syventäminen) | 2 | G5, G8 |
| MAB6.02 | indeksin | 2 | G8 |
| MAB6.03 | korkokäsitteen ja yksinkertaisen koron | 2 | G8 |
| MAB6.04 | verotuksen laskut | 2 | G8 |
| MAB6.05 | valuuttamuunnokset | 2 | G8 |

#### MAB7 Talousmatematiikka (1 op, pakollinen)

Sisältö on perusteissa sama kuin MAA9:n.

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB7.01 | koronkoron, talletukset ja säästämisen | 2→3 | G5, G8 |
| MAB7.02 | lainojen laskemisen | 2→3 | G5, G8 |
| MAB7.03 | lukujonoja ja summia hyödyntävät taloudelliset mallit: resurssien riittävyys, talouden suunnittelu, yrittäjyys ja kannattavuus; mallien rajoitukset | 2→3 | G5, G8 |
| MAB7.04 | aritmeettisen ja geometrisen lukujonon ja niiden summat talouden ongelmissa | 2→3 | G4, G5 |
| MAB7.05 | nykyarvon ja diskonttauksen | 2→3 | G5, G8 |

#### MAB8 Matemaattinen analyysi (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB8.01 | funktion muutosnopeuden tutkimisen graafisin ja numeerisin menetelmin, myös ohjelmistolla | 3 | G2, G5, G6 |
| MAB8.02 | polynomifunktion derivaatan ja sen tulkinnan muutosnopeutena | 3 | G2 |
| MAB8.03 | polynomifunktion merkin ja kulun tutkimisen derivaatan avulla | 3 | G3 |
| MAB8.04 | polynomifunktion suurimman ja pienimmän arvon suljetulla välillä | 3 | G4, G5 |

#### MAB9 Tilastolliset ja todennäköisyysjakaumat (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB9.01 | normaalijakauman mallina | 3 | G5 |
| MAB9.02 | jakauman normittamisen käsitteet (odotusarvo ja keskihajonta) | 3 | G2 |
| MAB9.03 | toistokokeen ja binomijakauman | 3 | G5 |
| MAB9.04 | luottamusvälin ja virhemarginaalin käsitteen ja määrittämisen ohjelmistolla | 3 | G3, G8 |
| MAB9.05 | tilastojen käsittelyn ja tutkimisen ohjelmistolla; jakaumien tunnuslukujen ja todennäköisyyksien määrittämisen | 3 | G6 |

## 4. Arviointi ja tehtävien tasot

**Arviointi lukiossa.** Opinnot arvioidaan opintojaksoittain asteikolla 4–10; arviointi perustuu moduulikohtaisiin tavoitteisiin, joista paikalliset opintojaksot muodostetaan. Oppimäärän arvosana on pakollisten ja valtakunnallisten valinnaisten opintojen arvosanojen opintopisteillä painotettu keskiarvo. Matematiikan arviointiteksti nimeää painopisteet (laskutaito, menetelmien valinta, matemaattinen ajattelu ja ongelmanratkaisu, päätelmien perustelu ja analysointi, ohjelmistojen valinta ja käyttö) mutta ei anna arvosanakriteerejä. Käytännön vaatimustason määrää ylioppilastutkinto.

**Ylioppilastutkinto.** Lyhyt ja pitkä matematiikka ovat eri kokeita. Kokeessa on A-osa ilman laskinohjelmistoja ja B-osa, jossa ohjelmistot ovat käytössä. YTL julkaisee jokaisesta kokeesta "hyvän vastauksen piirteet", joissa kuvataan pisteytys ja yleisimmät virheet. Ne ovat ainoa löydetty suomalainen, tehtävätasoinen lähde lukion vaikeista kohdista.

**Tasot** (sama merkintä kuin 7–9-tiedostossa, esim. `MAA6.06 / H`):

| Taso | Vastaa (ehdotus) | Tehtävätyyppi |
|---|---|---|
| P (perus) | opintojakson arvosana 5–6 | yksi askel, tuttu malli, kaava annettu |
| T (tyydyttävä) | 7 | suora laskutehtävä ilman vihjettä, YO:n A-osan perustehtävä |
| H (hyvä) | 8 | kaksi–kolme vaihetta, käsitteen tunnistaminen, perustelu |
| K (kiitettävä) | 9–10 | soveltava tai avoin ongelma, useita ratkaisutapoja, YO:n B2-osan tyyppinen tehtävä |

## 5. Vuosikurssijako (ehdotus)

| Vuosikurssi | Lyhyt | Pitkä |
|---|---|---|
| 1 | MAY1, MAB2, MAB3, (MAB4) | MAY1, MAA2, MAA3, (MAA4) |
| 2 | MAB4, MAB5, MAB6, MAB7 | MAA4, MAA5, MAA6, MAA7, (MAA8) |
| 3 | MAB8, MAB9 | MAA8, MAA9, MAA10–MAA12 |

Jako noudattaa tavallista kolmen vuoden suunnitelmaa ja kustantajien moduulijärjestystä. Paikallinen OPS ratkaisee.

## 6. Ohje tehtävien ja applettien laatimiseen

- Yksi tehtävä mittaa ensisijaisesti yhtä tunnistetta. Merkitse oppimäärä tunnisteen kautta (`MAB…`, `MAA…`, `MAY1…`).
- Merkitse, onko tehtävä tarkoitettu ilman apuvälineitä (A-osan tyyppi) vai ohjelmiston kanssa (B-osan tyyppi).
- Pysy perusteiden rajauksissa (luku 1, havainto 9). Esimerkiksi itseisarvoepäyhtälö, tangentin derivaatta ja ehdollinen todennäköisyys eivät ole perusteissa nimettyjä sisältöjä; niitä käyttävä tehtävä on paikallista syventävää sisältöä eikä saa pakollisen moduulin tunnistetta pääviitteeksi.
- Laskutehtävien lisäksi jokaisessa moduulissa vähintään yksi tehtävä, jossa perustellaan (G3) tai arvioidaan tuloksen mielekkyyttä (G4).
- Desimaalierotin pilkku, miinusmerkki U+2212, suomenkieliset termit (derivaatta, integraalifunktio, kulkukaavio, kulmakerroin, radiaani, odotusarvo, keskihajonta, luottamusväli).
- Lyhyen oppimäärän tehtävissä painottuvat sovellukset ja mallit, pitkän oppimäärän tehtävissä perustelu ja symbolinen käsittely.
- Virhekäsitykset ja niiden tunnisteet: `../misconceptions/lukio_misconceptions.md`.

**Yleisiä virhekäsityksiä lukiossa (vääriksi vastausvaihtoehdoiksi ja "Varo virhekäsitystä" -laatikoihin).** Täysi luettelo lähteineen on virhekäsitystiedostossa.

| ID | Virhekäsitys |
|---|---|
| MAY1.04, MAA5.05 | 2⁻¹ = −2; a^(1/3) = a/3; (a + b)² = a² + b² jatkuu lukioon |
| MAA2.04–MAA2.05 | x² = 3x jaetaan x:llä, ratkaisu x = 0 katoaa; (x − 2)(x − 3) = 6 ⇒ x = 8 tai x = 9 |
| MAA2.06 | epäyhtälö kerrotaan lausekkeella, jonka merkkiä ei tiedetä; x² < 4 ⇒ x < ±2 |
| MAA4.06 | \|x − 3\| = 5 ⇒ vain x = 8 (itseisarvo "poistaa miinuksen") |
| MAA4.07 | vektorien summan pituus on pituuksien summa, \|a + b\| = \|a\| + \|b\| |
| MAA5.04 | sin x = ½ ⇒ vain x = 30° (jaksollisuus unohtuu) |
| MAA5.07 | log(a + b) = log a + log b |
| MAA6.01 | raja-arvoa ei voi saavuttaa; 0,999… < 1 |
| MAA6.05–MAA6.06 | (fg)′ = f′g′; yhdistetyn funktion sisäderivaatta unohtuu |
| MAA6.08 | f′(x) = 0 ⇒ aina ääriarvo |
| MAA7.04 | määrätty integraali on aina pinta-ala, myös x-akselin alapuolella |
| MAB4.02, MAA9.03 | eksponentiaalinen kasvu arvioidaan lineaariseksi; 10 vuotta 3 %:n korolla = 30 % |
| MAA8.02, MAB5.03 | korrelaatio osoittaa syy-yhteyden |
| MAA8.04 | kaikki tulosvaihtoehdot ovat yhtä todennäköisiä (kahden nopan summa) |
| MAB9.04 | 95 %:n luottamusväli sisältää todellisen arvon 95 %:n todennäköisyydellä |

## 7. Nykyiset appletit ja kattavuus

| Applet | Kattaa |
|---|---|
| lukio-pitka/paraabeli-toisen-asteen-juuret.html | MAA2.03, MAA2.04, MAB2.03, MAB2.04 |
| lukio-pitka/yksikkoympyra-sini-kosini.html | MAA5.02, MAA5.03 |
| lukio-pitka/eksponentti-logaritmi.html | MAA5.06, MAA5.07 |
| lukio-pitka/derivaatta-sekantti-tangentti.html | MAA6.03, MAB8.01 |
| lukio-pitka/integraali-riemannin-summa.html | MAA7.03, MAA7.04, MAA7.07 |
| lukio-pitka/derivative_visualizer.html, integral-speed-distance.html, Vector_addition.html | MAA6.03, MAA7.06, MAA4.07 (vanhoja, eivät noudata APPLET_SPEC.md:tä) |
| lukio-pitka/complex-plane-explorer.html | ei valtakunnallista tunnistetta |
| lukio-lyhyt/makeishinnoittelu.html | MAB2.03, MAB4.01 (voiton maksimointi paraabelin huipusta) |
| lukio-lyhyt/pokerikasien-todennakoisyydet.html | MAB5.06, MAB5.07, MAA8.03 |

Suurimmat aukot (ehdokkaita BACKLOG.md:hen, applettiputken päätös): MAA4.07 vektorien yhteenlasku ja pituus, MAA6.08 kulkukaavio ja ääriarvot, MAA8.02 / MAB5.03 korrelaatio vs. syy-yhteys, MAB4.02 / MAA9.03 lineaarinen vs. eksponentiaalinen kasvu, MAB9.01–MAB9.04 normaalijakauma ja luottamusväli, MAA9.06 / MAB7.05 nykyarvo ja diskonttaus.

## 8. Muutokset versiossa 2 (L-R02)

Kaikki †-merkinnät on ratkaistu ePerusteiden tekstin perusteella; †-merkkejä on enää tässä taulukossa versio 1:n lainauksina.

| Kohta | Versio 1 | Versio 2 |
|---|---|---|
| MAB6 nimi | "Talousmatematiikka I" (myös "Talousmatematiikan alkeet" †) | **Talousmatematiikan alkeet** |
| MAB7 nimi | "Talousmatematiikka II" † | **Talousmatematiikka**; sisältö sama kuin MAA9 |
| MAY1.09 yhtälöpari † | | vahvistettu |
| MAY1.10 potenssiyhtälö xⁿ = a † | | vahvistettu, rajattu asteluvuille 2 ja 3 |
| MAA2.07 rationaali- ja juurifunktio † | | vahvistettu |
| MAA3.04 ympyrä † | | vahvistettu ("ympyrän ja sen osien ja siihen liittyvien suorien geometria") |
| MAA3.05 kappaleet | särmiö, lieriö, kartio, pallo | suora lieriö, suora kartio, pallo |
| MAA4.06 itseisarvoepäyhtälö † | | poistettu: perusteissa vain yhtälöt \|f(x)\| = a ja \|f(x)\| = \|g(x)\| |
| MAA4.08 pistetulo ja kulma † | | vahvistettu |
| MAA5.04 | sini- ja kosiniyhtälö | rajattu muotoon sin f(x) = a, sin f(x) = sin g(x) |
| MAA5.07 logaritmiyhtälö † | | vahvistettu; logaritmifunktio lisätty |
| MAA6.01 | toispuoleiset raja-arvot | ei nimetty perusteissa; "havainnollinen käsitys" |
| MAA6.07 derivaatat † | "trigonometristen" | vahvistettu, rajattu siniin ja kosiniin |
| MAA7.05 pyörähdyskappale † | | tilavuus määrätyllä integraalilla vahvistettu; pyörähdyskappale esimerkkinä |
| MAA8.04 geometrinen todennäköisyys † | | poistettu: perusteissa klassinen ja tilastollinen |
| MAA8.05 ehdollinen todennäköisyys † | | poistettu: perusteissa vain "todennäköisyyden laskusäännöt" |
| MAA9.03 | yksinkertainen korko mukana | yksinkertainen korko poistettu (kuuluu MAB6:een) |
| MAA9.05 verotus, indeksi, valuutat † | | **tunniste poistettu**: kuuluvat vain MAB6:een |
| MAA12.05 integraalilaskennan täydentävät taidot † | | vahvistettu; epäoleelliset integraalit lisätty |
| MAA12.06 normaalijakauma † | | vahvistettu, normittaminen lisätty |
| MAB2.07 sieventäminen, kaavan ratkaiseminen † | | muotoiltu perusteiden tavoitteen mukaan (lausekkeiden muodostaminen) |
| MAB3.05 tasokoordinaatisto † | | vahvistettu |
| MAB4.03 logaritmi † | | logaritmia ei nimetä; ratkaisu ohjelmistolla |
| MAB5.02 kvartiilit † | | poistettu: perusteissa vain "tunnuslukujen määrittäminen" |
| MAB5.07 kombinatoriikka † | | vahvistettu ("kombinaatiot ja tuloperiaate") |
| Luku 4 arvosanakriteerit † | | vahvistettu: perusteissa ei ole matematiikan arvosanakriteerejä |
| Uudet tunnisteet | | MAY1.11, MAA2.08, MAA3.07, MAA5.08, MAA7.07, MAA9.06, MAA9.07, MAA12.07, MAB4.05, MAB7.04, MAB7.05 |
| G1–G8 | | sisältö ennallaan, sanamuotoja tarkennettu; lisätty vastaavuus perusteiden kohtiin 1–8 |

## Lähteet

- Opetushallitus: Lukion opetussuunnitelman perusteet 2019 (OPH-2263-2019), luku 6.6 Matematiikka. ePerusteet: https://eperusteet.opintopolku.fi/#/2270454/lukiokoulutus/6828810/oppiaine/6831746 ; koneluettava teksti: https://eperusteet.opintopolku.fi/eperusteet-service/api/external/peruste/6828810 (kenttä `lops2019.oppiaineet`, koodi `MA`), luettu 2.10.2026
- OPH: Lyhyen matematiikan tukimateriaalia LOPS 2019:n toteuttamiseen, https://www.oph.fi/sites/default/files/documents/lops2019_mab.pdf
- MAOL: Pitkän matematiikan tukimateriaalia LOPS 2019:n toteuttamiseen, https://maol.fi/app/uploads/2020/01/LOPS2019_MAA_MAOL.pdf
- YTL: hyvän vastauksen piirteet, esim. https://tiedostot.ylioppilastutkinto.fi/kokeet/2026-03-18_M_fi/grading-instructions.html
