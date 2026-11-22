# system/

Production code that keeps the knowledge base true: scheduled jobs, the prompts they run, and the five automated checks. Leave this empty for the first few weeks, while you write your first artifacts.

**When to turn it on** (week 4 in [docs/07-adoption.md](../../docs/07-adoption.md)):

1. Copy `examples/lumen/system/` here as a starting point, then delete the example's generated reports and state.
2. Edit `system/config.json` for your company: your warehouse schemas, the id of your key-tables register, and `canonical_terms` (each governed term mapped to the one artifact that defines it).
3. Schedule `kb.py check` and the schema-integrity check daily. Add the weekly checks once you have about 20 artifacts.

How the checks work: [docs/05-system.md](../../docs/05-system.md). How they run: [docs/06-runtime.md](../../docs/06-runtime.md).
