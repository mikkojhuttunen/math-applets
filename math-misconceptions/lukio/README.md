# math-misconceptions / lukio

Exercise bank for upper secondary mathematics (lukio: MAY1, lyhyt MAB, pitkä MAA), built around documented misconceptions and linked to LOPS 2019 goal IDs. Same idea as the 7–9 pipeline one folder up, with its own files.

**Status (2026-10-01): framework and research only.** No schema, scripts, generators or exercises yet; no routine. `BACKLOG_LUKIO.md` section 2 lists what has to be built before generation starts.

```
math-misconceptions/lukio/
  README.md                                   this file
  BACKLOG_LUKIO.md                            framework, work queue, coverage matrix, log
  data/curriculum/
    LOPS_2019_matematiikka_oppimistavoitteet.md   LOPS 2019 modules and goal IDs (MAY1.03, MAB4.02, MAA6.06), levels, year split
  data/misconceptions/
    lukio_misconceptions.md                   45 lukio misconception rows (LFUN-01 …) plus carried-over 1–9 rows
    math_misconceptions_lukio.bib             sources (DOIs to verify)
  docs/
    lukio_curriculum_and_misconceptions.md    research summary: sources, structure, what is known about misconceptions
  (planned) schema/, scripts/, tests/, generators/, exercises/<TopicID>/<TypeCode>.json, ROUTINE_PROMPT_LUKIO.md
```

## Rules

- Work in this folder only. The 7–9 files one level up (`../math-misconceptions-7-9grades-backlog.md`, `../sources/`, `../scripts/`, `../schema/`) are read only here.
- The routine, once it exists, pushes to `claude/exercises-lukio`. Merge it into `main` with a merge commit, never squash.
- New items are always `draft`; only a teacher sets `approved`.
- No student data. Item stems are new; YTL exam tasks and textbook tasks are not copied.
