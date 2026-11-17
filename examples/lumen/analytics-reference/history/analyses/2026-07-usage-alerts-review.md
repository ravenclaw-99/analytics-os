---
id: analysis.2026-07-usage-alerts-review
type: analysis
title: Review — did usage alerts reduce churn?
owner: bizops
status: reviewed
updated: 2026-07-22
question: Did the April 2026 usage-alert emails reduce logo churn among low-activity customers?
confidence: medium
reviews: decision.2026-04-usage-alerts
depends_on: [metric.logo-churn-rate, source.product-events, entity.customer]
tags: [retention, review]
---

## Question
[[decision.2026-04-usage-alerts]] expected monthly logo churn among low-activity customers to fall from 3.1% to under 2.5% within one quarter.

## Method
Compared the low-activity cohort's [[metric.logo-churn-rate]] for May–July 2026 with Jan–Mar 2026. Activity was first measured with `session_start`, then re-measured with `workflow_run` after we found the issue below.

## Findings
1. Using `session_start`, the at-risk cohort seemed to shrink by 40%. **That was an artifact**: clicking an alert email triggers a login event (see [[source.product-events]]).
2. Using `workflow_run`, the at-risk cohort was essentially unchanged in size.
3. Churn in that cohort did fall, from 3.1% to 2.6%, just short of target.

## Conclusion
The alerts **worked, though not as well as the login data first suggested.** Outcome: `mixed`. Confidence is medium because a concurrent pricing-page change may account for part of the effect.

## What this changes
- Added a known issue to [[source.product-events]]: alert clicks create login events.
- Added a caveat to [[metric.logo-churn-rate]]: leading indicators must use `workflow_run`.
