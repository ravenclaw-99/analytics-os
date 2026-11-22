"""Review ledger: every accept / reject / refine decision on a finding, one JSON object per line.

The ledger lives at <kb_root>/system/state/review-ledger.jsonl. It is append-only: a decision is
never edited, only followed by a newer one. Everything the runtime learns (agreement rates,
autonomy levels, calibrated recommendations, lessons for the agents) is computed from it.

One line looks like this:

    {"ts": "2026-11-22T14:05:00Z", "ref": "SCH-3f2a1b", "check": "schema-integrity",
     "kind": "missing_table", "where": "analytics.fct_nrr_monthly", "severity": "high",
     "recommended_action": "accept", "confidence": "medium", "reviewer_agent_action": "accept",
     "human_action": "accept", "decided_by": "ben", "source": "human",
     "reason": "", "refinement": "", "pr": "https://github.com/...", "minutes": 3}

`source` is "human" for a person's decision and "auto" for a Level 2 auto-accept. Agreement
statistics count only the FIRST human decision on each finding, because that is the moment the
person judged the system's original recommendation. Later lines (an accept after a refine, a
human spot-check after an auto-accept) are history, not new votes.

Standard library only.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

ACTIONS = ("accept", "reject", "refine")

# Short prefix per check, so a reference code says where it came from at a glance.
CHECK_PREFIX = {
    "schema-integrity": "SCH",
    "semantic-integrity": "SEM",
    "cohesion-redundancy": "COH",
    "proactive-enrichment": "ENR",
    "analytical-gaps": "GAP",
}
CHECKS = list(CHECK_PREFIX)


def finding_ref(check: str, kind: str, where: str) -> str:
    """Stable reference code for a finding, e.g. SCH-3f2a1b.

    The same problem in the same place gets the same code on every run, so a decision made
    last week still applies when the check runs again.
    """
    prefix = CHECK_PREFIX.get(check, check[:3].upper())
    digest = hashlib.sha1(f"{check}|{kind}|{where}".encode("utf-8")).hexdigest()[:6]
    return f"{prefix}-{digest}"


def state_dir(root: Path) -> Path:
    return root / "system" / "state"


def ledger_path(root: Path) -> Path:
    return state_dir(root) / "review-ledger.jsonl"


def read_ledger(root: Path) -> list[dict]:
    path = ledger_path(root)
    if not path.exists():
        return []
    entries = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{n}: not valid JSON ({e})")
    return sorted(entries, key=lambda e: e.get("ts", ""))


def append(root: Path, entry: dict) -> dict:
    entry = {"ts": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **entry}
    path = ledger_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def latest_by_ref(entries: list[dict]) -> dict[str, dict]:
    """The most recent decision on each finding (human or auto)."""
    out: dict[str, dict] = {}
    for e in entries:
        out[e["ref"]] = e
    return out


def first_human_by_ref(entries: list[dict]) -> dict[str, dict]:
    """The first human decision on each finding: the one that counts toward agreement."""
    out: dict[str, dict] = {}
    for e in entries:
        if e.get("source", "human") == "human" and e["ref"] not in out:
            out[e["ref"]] = e
    return out


def votes(entries: list[dict]) -> list[dict]:
    """First human decisions, oldest first. Each is one vote on a system recommendation."""
    return sorted(first_human_by_ref(entries).values(), key=lambda e: e.get("ts", ""))


def status_of(latest: dict | None) -> str:
    """Where a finding stands, given its latest decision."""
    if latest is None:
        return "open"
    action = latest["human_action"]
    if action == "accept":
        return "accepted (auto)" if latest.get("source") == "auto" else "accepted"
    if action == "reject":
        return "rejected"
    return "refined"


# --- Reports -------------------------------------------------------------------------------

def reports_dir(root: Path) -> Path:
    return root / "system" / "reports"


def load_report(root: Path, check: str) -> dict | None:
    path = reports_dir(root) / f"{check}.json"
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    for f in report.get("findings", []):
        # Agent-written reports (checks 4-5) may not carry codes; give them the same stable ones.
        f.setdefault("id", finding_ref(check, f.get("kind", ""), f.get("where", "")))
    return report


def load_review(root: Path, check: str) -> dict[str, dict]:
    """The reviewer agent's opinions (Level 1), keyed by finding ref. Empty if it hasn't run."""
    path = reports_dir(root) / f"{check}.review.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {r["id"]: r for r in data.get("reviews", []) if r.get("action") in ACTIONS}


def all_reports(root: Path) -> dict[str, dict]:
    return {c: r for c in CHECKS if (r := load_report(root, c)) is not None}


def find(root: Path, ref: str) -> tuple[str, dict] | None:
    """Locate a finding by its reference code in the current reports."""
    ref = ref.upper()
    for check, report in all_reports(root).items():
        for f in report.get("findings", []) + report.get("suppressed", []):
            if f["id"].upper() == ref:
                return check, f
    return None
