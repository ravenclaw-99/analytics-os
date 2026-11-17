---
id: metric.cohort-retention
type: metric
title: Cohort Logo Retention
owner: bizops
status: reviewed
updated: 2026-09-18
unit: percent
grain: monthly cohort × months since start
direction: up_is_good
implementation: analytics.fct_cohort_retention
depends_on: [entity.customer, query.fct-arr-daily]
tags: [retention, cohorts]
---

## Definition
For customers whose first paid month is M₀, the share still active (ARR > 0) at month M₀+k.

## Formula
`active customers of cohort at month k / customers in cohort at month 0`

## Caveats
- The 2025-Q2 cohort includes a one-off enterprise migration. Exclude it in trend analyses, as [[analysis.2026-09-churn-by-cohort]] does.
- For revenue-weighted retention, use [[metric.net-revenue-retention]].
