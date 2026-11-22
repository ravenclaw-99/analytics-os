---
id: tooling.workspace-search
type: tooling
title: Searching Slack, Drive, GitHub, and agent memory
owner: bizops
status: reviewed
updated: 2026-11-22
system: Slack, Google Drive, and GitHub via MCP; local agent memory files
tags: [tooling, search, history]
---

## Connection
Four places hold past analytical work that never made it into `analytics-reference/history/`. Each one has its own connection and search syntax:

| Where | Connection | Best for |
|---|---|---|
| Slack | Slack MCP (read-only, search scope) | Quick answers and "here's the number" threads |
| Google Drive | Drive MCP (read-only) | Decks, memos, and the spreadsheets behind them |
| GitHub | GitHub MCP (read-only) | Notebooks and SQL in `lumen/analytics-notebooks`; pipeline changes in `lumen/data-pipelines` |
| Agent memory | Local files on the analyst's machine (for example Claude Code memory folders or exported chat notes) | "I asked an AI to do this once" work. Read only with the analyst's permission |

## What works
- **Search narrow first, then widen.** Start with the exact metric name plus one distinctive word (a segment, a cohort, a vendor) and a date window. Only drop terms if nothing comes back.
- **Slack:** use `in:#channel`, `from:@person`, `after:YYYY-MM-DD`, and quoted phrases. Analysis usually lives in `#ask-data`, `#analytics`, `#finance`, and `#bizops`. Open the whole thread, because the final answer is often a later reply.
- **Drive:** search titles first (`title contains '…'`), then full text. Analyses usually sit in `Analytics/Ad hoc` and `Finance/Board`. Look at the modified date and the owner: the newest copy isn't always the final one.
- **GitHub:** code search with `repo:` and `path:` qualifiers, for example `repo:lumen/analytics-notebooks path:cohorts/ nrr`. Commit messages and PR descriptions often explain *why* an analysis was done.
- **Synonyms:** people rarely use the governed name. Search for the informal names too ("net retention", "churn by plan", "annual vs monthly"), then map what you find back to the governed definitions.

## Gotchas
- Slack search returns messages, not threads. A hit in a thread reply needs the parent message for context.
- Drive full-text search doesn't index spreadsheet cell contents reliably. Search sheet titles and the docs that link to them.
- Private channels and personal drives are out of scope unless the analyst explicitly adds them. Never quote private content into a shared artifact.
- Memory files may hold personal notes. Pull only the parts about the analysis.
