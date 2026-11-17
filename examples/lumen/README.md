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
    models/                      ARR bridge
    frameworks/                  Horizontal methods: growth accounting, mix shift
    finance/                     Vendor register, AP/AR conventions
    product/                     Engagement event → product concept mapping
    history/                     Analyses and decisions, with review dates
  execution/
    skills/                      compare-forecast-versions, answer-metric-question
    tooling/                     Warehouse, planning tool, Google Sheets
  system/                        Scheduled jobs + prompts (stub)
```

Worth looking at:
- `metric.arr` → `query.fct-arr-daily`: a definition tied to a certified query.
- `history/`: `decision.2026-04-usage-alerts` has been reviewed, and its review analysis pushed a known issue back into `source.product-events`.
- `metric.cac-payback`: deliberately unowned, so you can see what the checker warns about.

```bash
python3 ../../tools/kb.py check .
python3 ../../tools/kb.py index .
```
