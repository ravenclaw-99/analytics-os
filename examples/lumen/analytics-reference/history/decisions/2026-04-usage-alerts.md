---
id: decision.2026-04-usage-alerts
type: decision
title: Launch usage-alert emails for low-activity customers
owner: bizops
status: reviewed
updated: 2026-07-22
decided_on: 2026-04-02
review_on: 2026-07-15
outcome: mixed
depends_on: [metric.logo-churn-rate, model.arr-bridge]
tags: [retention]
---

## Decision
Send automated weekly usage summaries and "you haven't run a workflow in 14 days" alerts to admins of low-activity customers.

## Rationale
Churn in the bottom activity quartile runs at roughly 3× the company average (per [[metric.logo-churn-rate]]). Per [[model.arr-bridge]], halving that gap is worth about $250K of ARR per year.

## Expected outcome
Monthly logo churn in the low-activity cohort falls from 3.1% to < 2.5% within one quarter.

## Alternatives considered
- CSM outreach to every low-activity account: rejected, because at current headcount it doesn't scale.

## Review
Reviewed in [[analysis.2026-07-usage-alerts-review]]. Outcome: **mixed** (2.6%, just short of target).
