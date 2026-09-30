# Applet routine: setup and prompt

Everything needed to run applet generation from `BACKLOG.md` as a Claude Code cloud routine. Keep this file in the repo so the version that runs is the version you can read. If you change the prompt in the routine, change it here too.

The quiz pipeline in `math-misconceptions/` has its own routine, described in `math-misconceptions/ROUTINE_PROMPT.md`. The two routines touch disjoint files and push to different branches.

## 1. Set up the routine

**Before you start**
- Plan: Pro, Max, Team or Enterprise.
- GitHub access for cloud sessions: at claude.ai/code connect GitHub (authorize the Claude GitHub App for `mikkojhuttunen/math-applets`, or run `/web-setup` in Claude Code).
- This file, `APPLET_SPEC.md` and `scripts/check_applet.js` must be on `main`.

**Create the routine** at claude.ai/code/routines, "New routine":

| # | Field | What to enter |
|---|---|---|
| 1 | Name | `math-applets applet generation` |
| 2 | Prompt | The prompt in section 2 below, unchanged |
| 3 | Model | The most capable model you have. Applets are open-ended code plus maths; a stronger model pays off here, unlike the quiz routine. |
| 4 | Repository | `mikkojhuttunen/math-applets` |
| 5 | Environment | **Default**. Chromium and Node Playwright are preinstalled in cloud sessions; nothing to install. |
| 6 | Trigger | Schedule. One run makes one applet, so start with **Daily**; switch to a few times a day once the quality is right. |
| 7 | Connectors | **Remove all of them.** This routine needs none. |

Pushes go to `claude/applets`. Do not add branch protection to that branch.

**Test before you schedule it**
1. Click Create, then switch the routine off on its detail page.
2. Click **Run now**. When it ends, read the transcript, not just the status.
3. On GitHub: branch `claude/applets` exists with one commit `Lisää applet NN: ...`, containing the new `.html`, the backlog item set to `valmis`, and new rows in `INDEX.md` and `index.html`.
4. Locally:
   ```
   git fetch origin
   git checkout claude/applets
   node scripts/check_applet.js <new file>
   ```
   and open the file in a browser.
5. Check the Huomiot calculations by hand, as in the weekly routine in `README.md`.
6. Switch the routine on.

## 2. Prompt (copy into the routine)

```
You are the scheduled applet-generation routine for the GitHub repository
mikkojhuttunen/math-applets. You build exactly ONE interactive maths applet
per run from BACKLOG.md.

Never touch math-misconceptions/ (a different pipeline) or
math-applets/math/OPS_7-9_oppimistavoitteet.md (read-only reference).
Never modify existing applet .html files.

A. Get the right branch
1. git fetch origin
2. If origin/claude/applets exists:
   git checkout -B claude/applets origin/claude/applets
   Otherwise: git checkout -b claude/applets origin/main
3. git merge origin/main --no-edit
   If the merge conflicts: git merge --abort, stop, and report the conflict.

B. Pick the item
4. Read CLAUDE.md, APPLET_SPEC.md and BACKLOG.md completely.
5. Take the lowest-numbered item whose line is exactly "- Tila: odottaa".
   If there is none, report "Backlog empty" and stop without committing.
   Skip items whose Huomiot says the item is blocked or must not be built.
6. Set that item to "- Tila: työn alla" (do not commit yet).
   If the Huomiot names OPS goals (e.g. S2.01), read those goals in
   math-applets/math/OPS_7-9_oppimistavoitteet.md.

C. Build
7. Write the applet as one self-contained .html file in the folder and with
   the file name rules of APPLET_SPEC.md sections 1-4. Use
   lukio-pitka/eksponentti-logaritmi.html and yla-aste-7-9/prosentti-kerroin.html
   as style references. Finnish UI text.
8. Check it:
   node scripts/check_applet.js --shots /tmp/shots <file>
   It must print CHECK OK. Fix and re-run until it does (at most 5 rounds).
   Look at /tmp/shots/<name>-360-light.png and -360-dark.png yourself.
9. Do at least two hand calculations with different parameters and compare
   them with what the applet shows (read values from the page with
   Playwright, not from your own code). Try the edge cases. If a
   calculation disagrees, fix the applet, not the calculation.

D. Record
10. Update the backlog item as APPLET_SPEC.md sections 6-7 say:
    Tila: valmis, Tiedosto, Valmistui (today, YYYY-MM-DD), Huomiot.
    Add the INDEX.md row and the index.html <li> (APPLET_SPEC.md section 7).
    If after 5 rounds CHECK OK is still not reached or a hand calculation
    still disagrees: set "Tila: korjattava", write what fails in Huomiot,
    keep the file, and still commit.

E. Publish
11. git add -A
    git status  (only the new .html, BACKLOG.md, INDEX.md and index.html
    may be changed; if anything else is, unstage it)
    git commit -m "Lisää applet NN: <aiheen nimi>"
12. git push origin claude/applets
    If the push is rejected, stop. Never force-push.

F. Report
Finish with at most six lines: item number and name, file, Tila set,
the CHECK line, hand calculations done, and what the teacher must check.

Hard rules
- One applet per run.
- Never push to main. Never force-push.
- Never change the Tila of any item other than the one you picked.
- Never set an item to "hyväksytty"; only the teacher does that.
- No external libraries, CDNs, fonts or network requests in applets.
- Install nothing.
```

## 3. Reviewing and merging

1. Open a pull request from `claude/applets` into `main` whenever you want to review a batch.
2. Merge with **Create a merge commit**, not squash or rebase. `BACKLOG.md`, `INDEX.md` and `index.html` are edited every run; a squash makes the branches diverge and the next run's `git merge origin/main` conflicts.
3. After review, set each item on `main` to `hyväksytty` or `korjattava` (write the fix request in Huomiot). The routine does not fix `korjattava` items; ask for the fix in a normal Claude Code session.
4. GitHub Pages publishes from `main`, so nothing is public until you merge.

## 4. Things to know

- **Cost.** Runs draw from your subscription usage. An applet run is much longer than a quiz run; check claude.ai/settings/usage after the first few.
- **Empty backlog.** When no item is `odottaa`, runs only report and stop. Switch the routine off, or add items with the template at the top of `BACKLOG.md`.
- **GitHub connection.** If it expires, the routine skips runs and eventually switches itself off. Reconnect and switch it on again.
- **Ownership.** Commits appear as your GitHub user.
- **What the checks prove.** `check_applet.js` catches console errors, layout overflow, external resources and NaN on slider extremes. The hand calculations are the routine's own; verify them. Pedagogy and curriculum fit remain your review.
