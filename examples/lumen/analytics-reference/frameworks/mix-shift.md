---
id: framework.mix-shift
type: framework
title: Mix-shift analysis
owner: finance
status: reviewed
updated: 2026-09-18
tags: [framework, horizontal]
---

## What it is
Separates a change in a blended rate (average price, margin, churn) into:
- **Rate effect:** the segments themselves changed
- **Mix effect:** the weight of each segment changed

```
Δ blended = Σ (Δ rate_i × weight_i,old)  +  Σ (Δ weight_i × rate_i,new)
             └──────── rate effect ───────┘   └─────── mix effect ───────┘
```

## When to use it
Whenever a blended metric moves and the segments have very different levels: annual vs. monthly churn, plan-tier ARPA, regional margin.

## How Lumen applies it
- [[decision.2026-10-annual-plan-discount]] is a deliberate mix shift: overall churn should fall because the *weight* of annual plans rises, even if neither segment's churn rate changes.
