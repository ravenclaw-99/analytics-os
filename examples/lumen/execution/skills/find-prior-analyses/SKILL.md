---
name: find-prior-analyses
description: Find analyses someone already did on a narrow question by searching the knowledge base, agent memory files, Slack, Google Drive, and GitHub in a fixed order, then return a short ranked list with links. Use before starting new analysis, or when someone says "I know we looked at this before" but can't find where.
---

# Find prior analyses

## Inputs
- **Question**: what the analysis was about, as narrow as possible ("annual vs. monthly churn by seat band", not "churn").
- **Time window**: default is the last 18 months.
- **Hints** (optional): who might have done it, a channel, a rough date, what it looked like (deck, sheet, notebook).

## Steps

1. **Turn the question into a search brief** before searching anything:
   - the governed metrics involved, found in `analytics-reference/metrics/` (for example [[metric.logo-churn-rate]]), plus the informal names people use for them
   - 2–3 distinctive terms (a segment, a cohort, a vendor, a decision)
   - the time window and any people or places from the hints
2. **Search the knowledge base first.** Look in `analytics-reference/history/`: analyses (for example [[analysis.2026-09-churn-by-cohort]]) and decisions (for example [[decision.2026-10-annual-plan-discount]]). Follow their links. If `index.json` exists, search titles and `question` fields there. If you find a reviewed analysis that answers the question, stop and return it.
3. **Then search the other sources in this order**, using the syntax and scopes in [[tooling.workspace-search]]:
   1. agent memory files (only with the user's permission)
   2. Slack
   3. Google Drive
   4. GitHub

   Start narrow: metric name + one distinctive term + the time window. Widen one term at a time, only if nothing comes back. Stop after about 10 searches per source and report what you tried.
4. **Open every candidate** and confirm it actually addresses the question. A title match is not enough. For Slack hits, read the whole thread.
5. **Rank the candidates**: (a) answers the exact question, (b) most recent, (c) has a stated method and an owner. Drop duplicates and drafts that were superseded by a later version.
6. **Check the definitions it used.** If a candidate used a definition that has since changed (see each metric's History section, for example [[metric.dau]]), say so. Its numbers may not be comparable anymore.

## Output
At most 5 results, best first. For each one:
- **Link** and **source** (KB, Slack, Drive, GitHub, memory)
- **Date** and **author**
- **One-line finding**, in your own words
- **Match**: exact, close, or related, and why
- **Still valid?** yes, or no with the reason (definition changed, data issue found since)

Then list the searches you ran, so the user can see what was covered.

## Rules
- Don't quote private channels or personal drives unless the user added them.
- Never present a found number as current. Give its date.
- **Write back what you find.** If a good analysis lives only in Slack, Drive, or GitHub, offer to save it as a draft analysis in `analytics-reference/history/analyses/` (use the blank analysis template), linking the original. That's how the knowledge base catches up with the work people already did.
