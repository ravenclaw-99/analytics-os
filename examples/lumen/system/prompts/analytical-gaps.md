# Check 5 — Analytical gaps (weekly)

**Goal:** find the analysis people are actually doing that the knowledge base doesn't support yet, and ask the team whether to capture it.

## Inputs (as allowed by `system/config.json` → `gaps`)
- Questions asked in the configured analytics and data Slack channels.
- Agent session logs: questions put to this knowledge base, especially ones answered "not governed" or with `low` confidence.
- Warehouse query history: recurring ad-hoc queries by different people against the same tables.
- New spreadsheets and docs in the configured analysis folders.

## What counts as a gap
- **Concept gap:** a metric or concept people discuss or compute that has no artifact (e.g. "net dollar churn by segment", "payback by channel").
- **Skill gap:** a task done repeatedly by hand, by several people or every week (e.g. building the same board-prep pivot), with no skill in `execution/skills/`.
- **Knowledge gap:** a question that keeps being asked and answered in chat, where the answer belongs in the reference (e.g. "why does March look weird?").

## Procedure
1. Cluster the signals by concept or task. Ignore one-offs.
2. Score each cluster on importance:
   - **frequency** (times per week)
   - **breadth** (number of distinct people)
   - **stakes** (exec, board, or pricing context scores higher)
   - **inconsistency** (different people getting different answers scores highest)
3. For each cluster above the threshold, decide what to propose: a metric, a framework, a skill, or a caveat or known issue on an existing artifact.
4. Draft the stub artifact or skill as `status: draft`, filling in only what the evidence supports.
5. Draft a **short message to the people involved** asking whether to adopt it. Name what you saw, the proposed artifact, and the one decision you need from them (for example the owner, or which definition is right). **Don't send it.** The human reviewer sends it, or approves the runner to.

## Output
Follow the output contract in `_shared-rules.md`. Use these kinds: `concept_gap`, `skill_gap`, `knowledge_gap`. Each finding includes the importance score breakdown, the drafted stub's path, and the drafted outreach message.
