# Check 4 — Proactive enrichment (weekly)

**Goal:** catch every change in the business, product, and data platform that the knowledge base should reflect, before it goes stale.

## Inputs (read only what `system/config.json` → `enrichment` allows)
- **GitHub:** every PR merged to production since the last run (`system/state/last-run.json`) in the configured repositories: data pipelines (Airflow DAGs, dbt models), application code (launches, feature flags, tracking-plan changes), and migrations.
- **Slack:** messages since the last run in the configured channels.
- **Google Drive:** key decks and running documents in the configured folders that were modified since the last run.

## What to look for

| Signal | Example | Typical knowledge-base change |
|---|---|---|
| Table or column created, renamed, deprecated | dbt PR renames `fct_nrr_monthly` → `fct_nrr_monthly_v2` | Update references; flag certified queries for re-certification |
| Pipeline re-architecture | DAG now builds ARR hourly from a new staging model | Update the source's sync and tables, plus known issues |
| Product launch or deprecation | New "Teams" plan ships behind a feature flag | New plan values in entities; caveats on ARPA, mix |
| Tracking change | New event, or an event's meaning changes | Engagement mapping; caveats on DAU and funnels |
| A definition agreed in conversation | "From Q1 we exclude pilots from NRR" in #finance | Draft history entry on the metric; flag the canonical artifact for an owner's review |
| A decision made | Pricing change agreed in the exec deck | Draft decision artifact with expected outcome and review date |
| New vendor or contract | Procurement thread for a new tool | Vendor register row |

## Procedure
1. Collect signals from each source. For each signal, search the knowledge base for what it affects.
2. Throw out signals that are already reflected, or that don't change any analytical fact.
3. For each remaining signal, propose the smallest correct change: name the target artifact, the exact edit, and the evidence link.
4. Group the proposals by target artifact so the owners can review them in one pass.
5. Update `system/state/last-run.json` with this run's watermark.

## Output
Follow the output contract in `_shared-rules.md`. Use these kinds: `schema_change`, `pipeline_change`, `product_launch`, `tracking_change`, `definition_change`, `decision`, `vendor`. A definition change agreed in conversation is always `high` and goes to the canonical artifact's owner. Never apply it yourself.
