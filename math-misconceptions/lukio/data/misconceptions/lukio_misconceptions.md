# Misconception catalogue, upper secondary (lukio)

Version 2026-10-01. Upper secondary counterpart of the `Misconceptions` sheet in `../../../sources/math_misconceptions_item_bank.xlsx` (grades 1–9). That workbook belongs to the 7–9 pipeline and is read only here, so the lukio rows live in this file until a human decides to add them to the workbook.

**Status: draft, evidence not yet checked.** Ratings below are a first assessment from the literature found on 1 October 2026 (web search only; the container could not open publisher pages or OPH). Before a topic is generated in bulk, do the same evidence check the grades 1–6 pipeline did: trace each source to the primary study and confirm the typical wrong answer appears there. Rows marked † cite a source from memory or from a secondary mention.

Keys in the Sources column refer to `math_misconceptions_lukio.bib` in this folder, or to the 7–9 bibliography `../../../sources/math_misconceptions_grades7-9.bib` (marked *7–9 bib*).

## 1. ID scheme

- New lukio rows: `L` + strand + number, e.g. `LDER-02`. The `L` prefix keeps them apart from the 1–9 workbook IDs (`ALG-`, `NUM-`, `FUN-`, …), which may still grow.
- Strands: `LFUN` functions, `LEQU` equations and inequalities, `LEXP` powers, exponentials and logarithms, `LTRI` trigonometry, `LGEO` geometry, `LVEC` vectors, `LLIM` limits and continuity, `LDER` derivative, `LINT` integral, `LSTA` statistics, `LPRB` probability and combinatorics, `LFIN` financial mathematics, `LLOG` logic and number theory.
- Rows from the 1–9 workbook that carry on into lukio keep their IDs (section 3). A lukio item may tag both kinds.
- Evidence scale as in the workbook: **Strong** = several studies or one large sample; **Moderate** = at least one empirical study; **Limited** = review, practitioner source or classroom report only.

## 2. Lukio rows

