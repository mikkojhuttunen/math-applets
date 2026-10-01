# Matematiikka, lukio (LOPS 2019): oppimistavoitteet tehtävien ja applettien laatimiseen

Tämä tiedosto on lukion vastine tiedostoille `OPS_1-6_oppimistavoitteet.md` ja `OPS_7-9_oppimistavoitteet.md`. Se kattaa lukion matematiikan yhteisen moduulin (MAY1), lyhyen oppimäärän (MAB) ja pitkän oppimäärän (MAA). Jokaisella oppimistavoitteella on pysyvä tunniste (esim. `MAA6.06`), johon tehtävät, appletit, virhekäsitykset ja backlog-merkinnät voivat viitata.

Versio: 2026-10-01

## 0. Lähteet ja luotettavuus

| Osa | Lähde | Luotettavuus |
|---|---|---|
| Moduulirakenne, moduulien nimet ja laajuudet (op), pakollinen / valtakunnallinen valinnainen | Lukion opetussuunnitelman perusteet 2019 (OPH-2263-2019), luku 6.6, sellaisena kuin se toistuu useiden lukioiden LOPS2021-sivuilla ja kustantajien (Otava, Sanoma Pro, Studeo) moduulikohtaisissa oppikirjoissa, haettu 1.10.2026 | Vahvistettu usealla toisistaan riippumattomalla lähteellä. Laajuudet täsmäävät tuntijakoon (lyhyt 12 op, pitkä 20 op pakollisia). |
| Moduulien keskeiset sisällöt (luku 3) | Sama perusteiden teksti koulujen opetussuunnitelmasivuilla (peda.net, tampere.fi, sites.utu.fi/lops2021tnk) ja OPH:n / MAOL:n tukimateriaaleissa (`lops2019_mab.pdf`, `LOPS2019_MAA_MAOL.pdf`), hakutulosten otteina | **Toisen käden lähde, ei sanatarkka.** OPH:n sivut ja ePerusteet eivät olleet luettavissa tästä ympäristöstä (verkkorajaus). Epävarmat rivit merkitty †. Tarkista ePerusteista ennen virallista käyttöä. |
| Oppiaineen yleiset tavoitteet G1–G8 (luku 2) | LOPS 2019, matematiikan oppiaineen tehtävä ja yleiset tavoitteet | **Tiivistetty ja numeroitu tätä tiedostoa varten.** Perusteissa tavoitteet ovat luettelona ilman tunnisteita. |
| Atomiset oppimistavoitteet (luku 3) | Pilkottu keskeisistä sisällöistä | Jokainen rivi palautuu moduulin sisältöön; † = sisällön kuuluminen juuri tähän moduuliin tarkistamatta |
| Arviointi ja tasot (luku 4) | LOPS 2019, luku 6.6 ja yleinen arviointiluku; ylioppilastutkintolautakunnan (YTL) kokeiden "hyvän vastauksen piirteet" | Lukiolle ei hauissa löytynyt kansallisia arvosanakriteerejä (vrt. perusopetuksen 5/7/8/9-taulukot). Tasot P/T/H/K on siksi johdettu YO-kokeen rakenteesta. † |
| Vuosikurssijako (luku 5) | **Ehdotus.** Perusteet eivät jaa moduuleja vuosikursseille; jaon tekee lukion oma OPS. | Tarkistettava paikallisesta OPS:sta |

## 1. Havainnot lähteistä

