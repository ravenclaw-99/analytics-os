---
id: entity.customer
type: entity
title: Customer
owner: finance
status: reviewed
updated: 2026-06-10
grain: One row per paying billing account (Stripe customer) with at least one active paid subscription.
primary_key: stripe_customer_id
depends_on: [source.stripe, source.product-events]
tags: [core]
---

## Definition
A **customer** is a billing account, not a user and not a workspace. This is the grain for all revenue and retention metrics.

## Identifiers across sources
| Source | Key | Join |
|---|---|---|
| [[source.stripe]] | `stripe_customer_id` | native |
| [[source.product-events]] | `workspace_id` | via `dim_workspace_customer` (one-to-many) |

## Edge cases
- **Free-tier accounts are not customers.** They're tracked as `account` only.
- **Mergers of two customer accounts** keep the older `stripe_customer_id`. The newer one is marked churned with reason `merged`, which is excluded from [[metric.logo-churn-rate]].
