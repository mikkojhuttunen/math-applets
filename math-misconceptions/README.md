# math-misconceptions

Exercise bank for grades 7-9 built around documented misconceptions and linked to the Finnish curriculum (OPS) goal IDs. A scheduled Claude routine fills it slowly; you review and approve; a Telegram bot or mobile app reads the result.

```
math-misconceptions/
  math-misconceptions-7-9grades-backlog.md   work queue, coverage matrix, log (the routine edits this)
  ROUTINE_PROMPT.md                          routine settings and prompt
  schema/item.schema.json                    what an exercise item looks like
  exercises/<TopicID>/<TypeCode>.json        the items (written by the routine)
  generators/<template>.py                   reproducible generators (written by the routine)
  scripts/verify.py                          checks structure, curriculum links and the algebra
  scripts/build_bank.py                      builds build/bank.json and build/index.json for clients
  tests/run_tests.py                         self-test for the two scripts
  sources/                                   item bank xlsx, exercise-types document, bibliography
                                             (the OPS goal file is read from ../math-applets/math/)
```

## Where this folder must be

`math-misconceptions/` sits at the **git root** of the repository, next to `index.html`, `BACKLOG.md` and `README.md` (not inside another folder such as `math-applets/`). All commands below are run from the git root unless stated otherwise. Check with:

```
cd "$(git rev-parse --show-toplevel)"
ls index.html BACKLOG.md math-misconceptions      # all three must be listed
```

## First-time setup on a machine

```
cd "$(git rev-parse --show-toplevel)"
pip install -r math-misconceptions/requirements.txt
python math-misconceptions/tests/run_tests.py                  # must end with "All tests passed"
python math-misconceptions/scripts/verify.py --check-backlog   # must print "VERIFY OK"
```

Then create the routine as described in `ROUTINE_PROMPT.md`. The first run creates the branch `claude/exercises` from `main`.

The OPS goal file is read from `math-applets/math/OPS_7-9_oppimistavoitteet.md` (where it currently lives in the repo). If you move it, `verify.py` warns and skips the S-ID existence check until you pass `--ops <path>` or update `find_ops()` in `scripts/verify.py` and the paths in the backlog.

## Everyday commands (run inside `math-misconceptions/`)

| Command | Purpose |
|---|---|
| `python scripts/verify.py --base HEAD --check-backlog` | full check; existing items unchanged, backlog matches files |
| `python scripts/verify.py` | structure, curriculum and algebra only |
| `python scripts/build_bank.py` | write `build/bank.json` with approved items only |
| `python scripts/build_bank.py --include-draft` | same, including drafts (beta) |
| `python tests/run_tests.py` | self-test after changing a script or the schema |

## Files a client reads

- `build/bank.json`: `{schema_version, bank_version, served_statuses, counts, items[]}`. Each item is the schema item plus `flags` (`text_only`, `needs_figure`, `telegram_poll`).
- `build/index.json`: item ids grouped by `by_ops`, `by_t`, `by_level`, `by_grade`, `by_misconception`, `by_type`, `by_topic`.

Answer checking rules (expression sampling, number tolerance, decimal comma) are described in the schema and the backlog, section 1.3.
