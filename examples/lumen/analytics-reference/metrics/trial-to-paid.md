---
id: metric.trial-to-paid
type: metric
title: Trial-to-Paid Conversion
owner: growth
status: reviewed
updated: 2026-08-05
unit: percent
grain: weekly signup cohort
direction: up_is_good
implementation: analytics.fct_signup_funnel
depends_on: [entity.engagement-event, entity.customer]
tags: [funnel, growth]
---

## Definition
Of the accounts that start a trial in a given week, the share that become a paying [[entity.customer]] within 30 days.

## Formula
`accounts converted to paid within 30 days / trials started in week`

## Caveats
- Cohorts need 30 days to mature. Never report the last four weeks as final.
- Funnel steps (signup → activated → paid) use the definitions in [[entity.engagement-event]].
