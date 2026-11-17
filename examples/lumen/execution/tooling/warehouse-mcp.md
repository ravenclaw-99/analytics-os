---
id: tooling.warehouse-mcp
type: tooling
title: Warehouse connection
owner: data
status: reviewed
updated: 2026-10-01
system: Snowflake via MCP (read-only role)
tags: [tooling, warehouse]
---

## Connection
- Use the **read-only** `ANALYST_AI` role. Writes are never allowed from an agent session.
- Default warehouse `XS_AI`. Queries that scan more than 50 GB need a human to approve them.

## What works
- Run certified queries by name from `analytics-reference/data/certified-queries/`. Copy the SQL exactly.
- Always `limit` exploratory queries, and sample before full scans.

## Gotchas
- Timestamps are UTC. Finance reports in America/New_York, so convert before you bucket by day.
- `analytics.*` is the modeled layer. Don't query `raw_*` unless a source artifact tells you to.
