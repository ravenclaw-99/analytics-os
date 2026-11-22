---
id: model.operating-model
type: model
title: Operating model build notes
owner: finance
status: reviewed
updated: 2026-11-22
kind: operating_model
depends_on: [model.arr-bridge, metric.arr, metric.logo-churn-rate, register.expense-tracking, register.vendors, register.ap-ar]
tags: [finance, forecast, fp&a, board]
---

## Relationships
How Lumen's monthly operating model is built in the planning tool (see [[tooling.planning-mcp]] for the connection). It has four blocks. Each one feeds the next:

```
1. Revenue build   →  2. Headcount  →  3. Non-headcount opex  →  4. Cash
   (ARR drivers)       (hires × cost)    (vendors × category)     (timing)
```

**1. Revenue build.** Starts from the [[model.arr-bridge]] flows, forecast by segment (monthly vs. annual):
- **New:** new customers × starting ARR per customer. New-customer volume comes from the growth plan (trials × [[metric.trial-to-paid]]).
- **Churn:** customers at start × churn rate, using [[metric.logo-churn-rate]] by segment. Rates come from cohort curves built per [[framework.cohort-methods]], not from a single blended rate.
- **Expansion and contraction:** a percentage of starting ARR by segment, calibrated on the trailing 12 months.
- **Ending ARR** reconciles to [[metric.arr]] for every closed month. Recognized revenue is ARR ÷ 12 per month, with annual prepaids recognized ratably. Revenue is never taken from invoices.

**2. Headcount.** One row per role (current employees and planned hires), with department, start date, and fully loaded annual cost (salary × 1.22 for taxes and benefits). The department mapping matches the "people" categories in [[register.expense-tracking]].

**3. Non-headcount opex.** One line per expense category in [[register.expense-tracking]]. Contracted vendors are forecast from [[register.vendors]] (amount, cycle, renewal date). Usage-billed vendors use a driver: hosting = forecast workflow runs × cost per run.

**4. Cash.** P&L lines are converted to cash with the payment terms and AP/AR conventions in [[register.ap-ar]]. Annual vendor prepaids hit cash on the payment date but the P&L monthly. Annual customer plans do the reverse: cash upfront, revenue spread over the year.

## Assumptions
- **Versions and scenarios.** Each published forecast is a new **version**, identified by version id. Each version has three **scenarios**: `base`, `upside`, `downside`. Scenarios differ only in the revenue drivers (new volume, churn, expansion) and the hiring plan. Vendor costs stay the same across scenarios unless a vendor is usage-billed.
- **Actuals.** Closed months are loaded from the GL after the books close (timing in [[register.ap-ar]]). After that load, a closed month's numbers should only change through a restatement, which gets flagged as one.
- **Definitions.** Revenue drivers use the governed definitions in `analytics-reference/metrics/`. Where the planning tool has its own line with a similar name, the governed metric wins. Check the gotchas in [[tooling.planning-mcp]].
- **Driver changes** are recorded in the planning tool's change log with a one-line reason. That log is what makes forecast-versus-forecast comparisons explainable.

## Sensitivities
- One point of monthly logo churn is the largest single revenue lever. Its ARR impact is in [[model.arr-bridge]].
- Headcount is about 70% of total opex, so the hiring-plan start dates move ending cash more than any vendor line.
- The annual-plan mix moves cash far more than revenue (upfront billing). See [[decision.2026-10-annual-plan-discount]] for the current bet on that mix.
- To split a change in any block into its drivers (volume, mix, rate), use [[framework.lmdi]].
