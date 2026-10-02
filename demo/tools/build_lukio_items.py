"""Writes ../data/lukio_items.json: the hand-written upper secondary demo
exercises. Edit the items here and run `python3 tools/build_lukio_items.py`
from demo/, then `npm test`."""
import json
import os
items = []
def ne(set_, text, answer, wrong=(), hint=None, steps=None, correct=None):
    n = sum(1 for i in items if i['set'] == set_) + 1
    p = {'answer': answer, 'wrong': [{'match': m, 'misconception': None, 'feedback': f} for m, f in wrong]}
    if hint: p['input_hint'] = hint
    items.append({'id': f'DEMO-{set_}-{n:02d}', 'set': set_, 'type': 'NE', 'status': 'demo', 'prompt': {'text': text}, 'payload': p,
                  'solution': {'steps': steps} if steps else None, 'feedback': {'correct': correct} if correct else None})
def mc(set_, text, options, right, steps=None):
    n = sum(1 for i in items if i['set'] == set_) + 1
    opts = [{'id': 'abcd'[k], 'text': t, 'misconception': None, 'feedback': f} for k, (t, f) in enumerate(options)]
    items.append({'id': f'DEMO-{set_}-{n:02d}', 'set': set_, 'type': 'MC', 'status': 'demo', 'prompt': {'text': text},
                  'payload': {'options': opts, 'correct': ['abcd'[right]]}, 'solution': {'steps': steps} if steps else None})
num = lambda v, **k: {'kind': 'number', 'value': v, **k}
st = lambda *v: {'kind': 'set', 'values': list(v)}
ex = lambda r: {'kind': 'expression', 'variables': ['x'], 'reference': r, 'samples': [[-2], [0], [3]]}
ty = lambda v: {'kind': 'typed', 'value': v}

S = 'MAA2-yhtalot'
ne(S, 'Ratkaise yhtälö x² − 5x + 6 = 0.', st(2, 3), [('−2; −3', 'Tarkista merkit: x² − 5x + 6 = (x − 2)(x − 3), joten nollakohdat ovat positiiviset.')], 'Kirjoita ratkaisut puolipisteellä, esim. 1; 4',
   ['Tulo (x − 2)(x − 3) = x² − 5x + 6', 'Tulo on nolla, kun x = 2 tai x = 3'])
ne(S, 'Montako reaalista ratkaisua yhtälöllä x² + 4x + 5 = 0 on?', num(0), [('2', 'Laske ensin diskriminantti D = b² − 4ac. Jos D < 0, reaalisia ratkaisuja ei ole.'), ('1', 'Yksi ratkaisu on vain silloin, kun diskriminantti on 0.')], 'Kirjoita luku',
   ['D = 4² − 4 · 1 · 5 = 16 − 20 = −4', 'D < 0, joten reaalisia ratkaisuja ei ole'])
ne(S, 'Ratkaise yhtälö x² = 49.', st(7, -7), [('7', 'Myös (−7)² = 49. Yhtälöllä on kaksi ratkaisua.')], 'Kirjoita ratkaisut puolipisteellä, esim. 1; 4', ['x = ±√49 = ±7'])
mc(S, 'Mihin suuntaan paraabeli y = −2x² + 3 aukeaa?', [('Ylöspäin', 'Katso x²:n kerrointa: −2 on negatiivinen.'), ('Alaspäin', None), ('Oikealle', 'Funktion y = ax² + c kuvaaja aukeaa aina ylös tai alas.')], 1,
   ['x²:n kerroin a = −2 < 0', 'Kun a < 0, paraabeli aukeaa alaspäin'])
ne(S, 'Paraabelin y = x² − 6x + 1 huippu on kohdassa x = ?', num(3), [('−3', 'Huipun x-koordinaatti on x = −b/(2a) = −(−6)/2. Tarkista merkki.')], 'Kirjoita luku', ['x = −b/(2a) = −(−6)/(2 · 1) = 3'])
ne(S, 'Ratkaise yhtälö 2x² − 8x = 0.', st(0, 4), [('4', 'Jos jaat x:llä, ratkaisu x = 0 katoaa. Ota x yhteiseksi tekijäksi: 2x(x − 4) = 0.')], 'Kirjoita ratkaisut puolipisteellä, esim. 1; 4',
   ['2x(x − 4) = 0', 'x = 0 tai x = 4'])

