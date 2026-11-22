# execution/

How the AI *does* things with the analytics reference. Two subfolders:

- **`skills/`**: step-by-step playbooks for recurring analytical tasks, one folder per skill with a `SKILL.md`. They follow the Agent Skills format (YAML `name` + `description`, then instructions), so Claude and other compatible agents can load them directly.
- **`tooling/`**: how to use each connected system (warehouse, planning tool, spreadsheets) reliably: which MCP to use, the approach that works, and the gotchas.

Skills cite the analytics reference with `[[id]]` links, and `tools/kb.py check` verifies that every link resolves. If a definition is renamed, the skills that depend on it fail the check instead of silently drifting.

| Skill | What it does |
|---|---|
| [`compare-forecast-versions`](skills/compare-forecast-versions/SKILL.md) | Diff the latest forecast against an earlier version and explain the deltas in a standard format |
| [`answer-metric-question`](skills/answer-metric-question/SKILL.md) | Answer "what is our X?" using only certified definitions and queries |
| [`month-end-flux`](skills/month-end-flux/SKILL.md) | Explain month-over-month P&L changes by category and vendor, timing effects separated |
| [`board-prep-pivot`](skills/board-prep-pivot/SKILL.md) | Build the quarterly board tables from certified sources, reconciled to the last deck |
| [`find-prior-analyses`](skills/find-prior-analyses/SKILL.md) | Find analysis someone already did, across the knowledge base, memory, Slack, Drive, and GitHub |
| [`shareable-dashboard`](skills/shareable-dashboard/SKILL.md) | Turn a description into a published HTML dashboard in the house format |
| [`create-airflow-dag`](skills/create-airflow-dag/SKILL.md) | Write an ETL DAG with tests, open a PR, and draft the knowledge-base updates |
| [`review-kb-checks`](skills/review-kb-checks/SKILL.md) | Talk through the automated checks' findings and open one PR with the accepted fixes |

| Tooling | Covers |
|---|---|
| [`tooling.warehouse-mcp`](tooling/warehouse-mcp.md) | Read-only warehouse access and conventions |
| [`tooling.planning-mcp`](tooling/planning-mcp.md) | Planning tool versions and exports |
| [`tooling.google-sheets`](tooling/google-sheets.md) | Sheet output conventions |
| [`tooling.html-dashboards`](tooling/html-dashboards.md) | Publishing and house format for HTML dashboards |
| [`tooling.workspace-search`](tooling/workspace-search.md) | Searching Slack, Drive, GitHub, and agent memory |
| [`tooling.airflow`](tooling/airflow.md) | DAG conventions and PR-only changes |
