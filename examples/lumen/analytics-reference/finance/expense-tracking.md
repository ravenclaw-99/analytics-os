---
id: register.expense-tracking
type: register
title: Expense tracking conventions
owner: finance
status: reviewed
updated: 2026-11-22
system: NetSuite (GL) + payroll (Gusto)
depends_on: [register.vendors, register.ap-ar]
tags: [finance, expenses, opex, close]
---

## What this is
How every dollar Lumen spends gets coded, so the P&L can be cut by **category**, **department**, and **vendor**, and month-over-month flux can be explained line by line. Vendor-level facts (cycle, terms, renewal) live in [[register.vendors]]. Payment timing and accrual rules live in [[register.ap-ar]]. This register covers coding and reporting only. (All values are fictional.)

**Where actuals come from:** the NetSuite saved search `Monthly P&L detail`, one row per GL line with account, vendor, department, amount, and memo. There's no NetSuite MCP connection yet, so export it as CSV after close.

## Expense categories

| Category | GL range | P&L section | Typical vendors | Flux owner |
|---|---|---|---|---|
| COGS: hosting | 5100–5199 | Cost of revenue | AWS | eng |
| COGS: data platform | 5200–5299 | Cost of revenue | Snowflake | data |
| COGS: support | 5300–5399 | Cost of revenue | support headcount | cx |
| S&M: people | 6100–6199 | Sales & marketing | payroll | revops |
| S&M: CRM | 6200–6299 | Sales & marketing | Salesforce | revops |
| S&M: paid acquisition | 6300–6399 | Sales & marketing | ad platforms | growth |
| R&D: people | 7100–7199 | Research & development | payroll | eng |
| G&A: people | 8100–8199 | General & administrative | payroll | finance |
| G&A: data tooling | 8200–8299 | General & administrative | Fivetran | data |
| G&A: facilities | 8300–8399 | General & administrative | WeWork | ops |
| G&A: payroll | 8400–8499 | General & administrative | Gusto (service fees only; wages go to "people" lines) | finance |

## Rules
- **The category follows the vendor.** A vendor's default category is the one in [[register.vendors]]. Code a bill to a different category only with a memo explaining why, such as a one-off project.
- **Department follows the person or team that owns the spend**, not the person who paid. Shared tools are split by seat count once a quarter.
- **People costs** (salary, payroll tax, benefits) come from the payroll journal, by the employee's department. Contractors are coded to the department they work for, never to G&A by default.
- **Reclasses** get a journal entry with a memo that starts `RECLASS:` and names the original month. The flux skill reads these memos to separate real changes from coding fixes.
- **One-time costs** over $25K (legal settlements, a data migration) get the tag `one-time` in the memo, so they can be excluded from run-rate views.
- **Flux threshold:** explain any category that moves more than **$10K and more than 10%** month over month. Smaller moves are listed but not explained.
- **Timing effects come first.** Before calling a change real, check whether it's an accrual true-up, a prepaid starting or ending amortization, or a bill coded to the wrong month. The conventions for each are in [[register.ap-ar]] and [[register.vendors]].
- **New category?** Add a row here before the first bill is coded to it, and update [[model.operating-model]] so the forecast has a matching line.
