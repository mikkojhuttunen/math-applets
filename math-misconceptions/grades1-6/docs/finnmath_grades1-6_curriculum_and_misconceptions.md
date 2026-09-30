# Finnish Math Curriculum and Misconceptions, Grades 1–6

30 September 2026. Condensed Markdown copy of the working document; the living version is a Claude document.

**EXPERT REVIEW REQUIRED.** This document is a research summary, not legal advice. Before any data about pupils in grades 1–6 is collected, logged or sent to a third-party or AI service, a data protection officer, legal counsel and a research ethics committee must review and decide (see the privacy section below and `../EXPERT_REVIEW_REQUIRED.md`).

## What the project files contain

The project files contain no curriculum description for grades 1–6; every file is scoped to grades 7–9.

| File | Scope | Grades 1–6 relevance |
| --- | --- | --- |
| OPS_7-9_oppimistavoitteet.md | Objectives T1–T20, content areas S1–S6, 61 atomic goals (IDs like S3.05), grade-band criteria 5/7/8/9, applet gaps | None. Its own header says it covers vuosiluokat 7–9 only. |
| math_misconceptions_item_bank.xlsx | 33 misconceptions, item template, sources sheet ("grades 7–9") | Indirect. The equal-sign and fraction/decimal entries have primary roots, but none were mapped to grades 1–6 at the time. |
| math_misconceptions_grades7-9.bib | 85 references, mostly algebra, rational numbers, geometry, graphs | Partial. A dozen sources concern decimals, fractions, natural number bias, division and angle, which are built in grades 1–6. |
| FinnMath_Exercise_Types_and_Learning_Analysis.docx | Exercise types, logging, analysis design, Grade 7 examples | Design only. Reusable for lower grades, but no content. |

The 7–9 file is detailed (per-goal IDs, grade proposals, assessment criteria). For grades 1–6 there was nothing to match it, so a parallel file was built from the sources below (`data/curriculum/OPS_1-6_oppimistavoitteet.md`).

## Open national sources (Opetushallitus)

The national curriculum for grades 1–6 is openly published by OPH as the 2014 core curriculum (POPS 2014, still the basis, with later amendments). The best machine-readable source is the ePerusteet service, which the tavoitteet.fi tool reads through public APIs.

