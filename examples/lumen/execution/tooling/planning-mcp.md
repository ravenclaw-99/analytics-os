---
id: tooling.planning-mcp
type: tooling
title: Planning tool connection (Pigment / Anaplan)
owner: finance
status: draft
updated: 2026-11-01
system: Planning tool via MCP
tags: [tooling, fp&a]
---

## Connection
Lumen's forecast lives in the planning tool. Tool names vary by vendor and MCP server version, so **list the available tools at the start of each session** and map them to the steps below.

## What works
- **Identify versions by id, not by name.** Version names like "Latest" or "Board" get reused.
- Export the **same scenario, time range, and dimensions** for both versions in a comparison. Changing the cut makes the deltas meaningless.
- Read the version change log (if the MCP exposes it). It's the best source for explaining *why* an assumption moved.

## Gotchas
- Some exports return formatted strings ("$1.2M"). Request raw values.
- Large exports may paginate. Confirm that the row count matches the dimension cardinality.

*Status: draft. Confirm these patterns against your planning tool's MCP before relying on them.*
