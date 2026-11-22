"""Shared plumbing for Canonical system checks: loading, findings, reports."""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runtime"))
import kb  # noqa: E402  (tools/kb.py)
import autonomy  # noqa: E402  (tools/runtime/autonomy.py)
import ledger  # noqa: E402  (tools/runtime/ledger.py)

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Finding:
    severity: str  # high | medium | low
    kind: str  # short machine-readable category
    where: str  # file path (relative to kb root) or object name
    message: str
    proposed_fix: str = ""
    evidence: list[str] = field(default_factory=list)
    recommended_action: str = ""  # accept | reject | refine (filled from DEFAULT_ACTION if empty)
    confidence: str = ""  # high | medium | low
    id: str = ""  # stable reference code, e.g. SCH-3f2a1b (filled by write_report)
    basis: str = ""  # where the recommendation came from: default | check | calibrated: ...
    status: str = ""  # open | accepted | refined (from the review ledger; rejected ones are hidden)


# What the system recommends the reviewer do, per finding kind, unless a check overrides it.
#   accept: the proposed fix can be applied as written
#   refine: the direction is right but a person must supply something (a description, the right replacement)
#   reject: not used as a default; reserved for checks that detect their own likely false positives
DEFAULT_ACTION = {
    "missing_table": ("accept", "medium"),
    "missing_column": ("accept", "medium"),
    "undocumented_column": ("refine", "high"),
    "no_key_tables": ("refine", "high"),
    "competing_definition": ("refine", "high"),
    "unlinked_mention": ("accept", "high"),
    "missing_canonical": ("refine", "high"),
    "misplaced": ("accept", "medium"),
    "oversized": ("refine", "medium"),
    "dead_end": ("refine", "medium"),
    "too_deep": ("accept", "low"),
    "crowded_folder": ("refine", "low"),
    "near_duplicate": ("accept", "medium"),
}


def load_config(root: Path) -> dict:
    path = root / "system" / "config.json"
    if not path.exists():
        raise SystemExit(f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_docs(root: Path) -> list[kb.Doc]:
    artifacts, skills, errors = kb.load(root)
    if errors:
        raise SystemExit("knowledge base has parse errors; run tools/kb.py check first:\n  " + "\n  ".join(errors))
    return artifacts + skills


def rel(root: Path, doc: kb.Doc) -> str:
    return str(doc.path.relative_to(root))


def full_text(doc: kb.Doc) -> str:
    return doc.path.read_text(encoding="utf-8")


def sentences(text: str) -> list[str]:
    """Split Markdown into rough sentences / table rows / list items."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if s.strip()]
    return out


def write_report(root: Path, check: str, title: str, findings: list[Finding], extra: dict | None = None) -> Path:
    today = dt.date.today().isoformat()
    calibration = autonomy.load_calibration(root)
    latest = ledger.latest_by_ref(ledger.read_ledger(root))
    for f in findings:
        f.id = ledger.finding_ref(check, f.kind, f.where)
        cal = calibration.get(autonomy.key(check, f.kind))
        if f.recommended_action:
            f.basis = "check"  # the check chose this recommendation for this specific finding
        elif cal:
            f.recommended_action, f.confidence, f.basis = cal["recommended_action"], cal["confidence"], cal["basis"]
        else:
            f.recommended_action, f.confidence = DEFAULT_ACTION.get(f.kind, ("refine", "low"))
            f.basis = "default"
        f.confidence = f.confidence or DEFAULT_ACTION.get(f.kind, ("refine", "low"))[1]
        f.status = ledger.status_of(latest.get(f.id))
    # A finding a reviewer rejected stays hidden on later runs, so the check stops repeating it.
    # Delete its ledger lines (or record a new decision) to bring it back.
    suppressed = [f for f in findings if f.status == "rejected"]
    findings = [f for f in findings if f.status != "rejected"]
    findings = sorted(findings, key=lambda f: (SEVERITY_ORDER[f.severity], f.kind, f.where))
    out_dir = root / "system" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / f"{check}"
    counts = {s: sum(f.severity == s for f in findings) for s in SEVERITY_ORDER}

    payload = {"check": check, "date": today, "counts": counts, "findings": [asdict(f) for f in findings],
               "suppressed": [asdict(f) for f in suppressed]}
    if extra:
        payload.update(extra)
    base.with_suffix(".json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# {title}",
        "",
        f"_Run {today} · {counts['high']} high · {counts['medium']} medium · {counts['low']} low._",
        "",
        "> **Human in the loop.** Nothing here has been changed. For each finding: **accept** the "
        "proposed fix, **reject** it (with a reason), or **refine** it (say what to change and the agent re-proposes). "
        "To act, run the `review-kb-checks` skill in your LLM tool and give it a finding's code.",
        "",
    ]
    if not findings:
        lines.append("No findings. ✅")
    for i, f in enumerate(findings, 1):
        lines += [f"### {i}. `{f.id}` [{f.severity}] {f.message}", "", f"- **Where:** `{f.where}`", f"- **Kind:** `{f.kind}`"]
        if f.proposed_fix:
            lines.append(f"- **Proposed fix:** {f.proposed_fix}")
        why = f"; {f.basis}" if f.basis.startswith("calibrated") else ""
        lines.append(f"- **Recommended action:** **{f.recommended_action}** ({f.confidence} confidence{why})")
        if f.status != "open":
            lines.append(f"- **Review status:** {f.status}")
        for e in f.evidence:
            lines.append(f"  - {e}")
        lines.append("")
    if suppressed:
        lines += [f"_{len(suppressed)} finding(s) hidden because a reviewer rejected them earlier: "
                  + ", ".join(f"`{f.id}`" for f in suppressed) + "._", ""]
    base.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{check}: {counts['high']} high · {counts['medium']} medium · {counts['low']} low"
          f"{f' · {len(suppressed)} hidden (rejected before)' if suppressed else ''} → {base.with_suffix('.md').relative_to(root)}")
    return base


def exit_code(findings: list[Finding], strict: bool) -> int:
    return 1 if strict and any(f.severity == "high" for f in findings) else 0
