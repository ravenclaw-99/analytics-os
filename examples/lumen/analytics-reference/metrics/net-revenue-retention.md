---
id: metric.net-revenue-retention
type: metric
title: Net Revenue Retention (NRR)
owner: finance
status: reviewed
updated: 2026-06-10
unit: percent
grain: trailing 12 months, company
direction: up_is_good
implementation: analytics.fct_nrr_monthly
depends_on: [metric.arr, entity.customer]
tags: [revenue, retention, board]
---

## Definition
Of the ARR we had from customers 12 months ago, what share do those same customers generate today, including expansion and net of contraction and churn?

## Formula
`NRR = ARR_today(cohort) / ARR_12mo_ago(cohort)`, where the cohort is every [[entity.customer]] active 12 months ago.

## Caveats
- New customers acquired in the window are **excluded** by construction.
- Merged accounts (see [[entity.customer]]) are treated as continuous, not as churn plus a new customer.

## History
- **2026-06-10:** Inherits the net-of-discount change in [[metric.arr]].
