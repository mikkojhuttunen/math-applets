# Finnish Upper Secondary Mathematics (lukio): Curriculum and Misconceptions

1 October 2026. Research summary that starts the lukio exercise pipeline; counterpart of `../../grades1-6/docs/finnmath_grades1-6_curriculum_and_misconceptions.md`.

## What the repository already had

The repository had no lukio curriculum description and no lukio misconceptions.

| File | Scope | Lukio relevance |
| --- | --- | --- |
| `math-applets/math/OPS_7-9_oppimistavoitteet.md` | Grades 7–9 goals T1–T20, S1–S6 | MAY1 revisits S2–S4; nothing beyond grade 9 |
| `grades1-6/data/curriculum/OPS_1-6_oppimistavoitteet.md` | Grades 1–6 | None |
| `sources/math_misconceptions_item_bank.xlsx` | 42 rows, grades 1–9 | About a dozen rows carry on into MAY1 and MAA2 (powers, brackets, percentages, linearity, graphs, chance) |
| `sources/math_misconceptions_grades7-9.bib` | 85 references | Five reusable: Vinner & Dreyfus (function), Matz and De Bock (linearity), Merenluoto & Lehtinen (real numbers and limits, Finnish data), Fischbein & Schnarch (probability) |
| `lukio-pitka/`, `lukio-lyhyt/` | 11 applets | Five follow `APPLET_SPEC.md` (parabola, unit circle, exp/log, derivative, Riemann sum); they cover MAA2, MAA5, MAA6 and MAA7 |
| `BACKLOG.md` | Applet queue | Lukio applets have the level field "lukio pitkä / lukio lyhyt" but no curriculum IDs |

## 1. National curriculum (Opetushallitus)

The national curriculum for upper secondary school is **Lukion opetussuunnitelman perusteet 2019** (LOPS 2019, regulation OPH-2263-2019). It has been in force since 1 August 2021, so schools call their local versions "LOPS2021". Mathematics is section 6.6.

