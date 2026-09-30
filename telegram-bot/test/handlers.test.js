'use strict';

const test = require('node:test');
const assert = require('node:assert');
const { makeBot, textUpdate } = require('./helpers');
const { parseCommand } = require('../src/handlers');
const texts = require('../src/texts');

test('parseCommand splits command, target and arguments', () => {
  assert.deepStrictEqual(parseCommand('/apua'), { command: 'apua', target: '', args: '' });
  assert.deepStrictEqual(parseCommand('/Tavoite@MathBot  A36.S2.04 '), {
    command: 'tavoite',
    target: 'mathbot',
    args: 'A36.S2.04',
  });
  assert.strictEqual(parseCommand('hei'), null);
});

for (const cmd of ['/start', '/apua', '/help']) {
  test(`${cmd} replies with the Finnish help text`, async () => {
    const { bot, tg } = makeBot();
    await bot.handleUpdate(textUpdate(cmd));
    assert.strictEqual(tg.sent.length, 1);
    assert.strictEqual(tg.sent[0].method, 'sendMessage');
    assert.strictEqual(tg.sent[0].payload.chat_id, 42);
    assert.strictEqual(tg.sent[0].payload.text, texts.HELP);
  });
}

test('a repeated update_id is handled only once', async () => {
  const { bot, tg } = makeBot();
  const u = textUpdate('/apua');
  await bot.handleUpdate(u);
  await bot.handleUpdate(u);
  assert.strictEqual(tg.sent.length, 1);
});

test('unknown command and free text get a pointer to /apua in a private chat', async () => {
  const { bot, tg } = makeBot();
  await bot.handleUpdate(textUpdate('/eiole'));
  await bot.handleUpdate(textUpdate('mikä on murtoluku?'));
  assert.deepStrictEqual(
    tg.sent.map((s) => s.payload.text),
    [texts.UNKNOWN_COMMAND, texts.FREE_TEXT]
  );
});

test('in a group, free text and unknown untargeted commands are ignored', async () => {
  const { bot, tg } = makeBot({ botUsername: 'mathbot' });
  await bot.handleUpdate(textUpdate('moi kaikki', { chatType: 'group' }));
  await bot.handleUpdate(textUpdate('/eiole', { chatType: 'group' }));
  await bot.handleUpdate(textUpdate('/apua@otherbot', { chatType: 'group' }));
  assert.strictEqual(tg.sent.length, 0);
  await bot.handleUpdate(textUpdate('/apua@MathBot', { chatType: 'supergroup' }));
  assert.strictEqual(tg.sent.length, 1);
});

test('updates without text are ignored', async () => {
  const { bot, tg } = makeBot();
  await bot.handleUpdate({ update_id: 999001 });
  await bot.handleUpdate({ update_id: 999002, message: { chat: { id: 1, type: 'private' } } });
  await bot.handleUpdate(null);
  assert.strictEqual(tg.sent.length, 0);
});

test('a failing Telegram call is logged, not thrown', async () => {
  const { bot, tg, errors } = makeBot();
  tg.call = async () => {
    throw new Error('boom');
  };
  await bot.handleUpdate(textUpdate('/apua'));
  assert.strictEqual(errors.length, 1);
  assert.match(errors[0], /boom/);
});
