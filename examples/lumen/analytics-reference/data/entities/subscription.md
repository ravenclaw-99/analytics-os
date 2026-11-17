---
id: entity.subscription
type: entity
title: Subscription
owner: finance
status: reviewed
updated: 2026-06-10
grain: One row per Stripe subscription per day (daily snapshot).
primary_key: subscription_id, snapshot_date
depends_on: [source.stripe, entity.customer]
tags: [core, revenue]
---

## Definition
A recurring paid agreement for one plan. A [[entity.customer]] may have several at once (e.g. a base plan plus an add-on).

## Identifiers across sources
- `subscription_id` from [[source.stripe]]

## Edge cases
- Paused subscriptions count as **inactive** for ARR but are not churned until they're cancelled.
