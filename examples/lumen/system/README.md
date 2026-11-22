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
  config.json      Warehouse schemas, canonical terms, structure rules, enrichment and gap sources, autonomy settings
  schedule.md      What runs when, who reviews, how fixes get merged
  jobs/run.sh      One check: deterministic pass, then agent pass
  jobs/pipeline.sh A full scheduled run: check → reviewer agent → Slack summary (dry run by default)
  prompts/         Agent instructions for each check, the reviewer agent, and shared rules
  reports/         Latest findings from each check (.md for people, .json for machines)
  state/           What carries over between runs: watermarks, the review ledger, calibration, lessons
  fixtures/        Simulated warehouse catalog for this example
```
Try it on the example (from `examples/lumen/`):

```bash
CATALOG=system/fixtures/catalog.json system/jobs/pipeline.sh schema-integrity
system/jobs/pipeline.sh semantic-integrity
system/jobs/pipeline.sh cohesion-redundancy
python3 ../../tools/runtime/cli.py findings .   # what's waiting for review, with codes
python3 ../../tools/runtime/cli.py stats .      # how often reviewers agreed with the recommendations
```

The example has deliberate drift built in: a renamed NRR table, a renamed and an undocumented column, a planning-tool "ARR" that includes one-time fees, and a copy-pasted known issue. The committed reports in `reports/` show what the checks find.

## Reviewing findings

Each finding has a code like `SCH-3eb1e7`. The Slack summary lists them. To act, the knowledge-base owner runs the [`review-kb-checks`](../execution/skills/review-kb-checks/SKILL.md) skill in their own LLM tool: it explains each finding, records accept, refine, or reject in `state/review-ledger.jsonl`, and opens one pull request with the fixes. See [docs/06-runtime.md](../../../docs/06-runtime.md).

**About the ledger in this example:** `state/review-ledger.jsonl` ships with eight weeks of *simulated* decisions (every line has `"simulated": true`), so `stats`, `autonomy`, and `learn` have a history to work from. `state/calibration.json` and `state/review-lessons.md` were generated from it. Delete all three to start with a clean slate.
