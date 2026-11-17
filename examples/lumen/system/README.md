# system/

Everything described in `analytics-reference/` and `execution/` is a **snapshot**. An agent connected to your warehouse, GitHub, and Drive can read that snapshot, but the business keeps moving underneath it. Products launch, tables are deprecated, pipelines are re-architected, and people start analyzing things in new ways. Without maintenance, a knowledge base goes stale within weeks.

`system/` is the back end that keeps it current: five automated checks, human-in-the-loop at first.

| # | Check | Cadence | Question it answers |
|---|---|---|---|
| 1 | **Schema integrity** | daily | Does every table and column the knowledge base mentions still exist? Is every column of every key table documented? |
| 2 | **Semantic integrity** | weekly | Does the knowledge base agree with itself? Does every use of ARR or DAU match the one validated definition? |
| 3 | **Organizational cohesion & redundancy** | weekly | Can an agent find things fast? Is any knowledge stored twice? |
| 4 | **Proactive enrichment** | weekly | What changed this week (merged PRs, launches, decisions in Slack and decks) that the knowledge base doesn't reflect yet? |
| 5 | **Analytical gaps** | weekly | What are people analyzing that isn't documented, and should it become a metric or a skill? |

```
system/
  config.json      Warehouse schemas, canonical terms, structure rules, enrichment and gap sources
  schedule.md      What runs when, who reviews, how fixes get merged
  jobs/run.sh      Runner: deterministic pass, then agent pass
  prompts/         Agent instructions for each check (plus shared rules)
  reports/         Latest findings from each check (.md for people, .json for machines)
  state/           Watermarks between runs
  fixtures/        Simulated warehouse catalog for this example
```

Try it on the example (from `examples/lumen/`):

```bash
CATALOG=system/fixtures/catalog.json system/jobs/run.sh schema-integrity
system/jobs/run.sh semantic-integrity
system/jobs/run.sh cohesion-redundancy
```

The example has deliberate drift built in: a renamed NRR table, a renamed and an undocumented column, a planning-tool "ARR" that includes one-time fees, and a copy-pasted known issue. The committed reports in `reports/` show what the checks find.
