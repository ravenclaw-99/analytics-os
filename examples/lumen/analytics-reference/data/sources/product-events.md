---
id: source.product-events
type: source
title: Product event stream
owner: data
status: reviewed
updated: 2026-07-22
system: Segment → warehouse
sync: Streaming, ~15 minutes latency, into raw_events.*
tags: [product, usage]
---

## Authoritative for
- Logins, workflow runs, seat activity
- Workspace-level usage (`workspace_id`)

## Not authoritative for
- Anything about billing or plan (see [[source.stripe]])

## Tables
- `raw_events.tracks`, `raw_events.identifies`

## Known issues
- **Workspaces ≠ customers.** One billing account can own several workspaces. Join through `dim_workspace_customer`, never on email domain.
- **Usage-alert emails trigger a login event.** *(Added 2026-07-22 from [[analysis.2026-07-usage-alerts-review]].)* Since the April 2026 usage-alert launch, clicking an alert email logs a `session_start` even when the user takes no action. Use `workflow_run`, not `session_start`, as the signal for activity.
