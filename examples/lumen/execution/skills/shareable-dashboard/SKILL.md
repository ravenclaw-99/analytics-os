---
name: shareable-dashboard
description: Turn a plain-language description ("a page showing annual-plan uptake since the discount change") into a single self-contained HTML dashboard with charts, governed definitions, and the house formatting, then publish it to the internal host and return the link. Use when someone wants a page they can send around internally rather than a spreadsheet.
---

# Shareable dashboard

## Inputs
- **Description**: what the page should show and who it's for.
- **Period and comparison**: default is the last 12 months against the prior 12 months.
- **Slug**: a short URL name. Default: derived from the title.

## Steps

1. **Write the spec back to the requester before building.** In 5 lines or fewer: title, the 3–5 headline numbers, the charts (one question each), the period, and the audience. Wait for a yes if they're around. Otherwise state your assumptions at the top of the page.
2. **Resolve every number to a governed metric** in `analytics-reference/metrics/` (for example [[metric.arr]], [[metric.logo-churn-rate]], [[metric.dau]]). If something isn't governed, say so in the spec. Don't invent a definition to fill the chart.
3. **Pull the data** with each metric's certified query or implementation through [[tooling.warehouse-mcp]]. Read the caveats of every metric you use, and apply the ones that affect the chart, for example the cohort maturity rule in [[framework.cohort-methods]].
4. **Check for prior work.** If the description matches an analysis or decision in `analytics-reference/history/` (for example [[decision.2026-10-annual-plan-discount]]), link it in the header and show its expected outcome as a reference line.
5. **Build the page** from the house template, following every rule in [[tooling.html-dashboards]]: header with as-of date, stat tiles, one-question charts with takeaway titles, the number formats, and the definitions footer.
6. **Check the page yourself before sharing:** open it, compare every stat tile to the query result, look at it at phone width and in dark mode, and confirm that no row-level customer data is embedded.
7. **Publish as a draft** to the drafts path in [[tooling.html-dashboards]] and send the requester the link. Move it to the final slug when they approve.

## Rules
- Embedded data is aggregated and dated. A snapshot never pretends to be live.
- Each chart's footer note names the metric id and the query used.
- Finance-only or board-only numbers don't go on the internal host. Use a restricted Sheet instead ([[tooling.google-sheets]]).

## Output contract
The draft link, the spec from step 1, and the as-of date. If a chart needed a metric that isn't governed, include a proposed draft definition.
