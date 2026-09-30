# Matematiikka, vuosiluokat 1–6: oppimistavoitteet tehtävien ja applettien laatimiseen

Tämä tiedosto on vuosiluokkien 1–6 vastine tiedostolle `OPS_7-9_oppimistavoitteet.md`. Se on tarkoitettu ohjaamaan uusien kyselyjen (quiz) ja applettien laatimista. Jokaisella oppimistavoitteella on pysyvä tunniste (esim. `A36.S2.11`), johon kysymykset, appletit, virhekäsitykset ja BACKLOG.md-merkinnät voivat viitata.

Versio: 2026-09-30

> **Expert review required before use with pupils.** Quizzes and applets built from this file must not collect data about pupils in grades 1–6 until the sign-off in `docs/privacy/expert_review_signoff_template.md` is complete. See `EXPERT_REVIEW_REQUIRED.md`.

## 0. Lähteet ja luotettavuus

| Osa | Lähde | Luotettavuus |
|---|---|---|
| Oppiaineen tehtävä, tavoitteet T1–T12 (lk 1–2) ja T1–T14 (lk 3–6), sisältöalueiden kuvaukset, oppimisympäristö-, tuki- ja arviointitekstit | POPS 2014, luvut 13.4.4 ja 14.4.4, sellaisena kuin ne on toistettu Keski-Suomen kuntien opetussuunnitelmapohjassa (peda.net, kohta "Perusopetuksen opetussuunnitelman perusteet"), luettu 30.9.2026 | Kansallinen teksti toisen käden kopiona. Tarkista sanamuoto OPH:n PDF:stä (`perusopetuksen_opetussuunnitelman_perusteet_2014.pdf`, matematiikka 3–6 sivuilla 234–238) ennen virallista käyttöä. |
| 6. luokan arviointikriteerit (arvosanat 5/7/8/9), luku 4 | OPH, *Matematiikka, kriteerit (6. lk)*, voimassa 1.8.2023 alkaen | PDF luettu kokonaan. Tässä **tiivistetty**, ei sanatarkka. PDF-tekstin sarakejako on paikoin epäselvä, epävarmat kohdat merkitty †. |
| Atomiset oppimistavoitteet (luku 3) | Pilkottu S1–S5-kuvauksista | Jokainen rivi palautuu OPS-tekstiin |
| Vuosiluokkajako 1–2 | Paikallinen: TNK POPS -sivuston (sites.utu.fi/popstnk) 1. ja 2. lk:n matematiikkasuunnitelmat | Koulukohtainen suunnitelma, ei kunnan. Valittu, koska sama sivusto on lähteenä 7–9-tiedostossa. |
| Vuosiluokkajako 3–6 | Paikallinen: Luumäen perusopetuksen opetussuunnitelma 2016, matematiikka 3.–6. lk (peda.net) | Kunnan OPS, kaikki neljä luokkaa luettu. Muuttunut mahdollisesti 2016 jälkeen. |
| Paikallisten jakojen vertailu (luku 5) | TNK 3.–5. lk, hakutulosotteet | Otteet, ei koko sivuja. Vain suuntaa antava. |

Päättöarviointia ei ole vuosiluokilla 1–6. Kansalliset arvosanakriteerit on annettu vain 6. luokan lukuvuosiarviointia varten. Vuosiluokille 1–2 en löytänyt kansallisia arvosanakriteereitä, vain arvioinnin kuvauksen.

## 1. Havainnot lähteistä

1. **Tavoitenumerot eivät ole yhteismitallisia.** T5 tarkoittaa eri asiaa luokilla 1–2 (käsitteet ja merkinnät), 3–6 (ongelmanratkaisu) ja 7–9 (looginen ja luova ajattelu). Tässä tiedostossa käytetään etuliitteitä: `A12.` (lk 1–2) ja `A36.` (lk 3–6). 7–9-tiedoston tunnisteet (`S3.05`) pysyvät ennallaan.
2. **Valtakunnallinen OPS ei jaa sisältöjä vuosiluokille** lk 1–2 eikä 3–6 sisällä. Jaon tekee paikallinen OPS. Luvun 5 jako on siksi ehdotus.
3. **Sisältöalueet vaihtelevat.** Lk 1–2: S1 ajattelun taidot, S2 luvut ja laskutoimitukset, S3 geometria ja mittaaminen, S4 tietojenkäsittely ja tilastot. Lk 3–6: S1 ajattelun taidot, S2 luvut ja laskutoimitukset, S3 algebra, S4 geometria ja mittaaminen, S5 tietojenkäsittely, tilastot ja todennäköisyys. Sama S-numero (S3, S4) tarkoittaa eri sisältöä lk 1–2 ja 3–6.
4. **Lk 3–6:n algebralla (S3) ei ole omaa sisältötavoitetta.** S3 liittyy vain yleisiin tavoitteisiin T1–T7. T8–T10 kuuluvat S2:lle, T11–T12 S4:lle, T13 S5:lle ja T14 S1:lle.
5. **Lk 3–6:n tavoitteet ovat T1–T14, lk 1–2:n T1–T12.** Molemmissa T1 (innostus ja minäkuva) ei vaikuta arvosanaan lk 3–6:lla.
6. **Ohjelmointi** alkaa vaiheittaisista toimintaohjeista (lk 1–2, T12) ja jatkuu graafiseen ohjelmointiympäristöön (lk 3–6, T14).
7. **Laskujärjestys, negatiiviset luvut ja murtoluvut** sijoittuvat luokkatasoille paikallisesti. Kansallinen teksti mainitsee negatiivisen luvun "pohjustamisen" ja laajentamisen negatiivisiin kokonaislukuihin, mutta ei luokkaa.