1. **Rakenne poikkeaa perusopetuksesta.** Lukion matematiikassa ei ole numeroituja T-tavoitteita eikä sisältöalueita S1–S6. Perusteet antavat oppiaineen yleiset tavoitteet ja jokaiselle moduulille omat tavoitteet ja keskeiset sisällöt. Tunnisteet on siksi muodostettu moduulikoodista: `MAY1.03`, `MAB4.02`, `MAA6.06`.
2. **Yhteinen alku.** MAY1 Luvut ja yhtälöt (2 op) kuuluu molempiin oppimääriin. Se kertaa ja syventää yläkoulun lukukäsitettä, potenssia, verrannollisuutta, funktiota ja yhtälöä, joten yläkoulun virhekäsitykset (7–9-tiedoston `S2.01`, `S2.10`, `S2.11`, `S3.02`, `S3.08`, `S4.05`) jatkuvat siinä suoraan.
3. **Moduulin numero ei kerro sisältöä oppimäärien välillä.** MAB3 ja MAA3 ovat molemmat geometriaa, mutta MAB5 on tilastoja ja MAA5 trigonometriaa, eksponenttia ja logaritmia. Tunnisteet ovat siksi aina oppimääräkohtaisia.
4. **Talousmatematiikka on jaettu.** Lyhyessä oppimäärässä kaksi 1 op:n moduulia (MAB6, MAB7), pitkässä yksi (MAA9, 1 op). Moduulien MAB6 ja MAB7 nimet vaihtelevat lähteissä ("Talousmatematiikan alkeet" / "Talousmatematiikka"). †
5. **Analyysi lyhyessä oppimäärässä on valinnaista.** Derivaatta on lyhyessä vain valtakunnallisessa valinnaisessa moduulissa MAB8. Normaalijakauma ja luottamusväli ovat lyhyessä moduulissa MAB9, pitkässä vasta valinnaisessa MAA12.
6. **Kompleksiluvut eivät kuulu LOPS 2019:n valtakunnallisiin moduuleihin.** Applet `lukio-pitka/complex-plane-explorer.html` ei siksi linkity mihinkään tunnisteeseen (paikallinen syventävä sisältö).
7. **Ohjelmistot ovat osa sisältöä.** Useat moduulit (MAB2, MAB4, MAB5, MAB9, MAA8) edellyttävät yhtälöiden ratkaisemista tai tilastojen käsittelyä ohjelmistolla. YO-kokeessa on A-osa ilman laskinohjelmistoja ja B-osa niiden kanssa. Tehtävään kannattaa merkitä, onko se tarkoitettu ratkaistavaksi ilman apuvälineitä.

## 2. Oppiaineen yleiset tavoitteet G1–G8 (tiivistetty)

| ID | Tavoite (opiskelija…) | Vastaa 7–9:n tavoitetta |
|---|---|---|
| G1 | luottaa omiin kykyihinsä ja työskentelee pitkäjänteisesti matematiikan parissa, myös yhdessä toisten kanssa | T1, T2 |
| G2 | ilmaisee matemaattista ajattelua täsmällisesti suullisesti ja kirjallisesti, käyttää symboleja ja käsitteitä oikein | T4 |
| G3 | perustelee, päättelee ja todistaa; erottaa esimerkin yleisestä perustelusta | T4, T5 |
| G4 | ratkaisee ongelmia ja arvioi ratkaisun ja tuloksen mielekkyyttä | T5, T6 |
| G5 | mallintaa ilmiöitä matemaattisesti ja arvioi mallin hyvyyttä ja rajoituksia | T7 |
| G6 | käyttää teknisiä apuvälineitä (CAS, taulukkolaskenta, dynaaminen geometria, ohjelmointi) tarkoituksenmukaisesti | T9, T20 |
| G7 | näkee yhteyksiä matematiikan osa-alueiden välillä ja matematiikan ja muiden tieteiden välillä | T3, T7 |
| G8 | ymmärtää matematiikan merkityksen kulttuurissa, yhteiskunnassa ja jatko-opinnoissa | T7, T8 |

## 3. Atomiset oppimistavoitteet moduuleittain

Sarakkeet: **ID** (käytä viitteenä), **Opiskelija osaa…**, **Vk** = ehdotettu vuosikurssi (1 / 2 / 3), **G** = liittyvät yleiset tavoitteet. † = kuuluminen tähän moduuliin tarkistettava ePerusteista.

### 3.1 Yhteinen moduuli

