'use strict';

// Thin Telegram Bot API client. Without a token it runs in dry-run mode:
// every call is logged and recorded in `sent` instead of going to Telegram.
function createTelegram({ token, fetchImpl = globalThis.fetch, log = console.log } = {}) {
  const sent = [];
  const dryRun = !token;

  async function call(method, payload) {
    if (dryRun) {
      sent.push({ method, payload });
      log(`[dry-run] ${method} ${JSON.stringify(payload)}`);
      return { ok: true, result: null };
    }
    const res = await fetchImpl(`https://api.telegram.org/bot${token}/${method}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(15000),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) {
      throw new Error(`Telegram ${method} failed: HTTP ${res.status} ${data.description || ''}`.trim());
    }
    return data;
  }

  return { call, sent, dryRun };
}

module.exports = { createTelegram };
