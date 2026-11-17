# Check 2 — Semantic integrity (weekly, agent pass)

**Goal:** the knowledge base agrees with itself. Every governed concept has one meaning, and every place that uses it uses that meaning.

## Inputs
- `system/reports/semantic-integrity.json` from the deterministic pass (`tools/checks/semantic_integrity.py`). Its `review_sets` list, for each canonical term, every file that discusses it.
- `system/config.json` → `canonical_terms`.
- The whole of `analytics-reference/` and `execution/`.

## Procedure

### A. Known-claim consistency
For each term in `review_sets`:
1. Read the canonical artifact. Note the exact definition: grain, filters, inclusions and exclusions, units, time zone, and the certified query.
2. Read every other file in the set. For each usage, decide: **consistent**, **narrower but compatible** (fine if stated, e.g. "ARR for annual plans only"), or **conflicting**.
3. A conflict is anything that would produce a different number: different inclusions (e.g. one-time fees), different grain (user vs. account), different event (`session_start` vs. `workflow_run`), different time zone.
4. Check certified queries: does the SQL actually implement the definition text? (Filters in the prose must appear in the SQL.)

### B. Full-scan self-agreement
Look for contradictions between any two claims anywhere in the knowledge base, not just governed terms:
- conventions (close day, time zone, fiscal calendar)
- numbers stated as facts (targets, thresholds, sync cadences)
- ownership (two artifacts naming different owners for the same thing)
- lineage (a metric's `implementation` disagreeing with the certified query it depends on)

### C. New terms
List any term defined in two or more places that is **not** in `canonical_terms`. Propose a canonical artifact for it and the config entry.

## Output
Follow the output contract in `_shared-rules.md`, merging with the deterministic findings, and use these kinds: `conflicting_usage`, `sql_definition_mismatch`, `contradiction`, `candidate_canonical_term`. For each conflict, quote both sides and say which one is right **according to the canonical artifact**. If the canonical artifact itself looks wrong, say so, with severity `high`.