#### MAY1 Luvut ja yhtälöt (2 op, pakollinen molemmissa oppimäärissä)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAY1.01 | lukujoukot N, Z, Q ja R sekä niiden suhteet; rationaali- ja irrationaaliluvun ero | 1 | G2 |
| MAY1.02 | peruslaskutoimitukset ja laskujärjestyksen; vastaluku, käänteisluku ja itseisarvo | 1 | G2 |
| MAY1.03 | prosenttilaskennan: prosenttiosuus, muutos- ja vertailuprosentti, prosenttiyksikkö | 1 | G5, G8 |
| MAY1.04 | potenssin laskusäännöt kokonaislukueksponentilla | 1 | G2 |
| MAY1.05 | neliö- ja kuutiojuuren | 1 | G2 |
| MAY1.06 | suoraan ja kääntäen verrannollisuuden ja verrannon | 1 | G5 |
| MAY1.07 | funktion käsitteen: määrittelyjoukko, arvo, nollakohta, kuvaajan piirtäminen ja tulkinta | 1 | G2, G5 |
| MAY1.08 | ensimmäisen asteen yhtälön ratkaisemisen ja ratkaisun tarkistamisen | 1 | G4 |
| MAY1.09 | yhtälöparin ratkaisemisen † | 1 | G4 |
| MAY1.10 | potenssifunktion ja potenssiyhtälön xⁿ = a † | 1 | G4 |

### 3.2 Pitkä oppimäärä (MAA)

#### MAA2 Funktiot ja yhtälöt 1 (3 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA2.01 | polynomien yhteen-, vähennys- ja kertolaskun sekä binomikaavat (a ± b)² ja (a + b)(a − b) | 1 | G2 |
| MAA2.02 | polynomin jakamisen tekijöihin (yhteinen tekijä, binomikaavat, nollakohdat) | 1 | G2 |
| MAA2.03 | ensimmäisen ja toisen asteen polynomifunktion kuvaajineen (paraabelin huippu ja nollakohdat) | 1 | G2, G7 |
| MAA2.04 | toisen asteen yhtälön: vajaat yhtälöt, ratkaisukaava ja diskriminantti | 1 | G4 |
| MAA2.05 | korkeamman asteen polynomiyhtälön ratkaisemisen tulon nollasäännöllä | 1 | G4 |
| MAA2.06 | polynomiepäyhtälön ratkaisemisen merkkikaavion avulla | 1 | G3, G4 |
| MAA2.07 | rationaali- ja juurifunktion ja -yhtälön † | 1 | G4 |

#### MAA3 Geometria (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA3.01 | kuvioiden ja kappaleiden yhdenmuotoisuuden; pinta-alojen ja tilavuuksien suhteet k² ja k³ | 1 | G3, G5 |
| MAA3.02 | suorakulmaisen kolmion trigonometrian ja Pythagoraan lauseen | 1 | G4 |
| MAA3.03 | sini- ja kosinilauseen sekä kolmion pinta-alan ½ab sin γ | 1 | G4 |
| MAA3.04 | ympyrään liittyvät kulmat ja suorat (kehä- ja keskuskulma, tangentti) † | 1 | G3 |
| MAA3.05 | kappaleiden (särmiö, lieriö, kartio, pallo) pinta-alat ja tilavuudet | 1 | G5 |
| MAA3.06 | geometrisen päättelyn ja perustelun; havaintojen, oletusten ja johtopäätösten erottamisen | 1 | G3 |

#### MAA4 Analyyttinen geometria ja vektorit (3 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA4.01 | käyrän yhtälön käsitteen: piste on käyrällä, jos se toteuttaa yhtälön | 1→2 | G2, G7 |
| MAA4.02 | suoran yhtälön (ratkaistu ja yleinen muoto); suorien yhdensuuntaisuuden ja kohtisuoruuden | 1→2 | G2 |
| MAA4.03 | kahden pisteen etäisyyden, keskipisteen ja pisteen etäisyyden suorasta | 1→2 | G4 |
| MAA4.04 | ympyrän ja paraabelin yhtälön | 1→2 | G7 |
| MAA4.05 | yhtälöryhmän ratkaisemisen | 1→2 | G4 |
| MAA4.06 | itseisarvoyhtälön (ja -epäyhtälön †) | 1→2 | G4 |
| MAA4.07 | vektorin käsitteen; tasovektorien yhteen- ja vähennyslaskun ja luvulla kertomisen | 1→2 | G2 |
| MAA4.08 | vektorin koordinaattiesityksen, pituuden ja yksikkövektorin; pistetulon ja vektorien välisen kulman † | 1→2 | G2 |
| MAA4.09 | tasogeometrian ongelmien ratkaisemisen vektoreilla | 1→2 | G3, G4 |

