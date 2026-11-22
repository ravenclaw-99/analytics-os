# 04 — Execution

`execution/` is where the reference turns into work. It has two parts.

## Skills

A **skill** is a step-by-step playbook for a recurring analytical task: the tried-and-true way to do it, written down once, so that any analyst or AI agent produces the same standardized output.

Each skill is a folder with a `SKILL.md`, in the open Agent Skills format: YAML frontmatter with `name` and `description`, then instructions. Claude and other compatible agents can load these directly. The `description` tells the agent *when* to use the skill.

Examples:

| Skill | What it does |
|---|---|
| `compare-forecast-versions` | Pull the latest forecast and the version from ~3 weeks ago from the planning tool, attribute the deltas to drivers, write a standard variance sheet with commentary |
| `answer-metric-question` | Answer "what's our X?" using only governed definitions and certified queries, with caveats and a confidence level |
| `month-end-flux` | Explain month-over-month P&L changes by expense category and vendor, separating timing effects (accruals, prepaids, reclasses) from real changes |
| `board-prep-pivot` | Build the quarterly board tables (ARR bridge, retention, cohorts, P&L and cash vs. plan) from certified sources, reconciled to the last deck |
| `find-prior-analyses` | Search the knowledge base, agent memory, Slack, Drive, and GitHub in a fixed order for analysis someone already did, and offer to save it to `history/` |
| `shareable-dashboard` | Turn a description into a self-contained HTML dashboard in the house format, with governed definitions in the footer, and publish it internally |
| `create-airflow-dag` | Write a new ETL DAG with tests, open it as a pull request, and draft the knowledge-base updates for the new table |

All seven are in `examples/lumen/execution/skills/`, next to `review-kb-checks`, the skill for reviewing check findings (see [05 — System](05-system.md)). A blank skill is in `templates/blanks/skill/SKILL.md`.

**A skill can also write back.** `find-prior-analyses` offers to save what it finds as a draft analysis, and `create-airflow-dag` drafts the key-tables entry for the table it creates. That's how the reference keeps up with the work.

**Skills reference, they don't redefine.** A skill links to `[[metric.arr]]`; it never restates the formula. The checker verifies every link in every skill, so renaming or removing a definition fails the check and doesn't silently break a workflow.

## Tooling

A **tooling** artifact documents how to use one connected system reliably: which MCP server or connector, which role or permissions, the approach that works, and the gotchas.

| Tooling | Covers |
|---|---|
| `tooling.warehouse-mcp` | Read-only role, cost limits, run certified queries by name, timezone conventions |
| `tooling.planning-mcp` | Pigment / Anaplan: identify versions by id, export identical cuts, request raw values |
| `tooling.google-sheets` | Output folder, naming, summary-tab-first, a `sources` tab citing every artifact |
| `tooling.html-dashboards` | Where internal dashboards are published, and the house format: header, stat tiles, number formats, definitions footer |
| `tooling.workspace-search` | Search syntax and scopes for Slack, Drive, GitHub, and agent memory files |
| `tooling.airflow` | DAG conventions, idempotent loads, read-only API access, PR-only changes |

Skills link to tooling (`[[tooling.planning-mcp]]`), so connection know-how lives in one place.

## Working with AI: the rules

- **`AGENTS.md` at the root** sets the ground rules: use governed definitions, use certified queries, cite artifact ids, state confidence.
- **Traverse, don't search.** To answer "why did NRR drop?", walk the graph: the metric and its caveats → the certified query → the sources and their known issues → the model above it → prior analyses and decisions. `tools/kb.py index` emits `index.json`, the whole graph in one file.
- **Agents draft, humans certify.** Agent-written artifacts are `status: draft` and arrive as pull requests. Only humans mark something `reviewed` or certify a query.

Next: [05 — System](05-system.md)
