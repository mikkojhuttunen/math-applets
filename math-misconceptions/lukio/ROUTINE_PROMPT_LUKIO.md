# Lukio routine: setup and prompt

Everything needed to run the lukio exercise generation in Claude cloud (a "routine"). Adapted from the 7–9 `../ROUTINE_PROMPT.md`. Keep this file in the repo so the version that runs is the version you can read. If you change the prompt in the routine, change it here too.

## 1. Set up the routine (step by step)

**Before you start**
- Plan: Pro, Max, Team or Enterprise. On Team and Enterprise an Owner must not have switched routines off (admin settings, Claude Code, "Routines" toggle).
- GitHub access for cloud sessions: at claude.ai/code connect GitHub (authorize the Claude GitHub App, or run `/web-setup` in Claude Code). The routine clones the repo with this connection and its commits carry your GitHub user.
- The lukio tooling (schema, `scripts/verify.py`, `scripts/build_bank.py`, `tests/`, `generators/gen_common.py`, this file) must be on `main`. The routine starts its branch from `main`.
- `ROUTINE_ENABLED` in `BACKLOG_LUKIO.md` section 1.1 is `no` until you set it to `yes` on `main`. While it is `no`, every run only reports "lukio routine not enabled" and commits nothing.

**Create the routine** at claude.ai/code/routines, "New routine":

| # | Field | What to enter |
|---|---|---|
| 1 | Name | `math-misconceptions lukio exercise generation` |
| 2 | Prompt | The prompt in section 2 below, unchanged |
| 3 | Model | Used on every run. Lukio items are symbolic (derivatives, integrals, trigonometric equations), so a stronger model than the 7–9 routine's pays off more often here. `verify.py` still does the checking. |
| 4 | Repository | `mikkojhuttunen/math-applets` |
| 5 | Environment | **Default**. Its Trusted network access reaches PyPI, so `pip install` in the prompt works. No setup script or variables are needed. |
| 6 | Trigger | Schedule, **Hourly** (minimum interval is one hour). Pick a different minute from the 7–9 routine, for example `37 * * * *`, so the two do not start together. |
| 7 | Connectors | **Remove all of them.** By default every connector you have is included, and a routine may use its write tools without asking. This routine needs none. |

Leave branch settings as they are. Pushes to `claude/`-prefixed branches are always accepted, and `claude/exercises-lukio` fits. Do not add a branch protection rule to it on GitHub, or pushes are rejected.

**Test before you let it run hourly**
1. Click Create, then immediately switch the routine off with the on/off switch on its detail page.
2. With `ROUTINE_ENABLED: no` click **Run now** once. The transcript must end with "lukio routine not enabled", and no branch or commit may appear. This shows the gate works.
3. Set `ROUTINE_ENABLED: yes` in `math-misconceptions/lukio/BACKLOG_LUKIO.md` on `main` and push.
4. Click **Run now** again. Open the run when it ends. A green status only means the session exited without an infrastructure error; read the transcript to see what happened.
5. On GitHub check: the branch `claude/exercises-lukio` exists, it has one commit `Lukio run 1: ...`, `math-misconceptions/lukio/exercises/` and `math-misconceptions/lukio/generators/` have new files, and the backlog shows `X` cells, log rows and "Runs completed 1". Nothing outside `math-misconceptions/lukio/` changed.
6. Locally:
   ```
   git fetch origin
   git checkout claude/exercises-lukio
   cd math-misconceptions/lukio
   python tests/run_tests.py
   python scripts/verify.py --base origin/main --check-backlog
   ```
   The tests must pass and verify must print `VERIFY OK`.
7. Read five or more generated items yourself: Finnish wording, sensible numbers, the misconception really shows in the distractors, MAB items at MAB level.
8. Switch the routine on. Log `L-T05` as done in `BACKLOG_LUKIO.md` section 2, and update the lukio row in the root `CLAUDE.md` pipeline table ("planned; no routine yet").

## 2. Prompt (copy into the routine)

