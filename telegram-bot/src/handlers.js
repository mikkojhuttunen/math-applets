'use strict';

const texts = require('./texts');

const SEEN_MAX = 1000;

// Splits "/cmd@botname args" into { command, target, args }; null for non-commands.
function parseCommand(text) {
  const m = /^\/([a-z0-9_]+)(?:@([a-z0-9_]+))?(?:\s+([\s\S]*))?$/i.exec(text.trim());
  if (!m) return null;
  return { command: m[1].toLowerCase(), target: (m[2] || '').toLowerCase(), args: (m[3] || '').trim() };
}

function createBot({ tg, botUsername = '', log = console.error }) {
  const seen = new Set();

  function alreadySeen(updateId) {
    if (seen.has(updateId)) return true;
    seen.add(updateId);
    if (seen.size > SEEN_MAX) seen.delete(seen.values().next().value);
    return false;
  }

  function reply(chatId, text) {
    return tg.call('sendMessage', { chat_id: chatId, text, link_preview_options: { is_disabled: true } });
  }

  const commands = {
    start: (msg) => reply(msg.chat.id, texts.HELP),
    apua: (msg) => reply(msg.chat.id, texts.HELP),
    help: (msg) => reply(msg.chat.id, texts.HELP),
  };

  async function handleUpdate(update) {
    if (!update || update.update_id === undefined) return;
    if (alreadySeen(update.update_id)) return;

    const msg = update.message;
    if (!msg || typeof msg.text !== 'string' || !msg.chat) return;

    const isPrivate = msg.chat.type === 'private';
    const cmd = parseCommand(msg.text);

    if (!cmd) {
      if (isPrivate) await reply(msg.chat.id, texts.FREE_TEXT);
      return;
    }
    // In groups, "/cmd@otherbot" belongs to another bot.
    if (cmd.target && botUsername && cmd.target !== botUsername) return;

    const handler = commands[cmd.command];
    if (handler) return handler(msg, cmd.args);
    if (isPrivate || cmd.target) await reply(msg.chat.id, texts.UNKNOWN_COMMAND);
  }

  // Never throws: errors are logged so one bad update cannot stop the server.
  async function safeHandleUpdate(update) {
    try {
      await handleUpdate(update);
    } catch (e) {
      log(`handleUpdate failed: ${e.message}`);
    }
  }

  return { handleUpdate: safeHandleUpdate, parseCommand };
}

module.exports = { createBot, parseCommand };
