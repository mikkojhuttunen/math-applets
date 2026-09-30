# Privacy, ethics and legal review briefing: FinnMath for grades 1–6

> **EXPERT REVIEW REQUIRED. NOT LEGAL ADVICE.**
>
> This briefing was drafted by an AI assistant to save experts' time. It has not been reviewed by a data protection officer, a lawyer or a research ethics committee. It lists facts that were checked, questions that experts must decide, and defaults proposed for them to accept, change or reject.
>
> **Do not collect, log or store data about pupils in grades 1–6 (ages about 7–12), and do not send pupil answers, work or messages to any third-party or AI service, until the sign-off in `expert_review_signoff_template.md` has been completed by the named experts.**
>
> *Asiantuntijoiden arvio vaaditaan. Tämä ei ole oikeudellinen neuvo. Oppilastietoja ei kerätä eikä tallenneta ennen kuin tietosuojavastaava, juristi ja tutkimuseettinen toimikunta ovat arvioineet suunnitelman.*

Date: 30 September 2026. Status: draft for expert review. Sign-off: **not reviewed**.

## 1. Who has to act

This is not a task an AI assistant or a project developer can close. The following people must review and decide.

| Role | Decides |
|---|---|
| Data protection officer (DPO) of the controller, for example the university (the project owner appears to be Tampere University; confirm) | Whether a data protection impact assessment (DPIA) is needed, legal basis, retention, processors, data subject rights |
| Legal counsel | GDPR roles (controller, joint controller, processor), EU AI Act classification and duties, contracts with hosting and AI providers |
| Research ethics committee (human sciences) | Whether and how children under 15 may take part, guardian information or consent, child-appropriate information |
| School owner (for example the municipality), if pupils use the app in class | Whether the school may use the service at all, and who is the controller for classroom use |
| Teacher or pedagogy expert | Whether items, feedback and any pupil-facing wording are suitable for ages 7–12 |
| Information security officer | Hosting, access control, logging, incident handling |

## 2. Why grades 1–6 need a separate review

- **All pupils are children under the consent age.** In Finland the age limit for a child's own consent to information society services is 13 (Data Protection Act 1050/2018, section 5). Below that, the custodian's consent or authorisation is needed for such services.
- **The design builds a profile of each child's errors.** The exercise-types document proposes logging every response, tagging misconceptions, tallying rules per pupil, selecting the next item adaptively, and analysing free text and photos. That is evaluation of children's performance, which is what data protection and AI rules treat with most care.
- **Inferences may say more than intended.** A pattern of errors can hint at learning difficulties. Whether such an inference counts as data about health or disability is a legal question, not a technical one.
- **The earlier privacy note assumed older users.** The exercise-types document said "many users will be minors" and pointed to lukio and yläkoulu. Pupils aged 7–12 need a fresh review.

## 3. Facts checked on 30 September 2026

