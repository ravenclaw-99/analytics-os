---
name: month-end-flux
description: Explain month-over-month changes in the P&L by expense category and vendor after the books close, separating timing effects from real changes, and produce the standard flux sheet with commentary. Use at month-end close, or when someone asks why an expense line moved.
---

# Month-end P&L flux

## Inputs
- **Month**: default is the most recently closed month.
- **Comparison**: default is the prior month. Also accepted: the same month last year, or the forecast for that month (a version id from the planning tool).
- **Scope**: default is every expense category in the P&L, plus total revenue as a reference line.

## Steps

1. **Confirm the month is closed.** Use the close timing in [[register.ap-ar]]. If you're running before then, stop and say the numbers aren't final.
2. **Pull actuals** for both months from the GL export named in [[register.expense-tracking]]: one row per GL line, with account, vendor, department, amount, and memo.
3. **Map every line** to its category using the GL ranges in [[register.expense-tracking]], and to its vendor in [[register.vendors]]. List any line that maps to no category or no vendor in an `unmapped` tab. Don't guess.
4. **Compute flux** per category: absolute and percent change. Then do the same per vendor within each category.
5. **Strip out timing effects before explaining anything.** For every category over the threshold in [[register.expense-tracking]], check in this order:
   - accrual true-ups (accrued last month, actual invoice this month), per [[register.ap-ar]]
   - prepaids starting or ending amortization, per [[register.vendors]]
   - reclasses (memo starts with `RECLASS:`) and one-time items (memo tag `one-time`)

   What's left is the **underlying change**.
6. **Explain the underlying change by driver:**
   - **Usage-billed vendors** (for example hosting): split into volume × unit cost with [[framework.lmdi]]. Volume comes from `workflow_run` counts in [[entity.engagement-event]].
   - **People lines**: split into headcount changes (hires, departures, by department) and cost per head (raises, bonus timing, payroll tax resets in January).
   - **Contracted vendors**: compare with the expected amount in [[register.vendors]]. A difference is a price change, a seat change, or a missing renewal.
7. **Compare with the forecast** if one was given: actual vs. the forecast line in [[model.operating-model]]. Flag lines where the forecast driver looks wrong, not just the variance.
8. **Write the output** to a new Google Sheet using [[tooling.google-sheets]], with tabs:
   - `summary`: total opex change, the top 5 underlying drivers, and timing effects as one line
   - `by-category`: category × (prior, current, Δ, Δ%, timing, underlying, explanation)
   - `by-vendor`: vendor × (prior, current, Δ, explanation)
   - `timing`: every accrual, prepaid, and reclass adjustment, with its memo
   - `unmapped`: anything from step 3
   - `sources`: artifact ids and the GL export date
9. **Draft commentary**: 5 bullets at most, one per driver, each with its dollar impact.

## Rules
- Category names and thresholds come from [[register.expense-tracking]]. Don't invent categories, and don't apply your own materiality threshold.
- Never net a timing effect against a real change in the commentary. Report them separately.
- If a vendor is in the GL but not in [[register.vendors]], flag it. The register's rules say it should have a row before the first payment.

## Output contract
A Sheet link plus the commentary bullets. If the same timing pattern explains a big move two months running, propose a draft edit to [[register.expense-tracking]] or [[register.vendors]] so next month's run expects it.
