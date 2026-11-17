---
id: register.ap-ar
type: register
title: Accounts payable & receivable conventions
owner: finance
status: reviewed
updated: 2026-09-01
system: NetSuite
depends_on: [register.vendors, source.stripe]
tags: [finance, ap, ar, cash]
---

## Accounts receivable
- Self-serve customers pay by card through [[source.stripe]]. AR is effectively zero.
- Invoiced (sales-assisted) customers are on net 30. DSO target is < 40 days.
- Aging buckets: current, 1–30, 31–60, 61–90, 90+. Anything at 90+ goes to the CFO weekly.

## Accounts payable
- Payment runs every other Thursday. Vendor terms come from [[register.vendors]].
- Accruals: any invoice not received by business day 3 is accrued from the register's expected amount.
