'use strict';

function readConfig(env = process.env) {
  return {
    token: env.TELEGRAM_TOKEN || '',
    webhookSecret: env.WEBHOOK_SECRET || '',
    botUsername: (env.BOT_USERNAME || '').replace(/^@/, '').toLowerCase(),
    port: parseInt(env.PORT || '3000', 10),
  };
}

module.exports = { readConfig };
