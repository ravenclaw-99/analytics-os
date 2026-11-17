#!/usr/bin/env bash
# Run one automated check. Execute from the knowledge-base root.
#
#   system/jobs/run.sh <check>
#
# checks: schema-integrity | semantic-integrity | cohesion-redundancy |
#         proactive-enrichment | analytical-gaps
#
# Environment:
#   GROUNDTRUTH_TOOLS  path to the Groundtruth tools/ folder   (default: ../../tools)
#   CATALOG            warehouse catalog JSON for schema checks (default: system/state/catalog.json)
#   AGENT_CMD          headless agent command that takes a prompt as its last argument and
#                      has the MCP servers this check needs, e.g. Claude Code: "claude -p"
set -euo pipefail

CHECK="${1:?usage: system/jobs/run.sh <check>}"
TOOLS="${GROUNDTRUTH_TOOLS:-../../tools}"
CATALOG="${CATALOG:-system/state/catalog.json}"

agent() {
  local prompt
  prompt="$(cat system/prompts/_shared-rules.md system/prompts/"$1".md)"
  if [[ -z "${AGENT_CMD:-}" ]]; then
    echo "AGENT_CMD not set; skipping the agent pass for $1 (deterministic results are still in system/reports/)." >&2
    return 0
  fi
  $AGENT_CMD "$prompt"
}

case "$CHECK" in
  schema-integrity)
    # The catalog is one information_schema query (system/config.json → warehouse.catalog_query),
    # exported by your warehouse CLI or MCP before this runs.
    python3 "$TOOLS/checks/schema_integrity.py" . --catalog "$CATALOG"
    ;;
  semantic-integrity)
    python3 "$TOOLS/checks/semantic_integrity.py" .
    agent semantic-integrity
    ;;
  cohesion-redundancy)
    python3 "$TOOLS/kb.py" index .
    python3 "$TOOLS/checks/cohesion.py" .
    agent cohesion-redundancy
    ;;
  proactive-enrichment | analytical-gaps)
    agent "$CHECK"
    ;;
  *)
    echo "unknown check: $CHECK" >&2
    exit 2
    ;;
esac
