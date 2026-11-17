---
id: entity.engagement-event
type: entity
title: Engagement events → product concepts
owner: data
status: reviewed
updated: 2026-07-22
grain: One row per tracked event.
primary_key: event_id
depends_on: [source.product-events, entity.customer]
tags: [product, engagement]
---

## Definition
Maps raw tracked events to the product concepts analysts actually use.

| Concept | Event(s) | Notes |
|---|---|---|
| **Active user** | `workflow_run` | **Not** `session_start`; see the known issues in [[source.product-events]] |
| **Activated account** | ≥ 3 `workflow_run` by ≥ 2 users within 14 days of signup | Used in the activation funnel |
| **Power user** | ≥ 20 `workflow_run` in a trailing 7 days | |
| **Seat utilization** | distinct active users / paid seats | Joins to [[entity.subscription]] for seats |

Used by [[metric.trial-to-paid]] (the activation step of the funnel).

## Edge cases
- API-triggered runs count as activity, but they're attributed to the API key's owner.
