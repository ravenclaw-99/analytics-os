---
id: framework.lmdi
type: framework
title: LMDI (Logarithmic Mean Divisia Index) decomposition
owner: finance
status: reviewed
updated: 2026-11-22
depends_on: [framework.mix-shift]
tags: [framework, horizontal, decomposition]
---

## What it is
An index decomposition method. When an aggregate is a product of factors, summed over segments, LMDI splits its change between two periods into one effect per factor. The effects **add up exactly** to the total change: no residual and no "interaction" bucket. The result doesn't depend on the order you take the factors in.

For an aggregate `V = Σ_s x1_s × x2_s × … × xn_s` (sum over segments s), the additive form gives the effect of factor k as:

```
ΔV_k = Σ_s  L(V_s,T , V_s,0) × ln( xk_s,T / xk_s,0 )

L(a, b) = (a − b) / (ln a − ln b)      logarithmic mean;  L(a, a) = a
```

The multiplicative form (`V_T / V_0 = Π_k D_k`) uses the same weights, divided by `L(V_T, V_0)`. Use it when you want "how many points of the growth rate came from each factor".

## When to use it
- A blended number moves and **more than two factors** are in play (volume, mix, intensity, price). [[framework.mix-shift]] handles rate vs. mix. LMDI generalizes it to any number of factors, without the leftover cross term.
- Someone needs the pieces to **sum exactly** to the change: board bridges, forecast variance, month-end flux.
- The same breakdown has to work for every period pair, so the effects stay comparable over time.

## How Lumen applies it

### Revenue: what drove the change in ARR
ARR here is [[metric.arr]] from [[query.fct-arr-daily]], split by billing interval. Four factors per segment s:

```
V = Σ_s  C × S_s × K_s × P_s        (V is ARR per [[metric.arr]])
C   = total customers ([[entity.customer]] grain)
S_s = share of customers in segment s (monthly, annual)
K_s = seats per customer in s (quantity on [[entity.subscription]])
P_s = ARR per seat in s (net of discounts)
```

Worked example (fictional), 2025-09-30 → 2026-09-30:

| Segment | Customers | Seats / customer | ARR / seat | ARR |
|---|---|---|---|---|
| Monthly, start | 1,000 | 9.0 | $480 | $4.32M |
| Annual, start | 380 | 15.0 | $400 | $2.28M |
| Monthly, end | 980 | 9.6 | $495 | $4.66M |
| Annual, end | 520 | 16.0 | $400 | $3.33M |

The total change, from $6.60M to $7.98M, is **+$1,384,960**:

| Effect | Amount | Reading |
|---|---|---|
| Customers (C) | +$605K | More customers overall |
| Mix (S) | +$173K | Annual share rose from 28% to 35%, and annual customers buy more seats |
| Seats (K) | +$468K | Seat expansion in both segments |
| Price (P) | +$138K | The monthly list-price change. Annual ARR per seat was flat |
| **Total** | **+$1,385K** | Exact, with no residual |

Blended ARR per seat actually *fell* (from $449 to $442) while every segment's price held or rose. That's the mix effect at work. Reporting the blended number alone would have suggested a price problem that doesn't exist. The flows view of the same change (new, expansion, contraction, churn) is [[model.arr-bridge]]. Use the bridge to say *who* moved, and LMDI to say *which driver* moved.

### Cost: why hosting spend moved
Hosting cost (AWS, see [[register.vendors]]) = workflow runs × cost per run. Runs are `workflow_run` events from [[entity.engagement-event]]. September → October 2026: runs went from 4.1M to 4.6M, and cost per 1,000 runs went from $11.20 to $10.90. Spend rose from $45,920 to $50,140 (**+$4,220**): **+$5,523 volume** and **−$1,303 unit cost**. That's the split the `month-end-flux` skill uses for usage-billed vendors.

## Pitfalls
- **Every value must be positive.** LMDI takes logs, so it can't handle a factor that's zero or changes sign (for example net income, or a segment that didn't exist in one period). Treat new and exited segments as their own flows, as in [[framework.growth-accounting]], and decompose only the segments present in both periods. Don't paper over zeros with tiny placeholder values without saying so.
- **The factors must multiply back to the aggregate exactly.** Check that `Π factors` reproduces each segment's value before decomposing. If it doesn't, the effects are meaningless.
- **Segment choice changes the mix effect.** Decomposing by billing interval and by plan tier gives different mix effects. State the segmentation, and keep it fixed across the periods you compare.
- **Use the same definition at both ends.** If a definition was restated between the two dates (see the History section of [[metric.arr]]), restate the earlier period first.
