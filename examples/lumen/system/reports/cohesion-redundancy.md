# Organizational cohesion & redundancy report (deterministic pass)

_Run 2026-11-22 · 0 high · 1 medium · 0 low._

> **Human in the loop.** Nothing here has been changed. For each finding: **accept** the proposed fix, **reject** it (with a reason), or **refine** it (say what to change and the agent re-proposes). To act, run the `review-kb-checks` skill in your LLM tool and give it a finding's code.

### 1. `COH-d3d570` [medium] Near-duplicate passages (57% overlap)

- **Where:** `analytics-reference/data/sources/stripe.md ↔ analytics-reference/finance/ap-ar.md`
- **Kind:** `near_duplicate`
- **Proposed fix:** Keep the text in `source.stripe` (more fundamental) and replace it in `register.ap-ar` with a link: [[source.stripe]].
- **Recommended action:** **refine** (medium confidence; calibrated: humans chose refine on 10 of the last 14 near_duplicate findings)
  - `analytics-reference/data/sources/stripe.md`: “- **Refunds post on a ~2-day lag.** Month-end revenue figures move by up to 0.4% in the first week of the following month. Close the books on business day 3, not day 1.”
  - `analytics-reference/finance/ap-ar.md`: “- Refunds post on a ~2-day lag, so month-end revenue figures can move by up to 0.4% in the first week of the following month. Close the books on business day 3.”
