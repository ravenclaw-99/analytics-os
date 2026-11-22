# execution/

How work gets done with the analytics reference.

- **`skills/`**: one folder per recurring analytical task, with a `SKILL.md` in the Agent Skills format. Start with the task that eats the most analyst time, often the monthly flux or a forecast-vs-forecast comparison.
- **`tooling/`**: one artifact per connected system, covering the connection, what works, and the gotchas. Write the tooling note for a system before the first skill that uses it.

Skills link to the reference with `[[id]]`, and `kb.py check` verifies every link, so a renamed definition fails the check instead of silently breaking a workflow.

| Skill | What it does |
|---|---|
| | |
