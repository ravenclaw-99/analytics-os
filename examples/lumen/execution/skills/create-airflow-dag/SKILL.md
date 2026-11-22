---
name: create-airflow-dag
description: Write a new Airflow DAG (ETL job) for Lumen's data pipelines from a plain-language description, with tests, and open it as a pull request for data-team review. Use when someone needs a new table loaded, a transformation scheduled, or an existing pipeline changed.
---

# Create an Airflow DAG

## Inputs
- **What**: the data to load or transform, and the table it should produce.
- **Cadence**: how fresh the data must be (default: daily).
- **Owner**: the team accountable for the DAG (required; ask if it isn't given).

## Steps

1. **Check that it doesn't exist already.** Look for the target in [[register.key-tables]] and in the source artifacts (for example [[source.stripe]] lists the tables already synced from billing). List existing DAGs through the read-only Airflow API described in [[tooling.airflow]]. If something close exists, propose changing it instead of adding a new one.
2. **Read the source's known issues** in its artifact under `analytics-reference/data/sources/`. They often decide the design, for example the refund lag in [[source.stripe]] means a daily revenue load must re-process the last few days, not just yesterday.
3. **Find the grain and key** of the output. Use the entity definitions (for example [[entity.customer]], [[entity.subscription]]). Write them in the PR description in one sentence: "one row per … per …".
4. **Design the DAG** with the conventions in [[tooling.airflow]]: name, UTC schedule, default args, idempotent partition overwrite, and the shared operators. Put the SQL in a dbt model. The DAG only schedules and orders tasks.
5. **Write the tests**: the DAG-import test plus dbt `unique` and `not_null` tests on the output's key.
6. **Dry-run the SQL** read-only through [[tooling.warehouse-mcp]] on one partition, with a `limit`. Report the row count and a sample.
7. **Open a pull request** on `lumen/data-pipelines` through the GitHub MCP. In the description, include: what it does, the grain, the schedule, the backfill plan (or "none"), the dry-run result, and the knowledge-base updates from step 8.
8. **Draft the knowledge-base updates** in the same session, as `status: draft`:
   - a row set in [[register.key-tables]] for the new table, if it's a key table: **every column** documented
   - a new or updated source artifact, if it's a new system of record
   - a known issue, if you found one while building

## Rules
- Never trigger, pause, or backfill a DAG, and never merge. Agents open PRs. People review and merge.
- Never hard-code credentials or connection strings.
- If the request needs a definition that isn't governed (for example a new metric), stop and propose the definition first. Don't encode an ungoverned definition in a pipeline.

## Output contract
A PR link, the dry-run summary, and links to the draft knowledge-base edits.