#### MAA5 Funktiot ja yhtälöt 2 (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA5.01 | suunnatun kulman ja radiaanin | 2 | G2 |
| MAA5.02 | yksikköympyrän; sinin, kosinin ja tangentin määritelmän sen avulla | 2 | G2, G7 |
| MAA5.03 | sini- ja kosinifunktion kuvaajineen, symmetria- ja jaksollisuusominaisuuksineen | 2 | G2 |
| MAA5.04 | sini- ja kosiniyhtälön ratkaisemisen (kaikki ratkaisut) | 2 | G4 |
| MAA5.05 | murtopotenssin ja sen yhteyden juureen | 2 | G2 |
| MAA5.06 | eksponenttifunktion ja eksponenttiyhtälön | 2 | G4, G5 |
| MAA5.07 | logaritmin ja logaritmin laskusäännöt; logaritmiyhtälön † | 2 | G4 |

#### MAA6 Derivaatta (3 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA6.01 | raja-arvon käsitteen (myös toispuoleiset raja-arvot) | 2 | G2, G3 |
| MAA6.02 | funktion jatkuvuuden | 2 | G2, G3 |
| MAA6.03 | derivaatan erotusosamäärän raja-arvona, tangentin kulmakertoimena ja hetkellisenä muutosnopeutena | 2 | G2, G7 |
| MAA6.04 | polynomifunktion derivoinnin ja derivointisäännöt | 2 | G2 |
| MAA6.05 | tulon ja osamäärän derivaatan; rationaalifunktion derivaatan | 2 | G2 |
| MAA6.06 | yhdistetyn funktion derivaatan | 2 | G2 |
| MAA6.07 | juuri-, trigonometristen, eksponentti- ja logaritmifunktioiden derivaatat † | 2 | G2 |
| MAA6.08 | kulkukaavion, monotonisuuden ja ääriarvojen määrittämisen | 2 | G3, G4 |
| MAA6.09 | suurimman ja pienimmän arvon suljetulla välillä ja ääriarvosovellukset | 2 | G4, G5 |

#### MAA7 Integraalilaskenta (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA7.01 | integraalifunktion ja integroimisvakion | 2 | G2 |
| MAA7.02 | alkeisfunktioiden integraalifunktiot | 2 | G2 |
| MAA7.03 | määrätyn integraalin ja analyysin peruslauseen | 2 | G3, G7 |
| MAA7.04 | pinta-alan laskemisen (käyrän ja x-akselin välissä, kahden käyrän välissä) | 2 | G4 |
| MAA7.05 | pyörähdyskappaleen tilavuuden † | 2 | G4 |
| MAA7.06 | integraalin sovellukset: muutosnopeudesta kokonaismuutokseen | 2 | G5, G7 |

#### MAA8 Tilastot ja todennäköisyys (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA8.01 | diskreetin tilastollisen jakauman esittämisen ja tunnusluvut (keskiarvo, moodi, mediaani, keskihajonta) | 2→3 | G5, G6 |
| MAA8.02 | korrelaation ja lineaarisen regression | 2→3 | G5, G8 |
| MAA8.03 | kombinatoriikan: tuloperiaate, permutaatiot, kombinaatiot | 2→3 | G4 |
| MAA8.04 | todennäköisyyden käsitteen: klassinen ja tilastollinen (geometrinen †) | 2→3 | G2 |
| MAA8.05 | todennäköisyyksien laskusäännöt: komplementti, yhteenlasku, kertolasku, riippumattomuus (ehdollinen †) | 2→3 | G3, G4 |
| MAA8.06 | diskreetin todennäköisyysjakauman ja odotusarvon | 2→3 | G5 |
| MAA8.07 | toistokokeen ja binomijakauman | 2→3 | G5 |