## 2. Tavoitteet

### 2.1 Vuosiluokat 1–2 (T1–T12)

Tavoitealueet: **A** = merkitys, arvot ja asenteet; **B** = työskentelyn taidot; **C** = käsitteelliset ja tiedonalakohtaiset tavoitteet.

| ID | Tavoite (opetuksen tavoite) | Alue | Sisältöalueet |
|---|---|---|---|
| A12.T1 | tukea oppilaan innostusta ja kiinnostusta matematiikkaa kohtaan sekä myönteisen minäkuvan ja itseluottamuksen kehittymistä | A | S1–S4 |
| A12.T2 | ohjata oppilasta kehittämään taitoaan tehdä havaintoja matematiikan näkökulmasta sekä tulkita ja hyödyntää niitä eri tilanteissa | B | S1–S4 |
| A12.T3 | kannustaa oppilasta esittämään ratkaisujaan ja päätelmiään konkreettisin välinein, piirroksin, suullisesti ja kirjallisesti myös tvt:tä hyödyntäen | B | S1–S4 |
| A12.T4 | ohjata oppilasta kehittämään päättely- ja ongelmanratkaisutaitojaan | B | S1–S4 |
| A12.T5 | ohjata oppilasta ymmärtämään matemaattisia käsitteitä ja merkintätapoja | C | S1–S4 |
| A12.T6 | tukea oppilasta lukukäsitteen kehittymisessä ja kymmenjärjestelmän periaatteen ymmärtämisessä | C | S2 |
| A12.T7 | perehdyttää oppilasta peruslaskutoimitusten periaatteisiin ja tutustuttaa niiden ominaisuuksiin | C | S2 |
| A12.T8 | ohjata oppilasta kehittämään sujuvaa peruslaskutaitoa luonnollisilla luvuilla ja käyttämään erilaisia päässälaskustrategioita | C | S2 |
| A12.T9 | tutustuttaa oppilas geometrisiin muotoihin ja ohjata havainnoimaan niiden ominaisuuksia | C | S3 |
| A12.T10 | ohjata oppilasta ymmärtämään mittaamisen periaate | C | S3 |
| A12.T11 | tutustuttaa oppilas taulukoihin ja diagrammeihin | C | S4 |
| A12.T12 | harjaannuttaa oppilasta laatimaan vaiheittaisia toimintaohjeita ja toimimaan ohjeen mukaan | C | S1 |

### 2.2 Vuosiluokat 3–6 (T1–T14)

| ID | Tavoite (opetuksen tavoite) | Alue | Sisältöalueet | Arvioinnin kohde |
|---|---|---|---|---|
| A36.T1 | pitää yllä oppilaan innostusta ja kiinnostusta matematiikkaa kohtaan sekä tukea myönteistä minäkuvaa ja itseluottamusta | A | S1–S5 | Ei vaikuta arvosanaan; itsearviointi |
| A36.T2 | ohjata oppilasta havaitsemaan yhteyksiä oppimiensa asioiden välillä | B | S1–S5 | Opittujen asioiden yhteydet |
| A36.T3 | ohjata oppilasta kehittämään taitoaan esittää kysymyksiä ja tehdä perusteltuja päätelmiä havaintojensa pohjalta | B | S1–S5 | Kysymysten esittäminen ja päättelytaidot |
| A36.T4 | kannustaa oppilasta esittämään päättelyään ja ratkaisujaan muille konkreettisin välinein, piirroksin, suullisesti ja kirjallisesti myös tvt:tä hyödyntäen | B | S1–S5 | Ratkaisujen ja päätelmien esittäminen |
| A36.T5 | ohjata ja tukea oppilasta ongelmanratkaisutaitojen kehittämisessä | B | S1–S5 | Ongelmanratkaisutaidot |
| A36.T6 | ohjata oppilasta kehittämään taitoaan arvioida ratkaisun järkevyyttä ja tuloksen mielekkyyttä | B | S1–S5 | Taito arvioida ratkaisua |
| A36.T7 | ohjata oppilasta käyttämään ja ymmärtämään matemaattisia käsitteitä ja merkintöjä | C | S1–S5 | Käsitteiden ymmärtäminen ja käyttö |
| A36.T8 | tukea ja ohjata oppilasta vahvistamaan ja laajentamaan ymmärrystään kymmenjärjestelmästä | C | S2 | Kymmenjärjestelmän ymmärtäminen |
| A36.T9 | tukea oppilasta lukukäsitteen kehittymisessä positiivisiin rationaalilukuihin ja negatiivisiin kokonaislukuihin | C | S2 | Lukukäsite |
| A36.T10 | opastaa oppilasta saavuttamaan sujuva laskutaito päässä ja kirjallisesti hyödyntäen laskutoimitusten ominaisuuksia | C | S2 | Laskutaidot ja laskutoimitusten ominaisuuksien hyödyntäminen |
| A36.T11 | ohjata oppilasta havainnoimaan ja kuvailemaan kappaleiden ja kuvioiden geometrisia ominaisuuksia sekä tutustuttaa geometrisiin käsitteisiin | C | S4 | Geometrian käsitteet ja ominaisuuksien havainnointi |
| A36.T12 | ohjata oppilasta arvioimaan mittauskohteen suuruutta ja valitsemaan mittaamiseen sopivan välineen ja mittayksikön sekä pohtimaan mittaustuloksen järkevyyttä | C | S4 | Mittaaminen |
| A36.T13 | ohjata oppilasta laatimaan ja tulkitsemaan taulukoita ja diagrammeja sekä käyttämään tilastollisia tunnuslukuja sekä tarjota kokemuksia todennäköisyydestä | C | S5 | Taulukoiden ja diagrammien laatiminen ja tulkinta |
| A36.T14 | innostaa oppilasta laatimaan toimintaohjeita tietokoneohjelmina graafisessa ohjelmointiympäristössä | C | S1 | Ohjelmointi graafisessa ohjelmointiympäristössä |

