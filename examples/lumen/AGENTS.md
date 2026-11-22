# AGENTS.md: Lumen analytics knowledge base

You are working with Lumen's analytics knowledge base. Lumen sells a workflow tool to operations teams on monthly and annual plans, about $8M ARR. (Lumen is fictional.)

## Layout

| Folder | What's in it | How you use it |
|---|---|---|
| `analytics-reference/` | The content house: metric definitions, certified queries, data sources and entities, finance registers, product mappings, horizontal frameworks, and the history of analyses and decisions | **Read** it. It's the source of truth |
| `execution/skills/` | Step-by-step playbooks for recurring tasks | **Follow** the matching skill when a request fits one |
| `execution/tooling/` | How to use each connected system (warehouse, planning tool, Sheets) | **Read** it before calling that system's MCP |
| `system/` | Production jobs and prompts | Don't modify it from an analysis session |

Each artifact has frontmatter with an `id` (e.g. `metric.arr`). Body text links to other artifacts as `[[id]]`. If `index.json` exists, load it first: it's the whole graph.

## Ground rules

1. **Use governed definitions.** Metrics come from `analytics-reference/metrics/`. Never invent or substitute a definition. If one doesn't exist, say so and propose a `draft`.
2. **Use certified queries** for governed metrics (`analytics-reference/data/certified-queries/`). Don't write fresh SQL for a number that already has a certified query.
3. **Cite artifact ids** for every number, definition, and claim.
4. **Read the caveats and known issues** of everything you touch before you answer.
5. **Check `analytics-reference/history/`** for prior work before starting new analysis. If it isn't there, the `find-prior-analyses` skill also searches Slack, Drive, GitHub, and agent memory.
6. **State your confidence** (low, medium, or high) and say why.
7. **Write back as drafts.** New or edited artifacts get `status: draft` and go through a pull request. Only humans set `reviewed`.
