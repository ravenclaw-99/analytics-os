# Starter knowledge base

Copy this whole folder to start your own Groundtruth knowledge base:

```bash
cp -R templates ~/my-kb
cd ~/my-kb
python3 /path/to/groundtruth/tools/kb.py check .
```

It starts empty, so the first check reports `0 artifacts · 0 errors`. Then follow the first 30 days in [docs/07-adoption.md](../docs/07-adoption.md).

```
AGENTS.md               Ground rules any AI agent reads first. Fill in the <placeholders>
analytics-reference/    The content house. Each subfolder's README says what goes there
execution/
  skills/               One folder per recurring task, each with a SKILL.md
  tooling/              One file per connected system (warehouse, planning tool, Sheets)
system/                 Automated checks. Turn these on in week 4
blanks/                 Blank artifacts to copy. The checker ignores this folder
```

## Adding an artifact

1. Copy the matching blank from `blanks/` into the right folder, for example `blanks/metric.md` → `analytics-reference/metrics/arr.md`.
2. Fill in the frontmatter: `id` (`<type>.<slug>`, like `metric.arr`), `title`, a real `owner` (or `unowned`, honestly), `status: draft`, and today's date in `updated`.
3. Write the body sections. Link other artifacts with `[[id]]` instead of repeating what they say.
4. Run `kb.py check`. It flags missing fields, broken links, and artifacts that nothing links to.

The artifact format is described in [docs/03-analytics-reference.md](../docs/03-analytics-reference.md), and skills and tooling in [docs/04-execution.md](../docs/04-execution.md). For a filled-in example of every type, see [examples/lumen/](../examples/lumen/).
