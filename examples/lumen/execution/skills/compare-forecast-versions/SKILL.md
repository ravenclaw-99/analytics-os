---
name: compare-forecast-versions
description: Compare the latest forecast with an earlier version (e.g. from three weeks ago), attribute the deltas to drivers, and produce the standard forecast-variance output. Use when someone asks what changed in the forecast, or before the weekly forecast review.
---

# Compare forecast versions

## Inputs
- **Current version**: default is the latest published version in the planning tool.
- **Comparison version**: default is the version published closest to 21 days ago.
- **Scope**: default is company-level ARR, revenue, opex, and ending cash for the next four quarters.

## Steps

1. **Pull both versions** through the planning-tool connection described in [[tooling.planning-mcp]]. Export the same scenario, the same time range, and the same dimension cut for both. Confirm both exports have identical row keys before going further. If they don't, stop and report the mismatch.
2. **Compute deltas** per line × period: absolute and percent.
3. **Attribute ARR deltas** using the bridge in [[model.arr-bridge]]: new, expansion, contraction, churn. Attribute any blended-rate change (ARPA, churn rate) with [[framework.mix-shift]].
4. **Check actuals.** If a delta in a closed period exists, it's an actuals restatement. Reconcile to [[query.fct-arr-daily]] and flag it separately.
5. **Rank** the top 5 drivers by absolute impact on ending ARR and ending cash.
6. **Write the output** to a new Google Sheet using [[tooling.google-sheets]], with tabs:
   - `summary`: headline deltas and the top 5 drivers in plain language
   - `detail`: line × period, v_old, v_new, Δ, Δ%
   - `arr-bridge`: old vs. new bridge side by side
7. **Draft commentary**: 5 bullets maximum. Each bullet names a driver, gives its impact, and cites a source (version id, metric id).

## Rules
- Use metric definitions from [[metric.arr]] and [[metric.net-revenue-retention]], never the planning tool's labels alone.
- Don't round until the summary tab.
- If an assumption change can't be explained from the planning tool's change log, say so. Don't guess.

## Output contract
A Sheet link plus the commentary bullets. Save a draft analysis to `analytics-reference/history/analyses/` only if the user asks to keep it.
