---
id: framework.growth-accounting
type: framework
title: Growth accounting
owner: bizops
status: reviewed
updated: 2026-06-10
tags: [framework, horizontal]
---

## What it is
A general method for decomposing the change in any stock (customers, ARR, active users) into the flows that caused it:

```
end = start + new + resurrected + expansion − contraction − churned
```

## When to use it
Any time someone asks "why did X go up/down?" about a stock metric. Answer with the decomposition first and the narrative second.

## How Lumen applies it
- ARR: see [[model.arr-bridge]]
- Active users: new / retained / resurrected / churned, using `workflow_run` from [[entity.engagement-event]]

## Pitfalls
- Classify movements at the right grain ([[entity.customer]], not subscription). Otherwise plan swaps look like churn plus new.
