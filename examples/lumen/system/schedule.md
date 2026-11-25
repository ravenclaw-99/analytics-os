# Schedule

Every check starts **human-in-the-loop**: it writes a report (and optionally a draft pull request) and changes nothing on its own. Graduate a check to auto-fixing a category of finding only after it has a track record. Start with low-risk categories, such as adding a missing column to the key-tables register.

| # | Check | Cadence | Runs | Needs | Output goes to |
|---|---|---|---|---|---|
| 0 | `kb-check` (lint) | every PR + daily | `tools/kb.py check` | nothing | CI status |
| 1 | `schema-integrity` | **daily**, 06:00 | deterministic | warehouse catalog (MCP / CLI) | `#data-quality`; data owner |
| 2 | `semantic-integrity` | **weekly**, Tue | deterministic + agent | knowledge base only | canonical artifacts' owners |
| 3 | `cohesion-redundancy` | **weekly**, Tue | deterministic + agent | knowledge base only | knowledge-base maintainer |
| 4 | `proactive-enrichment` | **weekly**, Fri | agent | GitHub, Slack, Drive MCPs | owners of affected artifacts |
| 5 | `analytical-gaps` | **weekly**, Fri | agent | Slack, Drive, query history, agent logs | BizOps / analytics lead |

## Review loop

1. The job (`system/jobs/pipeline.sh <check>`) writes `system/reports/<check>.md` and `.json`. If the reviewer agent is on for the check (`config.json` → `autonomy.reviewer_agent`), it adds a second opinion per finding. Then it posts one summary to `#data-quality`, with a code per finding.
2. The named reviewer (above) runs the `review-kb-checks` skill in their own LLM tool, whenever suits them. For each finding they **accept** (the fix goes into the PR), **reject** (note why, so the check learns and stops repeating it), or **refine** (say what to change, and the agent re-proposes).
3. The skill opens one pull request with the accepted fixes and the ledger update. `tools/kb.py check` runs on it as a gate.
4. Kinds of finding that reach ≥ 90% agreement over ≥ 20 reviews become eligible for auto-accept. The owner switches each one on in `config.json` → `autonomy.auto_accept`.

## GitHub Actions

`.github/workflows/kb-checks.yml` (at the repo root) runs this schedule:

```yaml
on:
  schedule:
    - cron: "0 6 * * *"   # daily: schema integrity
    - cron: "0 7 * * 2"   # Tuesdays: semantic + cohesion
    - cron: "0 7 * * 5"   # Fridays: enrichment + gaps
```
Each entry exports the warehouse catalog, then calls `system/jobs/pipeline.sh <check>`, with `AGENT_CMD` pointed at a headless agent that has the right MCP servers and a read-only role. It stays a dry run (summaries printed to the log, not posted) until the repo variable `CANONICAL_SEND` is `true` and the webhook secret is set. The same pipeline runs under any other scheduler: Airflow, Cloud Scheduler, or cron.
