import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const TEST_DIR = path.dirname(fileURLToPath(import.meta.url));
export const SITE_DIR = path.resolve(TEST_DIR, '..');

// fetch() stand-in that reads file:// URLs from disk.
export async function fileFetch(url) {
  const p = fileURLToPath(url);
  if (!fs.existsSync(p)) return { ok: false, status: 404, json: async () => ({}) };
  const text = fs.readFileSync(p, 'utf8');
  return { ok: true, status: 200, json: async () => JSON.parse(text) };
}

export function fileUrl(p) {
  return pathToFileURL(p).href;
}