| Topic | What the sources say | Source | How firm |
|---|---|---|---|
| Consent age in Finland | 13. Children below need a custodian's consent for information society services. Counselling and support services are an exception. Consent by the custodian does not lapse automatically when the child reaches the age. | [Data Protection Ombudsman](https://tietosuoja.fi/en/consent-of-the-data-subject) | Official authority page |
| Scope of the age limit | It applies to consent given for information society services offered directly to a child. Whether consent is the right basis for a school or research use is a separate question. | Data Protection Ombudsman, as above; [Linklaters overview](https://www.linklaters.com/en/insights/data-protected/data-protected---finland) | Authority plus law firm summary |
| DPIA | Required before processing that is likely to be high risk (GDPR Article 35). The Data Protection Ombudsman publishes a list of processing that requires one. Guidance describes a rule of thumb: two or more risk criteria usually mean a DPIA, and unclear cases should get one. Evaluation and scoring, including profiling, is one criterion. | [Ombudsman list](https://tietosuoja.fi/luettelo-vaikutustenarviointia-edellyttavista-kasittelytoimista) (not opened in this check; linked from a secondary page), [OPH guidance page](https://www.oph.fi/fi/koulutus-ja-tutkinnot/vaikutustenarvioinnin-toteuttaminen-ja-ennakkokuuleminen) | Secondary description of official guidance |
| Research ethics | A statement from a human sciences ethics committee is required if, among other cases, the research focuses on minors under 15 without separate guardian consent, or without informing guardians in a way that lets them prevent participation. | [TENK](https://tenk.fi/en/ethical-review/ethical-review-human-sciences) | Official guideline page |
| EU AI Act dates | The Digital Omnibus on AI entered into force on 27 July 2026. High-risk obligations for stand-alone Annex III systems, which include education systems that evaluate learning outcomes, apply from 2 December 2027 instead of 2 August 2026. Article 50 transparency duties (telling people they are dealing with an AI system) applied from 2 August 2026. | Law firm and industry analyses, for example [Jones Walker](https://www.joneswalker.com/en/insights/blogs/ai-law-blog/yes-august-2-still-matters-the-eu-approved-a-high-risk-ai-delay-but-most-trans.html?id=102nbon), [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/), [Winston Taylor](https://www.winstontaylor.com/insights/ai-act-rules-on-high-risk-ai-delayed-as-ai-digital-omnibus-agreed) | Secondary sources only. Confirm in the Official Journal. |

Not checked: Finnish education law on pupil records, the Act on Electronic Communications Services (cookies and analytics), and the terms of any hosting or AI provider. Counsel should cover these.

## 4. What the app is planned to process

See `data_inventory_grades1-6.csv` for the full list with a default for each item. In short, from the exercise-types design:

- Answers to exercises: typed entries, chosen options, tapped lines, ordering sequences, graph points.
- Correctness and a misconception tag per answer.
- Timing, hint requests, skips and abandonment.
- Optional "how sure are you" ratings.
- Tutor chat questions, free-text explanations and photos of handwritten work (these are Tier 3 and use a language model).
- Class and cohort statistics for a teacher dashboard.
- Batches of wrong answers sent to a language model for labelling.

## 5. Defaults proposed for a first pilot (for experts to accept, change or reject)

1. **No identity.** No accounts, names, emails or device identifiers. A class code and a random session code per pupil, chosen by the teacher. Re-identification through small classes must still be assessed.
2. **Tier 3 off.** No photos, no free text, no tutor chat, no language model on anything a pupil writes or says. Photos of handwriting can show names; free text can reveal identity. If an AI feature is later added, Article 50 disclosure and a processor agreement are needed first.
3. **Aggregates first.** The teacher sees class-level statistics. Individual pupil views only if the experts approve, and never rankings or labels. Groups below a minimum size chosen by the DPO are suppressed.
4. **Short retention.** Raw responses are deleted after a fixed period chosen by the DPO. Only aggregate statistics are kept.
5. **Purpose separation.** Product improvement and research are separate purposes with separate decisions. Research use needs its own ethics statement.
6. **No decisions about children.** No grades, no placement, no automated decisions. Misconception statistics improve exercises and feedback only. This also matters for the AI Act classification, which counsel must confirm.
7. **Hosting.** Servers in the EU or EEA, with a list of every processor. No third-party analytics or advertising trackers.
8. **Child-friendly information.** A short notice in plain Finnish (and Swedish where needed) for pupils, and information for custodians. A pupil or custodian can decline without any disadvantage.
9. **Teacher in the loop.** Pilot in one class with a teacher who has agreed the use with the school owner.

## 6. Questions for the experts

| # | Question | Who decides |
|---|---|---|
| 1 | Who is the controller? The university, the school owner, both jointly, or the project? Who is the processor? | Legal counsel, DPO |
| 2 | Which legal basis fits classroom use, and which fits research use? Is custodian consent needed, or would another basis be used with custodian information? | DPO, counsel |
| 3 | Does the design need a DPIA before the pilot? Does it need prior consultation with the Data Protection Ombudsman? | DPO |
| 4 | Is a research ethics statement needed? What must guardians and children be told, and how is a child's own agreement handled? | Ethics committee |
| 5 | If pupils are not identified, which data subject rights (access, erasure) can still be met, and how? | DPO |
| 6 | Can a misconception profile reveal something about a learning difficulty, and if so does it fall under special categories of data? | DPO, counsel |
| 7 | Do misconception diagnosis and adaptive item selection count as evaluating learning outcomes under Annex III of the AI Act? Does the tutor chat need an Article 50 disclosure? | Counsel |
| 8 | Which retention period, and which minimum group size for aggregates? | DPO |
| 9 | Which hosting and processors are acceptable? Any transfers outside the EEA? | DPO, security officer |
| 10 | Are cookies or analytics used, and what does the Act on Electronic Communications Services require? | Counsel |
| 11 | What is the incident and breach plan for a service used by children? | Security officer, DPO |
| 12 | Are the items and any feedback wording suitable for ages 7–12, including pupils with reading difficulties? | Teacher, pedagogy expert |
| 13 | Must the pilot exclude pupils whose custodians decline, without disadvantage, and how is that arranged in class? | School owner, ethics committee |

## 7. Gate: what must not happen before sign-off

- No pupil in grades 1–6 uses a version that logs answers with any identifier.
- No pupil-authored content leaves the project's own servers.
- No language model receives pupil input.
- No misconception profile is shown to anyone as a statement about a named child.
- No data about pupils is collected for research.

Developers can continue to build and test with synthetic data. The code in `tools/buggy_rules/` runs without storing anything about pupils, except the optional `Tally` class, which must stay disabled until sign-off.

## 8. Suggested order of work

1. Send this briefing and the data inventory to the DPO. Ask for a screening decision on the DPIA.
2. In parallel, ask counsel the AI Act questions (7) and the roles question (1).
3. Once roles are clear, submit the plan to the ethics committee.
4. Agree the pilot with one teacher and the school owner.
5. Complete `expert_review_signoff_template.md`, with conditions, before any pupil uses the app.
6. Repeat the review when the design changes, for example when Tier 3 features are added.

## 9. Limits of this briefing

- Written by an AI assistant from public sources on 30 September 2026. Laws and guidance change.
- Several sources are law firm and industry summaries, not the legal texts.
- It does not describe the app's actual hosting, code or contracts, because none were provided.
- It does not decide any question in section 6.