| ID | Misconception | Typical wrong answer | Correct | Main goal (also) | Syllabus | Evidence | Sources | Notes |
|---|---|---|---|---|---|---|---|---|
| LFUN-01 | A function must be one formula; a piecewise or constant rule is not a function | "f(x) = 2 for every x is not a function"; piecewise f rejected | Any rule giving one value per input is a function | MAA12.01 (MAY1.07) | MAA, MAB | Strong | vinner1989images (*7–9 bib*), breidenbach1992development | Same idea as 7–9 FUN-04 |
| LFUN-02 | Linearity applied to every function: f(a + b) = f(a) + f(b) | √(9 + 16) = 3 + 4 = 7; sin(a + b) = sin a + sin b | √25 = 5; use the function's own rules | MAA2.01 (MAA5.03, MAA5.07) | MAA, MAB | Strong | matz1982process (*7–9 bib*), debock2002improper (*7–9 bib*) | Umbrella for LEXP-01 and LTRI-02; tag the specific row too |
| LFUN-03 | f⁻¹ read as the reciprocal 1/f | inverse of f(x) = 2x + 1 given as 1/(2x + 1) | f⁻¹(x) = (x − 1)/2 | MAA12.04 | MAA | Limited | † | No study found yet; notation clash with x⁻¹ is the suspected cause |
| LEQU-01 | Dividing both sides by an expression that can be zero | x² = 3x ⇒ x = 3 | x = 0 or x = 3 | MAA2.05 (MAA2.04, MAB2.04) | MAA, MAB | Moderate | vaiyavutjamai2006effects † | Very common in YTL marking notes † |
| LEQU-02 | Zero-product rule used when the product is not zero | (x − 2)(x − 3) = 6 ⇒ x = 8 or x = 9 | expand: x² − 5x = 0, so x = 0 or x = 5 | MAA2.05 | MAA | Moderate | vaiyavutjamai2006effects | Check full text for the exact item |
| LEQU-03 | Inequality multiplied by an expression of unknown sign | 1/x < 2 ⇒ 1 < 2x ⇒ x > ½ | x < 0 or x > ½ | MAA2.06 (MAA2.07) | MAA | Moderate | tsamir2004consistencies † | 7–9 EXT-03 is the numeric version |
| LEQU-04 | Square root taken across an inequality | x² < 4 ⇒ x < ±2 or x < 2 | −2 < x < 2 | MAA2.06 | MAA | Moderate | tsamir2004consistencies † | Continues 7–9 EXT-04 (x² = 9) |
| LEQU-05 | Absolute value means "drop the minus sign" | \|x − 3\| = 5 ⇒ x = 8 only; \|−a\| = a for every a, so \|x\| = −x impossible | x = 8 or x = −2; \|x\| = −x when x ≤ 0 | MAA4.06 (MAY1.02) | MAA | Moderate | almog2012absolute | |
| LEXP-01 | Logarithm rules made linear or mixed with power rules | log(a + b) = log a + log b; log a / log b = log(a/b) | log(ab) = log a + log b; log a / log b = log_b a | MAA5.07 (MAB4.03) | MAA, MAB | Moderate | kenney2013links, weber2002developing | |
| LEXP-02 | Fractional or negative exponent read as division or a negative number | 8^(1/3) = 8/3; 2⁻³ = −6 or −8 | 8^(1/3) = 2; 2⁻³ = 1/8 | MAA5.05 (MAY1.04) | MAA, MAB | Moderate | weber2002developing † | 7–9 EXT-02 is the integer-exponent version |
| LEXP-03 | Exponential growth judged as linear (exponential growth bias) | 3 % a year for 20 years: +60 %; doubling time underestimated or overestimated | 1,03²⁰ ≈ 1,81, so +81 % | MAB4.02 (MAA5.06, MAA9.03, MAB7.01) | MAA, MAB | Strong | wagenaar1975misperception, stango2009exponential | Adults and students; strong link to LFIN-01 |
| LEXP-04 | Exponential equation solved by dividing by the base | 2^x = 10 ⇒ x = 5 | x = log₂ 10 ≈ 3,32 | MAA5.06 (MAB4.03) | MAA, MAB | Limited | weber2002developing † | |
| LTRI-01 | Trigonometric equation has one solution | sin x = ½ ⇒ x = 30° (or π/6) only | x = π/6 + n·2π or x = 5π/6 + n·2π | MAA5.04 | MAA | Moderate | weber2005students † | |
| LTRI-02 | Sine treated as a factor that can be split | sin 2x = 2 sin x; sin(x)/x = sin | sin 2x = 2 sin x cos x | MAA5.03 (MAA6.07) | MAA | Moderate | weber2005students †, matz1982process (*7–9 bib*) | Sub-case of LFUN-02 |
| LTRI-03 | Radian not seen as a measure of angle; π "is 180" | π = 180; calculator left in degree mode gives sin 2 ≈ 0,035 | π rad corresponds to 180°; π ≈ 3,14 | MAA5.01 | MAA | Moderate | akkoc2008preservice, moore2014quantitative | |
| LTRI-04 | sin⁻¹ x read as 1/sin x | sin⁻¹(0,5) = 2 | sin⁻¹(0,5) = 30° (arcsin) | MAA5.04 | MAA | Limited | † | Calculator notation; same clash as LFUN-03 |
| LGEO-01 | Sine law gives one triangle in the ambiguous case (SSA) | one angle reported, obtuse alternative missed | two triangles when both angles fit | MAA3.03 | MAA | Limited | † | YTL marking notes; no study found |
| LVEC-01 | Length of a sum is the sum of lengths | \|a + b\| = \|a\| + \|b\| = 7 for \|a\| = 3, \|b\| = 4 at right angles | \|a + b\| = 5 | MAA4.07 (MAA4.08) | MAA | Strong | nguyen2003initial | 2 031 students; physics context |
| LVEC-02 | A vector is tied to its position | vectors not moved tail to head before adding; equal vectors in different places called different | a vector is a free displacement | MAA4.07 | MAA | Moderate | nguyen2003initial, barniol2014test | |
| LVEC-03 | Dot product gives a vector | a · b = (a₁b₁, a₂b₂) | a · b = a₁b₁ + a₂b₂, a number | MAA4.08 (MAA10.02) | MAA | Moderate | barniol2014test | |
| LLIM-01 | A limit cannot be reached; it is a bound | "the limit of f(x) = 3 as x → 2 is never 3"; limit as "almost" | the limit is a number; the function may equal it | MAA6.01 | MAA | Strong | tall1981concept, williams1991models, cornu1991limits | |
| LLIM-02 | 0,999… is less than 1 | 0,999… < 1 "by an infinitely small amount" | 0,999… = 1 | MAA6.01 (MAY1.01) | MAA | Strong | tall1978conflicts, merenluoto2004number (*7–9 bib*) | Finnish data in Merenluoto & Lehtinen |
| LLIM-03 | Limit is the function value | lim x→a f(x) = f(a) always; limit exists only if f is continuous | limit may differ from f(a) or exist where f is undefined | MAA6.01 (MAA6.02) | MAA | Moderate | williams1991models, palomaki2024ylioppilaskokelaiden | Finnish YO data (2020–2022) |
| LLIM-04 | Continuous means "drawn without lifting the pen" on all of ℝ | f(x) = 1/x is not continuous | 1/x is continuous on its domain | MAA6.02 (MAA12.02) | MAA | Moderate | tall1981concept, palomaki2024ylioppilaskokelaiden | |
| LDER-01 | Product and quotient rules made linear | (fg)′ = f′g′; (f/g)′ = f′/g′ | (fg)′ = f′g + fg′ | MAA6.05 | MAA | Moderate | orton1983differentiation | |
| LDER-02 | Chain rule: inner derivative omitted | d/dx sin 3x = cos 3x; d/dx e^(2x) = e^(2x) | 3 cos 3x; 2e^(2x) | MAA6.06 | MAA | Moderate | clark1997constructing, orton1983differentiation | |
| LDER-03 | f′(a) = 0 always gives an extremum; extrema only where f′ = 0 | x³ has a minimum at 0; endpoints of a closed interval ignored | x³ has a terrace point; check sign change and endpoints | MAA6.08 (MAA6.09, MAB8.04) | MAA, MAB | Moderate | hahkioniemi2006role †, derivaatta2021ylioppilas † | Finnish YO analysis; check full text |
| LDER-04 | Graph of f′ read as graph of f | where f′ is highest, f is highest; f′ < 0 read as f < 0 | f′ gives the slope of f | MAA6.08 (MAB8.03) | MAA, MAB | Strong | asiala1997development, nemirovsky1992students † | Continues 7–9 FUN-02 (slope–height) |
| LDER-05 | Continuous implies differentiable; piecewise derivative from the pieces only | \|x\| differentiable at 0; derivative at a joint taken from one piece | check both one-sided derivative limits | MAA12.02 (MAA6.02) | MAA | Moderate | viholainen2008incoherence, palomaki2024ylioppilaskokelaiden | Finnish sources |
| LINT-01 | Integration constant omitted; antiderivative is unique | ∫2x dx = x² | x² + C | MAA7.01 | MAA | Moderate | orton1983integration | |
| LINT-02 | Definite integral is always an area | ∫ from −1 to 1 of x³ dx called area 0; area below the axis added with its sign | area = ∫\|f\|; integral is signed | MAA7.04 (MAA7.03) | MAA | Moderate | orton1983integration, kuningas2023lukiolaisten † | Finnish thesis; check full text |
| LINT-03 | Integral of a product or quotient taken factor by factor; power rule used for n = −1 | ∫x·eˣ dx = (x²/2)·eˣ; ∫x⁻¹ dx = x⁰/0 | (x − 1)eˣ + C; ln\|x\| + C | MAA7.02 (MAA12.05) | MAA | Limited | orton1983integration † | |
| LSTA-01 | Correlation shows causation | "ice cream sales cause drownings (r = 0,8)" | correlation alone shows association | MAA8.02 (MAB5.03) | MAA, MAB | Moderate | batanero1996intuitive, estepa1996judgments † | |
| LSTA-02 | r ≈ 0 means no relation; r is the slope | parabola-shaped data with r ≈ 0 called unrelated; steeper line ⇒ larger r | r measures linear association only | MAA8.02 (MAB5.03) | MAA, MAB | Moderate | estepa1996judgments † | |
| LSTA-03 | Standard deviation as bumpiness or range | a bar chart with uneven bar heights judged to have the larger SD | SD measures spread around the mean | MAA8.01 (MAB5.02) | MAA, MAB | Moderate | delmas2005exploring | |
| LSTA-04 | Confidence interval read as a probability about the true value | "95 % probability that μ lies in [12,1; 13,4]" | 95 % of intervals built this way contain μ | MAB9.04 | MAB | Strong | hoekstra2014robust, sotos2007students | Adults and researchers; sensitive for lyhyt |
| LPRB-01 | Equiprobability bias | sums 7 and 12 with two dice equally likely | P(7) = 6/36, P(12) = 1/36 | MAA8.04 (MAB5.06) | MAA, MAB | Strong | lecoutre1992cognitive | Grows with instruction |
| LPRB-02 | Confusion of the inverse: P(A\|B) = P(B\|A) | positive test ⇒ 99 % sick when the test is 99 % sensitive | depends on the base rate | MAA8.05 | MAA | Moderate | falk1986conditional †, batanero2005high | Conditional probability † in MAA8 |
| LPRB-03 | Conjunction fallacy | P(A and B) judged larger than P(A) | P(A ∩ B) ≤ P(A) | MAA8.05 (MAB5.06) | MAA, MAB | Strong | tversky1983extensional | |
| LPRB-04 | Representativeness: an "irregular" sequence is more likely | HTHHT more likely than HHHHH | equal, 1/32 each | MAA8.04 (MAB5.06) | MAA, MAB | Strong | kahneman1972subjective †, fischbein1997evolution (*7–9 bib*) | Related to 7–9 PRB-01 |
| LPRB-05 | Independent and mutually exclusive confused | disjoint events with P > 0 called independent | disjoint events with P > 0 are dependent | MAA8.05 | MAA | Limited | † | |
| LPRB-06 | Order handled wrongly in counting | committee of 3 from 10 counted as 10·9·8 | C(10, 3) = 120 | MAA8.03 (MAB5.07) | MAA, MAB | Strong | batanero1997effect | |
| LFIN-01 | Compound interest computed as simple interest | 2 % for 5 years = 10 % | 1,02⁵ − 1 ≈ 10,4 % | MAA9.03 (MAB7.01) | MAA, MAB | Moderate | stango2009exponential | Applied case of LEXP-03 |
| LFIN-02 | Nominal change taken as real change | wage +3 % with inflation 4 % called a rise in purchasing power | 1,03/1,04 ≈ 0,99, a fall of about 1 % | MAB6.02 (MAA9.05) | MAB, MAA | Limited | † | No study found |
| LLOG-01 | Implication confused with its converse | "if n is divisible by 6 it is even" ⇒ "if n is even it is divisible by 6" | the converse needs its own proof | MAA11.02 (MAA3.06) | MAA | Moderate | durandguerrier2003which | |