S = 'MAA6-derivaatta'
ne(S, 'Derivoi f(x) = x³ − 4x.', ex('3x² − 4'), [('3x² − 4x', 'Termin −4x derivaatta on −4, ei −4x.'), ('3x²', 'Myös termi −4x derivoidaan: sen derivaatta on −4.')], 'Kirjoita esim. 2x + 1',
   ['D x³ = 3x²', 'D(−4x) = −4', "f'(x) = 3x² − 4"])
ne(S, "Olkoon f(x) = x². Laske f'(3).", num(6), [('9', "Laskit funktion arvon f(3). Derivoi ensin: f'(x) = 2x.")], 'Kirjoita luku', ["f'(x) = 2x", "f'(3) = 2 · 3 = 6"])
ne(S, 'Mikä on käyrän y = x² − 2x tangentin kulmakerroin kohdassa x = 1?', num(0), [('−1', "Laskit käyrän pisteen y-koordinaatin. Kulmakerroin on derivaatan arvo: y' = 2x − 2.")], 'Kirjoita luku',
   ["y' = 2x − 2", "y'(1) = 2 − 2 = 0"])
mc(S, "Funktiolle pätee f'(2) = 0, ja derivaatta vaihtaa kohdassa x = 2 merkkinsä negatiivisesta positiiviseksi. Mikä kohta x = 2 on?",
   [('Minimikohta', None), ('Maksimikohta', 'Funktio ensin vähenee (f\' < 0) ja sitten kasvaa (f\' > 0). Silloin kohta on pohja, ei huippu.'), ('Ei kumpikaan', 'Kun derivaatan merkki vaihtuu, kohta on ääriarvokohta.')], 0,
   ['Vasemmalla f vähenee, oikealla kasvaa', 'Kohta x = 2 on paikallinen minimikohta'])
ne(S, 'Derivoi f(x) = 5x² + 3x + 7.', ex('10x + 3'), [('10x + 10', 'Vakion 7 derivaatta on 0.')], 'Kirjoita esim. 2x + 1',
   ['D 5x² = 10x', 'D 3x = 3', 'D 7 = 0', "f'(x) = 10x + 3"])

S = 'MAA7-yksikkoympyra'
mc(S, 'Mikä on sin 30°?', [('1/2', None), ('√3/2', 'Tämä on cos 30°. Sini on yksikköympyrän pisteen y-koordinaatti.'), ('√2/2', 'Tämä on sin 45°.'), ('3/10', 'Kulman asteluku ei ole sinin arvo.')], 0,
   ['Kulmaa 30° vastaava piste on (√3/2, 1/2)', 'sin 30° on y-koordinaatti 1/2'])
ne(S, 'Mikä on cos 180°?', num(-1), [('1', 'Kulmaa 180° vastaava piste on (−1, 0). Kosini on x-koordinaatti.'), ('0', 'Kulmaa 180° vastaava piste on (−1, 0). Kosini on x-koordinaatti, sini y-koordinaatti.')], 'Kirjoita luku',
   ['Kulmaa 180° vastaava piste on (−1, 0)', 'cos 180° = −1'])
mc(S, 'Kuinka monta radiaania on 90°?', [('π/2', None), ('π', 'π radiaania on 180°.'), ('π/4', 'π/4 radiaania on 45°.'), ('90π', 'Muunnos: kerro luvulla π/180°.')], 0, ['90° · π/180° = π/2'])
mc(S, 'Kulmalle α pätee sin α > 0 ja cos α < 0. Missä neljänneksessä kulman kehäpiste on?',
   [('I neljänneksessä', 'I neljänneksessä sekä sini että kosini ovat positiivisia.'), ('II neljänneksessä', None), ('III neljänneksessä', 'III neljänneksessä myös sini on negatiivinen.'), ('IV neljänneksessä', 'IV neljänneksessä sini on negatiivinen ja kosini positiivinen.')], 1,
   ['y-koordinaatti positiivinen, x-koordinaatti negatiivinen', 'Piste on vasemmalla ylhäällä: II neljännes'])
