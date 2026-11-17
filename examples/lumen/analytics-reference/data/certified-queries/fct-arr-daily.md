---
id: query.fct-arr-daily
type: query
title: Certified — daily ARR by customer
owner: finance
status: reviewed
updated: 2026-06-10
certified_by: finance
certified_on: 2026-06-10
warehouse_object: analytics.fct_arr_daily
depends_on: [entity.subscription, entity.customer, source.stripe]
tags: [certified, revenue]
---

## What it returns
One row per [[entity.customer]] per day, with ARR (net of discounts). This is the **only** query that may be used to report [[metric.arr]] and the metrics derived from it.

## SQL
```sql
-- Certified 2026-06-10 (finance). Changes require re-certification.
select
  s.snapshot_date,
  s.stripe_customer_id,
  sum(
    s.unit_amount_net / 100.0
    * s.quantity
    * case s.billing_interval when 'year' then 1.0 / 12 else 1 end
  ) * 12 as arr_usd
from analytics.stg_stripe__subscriptions_daily s
where s.status = 'active'
  and s.is_paid_plan
  and s.stripe_customer_id not like 'cus_TEST%'
group by 1, 2
```

## Validation
- Reconciles to the Stripe MRR report within ±0.5% each month-end (see [[source.stripe]] known issues for the refund lag).
- Row count per day equals active paying customers in [[entity.customer]].