| Source | What it gives | Use for FinnMath |
| --- | --- | --- |
| [POPS 2014 full PDF (OPH 2014:96)](https://www.oph.fi/sites/default/files/documents/perusopetuksen_opetussuunnitelman_perusteet_2014.pdf) | Whole curriculum. Grades 3–6 mathematics is section 14.4.4 (pp. 234–238 by the PDF's contents list); grades 1–2 is section 13.4.4 | Authoritative wording of objectives (T) and content areas (S) |
| [OPH: Perusopetuksen opetussuunnitelman perusteet](https://www.oph.fi/fi/koulutus-ja-tutkinnot/perusopetuksen-opetussuunnitelman-perusteet) | Landing page with amendments (e.g. 2019 A1 languages grades 1–2, 2023 grade-6 criteria, 2024 B1 languages) | Check for the current amendment status |
| [OPH: 6. vuosiluokan lukuvuosiarviointi](https://www.oph.fi/fi/koulutus-ja-tutkinnot/6-vuosiluokan-lukuvuosiarviointi) | National year-end criteria for grade 6, in force from 1.8.2023, first applied spring 2024 | Difficulty levels (5/7/8/9) for grades 3–6 |
| [Matematiikka, kriteerit (6. lk), PDF](https://www.oph.fi/sites/default/files/documents/Matematiikka%2C%20kriteerit%20%286.%20lk%29.pdf) | Table of objectives T1–T14 for grades 3–6, with grade 5/7/8/9 descriptions | Direct counterpart to the 7–9 criteria table |
| [ePerusteet (Opintopolku)](https://eperusteet.opintopolku.fi/#/fi/perusopetus/419550/tiedot) | Official digital curriculum, public API | Structured import of T and S items |
| tavoitteet.fi: [grades 1–2](https://www.tavoitteet.fi/fi/opetussuunnitelman-perusteet/vuosiluokat-1-2/matematiikka/) and [grades 3–6](https://www.tavoitteet.fi/fi/opetussuunnitelman-perusteet/vuosiluokat-3-6/matematiikka/) | Browsable view of the national text, run by Digivoima Oy, not OPH | Quick reading; verify against OPH PDF |

The national text does not assign content to single grades inside 1–2 and 3–6; municipalities do that locally. Reuse licences for these documents were not checked.

## Curriculum structure, grades 1–6

Grades 1–2 have objectives T1–T12 and four content areas; grades 3–6 have T1–T14 and five. Both are lighter than the 7–9 block (T1–T20, S1–S6).

| Block | Content areas (S) |
| --- | --- |
| Grades 1–2 | S1 thinking skills, S2 numbers and operations, S3 geometry and measuring, S4 data and statistics |
| Grades 3–6 | S1 thinking skills (incl. graphical programming), S2 numbers and operations, S3 algebra, S4 geometry and measuring, S5 data, statistics and probability |

The full objective lists, atomic goals with IDs, grade-6 criteria and the local grade split are in `data/curriculum/OPS_1-6_oppimistavoitteet.md`.

## Typical misconceptions, grades 1–6

The best-documented misconceptions in grades 1–6 cluster around four ideas: place value, the equal sign, whole-number thinking applied to fractions and decimals, and operation models that break when numbers stop being whole. Geometry and measurement have fewer robust studies; statistics and probability are not covered here.

| Topic (grades) | Misconception | Typical wrong response | Sources |
| --- | --- | --- | --- |
| Place value (1–3) | Two-digit numbers are read as two separate single digits, not tens and ones | Digits handled as single digits side by side; errors in regrouping | [Fuson et al. 1997, JRME 28(2)](https://nctm.org/Publications/journal-for-research-in-mathematics-education/1997/Vol28/Issue2/Children_s-Conceptual-Structures-for-Multidigit-Numbers-and-Methods-of-Multidigit-Addition-and-Subtraction) |
| Written subtraction (2–4) | Smaller digit is always subtracted from larger, whatever its position | 453 − 127 = 334 (correct 326) | [Vermeulen et al. 2020](https://doi.org/10.3389/feduc.2020.537531); Brown & VanLehn 1980 |
| Equal sign (1–6) | "=" means "calculate the answer" and belongs at the end | 8 + 4 = □ + 5 answered 12 or 17 (correct 7) | McNeil & Alibali 2005, Child Development 76:883–899; Kieran 1981; Knuth et al. 2006 |
| Multiplication (2–5) | Multiplication is only repeated addition of equal groups | Repeated-addition model applied to every multiplication problem | [Mulligan & Mitchelmore 1997, JRME 28(3)](https://nctm.org/Publications/journal-for-research-in-mathematics-education/1997/Vol28/Issue3/jrme1997-05-309a_pdf); Fischbein et al. 1985, JRME 16(1) |
| Multiplication and division (4–6) | Multiplication always enlarges, division always reduces; the dividend must exceed the divisor | 6 ÷ 0,5 answered 3 (correct 12) | Fischbein et al. 1985; [Giberti & Maffia 2022](https://doi.org/10.1163/26670127-bja10007) (replication, grade 7) |
| Fractions (3–6) | Whole-number thinking: a larger denominator means a larger fraction | 1/8 > 1/4 | [Ni & Zhou 2005](https://doi.org/10.1207/s15326985ep4001_3); [Siegler & Lortie-Forgues 2015](https://doi.org/10.1037/edu0000025); [Van Hoof et al. 2015](https://doi.org/10.1007/s10649-015-9613-3) |
| Fraction addition (4–6) | Add numerators and add denominators | 1/2 + 1/3 = 2/5 | Same; also [Van Hoof et al. 2025](https://doi.org/10.5964/jnc.14075) |
| Decimals (4–6) | Longer decimal is larger, or shorter decimal is larger | 0,123 > 0,5; 0,25 > 0,3 | Stacey et al. 2001, J. Math. Behavior 20(2):207–227 (grades 5–10); Steinle & Stacey 2004 |
| Negative numbers (5–6) | The minus sign has one meaning only (subtraction) | Difficulty reading −3 as a number | [Vlassis 2004](https://doi.org/10.1016/j.learninstruc.2004.06.012) |
| Quadrilaterals (3–6) | Shapes are judged by a prototype and orientation; a square is not a rectangle | Rotated square called a diamond, not a square | [Heinze 2002](https://doi.org/10.1007/BF02655704); [Fujita & Jones 2007](https://doi.org/10.1080/14794800008520167); [Fujita 2012](https://doi.org/10.1016/j.jmathb.2011.08.003) |
| Angle (2–6) | The drawn arms are confused with the amount of opening | Longer arms mean larger angle | Mitchelmore & White 2000, Educ. Studies in Math. 41 |
| Area (1–5) | Covering is not seen as rows and columns; formula learned before the covering idea | Counts squares one by one; area and perimeter mixed | [Outhred & Mitchelmore 2000](https://doi.org/10.2307/749749) (grades 1–4); [Awawdeh Shahbari 2021](https://doi.org/10.3390/math9141672) |

Example responses in the third column are illustrative, not quoted from the studies. The item bank (`data/misconceptions/math_misconceptions_item_bank.xlsx`) holds the evidence rating and sources for each row.

**Persistence.** McNeil and Alibali found that success on equal-sign problems fell between ages 7 and 9 and recovered by 11 in US samples, which they attribute to arithmetic practice reinforcing the "answer follows" pattern. They report that this did not appear in a Chinese sample, so the pattern depends on how arithmetic is taught.

**Finnish context.** Merenluoto and Lehtinen studied conceptual change in the number concept with [Finnish students](https://doi.org/10.1016/j.learninstruc.2004.06.016), and McMullen and colleagues modelled [rational number development](https://doi.org/10.1016/j.learninstruc.2013.12.004). The University of Helsinki [Murtoraketti study](https://www.helsinki.fi/fi/tutkimusryhmat/matemaattiset-oppimisvaikeudet/projektit/murtoraketti-interventiotutkimus) tests virtual versus concrete tools for fractions and decimals in grades 4–5. No Finnish item-level error catalogue for grades 1–6 turned up in the searches.

## Evidence check (30 September 2026)

Tracing the † rows to primary studies raised one row, reworded one, and found no study for a third. The 2025 Hansen review should not be used as a source.

| Item bank row | Before | After | Why |
| --- | --- | --- | --- |
| NUM-10, smaller digit from larger | Limited (recalled) | Moderate | [Vermeulen et al. 2020](https://doi.org/10.3389/feduc.2020.537531) (264 Dutch third-graders) describe it, with three variants, and cite earlier studies calling it frequent. Item changed from 302 − 148 to 453 − 127: a subtrahend ending in 8 invites compensation strategies. |
| GEO-03, angle read from arm length | Limited | Limited, reworded | [Mitchelmore & White 2000](https://link.springer.com/article/10.1023/A:1003927811079) (192 children, grades 2–8) show that finding the two arms is the main difficulty. Arm length as a distractor appears only as a classroom episode in a [grade 3–4 teaching study](https://files.eric.ed.gov/fulltext/ED501155.pdf). |
| MEA-02, area units with the linear factor | Limited (title only) | Limited, no study | [Tan Sisman & Aksu 2016](https://doi.org/10.1007/s10763-015-9642-5) (445 sixth graders) document other errors. The unit error appears only in practitioner guides. |
| MEA-01, area as a sum of sides | Moderate | Moderate, stronger | The same 2016 study shows "area = length + width" among student errors. |
| NUM-03, fraction addition | Strong | Strong, Finnish source added | [Van Hoof et al. 2025](https://doi.org/10.5964/jnc.14075) (University of Turku) use 1/4 + 1/3 = 2/7 as the natural-number-bias answer. |
| NUM-13, "add a zero" for × 10 (new) | none | Moderate | [Hurst & Hurrell 2020](https://researchonline.nd.edu.au/edu_article/247): 530 children aged 10–11; most explanations were "a zero is added". |

**Hansen review.** It is self-published (Summit Institute), calls itself systematic but gives no search method, and has citation errors that could be confirmed. It attributes "A holistic investigation of fraction learning" to McMullen et al. in *Cognition and Instruction*; the paper is [Xu et al. 2024](https://pure.qub.ac.uk/en/publications/a-holistic-investigation-of-fraction-learning-examining-the-hiera/) in *Journal of Cognitive Psychology*, on Northern Irish pupils. It gives Hurst & Hurrell as issue 15(2); it is 15(3). It contains an arithmetic slip ("5.75 instead of 5.75"). Its headline prevalence figures rest on small or untraceable samples: 53.91 % is 23 pupils from a 2017 IOP Publishing paper, and 55 % comes from a 1994 report cited without a venue.

Use it only as an index of topics. Confirmed against primary sources: the equal-sign pattern, "add a zero", the fraction whole-number bias, and the multi-digit subtraction error. Not traced: zero read as "nothing" (305 written as 35), rounding always up, and the keyword strategy for word problems.

## Privacy and ethics review, grades 1–6 (task 6)

**This must be reviewed and decided by qualified people.** The draft briefing lists the questions for them; it does not answer them. Needed: the university data protection officer, legal counsel (GDPR and the EU AI Act), a research ethics committee, and the school owner if pupils use the app in class.

| Fact checked 30 September 2026 | Consequence to put to the experts |
| --- | --- |
| In Finland a child needs a custodian's consent for information society services below age 13 ([Data Protection Ombudsman](https://tietosuoja.fi/en/consent-of-the-data-subject)) | Every grade 1–6 pupil is a child under this rule. Whether consent is the right legal basis for a school or research use is an expert call. |
| A data protection impact assessment (GDPR Art. 35) is due before processing that likely poses high risk; a Finnish [list of such processing](https://tietosuoja.fi/luettelo-vaikutustenarviointia-edellyttavista-kasittelytoimista) and the two-criteria rule apply | Scoring and profiling children's answers probably qualifies. The DPO decides. |
| The [TENK guidelines](https://tenk.fi/en/ethical-review/ethical-review-human-sciences) require an ethics statement when research focuses on minors under 15 without separate guardian consent or without informing guardians so they can prevent participation | The plan needs guardian information or consent, or a committee statement. |
| The EU AI Act's Digital Omnibus entered into force on 27 July 2026 (secondary sources). Education AI that evaluates learning outcomes is high-risk from 2 December 2027; chatbot disclosure under Article 50 applies from 2 August 2026 | The tutor chat needs an AI disclosure now. Whether misconception diagnosis counts as evaluating learning outcomes is a legal classification to confirm in the Official Journal. |

**Defaults proposed for the pilot, pending review:** no accounts, names or emails; no photos, free text, tutor chat or AI calls on pupil input for grades 1–6; class-level statistics by default with small groups suppressed; fixed deletion of raw responses; no labels or ranking of pupils; EU/EEA hosting.

Repository files: `docs/privacy/grades1-6_privacy_review_briefing.md`, `data_inventory_grades1-6.csv` and `expert_review_signoff_template.md`. Sign-off status: not reviewed.

## Next steps for FinnMath

Grades 1–6 (alakoulu) can reuse the 7–9 design, but the curriculum file and the item bank both needed a lower-grade counterpart first.

1. **Done: curriculum file.** OPS_1-6 file with T1–T12 (grades 1–2) and T1–T14 (grades 3–6), atomic goals with stable IDs and the grade 5/7/8/9 criteria.
2. **Done: local grade split.** Luumäki (grades 3–6) and TNK (grades 1–2), labelled as local.
3. **Done: item bank.** Primary rows added to the misconception workbook.
4. **Done: exercise types.** Buggy-rule generators, classifier and error spotting in `tools/buggy_rules/`.
5. **Done: evidence check.** † rows and the Hansen checklist traced to primary studies.
6. **Drafted for expert review: younger users.** Privacy and ethics briefing in `docs/privacy/`. The review and every decision belong to the experts.

Not covered here: statistics and probability in grades 3–6 (T13), programming (T14), and any Finnish classroom-based error data.
