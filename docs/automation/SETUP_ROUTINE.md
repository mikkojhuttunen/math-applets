# Setting up the grades 1–6 exercise routine in Claude cloud

> **EXPERT REVIEW REQUIRED BEFORE USE WITH PUPILS. NOT LEGAL ADVICE.** This automation prepares exercise *content* from synthetic data. It must never touch data about pupils. Using the exercises with pupils is a separate step that needs the sign-off described in `docs/privacy/`.

Checked against the Claude Code documentation on 30 September 2026. Routines are a research preview, so behaviour and limits can change. Confirm the current details at <https://code.claude.com/docs/en/web-scheduled-tasks>.

## What a routine is

A routine is a saved Claude Code session: a prompt, one or more GitHub repositories, an environment and optional connectors. It runs on Anthropic's cloud on a schedule, on an API call, or on a GitHub event, even when your computer is off. It runs unattended with no approval prompts, so the safeguards must be in the prompt, the repository and the branch rules. That is why this repository has a verifier, a backlog and a standing prompt file.

Facts from the documentation that shape the setup:

- The routine clones the repository's **default branch** at the start of each run. Anything not merged into it does not exist for the routine.
- Claude pushes to branches prefixed `claude/`, which are always accepted. Pushes to other branches are checked and rejected if the branch is protected.
- Commits and pull requests carry **your** GitHub identity.
- All your connected connectors are included by default, and Claude can use every tool of an included connector, including writes, without asking. Remove all of them.
- The **Default** environment has Trusted network access: package registries and common development domains only. This project needs nothing else.
- The schedule minimum is one hour. Runs may start a few minutes late. Times are entered in your local time zone.
- Routines count against a daily run cap and your subscription usage. A green status only means the session ran, not that the task succeeded.

## Part A. Get the repository ready

1. **Merge the files into the default branch.** Apply both patches (the `APPLY_PATCH.md` that came with them explains how), open the pull request and merge it with a merge commit. Until then the routine cannot see them.
2. **Run the checks on your own machine once:**
   ```bash
   python -m unittest discover -s tools/buggy_rules
   python -m unittest discover -s tools/exercise_pipeline
   python tools/exercise_pipeline/verify_items.py "exercises/grades1-6/*.json"
   ```
   Expect `OK`, `OK` and `no problems`.
3. **Protect the default branch on GitHub** (Settings, Branches): require a pull request before merging and require the `verify-exercises` check to pass. This makes the human review a rule, not a habit.
4. **Confirm that GitHub access is granted** for the repository to your Claude account (Claude Code on the web, or `/web-setup` in the CLI). For the optional GitHub trigger, install the Claude GitHub App on the repository.
5. **Read `docs/privacy/README.md`.** The routine uses synthetic data only. If anything in a run looks like pupil data, stop.

## Part B. Do a manual dry run first

Before scheduling anything, run the prompt once by hand so you can read every step.

1. Open Claude Code on the web (claude.ai/code), select the repository, and start a session.
2. Paste: `Follow ROUTINE_PROMPT_1-6.md in this repository.`
3. Watch it read the backlog, generate a batch, run the three checks, and open a pull request from a `claude/` branch.
4. Review the pull request as described in Part D. Fix the prompt file (through a pull request) if anything was unclear.

Repeat until a run needs no correction.

## Part C. Create the routine

On the web at <https://claude.ai/code/routines>, click **New routine**. Or run `/schedule` in the CLI and answer its questions.

| Field | Value |
|---|---|
| Name | `FinnMath grades 1-6 exercise batch` |
| Prompt | `Follow ROUTINE_PROMPT_1-6.md in this repository. Prepare one batch, verify it, open a pull request, and stop.` |
| Model | Choose one. Template-driven items rarely need the largest model. Move up only if reviews find quality problems. |
| Repository | The repository that contains this material. Add no other repository. |
| Environment | **Default** (Trusted network). No setup script is needed: the tools use the Python standard library. If you later read the workbook in the run, `openpyxl` is required; add `pip install openpyxl` as a setup script. |
| Trigger | **Schedule**, daily, for example 06:00 in your local time. See "How often" below. |
| Connectors | **Remove all.** The routine needs none. |

