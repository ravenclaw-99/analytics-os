# Example: Lumen

**Lumen** is a fictional B2B SaaS company: a workflow tool for operations teams, about $8M ARR, 70 employees, monthly and annual plans. All numbers and vendors are made up.

```
lumen/
  AGENTS.md                      Read first: ground rules for any AI agent
  analytics-reference/           The content house
    metrics/                     ARR, NRR, logo churn, cohort retention, trial-to-paid, …
    data/sources/                Stripe, product events, and their known issues
    data/entities/               Customer, subscription: grain and joins
    data/certified-queries/      SQL certified as a source of truth
    models/                      ARR bridge, operating-model build notes
    frameworks/                  Horizontal methods: growth accounting, mix shift, LMDI, cohort methods
    finance/                     Vendor register, AP/AR conventions, expense tracking
    product/                     Engagement event → product concept mapping
    history/                     Analyses and decisions, with review dates
  execution/
    skills/                      Eight playbooks: forecast comparison, metric questions, month-end flux,
                                 board prep, finding prior analyses, dashboards, Airflow DAGs,
                                 reviewing check findings
    tooling/                     Warehouse, planning tool, Sheets, HTML dashboards, workspace search, Airflow
  system/                        Scheduled jobs + prompts (stub)
```

Worth looking at:
- `metric.arr` → `query.fct-arr-daily`: a definition tied to a certified query.
- `history/`: `decision.2026-04-usage-alerts` has been reviewed, and its review analysis pushed a known issue back into `source.product-events`.
- `framework.lmdi`: a worked LMDI decomposition of a year's ARR change into customers, mix, seats, and price, adding up exactly, plus a hosting-cost example.
- `model.operating-model`: how the operating model is built (revenue build → headcount → opex → cash), which the `month-end-flux` and `board-prep-pivot` skills rely on.
- `execution/skills/`: each skill links to definitions and tooling instead of restating them. `month-end-flux` pulls its categories and thresholds from `register.expense-tracking`, for example.
- `metric.cac-payback`: deliberately unowned, so you can see what the checker warns about.

```bash
python3 ../../tools/kb.py check .
python3 ../../tools/kb.py index .
```