## 3. Atomiset oppimistavoitteet sisältöalueittain

Sarakkeet: **ID** (käytä viitteenä), **Oppilas osaa…**, **T** = liittyvät tavoitteet (saman lohkon T-numerot).

### 3.1 Vuosiluokat 1–2

#### S1 Ajattelun taidot

| ID | Oppilas osaa… | T |
|---|---|---|
| A12.S1.01 | löytää yhtäläisyyksiä, eroja ja säännönmukaisuuksia | T2, T4 |
| A12.S1.02 | vertailla, luokitella ja asettaa järjestykseen | T4 |
| A12.S1.03 | havaita syy- ja seuraussuhteita | T2, T4 |
| A12.S1.04 | tarkastella matemaattisia tilanteita eri näkökulmista | T4 |
| A12.S1.05 | laatia vaiheittaisia toimintaohjeita ja testata niitä; toimia ohjeen mukaan (ohjelmoinnin alkeet) | T12 |

#### S2 Luvut ja laskutoimitukset

| ID | Oppilas osaa… | T |
|---|---|---|
| A12.S2.01 | yhdistää lukumäärän, lukusanan ja numeromerkinnän | T6 |
| A12.S2.02 | laskea, hahmottaa ja arvioida lukumääriä | T6 |
| A12.S2.03 | lukujonotaidot; vertailla ja asettaa lukuja järjestykseen | T6 |
| A12.S2.04 | tutkia lukujen ominaisuuksia: parillisuus, monikerrat, puolittaminen | T6, T7 |
| A12.S2.05 | lukujen 1–10 hajotelmat | T6, T8 |
| A12.S2.06 | kymmenjärjestelmän periaate konkreettisten mallien avulla | T6 |
| A12.S2.07 | käyttää lukuja lukumäärän, järjestyksen ja mittaustuloksen ilmaisemiseen sekä laskutoimituksissa | T5, T6 |
| A12.S2.08 | laskea yhteen- ja vähennyslaskuja lukualueella 0–20 | T7, T8 |
| A12.S2.09 | laskea yhteen- ja vähennyslaskuja lukualueella 0–100 | T7, T8 |
| A12.S2.10 | käyttää erilaisia päässälaskustrategioita; soveltaa laskuja sovellustilanteissa | T8 |
| A12.S2.11 | hyödyntää vaihdannaisuutta ja liitännäisyyttä yhteenlaskussa | T7 |
| A12.S2.12 | ymmärtää kertolaskun käsitteen konkretian avulla; kertotaulut 1–5 ja 10 | T7, T8 |
| A12.S2.13 | hyödyntää vaihdannaisuutta kertolaskussa; tutustua kertolaskun liitännäisyyteen | T7 |
| A12.S2.14 | jakolaskun ja kerto- ja jakolaskun yhteyden pohjustus | T7 |
| A12.S2.15 | murtoluvun käsitteen pohjustus jakamalla kokonainen yhtä suuriin osiin | T5, T6 |

#### S3 Geometria ja mittaaminen

| ID | Oppilas osaa… | T |
|---|---|---|
| A12.S3.01 | hahmottaa kolmiulotteista ympäristöä ja havaita siinä tasogeometriaa; käyttää suunta- ja sijaintikäsitteitä | T9 |
| A12.S3.02 | tutkia, rakentaa ja piirtää kappaleita ja tasokuvioita | T9 |
| A12.S3.03 | nimetä kappaleiden ja kuvioiden ominaisuuksia ja luokitella niitä | T9 |
| A12.S3.04 | ymmärtää mittaamisen periaate | T10 |
| A12.S3.05 | käyttää suureita pituus, massa, tilavuus ja aika sekä mittayksiköitä m, cm, kg, g, l ja dl | T10 |
| A12.S3.06 | lukea kellonaikoja ja käyttää ajanyksiköitä | T10 |

