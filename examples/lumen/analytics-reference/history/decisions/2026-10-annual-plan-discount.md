---
id: decision.2026-10-annual-plan-discount
type: decision
title: Increase the annual-plan discount from 10% to 17%
owner: bizops
status: reviewed
updated: 2026-10-01
decided_on: 2026-10-01
review_on: 2027-01-15
outcome: pending
depends_on: [analysis.2026-09-churn-by-cohort, model.arr-bridge, metric.arr]
tags: [pricing, retention]
---

## Decision
Raise the annual-plan discount to 17% (two months free) for new and renewing customers, starting 2026-10-15.

## Rationale
[[analysis.2026-09-churn-by-cohort]] shows annual customers churn materially less, even after controlling for size. Per [[model.arr-bridge]], a 10-point shift in annual mix outweighs the discount within about 14 months.

## Expected outcome
- Annual share of new bookings rises from 31% to ≥ 40% by 2027-01-15.
- Near-term [[metric.arr]] dips by no more than 1.5% from discounting.

## Alternatives considered
- Discount for new customers only: rejected, because renewals are where conversion is cheapest.
- Annual-only pricing for small plans: deferred, as too much risk to top-of-funnel conversion.
