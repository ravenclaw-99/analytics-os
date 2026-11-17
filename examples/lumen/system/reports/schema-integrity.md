# Schema integrity report

_Run 2026-11-16 · 2 high · 2 medium · 0 low._

> **Human in the loop.** Nothing here has been changed. For each finding: **accept** the proposed fix, **reject** it (with a reason), or **refine** it (say what to change and the agent re-proposes).

### 1. [high] Documented column `analytics.fct_signup_funnel.trial_started_at` no longer exists

- **Where:** `analytics.fct_signup_funnel.trial_started_at`
- **Kind:** `missing_column`
- **Proposed fix:** Looks renamed to `trial_start_ts`; update the register and any queries.
- **Recommended action:** **accept** (medium confidence)
  - documented in `analytics-reference/data/key-tables.md`

### 2. [high] `analytics.fct_nrr_monthly` is referenced in the knowledge base but no longer exists in the warehouse

- **Where:** `analytics.fct_nrr_monthly`
- **Kind:** `missing_table`
- **Proposed fix:** It looks like it was renamed to `analytics.fct_nrr_monthly_v2`. Update the references and re-validate.
- **Recommended action:** **accept** (medium confidence)
  - referenced at `analytics-reference/metrics/net-revenue-retention.md:11`

### 3. [medium] Key table column `analytics.fct_arr_daily.plan_tier` exists in the warehouse but isn't documented anywhere

- **Where:** `analytics.fct_arr_daily.plan_tier`
- **Kind:** `undocumented_column`
- **Proposed fix:** Add a row for `plan_tier` under `### analytics.fct_arr_daily` in `analytics-reference/data/key-tables.md`, with a description.
- **Recommended action:** **refine** (high confidence)

### 4. [medium] Key table column `analytics.fct_signup_funnel.trial_start_ts` exists in the warehouse but isn't documented anywhere

- **Where:** `analytics.fct_signup_funnel.trial_start_ts`
- **Kind:** `undocumented_column`
- **Proposed fix:** Add a row for `trial_start_ts` under `### analytics.fct_signup_funnel` in `analytics-reference/data/key-tables.md`, with a description.
- **Recommended action:** **refine** (high confidence)
