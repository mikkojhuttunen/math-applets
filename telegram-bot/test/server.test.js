'use strict';

const test = require('node:test');
const assert = require('node:assert');
const { createServer } = require('../src/server');

async function withServer(opts, fn) {
  const received = [];
  const server = createServer({ handleUpdate: (u) => received.push(u), version: '9.9.9', ...opts });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    await fn(base, received);
  } finally {
    await new Promise((r) => server.close(r));
  }
}

test('GET / and /healthz answer with the version', async () => {
  await withServer({ health: () => ({ dryRun: true }) }, async (base) => {
    const root = await fetch(`${base}/`);
    assert.match(await root.text(), /v9\.9\.9/);
    const h = await (await fetch(`${base}/healthz`)).json();
    assert.strictEqual(h.ok, true);
    assert.strictEqual(h.version, '9.9.9');
    assert.strictEqual(h.dryRun, true);
    assert.ok(Number.isInteger(h.uptimeSeconds));
  });
});

test('webhook passes the update on and answers 200', async () => {
  await withServer({}, async (base, received) => {
    const res = await fetch(`${base}/webhook`, { method: 'POST', body: JSON.stringify({ update_id: 5 }) });
    assert.strictEqual(res.status, 200);
    assert.deepStrictEqual(received, [{ update_id: 5 }]);
  });
});

test('webhook checks the secret token when one is set', async () => {
  await withServer({ webhookSecret: 's3cret' }, async (base, received) => {
    const bad = await fetch(`${base}/webhook`, { method: 'POST', body: '{"update_id":1}' });
    assert.strictEqual(bad.status, 403);
    const good = await fetch(`${base}/webhook`, {
      method: 'POST',
      headers: { 'x-telegram-bot-api-secret-token': 's3cret' },
      body: '{"update_id":2}',
    });
    assert.strictEqual(good.status, 200);
    assert.deepStrictEqual(received, [{ update_id: 2 }]);
  });
});

test('webhook rejects invalid JSON, unknown paths give 404', async () => {
  await withServer({}, async (base, received) => {
    assert.strictEqual((await fetch(`${base}/webhook`, { method: 'POST', body: 'not json' })).status, 400);
    assert.strictEqual((await fetch(`${base}/nope`)).status, 404);
    assert.strictEqual(received.length, 0);
  });
});
