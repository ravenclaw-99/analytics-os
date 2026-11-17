# Schedule

Every check starts **human-in-the-loop**: it writes a report (and optionally a draft pull request) and changes nothing on its own. Graduate a check to auto-fixing a category of finding only after it has a track record. Start with low-risk categories, such as adding a missing column to the key-tables register.

| # | Check | Cadence | Runs | Needs | Output goes to |
|---|---|---|---|---|---|
| 0 | `kb-check` (lint) | every PR + daily | `tools/kb.py check` | nothing | CI status |
| 1 | `schema-integrity` | **daily**, 06:00 | deterministic | warehouse catalog (MCP / CLI) | `#data-quality`; data owner |
| 2 | `semantic-integrity` | **weekly**, Mon | deterministic + agent | knowledge base only | canonical artifacts' owners |
| 3 | `cohesion-redundancy` | **weekly**, Mon | deterministic + agent | knowledge base only | knowledge-base maintainer |
| 4 | `proactive-enrichment` | **weekly**, Fri | agent | GitHub, Slack, Drive MCPs | owners of affected artifacts |
| 5 | `analytical-gaps` | **weekly**, Fri | agent | Slack, Drive, query history, agent logs | BizOps / analytics lead |

## Review loop

1. The job writes `system/reports/<check>.md` and `.json`. If the runner has repo write access, it also opens a pull request with `status: draft` changes only.
2. A named reviewer (above) acts on each finding, guided by the system's recommended action: **accept** (merge the fix), **reject** (note why, so the check learns), or **refine** (say what to change, and the agent re-proposes).
3. Accepted fixes are merged. Then `tools/kb.py check` runs on the pull request as a gate.

## Example: GitHub Actions

```yaml
on:
  schedule:
    - cron: "0 6 * * *"   # daily: schema integrity
    - cron: "0 7 * * 1"   # Mondays: semantic + cohesion
    - cron: "0 7 * * 5"   # Fridays: enrichment + gaps
```
Each cron entry calls `system/jobs/run.sh <check>` after exporting the catalog, with `AGENT_CMD` pointed at a headless agent that has the right MCP servers and a read-only role.
