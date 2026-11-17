---
id: analysis.2026-09-churn-by-cohort
type: analysis
title: Churn by billing interval and cohort
owner: finance
status: reviewed
updated: 2026-09-18
question: Do annual-plan customers retain better than monthly, controlling for size and cohort?
confidence: high
depends_on: [metric.logo-churn-rate, metric.net-revenue-retention, entity.subscription]
tags: [retention, pricing]
---

## Question
Is the retention gap between annual and monthly plans real, or just a selection effect?

## Method
Cohorted customers by start quarter (2024 Q1 – 2026 Q1) and seat band, then compared 12-month [[metric.logo-churn-rate]] and [[metric.net-revenue-retention]] between annual and monthly within each cell. Excluded the 2025 Q2 enterprise migration cohort as an outlier.

## Findings
- Within the same size band, annual customers churn **58% less** over 12 months than monthly ones.
- About 40% of the raw gap is selection (larger customers choose annual). The rest holds up after controlling for size.
- NRR is 8 points higher for annual customers, mostly from lower contraction.

Cohort curves use [[metric.cohort-retention]].

## Conclusion
Moving more customers to annual plans is a real retention lever, not just an accounting effect.

## What this changes
- Feeds [[decision.2026-10-annual-plan-discount]].
