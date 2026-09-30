# Maths Telegram bot: backlog

Work queue for a Telegram bot that serves the material in this repo (applets, curriculum goals, exercises) in Finnish. Design background: `BOT_ANALYSIS.md`.

## How to use this file

- Take the lowest-numbered task whose state is `todo` and whose `Needs` are all `done`. Do one task per session.
- States: `todo` → `in progress` → `done`. Decisions (`D`) are made by the teacher; Claude only sets them to `proposed` with a recommendation.
- When a task is finished: fill `Done`, `Notes` (what was built, how it was tested), run the checks in "Definition of done", commit with a message like `Botti B03: /appletit-komento`.
- The bot code lives only in `telegram-bot/`. It reads other pipelines' files but never edits them.

## Definition of done (every B task)

1. `cd telegram-bot && npm test` passes with no network access (`node --test` finds `test/*.test.js`).
2. `node bot.js` starts without `TELEGRAM_TOKEN` in a dry-run mode and `GET /healthz` answers.
3. User-facing text is Finnish, numbers use a decimal comma and U+2212 minus.
4. Nothing about pupils is stored or logged beyond what the decisions allow.
5. `CHANGELOG.md` in this folder has a line for the new version.

## Decisions

### D1 Audience and age
- State: done (2026-09-30)
- Decision: no minors use AI products directly. AI only helps prepare the materials (exercises, applets) that minors are given, and a teacher reviews them first. The bot users are teachers and upper-secondary students; younger pupils get the material through their teacher.
- Question: who talks to the bot? Teachers only, upper secondary (lukio), grades 7-9, grades 1-6?
- Why it matters: pupils are minors. Telegram's terms set a minimum age for users, the Anthropic usage policy has extra requirements for products used by minors, and `math-misconceptions/grades1-6/EXPERT_REVIEW_REQUIRED.md` forbids pupil data for grades 1-6 until a reviewer signs off. Check the current terms of both before choosing.
- Recommendation: v1 for **teachers** (browse applets, curriculum goals, preview and review exercises) and **lukio students**. Grades 1-9 content reaches pupils through the teacher (shared applet links, exercises shown in class), not through pupils' own Telegram accounts.

### D2 AI layer
- State: done (2026-09-30)
- Decision: the bot makes no AI calls. Everything it does is deterministic code over reviewed content in this repo.
- Question: does v1 call Claude at all?
- Recommendation: **no**. v1 is fully deterministic (links, goal lookup, bank quizzes graded in code), so it costs nothing to run and stores nothing. Add Claude later (B20-B22) only for the audience D1 allows, with the laser/optics access and credit model.

### D3 Where the code lives and how it is hosted
- State: done (2026-09-30)
- Decision: `telegram-bot/` in this repo.
- Recommendation: this folder (`telegram-bot/`) in this repo, so the bot reads the content directly; deploy on Railway like the course bots, with Railway's root directory set to `telegram-bot/`. Move to a separate repo later only if the bot needs its own release cycle.

### D4 Bot identity
- State: todo
- Question: bot name and @username (BotFather), and whether a teachers' channel gates admin commands.

## Tasks

### B01 Project skeleton
- State: done
- Needs: D3
- What: `package.json` (Node 18+, no dependencies: built-in `http` server and `fetch`, no bot framework), `bot.js` with `POST /webhook` (secret check, immediate HTTP 200, `update_id` dedupe), `GET /`, `GET /healthz` (version, uptime), `tg()` helper, `/start` and `/apua` in Finnish, `BOT_VERSION`, `CHANGELOG.md`, `.gitignore`, `README.md` with local run steps. Dry-run mode without a token prints outgoing messages instead of sending them.
- Test: `test/` with Node's built-in `node:test`; feed fake updates to `handleUpdate()` and assert on captured outgoing calls.
- Done: 2026-09-30, v0.1.0
- Notes: no npm dependencies (built-in `http` and `fetch` instead of express and axios). Modules `src/config.js`, `src/server.js`, `src/telegram.js`, `src/handlers.js`, `src/texts.js`. In groups the bot answers only commands, and ignores `/cmd@otherbot`; in private chats free text and unknown commands point to `/apua`. Errors in handling are logged, never thrown. Start-up warns if a token is set without `WEBHOOK_SECRET`. 15 tests: command parsing, help replies, dedupe, group rules, Telegram errors, webhook secret, bad JSON, 404, healthz, dry-run and live API client (fake fetch). Also checked by hand: `node bot.js` in dry-run, `curl /healthz`, POST `/apua` to `/webhook` printed the help message.

