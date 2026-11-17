---
id: tooling.google-sheets
type: tooling
title: Google Sheets output
owner: bizops
status: reviewed
updated: 2026-10-01
system: Google Drive / Sheets via MCP
tags: [tooling, output]
---

## Conventions
- Create output in the shared `AI Outputs/` Drive folder, never in someone's personal drive.
- Name files `YYYY-MM-DD — <skill> — <short description>`.
- The first tab is always `summary`. Put the data in later tabs. Freeze the header rows.
- Write numbers as numbers, not formatted strings, and apply number formats afterwards.
- Add a `sources` tab that lists every artifact id and query used.
