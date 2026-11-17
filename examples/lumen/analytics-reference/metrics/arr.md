---
id: metric.arr
type: metric
title: Annual Recurring Revenue (ARR)
owner: finance
status: reviewed
updated: 2026-06-10
unit: usd
grain: daily snapshot, company
direction: up_is_good
implementation: query.fct-arr-daily
depends_on: [query.fct-arr-daily, entity.subscription, entity.customer]
tags: [revenue, board]
---

## Definition
The annualized value of all active, paid, recurring subscriptions on a given day, after discounts and excluding one-time fees.

## Formula
`ARR = Σ (monthly-normalized subscription price × quantity) × 12` over active subscriptions in [[entity.subscription]]. Computed **only** by the certified query [[query.fct-arr-daily]].

## Caveats
- Annual plans are normalized to monthly before ×12. Never use invoice amounts (see [[source.stripe]] known issues).
- Paused subscriptions are excluded.

## History
- **2026-06-10:** Discounts are now netted in ARR (previously reported gross). Restated back to January 2025.