ne(S, 'Laske sin² 40° + cos² 40°.', num(1), [], 'Kirjoita luku', ['Yksikköympyrän piste toteuttaa x² + y² = 1', 'Siksi sin² α + cos² α = 1 kaikilla α'])

S = 'MAA8-eksp-log'
ne(S, 'Laske log₂ 8.', num(3), [('4', 'log₂ 8 kysyy, mihin potenssiin 2 korotetaan, jotta saadaan 8. Se ei ole 8 : 2.')], 'Kirjoita luku', ['2³ = 8', 'Siis log₂ 8 = 3'])
ne(S, 'Laske lg 1000.', num(3), [('100', 'lg on kymmenkantainen logaritmi: mihin potenssiin 10 korotetaan, jotta saadaan 1000?')], 'Kirjoita luku', ['10³ = 1000', 'lg 1000 = 3'])
ne(S, 'Ratkaise yhtälö 2ˣ = 32.', num(5), [('16', 'Kysytään eksponenttia: kuinka monta kakkosta kerrotaan, jotta saadaan 32?')], 'Kirjoita luku', ['32 = 2⁵', 'x = 5'])
ne(S, 'Laske ln(e⁴).', num(4), [], 'Kirjoita luku', ['ln ja e-kantainen potenssi kumoavat toisensa', 'ln(e⁴) = 4'])
mc(S, 'Laske log₃ 9 + log₃ 3.', [('3', None), ('log₃ 12', 'Logaritmien summa on tulon logaritmi: log₃(9 · 3), ei summan.'), ('2', 'log₃ 9 = 2, mutta myös log₃ 3 = 1 lasketaan mukaan.'), ('12', 'Logaritmeja ei voi korvata niiden argumenteilla.')], 0,
   ['log₃ 9 = 2 ja log₃ 3 = 1', 'Summa on 3 (tai log₃ 27 = 3)'])
ne(S, 'Ratkaise yhtälö 3ˣ = 1.', num(0), [('1', 'Mikä tahansa nollasta poikkeava luku potenssiin 0 on 1.')], 'Kirjoita luku', ['3⁰ = 1', 'x = 0'])

S = 'MAA9-integraali'
ne(S, 'Laske integraali ∫₀² 2x dx.', num(4), [('2', 'Integraalifunktio on x². Sijoita rajat: 2² − 0².'), ('8', 'Älä kerro funktion arvoa välin pituudella: alue on kolmio, jonka ala on 2 · 4 / 2.')], 'Kirjoita luku',
   ['Integraalifunktio F(x) = x²', 'F(2) − F(0) = 4 − 0 = 4'])
ne(S, 'Anna funktion f(x) = x² integraalifunktio, jossa vakio C = 0.', ex('x³/3'), [('2x', 'Tämä on derivaatta. Integroinnissa eksponenttia kasvatetaan yhdellä ja jaetaan uudella eksponentilla.'), ('x³', 'Muista jakaa uudella eksponentilla: x³/3.')], 'Kirjoita esim. x^4/4',
   ['∫ xⁿ dx = xⁿ⁺¹/(n + 1)', 'F(x) = x³/3'])
ne(S, 'Laske integraali ∫₁³ 5 dx.', num(10), [('5', 'Vakiofunktion integraali on suorakulmion ala: korkeus 5, leveys 3 − 1 = 2.'), ('15', 'Välin pituus on 3 − 1 = 2, ei 3.')], 'Kirjoita luku', ['Integraalifunktio 5x', '5 · 3 − 5 · 1 = 10'])
ne(S, 'Laske integraali ∫₀³ x² dx.', num(9), [('27', 'Integraalifunktio on x³/3: muista jakaa kolmella.'), ('6', 'Derivoit funktion. Integraalissa tarvitaan integraalifunktio x³/3.')], 'Kirjoita luku',
   ['F(x) = x³/3', 'F(3) − F(0) = 27/3 = 9'])
