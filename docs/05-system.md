# 05 — System

`system/` is the production back end that keeps the knowledge base alive:

```
system/
  jobs/        Python entry points, one per automated job
  prompts/     Prompt files used by daily and weekly runs
  schedule.md  What runs when, and who gets the output
```

## Jobs

Jobs run on a schedule (cron, GitHub Actions, Airflow, or whatever you already have). Most jobs are a skill from `execution/skills/` running unattended with a prompt from `system/prompts/`, sending output to a known destination (Slack, email, a Sheet, a pull request).

The baseline job every Groundtruth instance should run:

| Job | Cadence | What it does |
|---|---|---|
| `kb-check` | daily, and on every pull request | `tools/kb.py check`: broken links, unowned or stale definitions, queries changed after certification, overdue decision reviews |

## Automated checks

*This section is being written.* It will cover the automated checks that make the system self-maintaining.

Next: [06 — Adoption](06-adoption.md)
