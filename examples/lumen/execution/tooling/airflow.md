---
id: tooling.airflow
type: tooling
title: Airflow pipelines (ETL)
owner: data
status: reviewed
updated: 2026-11-22
system: Airflow (managed) + GitHub repo lumen/data-pipelines, via GitHub MCP
tags: [tooling, etl, pipelines]
---

## Connection
- DAGs live in the `lumen/data-pipelines` repo under `dags/`, one file per DAG. Shared helpers are in `dags/common/`.
- Agents work through the **GitHub MCP**: create a branch, commit, and open a pull request. The Airflow API is **read-only** for agents (list DAGs, read run history and task logs). Agents never trigger, pause, or backfill DAGs.
- Merging to `main` deploys to production within about 10 minutes. A data-team reviewer must approve every PR.

## What works
- **Naming:** `<source>__<target>__<cadence>`, for example `stripe__stg_subscriptions__6h`. The DAG id matches the file name.
- **Schedules are in UTC** cron, like the warehouse (see [[tooling.warehouse-mcp]]). Never schedule into the 00:00–02:00 UTC window, when the Fivetran syncs land.
- **Default args:** `owner` set to a team (not a person), `retries=2`, `retry_delay=10m`, and `sla` set to the cadence. Failures alert `#data-alerts`.
- **Idempotent tasks only.** Each run overwrites one partition (usually the date) with `delete … where partition = …` and then `insert`, or a `merge`. Re-running a date must give the same result.
- **Use the operators in `dags/common/`** (`SnowflakeQueryOperator`, `DbtRunOperator`). Don't call `snowflake.connector` directly in a DAG.
- **Transformations belong in dbt models**, not in DAG Python. The DAG schedules and orders. dbt holds the SQL.
- **Tests in the same PR:** a DAG-import test (`pytest tests/test_dag_integrity.py`) and dbt `unique` + `not_null` tests on the new model's key.

## Gotchas
- `catchup=False` by default. A PR that sets `catchup=True` needs an explicit backfill plan in its description, because merging it starts every missed run at once.
- Connection ids are environment-specific (`snowflake_prod`, `snowflake_dev`). Read them from the `common.connections` helper and never hard-code credentials.
- A new table in `analytics.*` is not done until its columns are documented. If it's a key table, add it to [[register.key-tables]], or the daily schema-integrity check will flag every undocumented column.
