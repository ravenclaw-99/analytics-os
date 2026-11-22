---
name: review-kb-checks
description: Walk the knowledge-base owner through the latest automated-check findings one at a time (explain, discuss, accept, refine, or reject), record every decision in the review ledger, and open one pull request with the accepted fixes. Use when someone says "review the KB checks", pastes a finding code like SCH-3eb1e7 from the Slack summary, or asks what the checks found.
---

# Review knowledge-base check findings

The scheduled checks post a summary to Slack with a code for each finding. This skill is how the owner acts on them: a conversation, not a form. You explain each finding in plain language, help the owner decide, record the decision, and turn the accepted fixes into a single pull request.

## Inputs
- **Which findings**: one or more codes (e.g. `SCH-3eb1e7`), a check name, or "all open". The default is all open findings, highest severity first.
- **Reviewer name**: who is deciding. Ask once if you don't know.

In the commands below, `GT` is the Groundtruth runtime: `python3 <tools>/runtime/cli.py`. In this example it's `python3 ../../tools/runtime/cli.py`, run from the knowledge-base root.

## Steps

1. **Get the latest reports.** Pull the default branch. If the reports are attached to a CI run instead of committed, download them into `system/reports/` (for GitHub Actions: `gh run download --name kb-check-reports`).
2. **List what's waiting.** Run `GT findings .`. Tell the owner how many findings are open, by severity, and which are auto-accepted.
3. **Auto-accepted findings first.** If any are listed as auto-accepted (Level 2), show them as a short list and ask: "Apply all of these, or pull any out for discussion?" Record each one you apply with `--source auto`. Anything pulled out goes into the normal flow below.
4. **One finding at a time.** For each finding, run `GT show . <REF>`, then:
   - **Explain it plainly**: what's wrong, where, why it matters, and who could be misled. Open the file in `where` and show the relevant lines. Don't just repeat the message.
   - **Give both opinions**: the system's recommendation and confidence, and the reviewer agent's opinion if there is one. Mention any past decision on the same code.
   - **Discuss.** Answer the owner's questions. Check the warehouse or related artifacts if they ask. Never push them toward an answer.
   - **Decide.** The owner chooses one of:
     - **accept**: the fix is right as written
     - **refine**: the owner says what to change. Revise the fix, show the exact edit, and ask again (accept, refine more, or reject)
     - **reject / ignore**: ask for one sentence on why. The reason is how the check learns, and a rejected finding stays hidden on later runs
5. **Record every decision as it's made**, before moving on:
   - `GT record . <REF> accept --by <name> --minutes <n> --pr kb-review/<YYYY-MM-DD>` (the branch the fix goes on)
   - `GT record . <REF> refine --by <name> --refinement "<what to change>"`, then a second `record` with the final accept or reject
   - `GT record . <REF> reject --by <name> --reason "<why>"`
6. **Apply the accepted fixes** on a new branch named `kb-review/<YYYY-MM-DD>`. Follow `AGENTS.md`: smallest correct change, links instead of copies, and new or edited artifacts stay `status: draft` unless the owner explicitly says to mark them reviewed.
7. **Validate.** Run `python3 <tools>/kb.py check .`. It must show 0 errors. Fix anything you broke.
8. **Update what the system learned.** Run `GT learn .` so the next run uses the new decisions.
9. **Open one pull request**, after showing the owner the summary and getting a yes. Commit the fixes, `system/state/review-ledger.jsonl`, `calibration.json`, and `review-lessons.md` together, so the decisions and the fixes merge (or get reverted) as one unit. The PR body lists every code with its decision and a one-line summary. A session that only rejected findings still opens a PR, containing just the ledger and lessons.
10. **Wrap up.** Run `GT stats .` and tell the owner the agreement rate for the kinds they just reviewed, and whether any kind is now eligible for auto-accept.

## Rules
- **The owner decides.** You explain and draft. You never accept, reject, or refine on their behalf, except for findings already auto-accepted under Level 2.
- **Definition changes and certifications are the artifact owner's call.** If a fix changes what a metric means or certifies a query and the person reviewing isn't that artifact's `owner`, record it as refine with "needs <owner>", and don't apply it.
- **One finding at a time.** Don't batch normal findings into a single question.
- **Plain language.** The owner may not be technical. Explain table and column names in terms of what they're used for.
- **Ask before anything leaves the machine**: pushing a branch, opening a PR, or posting to Slack.

## Output contract
For each finding reviewed, a ledger line. One pull request (with the owner's OK) containing the accepted fixes and the updated `system/state/` files. Finish with a short summary: decisions by type, the PR link, and the stats from step 10.
