---
name: board-prep-pivot
description: Build the standard quarterly board tables (ARR bridge, retention, cohort curves, P&L and cash vs. plan) from certified sources, reconciled to the last board deck. Use when preparing a board deck or investor update, or when someone asks for "the board numbers" for a quarter.
---

# Board-prep pivot

## Inputs
- **Quarter**: default is the most recently closed quarter.
- **Plan**: default is the board-approved scenario of the forecast version presented at the start of the year (a version id from the planning tool).
- **Prior deck**: the Sheet behind the previous board deck, for reconciliation.

## Steps

1. **Confirm the quarter is closed**: all three months closed per [[register.ap-ar]].
2. **Pull the revenue tables** with certified sources only, through [[tooling.warehouse-mcp]]:
   - **ARR**, start and end of quarter, from [[query.fct-arr-daily]] as defined in [[metric.arr]]
   - **ARR bridge** (new, expansion, contraction, churn) per [[model.arr-bridge]], for each month and the quarter
   - **NRR** per [[metric.net-revenue-retention]] and **logo churn** per [[metric.logo-churn-rate]], last 5 quarters
3. **Build the cohort table** with [[framework.cohort-methods]]: quarterly start cohorts × quarters since start, for [[metric.cohort-retention]] (logos) and revenue retention. Apply the exclusions in each metric's caveats, and cut immature cells instead of showing zeros.
4. **Explain the quarter's ARR change by driver** with [[framework.lmdi]] (customers, mix, seats, price). Put it next to the bridge: the bridge says who moved, LMDI says which driver moved.
5. **Pull the P&L and cash vs. plan** from the operating model ([[model.operating-model]]) through [[tooling.planning-mcp]]: actuals for the quarter against the plan scenario, by P&L section. Ending cash and months of runway go last.
6. **Reconcile to the prior deck.** Every number that also appeared last quarter must match it. If one doesn't, it's a restatement: find the cause (each metric's History section lists definition changes) and list it in a `restatements` tab. Never silently show a different number for a past period.
7. **Write the output** to a new Google Sheet using [[tooling.google-sheets]], with tabs:
   - `summary`: the 6 headline numbers (ending ARR, quarterly net new ARR, NRR, logo churn, opex vs. plan, ending cash), each with its prior-quarter value
   - `arr-bridge`, `lmdi`, `retention`, `cohorts`, `pnl-vs-plan`, `cash`
   - `restatements`: past numbers that changed and why
   - `sources`: every artifact id, query, and version id used
8. **Draft talking points**: 5 bullets at most, each a fact with its source.

## Rules
- **Reviewed metrics only.** Any metric with `status: draft` stays out of board material, even if someone asks for it. Say it isn't governed yet and name its owner (or say it has none).
- Use governed metric names in the tables, not the planning tool's line labels.
- Don't round until the `summary` tab. Use the number formats in [[tooling.google-sheets]].

## Output contract
A Sheet link, the talking points, and the list of restatements, if there are any. A human from finance signs off before anything goes into the deck.
