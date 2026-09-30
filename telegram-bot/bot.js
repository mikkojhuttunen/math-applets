'use strict';
/**
 * math-applets Telegram bot. Serves the material in this repository in
 * Finnish. Makes no AI calls (BACKLOG_BOT.md, decision D2).
 * Version history: CHANGELOG.md.
 */

const { readConfig } = require('./src/config');
const { createTelegram } = require('./src/telegram');
const { createBot } = require('./src/handlers');
const { createServer } = require('./src/server');

const BOT_VERSION = '0.1.0';

function main() {
  const config = readConfig();
  const tg = createTelegram({ token: config.token });
  if (config.token && !config.webhookSecret) {
    console.warn('WEBHOOK_SECRET is not set: anyone who finds the URL can post fake updates.');
  }
  const bot = createBot({ tg, botUsername: config.botUsername });
  const server = createServer({
    handleUpdate: bot.handleUpdate,
    webhookSecret: config.webhookSecret,
    version: BOT_VERSION,
    health: () => ({ dryRun: tg.dryRun }),
  });
  server.listen(config.port, () => {
    console.log(`math-applets bot v${BOT_VERSION} listening on ${config.port}${tg.dryRun ? ' (dry-run, no TELEGRAM_TOKEN)' : ''}`);
  });
  return server;
}

if (require.main === module) main();

module.exports = { BOT_VERSION, main };
