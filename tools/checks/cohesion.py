#!/usr/bin/env python3
"""Check 3 — Organizational cohesion & redundancy (run weekly). Deterministic pass.

Is the knowledge base organized so an agent can find things fast, and is it free of
duplicated knowledge?

Cohesion
  misplaced            artifact type doesn't belong in its folder (config: structure.folders)
  crowded_folder       too many files in one folder (structure.max_files_per_folder)
  too_deep             nested deeper than structure.max_depth
  oversized            artifact longer than structure.max_words; split it
  dead_end             derived artifact (metric and above) with no outbound links

Redundancy
  near_duplicate       two passages in different files say nearly the same thing
                       (word 4-gram Jaccard ≥ structure.duplicate_threshold). Keep it in
                       the more fundamental artifact and link from the other.

The agent pass (system/prompts/cohesion-redundancy.md) handles what this can't:
paraphrased duplicates, artifacts that should be merged, and missing index pages.

Usage:
    python3 tools/checks/cohesion.py <kb_root> [--strict]
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from itertools import combinations
from pathlib import Path

from common import Finding, exit_code, kb, load_config, load_docs, rel, write_report

WORD = re.compile(r"[a-z0-9]+")


def passages(body: str) -> list[str]:
    """Paragraphs and list items with ≥ 10 words, excluding code blocks and tables."""
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    out = []
    for block in re.split(r"\n\s*\n|\n(?=\s*[-*]\s|\s*\d+\.\s)", body):
        block = block.strip()
        if block.startswith(("|", "#")):
            continue
        if len(WORD.findall(block.lower())) >= 10:
            out.append(block)
    return out


def shingles(text: str, n: int = 4) -> set[tuple[str, ...]]:
    words = WORD.findall(re.sub(r"\[\[[^\]]+\]\]", "", text.lower()))
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kb_root", type=Path)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    root = args.kb_root
    cfg = load_config(root)["structure"]
    docs = [d for d in load_docs(root) if not d.skill]
    findings: list[Finding] = []

    # --- Cohesion -------------------------------------------------------------
    folders: dict[str, list[str]] = cfg["folders"]
    for d in docs:
        path = rel(root, d)
        parent = str(Path(path).parent)
        rule = max((f for f in folders if parent == f or parent.startswith(f + "/")), key=len, default=None)
        if rule and d.type not in folders[rule]:
            findings.append(Finding("medium", "misplaced", path,
                                    f"A `{d.type}` in `{parent}/`, which is meant for {', '.join(folders[rule])}",
                                    "Move it to the folder for its type so agents find it where they expect."))
        if len(Path(path).parts) - 1 > cfg["max_depth"]:
            findings.append(Finding("low", "too_deep", path, f"Nested {len(Path(path).parts) - 1} levels deep",
                                    f"Flatten to ≤ {cfg['max_depth']} levels."))
        words = len(WORD.findall(d.body.lower()))
        if words > cfg["max_words"]:
            findings.append(Finding("medium", "oversized", path, f"{words} words (limit {cfg['max_words']})",
                                    "Split into focused artifacts that link to each other. Agents retrieve small, single-topic files more reliably."))
        if kb.RANK.get(d.type, 0) >= kb.RANK["metric"] and not d.list_field("depends_on") and not d.wiki_links():
            findings.append(Finding("medium", "dead_end", path, "Derived artifact with no outbound links",
                                    "Link what it's built from (depends_on) so agents can trace its lineage."))
    for folder, n in Counter(str(Path(rel(root, d)).parent) for d in docs).items():
        if n > cfg["max_files_per_folder"]:
            findings.append(Finding("low", "crowded_folder", folder, f"{n} artifacts in one folder",
                                    "Group into subfolders by domain."))

    # --- Redundancy -----------------------------------------------------------
    chunks = [(d, p, shingles(p)) for d in docs for p in passages(d.body)]
    for (d1, p1, s1), (d2, p2, s2) in combinations(chunks, 2):
        if d1.path == d2.path:
            continue
        score = jaccard(s1, s2)
        if score >= cfg["duplicate_threshold"]:
            # Keep the more fundamental artifact; on a tie prefer sources, then the older (original) text.
            keep, other = sorted([d1, d2], key=lambda d: (kb.RANK.get(d.type, 9), d.type != "source",
                                                         str(d.meta.get("updated", "")), d.id))
            findings.append(Finding(
                "medium", "near_duplicate", f"{rel(root, d1)} ↔ {rel(root, d2)}",
                f"Near-duplicate passages ({score:.0%} overlap)",
                f"Keep the text in `{keep.id}` (more fundamental) and replace it in `{other.id}` with a link: [[{keep.id}]].",
                [f"`{rel(root, d1)}`: “{p1[:180]}”", f"`{rel(root, d2)}`: “{p2[:180]}”"],
            ))

    write_report(root, "cohesion-redundancy", "Organizational cohesion & redundancy report (deterministic pass)", findings,
                 {"artifacts": len(docs), "passages_compared": len(chunks)})
    return exit_code(findings, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