Click **Create**, then **Run now** on the detail page for the first scheduled-style run. Open the run and read the transcript. Do not trust the green status alone.

### How often

Start with **once a day** on weekdays. For a custom schedule, pick the closest preset in the form and then run `/schedule update` in the CLI to set a cron expression, for example `0 6 * * 1-5` for 06:00 on weekdays. Hourly is possible, but each run opens a pull request that a person must review; do not schedule faster than you can review. Runs that cannot fit under your daily cap or usage limit are rejected unless usage credits are on.

To test without using the daily cap, schedule a one-off run from the CLI, for example `/schedule tomorrow at 9am, follow ROUTINE_PROMPT_1-6.md`. One-off runs do not count against the daily routine cap.

## Part D. Review loop (every run)

1. Open the pull request from the `claude/` branch. The `verify-exercises` check must be green.
2. Read the three sample items shown in the pull request body, then read more. Check: is the task clear for the age, is there only one reasonable reading, is the Finnish natural, is the wrong answer the one the misconception really produces.
3. Reject or edit items you do not want. Delete an item by removing it from the batch file in the pull request.
4. A teacher sets `"status": "reviewed"` on items that pass, in a separate commit, and runs `python tools/exercise_pipeline/verify_items.py --allow-reviewed "exercises/grades1-6/*.json"`.
5. Merge with a **merge commit** (not squash), so the backlog file does not conflict on the next run.
6. Merge before the next run starts. Two open pull requests both edit `BACKLOG_1-6.md` and will conflict.

Reviewed items are still content only. They must not go in front of pupils until the expert sign-off is complete.

## Part E. Optional extras

- **GitHub trigger.** Add a second routine that starts on `pull_request.opened` filtered to head branch starts with `claude/`, whose prompt reads the pull request and checks each item against the rules in `ROUTINE_PROMPT_1-6.md`. Use it as a second pair of eyes, not a replacement for the teacher. GitHub webhook events have per-hour caps.
- **API trigger.** A routine can be started by an HTTP POST with a per-routine token, for example from a script. Store the token as a secret; it is shown once.
- **Your 7–9 routine.** The existing routine for grades 7–9 can stay as it is. Give this one its own name and prompt file. Do not put keys in the environment variables of either, because they are visible to anyone who uses that environment.

## Part F. If something goes wrong

| Symptom | Likely cause and fix |
|---|---|
| Run is green but nothing changed | Read the transcript. The backlog may have no qualifying row, or the prompt file is not on the default branch yet. |
| The routine cannot find `ROUTINE_PROMPT_1-6.md` | The files were not merged into the default branch. Merge, then run again. |
| Push rejected | The routine tried to push to a branch that is protected or not prefixed `claude/`. It must use a `claude/` branch. |
| `403` and `host_not_allowed` | A domain outside the Trusted list was requested. This project needs none. Do not widen network access; fix the prompt instead. |
| `/schedule` unknown | You are signed in with an API key or inside a cloud session, or an Owner turned routines off. Use the web form, or sign in with your claude.ai account. |
| "Routines are disabled by your organization's policy" | A Team or Enterprise Owner turned off the Routines toggle. Ask an Owner. |
| Run starts late | Stagger of a few minutes is normal. |
| Daily cap reached | Reduce frequency, or turn on usage credits. |
| Batch fails the verifier in CI | Read the `FAIL` lines. Fix the items, not the verifier. |

## Rules that never change

- No pupil data in the repository, the prompt, the environment or the routine's output.
- No connectors on this routine.
- `status` stays `draft` until a human reviews.
- Every change to the prompt or the tools goes through a pull request.
- Expert sign-off before any use with pupils: `docs/privacy/expert_review_signoff_template.md`.