### B02 Content loader
- State: todo
- Needs: B01
- What: `content/` module that reads, at start-up, from the repo root: the applet list from `index.html` (title, level, relative path → GitHub Pages URL), curriculum goals from both OPS files (id, text, grade band), grades 1-6 items from `math-misconceptions/grades1-6/exercises/grades1-6/*.json`, grades 7-9 items from `math-misconceptions/build/bank.json` when it exists. A missing source gives an empty list and a warning, never a crash. `/healthz` reports counts per source.
- Test: loader tests against the real repo files and against small fixtures in `test/fixtures/`.
- Done:
- Notes:

### B03 /appletit
- State: todo
- Needs: B02
- What: `/appletit` shows level buttons (luokat 1-6, yläkoulu 7-9, lukio pitkä, lukio lyhyt); a tap lists that level's applets as links. `/appletit <hakusana>` searches titles. Long lists are split under Telegram's 4096-character limit.
- Test: fake updates and callback taps; message length check.
- Done:
- Notes:

### B04 /tavoite
- State: todo
- Needs: B02
- What: `/tavoite A36.S2.04` shows that goal; `/tavoite <hakusana>` lists up to 10 matching goals. Where applets or exercises are linked to the goal, list them too. Like `/define` in the course bots.
- Test: exact id, partial search, no match.
- Done:
- Notes:

### B05 Answer parsing
- State: todo
- Needs: B01
- What: `answers.js`: normalise a typed answer (spaces, decimal comma or point, U+2212 or hyphen minus, `1/2` fractions, trailing units), compare with an item's `answer`, and return `correct`, `wrong` or `unparsed`. Port the checking rules that `math-misconceptions` documents (schema and backlog section 1.3) so the bot and the Python verifiers agree.
- Test: table of inputs and expected results, including every answer in the current 1-6 batches.
- Done:
- Notes:

### B06 Misconception texts
- State: todo
- Needs: B02
- What: `scripts/build_misconceptions.js` (or `.py`) that turns the `Misconceptions` sheet of `math_misconceptions_item_bank.xlsx` plus the sub-variants in `grades1-6/tools/buggy_rules/buggy_rules.py` into `data/misconceptions_fi.json`: id → short Finnish feedback for the pupil ("Vähensit pienemmän numeron suuremmasta joka sarakkeessa...") and a teacher note. The Finnish texts are drafts until the teacher reviews them (`status` field).
- Test: every misconception id used in the exercise batches has an entry.
- Done:
- Notes:

### B07 Numeric-entry quiz
- State: todo
- Needs: B02, B05, B06, D1
- What: `/harjoittele` serves `numeric_entry` items one at a time (5 per round), grades the typed reply with B05, and on a wrong answer checks it against the item's `misconceptions` answers: a match shows that misconception's feedback from B06, otherwise a generic hint. Round summary at the end. Sessions in memory with expiry, nothing written to disk. Only `reviewed` items are served; `draft` items are served to `ADMIN_USER_IDS` only, marked `[LUONNOS]`.
- Test: full round with fake updates, including a misconception answer, an unparsed answer and session expiry.
- Done:
- Notes:

