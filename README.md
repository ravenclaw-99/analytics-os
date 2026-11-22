# Canonical

**A recursive, self-improving knowledge base that serves as the analytical foundation for product, data science, finance, and BizOps teams, and for the AI agents that work alongside them.**

---

## The problem

Every company's analytical knowledge is scattered. Metric definitions sit in a BI tool. Caveats live in one analyst's head. The validated query for ARR is in someone's personal folder. The tried-and-true way to compare two forecast versions exists only as muscle memory.

People get by on tribal knowledge. AI can't. Point an LLM at your warehouse and it will happily compute "churn" four different ways, none of them yours. The bottleneck for AI in analytics isn't model capability. It's **context**.

And even after you write it all down, **it goes stale.** Every week, products launch, tables get deprecated, pipelines get re-architected, and people start analyzing things in new ways. A knowledge base that's accurate on day one is quietly wrong a month later, and an AI working from it is confidently wrong.

## The idea

One version-controlled repository, shared across teams, with three folders:

```
your-kb/
  AGENTS.md               Ground rules any AI agent reads first
  analytics-reference/    The content house: what the company knows
  execution/              How work gets done: skills + tooling
  system/                 What keeps it alive: jobs, prompts, automated checks
```

| Folder | What lives there |
|---|---|
| **analytics-reference/** | Metric definitions (ARR, NRR, cohort retention, funnel conversion) · **certified** tables and queries · data sources and their known issues · finance registers (vendors, billing cycles, AP/AR) · product and engagement mappings · how the financial model is built · horizontal frameworks (growth accounting, mix shift) · history of analyses and decisions |
| **execution/** | **Skills**: step-by-step playbooks an AI follows for recurring work, like comparing this forecast with the one from three weeks ago in a standard format · **Tooling**: how to use each connected system (warehouse, Pigment/Anaplan, Google Sheets) through its MCP reliably |
| **system/** | Production code: scheduled jobs, the prompts they run, and **five automated checks** that keep the reference true |

### The five checks

| # | Check | Cadence | Catches |
|---|---|---|---|
| 1 | **Schema integrity** | daily | Tables and columns the knowledge base mentions that no longer exist; key-table columns nobody documented |
| 2 | **Semantic integrity** | weekly | Two definitions of ARR; any part of the knowledge base that disagrees with another |
| 3 | **Cohesion & redundancy** | weekly | Knowledge an agent can't find quickly; the same fact stored in three places |
| 4 | **Proactive enrichment** | weekly | Merged PRs, launches, and decisions in Slack and decks that the knowledge base doesn't reflect yet |
| 5 | **Analytical gaps** | weekly | Analysis people keep doing that isn't captured as a metric or skill. It asks the team whether to add it |

Every check is **human-in-the-loop** to start. Each finding gets a reference code and a recommended **accept / reject / refine**. A summary of each check goes to Slack for everyone to see. The knowledge-base owner then runs a **review skill** in their own LLM tool to talk each finding through and turn the accepted fixes into one pull request. A review ledger records every decision. Rejected findings stay rejected, recommendations recalibrate toward what people actually decide, and kinds of finding that reach 90%+ agreement become eligible to auto-accept. See [docs/05-system.md](docs/05-system.md) and [docs/06-runtime.md](docs/06-runtime.md).

The runtime is vendor-neutral: any scheduler, any sandbox, any agent CLI (frontier or open-source), any read-only MCP servers. A reference implementation runs on GitHub Actions and works end to end on the example without accounts or API keys.

### Why "recursive"

Execution reads the reference. System runs execution on a schedule and checks the reference for drift. Every analysis and every decision review writes what it learned back into the reference: a new known issue, a sharper caveat, a corrected assumption. **The knowledge base gets more accurate the more it's used.** Most data stacks wear out over time. This one compounds.

## Principles

1. **Plain text over platforms.** Markdown with frontmatter in Git. It works in Obsidian, any editor, and any LLM's context window.
2. **Define once, reference everywhere.** Skills link to definitions. They never copy them.
3. **Certified or it doesn't count.** A governed metric has an owner and a reconciled, certified query.
4. **Decisions are artifacts.** Log the expected outcome and a review date, then check.
5. **Agents draft, humans certify.** AI proposes changes as pull requests. People approve them.

## Quick start

No dependencies, only Python 3.9+.

```bash
# Validate the example: schema, broken links (including inside skills), certification drift, overdue reviews
python3 tools/kb.py check examples/lumen

# Build a machine-readable graph (index.json) and a browsable INDEX.md
python3 tools/kb.py index examples/lumen

# Run the automated checks against the example's deliberately drifted warehouse
cd examples/lumen
CATALOG=system/fixtures/catalog.json system/jobs/run.sh schema-integrity
system/jobs/run.sh semantic-integrity
system/jobs/run.sh cohesion-redundancy

# The runtime: one summary per check (printed, not posted), the review queue, and the learning loop
python3 ../../tools/runtime/cli.py notify . --to slack     # dry run unless --send and a webhook are set
python3 ../../tools/runtime/cli.py findings .              # open findings with their reference codes
python3 ../../tools/runtime/cli.py stats .                 # agreement with human reviewers (simulated history)
```

To start your own, copy `templates/` and follow [docs/07-adoption.md](docs/07-adoption.md).

## Repository layout

```
docs/
  01-why.md                 The argument
  02-architecture.md        The three folders and how they fit together
  03-analytics-reference.md What goes in the content house; artifact format
  04-execution.md           Skills and tooling; working with AI
  05-system.md              Keeping it alive: the five automated checks
  06-runtime.md             How checks run: scheduler → sandbox → agent + MCP → report → Slack → review → autonomy
  07-adoption.md            The first 30 days, by function
templates/                  Starter knowledge base to copy: AGENTS.md, the three folders, blank artifacts
examples/lumen/             A worked example: a fictional B2B SaaS company
tools/kb.py                 Validator + indexer (stdlib only)
tools/checks/               Deterministic passes for checks 1–3
tools/runtime/              Delivery, review ledger, learning loop, autonomy ladder
.github/workflows/          CI, plus a scheduled run of the checks (dry run by default)
```

## Status

v0.1, an early public draft. Feedback and issues are welcome.

## License

MIT. See [LICENSE](LICENSE).
