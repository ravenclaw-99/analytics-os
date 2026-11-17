---
id: source.stripe
type: source
title: Stripe (billing)
owner: finance
status: reviewed
updated: 2026-10-02
system: Stripe
sync: Fivetran, every 6 hours, into raw_stripe.*
tags: [billing, revenue]
---

## Authoritative for
- Subscriptions, plan, price, and billing interval
- Invoices, payments, refunds
- The billing account (`stripe_customer_id`): the canonical grain of [[entity.customer]]

## Not authoritative for
- Product usage or seats in use (see [[source.product-events]])
- Sales-assisted contract terms before they're entered in Stripe

## Tables
- `raw_stripe.subscriptions`, `raw_stripe.subscription_items`, `raw_stripe.invoices`, `raw_stripe.refunds`

## Known issues
- **Refunds post on a ~2-day lag.** Month-end revenue figures move by up to 0.4% in the first week of the following month. Close the books on business day 3, not day 1.
- **Annual plans are billed upfront.** Never derive ARR from invoice amounts. Use subscription price × interval normalization (see [[metric.arr]]).
- **Two test-mode customers leaked into production in March 2025** (`cus_TEST*`). They're excluded in `stg_stripe__customers`.
