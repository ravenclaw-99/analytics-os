# 01 — Why

## Analytics has a memory problem

Ask three people at a 60-person startup what last quarter's net revenue retention was, and you'll get three numbers. None of them is wrong. One excludes customers acquired mid-quarter. One counts a downgrade-then-upgrade as flat. One comes from a dashboard that was built before the pricing change and never updated.

The trouble isn't the arithmetic. It's that **the knowledge needed to produce the right number isn't written down anywhere that lasts.** It lives in:

- **people**, who leave
- **BI tools**, which store the *how* (the SQL) but not the *why* (the caveats, the history, the edge cases)
- **chat threads and slide decks**, which are written once and never updated

A healthy analytics function survives on tribal knowledge plus a few senior people who remember everything. That works until it doesn't: a key analyst leaves, the company doubles, or an AI agent shows up.

## AI makes this urgent

Large language models are already good at the mechanics of analysis. They write SQL, build models, and summarize findings. What they don't have is **your company's context**:

- that "active customer" excludes the free tier
- that Stripe refunds post two days late, so month-end numbers drift
- that the 2025 cohort is distorted by a one-off enterprise migration
- that the team already tested an annual-plan discount and it cannibalized monthly upgrades

Without that context, an agent produces answers that look confident and are subtly wrong. Subtly wrong is worse than obviously wrong, because people act on it.

The fix isn't a better model. It's a better substrate: **a body of analytical knowledge that is explicit, linked, versioned, and readable by machines.**

## What "good" looks like

A company with a strong analytical foundation can:

1. **Answer "what's our X?" once**, with one definition, one owner, and one lineage.
2. **Explain any number** by tracing it back through metrics and entities to the source systems and their known problems.
3. **Remember why it decided things** and check whether those decisions worked.
4. **Onboard a new analyst, or a new AI agent, in a day**, by pointing them at the knowledge base.
5. **Get smarter over time**, because each analysis and each decision review adds to what's already known.

Canonical is a framework for building that foundation with tools you already have: text files, Git, and discipline.

## Why not just a semantic layer?

Semantic layers (dbt metrics, LookML, Cube, and others) are excellent, and Canonical complements them. A semantic layer encodes **how to compute** a metric. Canonical also captures:

- **why** the metric is defined this way, and what was considered and rejected
- **caveats** that don't fit in SQL
- **models** of how metrics drive each other
- **analyses and decisions**, the reasoning that consumes the metrics

Think of the semantic layer as the compiler and Canonical as the documentation, the design history, and the lab notebook, all in one graph. A metric artifact can point at its semantic-layer object or certified query through its `implementation` field (see [03 — Analytics reference](03-analytics-reference.md)).

Next: [02 — Architecture](02-architecture.md)
