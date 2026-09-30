# How the Laser Physics and Optics bots work, and what a maths bot takes from them

Read on 2026-09-30 from `mikkojhuttunen/Laser_physics_bot` (FYS.501, v1.6.0) and `mikkojhuttunen/FYS240_Optics_TGbot` (FYS.240, v2.8.0). Both are public; this file is a summary, not a copy.

## 1. Architecture shared by both bots

| Part | How it works | Files |
|---|---|---|
| Runtime | Node 18+, `express` webhook server, `axios` for the Telegram Bot API and the Anthropic Messages API. No bot framework. Deployed on Railway. | `bot_fys501.js`, `bot_fys240.js`, `package.json` |
| Webhook | `POST /webhook` checks `WEBHOOK_SECRET`, answers HTTP 200 **before** doing any work, then handles the update. This stopped the Telegram retry storm that once crashed the container. Duplicate `update_id`s are dropped. | `app.post("/webhook")`, `handleUpdate()` |
| Routing | One big `handleUpdate()`: a chain of regexes on the message text (`/start`, `/help`, `/HW3.2`, `/quiz 2.3`, `/define ...`, free-text "quiz me"). Button taps arrive as `callback_query` and go to `handleCallbackQuery()`, routed by a `callback_data` prefix (`quizchapter:`, `mv:`). | same |
| Deterministic features | Lecture/video lists, `/weekN`, glossary `/define`, homework overviews, quiz grading. No Claude call, free for everyone. | `lectureLinks_*.js`, `corpusLoader*.js`, `terminology*.json`, `homework_problems*.json` |
| AI features | Free-text Q&A, homework hints, photo work-check. The whole course text (`course_corpus*.txt`, 0.3 MB) goes in the system prompt with `cache_control` (1 h TTL), so repeat questions cost about 5 % of the first. Model `claude-haiku-4-5` by default, `max_tokens` 900, 6-turn history per chat, 3 retries on 429/5xx. Prompt rules: short answers, hints not solutions, plain Unicode maths (a `latexToUnicode()` pass cleans up stray LaTeX). | `askClaude()`, `TA_INSTRUCTIONS`, `buildSystemBlocks()` |
| Quizzes | Bank first: questions are drawn from a reviewed JSON bank (`quizBank_*.json`, keyed chapter → section). Only when the bank runs short is Claude asked to generate more, from that section's corpus excerpt, as structured JSON. Grading is always in code. Generated questions go to a **pending** file for human review and are merged into the bank with `mergePending_*.js`; they are never served from pending. Single-answer quiz uses an inline keyboard; a separate multi-select ("valitse kaikki oikeat") add-on has its own bank, sessions and `mv:` callback namespace. Sessions are in-memory Maps with expiry. | `quizGenerator_*.js`, `multivalueQuizGenerator_*.js`, `pendingStore_fys240.js`, `pendingAdmin_*.js`, `mergePending_*.js` |
| Access and cost | Everything deterministic is open. AI actions need membership of a private course channel (`COURSE_CHANNEL_ID`, checked with `getChatMember`, cached 5 min) and cost credits from a per-student daily allowance (`STUDENT_LLM_DAILY_USAGE`, default 10), under a shared daily euro backstop (`DAILY_BACKSTOP_EUR`). Admins (`ADMIN_USER_IDS`) are exempt. State is in memory, so it resets on redeploy; the Anthropic Console limit is the hard stop. | `membership.js`, `usageLimiter.js`, `accessGuard.js` |
| Analytics (laser bot only, off by default) | One pseudonymous event per graded answer (keyed hash of the Telegram id, date only), `/privacy`, `/optout`, admin `/quizstats` briefing with small-group suppression. Questions can carry `concepts` and per-option `optionTags` = misconception ids. | `quizAnalytics_fys501.js`, `quizStats_fys501.js`, `misconceptions_fys501.json`, `concepts_fys501.json` |
| Diagnostics | `/healthz` (JSON: version, data health, counts), `/source_materials`, `/source_quizzes`, and course-mismatch guards that refuse to serve data that looks like the other course. | `bot_*.js` |
| Languages | Optics bot is bilingual EN/FI: language detected from the Telegram client or the text, Finnish mirror questions (`_fi` ids), Finnish-only commands (`/luennot`, `/viikkoN`, `/moquiz`). | `bot_fys240.js` |
| Versioning | `BOT_VERSION` plus a CHANGELOG block in the bot file header; shown in `/healthz` and the startup log. | header comments |

## 2. What works well and should be kept

1. Acknowledge the webhook first, then work.
2. Bank first, AI as fallback, grading in code, AI output reviewed by a human before it enters the bank.
3. Open deterministic layer, gated and metered AI layer.
4. Misconception ids on wrong options, which is exactly what the math-applets exercise pipelines already produce (`misconceptions: {"NUM-10a": {"answer": "836"}}`).
5. `/healthz` and a version number you can check on the live deployment.

## 3. What to do differently

1. **Modules from day one.** `bot_fys240.js` is 128 KB with routing, prompts, formatting and reports in one file, and both repos carry duplicate or deprecated copies (`scripts/clean.js` vs `clean_fys240.js`, `*_deprecated.js`, `*_bug_dontrun.js`, `.patch` files). The maths bot gets small modules and one copy of each.
2. **Tests that run offline**, in the repo, before every commit (the bots have `e2e_*_test.js`, but not as one command).
3. **Read the content straight from this repo** instead of copying it: applet list from `index.html`, curriculum goals from the OPS files, exercises from the two pipelines' JSON. The bot then updates when `main` updates.
4. **Finnish only** for users, so no language detection.
5. **Pupils are minors.** The course bots serve university students. Here, audience, age limits and data handling must be decided before any feature that stores anything or calls an AI (see `BACKLOG_BOT.md`, decisions D1-D2, and `math-misconceptions/grades1-6/EXPERT_REVIEW_REQUIRED.md`).

## 4. Material in this repo the bot can use (2026-09-30)

| Material | Where | State |
|---|---|---|
| Applets | `index.html` (links), `INDEX.md`, `luokat-1-6/`, `yla-aste-7-9/`, `lukio-pitka/`, `lukio-lyhyt/`; published at `https://mikkojhuttunen.github.io/math-applets/` | About 20 applets, 1 for grades 1-6 |
| Curriculum goals 1-6 | `math-misconceptions/grades1-6/data/curriculum/OPS_1-6_oppimistavoitteet.md` | Stable ids such as `A36.S2.04` |
| Curriculum goals 7-9 | `math-applets/math/OPS_7-9_oppimistavoitteet.md` | S1-S6 ids |
| Exercises 1-6 | `math-misconceptions/grades1-6/exercises/grades1-6/batch-*.json` | 40 items, all `draft`, all three-digit subtraction (`A36.S2.04`, `NUM-10`) |
| Exercises 7-9 | `math-misconceptions/exercises/`, built to `build/bank.json` by `scripts/build_bank.py` (flags `text_only`, `telegram_poll`) | Empty so far (routine has not run) |
| Misconception catalogue | `math-misconceptions/sources/math_misconceptions_item_bank.xlsx` (sheet `Misconceptions`), sub-variants such as `NUM-10a` in `math-misconceptions/grades1-6/tools/buggy_rules/buggy_rules.py` | 42 misconceptions for grades 1-9, descriptions in English |

So a quiz feature has almost nothing reviewed to serve yet. The first bot versions should build the engine against the draft items (visible to admins only) and grow as the pipelines produce reviewed content.
