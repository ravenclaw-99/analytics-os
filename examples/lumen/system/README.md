# system/

The production back end that keeps this knowledge base alive: scheduled jobs, the prompts they run, and the scripts behind them.

```
system/
  jobs/       Python entry points, one per automated job
  prompts/    Prompt files used by daily / weekly runs
  schedule.md What runs when, and who gets the output
```

## Jobs

| Job | Cadence | What it does |
|---|---|---|
| `kb-check` | daily | Runs `tools/kb.py check`: broken links, unowned or stale definitions, overdue decision reviews |
| *automation checks* | *TBD* | *To be defined* |

> The automated checks that make the system self-maintaining will be documented here.
