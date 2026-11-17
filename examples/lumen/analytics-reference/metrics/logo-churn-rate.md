---
id: metric.logo-churn-rate
type: metric
title: Logo Churn Rate
owner: bizops
status: reviewed
updated: 2026-07-22
unit: percent
grain: monthly, company
direction: down_is_good
implementation: models/marts/fct_logo_churn_monthly.sql
depends_on: [entity.customer]
tags: [retention]
---

## Definition
The share of customers active at the start of a month who have no active paid subscription at the end of it.

## Formula
`churned customers in month / customers active at start of month`

## Caveats
- Accounts with churn reason `merged` are excluded.
- **Leading indicators must use `workflow_run`, not logins.** *(Added 2026-07-22 from [[analysis.2026-07-usage-alerts-review]].)* Login-based "at-risk" scores became inflated after the April 2026 usage-alert launch.

## History
- **2026-07-22:** Caveat added. The definition itself is unchanged.
