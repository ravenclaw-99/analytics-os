---
id: metric.dau
type: metric
title: Daily Active Users (DAU)
owner: product
status: reviewed
updated: 2026-07-22
unit: count
grain: daily (UTC), company
direction: up_is_good
implementation: analytics.fct_daily_active_users
depends_on: [entity.engagement-event]
tags: [product, engagement]
---

## Definition
Distinct users with at least one `workflow_run` on a given UTC day.

## Formula
`DAU = count(distinct user_id) where event = 'workflow_run'`, grouped by UTC day.

## Caveats
- Logins (`session_start`) don't count. Usage-alert emails inflate them; see [[source.product-events]].

## History
- **2026-07-22:** Switched from `session_start` to `workflow_run` after [[analysis.2026-07-usage-alerts-review]].