#### S4 Tietojenkäsittely ja tilastot

| ID | Oppilas osaa… | T |
|---|---|---|
| A12.S4.01 | kerätä ja tallentaa tietoja kiinnostavista aihepiireistä (pohjustus) | T11 |
| A12.S4.02 | laatia ja tulkita yksinkertaisia taulukoita ja pylväsdiagrammeja | T11 |

### 3.2 Vuosiluokat 3–6

#### S1 Ajattelun taidot

| ID | Oppilas osaa… | T |
|---|---|---|
| A36.S1.01 | löytää yhtäläisyyksiä, eroja ja säännönmukaisuuksia | T2, T3 |
| A36.S1.02 | vertailla, luokitella ja asettaa järjestykseen | T3, T5 |
| A36.S1.03 | etsiä vaihtoehtoja systemaattisesti | T5 |
| A36.S1.04 | havaita syy- ja seuraussuhteita sekä yhteyksiä matematiikassa | T2, T3 |
| A36.S1.05 | suunnitella ja toteuttaa ohjelmia graafisessa ohjelmointiympäristössä | T14 |

#### S2 Luvut ja laskutoimitukset

| ID | Oppilas osaa… | T |
|---|---|---|
| A36.S2.01 | ymmärtää kymmenjärjestelmän (syventäminen ja varmentaminen) | T8 |
| A36.S2.02 | tutkia ja luokitella lukuja: rakenne, yhteydet, jaollisuus | T8, T10 |
| A36.S2.03 | laskea peruslaskutoimituksia päässä | T10 |
| A36.S2.04 | käyttää yhteen- ja vähennyslaskualgoritmeja | T10 |
| A36.S2.05 | ymmärtää kertolaskun käsitteen; kertotaulut 6–9; kertotaulut 1–10 varmasti | T10 |
| A36.S2.06 | käyttää kertolaskualgoritmia | T10 |
| A36.S2.07 | jakolasku sisältö- ja ositusjakotilanteissa; lukuyksiköittäin jakaminen | T10 |
| A36.S2.08 | hyödyntää laskutoimitusten ominaisuuksia ja niiden välisiä yhteyksiä | T10 |
| A36.S2.09 | pyöristää lukuja ja laskea likiarvoilla; arvioida tuloksen suuruusluokka | T6, T10 |
| A36.S2.10 | ymmärtää negatiivisen luvun käsitteen; kokonaislukujen lukualue | T9 |
| A36.S2.11 | ymmärtää murtoluvun käsitteen | T9 |
| A36.S2.12 | laskea murtolukujen peruslaskutoimituksia (kerto- ja jakolaskussa luonnollinen luku kertojana tai jakajana) | T9, T10 |
| A36.S2.13 | ymmärtää desimaaliluvut osana kymmenjärjestelmää | T8, T9 |
| A36.S2.14 | laskea peruslaskutoimituksia desimaaliluvuilla | T9, T10 |
| A36.S2.15 | ymmärtää prosentin käsitteen; laskea prosenttiluku ja prosenttiarvo yksinkertaisissa tapauksissa | T9 |
| A36.S2.16 | hyödyntää murtoluvun, desimaaliluvun ja prosentin välisiä yhteyksiä | T9 |

#### S3 Algebra

| ID | Oppilas osaa… | T |
|---|---|---|
| A36.S3.01 | tutkia lukujonon säännönmukaisuutta ja jatkaa lukujonoa säännön mukaan | T2, T5 |
| A36.S3.02 | ymmärtää tuntemattoman käsitteen | T7 |
| A36.S3.03 | tutkia yhtälöä ja löytää sen ratkaisuja päättelemällä ja kokeilemalla | T5, T7 |

#### S4 Geometria ja mittaaminen

| ID | Oppilas osaa… | T |
|---|---|---|
| A36.S4.01 | rakentaa, piirtää, tutkia ja luokitella kappaleita ja kuvioita | T11 |
| A36.S4.02 | luokitella kappaleet lieriöihin, kartioihin ja muihin; tuntea särmiön, ympyrälieriön, ympyräpohjaisen kartion ja pyramidin | T11 |
| A36.S4.03 | luokitella tasokuviot monikulmioihin ja muihin kuvioihin; tuntea kolmioiden, nelikulmioiden ja ympyrän ominaisuudet | T11 |
| A36.S4.04 | käyttää pisteen, janan, suoran ja kulman käsitteitä; piirtää, mitata ja luokitella kulmia | T11 |
| A36.S4.05 | tarkastella suoran suhteen peilaussymmetriaa; havaita kierto- ja siirtosymmetrioita ympäristössä | T11 |
| A36.S4.06 | käyttää koordinaatistoa: ensin ensimmäinen neljännes, sitten kaikki | T11 |
| A36.S4.07 | käyttää mittakaavaa suurennoksissa ja pienennöksissä sekä kartalla | T11, T12 |
| A36.S4.08 | mitata; huomioida mittaustarkkuus; arvioida ja tarkistaa mittaustulos | T12, T6 |
| A36.S4.09 | mitata ja laskea erimuotoisten kuvioiden piirejä ja pinta-aloja | T12 |
| A36.S4.10 | laskea suorakulmaisen särmiön tilavuus | T12 |
| A36.S4.11 | ymmärtää mittayksikköjärjestelmän rakenne; muuntaa yleisimpiä yksiköitä | T12 |

