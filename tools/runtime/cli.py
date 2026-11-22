#!/usr/bin/env python3
"""Canonical runtime: deliver reports, record reviews, and track the autonomy ladder.

Usage (run from anywhere; <kb> is the knowledge-base root, e.g. examples/lumen):

  Delivery
    cli.py notify   <kb> [--check C ...] [--to stdout|slack] [--send]
                    One summary per check. Prints unless --send AND CANONICAL_SLACK_WEBHOOK_URL is set.

  Review (what the review-kb-checks skill calls)
    cli.py findings <kb> [--check C] [--all] [--json]   open findings with their reference codes
    cli.py show     <kb> <REF> [--json]                 one finding in full, with its history
    cli.py record   <kb> <REF> accept|reject|refine --by NAME
                    [--reason TEXT] [--refinement TEXT] [--pr URL] [--minutes N] [--source human|auto]

  Learning loop
    cli.py stats    <kb> [--json]          agreement between recommendation and human, per check and kind
    cli.py autonomy <kb> [--write]         autonomy level per kind; which open findings would auto-accept
    cli.py learn    <kb>                   write calibration.json and review-lessons.md from the ledger

  Reviewer agent (Level 1)
    cli.py reviewer-prompt <kb> <check>    print the reviewer agent's full prompt (pipe it to any LLM)
    cli.py ingest-review   <kb> <check>    read the agent's reply on stdin; save <check>.review.json

Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "checks"))

import autonomy  # noqa: E402
import delivery  # noqa: E402
import ledger  # noqa: E402
from common import DEFAULT_ACTION  # noqa: E402


def pct(x: float | None) -> str:
    return "—" if x is None else f"{x:.0%}"


# --- Delivery -------------------------------------------------------------------------------

def cmd_notify(a) -> int:
    import os
    to = a.to or os.environ.get("CANONICAL_DELIVERY", "stdout")
    return delivery.deliver(a.kb, a.check or ledger.CHECKS, to=to, send=a.send)


# --- Review ---------------------------------------------------------------------------------

def _open_findings(root: Path, check: str | None, include_all: bool) -> list[dict]:
    latest = ledger.latest_by_ref(ledger.read_ledger(root))
    rows = {r["key"]: r for r in autonomy.levels(root)}
    out = []
    for c, report in ledger.all_reports(root).items():
        if check and c != check:
            continue
        reviews = ledger.load_review(root, c)
        for f in report.get("findings", []):
            status = ledger.status_of(latest.get(f["id"]))
            if status != "open" and not include_all:
                continue
            ok, why = autonomy.auto_accept_gate(f, rows.get(autonomy.key(c, f["kind"])), reviews.get(f["id"]))
            out.append({**f, "check": c, "status": status, "reviewer_agent": reviews.get(f["id"]),
                        "auto_accept": ok, "auto_accept_why": why})
    return out


def cmd_findings(a) -> int:
    items = _open_findings(a.kb, a.check, a.all)
    if a.json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return 0
    if not items:
        print("Nothing awaiting review. 🎉")
        return 0
    auto = [f for f in items if f["auto_accept"]]
    if auto:
        print(f"Auto-accepted (Level 2): {len(auto)}. Apply these without discussion unless the owner objects.")
        for f in auto:
            print(f"  {f['id']}  [{f['severity']}] {f['message']}")
        print()
    print(f"{'REF':<11} {'SEV':<7} {'REC':<14} {'STATUS':<9} MESSAGE")
    for f in items:
        if f["auto_accept"]:
            continue
        rec = f"{f['recommended_action']}/{f['confidence'][0]}"
        if f["reviewer_agent"]:
            rec += f" ra:{f['reviewer_agent']['action'][:3]}"
        print(f"{f['id']:<11} {f['severity']:<7} {rec:<14} {f['status']:<9} {delivery._short(f['message'], 90)}")
    print("\nrec = recommended action / confidence (h, m, l); ra = reviewer agent's opinion")
    return 0


def cmd_show(a) -> int:
    hit = ledger.find(a.kb, a.ref)
    if not hit:
        raise SystemExit(f"{a.ref}: not in the current reports. Run `findings --all` to list codes.")
    check, f = hit
    history = [e for e in ledger.read_ledger(a.kb) if e["ref"] == f["id"]]
    review = ledger.load_review(a.kb, check).get(f["id"])
    rows = {r["key"]: r for r in autonomy.levels(a.kb)}
    row = rows.get(autonomy.key(check, f["kind"]))
    ok, why = autonomy.auto_accept_gate(f, row, review)
    if a.json:
        print(json.dumps({**f, "check": check, "reviewer_agent": review, "history": history,
                          "autonomy": row and {k: row[k] for k in ("level", "votes", "agreement", "note")},
                          "auto_accept": ok, "auto_accept_why": why}, indent=2, ensure_ascii=False, default=str))
        return 0
    print(f"{f['id']}  ·  {check}  ·  {f['kind']}  ·  {f['severity']} severity")
    print(f"\n{f['message']}\n")
    print(f"Where:         {f['where']}")
    print(f"Proposed fix:  {f.get('proposed_fix') or '(none)'}")
    basis = f.get("basis", "")
    print(f"Recommended:   {f['recommended_action']} ({f['confidence']} confidence"
          f"{'; ' + basis if basis.startswith('calibrated') else ''})")
    if review:
        print(f"Reviewer agent: {review['action']} ({review.get('confidence', '?')}): {review.get('reason', '')}")
    for e in f.get("evidence", []):
        print(f"  evidence: {e}")
    if row:
        print(f"\nThis kind: level {row['level']} ({autonomy.LEVEL_NAMES[row['level']]}), "
              f"{row['votes']} votes, {pct(row['agreement'])} agreement. {row['note']}")
    print(f"Auto-accept:   {'yes' if ok else 'no'} ({why})")
    print(f"Status:        {ledger.status_of(history[-1] if history else None)}")
    for e in history:
        extra = e.get("refinement") or e.get("reason") or ""
        print(f"  {e['ts']}  {e['human_action']:<7} by {e.get('decided_by', '?')} ({e.get('source', 'human')})"
              f"{': ' + extra if extra else ''}{'  ' + e['pr'] if e.get('pr') else ''}")
    return 0


def cmd_record(a) -> int:
    hit = ledger.find(a.kb, a.ref)
    if not hit:
        raise SystemExit(f"{a.ref}: not in the current reports. Run `findings --all` to list codes.")
    check, f = hit
    if a.action == "reject" and not a.reason:
        raise SystemExit("reject needs --reason (one line is enough). It's how the check learns what isn't a problem.")
    if a.action == "refine" and not (a.refinement or a.reason):
        raise SystemExit("refine needs --refinement: what should change about the proposed fix.")
    review = ledger.load_review(a.kb, check).get(f["id"])
    entry = ledger.append(a.kb, {
        "ref": f["id"], "check": check, "kind": f["kind"], "where": f["where"], "severity": f["severity"],
        "recommended_action": f["recommended_action"], "confidence": f["confidence"],
        "reviewer_agent_action": review["action"] if review else None,
        "human_action": a.action, "decided_by": a.by, "source": a.source,
        "reason": a.reason or "", "refinement": a.refinement or "", "pr": a.pr or "",
        "minutes": a.minutes,
    })
    agreed = "agrees with" if entry["human_action"] == entry["recommended_action"] else "differs from"
    print(f"recorded: {entry['ref']} {entry['human_action']} by {entry['decided_by']} "
          f"({agreed} the recommendation: {entry['recommended_action']})")
    return 0


# --- Learning loop --------------------------------------------------------------------------

def cmd_stats(a) -> int:
    root = a.kb
    entries = ledger.read_ledger(root)
    s = autonomy.settings(root)
    rows = [r for r in autonomy.levels(root, entries) if r["votes_total"]]
    if a.json:
        print(json.dumps([{k: (dict(v) if hasattr(v, "items") else v) for k, v in r.items() if k != "pairs"}
                          for r in rows], indent=2, default=str))
        return 0
    votes = ledger.votes(entries)
    simulated = sum(bool(e.get("simulated")) for e in entries)
    print(f"Review ledger: {len(entries)} decisions, {len(votes)} first-time human reviews"
          + (f" ({simulated} simulated, from the example)" if simulated else ""))
    print(f"Graduation bar: ≥ {s['agreement_threshold']:.0%} agreement over ≥ {s['min_decisions']} reviews "
          f"(last {s['window']} per kind)\n")
    if not rows:
        print("No decisions yet. Record one with `record`.")
        return 0
    print(f"{'CHECK / KIND':<46} {'VOTES':>5} {'AGREE':>6}  {'ACC':>3} {'REJ':>3} {'REF':>3}  LVL  NOTE")
    for r in rows:
        h = r["human_actions"]
        print(f"{r['key']:<46} {r['votes']:>5} {pct(r['agreement']):>6}  {h['accept']:>3} {h['reject']:>3} "
              f"{h['refine']:>3}  {r['level']:>3}  {r['note']}")
    print()
    by_check: dict[str, list[dict]] = {}
    for v in votes:
        by_check.setdefault(v["check"], []).append(v)
    for check, vs in sorted(by_check.items()):
        agree = sum(v["recommended_action"] == v["human_action"] for v in vs)
        print(f"{check:<46} {len(vs):>5} {pct(agree / len(vs)):>6}   (all kinds)")
    total = sum(v["recommended_action"] == v["human_action"] for v in votes)
    print(f"{'overall':<46} {len(votes):>5} {pct(total / len(votes)):>6}")
    rv = [v for v in votes if v.get("reviewer_agent_action") in ledger.ACTIONS]
    if rv:
        ra = sum(v["reviewer_agent_action"] == v["human_action"] for v in rv)
        print(f"{'reviewer agent vs. human':<46} {len(rv):>5} {pct(ra / len(rv)):>6}")
    mins = [v["minutes"] for v in votes if isinstance(v.get("minutes"), (int, float))]
    if mins:
        print(f"\nMedian review time: {sorted(mins)[len(mins) // 2]} min per finding")
    return 0


def cmd_autonomy(a) -> int:
    root = a.kb
    rows = autonomy.levels(root)
    levels = autonomy.check_levels(rows)
    print("Autonomy level per check (0 human · 1 agent pre-review · 2 auto-accept · 3 self-maintaining)")
    for check, lvl in levels.items():
        print(f"  {check:<24} level {lvl}: {autonomy.LEVEL_NAMES[lvl]}")
    print("\nPer kind:")
    for r in rows:
        print(f"  L{r['level']}  {r['key']:<46} {r['votes']:>3} votes {pct(r['agreement']):>5}  {r['note']}")
    auto = [f for f in _open_findings(root, None, False) if f["auto_accept"]]
    print(f"\nOpen findings that would auto-accept now: {len(auto)}")
    for f in auto:
        print(f"  {f['id']}  {f['message']}")

    if a.write:
        path = ledger.state_dir(root) / "autonomy.json"
        before = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        now = {r["key"]: {"level": r["level"], "eligible": r["eligible"], "agreement": r["agreement"],
                          "votes": r["votes"]} for r in rows}
        for k, v in now.items():
            old = before.get(k, {})
            if old and old.get("level") != v["level"]:
                print(f"  CHANGE: {k} level {old.get('level')} → {v['level']}")
            elif old and not old.get("eligible") and v["eligible"]:
                print(f"  NEW: {k} is now eligible for auto-accept")
        path.write_text(json.dumps(now, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"\nwrote {path.relative_to(root)}")
    return 0


def cmd_learn(a) -> int:
    cal_path, lessons_path, cal = autonomy.learn(a.kb, DEFAULT_ACTION)
    print(f"wrote {cal_path.relative_to(a.kb)} ({len(cal)} calibrated kinds)")
    for k, v in sorted(cal.items()):
        print(f"  {k}: now recommends {v['recommended_action']} ({v['confidence']}): {v['basis']}")
    print(f"wrote {lessons_path.relative_to(a.kb)}")
    print("The next run of each check uses both. Re-run the checks to see updated recommendations.")
    return 0


# --- Reviewer agent -------------------------------------------------------------------------

def cmd_reviewer_prompt(a) -> int:
    root = a.kb
    report = ledger.load_report(root, a.check)
    if report is None:
        raise SystemExit(f"no report for {a.check}; run the check first")
    prompt = (root / "system" / "prompts" / "reviewer.md").read_text(encoding="utf-8")
    lessons_path = ledger.state_dir(root) / "review-lessons.md"
    lessons = lessons_path.read_text(encoding="utf-8") if lessons_path.exists() else "(none yet)"
    # Independence: the reviewer must not see the system's own recommendation.
    hidden = {"recommended_action", "confidence", "basis", "status"}
    findings = [{k: v for k, v in f.items() if k not in hidden} for f in report.get("findings", [])]
    print(prompt.rstrip())
    print("\n---\n\n## Review lessons (from the ledger)\n")
    print(lessons.rstrip())
    print(f"\n---\n\n## Findings to review: {a.check}, {report.get('date', '')}\n")
    print("```json")
    print(json.dumps(findings, indent=2, ensure_ascii=False))
    print("```")
    return 0


def cmd_ingest_review(a) -> int:
    text = sys.stdin.read()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise SystemExit("no JSON object in the reviewer agent's reply; nothing saved")
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        raise SystemExit(f"reviewer agent's reply isn't valid JSON ({e}); nothing saved")
    report = ledger.load_report(a.kb, a.check) or {"findings": []}
    known = {f["id"] for f in report["findings"]}
    reviews = [r for r in data.get("reviews", []) if r.get("id") in known and r.get("action") in ledger.ACTIONS]
    dropped = len(data.get("reviews", [])) - len(reviews)
    out = {"check": a.check, "date": dt.date.today().isoformat(), "reviews": reviews}
    path = ledger.reports_dir(a.kb) / f"{a.check}.review.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"saved {len(reviews)} reviewer-agent opinions to {path.relative_to(a.kb)}"
          + (f" (ignored {dropped} with unknown codes or actions)" if dropped else ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_):
        p = sub.add_parser(name, help=help_)
        p.add_argument("kb", type=Path)
        p.set_defaults(fn=fn)
        return p

    p = add("notify", cmd_notify, "post (or print) one summary per check")
    p.add_argument("--check", action="append", choices=ledger.CHECKS)
    p.add_argument("--to", choices=["stdout", "slack"])
    p.add_argument("--send", action="store_true", help="actually post (also needs the webhook env var)")

    p = add("findings", cmd_findings, "list findings awaiting review")
    p.add_argument("--check", choices=ledger.CHECKS)
    p.add_argument("--all", action="store_true", help="include already-decided findings")
    p.add_argument("--json", action="store_true")

    p = add("show", cmd_show, "one finding in full")
    p.add_argument("ref")
    p.add_argument("--json", action="store_true")

    p = add("record", cmd_record, "record a decision in the review ledger")
    p.add_argument("ref")
    p.add_argument("action", choices=ledger.ACTIONS)
    p.add_argument("--by", required=True, help="who decided")
    p.add_argument("--reason")
    p.add_argument("--refinement")
    p.add_argument("--pr")
    p.add_argument("--minutes", type=float)
    p.add_argument("--source", choices=["human", "auto"], default="human")

    p = add("stats", cmd_stats, "agreement rates from the review ledger")
    p.add_argument("--json", action="store_true")

    p = add("autonomy", cmd_autonomy, "autonomy level per finding kind")
    p.add_argument("--write", action="store_true", help="save system/state/autonomy.json and report changes")

    add("learn", cmd_learn, "update calibration.json and review-lessons.md")

    p = add("reviewer-prompt", cmd_reviewer_prompt, "print the reviewer agent's prompt")
    p.add_argument("check", choices=ledger.CHECKS)
    p = add("ingest-review", cmd_ingest_review, "save the reviewer agent's reply (stdin)")
    p.add_argument("check", choices=ledger.CHECKS)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
