'use strict';

const { createTelegram } = require('../src/telegram');
const { createBot } = require('../src/handlers');

let nextUpdateId = 1;

function makeBot(opts = {}) {
  const tg = createTelegram({ token: '', log: () => {} });
  const errors = [];
  const bot = createBot({ tg, log: (m) => errors.push(m), ...opts });
  return { bot, tg, errors };
}

function textUpdate(text, { chatType = 'private', chatId = 42 } = {}) {
  return {
    update_id: nextUpdateId++,
    message: { message_id: 1, chat: { id: chatId, type: chatType }, from: { id: 7 }, text },
  };
}

module.exports = { makeBot, textUpdate };