#### S5 Tietojenkäsittely, tilastot ja todennäköisyys

| ID | Oppilas osaa… | T |
|---|---|---|
| A36.S5.01 | kerätä tietoa järjestelmällisesti kiinnostavista aihepiireistä | T13 |
| A36.S5.02 | tallentaa ja esittää tietoa taulukoin ja diagrammein | T13 |
| A36.S5.03 | määrittää suurimman ja pienimmän arvon, keskiarvon ja tyyppiarvon | T13 |
| A36.S5.04 | päätellä arkitilanteessa, onko tapahtuma mahdoton, mahdollinen vai varma | T13 |

## 4. Arviointikriteerit 6. luokan päätteeksi tiivistettyinä (arvosanat 5 / 7 / 8 / 9)

Tiivistelmä OPH:n 6. luokan kriteereistä (lk 3–6). Ylemmän arvosanan kuvaus sisältää alemmat. † = PDF-tekstin sarakejako epäselvä, tason sijoitus tulkittu. Käytä tehtävien vaikeustasojen mitoittamiseen (ks. luku 6). T1 ei vaikuta arvosanaan.

| T | 5 | 7 | 8 | 9 |
|---|---|---|---|---|
| T2 | havaitsee ohjattuna yhteyksiä | havaitsee yhteyksiä ja antaa ohjattuna esimerkkejä | tunnistaa yhteyksiä ja antaa esimerkkejä | kuvailee ja selittää, mistä yhteydet johtuvat |
| T3 | havaitsee, mihin tarvitsee apua; tekee ohjattuna havaintoja ja kokoaa tietoa | harjoittelee kysymysten esittämistä; perustelee ohjattuna päätelmiään | esittää aiheeseen liittyviä kysymyksiä; perustelee päätelmiään | esittää aihetta tukevia kysymyksiä; selkeät perustelut |
| T4 | kertoo päättelystään ja esittää ratkaisuja ohjattuna | esittää jollakin ilmaisukeinolla | tarvittaessa myös toisella ilmaisukeinolla | tilanteeseen sopivalla ilmaisukeinolla |
| T5 | käyttää ohjattuna jotakin ratkaisutapaa | kokeilee oikeaan tulokseen johtavaa tapaa | valitsee ja käyttää toimivaa ratkaisutapaa | arvioi ratkaisutavan toimivuutta ja tehokkuutta |
| T6 | hahmottaa ohjattuna tuloksen järkevyyttä | pohtii mielekkyyttä; arvioi ohjattuna ratkaisuaan | tarkastelee ratkaisua ja mielekkyyttä kriittisesti | arvioi ja perustelee ratkaisun ja tuloksen |
| T7 | tunnistaa ohjattuna käsitteitä; harjoittelee merkintöjä | tuntee käsitteitä; pääsääntöisesti oikeat merkinnät | käyttää käsitteitä ja oikeita merkintöjä | ymmärtää ja käyttää oikeita käsitteitä ja merkintöjä |
| T8 | erottaa kokonaislukujen suuruusluokkia; tunnistaa ohjattuna desimaaliluvun lukuyksiköt | nimeää desimaaliluvun lukuyksiköt; käyttää kymmenjärjestelmää luonnollisten lukujen laskuissa | hyödyntää kymmenjärjestelmää paikkajärjestelmänä laskuissa | ymmärtää kymmenjärjestelmän olevan yksi paikkajärjestelmistä |
| T9 | asettaa negatiiviset luvut järjestykseen; vertailee ohjattuna murtolukuja | asettaa murtolukuja järjestykseen; antaa esimerkkejä negatiivisista luvuista | käyttää positiivisia rationaalilukuja ja negatiivisia kokonaislukuja laskutoimituksissa | käyttää niitä osana ongelmanratkaisua |
| T10 | peruslaskutoimitukset kahdella luonnollisella luvulla | useamman laskutoimituksen laskut luonnollisilla luvuilla; hajottaa ohjattuna luvut helpompaan muotoon | laskee sujuvasti useita laskulausekkeita sisältäviä laskuja; hajottaa luvut | käyttää monipuolisesti erilaisia laskutapoja |
| T11 | tunnistaa ja nimeää yleisimmät kuviot, kappaleet ja niiden osat; piirtää yleisimmät kuviot | havainnoi pisteen, janan, suoran ja kulman yhteyksiä; tunnistaa suoran suhteen symmetrisiä kuvioita; suurentaa ohjattuna kuviota | kuvailee ominaisuuksia; piirtää pisteen tai suoran suhteen symmetrisiä kuvioita koordinaatistossa; käyttää annettua mittakaavaa; merkitsee pisteen koordinaatistoon † | hyödyntää ominaisuuksia ongelmanratkaisussa; piirtää suurennoksia ja pienennöksiä ja määrittää mittakaavan |
| T12 | mittaa annetulla välineellä; muuttaa ohjattuna pituusyksikön toiseksi | mittaa valitsemallaan välineellä ja ilmoittaa pyydetyssä yksikössä; muuttaa vetomittojen yksiköitä | arvioi mittauskohteen suuruutta ja valitsee välineen; hallitsee yleisimmät yksikkömuunnokset; pohtii tuloksen järkevyyttä | selittää tarkkuuteen vaikuttavia tekijöitä ja valitsee oikean yksikön; muuttaa pinta-alojen yksiköitä |
| T13 | taulukoi havainnot ja lukee pylväsdiagrammia; poimii yleisimmän havainnon; laskee ohjattuna keskiarvon; tunnistaa varman tapahtuman † | tulkitsee erilaisia diagrammeja; määrittää tyyppiarvon ja laskee keskiarvon; laskee kysyttyjen ja kaikkien vaihtoehtojen lukumäärän † | laatii käyttökelpoisen kuvauksen taululla tai diagrammilla; päättelee todennäköisimmän vaihtoehdon † | hyödyntää taulukoita, diagrammeja, tyyppiarvoa ja keskiarvoa; määrittää vastatapahtuman † |
| T14 | testaa valmista ohjelmaa ja tunnistaa komentojen vaikutukset | lisää valmiiseen ohjelmaan ehto- tai toistorakenteen; etsii ja korjaa virheen | ohjelmoi toimivan ohjelman ehto- ja toistorakentein | hyödyntää ohjelmointia ongelmanratkaisussa; arvioi ja muokkaa ohjelmaa |

