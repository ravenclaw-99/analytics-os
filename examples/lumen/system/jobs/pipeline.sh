#!/usr/bin/env bash
# One full scheduled run of a check: check → reviewer agent → delivery. Execute from the KB root.
#
#   system/jobs/pipeline.sh <check> [--send]
#
# 1. Runs the check (system/jobs/run.sh): deterministic pass, then the agent pass if AGENT_CMD is set.
# 2. Level 1: if this check is listed in config.json → autonomy.reviewer_agent and AGENT_CMD is set,
#    a reviewer agent gives an independent opinion on every finding (system/reports/<check>.review.json).
# 3. Delivers one summary. Without --send, or without GROUNDTRUTH_SLACK_WEBHOOK_URL, it is only printed.
#
# Nothing here changes the knowledge base. People act on findings later with the review-kb-checks skill.
#
# Environment: everything run.sh takes, plus
#   GROUNDTRUTH_DELIVERY          stdout | slack          (default: slack, which dry-runs without --send)
#   GROUNDTRUTH_SLACK_WEBHOOK_URL Slack incoming-webhook URL (keep it in your scheduler's secrets)
#   GROUNDTRUTH_REPORT_URL_BASE / GROUNDTRUTH_RUN_URL   where the summary's "full report" link points
set -euo pipefail

CHECK="${1:?usage: system/jobs/pipeline.sh <check> [--send]}"
SEND="${2:-}"
TOOLS="${GROUNDTRUTH_TOOLS:-../../tools}"
GT="python3 $TOOLS/runtime/cli.py"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$HERE/run.sh" "$CHECK"

reviewer_on="$(python3 -c "import json,sys; c=json.load(open('system/config.json')); print('yes' if sys.argv[1] in c.get('autonomy',{}).get('reviewer_agent',[]) else 'no')" "$CHECK")"
if [[ "$reviewer_on" == "yes" ]]; then
  if [[ -n "${AGENT_CMD:-}" ]]; then
    echo "reviewer agent: reviewing $CHECK findings"
    $AGENT_CMD "$($GT reviewer-prompt . "$CHECK")" | $GT ingest-review . "$CHECK"
  else
    echo "reviewer agent is on for $CHECK, but AGENT_CMD isn't set; skipping the second opinion." >&2
  fi
fi

$GT notify . --check "$CHECK" --to "${GROUNDTRUTH_DELIVERY:-slack}" ${SEND:+--send}