| Source | What it gives | Use |
| --- | --- | --- |
| [ePerusteet: LOPS 2019, matematiikka](https://eperusteet.opintopolku.fi/#/2270454/lukiokoulutus/6828810/oppiaine/6831746) | Official digital text: subject goals, module goals and core contents, assessment | Authoritative wording; structured import later |
| OPH: [LOPS 2019 PDF](https://www.oph.fi/sites/default/files/documents/lukion_opetussuunnitelman_perusteet_2019.pdf) | Whole curriculum | Same text as ePerusteet |
| OPH: [Lyhyen matematiikan tukimateriaali](https://www.oph.fi/sites/default/files/documents/lops2019_mab.pdf); MAOL: [pitkän matematiikan tukimateriaali](https://maol.fi/app/uploads/2020/01/LOPS2019_MAA_MAOL.pdf) | Guidance on how to teach each module | Module interpretation, example tasks |
| YTL: hyvän vastauksen piirteet, e.g. [spring 2026 pitkä](https://tiedostot.ylioppilastutkinto.fi/kokeet/2026-03-18_M_fi/grading-instructions.html), [spring 2025](https://tiedostot.ylioppilastutkinto.fi/kokeet/2025-03-19_N_fi/grading-instructions.html) | Marking notes for every matriculation exam task | De facto difficulty levels; typical errors |
| School LOPS2021 pages, e.g. [Laukaa MAA](https://peda.net/laukaa/lukio/opiskelijoille/oppiaineiden-sivut-lops2021/MAA), [Laukaa MAB](https://peda.net/laukaa/lukio/opiskelijoille/oppiaineiden-sivut-lops2021/MAB), [Tampere](https://www.tampere.fi/tampereen-teknillinen-lukio/opiskelijalle/opetussuunnitelma-ja-opintojaksojen-kuvaukset-lops2021/matematiikan-pitka-oppimaara), [TNK](https://sites.utu.fi/lops2021tnk/fi/oppiaineet/matematiikka/) | National module text repeated, plus the local course split | Second-hand copy of the national text |

**Limit of this session.** The cloud environment's network policy blocked oph.fi, eperusteet.opintopolku.fi, peda.net and ylioppilastutkinto.fi, so no page was read in full. The module structure and credits were confirmed from several independent search results and match the national hour allocation (lyhyt 12 op, pitkä 20 op compulsory). The core contents are condensed from search excerpts; uncertain placements are marked † in the curriculum file. To check the wording, either allow those hosts in the environment's network settings or read ePerusteet yourself.

### Structure

| | Lyhyt (MAB) | Pitkä (MAA) |
| --- | --- | --- |
| Common module | MAY1 Luvut ja yhtälöt, 2 op | MAY1 Luvut ja yhtälöt, 2 op |
| Compulsory | MAB2 Lausekkeet ja yhtälöt 2, MAB3 Geometria 2, MAB4 Matemaattisia malleja 2, MAB5 Tilastot ja todennäköisyys 2, MAB6 Talousmatematiikka I 1, MAB7 Talousmatematiikka II 1 | MAA2 Funktiot ja yhtälöt 1 3, MAA3 Geometria 2, MAA4 Analyyttinen geometria ja vektorit 3, MAA5 Funktiot ja yhtälöt 2 2, MAA6 Derivaatta 3, MAA7 Integraalilaskenta 2, MAA8 Tilastot ja todennäköisyys 2, MAA9 Talousmatematiikka 1 |
| Compulsory total | 12 op | 20 op |
| National optional | MAB8 Matemaattinen analyysi 2, MAB9 Tilastolliset ja todennäköisyysjakaumat 2 | MAA10 3D-geometria 2, MAA11 Algoritmit ja lukuteoria 2, MAA12 Analyysi ja jatkuva jakauma 2 |

How it differs from the grades 1–9 files:

- No numbered T-goals and no S content areas. Each module has its own goals and core contents. Goal IDs are therefore built from the module code (`MAA6.06`), and the subject's general goals are numbered G1–G8 for this project.
- No national grade criteria were found for lukio mathematics (grades 4–10 per module). The matriculation exam sets the practical standard, so the P/T/H/K levels are tied to its A part (no CAS) and B part (CAS allowed).
- Complex numbers are not in the national modules; the existing `complex-plane-explorer.html` applet maps to no goal.

Full goal list with IDs: `../data/curriculum/LOPS_2019_matematiikka_oppimistavoitteet.md`.

## 1b. Documentation on misconceptions and difficult topics

**Short answer: no ready-made Finnish catalogue exists, but the research base is larger than for grades 1–6.** Most of it is international and comes from first-year university calculus and statistics courses, so it applies to MAA6–MAA8 and MAB5/MAB9 with care. The Finnish sources are matriculation exam marking notes and a few theses and dissertations.

| Area (modules) | Best-documented difficulty | Key sources | Finnish source |
| --- | --- | --- | --- |
| Limits and continuity (MAA6, MAA12) | Limit as an unreachable bound; 0,999… < 1; continuity as "no pen lift" | Tall & Vinner 1981; Williams 1991; Cornu 1991 | Palomäki 2024 (YO answers 2020–2022); Merenluoto & Lehtinen 2004 |
| Derivative (MAA6, MAB8) | f′ graph read as f; chain rule omitted; f′ = 0 taken as an extremum | Asiala et al. 1997; Orton 1983; Clark et al. 1997 | Hähkiöniemi 2006; Viholainen 2008; Helsinki thesis on derivatives in YO exams |
| Integral (MAA7) | Integral = area always; constant of integration omitted | Orton 1983 | Kuningas (Turku thesis) |
| Function concept (MAY1, MAA12) | Function must be one formula; linearity overgeneralised | Vinner & Dreyfus 1989; Breidenbach et al. 1992; Matz 1982 | – |
| Equations and inequalities (MAA2, MAA4) | Dividing by x loses a root; zero-product rule misused; absolute value | Vaiyavutjamai & Clements 2006; Tsamir & Bazzini; Almog & Ilany 2012 | YTL marking notes |
| Exponentials and logarithms (MAA5, MAB4, MAA9) | log(a + b) = log a + log b; exponential growth judged linear | Kenney & Kastberg 2013; Weber 2002; Wagenaar & Sagaria 1975; Stango & Zinman 2009 | – |
| Trigonometry (MAA5) | One solution only; radian not a measure | Weber 2005; Moore 2014; Akkoç 2008 | – |
| Vectors (MAA4) | \|a + b\| = \|a\| + \|b\|; vector tied to position | Nguyen & Meltzer 2003 (n = 2 031); Barniol & Zavala 2014 | – |
| Statistics (MAA8, MAB5, MAB9) | Correlation as causation; SD as bumpiness; confidence interval as probability | Batanero et al. 1996; delMas & Liu 2005; Hoekstra et al. 2014 | – |
| Probability (MAA8, MAB5) | Equiprobability; conjunction fallacy; P(A\|B) = P(B\|A); counting order | Lecoutre 1992; Tversky & Kahneman 1983; Batanero et al. 1997 | – |

The catalogue with 45 lukio rows (IDs `LFUN-01` … `LLOG-01`), typical wrong answers, goals and evidence ratings is in `../data/misconceptions/lukio_misconceptions.md`. The bibliography is in `../data/misconceptions/math_misconceptions_lukio.bib`.

**Caveats.**

- **Evidence not checked.** Ratings are a first pass from search results and memory, and several DOIs are unverified. The grades 1–6 work found that a self-published review had wrong citations. Repeat that kind of check before a topic is generated in bulk.
- **University samples.** Many calculus and statistics studies used first-year university students. The errors are the same ones Finnish YO marking notes describe, but frequencies do not transfer.
- **YTL marking notes are the best Finnish source** and are public for every exam since the digital exam began. A systematic pass through them (A-part tasks, both syllabi, 2019–2026) would give a Finnish, item-level list of errors. That is backlog task L-R01.

## Privacy

Lukio students are mostly 16–19. In Finland the age limit for a child's own consent to information society services is 13, so the custodian-consent question that blocks grades 1–6 does not arise in the same form. Logging answers of named students is still personal data processing under GDPR, and AI tutoring in education may fall under the EU AI Act's high-risk category. The exercise pipeline itself uses no student data. Any data collection needs the same kind of review as `../../grades1-6/EXPERT_REVIEW_REQUIRED.md` before use with students. This is not legal advice.

## Next steps

1. **Done: curriculum file.** LOPS 2019 modules with IDs, levels and a proposed year split.
2. **Done: misconception catalogue, draft.** 45 lukio rows plus 18 rows carried over from the 1–9 workbook and the 7–9 seeds.
3. **Proposed: backlog and framework.** `../BACKLOG_LUKIO.md`, which starts with the tooling the routine needs.
4. **To do: verify the curriculum wording** against ePerusteet (task L-R02).
5. **To do: evidence check** of the catalogue and a pass through YTL marking notes (L-R01, L-R03).
