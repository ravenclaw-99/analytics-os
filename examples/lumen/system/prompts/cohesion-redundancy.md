# Check 3 — Organizational cohesion & redundancy (weekly, agent pass)

**Goal:** an agent can find any piece of knowledge quickly, and each piece of knowledge exists once.

## Inputs
- `system/reports/cohesion-redundancy.json` from the deterministic pass (`tools/checks/cohesion.py`).
- `index.json` (run `tools/kb.py index` first), `AGENTS.md`, and the whole knowledge base.

## Procedure

### A. Findability test
1. Write 15 realistic questions a finance, product, data, or BizOps person would ask (e.g. "what's our NRR and why did it move?", "which vendors renew next quarter?").
2. For each, starting from `AGENTS.md`, find the answer by following folders and links. Record the number of files opened and any dead ends.
3. Any question needing more than 4 file opens, or that you answered from the wrong artifact first, is a cohesion finding. Propose the link, move, or index entry that would have taken you straight there.

### B. Structure
- Does `AGENTS.md` accurately describe the current layout? Propose edits if not.
- Are there clusters of artifacts that belong together but are scattered, or folders mixing unrelated domains?
- Are any artifacts trying to cover several topics? Propose a split.

### C. Redundancy (paraphrase-level)
The deterministic pass only catches near-verbatim duplicates. Look for:
- the same fact stated in different words in two or more places
- artifacts whose scope overlaps so much they should be merged
- skills that restate definitions instead of linking them

For each one, propose **where the knowledge should live** (the most fundamental artifact) and the exact text to replace the copies with a link.

## Output
Follow the output contract in `_shared-rules.md`, merging with the deterministic findings. Use these kinds: `hard_to_find`, `agents_md_stale`, `scattered`, `split_candidate`, `paraphrased_duplicate`, `merge_candidate`, `skill_restates_definition`. Report the findability score: questions answered in ≤ 4 opens, out of 15.
