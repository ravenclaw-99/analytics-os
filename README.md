# Groundtruth

**A recursive knowledge base that serves as the analytical foundation for product, data science, finance, and BizOps teams, and for the AI agents that work alongside them.**

> *Groundtruth* is a working name. The ideas matter more than the label.

---

## The problem

Every company's analytical knowledge is scattered. Metric definitions sit in a BI tool. Caveats live in one analyst's head. The validated query for ARR is in someone's personal folder. The tried-and-true way to compare two forecast versions exists only as muscle memory.

People get by on tribal knowledge. AI can't. Point an LLM at your warehouse and it will happily compute "churn" four different ways, none of them yours. The bottleneck for AI in analytics isn't model capability. It's **context**.

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
| **system/** | Production code: scheduled daily and weekly jobs, the prompts they run, and the automated checks that keep the reference accurate |

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
```

To start your own, copy `templates/` and follow [docs/06-adoption.md](docs/06-adoption.md).

## Repository layout

```
docs/
  01-why.md                 The argument
  02-architecture.md        The three folders and how they fit together
  03-analytics-reference.md What goes in the content house; artifact format
  04-execution.md           Skills and tooling; working with AI
  05-system.md              Jobs, prompts, automated checks
  06-adoption.md            The first 30 days, by function
templates/                  Blank artifacts and a skill template
examples/lumen/             A worked example: a fictional B2B SaaS company
tools/kb.py                 Validator + indexer (stdlib only)
```

## Status

v0.1, an early public draft. Feedback and issues are welcome.

## License

MIT. See [LICENSE](LICENSE).
