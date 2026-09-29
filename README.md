# diff-bots.js

Re-diffs the FYS.240 Optics bot and FYS.501 Laser bot repos on demand, and
tracks what changed since the last time you ran it.

## Setup

1. Drop `diff-bots.js` into any folder (doesn't need to be inside either
   repo — it clones its own working copies).
2. Requirements: Node.js ≥ 18 and `git` on your PATH. No `npm install`
   needed — it only uses Node built-ins.

## Usage

```bash
node diff-bots.js              # pulls latest from both repos, diffs, reports
node diff-bots.js --no-pull    # skip the git fetch, just re-analyze what's cached
node diff-bots.js --json       # also dump the raw snapshot as JSON
```

Each run:
- clones (first time) or `git pull`s (every time after) both repos into
  `./.cache/`
- writes a full Markdown report to `./reports/report-<timestamp>.md` and
  overwrites `./reports/latest.md`
- prints a console summary, including a **"changed since last run"**
  section once you've run it at least twice — new commands, version bumps,
  quiz-bank growth, new changelog entries, feature-flag flips

That last part is the point: run it after every deploy or merge to either
repo and it'll tell you exactly what moved.

## What it checks

- `BOT_VERSION` + in-file CHANGELOG entries (only the Optics bot has these
  right now — the Laser bot has no versioning scheme yet)
- The command surface (`/HW`, `/quiz`, `/define`, `/mvquiz`, ...), extracted
  by scanning for the bots' own `^\/command` regex patterns
- A dozen feature flags (membership gating, photo work-check, `/pending`
  admin export, course-mismatch guards, glossary wiring, etc.)
- Quiz bank question counts (single-select and multi-select banks)
- Corpus file size, conversation-history depth, file/line counts

## Known limitations

- It only reads each repo's **main bot file** (`bot_fys240.js` /
  `bot_fys501.js`). Logic that lives in helper modules (`accessGuard.js`,
  `usageLimiter.js`, `membership.js`, etc.) isn't inspected directly — a
  couple of flags (e.g. `requireMember()`/`requireLLMBudget()` presence) are
  proxies for "gating exists somewhere," not a full picture of *where* it's
  enforced. Read the note printed above the feature-flag table.
- Command detection is regex-based against known patterns in these two
  files, not a real JS parser. It's been checked against both repos as of
  2026‑09‑21 but if either bot changes how it declares commands (e.g. a
  new dispatch style), the extraction regexes in `extractSignals()` may need
  a small update — they're commented inline for exactly that reason.
- If you rename either main file or repo, update the `REPOS` array at the
  top of `diff-bots.js`.

## Files it creates (git-ignore these if you keep this script in a repo)

```
.cache/        # cloned repo working copies + snapshot.json (previous-run state)
reports/       # generated Markdown reports (+ optional JSON snapshots)
```
# math-applets