### B08 Choice items
- State: todo
- Needs: B07
- What: `choice` items (1-6) and `MC`/`TF` items (7-9 bank) shown with inline-keyboard buttons, the option text written into the message body with letters so Telegram does not truncate it (the optics bot's fix). Graded in code; wrong options map to misconception feedback like B07.
- Test: fake callback taps, shuffled option order still grades right.
- Done:
- Notes:

### B09 Filters
- State: todo
- Needs: B07
- What: `/harjoittele luokka 3`, `/harjoittele A36.S2.04`, `/harjoittele NUM-10`; with no argument, buttons by grade band and topic that actually have items.
- Test: each filter form, filter with no items.
- Done:
- Notes:

### B10 Grades 7-9 bank adapter
- State: todo
- Needs: B02, B08
- What: map `build/bank.json` items (types `NE`, `MC`, `TF`, ...; `flags.text_only`) to the same internal item shape as the 1-6 items, skip items that need a figure. Uses `solution.steps` and `feedback` texts when present.
- Test: fixtures built with `scripts/build_bank.py --include-draft` from a sample item.
- Done:
- Notes:

### B11 Teacher review commands
- State: todo
- Needs: B07, D4
- What: admin-only `/esikatsele <item-id>` and `/luonnokset [erä]`: page through draft items with answer and misconception answers shown, so the teacher can review on the phone. The bot does not change item status; it prints the ids to mark `reviewed` in the JSON.
- Test: admin vs non-admin.
- Done:
- Notes:

### B12 Diagnostics
- State: todo
- Needs: B02
- What: `/healthz` details plus admin `/lahteet` report (files loaded, item counts by status and goal, applets per level), like the course bots' `/source_*` commands.
- Test: report content from fixtures.
- Done:
- Notes:

### B13 Deployment guide
- State: todo
- Needs: B01, D3, D4
- What: `DEPLOY.md`: BotFather steps, Railway service with root directory `telegram-bot/`, environment variables (`TELEGRAM_TOKEN`, `WEBHOOK_SECRET`, `ADMIN_USER_IDS`, `REPO_ROOT`, `PAGES_BASE_URL`), `setWebhook` call with `secret_token`, how a push to `main` redeploys and so refreshes the content.
- Done:
- Notes:

### B14 End-to-end test and v1.0.0
- State: todo
- Needs: B03, B04, B07, B08, B09, B12, B13
- What: one scripted conversation covering every command, run by `npm test`; tag `BOT_VERSION` 1.0.0.
- Done:
- Notes:

## Later (only if D2 is reopened)

D2 rules out B20-B22 for now. They stay here as a record of what the course bots do, not as planned work. B23 does not need AI but stores data about users, so it needs its own decision.

### B20 Access control and credits
- State: blocked by D2
- Needs: D1, D2
- What: port `membership.js`, `usageLimiter.js`, `accessGuard.js` from the course bots, texts in Finnish.

### B21 Claude Q&A for teachers
- State: blocked by D2
- Needs: B20
- What: free-text questions answered from a cached system prompt built from the OPS goal files and the applet backlog descriptions (`BACKLOG.md` fields Tavoite, Yleinen virhekäsitys, Interaktio). Short answers, plain Unicode maths, links to applets.

### B22 Live exercise generation with review
- State: blocked by D2
- Needs: B20
- What: when the bank has too few items for a filter, generate more with Claude into a pending file, never served until reviewed; export with an admin command and hand over to the exercise pipelines, whose verify scripts decide what enters the bank.

### B23 Learning analytics
- State: todo
- Needs: D1 and a completed privacy review
- What: the laser bot's pseudonymous per-answer events, `/tietosuoja`, `/kiellä`, admin statistics by goal and misconception. Not for grades 1-6 while `EXPERT_REVIEW_REQUIRED.md` applies.

## Log

| Date | Task | Result |
|---|---|---|
| 2026-09-30 | backlog | Created from the analysis in `BOT_ANALYSIS.md` |
| 2026-09-30 | D1-D3 | Decided: teachers and upper-secondary students, no AI calls, code in `telegram-bot/` |
| 2026-09-30 | B01 | Skeleton, v0.1.0, 15 tests pass |
