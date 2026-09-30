# math-applets Telegram bot

Telegram bot that serves the material in this repository (applets, curriculum goals, exercises) in Finnish. It makes no AI calls and stores nothing about its users (decisions D1-D2 in `BACKLOG_BOT.md`).

- `BACKLOG_BOT.md`: work queue, one task at a time
- `BOT_ANALYSIS.md`: how the Laser Physics and Optics bots work and what this bot takes from them
- `CHANGELOG.md`: versions

## Layout

| File | Role |
|---|---|
| `bot.js` | Entry point: reads the environment, wires the parts, starts the server |
| `src/config.js` | Environment variables |
| `src/server.js` | HTTP server: `GET /`, `GET /healthz`, `POST /webhook` |
| `src/telegram.js` | Telegram Bot API client, dry-run without a token |
| `src/handlers.js` | Update routing and commands |
| `src/texts.js` | Finnish user-facing texts |
| `test/` | Offline tests (`node:test`) |

No npm dependencies: Node 18 or newer is enough.

## Run locally

```
cd telegram-bot
npm test
node bot.js
```

Without `TELEGRAM_TOKEN` the bot runs in dry-run mode and prints the messages it would send. Try it from a second terminal:

```
curl localhost:3000/healthz
curl -X POST localhost:3000/webhook -d '{"update_id":1,"message":{"message_id":1,"chat":{"id":5,"type":"private"},"text":"/apua"}}'
```

## Environment variables

| Variable | Meaning |
|---|---|
| `TELEGRAM_TOKEN` | Bot token from BotFather; unset = dry-run |
| `WEBHOOK_SECRET` | Secret token given to `setWebhook`; requests without it get 403. Always set in production. |
| `BOT_USERNAME` | The bot's @username, so group commands addressed to other bots are ignored |
| `PORT` | HTTP port (default 3000) |

Deployment steps come in task B13.
