"""Shared plumbing for Groundtruth system checks: loading, findings, reports."""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kb  # noqa: E402  (tools/kb.py)

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Finding:
    severity: str  # high | medium | low
    kind: str  # short machine-readable category
    where: str  # file path (relative to kb root) or object name
    message: str
    proposed_fix: str = ""
    evidence: list[str] = field(default_factory=list)


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
    findings = sorted(findings, key=lambda f: (SEVERITY_ORDER[f.severity], f.kind, f.where))
    out_dir = root / "system" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / f"{check}"
    counts = {s: sum(f.severity == s for f in findings) for s in SEVERITY_ORDER}

    payload = {"check": check, "date": today, "counts": counts, "findings": [asdict(f) for f in findings]}
    if extra:
        payload.update(extra)
    base.with_suffix(".json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# {title}",
        "",
        f"_Run {today} · {counts['high']} high · {counts['medium']} medium · {counts['low']} low._",
        "",
        "> **Human in the loop.** Nothing here has been changed. Review each finding, then accept "
        "the proposed fix (in a pull request), reject it, or mark it as expected.",
        "",
    ]
    if not findings:
        lines.append("No findings. ✅")
    for i, f in enumerate(findings, 1):
        lines += [f"### {i}. [{f.severity}] {f.message}", "", f"- **Where:** `{f.where}`", f"- **Kind:** `{f.kind}`"]
        if f.proposed_fix:
            lines.append(f"- **Proposed fix:** {f.proposed_fix}")
        for e in f.evidence:
            lines.append(f"  - {e}")
        lines.append("")
    base.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{check}: {counts['high']} high · {counts['medium']} medium · {counts['low']} low → {base.with_suffix('.md').relative_to(root)}")
    return base


def exit_code(findings: list[Finding], strict: bool) -> int:
    return 1 if strict and any(f.severity == "high" for f in findings) else 0
