'use strict';

const http = require('http');

const MAX_BODY = 1024 * 1024;

function sendJson(res, status, obj) {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(obj));
}

// GET / and /healthz for monitoring, POST /webhook for Telegram.
// The webhook answers 200 before the update is handled, so a slow reply
// never makes Telegram retry the same update.
function createServer({ handleUpdate, webhookSecret = '', version, health = () => ({}) }) {
  const startedAt = Date.now();

  return http.createServer((req, res) => {
    const url = (req.url || '').split('?')[0];

    if (req.method === 'GET' && url === '/') {
      res.writeHead(200, { 'content-type': 'text/plain; charset=utf-8' });
      return res.end(`math-applets bot v${version} is running`);
    }
    if (req.method === 'GET' && url === '/healthz') {
      return sendJson(res, 200, {
        ok: true,
        version,
        uptimeSeconds: Math.round((Date.now() - startedAt) / 1000),
        ...health(),
      });
    }
    if (req.method === 'POST' && url === '/webhook') {
      if (webhookSecret && req.headers['x-telegram-bot-api-secret-token'] !== webhookSecret) {
        res.writeHead(403);
        return res.end();
      }
      const chunks = [];
      let size = 0;
      req.on('data', (c) => {
        size += c.length;
        if (size > MAX_BODY) {
          res.writeHead(413);
          res.end();
          req.destroy();
        } else {
          chunks.push(c);
        }
      });
      req.on('end', () => {
        if (res.writableEnded) return;
        let update;
        try {
          update = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        } catch {
          res.writeHead(400);
          return res.end();
        }
        res.writeHead(200);
        res.end();
        handleUpdate(update);
      });
      return;
    }
    res.writeHead(404);
    res.end();
  });
}

module.exports = { createServer };