mc(S, 'Funktio f on välillä [1, 4] negatiivinen. Mikä on integraalin ∫₁⁴ f(x) dx merkki?', [('Negatiivinen', None), ('Positiivinen', 'Pinta-ala on positiivinen, mutta x-akselin alapuolinen alue tuo integraaliin negatiivisen osuuden.'), ('Nolla', 'Integraali on nolla vain, jos ylä- ja alapuolisten alueiden alat kumoavat toisensa.')], 0,
   ['Kuvaaja on x-akselin alapuolella koko välillä', 'Integraali on alueen pinta-alan vastaluku, siis negatiivinen'])

S = 'MAB-toisen-asteen-malli'
ne(S, 'Voitto on V(x) = −2x² + 40x − 100 euroa, kun myydään x kappaletta. Millä x:n arvolla voitto on suurin?', num(10), [('−10', 'Huipun kohta on x = −b/(2a) = −40/(2 · (−2)). Tarkista merkit.'), ('20', 'Muista kerroin 2 nimittäjässä: x = −b/(2a).')], 'Kirjoita luku',
   ['a = −2, b = 40', 'x = −40/(2 · (−2)) = 10'])
ne(S, 'Voitto on V(x) = −2x² + 40x − 100 euroa. Kuinka suuri on suurin voitto (x = 10)?', num(100, unit='€'), [('500', 'Sijoita x = 10 jokaiseen termiin: −2 · 10² = −200.')], 'Kirjoita luku',
   ['V(10) = −2 · 100 + 400 − 100', 'V(10) = 100 €'])
ne(S, 'Ratkaise yhtälö x² − 16 = 0.', st(4, -4), [('4', 'Myös (−4)² = 16. Yhtälöllä on kaksi ratkaisua.')], 'Kirjoita ratkaisut puolipisteellä, esim. 1; 4', ['x² = 16', 'x = 4 tai x = −4'])
ne(S, 'Laske funktion f(x) = 3x² − 2 arvo, kun x = −2.', num(10), [('−14', '(−2)² = 4, ei −4. Neliö on aina ei-negatiivinen.'), ('34', 'Potenssi lasketaan ennen kertolaskua: 3 · (−2)² = 3 · 4.')], 'Kirjoita luku',
   ['(−2)² = 4', '3 · 4 − 2 = 10'])
ne(S, 'Ratkaise yhtälö x² + 2x − 15 = 0.', st(3, -5), [('−3; 5', 'Tarkista merkit: x² + 2x − 15 = (x + 5)(x − 3).')], 'Kirjoita ratkaisut puolipisteellä, esim. 1; 4',
   ['Ratkaisukaava: x = (−2 ± √(4 + 60)) / 2 = (−2 ± 8) / 2', 'x = 3 tai x = −5'])

S = 'MAB-prosentit-talous'
ne(S, 'Takki maksaa 250 €. Hintaa alennetaan 20 %. Mikä on uusi hinta?', num(200, unit='€'), [('230', 'Alennus on 20 prosenttia hinnasta, ei 20 euroa: 0,20 · 250 € = 50 €.'), ('50', 'Tämä on alennuksen suuruus. Kysyttiin uutta hintaa.')], 'Kirjoita luku',
   ['Kerroin 1 − 0,20 = 0,80', '0,80 · 250 € = 200 €'])
ne(S, 'Hinta nousee ensin 10 % ja laskee sitten 10 %. Montako prosenttia uusi hinta on alkuperäisestä?', num(99, unit='%'), [('100', 'Lasku lasketaan jo korotetusta hinnasta. Kertoimet: 1,10 · 0,90.')], 'Kirjoita luku',
   ['1,10 · 0,90 = 0,99', 'Uusi hinta on 99 % alkuperäisestä'])
ne(S, 'Tilille talletetaan 1000 €. Vuotuinen korko on 2 % ja korko lisätään pääomaan. Paljonko tilillä on 2 vuoden kuluttua?', num(1040.4, unit='€', tolerance=0.005), [('1040', 'Toisena vuonna korkoa kertyy myös ensimmäisen vuoden korolle: 1000 · 1,02².')], 'Kirjoita luku sentin tarkkuudella',
   ['1000 € · 1,02² = 1000 € · 1,0404', '= 1040,40 €'])
