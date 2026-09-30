# Routine setup and prompt

Everything needed to run the exercise generation in Claude cloud (a "routine"). Keep this file in the repo so the version that runs is the version you can read. If you change the prompt in the routine, change it here too.

## 1. Set up the routine (step by step)

**Before you start**
- Plan: Pro, Max, Team or Enterprise. On Team and Enterprise an Owner must not have switched routines off (admin settings, Claude Code, "Routines" toggle).
- GitHub access for cloud sessions: at claude.ai/code connect GitHub (authorize the Claude GitHub App, or run `/web-setup` in Claude Code). The routine clones the repo with this connection and its commits carry your GitHub user.
- The kit is already on `main` of `mikkojhuttunen/math-applets` (see README.md).

**Create the routine** at claude.ai/code/routines, "New routine":

| # | Field | What to enter |
|---|---|---|
| 1 | Name | `math-misconceptions exercise generation` |
| 2 | Prompt | The prompt in section 2 below, unchanged |
| 3 | Model | The model you choose is used on every run. Start with a mid-tier model: `verify.py` does the checking, so a bigger model only pays off if runs fail often. |
| 4 | Repository | `mikkojhuttunen/math-applets` |
| 5 | Environment | **Default**. Its Trusted network access reaches PyPI, so `pip install` in the prompt works. No setup script or variables are needed. |
| 6 | Trigger | Schedule, **Hourly** (minimum interval is one hour) |
| 7 | Connectors | **Remove all of them.** By default every connector you have is included, and a routine may use its write tools without asking. This routine needs none. |

Leave branch settings as they are. Pushes to `claude/`-prefixed branches are always accepted, and `claude/exercises` fits. Do not add a branch protection rule to `claude/exercises` on GitHub, or pushes are rejected.

**Test before you let it run hourly**
1. Click Create, then immediately switch the routine off with the on/off switch on its detail page.
2. Click **Run now**. Open the run when it ends. A green status only means the session exited without an infrastructure error; read the transcript to see what happened.
3. On GitHub check: the branch `claude/exercises` exists, it has one commit `Run 1: ...`, `math-misconceptions/exercises/` has new files, and the backlog shows `X` cells and log rows.
4. Locally: `git fetch && git checkout claude/exercises && cd math-misconceptions && python scripts/verify.py --base origin/main --check-backlog` must print `VERIFY OK`.
5. Read three to five generated items yourself (Finnish wording, sensible numbers).
6. Switch the routine on again. If you want a fixed minute instead of "on the hour, possibly several minutes late", ask Claude Code for `/schedule update` and give a cron expression such as `7 * * * *`.

## 2. Prompt (copy into the routine)

```
You are the scheduled exercise-generation routine for the GitHub repository
mikkojhuttunen/math-applets. Work only inside the folder math-misconceptions/.
Never touch other files: BACKLOG.md, INDEX.md, index.html and the applet
folders belong to a different pipeline. You may read
math-applets/math/OPS_7-9_oppimistavoitteet.md but never edit it.

A. Get the right branch
1. git fetch origin
2. If origin/claude/exercises exists, run:
   git checkout -B claude/exercises origin/claude/exercises
   Otherwise run: git checkout -b claude/exercises origin/main
3. git merge origin/main --no-edit
   This brings in changes I made on main (for example items I approved).
   If the merge conflicts: git merge --abort, stop, and report the conflict.

B. Do the run
4. cd math-misconceptions && pip install -q -r requirements.txt
5. python tests/run_tests.py
   If any test fails, stop and report: the tooling is broken.
6. Read math-misconceptions-7-9grades-backlog.md completely and follow its
   section 1 exactly: configuration block, steps 1-8, item schema in 1.3.
   The configuration block in the backlog is authoritative.

C. Verify and publish
7. python scripts/verify.py --base HEAD --check-backlog
   It must print VERIFY OK. Backlog section 1.2 step 6 says what to do
   if it does not.
8. From the repository root:
   git add math-misconceptions
   git commit -m "Run <N>: <topic ids> <type codes>, +<K> items"
   where <N> is the new value of "Runs completed" in the backlog.
   If nothing changed, do not commit.
9. git push origin claude/exercises
   If the push is rejected, stop. Never force-push.

D. Report
Finish with at most six lines: run number, topics and types done, number of
new items, the VERIFY line, and anything skipped or failed and why.

Hard rules
- Never push to main. Never force-push.
- Never edit, renumber or delete an existing item.
- New items always have status "draft".
- Never change section 1 of the backlog.
- Install nothing except requirements.txt.
```

## 3. Variant for a local Cowork task (no GitHub push)

Your repo README says local scheduled tasks cannot push to GitHub, so pushing stays manual. Use the same prompt without parts A and C (steps 1-3, 8, 9). Point the task at a local clone of the repo, keep step 7 as it is, and commit and push yourself. `--base HEAD` then compares against your last commit, so items from earlier runs that you have not committed yet count as new, and edits to them would not be caught. Commit after every review to avoid that.

## 4. Reviewing and merging

1. Open a pull request from `claude/exercises` into `main` whenever you want to review a batch.
2. Merge with **"Create a merge commit"**, not squash and not rebase. A squash makes `claude/exercises` diverge from `main`, and the backlog file (edited every run) then conflicts on the next run's `git merge origin/main`.
3. Items arrive on `main` as `draft`. Approve an item by changing `"status": "draft"` to `"approved"` on `main`. The next run merges that in and treats it as unchanged.
4. Only approved items are served by `python scripts/build_bank.py`. For beta testing with unreviewed items use `--include-draft`.

## 5. Things to know

- **Cost.** Routine runs draw from your normal subscription usage. When the limit is hit, further runs are rejected until the window resets, unless you have usage credits switched on. Check claude.ai/settings/usage after the first day. Scheduled runs are also capped at 100 per hour per account, which an hourly routine never reaches.
- **Length of the job.** Phases 0-2 have 137 planned cells; at six cells per run that is about 23 runs, roughly a day. When no cell is left the routine only reports and stops, but the hourly schedule keeps starting runs. Switch the routine off when it says the phase is finished, or change `ACTIVE_PHASES` in the backlog to continue.
- **GitHub connection.** If the connection expires, the routine skips runs for up to 72 hours and then turns itself off. Reconnect and switch it on again.
- **Ownership.** The routine belongs to your claude.ai account and is not shared. Anything it commits appears as you.
- **Public repo.** The repo is public and published with GitHub Pages, so drafts and answer keys in `exercises/` are public. That is fine for a beta; think twice before adding material you would not publish.
- **Repeated failures.** If the same cell fails twice, the backlog log holds two `Failed` rows and the routine skips that cell. Read the log row, fix the cause, and delete the two rows to retry.
- **What `verify.py` proves.** Recomputed algebra, tags and curriculum links are consistent. It does not judge pedagogy, wording or the correctness of MC options. That remains your review.
- Routines are a research preview: behaviour and limits may change.