Vuosiluokille 1–2 ei ole valtakunnallisia arvosanakriteereitä. Arvioinnin kohteina OPS mainitsee edistymisen lukukäsitteen ymmärtämisessä ja lukujonotaidoissa, kymmenjärjestelmän ymmärtämisessä, laskutaidon sujuvuudessa, kappaleiden ja kuvioiden luokittelussa sekä matematiikan käyttämisessä ongelmanratkaisussa.

## 5. Vuosiluokittainen näkymä (ehdotus)

Työjako. Lk 1–2: TNK POPS. Lk 3–6: Luumäen OPS 2016. Jako on paikallinen ja tyypillinen, ei valtakunnallinen. Päivitä, jos käytät toista OPS:ää.

**1. luokka: lukualue 0–20**
- Ajattelu: A12.S1.02, S1.03, S1.05 (luokittelu, vertailu, ohjelmoinnin alkeet)
- Luvut: A12.S2.01, S2.02, S2.03, S2.05 (hajotelmat 0–10), S2.06 (tutustuminen), S2.08 (myös kymmenylitys), S2.10, S2.11
- Geometria ja mittaaminen: A12.S3.02, S3.03 (neliö, kolmio, ympyrä, pallo), S3.04, S3.05 (cm), S3.06 (tasa- ja puolitunnit)
- Tilastot: A12.S4.02 (pylväsdiagrammit)

**2. luokka: lukualue 0–100**
- Ajattelu: A12.S1.05
- Luvut: A12.S2.06 (periaate), S2.09, S2.10, S2.12 (kertotaulut 0–5 ja 10), S2.13
- Geometria ja mittaaminen: A12.S3.03, S3.05 (pituus, massa, tilavuus), S3.06 (kellonajat)
- Tilastot: A12.S4.01, S4.02 (tulkinta ja laatiminen)
- Ei sijoitettu lähteiden perusteella: A12.S2.04, S2.07, S2.14, S2.15, A12.S1.01, S1.04, S3.01. Sijoita paikallisesti.

**3. luokka: laskualgoritmit, kertotaulut, jakolasku, murtoluvun käsite**
- Ajattelu: A36.S1.01, S1.02, S1.05 (tutustuminen koodaukseen)
- Luvut: A36.S2.01, S2.03, S2.04 (päässä ja allekkain), S2.05 (kertotaulut 1–10), S2.06 (allekkain, muistinumero), S2.07, S2.11, S2.12 (samannimisten yhteen- ja vähennyslasku), S2.09 (pyöristys kymmeneen ja sataan, TNK)
- Algebra: A36.S3.01
- Geometria ja mittaaminen: A36.S4.03 (monikulmiot), S4.04 (kulmat), S4.09 (piiri ja pinta-ala), S4.08, S4.11 (mm, cm, m, km; kellonajat 0–24)
- Tilastot: A36.S5.02 (tutustuminen diagrammeihin)

**4. luokka: negatiiviset luvut, murto- ja desimaaliluvut, koordinaatisto**
- Luvut: A36.S2.08 (laskujärjestys, paikallinen lisäys), S2.05–S2.07, S2.10 (suuruusvertailu ja laskutoimitukset), S2.11–S2.14
- Algebra: A36.S3.01
- Geometria ja mittaaminen: A36.S4.03 (kolmio, nelikulmio), S4.05 (peilaus), S4.06 (koordinaatisto), S4.11 (pituus, massa, tilavuus, aika; yksikkömuutokset)
- Tilastot: A36.S5.02
- Ajattelu: A36.S1.05 (koodaus)

