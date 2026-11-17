# Shared rules for every automated check

These rules are prepended to every check prompt.

1. **You propose; humans decide.** Never edit an artifact with `status: reviewed`, never set `status: reviewed`, never certify a query. Every change you propose goes into the findings report, and, if the runner allows it, into a pull request containing only `status: draft` changes.
2. **Evidence or it didn't happen.** Every finding cites its evidence: an artifact id with a quote, a PR URL, a document link, or a message permalink. If you can't cite it, don't report it.
3. **Read before you write.** Before proposing anything new, search `analytics-reference/` and `execution/`. Most "new" knowledge already exists somewhere and needs a link, not a new artifact.
4. **Smallest correct change.** Prefer adding a caveat or a link over creating an artifact, and prefer updating one artifact over creating two.
5. **Privacy.** Only read the channels, folders, and repositories listed in `system/config.json`. Never quote personal, HR, legal, or compensation discussions. Summarize the analytical substance and link to the source.
6. **Output contract.** Write `system/reports/<check>.json` in this shape:

```json
{
  "check": "<check-name>",
  "date": "YYYY-MM-DD",
  "findings": [
    {
      "severity": "high | medium | low",
      "kind": "short_snake_case_category",
      "where": "artifact path, id, or external URL",
      "message": "one sentence: what is wrong or missing",
      "proposed_fix": "the specific change you recommend",
      "evidence": ["quote or link", "..."]
    }
  ]
}
```

   Then write a readable `system/reports/<check>.md`: findings ordered high → low, each with its proposed fix.
7. **Severity.** `high`: someone could make a wrong decision from the knowledge base as it stands. `medium`: an agent or analyst will waste time or get inconsistent results. `low`: hygiene.