#### MAA9 Talousmatematiikka (1 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA9.01 | aritmeettisen ja geometrisen lukujonon | 2→3 | G2 |
| MAA9.02 | aritmeettisen ja geometrisen summan | 2→3 | G4 |
| MAA9.03 | korkolaskennan: yksinkertainen korko, koronkorko, talletukset ja säästäminen | 2→3 | G5, G8 |
| MAA9.04 | lainalaskennan (annuiteetti, tasalyhennys) | 2→3 | G5, G8 |
| MAA9.05 | verotuksen, indeksin ja valuuttojen laskut † | 2→3 | G8 |

#### MAA10 3D-geometria (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA10.01 | vektoriesityksen kolmiulotteisessa koordinaatistossa | 3 | G2 |
| MAA10.02 | piste- ja ristitulon | 3 | G2 |
| MAA10.03 | pisteen, suoran ja tason avaruudessa | 3 | G7 |
| MAA10.04 | kulmat avaruudessa | 3 | G4 |
| MAA10.05 | yhden muuttujan differentiaali- ja integraalilaskennan sovelluksia avaruusgeometriassa | 3 | G7 |
| MAA10.06 | kahden muuttujan funktion ja pinnan avaruudessa | 3 | G7 |

#### MAA11 Algoritmit ja lukuteoria (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA11.01 | algoritmisen ajattelun perusteet: peräkkäisyys, valinta, toisto, vuokaavio; yksinkertaisten algoritmien ohjelmoinnin | 3 | G6 |
| MAA11.02 | konnektiivit ja totuusarvot | 3 | G3 |
| MAA11.03 | kokonaislukujen jaollisuuden ja jakoyhtälön | 3 | G3 |
| MAA11.04 | kongruenssin | 3 | G3 |
| MAA11.05 | Eukleideen algoritmin ja aritmetiikan peruslauseen | 3 | G3, G6 |

#### MAA12 Analyysi ja jatkuva jakauma (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAA12.01 | paloittain määritellyn funktion | 3 | G2 |
| MAA12.02 | funktion jatkuvuuden ja derivoituvuuden tutkimisen | 3 | G3 |
| MAA12.03 | jatkuvien ja derivoituvien funktioiden yleisiä ominaisuuksia | 3 | G3 |
| MAA12.04 | käänteisfunktion | 3 | G2, G7 |
| MAA12.05 | integraalilaskennan täydentävät taidot † | 3 | G2 |
| MAA12.06 | jatkuvan todennäköisyysjakauman ja tiheysfunktion; normaalijakauman † | 3 | G5 |

### 3.3 Lyhyt oppimäärä (MAB)

#### MAB2 Lausekkeet ja yhtälöt (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB2.01 | muotoilla ongelman yhtälöksi sekä tulkita ja arvioida ratkaisun | 1 | G4, G5 |
| MAB2.02 | ratkaista yhtälön käsin ja ohjelmistolla | 1 | G4, G6 |
| MAB2.03 | toisen asteen polynomifunktion ja sen kuvaajan | 1 | G2 |
| MAB2.04 | toisen asteen yhtälön ratkaisemisen | 1 | G4 |
| MAB2.05 | aritmeettisen lukujonon ja summan | 1 | G5 |
| MAB2.06 | geometrisen lukujonon ja summan | 1 | G5 |
| MAB2.07 | lausekkeiden sieventämisen ja kaavan ratkaisemisen halutun suureen suhteen † | 1 | G2 |

#### MAB3 Geometria (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB3.01 | kuvioiden yhdenmuotoisuuden ja mittakaavan | 1 | G5 |
| MAB3.02 | suorakulmaisen kolmion trigonometrian | 1 | G4 |
| MAB3.03 | Pythagoraan lauseen ja sen käänteislauseen | 1 | G3 |
| MAB3.04 | kuvioiden ja kappaleiden pinta-alat ja tilavuudet | 1 | G5 |
| MAB3.05 | geometrian menetelmät tasokoordinaatistossa † | 1 | G7 |