**5. luokka: prosentin käsite, yhtälöt, kulmat**
- Luvut: A36.S2.03, S2.08 (laskujärjestys), S2.11–S2.14, S2.15 (prosentin käsite)
- Algebra: A36.S3.01, S3.02, S3.03 (yhteen- ja vähennyslaskuyhtälöt)
- Geometria ja mittaaminen: A36.S4.04 (pisteestä kulmaan, yhdensuuntaiset ja leikkaavat suorat, kulman piirtäminen ja mittaaminen, kolmion kulmien summa), S4.03 (ympyrä), S4.06, S4.11
- Tilastot: A36.S5.01, S5.02, S5.03, S5.04 (T13:n perusteella)
- Ajattelu: A36.S1.03, S1.05 (algoritminen ajattelu, koodaus)

**6. luokka: mittakaava, pinta-alat ja tilavuus, prosentit, yhtälöt**
- Luvut: A36.S2.11–S2.16 (murto-, desimaali- ja prosenttiluvut)
- Algebra: A36.S3.01–S3.03 (myös kerto- ja jakolaskuyhtälöt)
- Geometria ja mittaaminen: A36.S4.07 (mittakaava, kartta), S4.09 (kolmion ja nelikulmion pinta-ala), S4.10 (särmiön pinta-ala ja tilavuus), S4.06, S4.11
- Tilastot: A36.S5.01–S5.04
- Ajattelu: A36.S1.05 (algoritminen ajattelu, graafinen koodaus)
- Kertaus 6. luokan lukuvuosiarviointia varten: kaikki T7–T14

**Paikallisten jakojen ero (suuntaa antava).** TNK-sivuston jaossa lukualue laajenee 0–1000 (3. lk), 0–10 000 (4. lk) ja 0–1 000 000 (5. lk), desimaaliluvut kymmenes- ja sadasosin alkavat jo 3. luokalla, murtolukujen yhteenlasku ja laventaminen 4. luokalla, supistaminen ja kertolasku 5. luokalla. Luumäellä negatiiviset luvut (suuruusvertailu ja laskutoimitukset) ovat 4. luokalla, TNK-otteissa 3.–5. luokalla niitä ei näkynyt. Prosentin käsite sijoittuu molemmissa 5. luokalle. Jos kysely on tarkoitettu tietylle koululle, tarkista sen oma jako.

## 6. Ohje kyselyjen ja applettien laatimiseen

**Tasot (lk 3–6).** Merkitse jokaiseen kysymykseen tunniste ja taso, esim. `A36.S2.11 / H`.

| Taso | Vastaa 6. luokan arvosanaa | Tehtävätyyppi |
|---|---|---|
| P (perus) | 5 | yksi askel, tuttu malli, apuväline tai kuva sallittu |
| T (tyydyttävä) | 7 | suora laskutehtävä ilman vihjettä |
| H (hyvä) | 8 | kaksi–kolme vaihetta, perustelu, käsitteen tunnistaminen |
| K (kiitettävä) | 9 | soveltava ongelma, useita ratkaisutapoja, ratkaisun arviointi |

Vuosiluokilla 1–2 tasoja ei ole. Käytä kahta merkintää: `V` (vahvistava, tuttu tilanne) ja `S` (soveltava, uusi tilanne), ja vältä arvosanamerkintöjä.

**Periaatteet.**
- Yksi kysymys tai applet mittaa ensisijaisesti yhtä ID:tä; sivutavoitteet (T4, T6) voi merkitä erikseen.
- Lk 1–2: konkretia ensin (kuva, esine, lukusuora, kymmenkannat), symbolit vasta sen jälkeen. Hyvin lyhyet tekstit; ohjeet voi lukea ääneen.
- Lk 3–6: laskutehtävän lisäksi vähintään yksi kysymys, jossa selitetään tai perustellaan (T4) ja arvioidaan tuloksen järkevyyttä (T6).
- Desimaalierotin pilkku, suomenkieliset termit: hajotelma, kymmenylitys, ositusjako, sisältöjako, jakojäännös, nimittäjä, osoittaja, samannimiset murtoluvut, laventaminen, supistaminen, kulma, monikulmio, pinta-ala, piiri, mittakaava, tyyppiarvo, keskiarvo.
- Arkisia yhteyksiä: rahat, kellonajat, reseptit, kartan mittakaava, urheilutilastot, alennukset.

**Yleisiä virhekäsityksiä (vääriksi vastausvaihtoehdoiksi ja "Varo virhekäsitystä" -laatikoihin).** Lähteet ja todistusvoima: Claude-dokumentti *Finnish Math Curriculum and Misconceptions, Grades 1–6* (30.9.2026). † = tunnettu kirjallisuudessa, ei tarkistettu.

