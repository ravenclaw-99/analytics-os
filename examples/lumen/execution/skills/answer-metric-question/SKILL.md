---
name: answer-metric-question
description: Answer a question about a business metric ("what's our NRR?", "how many active customers?") using only the governed definitions and certified queries in analytics-reference. Use for any quantitative question about Lumen's metrics.
---

# Answer a metric question

1. **Resolve the metric.** Find it in `analytics-reference/metrics/`. If it isn't there, say it isn't governed, offer the closest governed metric, and propose a draft definition. **Never invent a definition.**
2. **Read the whole artifact**, especially **Caveats** and **History**. Then read the caveats on everything in its `depends_on`, including the known issues of its sources (for example [[source.stripe]]).
3. **Use the certified query** named in `implementation` (for example [[query.fct-arr-daily]]). Run it through [[tooling.warehouse-mcp]]. Don't write fresh SQL for a governed metric.
4. **Check for prior work** in `analytics-reference/history/` on the same question.
5. **Answer** in this format:
   - **Number**, with as-of date and grain
   - **Definition used** (artifact id)
   - **Caveats that apply** to this specific answer
   - **Confidence**: low / medium / high, with a reason