```
You are the scheduled lukio exercise-generation routine for the GitHub
repository mikkojhuttunen/math-applets. Work only inside the folder
math-misconceptions/lukio/. Never touch files outside it: the rest of
math-misconceptions/ belongs to the grades 7-9 and 1-6 pipelines, and the
applet files belong to another pipeline. You may read
../math-misconceptions-7-9grades-backlog.md, ../sources/ and
../requirements.txt but never edit them.

A. Get the right branch
1. git fetch origin
2. If origin/claude/exercises-lukio exists, run:
   git checkout -B claude/exercises-lukio origin/claude/exercises-lukio
   Otherwise run: git checkout -b claude/exercises-lukio origin/main
3. git merge origin/main --no-edit
   This brings in changes I made on main (for example items I approved).
   If the merge conflicts: git merge --abort, stop, and report the conflict.

B. Do the run
4. pip install -q -r math-misconceptions/requirements.txt
   cd math-misconceptions/lukio
5. Read BACKLOG_LUKIO.md section 1.1. If ROUTINE_ENABLED is no, stop:
   change nothing, do not commit, report "lukio routine not enabled".
6. python tests/run_tests.py
   If any test fails, stop and report: the tooling is broken.
7. Read BACKLOG_LUKIO.md completely and follow its section 1 exactly:
   configuration block, steps 1-8, quality rules in 1.3. The configuration
   block in the backlog is authoritative. Item format: schema/item.schema.json;
   tests/fixtures/good/ has one hand-written example per type.
   Generators import generators/gen_common.py (base_item, mc_options, cli,
   frac, show); generators/example_ltri01_ne.py is the model to follow.
   Run generators from math-misconceptions/lukio/:
   python generators/<template>.py --write --run <N> --date <today>

C. Verify and publish
8. python scripts/verify.py --base HEAD --check-backlog
   It must print VERIFY OK. Backlog section 1.2 step 6 says what to do
   if it does not. Then run python tests/run_tests.py once more.
9. From the repository root:
   git add math-misconceptions/lukio
   git commit -m "Lukio run <N>: <topic ids> <type codes>, +<K> items"
   where <N> is the new value of "Runs completed" in the backlog.
   If nothing changed, do not commit.
10. git push origin claude/exercises-lukio
   If the push is rejected, stop. Never force-push.

D. Report
Finish with at most six lines: run number, topics and types done, number of
new items (MAA / MAB), the VERIFY line, and anything skipped or failed and why.

Hard rules
- Never push to main. Never force-push.
- Write only: new generators/<template>.py files, new
  exercises/<TopicID>/<TypeCode>.json files, and BACKLOG_LUKIO.md as its
  step 1.2.5 allows. Never edit scripts/, schema/, tests/,
  generators/gen_common.py, generators/example_*.py, data/ or docs/.
- Never edit, renumber or delete an existing item.
- New items always have status "draft".
- Never change sections 0-2 of the backlog.
- Never copy YTL exam tasks or textbook tasks; stems are new.
- Install nothing except math-misconceptions/requirements.txt.
```

## 3. Reviewing and merging

1. Open a pull request from `claude/exercises-lukio` into `main` whenever you want to review a batch.
2. Merge with **"Create a merge commit"**, not squash and not rebase. A squash makes `claude/exercises-lukio` diverge from `main`, and the backlog file (edited every run) then conflicts on the next run's `git merge origin/main`.
3. Items arrive on `main` as `draft`. Approve an item by changing `"status": "draft"` to `"approved"` on `main`. The next run merges that in and treats it as unchanged.
4. Only approved items are served by `python scripts/build_bank.py` (run from `math-misconceptions/lukio/`). For beta testing with unreviewed items use `--include-draft`.

## 4. Things to know

- **Cost.** Routine runs draw from your normal subscription usage, shared with the 7–9 routine. When the limit is hit, further runs are rejected until the window resets, unless you have usage credits switched on. Check claude.ai/settings/usage after the first day.
- **Length of the job.** Phases 0–2 have 151 planned cells; at six cells per run (3 topics × 2 types) that is about 26 runs, roughly a day of hourly runs. When no cell is left the routine only updates "Last run" and stops, but the hourly schedule keeps starting runs. Switch the routine off when it says the phase is finished, or change `ACTIVE_PHASES` in the backlog to continue.
- **Seeds.** Cells marked `s` have a hand-written seed in `tests/fixtures/good/`. The routine generates a full batch for them like for `o` cells; the seed stays a test fixture and is not part of the bank.
- **Evidence.** The catalogue is a first assessment (L-R03 not done). Log rows for `Limited` topics carry "evidence to be checked"; read those items with that in mind.
- **GitHub connection.** If the connection expires, the routine skips runs for up to 72 hours and then turns itself off. Reconnect and switch it on again.
- **Ownership.** The routine belongs to your claude.ai account and is not shared. Anything it commits appears as you.
- **Public repo.** The repo is public and published with GitHub Pages, so drafts and answer keys in `exercises/` are public.
- **Repeated failures.** If the same cell fails twice, the log holds two `Failed` rows and the routine skips that cell. Read the log row, fix the cause, and delete the two rows to retry.
- **What `verify.py` proves.** Recomputed algebra (including antiderivatives, periodic solutions and intervals), tags and curriculum links are consistent. It does not judge pedagogy, wording, MAB level or the correctness of MC options. That remains your review.
- Routines are a research preview: behaviour and limits may change.
