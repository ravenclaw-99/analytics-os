# 07 — Adoption

You don't need a data team, a semantic layer, or a migration project to start. You need a repo and the discipline to write things down.

## The first 30 days

### Week 1: three metrics, certified
Pick the three numbers leadership argues about most. For each one, write a metric artifact with a real owner and a certified query, reconciled against an independent source. You'll run into entity disagreements right away. Write those down too.

### Week 2: sources and registers
Write a source artifact for every system behind those metrics, and put most of the effort into **known issues**. Start the finance registers: the vendor list and AP/AR conventions.

### Week 3: one skill
Pick the recurring task that eats the most analyst time (often the forecast-vs-forecast comparison or the monthly flux) and write it as a skill. Run it with your AI agent. Fix the skill, not the output.

### Week 4: turn on the system
Schedule `kb-check` and **schema integrity** daily, so drift gets caught from day one. Log one real decision with an expected outcome and a review date.

### Month 2: the weekly checks
Add semantic integrity and cohesion/redundancy once you have about 20 artifacts. Add proactive enrichment and analytical gaps once the GitHub, Slack, and Drive connections are in place. Keep all of them human-in-the-loop until their proposals are reliably right.

At the end of 30 days: about 20 artifacts, a skill that saves real hours, and a check that keeps it honest.

## By function

**Finance.** Own `metrics/`, `data/certified-queries/`, `finance/`, and `models/`. The ARR bridge and the vendor register are your anchors.

**BizOps / strategy.** Own `frameworks/` and `history/`, and make decision reviews a standing agenda item.

**Product.** Own `product/` (what "active" and "activated" mean) and the funnel metrics. Every experiment readout becomes an analysis.

**Data science.** Own `data/sources/` and `data/entities/`, keep known issues current, and maintain the warehouse tooling.

## Common failure modes

- **Boiling the ocean.** Documenting 200 metrics on day one. Start with three.
- **Uncertified "sources of truth".** If nobody has reconciled the query, it isn't certified, whatever the dashboard says.
- **Skills that redefine metrics.** Skills should link to the reference, never copy it.
- **Treating it as documentation.** It isn't a wiki you update after the work. It's where the work happens.
