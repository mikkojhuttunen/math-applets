# Changelog

`BOT_VERSION` in `bot.js` and `version` in `package.json` are bumped together. MAJOR: a command changes behaviour or is removed; MINOR: new command or feature; PATCH: fix with no new command.

## 0.1.0 (2026-09-30)

- B01: project skeleton. Webhook server on Node's built-in `http` (secret check, HTTP 200 before handling, duplicate `update_id`s dropped), `GET /` and `GET /healthz`, Telegram client on built-in `fetch` with a dry-run mode, `/start`, `/apua` (alias `/help`) in Finnish. No npm dependencies, no AI calls.
