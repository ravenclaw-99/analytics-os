---
id: framework.cohort-methods
type: framework
title: Cohort methods
owner: bizops
status: reviewed
updated: 2026-11-22
depends_on: [framework.growth-accounting]
tags: [framework, horizontal, cohorts, retention]
---

## What it is
Group customers (or trials, or users) by **when they started** and follow each group over **time since start**, not calendar time. This separates "are newer customers behaving differently?" from "did something happen this month?". A single company-wide rate mixes the two up.

## When to use it
- Retention, expansion, or conversion questions where the customer base keeps growing. Fast growth adds young customers, and young customers churn at different rates, so blended rates move even when no cohort changed.
- Checking whether a launch, pricing change, or decision affected **new** customers only, or everyone.
- Building forecast assumptions: retention curves by cohort age feed the churn and expansion drivers in [[model.operating-model]].

## How Lumen applies it

### Choose the cohort and the clock
| Question | Cohort by | Clock starts | Measure |
|---|---|---|---|
| Logo retention | First paid month | Month 0 = first paid month | [[metric.cohort-retention]] |
| Revenue retention | First paid month | Month 0 ARR | Cohort ARR ÷ month-0 ARR, using [[metric.arr]] |
| Trial conversion | Trial-start week | Trial start | [[metric.trial-to-paid]] |
| Product engagement | First `workflow_run` week | First run | Weekly active share, per [[entity.engagement-event]] |

The cohort unit is the [[entity.customer]] (billing account) for anything about revenue or retention. Workspaces and users are not customers.

### Read it as a triangle
Lay cohorts out as rows and months-since-start as columns. Then read it three ways:
1. **Down a column** (same age, different cohorts): are newer cohorts better or worse at month 6?
2. **Along a row** (one cohort over time): the shape of the curve. Where does it flatten?
3. **Along a diagonal** (same calendar month): a calendar shock hits every cohort in the same month, such as a pricing change or an outage.

### Standard cuts
- **Billing interval** (monthly vs. annual) and **seat band**. [[analysis.2026-09-churn-by-cohort]] shows why both matter: interval alone overstates the annual effect, because larger customers choose annual.
- **Acquisition channel** (self-serve vs. sales-assisted) when looking at conversion or payback.

### Revenue vs. logo curves
Logo retention can only fall. Revenue retention can rise above 100% through expansion. Show both, because a cohort can lose logos and still grow revenue. The flows behind a revenue curve are the same ones as in [[framework.growth-accounting]].

## Pitfalls
- **Immature cohorts.** The most recent cohorts haven't had time to show month-k behavior. Cut each curve where the data ends instead of plotting zeros, and never average across cohorts of different ages without weighting. Funnel cohorts have their own maturity rule in [[metric.trial-to-paid]].
- **Outlier cohorts.** Check each metric's caveats for known exclusions before trending (for example the caveats on [[metric.cohort-retention]]). Say which cohorts you excluded and why.
- **Survivorship.** "Customers who reached month 24 expand a lot" describes survivors, not the average customer. Always state the denominator.
- **Blended averages of rates.** To combine cohorts, weight by cohort size (logos) or month-0 ARR (revenue). Never take a simple average of cohort percentages.
- **Calendar vs. cohort time.** Don't mix the two in one chart. If the question is about a calendar event, look at the diagonal and say so.
