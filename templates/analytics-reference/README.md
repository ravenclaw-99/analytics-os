# analytics-reference/

The content house: everything the company knows about its own numbers. Each subfolder has a short README saying what goes there and which blank to copy.

| Folder | What goes there |
|---|---|
| `metrics/` | Governed metric definitions |
| `data/sources/` | Systems of record and their known issues |
| `data/entities/` | Business objects, their grain, and their joins |
| `data/certified-queries/` | SQL certified as the source of truth for a metric |
| `models/` | Revenue bridges, driver trees, operating-model build notes |
| `frameworks/` | Horizontal methods: growth accounting, mix shift, LMDI, cohort methods |
| `finance/` | Vendor register, AP/AR conventions, expense tracking |
| `product/` | Engagement and usage data mapped to product concepts |
| `history/` | Analyses and decisions, with review dates |

Rename or add folders to fit your company. The checker finds artifacts at any depth.