#### MAB4 Matemaattisia malleja (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB4.01 | lineaarisen mallin muodostamisen ja soveltamisen; kulmakerroin muutosnopeutena | 1→2 | G5 |
| MAB4.02 | eksponentiaalisen mallin muodostamisen ja soveltamisen | 1→2 | G5 |
| MAB4.03 | eksponenttiyhtälön ratkaisemisen (ohjelmistolla tai logaritmilla †) | 1→2 | G4, G6 |
| MAB4.04 | ennusteiden tekemisen ja mallin hyvyyden ja rajoitusten arvioinnin | 1→2 | G4, G5 |

#### MAB5 Tilastot ja todennäköisyys (2 op, pakollinen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB5.01 | tilastoaineiston esittämisen taulukoin ja diagrammein | 2 | G5, G6 |
| MAB5.02 | tunnusluvut (keskiarvo, mediaani, moodi, keskihajonta; kvartiilit †) | 2 | G5 |
| MAB5.03 | regression ja korrelaation käsitteet | 2 | G5, G8 |
| MAB5.04 | havaintojen ja poikkeavien havaintojen tulkinnan | 2 | G4 |
| MAB5.05 | ennusteiden tekemisen aineiston perusteella | 2 | G5 |
| MAB5.06 | todennäköisyyden käsitteen ja laskusäännöt | 2 | G2, G4 |
| MAB5.07 | kombinatoriikan perusteet † | 2 | G4 |

#### MAB6 Talousmatematiikka I (1 op, pakollinen; nimi lähteissä myös "Talousmatematiikan alkeet" †)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB6.01 | suhteellisen osuuden, vertailun ja muutoksen laskemisen | 2 | G5, G8 |
| MAB6.02 | indeksin | 2 | G8 |
| MAB6.03 | korkokäsitteen ja yksinkertaisen koron | 2 | G8 |
| MAB6.04 | verotuksen laskut | 2 | G8 |
| MAB6.05 | valuuttamuunnokset | 2 | G8 |

#### MAB7 Talousmatematiikka II (1 op, pakollinen †)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB7.01 | koronkoron ja säästämisen | 2→3 | G5, G8 |
| MAB7.02 | lainalaskennan | 2→3 | G5, G8 |
| MAB7.03 | talouden suunnittelun, resurssien riittävyyden ja kannattavuuden laskut | 2→3 | G5, G8 |

#### MAB8 Matemaattinen analyysi (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB8.01 | funktion muutosnopeuden | 3 | G2, G5 |
| MAB8.02 | polynomifunktion derivaatan | 3 | G2 |
| MAB8.03 | derivaatan merkin ja funktion kulun yhteyden | 3 | G3 |
| MAB8.04 | polynomifunktion suurimman ja pienimmän arvon | 3 | G4, G5 |

#### MAB9 Tilastolliset ja todennäköisyysjakaumat (2 op, valtakunnallinen valinnainen)

| ID | Opiskelija osaa… | Vk | G |
|---|---|---|---|
| MAB9.01 | normaalijakauman mallina | 3 | G5 |
| MAB9.02 | normituksen (odotusarvo ja keskihajonta) | 3 | G2 |
| MAB9.03 | toistokokeen ja binomijakauman | 3 | G5 |
| MAB9.04 | luottamusvälin | 3 | G3, G8 |
| MAB9.05 | tilastollisen tutkimuksen tekemisen ohjelmistolla | 3 | G6 |

## 4. Arviointi ja tehtävien tasot

**Arviointi lukiossa.** Moduulit ja opintojaksot arvioidaan numeroin 4–10. Oppimäärän arvosana on opintojaksojen arvosanojen opintopisteillä painotettu keskiarvo. Kansallisia arvosanakriteerejä (vrt. perusopetuksen 5/7/8/9) matematiikalle ei hauissa löytynyt. † Käytännön vaatimustason määrää ylioppilastutkinto.

**Ylioppilastutkinto.** Lyhyt ja pitkä matematiikka ovat eri kokeita. Kokeessa on A-osa ilman laskinohjelmistoja ja B-osa, jossa ohjelmistot ovat käytössä. YTL julkaisee jokaisesta kokeesta "hyvän vastauksen piirteet", joissa kuvataan pisteytys ja yleisimmät virheet. Ne ovat ainoa löydetty suomalainen, tehtävätasoinen lähde lukion vaikeista kohdista.

