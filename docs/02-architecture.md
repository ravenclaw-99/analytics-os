# 02 — Architecture

A Groundtruth knowledge base is a Git repository shared by the analytics, finance, product, and BizOps teams. It has three top-level folders:

```
your-kb/
  AGENTS.md               Ground rules any AI agent reads first
  analytics-reference/    The content house: what the company knows
  execution/              How work gets done: skills + tooling
  system/                 What keeps it alive: jobs, prompts, automation
```

| Folder | Role | Who writes it | Who reads it |
|---|---|---|---|
| **analytics-reference/** | The source of truth: definitions, certified queries, mappings, frameworks, history | Analysts, finance, data; agents propose drafts | Everyone, and every agent |
| **execution/** | Repeatable playbooks (skills) and connection guides (tooling) | Whoever owns the workflow | Agents, when doing a task |
| **system/** | Production code: scheduled jobs, the prompts they run, automated checks | Whoever owns the platform | The scheduler |

## How the three fit together

```
            ┌────────────────────────────┐
            │     analytics-reference    │  ◀── the content house
            │  metrics · queries · data  │
            │  finance · product · ...   │
            └──────▲──────────────┬──────┘
         writes    │              │  reads
         back      │              ▼
     ┌─────────────┴──┐      ┌─────────────────┐
     │     system     │      │    execution    │
     │ jobs · prompts │─────▶│ skills · tooling│ ──▶ answers, sheets,
     │ automated      │ runs │                 │     forecasts, decks
     │ checks         │      └─────────────────┘
     └────────────────┘
```

- **Execution reads reference.** A skill like `compare-forecast-versions` doesn't define ARR. It links to `[[metric.arr]]` and `[[model.arr-bridge]]`. Change the definition once, and every skill that uses it inherits the change.
- **System runs execution on a schedule.** The daily and weekly jobs are mostly skills that run without a person in the loop, using prompts kept in `system/prompts/`.
- **System writes back to reference.** Automated checks catch drift (a certified query edited without re-certification, a metric with no owner, a decision past its review date, a source whose data stopped matching) and open pull requests or alerts. Analyses and decision reviews add new caveats and known issues.

## Why it's recursive

Most data stacks decay: people leave, definitions drift, dashboards rot. Here, every use of the system can improve it:

1. An analysis uses the reference and finds a data quirk → the quirk becomes a **known issue** on the source.
2. A decision is logged with an expected outcome and a review date → the review becomes a **new analysis** → its findings update metric caveats and model assumptions.
3. Automated checks run every day → anything stale, unowned, or broken gets surfaced before someone relies on it.

The reference gets more accurate the more it's used, and every agent and analyst after that starts from a better base.

Next: [03 — Analytics reference](03-analytics-reference.md)
