---
id: register.key-tables
type: register
title: Key tables and their columns
owner: data
status: reviewed
updated: 2026-10-01
system: Snowflake
depends_on: [source.stripe, source.product-events]
tags: [data, schema]
---

## What this is
The tables that matter most for analysis. **Every column in these tables must be documented here.** The daily schema-integrity check enforces this against the live warehouse.

### analytics.fct_arr_daily
Built by [[query.fct-arr-daily]]. One row per customer per day.

| Column | Description |
|---|---|
| `snapshot_date` | Day of the snapshot (UTC) |
| `stripe_customer_id` | Billing account; see [[entity.customer]] |
| `arr_usd` | ARR in USD, net of discounts; see [[metric.arr]] |

### analytics.fct_signup_funnel
One row per trial account. Used by [[metric.trial-to-paid]].

| Column | Description |
|---|---|
| `account_id` | Trial account |
| `trial_started_at` | Trial start timestamp (UTC) |
| `activated_at` | First time activation criteria were met; see [[entity.engagement-event]] |
| `converted_at` | First paid invoice; null if not converted |

### analytics.dim_workspace_customer
Maps product workspaces to billing accounts (one-to-many).

| Column | Description |
|---|---|
| `workspace_id` | Product workspace |
| `stripe_customer_id` | Billing account |
