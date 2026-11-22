"""The autonomy ladder and the learning loop, computed from the review ledger.

Levels (per finding kind, e.g. `schema-integrity/undocumented_column`):

    0  Human in the loop   a person reviews every finding
    1  Agent pre-review    a reviewer agent gives a second opinion; the person still decides
    2  Auto-accept         ("YOLO mode") findings of this kind that pass every gate below are
                           accepted without asking; people spot-check
    3  Self-maintaining    a whole check whose every graduatable kind is at Level 2

A kind becomes ELIGIBLE for Level 2 when, over its most recent `window` votes, humans agreed with
the system's recommendation at least `agreement_threshold` of the time across at least
`min_decisions` votes. Eligible is not the same as ON: the knowledge-base owner switches a kind on
by adding it to `autonomy.auto_accept` in system/config.json. If agreement later falls below the
bar, the kind drops back to Level 1 automatically, even if it was switched on.

Some kinds NEVER graduate, whatever their record: anything that changes what a metric means or
certifies a query. Those always go to the artifact's owner.

The learning loop (`learn`) turns the ledger into two files the next run uses:
  system/state/calibration.json    per kind, the recommendation humans actually make, when it
                                   clearly differs from the built-in default
  system/state/review-lessons.md   the reasons people gave for rejecting or refining, which every
                                   check prompt and the reviewer agent read before reporting
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import ledger

DEFAULTS = {
    "agreement_threshold": 0.90,
    "min_decisions": 20,
    "window": 50,
    "reviewer_agent": [],  # checks where the Level 1 reviewer agent runs
    "auto_accept": [],  # "check/kind" entries the owner has switched on
    "never_auto": [],  # extra kinds to keep human-only (added to the built-in list)
}

# Kinds that change a definition, certify something, or need the team's say. These never graduate.
ALWAYS_HUMAN = {
    "competing_definition",
    "missing_canonical",
    "conflicting_usage",
    "sql_definition_mismatch",
    "contradiction",
    "candidate_canonical_term",
    "definition_change",
    "certification",
    "concept_gap",
    "skill_gap",
    "knowledge_gap",
}
# A proposed fix that mentions any of these is treated as a definition or certification change.
ALWAYS_HUMAN_WORDS = ("certif", "status: reviewed", "redefine", "definition of")

LEVEL_NAMES = {0: "human in the loop", 1: "agent pre-review", 2: "auto-accept", 3: "self-maintaining"}


def settings(root: Path) -> dict:
    cfg_path = root / "system" / "config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    s = {**DEFAULTS, **cfg.get("autonomy", {})}
    s["never_auto"] = sorted(ALWAYS_HUMAN | set(s["never_auto"]))
    return s


def key(check: str, kind: str) -> str:
    return f"{check}/{kind}"


# --- Agreement ------------------------------------------------------------------------------

def kind_records(entries: list[dict], s: dict) -> dict[str, dict]:
    """Per finding kind: votes, agreement over the rolling window, and what humans chose."""
    by_kind: dict[str, list[dict]] = defaultdict(list)
    for v in ledger.votes(entries):
        by_kind[key(v["check"], v["kind"])].append(v)
    out = {}
    for k, vs in by_kind.items():
        recent = vs[-s["window"]:]
        agree = sum(v["recommended_action"] == v["human_action"] for v in recent)
        reviewed = [v for v in recent if v.get("reviewer_agent_action") in ledger.ACTIONS]
        out[k] = {
            "votes_total": len(vs),
            "votes": len(recent),
            "agree": agree,
            "agreement": agree / len(recent) if recent else None,
            "human_actions": Counter(v["human_action"] for v in recent),
            "pairs": Counter((v["recommended_action"], v["human_action"]) for v in recent),
            "reviewer_votes": len(reviewed),
            "reviewer_agree": sum(v["reviewer_agent_action"] == v["human_action"] for v in reviewed),
        }
    return out


def levels(root: Path, entries: list[dict] | None = None) -> list[dict]:
    """One row per finding kind seen in the ledger or in the current reports."""
    s = settings(root)
    entries = ledger.read_ledger(root) if entries is None else entries
    records = kind_records(entries, s)
    keys = set(records)
    for check, report in ledger.all_reports(root).items():
        keys |= {key(check, f["kind"]) for f in report.get("findings", [])}

    rows = []
    for k in sorted(keys):
        check, kind = k.split("/", 1)
        r = records.get(k, {"votes": 0, "votes_total": 0, "agree": 0, "agreement": None,
                            "human_actions": Counter(), "pairs": Counter(),
                            "reviewer_votes": 0, "reviewer_agree": 0})
        never = kind in s["never_auto"]
        recs = Counter(rec for rec, _ in r["pairs"].elements())
        mostly_accept = bool(recs) and recs["accept"] / sum(recs.values()) >= 0.5
        meets_bar = (r["votes"] >= s["min_decisions"] and r["agreement"] is not None
                     and r["agreement"] >= s["agreement_threshold"])
        # Only an "accept" recommendation can be applied without a person. A kind whose findings are
        # usually "refine" (a person must supply something) can be trusted, but not automated.
        eligible = not never and meets_bar and mostly_accept
        enabled = k in s["auto_accept"]
        reviewer_on = check in s["reviewer_agent"]
        level = 0
        if reviewer_on:
            level = 2 if (eligible and enabled) else 1

        if never:
            note = "never graduates (changes a definition or certification, or needs the team's say)"
        elif eligible and enabled and not reviewer_on:
            note = f"switched on, but the reviewer agent is off for {check}; auto-accept needs both opinions"
        elif eligible and enabled:
            note = "auto-accept ON"
        elif eligible:
            note = "ELIGIBLE for auto-accept: add it to autonomy.auto_accept to switch it on"
        elif meets_bar and not mostly_accept:
            note = "humans agree, but its fixes need a person to supply something (refine), so it can't auto-accept"
        elif enabled:
            note = f"auto-accept PAUSED: agreement below {s['agreement_threshold']:.0%}, back to human review"
        elif r["votes"] < s["min_decisions"]:
            note = f"needs {s['min_decisions'] - r['votes']} more decisions"
        else:
            note = f"agreement below {s['agreement_threshold']:.0%}"
        rows.append({"key": k, "check": check, "kind": kind, **r, "never": never, "eligible": eligible,
                     "enabled": enabled, "reviewer_on": reviewer_on, "level": level, "note": note})
    return rows


def check_levels(rows: list[dict]) -> dict[str, int]:
    """A check is Level 3 when every kind that can graduate is auto-accepting."""
    out: dict[str, int] = {}
    for check in sorted({r["check"] for r in rows}):
        mine = [r for r in rows if r["check"] == check]
        graduatable = [r for r in mine if not r["never"]]
        lvl = max(r["level"] for r in mine)
        if graduatable and all(r["level"] == 2 for r in graduatable):
            lvl = 3
        out[check] = lvl
    return out


# --- Per-finding gate for Level 2 -----------------------------------------------------------

def auto_accept_gate(finding: dict, row: dict | None, review: dict | None) -> tuple[bool, str]:
    """Would this finding be accepted without a human? Returns (yes/no, why)."""
    if row is None or row["level"] < 2:
        return False, "kind not at Level 2"
    if finding.get("recommended_action") != "accept":
        return False, "the system did not recommend accept"
    if finding.get("confidence") != "high":
        return False, "confidence is not high"
    if finding.get("severity") == "high" and finding.get("confidence") == "low":
        return False, "high severity with low confidence always goes to the owner"
    fix = (finding.get("proposed_fix") or "").lower()
    if any(w in fix for w in ALWAYS_HUMAN_WORDS):
        return False, "the fix touches a definition or certification"
    if not review:
        return False, "no reviewer-agent opinion yet"
    if review.get("action") != "accept":
        return False, f"the reviewer agent said {review.get('action')}"
    return True, "both agents recommend accept, high confidence, kind at Level 2"


# --- Learning loop --------------------------------------------------------------------------

def calibrate(root: Path, entries: list[dict], defaults: dict[str, tuple[str, str]]) -> dict:
    """When humans clearly and repeatedly choose a different action, recommend that instead.

    `defaults` is the built-in recommendation per kind (tools/checks/common.py → DEFAULT_ACTION).
    Comparing against the built-in default, not last week's recommendation, keeps a calibration
    in place once humans start agreeing with it.
    """
    s = settings(root)
    out = {}
    for k, r in kind_records(entries, s).items():
        if r["votes"] < max(5, s["min_decisions"] // 2):
            continue
        kind = k.split("/", 1)[1]
        recommended = defaults.get(kind, (None,))[0] or \
            Counter(rec for rec, _ in r["pairs"].elements()).most_common(1)[0][0]
        top, n = r["human_actions"].most_common(1)[0]
        share = n / r["votes"]
        if top != recommended and share >= 0.6:
            out[k] = {
                "recommended_action": top,
                "confidence": "high" if share >= 0.8 else "medium",
                "basis": f"calibrated: humans chose {top} on {n} of the last {r['votes']} {k.split('/')[1]} findings",
            }
    return out


def lessons_markdown(entries: list[dict], per_kind: int = 8) -> str:
    """What reviewers said when they rejected or refined, grouped by kind. Agents read this."""
    notes: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        if e.get("source", "human") != "human" or e["human_action"] == "accept":
            continue
        text = (e.get("refinement") or e.get("reason") or "").strip()
        if text:
            notes[key(e["check"], e["kind"])].append(e)
    lines = [
        "# Review lessons",
        "",
        "_Generated by `tools/runtime/cli.py learn` from `review-ledger.jsonl`. Do not edit by hand._",
        "",
        "What reviewers said when they **rejected** or **refined** a finding. Every check prompt and the "
        "reviewer agent read this before reporting: don't raise a finding a reviewer already rejected for a "
        "reason that still applies, and shape proposals the way reviewers keep refining them.",
        "",
    ]
    if not notes:
        lines.append("No rejections or refinements recorded yet.")
    for k in sorted(notes):
        es = notes[k]
        lines += [f"## `{k}` ({len(es)} rejected or refined)", ""]
        for e in es[-per_kind:]:
            text = (e.get("refinement") or e.get("reason")).replace("\n", " ")
            lines.append(f"- **{e['human_action']}** `{e['ref']}` ({e['ts'][:10]}): {text}")
        lines.append("")
    return "\n".join(lines) + "\n"


def learn(root: Path, defaults: dict[str, tuple[str, str]]) -> tuple[Path, Path, dict]:
    entries = ledger.read_ledger(root)
    cal = calibrate(root, entries, defaults)
    sd = ledger.state_dir(root)
    sd.mkdir(parents=True, exist_ok=True)
    cal_path = sd / "calibration.json"
    cal_path.write_text(json.dumps(cal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lessons_path = sd / "review-lessons.md"
    lessons_path.write_text(lessons_markdown(entries), encoding="utf-8")
    return cal_path, lessons_path, cal


def load_calibration(root: Path) -> dict:
    path = ledger.state_dir(root) / "calibration.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
