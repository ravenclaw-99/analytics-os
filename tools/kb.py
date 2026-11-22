#!/usr/bin/env python3
"""Canonical tool: validate and index a knowledge base.

Usage:
    python3 tools/kb.py check <kb_root> [--today YYYY-MM-DD]
    python3 tools/kb.py index <kb_root>

<kb_root> contains the three top-level folders:
    analytics-reference/   artifacts (any depth)
    execution/tooling/     tooling artifacts
    execution/skills/      skills (SKILL.md); their [[links]] are checked
    system/                not parsed

Standard library only. Frontmatter uses a deliberately small YAML subset:
`key: value` scalars and inline lists `key: [a, b, c]`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

# Lower rank = more fundamental. An artifact may only depend on equal or lower rank.
RANK = {
    "source": 0,
    "register": 0,
    "tooling": 0,
    "entity": 1,
    "query": 2,
    "metric": 3,
    "model": 4,
    "framework": 4,
    "analysis": 5,
    "decision": 6,
}
ARTIFACT_DIRS = ["analytics-reference", "execution/tooling"]
SKILLS_DIR = "execution/skills"
COMMON_REQUIRED = ["id", "type", "title", "owner", "status", "updated"]
TYPE_REQUIRED = {
    "source": ["system"],
    "register": ["system"],
    "tooling": ["system"],
    "entity": ["grain", "primary_key"],
    "query": ["certified_by", "certified_on", "warehouse_object"],
    "metric": ["unit", "grain"],
    "model": ["kind"],
    "framework": [],
    "analysis": ["question", "confidence"],
    "decision": ["decided_on", "review_on", "outcome"],
}
ENUMS = {
    "status": {"draft", "reviewed", "deprecated"},
    "confidence": {"low", "medium", "high"},
    "outcome": {"pending", "worked", "mixed", "failed", "unclear"},
}
WIKI_LINK = re.compile(r"\[\[([a-z]+\.[a-z0-9\-]+)\]\]")
STALE_DRAFT_DAYS = 30


class Doc:
    def __init__(self, path: Path, meta: dict, body: str, skill: bool = False):
        self.path = path
        self.meta = meta
        self.body = body
        self.skill = skill

    @property
    def id(self) -> str:
        if self.skill:
            return f"skill.{self.meta.get('name', self.path.parent.name)}"
        return self.meta.get("id", "")

    @property
    def type(self) -> str:
        return "skill" if self.skill else self.meta.get("type", "")

    def list_field(self, key: str) -> list[str]:
        value = self.meta.get(key, [])
        return value if isinstance(value, list) else [value] if value else []

    def wiki_links(self) -> list[str]:
        return sorted(set(WIKI_LINK.findall(self.body)))


def parse_value(raw: str):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [item.strip() for item in inner.split(",") if item.strip()] if inner else []
    return raw


def parse_file(path: Path, skill: bool = False) -> Doc | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None  # plain Markdown (READMEs etc.) is not an artifact
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    meta: dict = {}
    for lineno, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"line {lineno}: expected 'key: value'")
        key, _, value = line.partition(":")
        meta[key.strip()] = parse_value(value)
    return Doc(path, meta, text[end + 4 :], skill=skill)


def load(root: Path) -> tuple[list[Doc], list[Doc], list[str]]:
    artifacts, skills, errors = [], [], []
    for d in ARTIFACT_DIRS:
        for path in sorted((root / d).rglob("*.md")):
            try:
                doc = parse_file(path)
            except ValueError as exc:
                errors.append(f"{path.relative_to(root)}: {exc}")
                continue
            if doc:
                artifacts.append(doc)
    for path in sorted((root / SKILLS_DIR).glob("*/SKILL.md")):
        try:
            doc = parse_file(path, skill=True)
        except ValueError as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        if not doc or not doc.meta.get("name") or not doc.meta.get("description"):
            errors.append(f"{path.relative_to(root)}: skill needs 'name' and 'description' frontmatter")
            continue
        skills.append(doc)
    return artifacts, skills, errors


def parse_date(value) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def check(root: Path, today: dt.date) -> tuple[list[str], list[str], int]:
    artifacts, skills, errors = load(root)
    warnings: list[str] = []
    by_id: dict[str, Doc] = {}
    rel = lambda d: d.path.relative_to(root)  # noqa: E731

    for a in artifacts:
        if a.type not in RANK:
            errors.append(f"{rel(a)}: unknown type '{a.type}' (expected one of {sorted(RANK)})")
        for key in COMMON_REQUIRED + TYPE_REQUIRED.get(a.type, []):
            if not a.meta.get(key):
                errors.append(f"{rel(a)}: missing required field '{key}'")
        if a.id and a.type and not a.id.startswith(f"{a.type}."):
            errors.append(f"{rel(a)}: id '{a.id}' must start with '{a.type}.'")
        for key, allowed in ENUMS.items():
            if a.meta.get(key) and a.meta[key] not in allowed:
                errors.append(f"{rel(a)}: {key} '{a.meta[key]}' not in {sorted(allowed)}")
        if a.id in by_id:
            errors.append(f"{rel(a)}: duplicate id '{a.id}' (also in {rel(by_id[a.id])})")
        elif a.id:
            by_id[a.id] = a

    inbound: dict[str, int] = {i: 0 for i in by_id}
    for a in artifacts + skills:
        for dep in a.list_field("depends_on"):
            target = by_id.get(dep)
            if not target:
                errors.append(f"{rel(a)}: depends_on '{dep}' does not exist")
                continue
            inbound[dep] += 1
            if a.type in RANK and target.type in RANK and RANK[target.type] > RANK[a.type]:
                errors.append(f"{rel(a)}: {a.type} cannot depend on higher-level {target.type} '{dep}'")
        for link in a.wiki_links():
            if link not in by_id:
                errors.append(f"{rel(a)}: broken link [[{link}]]")
            elif link != a.id:
                inbound[link] += 1
        reviews = a.meta.get("reviews")
        if reviews:
            target = by_id.get(reviews)
            if not target or target.type != "decision":
                errors.append(f"{rel(a)}: reviews '{reviews}' is not an existing decision")
            else:
                inbound[reviews] += 1

    reviewed = {a.meta.get("reviews") for a in artifacts if a.meta.get("reviews")}
    for a in artifacts:
        if a.meta.get("owner") == "unowned":
            warnings.append(f"{rel(a)}: no owner (owner: unowned)")
        updated = parse_date(a.meta.get("updated"))
        if a.meta.get("status") == "draft" and updated and (today - updated).days > STALE_DRAFT_DAYS:
            warnings.append(f"{rel(a)}: draft for {(today - updated).days} days; review or delete it")
        if a.type == "query":
            certified = parse_date(a.meta.get("certified_on"))
            if certified and updated and updated > certified:
                warnings.append(f"{rel(a)}: changed after certification ({certified}); re-certify")
        if a.type == "decision":
            review_on = parse_date(a.meta.get("review_on"))
            outcome = a.meta.get("outcome")
            if outcome == "pending" and review_on and review_on < today:
                warnings.append(f"{rel(a)}: review overdue since {review_on}; close the loop")
            if outcome and outcome != "pending" and a.id not in reviewed:
                warnings.append(f"{rel(a)}: outcome '{outcome}' has no review analysis (reviews: {a.id})")
        elif a.id in inbound and inbound[a.id] == 0:
            warnings.append(f"{rel(a)}: nothing links to this artifact")

    return errors, warnings, len(artifacts) + len(skills)


def build_index(root: Path) -> dict:
    artifacts, skills, errors = load(root)
    if errors:
        raise SystemExit("cannot index, parse errors:\n  " + "\n  ".join(errors))
    nodes, edges = [], []
    for a in artifacts + skills:
        meta = {k: v for k, v in a.meta.items() if k not in ("id", "type")}
        nodes.append({"id": a.id, "type": a.type, **meta, "path": str(a.path.relative_to(root))})
        edges += [{"from": a.id, "to": d, "kind": "depends_on"} for d in a.list_field("depends_on")]
        edges += [{"from": a.id, "to": l, "kind": "link"} for l in a.wiki_links() if l != a.id]
        if a.meta.get("reviews"):
            edges.append({"from": a.id, "to": a.meta["reviews"], "kind": "reviews"})
    return {"generated": dt.date.today().isoformat(), "nodes": nodes, "edges": edges}


def render_markdown(index: dict) -> str:
    lines = [
        "# Knowledge base index",
        "",
        f"_Generated by `tools/kb.py index` on {index['generated']}. Do not edit by hand._",
        "",
    ]
    order = sorted(RANK, key=lambda t: (RANK[t], t)) + ["skill"]
    for t in order:
        nodes = [n for n in index["nodes"] if n["type"] == t]
        if not nodes:
            continue
        lines += [f"## {t.capitalize()} ({len(nodes)})", "", "| id | title | owner | status |", "|---|---|---|---|"]
        for n in sorted(nodes, key=lambda n: n["id"]):
            title = n.get("title") or n.get("description", "")[:80]
            lines.append(f"| [`{n['id']}`]({n['path']}) | {title} | {n.get('owner', '')} | {n.get('status', '')} |")
        lines.append("")
    pending = [n for n in index["nodes"] if n["type"] == "decision" and n.get("outcome") == "pending"]
    if pending:
        lines += ["## Decisions awaiting review", ""]
        for n in sorted(pending, key=lambda n: n.get("review_on", "")):
            lines.append(f"- **{n.get('review_on')}**: [`{n['id']}`]({n['path']}) {n.get('title', '')}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_check = sub.add_parser("check", help="validate a knowledge base")
    p_check.add_argument("kb_root", type=Path)
    p_check.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    p_index = sub.add_parser("index", help="write index.json and INDEX.md into <kb_root>")
    p_index.add_argument("kb_root", type=Path)
    args = parser.parse_args()

    if not (args.kb_root / "analytics-reference").is_dir():
        print(f"no analytics-reference/ folder in {args.kb_root}", file=sys.stderr)
        return 2

    if args.command == "check":
        errors, warnings, n = check(args.kb_root, args.today)
        for e in errors:
            print(f"error    {e}")
        for w in warnings:
            print(f"warning  {w}")
        print(f"\n{n} artifacts and skills · {len(errors)} errors · {len(warnings)} warnings")
        return 1 if errors else 0

    index = build_index(args.kb_root)
    (args.kb_root / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (args.kb_root / "INDEX.md").write_text(render_markdown(index), encoding="utf-8")
    print(f"wrote index.json and INDEX.md ({len(index['nodes'])} nodes, {len(index['edges'])} edges)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
