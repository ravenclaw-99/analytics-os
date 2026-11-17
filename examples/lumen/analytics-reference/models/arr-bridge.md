---
id: model.arr-bridge
type: model
title: ARR Bridge
owner: finance
status: reviewed
updated: 2026-06-10
kind: bridge
depends_on: [metric.arr, metric.net-revenue-retention, metric.logo-churn-rate]
tags: [revenue, board]
---

## Relationships
Lumen's application of [[framework.growth-accounting]] to ARR.

```
ARR_end = ARR_start
        + new            (customers with first paid subscription in period)
        + expansion      (existing customers, ARR up)
        − contraction    (existing customers, ARR down, still active)
        − churn          (existing customers, ARR to zero)
```
- Expansion, contraction, and churn together explain the gap between [[metric.net-revenue-retention]] and 100%.
- The churn component's count is [[metric.logo-churn-rate]] × customers at period start.

## Assumptions
- Movements are classified per [[entity.customer]], not per subscription, so a plan swap within one customer is expansion or contraction, not churn plus new.

## Sensitivities
- At Lumen's current mix, 1 point of monthly logo churn ≈ $0.9M of ARR per year.
