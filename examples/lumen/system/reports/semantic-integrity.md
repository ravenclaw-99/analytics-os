# Semantic integrity report (deterministic pass)

_Run 2026-11-22 · 1 high · 0 medium · 5 low._

> **Human in the loop.** Nothing here has been changed. For each finding: **accept** the proposed fix, **reject** it (with a reason), or **refine** it (say what to change and the agent re-proposes). To act, run the `review-kb-checks` skill in your LLM tool and give it a finding's code.

### 1. `SEM-182724` [high] Defines 'ARR' outside its canonical artifact `metric.arr`

- **Where:** `execution/tooling/planning-mcp.md`
- **Kind:** `competing_definition`
- **Proposed fix:** Replace the definition with a link to [[metric.arr]]. If the difference is real and intentional, give it a distinct governed name.
- **Recommended action:** **refine** (high confidence)
  - “- The planning model's "ARR" line is defined as contracted MRR × 12, including one-time implementation fees.”

### 2. `SEM-5500e8` [low] Uses 'ARR' but never links its canonical definition

- **Where:** `analytics-reference/data/entities/subscription.md`
- **Kind:** `unlinked_mention`
- **Proposed fix:** Link [[metric.arr]] at the first mention.
- **Recommended action:** **accept** (high confidence)
  - “- Paused subscriptions count as **inactive** for ARR but are not churned until they're cancelled.”

### 3. `SEM-fb5e56` [low] Uses 'ARR' but never links its canonical definition

- **Where:** `analytics-reference/frameworks/growth-accounting.md`
- **Kind:** `unlinked_mention`
- **Proposed fix:** Link [[metric.arr]] at the first mention.
- **Recommended action:** **accept** (high confidence)
  - “A general method for decomposing the change in any stock (customers, ARR, active users) into the flows that caused it:”

### 4. `SEM-8aba47` [low] Uses 'ARR' but never links its canonical definition

- **Where:** `analytics-reference/history/decisions/2026-04-usage-alerts.md`
- **Kind:** `unlinked_mention`
- **Proposed fix:** Link [[metric.arr]] at the first mention.
- **Recommended action:** **accept** (high confidence)
  - “Per [[model.arr-bridge]], halving that gap is worth about $250K of ARR per year.”

### 5. `SEM-605e02` [low] Uses 'ARR' but never links its canonical definition

- **Where:** `analytics-reference/metrics/cohort-retention.md`
- **Kind:** `unlinked_mention`
- **Proposed fix:** Link [[metric.arr]] at the first mention.
- **Recommended action:** **accept** (high confidence)
  - “For customers whose first paid month is M₀, the share still active (ARR > 0) at month M₀+k.”

### 6. `SEM-854cd3` [low] Uses 'ARR' but never links its canonical definition

- **Where:** `execution/tooling/planning-mcp.md`
- **Kind:** `unlinked_mention`
- **Proposed fix:** Link [[metric.arr]] at the first mention.
- **Recommended action:** **accept** (high confidence)
  - “- The planning model's "ARR" line is defined as contracted MRR × 12, including one-time implementation fees.”
