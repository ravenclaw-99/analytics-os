# 05 — System: keeping it alive

## The problem: knowledge bases go stale

Everything in `analytics-reference/` and `execution/` is a snapshot. Connecting an AI to all your systems (the warehouse, GitHub, the Airflow DAGs that build tables, Google Drive) lets it *read* that snapshot. It doesn't keep the snapshot true.

The business keeps moving. Every week, products launch, tables get deprecated, pipelines get re-architected, and people start analyzing data in new ways based on conversations the knowledge base never sees. Within weeks, a knowledge base that was accurate on day one is quietly wrong. An agent working from a stale knowledge base is worse than one with none, because it's confident.

**This is the problem Groundtruth exists to solve.** The solution is a set of automated checks that run on a schedule. At first they're **human-in-the-loop reviews**: they find problems and propose fixes, and people decide.

## The five checks

| # | Check | Cadence | Kind | Question |
|---|---|---|---|---|
| 1 | Schema integrity | daily | deterministic | Is everything the knowledge base mentions still live? |
| 2 | Semantic integrity | weekly | deterministic + agent | Does the knowledge base agree with itself? |
| 3 | Organizational cohesion & redundancy | weekly | deterministic + agent | Is it organized for fast retrieval, with no duplication? |
| 4 | Proactive enrichment | weekly | agent | What changed in the business that the knowledge base is missing? |
| 5 | Analytical gaps | weekly | agent | What are people analyzing that isn't captured yet? |

Checks 1–3 protect what's **already in** the knowledge base. Checks 4–5 bring **new knowledge in**. Together they make it recursive: the knowledge base keeps re-validating itself against reality and growing from the work people actually do.

---

### 1. Schema integrity (daily)

The basic layer. Through the warehouse MCP or CLI, run one `information_schema` query against Snowflake, Redshift, Supabase/Postgres, or whatever you use. Then deterministically verify:

- **Every table mentioned anywhere** in the knowledge base (references, certified queries, `implementation` fields) still exists.
- **Every column documented** for a key table still exists.
- **Every column that exists** in a key table is documented somewhere. The key-tables register lists the tables where coverage must be complete.

When a table or column has disappeared, the check suggests the likely rename (`fct_nrr_monthly` → `fct_nrr_monthly_v2`). It runs daily because schema drift breaks things immediately.

`tools/checks/schema_integrity.py`

### 2. Semantic integrity (weekly)

Every governed concept (ARR, DAU, NRR) has **one canonical artifact**, declared in `system/config.json` → `canonical_terms`.

- **Known-claim consistency.** The deterministic pass finds every place a governed term appears. It flags *competing definitions* (text outside the canonical artifact that defines the term) and *unlinked mentions*. Whenever ARR or DAU is added anywhere new, it's checked against the validated definition.
- **Full-scan self-agreement.** The agent pass reads every usage of each term and checks that the *meaning* agrees: same inclusions, grain, events, and time zone. It then scans for contradictions anywhere (close calendar, thresholds, owners) and checks that certified SQL implements its prose definition.

Weekly is enough. Definitions don't change daily, and this pass reads the whole knowledge base.

`tools/checks/semantic_integrity.py` + `prompts/semantic-integrity.md`

### 3. Organizational cohesion & redundancy (weekly)

- **Cohesion.** Is everything stored where an agent will look for it? The deterministic pass checks folder conventions, oversized artifacts, and dead ends. The agent pass runs a **findability test**: it writes 15 realistic questions, answers each one starting from `AGENTS.md`, counts the files it had to open, and proposes the links or moves that would shorten the path.
- **Redundancy.** Is anything stored twice? The deterministic pass finds near-verbatim duplicates across files. The agent pass finds paraphrased duplicates, merge candidates, and skills that restate definitions. Every proposal says where the knowledge should live and how to replace the copies with links. This keeps the knowledge base from growing without limit.

`tools/checks/cohesion.py` + `prompts/cohesion-redundancy.md`

### 4. Proactive enrichment (weekly)

How knowledge gets *added* efficiently. Since the last run, the agent scans:

- **every PR merged to production** in the configured repos: DAGs, dbt models, migrations, tracking plans, feature flags. This catches launches and data-architecture changes.
- **Slack** conversations in configured channels: definitions agreed, decisions made.
- **key decks and running documents** in configured Drive folders.

For each signal, it checks whether the knowledge base already reflects it. If not, it proposes the smallest correct change, with the evidence link, grouped by the owner who should review it.

`prompts/proactive-enrichment.md`

### 5. Analytical gaps (weekly)

Looks at the analysis people are actually doing: questions in analytics channels, questions agents couldn't answer from governed definitions, recurring ad-hoc queries in warehouse history, new analysis docs. It asks: *is this documented anywhere?*

When several people keep working on a concept or task that isn't captured, it scores the gap (frequency, breadth, stakes, inconsistency). Then it drafts a stub metric or skill and a short message **asking the team** whether to adopt it. The message isn't sent until a person approves.

`prompts/analytical-gaps.md`

---

## Human in the loop, then graduate

Every check writes `system/reports/<check>.md` (for people) and `.json` (for machines). Nothing is changed automatically:

1. Each finding arrives with a recommended action. A named reviewer then **accepts**, **rejects** (with a reason), or **refines** it (says what to change, and the agent re-proposes).
2. Accepted fixes merge as pull requests, gated by `tools/kb.py check`.
3. Once a *category* of finding has a long run of correct recommendations (for example, "add a newly created column to the key-tables register"), let that category auto-fix. Keep definition changes human-approved permanently.

## Running it

```bash
cd examples/lumen
CATALOG=system/fixtures/catalog.json system/jobs/run.sh schema-integrity
system/jobs/run.sh semantic-integrity
system/jobs/run.sh cohesion-redundancy
AGENT_CMD="claude -p" system/jobs/run.sh proactive-enrichment   # needs GitHub/Slack/Drive MCPs
```

See `examples/lumen/system/schedule.md` for cadences, reviewers, and a GitHub Actions example.

Next: [06 — Runtime](06-runtime.md)
