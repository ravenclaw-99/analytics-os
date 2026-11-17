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
| `build-scenario-sheet` | Create a Google Sheet comparing forecast scenarios in the house format |
| `month-end-flux` | Explain month-over-month variances on the P&L by vendor and category |

**Skills reference, they don't redefine.** A skill links to `[[metric.arr]]`; it never restates the formula. The checker verifies every link in every skill, so renaming or removing a definition fails the check and doesn't silently break a workflow.

## Tooling

A **tooling** artifact documents how to use one connected system reliably: which MCP server or connector, which role or permissions, the approach that works, and the gotchas.

| Tooling | Covers |
|---|---|
| `tooling.warehouse-mcp` | Read-only role, cost limits, run certified queries by name, timezone conventions |
| `tooling.planning-mcp` | Pigment / Anaplan: identify versions by id, export identical cuts, request raw values |
| `tooling.google-sheets` | Output folder, naming, summary-tab-first, a `sources` tab citing every artifact |

Skills link to tooling (`[[tooling.planning-mcp]]`), so connection know-how lives in one place.

## Working with AI: the rules

- **`AGENTS.md` at the root** sets the ground rules: use governed definitions, use certified queries, cite artifact ids, state confidence.
- **Traverse, don't search.** To answer "why did NRR drop?", walk the graph: the metric and its caveats → the certified query → the sources and their known issues → the model above it → prior analyses and decisions. `tools/kb.py index` emits `index.json`, the whole graph in one file.
- **Agents draft, humans certify.** Agent-written artifacts are `status: draft` and arrive as pull requests. Only humans mark something `reviewed` or certify a query.

Next: [05 — System](05-system.md)
