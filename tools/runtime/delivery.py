"""Delivery: one short summary per check, posted where everyone can see it.

The summary is a notice board, not a review tool. It shows counts by severity, the top findings
with their reference codes, and a link to the full report. Reviewers act later by running the
`review-kb-checks` skill in their own LLM tool and giving it a code.

Adapters (pick with --to, or CANONICAL_DELIVERY):
    stdout   print the message (the default, and what every dry run does)
    slack    POST to a Slack incoming webhook (https://api.slack.com/messaging/webhooks)

Adding a destination (Microsoft Teams, Discord, email, a GitHub issue) means adding one function
that takes the rendered message and sends it. The checks don't change.

Safety: a message is only sent when BOTH are true:
    1. the command was run with --send, and
    2. the webhook URL is in the environment variable CANONICAL_SLACK_WEBHOOK_URL.
Otherwise it is printed and nothing leaves the machine.
"""
from __future__ import annotations

import json
import os
import urllib.request

import autonomy
import ledger

SEVERITY_ICON = {"high": "🔴", "medium": "🟠", "low": "⚪"}
CHECK_TITLE = {
    "schema-integrity": "Schema integrity",
    "semantic-integrity": "Semantic integrity",
    "cohesion-redundancy": "Cohesion & redundancy",
    "proactive-enrichment": "Proactive enrichment",
    "analytical-gaps": "Analytical gaps",
}
WEBHOOK_ENV = "CANONICAL_SLACK_WEBHOOK_URL"


def _short(text: str, n: int = 140) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1] + "…"


def report_link(check: str) -> str:
    """Where the full report can be read.

    CANONICAL_REPORT_URL_BASE  e.g. https://github.com/acme/kb/blob/main  (reports are committed)
    CANONICAL_RUN_URL          e.g. the CI run page, where reports are attached as an artifact
    """
    path = f"system/reports/{check}.md"
    base = os.environ.get("CANONICAL_REPORT_URL_BASE", "").rstrip("/")
    if base:
        return f"<{base}/{path}|{path}>"
    run = os.environ.get("CANONICAL_RUN_URL", "")
    if run:
        return f"<{run}|this run's reports> (`{path}`)"
    return f"`{path}`"


def render(root, check: str, top: int = 5) -> str | None:
    """The summary text for one check (Slack mrkdwn), or None if the check hasn't run."""
    report = ledger.load_report(root, check)
    if report is None:
        return None
    findings = report.get("findings", [])
    hidden = len(report.get("suppressed", []))
    reviews = ledger.load_review(root, check)
    latest = ledger.latest_by_ref(ledger.read_ledger(root))
    rows = {r["key"]: r for r in autonomy.levels(root)}
    c = report.get("counts", {})

    open_ = [f for f in findings if ledger.status_of(latest.get(f["id"])) == "open"]
    auto = [f for f in open_ if autonomy.auto_accept_gate(
        f, rows.get(autonomy.key(check, f["kind"])), reviews.get(f["id"]))[0]]

    lines = [
        f"*Knowledge-base check · {CHECK_TITLE.get(check, check)}* · {report.get('date', '')}",
        " · ".join(f"{SEVERITY_ICON[s]} {c.get(s, 0)} {s}" for s in ("high", "medium", "low"))
        + f"   ({len(open_) - len(auto)} awaiting review"
        + (f", {len(auto)} auto-accepted" if auto else "")
        + (f", {hidden} hidden as previously rejected" if hidden else "")
        + ")",
    ]
    if not findings:
        lines.append("No findings. ✅")
    for f in findings[:top]:
        rec = f"→ *{f['recommended_action']}* ({f['confidence']})"
        if f["id"] in reviews:
            rec += f" · reviewer agent: {reviews[f['id']]['action']}"
        status = ledger.status_of(latest.get(f["id"]))
        if f in auto:
            status = "auto-accepted"
        tag = "" if status == "open" else f" _[{status}]_"
        lines.append(f"• `{f['id']}` {SEVERITY_ICON[f['severity']]} {_short(f['message'])} {rec}{tag}")
    if len(findings) > top:
        lines.append(f"_…and {len(findings) - top} more in the full report._")
    lines += [
        f"Full report: {report_link(check)}",
        "To act on a finding, run the `review-kb-checks` skill in your LLM tool and give it the code"
        " (or say \"all open\").",
    ]
    return "\n".join(lines)


def send_stdout(text: str) -> None:
    print(text)
    print()


def send_slack(text: str, webhook: str) -> None:
    body = json.dumps({"text": text, "unfurl_links": False}).encode("utf-8")
    req = urllib.request.Request(webhook, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        if resp.status >= 300:
            raise SystemExit(f"Slack webhook returned HTTP {resp.status}")


def deliver(root, checks: list[str], to: str = "stdout", send: bool = False) -> int:
    webhook = os.environ.get(WEBHOOK_ENV, "")
    live = send and to == "slack" and bool(webhook)
    if to == "slack" and not live:
        why = "no --send flag" if not send else f"{WEBHOOK_ENV} is not set"
        print(f"[dry run: {why}; printing instead of posting to Slack]\n")
    sent = 0
    for check in checks:
        text = render(root, check)
        if text is None:
            continue
        if live:
            send_slack(text, webhook)
            print(f"posted {check} summary to Slack")
        else:
            send_stdout(text)
        sent += 1
    if sent == 0:
        print("no reports found in system/reports/; run the checks first")
    return 0
