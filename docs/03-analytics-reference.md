# 03 — Analytics reference

The content house: everything the company knows about its own numbers, written so that a new analyst or an AI agent can do correct work on day one.

## What goes in it

Organize subfolders however suits your company. The checker finds artifacts at any depth. A typical layout:

| Folder | Contents | Example |
|---|---|---|
| `metrics/` | Governed definitions for every number that matters: revenue (ARR, NRR), retention (logo, cohort), funnel (signup → activated → paid), efficiency (CAC payback) | `metric.arr` |
| `data/certified-queries/` | SQL that's been validated and **certified** as the source of truth for a metric | `query.fct-arr-daily` |
| `data/sources/` | Every system of record, what it's authoritative for, and its **known issues** | `source.stripe` |
| `data/entities/` | Business objects and their grain: customer, subscription, user, workspace | `entity.customer` |
| `models/` | How metrics connect: ARR bridges, driver trees, how the financial model is built | `model.arr-bridge` |
| `finance/` | Everything needed to calculate financial metrics: vendor register (every vendor, cycle, terms), AP/AR conventions, expense tracking, close calendar | `register.vendors` |
| `product/` | Mapping of engagement and user data to product concepts: what "active" means, activation, seat utilization | `entity.engagement-event` |
| `frameworks/` | **Horizontal** methods that apply across domains: growth accounting, mix-shift analysis, cohort methods | `framework.mix-shift` |
| `history/` | Analyses (question, method, finding, confidence) and decisions (expected outcome, review date) | `decision.2026-10-annual-plan-discount` |

## Artifact format

Each artifact is one Markdown file with frontmatter. The reference tool parses a deliberately small YAML subset: `key: value` and inline lists `key: [a, b]`.

### Common fields

| Field | Required | Description |
|---|---|---|
| `id` | yes | `<type>.<slug>`, globally unique |
| `type` | yes | see below |
| `title` | yes | Human-readable name |
| `owner` | yes | Person or team accountable. Use `unowned` honestly instead of guessing |
| `status` | yes | `draft` · `reviewed` · `deprecated` |
| `updated` | yes | ISO date of the last meaningful change |
| `depends_on` | no | Ids this artifact is built from |
| `tags` | no | Free-form |

### Types

Types are ordered from fundamental to derived. An artifact may only `depend_on` the same level or a lower one.

| Level | Type | Extra required fields | Body sections |
|---|---|---|---|
| 0 | `source` | `system` | Authoritative for · Not authoritative for · Tables · Known issues |
| 0 | `register` | `system` | What this is · the register table · Rules |
| 0 | `tooling` | `system` | Connection · What works · Gotchas (lives in `execution/tooling/`) |
| 1 | `entity` | `grain`, `primary_key` | Definition · Identifiers across sources · Edge cases |
| 2 | `query` | `certified_by`, `certified_on`, `warehouse_object` | What it returns · SQL · Validation |
| 3 | `metric` | `unit`, `grain` | Definition · Formula · Caveats · History |
| 4 | `model` | `kind` | Relationships · Assumptions · Sensitivities |
| 4 | `framework` | none | What it is · When to use it · How we apply it · Pitfalls |
| 5 | `analysis` | `question`, `confidence` | Question · Method · Findings · Conclusion · What this changes |
| 6 | `decision` | `decided_on`, `review_on`, `outcome` | Decision · Rationale · Expected outcome · Alternatives considered |

Use `[[id]]` in body text to link anywhere. These are Obsidian-compatible wiki links, so the reference doubles as a browsable graph.

## Certification

A certified query is the **only** sanctioned way to compute its metric. Certifying it means a named owner has reconciled it against an independent source (for example, ARR against the billing system's MRR report) and recorded the reconciliation under **Validation**. If the query changes after `certified_on`, the checker warns until someone re-certifies it.

## What the checker enforces

`python3 tools/kb.py check <kb_root>`

- **Errors:** missing required fields, unknown types, duplicate ids, broken `depends_on` or `[[links]]` (including links inside skills), dependencies pointing up a level.
- **Warnings:** unowned artifacts, drafts older than 30 days, queries changed after certification, decisions past their review date, artifacts nothing links to.

Next: [04 — Execution](04-execution.md)
