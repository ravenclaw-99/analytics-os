---
id: register.vendors
type: register
title: Vendor register
owner: finance
status: reviewed
updated: 2026-11-01
system: NetSuite (AP) + this register
tags: [finance, expenses, ap]
---

## What this is
Every vendor Lumen pays, with billing cycle and expense category. Used for expense tracking, AP forecasting, and the opex lines in [[model.arr-bridge]]'s companion operating model. (All entries are fictional.)

| Vendor | Category | Cycle | Terms | Owner | Renewal |
|---|---|---|---|---|---|
| AWS | COGS: hosting | monthly, usage | card | eng | n/a |
| Snowflake | COGS: data platform | annual prepaid credits | net 30 | data | 2027-03-01 |
| Fivetran | G&A: data tooling | monthly | card | data | n/a |
| Salesforce | S&M: CRM | annual | net 30 | revops | 2027-02-15 |
| Gusto | G&A: payroll | monthly | auto-debit | finance | n/a |
| WeWork | G&A: facilities | monthly | net 15 | ops | 2026-12-31 |

## Rules
- Annual prepaids are amortized monthly in the P&L. AP forecasting uses the cash date.
- New vendors over $10K/yr need a row here before the first payment.
- Payment terms and accrual rules: [[register.ap-ar]].