ne(S, 'Hinta laskee 15 %. Millä kertoimella vanha hinta kerrotaan, jotta saadaan uusi hinta?', num(0.85), [('0,15', 'Tämä on muutos. Uusi hinta on 100 % − 15 % vanhasta.'), ('1,15', 'Kerroin 1,15 tarkoittaa 15 %:n nousua.')], 'Kirjoita desimaaliluku', ['100 % − 15 % = 85 %', 'Kerroin 0,85'])
ne(S, 'Kuukausipalkka nousee 1800 eurosta 1890 euroon. Montako prosenttia palkka nousi?', num(5, unit='%'), [('90', 'Tämä on nousu euroina. Jaa nousu vanhalla palkalla.'), ('4,76', 'Vertaa vanhaan palkkaan: 90 € / 1800 €, ei uuteen.')], 'Kirjoita luku',
   ['Nousu 1890 € − 1800 € = 90 €', '90 / 1800 = 0,05 = 5 %'])

S = 'MAB-todennakoisyys'
ne(S, 'Noppaa heitetään kaksi kertaa. Millä todennäköisyydellä saadaan kaksi kuutosta? Anna vastaus murtolukuna.', ty('1/36'), [('1/3', 'Riippumattomien tapahtumien todennäköisyydet kerrotaan, ei lasketa yhteen.'), ('2/36', 'Kaksi kuutosta on vain yksi alkeistapaus (6, 6) kaikista 36:sta.')], 'Kirjoita esim. 1/6',
   ['P(kuutonen) = 1/6 kummallakin heitolla', '1/6 · 1/6 = 1/36'])
ne(S, 'Kuinka monessa eri järjestyksessä neljä kirjaa voidaan asettaa hyllyyn?', num(24), [('16', 'Järjestyksiä on 4!, eli 4 · 3 · 2 · 1.'), ('4', 'Ensimmäiselle paikalle on 4 vaihtoehtoa, toiselle 3 ja niin edelleen.')], 'Kirjoita luku', ['4! = 4 · 3 · 2 · 1 = 24'])
ne(S, 'Viiden hengen joukosta valitaan kaksi edustajaa. Kuinka monella tavalla valinta voidaan tehdä?', num(10), [('20', 'Järjestyksellä ei ole väliä: pari (A, B) on sama kuin (B, A). Jaa kahdella.'), ('25', 'Samaa henkilöä ei voi valita kahdesti, eikä järjestyksellä ole väliä.')], 'Kirjoita luku',
   ['Järjestettyjä pareja 5 · 4 = 20', 'Jokainen pari kahdesti: 20 : 2 = 10'])
ne(S, 'Korttipakasta (52 korttia) nostetaan yksi kortti. Millä todennäköisyydellä se on hertta? Anna vastaus murtolukuna.', ty('1/4'), [('1/13', 'Herttoja on 13 kappaletta, joten todennäköisyys on 13/52.'), ('1/52', 'Herttoja on 13, ei yksi.')], 'Kirjoita esim. 1/6',
   ['Herttoja on 13', '13/52 = 1/4'])
mc(S, 'Tapahtuman A todennäköisyys on 0,3. Mikä on todennäköisyys, että A ei tapahdu?', [('0,7', None), ('0,3', 'Vastatapahtuman todennäköisyys on 1 − P(A).'), ('−0,3', 'Todennäköisyys ei voi olla negatiivinen.'), ('1,3', 'Todennäköisyys on enintään 1. Vähennä: 1 − 0,3.')], 0, ['P(ei A) = 1 − 0,3 = 0,7'])

for i in items:
    if i.get('solution') is None: i.pop('solution', None)
    if i.get('feedback') is None: i.pop('feedback', None)
out = {'schema_version': 1, 'note': 'Demo exercises for upper secondary (lukio), written by hand for the demo site. Same item shape as the grades 7-9 bank (math-misconceptions/schema/item.schema.json, types NE and MC), plus `set` naming the demo topic. Not reviewed by a teacher.', 'items': items}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'lukio_items.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(items))