**Tasot** (sama merkintä kuin 7–9-tiedostossa, esim. `MAA6.06 / H`):

| Taso | Vastaa (ehdotus) | Tehtävätyyppi |
|---|---|---|
| P (perus) | moduuliarvosana 5–6 | yksi askel, tuttu malli, kaava annettu |
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
- Laskutehtävien lisäksi jokaisessa moduulissa vähintään yksi tehtävä, jossa perustellaan (G3) tai arvioidaan tuloksen mielekkyyttä (G4).
- Desimaalierotin pilkku, miinusmerkki U+2212, suomenkieliset termit (derivaatta, integraalifunktio, kulkukaavio, kulmakerroin, radiaani, odotusarvo, keskihajonta, luottamusväli).
- Lyhyen oppimäärän tehtävissä painottuvat sovellukset ja mallit, pitkän oppimäärän tehtävissä perustelu ja symbolinen käsittely.
- Virhekäsitykset ja niiden tunnisteet: `../misconceptions/lukio_misconceptions.md`.

**Yleisiä virhekäsityksiä lukiossa (vääriksi vastausvaihtoehdoiksi ja "Varo virhekäsitystä" -laatikoihin).** Täysi luettelo lähteineen on virhekäsitystiedostossa.

| ID | Virhekäsitys |
|---|---|
| MAY1.04, MAA5.05 | 2⁻¹ = −2; a^(1/3) = a/3; (a + b)² = a² + b² jatkuu lukioon |
| MAA2.04–MAA2.05 | x² = 3x jaetaan x:llä, ratkaisu x = 0 katoaa; (x − 2)(x − 3) = 6 ⇒ x = 8 tai x = 9 |
| MAA2.06, MAA4.06 | epäyhtälö kerrotaan lausekkeella, jonka merkkiä ei tiedetä; x² < 4 ⇒ x < ±2 |
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
| lukio-pitka/integraali-riemannin-summa.html | MAA7.03, MAA7.04 |
| lukio-pitka/derivative_visualizer.html, integral-speed-distance.html, Vector_addition.html | MAA6.03, MAA7.06, MAA4.07 (vanhoja, eivät noudata APPLET_SPEC.md:tä) |
| lukio-pitka/complex-plane-explorer.html | ei valtakunnallista tunnistetta |
| lukio-lyhyt/makeishinnoittelu.html, pokerikasien-todennakoisyydet.html | MAB4.01, MAB5.06, MAA8.03 † |

Suurimmat aukot (ehdokkaita BACKLOG.md:hen, applettiputken päätös): MAA4.07 vektorien yhteenlasku ja pituus, MAA6.08 kulkukaavio ja ääriarvot, MAA8.02 / MAB5.03 korrelaatio vs. syy-yhteys, MAB4.02 / MAA9.03 lineaarinen vs. eksponentiaalinen kasvu, MAB9.01–MAB9.04 normaalijakauma ja luottamusväli.

## Lähteet

- Opetushallitus: Lukion opetussuunnitelman perusteet 2019 (OPH-2263-2019), luku 6.6 Matematiikka. ePerusteet: https://eperusteet.opintopolku.fi/#/2270454/lukiokoulutus/6828810/oppiaine/6831746 (ei luettavissa tästä ympäristöstä)
- OPH: Lyhyen matematiikan tukimateriaalia LOPS 2019:n toteuttamiseen, https://www.oph.fi/sites/default/files/documents/lops2019_mab.pdf
- MAOL: Pitkän matematiikan tukimateriaalia LOPS 2019:n toteuttamiseen, https://maol.fi/app/uploads/2020/01/LOPS2019_MAA_MAOL.pdf
- Koulujen LOPS2021-sivut, joilla perusteiden sisällöt toistuvat: Laukaan lukio (peda.net/laukaa/lukio), Tampereen teknillinen lukio (tampere.fi), TNK (sites.utu.fi/lops2021tnk), Tuusniemi, Sievi, Sotungin lukio
- YTL: hyvän vastauksen piirteet, esim. https://tiedostot.ylioppilastutkinto.fi/kokeet/2026-03-18_M_fi/grading-instructions.html