| ID | Virhekäsitys |
|---|---|
| A12.S2.06, A36.S2.01 | Kaksinumeroinen luku luetaan kahtena erillisenä yksinumeroisena lukuna, ei kymmeninä ja ykkösinä |
| A36.S2.04 | Pienempi numero vähennetään aina suuremmasta, riippumatta paikasta†: 302 − 148 = 246 (oikein 154) |
| A12.S2.08, A36.S3.03 | "=" tarkoittaa "laske vastaus" ja on aina lopussa: 8 + 4 = □ + 5 vastataan 12 tai 17 (oikein 7) |
| A12.S2.12, A36.S2.05 | Kertolasku on vain yhtä suurten ryhmien yhteenlasku |
| A36.S2.07, S2.12, S2.14 | Kertolasku aina suurentaa ja jakolasku pienentää; jaettavan täytyy olla jakajaa suurempi: 6 : 0,5 = 3 (oikein 12) |
| A36.S2.11 | Suurempi nimittäjä tarkoittaa suurempaa murtolukua: 1/8 > 1/4 |
| A36.S2.12 | Murtolukujen yhteenlasku osoittajat ja nimittäjät erikseen: 1/2 + 1/3 = 2/5 |
| A36.S2.13 | Pidempi desimaaliluku on suurempi (tai lyhyempi suurempi): 0,123 > 0,5; 0,25 > 0,3 |
| A36.S2.10 | Miinusmerkillä on vain yksi merkitys (vähennys), ei luvun merkkiä |
| A36.S4.03 | Neliö ei ole suorakulmio; kuvio tunnistetaan vain tutun asennon perusteella |
| A36.S4.04 | Kulman suuruus on haarojen pituus tai kuvion muoto† |
| A36.S4.09 | Pinta-ala ja piiri sekoittuvat; ruudukkoa ei nähdä riveinä ja sarakkeina, kaava opitaan ennen peittämisen ideaa |

**Lukutaito.** Sanalliset tehtävät edellyttävät lukutaitoa. Pidä tekstit lyhyinä lk 1–3:n tehtävissä.

## 7. Nykyiset appletit ja kattavuus

Ei tunnettuja appletteja vuosiluokille 1–6. Nykyiset appletit (`suoran-yhtalo`, `pythagoras-neliot`, `prosentti-kerroin`) on tarkoitettu lk 7–9:lle.

Ehdokkaita BACKLOG.md:hen (jokainen palautuu yhteen ID:hen ja virhekäsitykseen):

- A12.S2.06 kymmenjärjestelmä kymmenkantojen ja lukusuoran avulla (kaksinumeroiset luvut kymmeninä ja ykkösinä)
- A12.S2.08 yhtälö vaakana: 8 + 4 = □ + 5 ("=" tarkoittaa yhtä suurta)
- A36.S2.11 murtoluku alueina ja lukusuorana (suurempi nimittäjä, pienempi osa)
- A36.S2.12 murtolukujen yhteenlasku alueina (osoittajat ja nimittäjät)
- A36.S2.13 desimaaliluvut lukusuoralla ja paikkataulukossa
- A36.S2.07 jakolasku ositus- ja sisältöjakona myös desimaalijakajalla
- A36.S4.04 kulman mittaaminen ja piirtäminen
- A36.S4.09 pinta-ala peittämällä ruudukolla ennen kaavaa; piiri vs. pinta-ala

## Lähteet

- POPS 2014, matematiikka 1–2 ja 3–6 (peda.net, Keski-Suomen kuntien opetussuunnitelman työversio, kohta "Perusopetuksen opetussuunnitelman perusteet"): luku 13.4.4 ja 14.4.4
- Opetushallitus: [Perusopetuksen opetussuunnitelman perusteet 2014, PDF](https://www.oph.fi/sites/default/files/documents/perusopetuksen_opetussuunnitelman_perusteet_2014.pdf)
- Opetushallitus: [6. vuosiluokan lukuvuosiarviointi](https://www.oph.fi/fi/koulutus-ja-tutkinnot/6-vuosiluokan-lukuvuosiarviointi) ja [Matematiikka, kriteerit (6. lk), PDF](https://www.oph.fi/sites/default/files/documents/Matematiikka%2C%20kriteerit%20%286.%20lk%29.pdf)
- Luumäen perusopetuksen opetussuunnitelma 2016, matematiikka 3.–6. lk: [3. lk](https://peda.net/luumaki/perusopetus/ol/1vmosotjksl/tjkvnl/14-4-4-matematiikka/matematiikka-3-lk/mtjs), [4. lk](https://peda.net/luumaki/perusopetus/ol/1vmosotjksl/tjkvnl/14-4-4-matematiikka/matematiikka-4-lk), [5. lk](https://peda.net/luumaki/perusopetus/ol/1vmosotjksl/tjkvnl/14-4-4-matematiikka/matematiikka-5-lk), [6. lk](https://peda.net/luumaki/perusopetus/ol/1vmosotjksl/tjkvnl/14-4-4-matematiikka/matematiikka-6-lk)
- TNK POPS: [1. lk](https://sites.utu.fi/popstnk/wp-content/uploads/sites/278/2023/01/1.lk-matematiikka.pdf), [2. lk](https://sites.utu.fi/popstnk/wp-content/uploads/sites/278/2023/01/2.lk-matematiikka.pdf), [3. lk](https://sites.utu.fi/popstnk/wp-content/uploads/sites/278/2023/01/3.lk-matematiikka.pdf), [4. lk](https://sites.utu.fi/popstnk/wp-content/uploads/sites/278/2023/01/4.lk-matematiikka.pdf), [5. lk](https://sites.utu.fi/popstnk/wp-content/uploads/sites/278/2023/01/5.lk-matematiikka.pdf)
