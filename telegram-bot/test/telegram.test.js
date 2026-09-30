'use strict';

const test = require('node:test');
const assert = require('node:assert');
const { createTelegram } = require('../src/telegram');

test('without a token, calls are recorded and not sent', async () => {
  const tg = createTelegram({ token: '', fetchImpl: () => assert.fail('fetch called'), log: () => {} });
  assert.strictEqual(tg.dryRun, true);
  await tg.call('sendMessage', { chat_id: 1, text: 'x' });
  assert.deepStrictEqual(tg.sent, [{ method: 'sendMessage', payload: { chat_id: 1, text: 'x' } }]);
});

test('with a token, calls go to the Bot API and errors are raised', async () => {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, body: JSON.parse(init.body) });
    const ok = calls.length === 1;
    return { ok, status: ok ? 200 : 400, json: async () => (ok ? { ok: true, result: {} } : { ok: false, description: 'Bad Request' }) };
  };
  const tg = createTelegram({ token: 'T', fetchImpl });
  await tg.call('sendMessage', { chat_id: 1, text: 'x' });
  assert.strictEqual(calls[0].url, 'https://api.telegram.org/botT/sendMessage');
  await assert.rejects(tg.call('sendMessage', { chat_id: 1, text: 'y' }), /Bad Request/);
});