## 3. Rows from the 1–9 workbook that carry on into lukio

Items in MAY1 especially should reuse these rather than define near-duplicates.

| ID | Misconception | Lukio goals |
|---|---|---|
| ALG-09 | Square of a sum: (a + b)² = a² + b² | MAA2.01, MAB2.07 |
| ALG-11 | Minus sign not distributed | MAA2.01, MAA6.04 |
| NUM-06 | No number between 0,3 and 0,4 (density) | MAY1.01 |
| NUM-07 | Wrong base in reverse percentage | MAY1.03, MAB6.01 |
| NUM-08 | Successive percentage changes | MAY1.03, MAB6.01, MAA9.03 |
| PRO-01, PRO-02 | Linearity illusion for area and volume | MAA3.01, MAB3.01 |
| FUN-01, FUN-02 | Graph as picture; slope–height confusion | MAY1.07, MAA6.03 |
| FUN-04, FUN-05 | Function needs a formula; every linear function is proportional | MAY1.06, MAY1.07, MAB4.01 |
| PRB-01, PRB-02 | Gambler's fallacy; counts instead of proportions | MAA8.04, MAB5.06 |
| EXT-01, EXT-02 | −3² = 9; 2³ = 6, a⁰ = 0, 2⁻¹ = −2 | MAY1.04 |
| EXT-03, EXT-04 | Inequality sign; x² = 9 gives only x = 3 | MAA2.04, MAA2.06 |
| EXT-08 | Median from unsorted data; mean as "typical" | MAA8.01, MAB5.02 |

`EXT-` rows are seeds in the 7–9 backlog (section 3.2), not workbook rows.

## 4. Gaps

- No Finnish item-level error catalogue for lukio turned up. The nearest are the YTL marking notes per exam and three theses on YO answers (Palomäki 2024 on continuity and differentiability; a Helsinki thesis on derivatives in YO exams; a Turku thesis on integration errors).
- Thin or missing evidence: inverse-function and arcsin notation (LFUN-03, LTRI-04), the sine-law ambiguous case (LGEO-01), independence vs disjointness (LPRB-05), real vs nominal change (LFIN-02).
- Not covered yet: MAA10 3D geometry (cross product, planes), MAA11 programming and congruences, MAB9 normal distribution beyond confidence intervals, modelling and software use (B-part skills).
