---
id: tooling.html-dashboards
type: tooling
title: Shareable HTML dashboards
owner: bizops
status: reviewed
updated: 2026-11-22
system: Internal static host (dashboards.lumen.internal, behind SSO)
tags: [tooling, output, dashboards]
---

## Connection
- A dashboard is **one self-contained HTML file**: data embedded as JSON, styles inline, charts drawn with one pinned charting library loaded from a CDN. It reads no live data and holds no credentials.
- Publish by uploading to the `dashboards/` bucket through the internal-host MCP. The file is then served at `https://dashboards.lumen.internal/<slug>/`, readable by anyone at Lumen after SSO. Re-uploading to the same slug replaces the page and keeps the link.
- Draft first: upload to `dashboards/_drafts/<slug>/` and share the link with the requester only. Move it to the final slug once they're happy.

## What works
**House format.** Every dashboard uses the same layout and formatting, so readers never have to relearn one:

| Element | Rule |
|---|---|
| Header | Title, one-sentence purpose, **as-of date**, owner |
| Top row | 3–5 stat tiles: value, change vs. the comparison period, comparison label |
| Charts | One question per chart. The title states the takeaway, for example "Annual share of new bookings is rising" |
| Currency | `$1.2M`, `$840K`, `$9,400`. Full dollars only in tables |
| Percentages | One decimal (`2.6%`). Changes in percentage points are labeled `pts` |
| Dates | `2026-10` for months, `2026-Q3` for quarters, ISO dates elsewhere |
| Colors | Brand palette: one accent color for the headline series and grey for comparisons. Red and green only for bad and good |
| Footer | **Definitions** (each metric's id linking to the knowledge base), sources, and query names |
| Theme | Works in light and dark mode and at phone width |

- Start from the template in the `lumen/dashboards` repo (`templates/house.html`) instead of writing styles from scratch.
- Keep embedded data at the grain the charts need, aggregated. Never embed row-level customer data.

## Gotchas
- Snapshot data goes stale silently. The as-of date in the header is mandatory, and a dashboard that should refresh needs a scheduled job, not a re-upload by hand.
- Large embedded datasets (over about 5 MB) make the page slow on phones. Aggregate before embedding.
- Anyone at Lumen can open a published page. Anything that's only for finance or the board goes in Drive with restricted sharing instead.
