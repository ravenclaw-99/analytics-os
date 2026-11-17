#!/usr/bin/env python3
"""Check 2 — Semantic integrity (run weekly). Deterministic pass.

Every governed term (ARR, DAU, NRR, …) has exactly one canonical artifact, listed in
system/config.json → canonical_terms. This pass scans the whole knowledge base and
flags:

  competing_definition  (high)   text outside the canonical artifact that *defines* the
                                 term ("X is defined as", "X =", "X means") without
                                 deferring to the canonical link
  unlinked_mention      (low)    a file that uses the term but never links its canonical
                                 definition, so an agent reading it can't find the source of truth

It also writes `review_sets` into the JSON report: for each term, every file that
discusses it. The agent pass (system/prompts/semantic-integrity.md) reads those sets
and checks that the meaning actually agrees, which needs judgment, not regexes.

Usage:
    python3 tools/checks/semantic_integrity.py <kb_root> [--strict]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import Finding, exit_code, full_text, load_config, load_docs, rel, sentences, write_report

DEFINES = re.compile(r"(\bdefined as\b|\bcalculated as\b|\bmeans\b|(?<![<>!=])=(?!=))", re.I)


def term_pattern(term: str) -> re.Pattern:
    # Acronyms are case-sensitive (ARR ≠ "arr"); phrases are not.
    # Word boundaries exclude identifiers like ARR_end or arr_usd.
    flags = 0 if term.isupper() else re.I
    return re.compile(rf"(?<![\w.`]){re.escape(term)}(?![\w`])", flags)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kb_root", type=Path)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    root = args.kb_root
    terms: dict[str, str] = load_config(root)["canonical_terms"]
    docs = load_docs(root)
    ids = {d.id for d in docs}
    findings: list[Finding] = []
    review_sets: dict[str, list[str]] = {}

    for term, canonical in terms.items():
        if canonical not in ids:
            findings.append(Finding("high", "missing_canonical", term,
                                    f"Canonical artifact `{canonical}` for '{term}' doesn't exist",
                                    "Fix system/config.json or create the artifact."))
            continue
        pat = term_pattern(term)
        link = f"[[{canonical}]]"
        mentioned_in = []
        for d in docs:
            if d.id == canonical:
                continue
            text = full_text(d)
            hits = [s for s in sentences(d.body) if pat.search(s)]
            if not hits:
                continue
            mentioned_in.append(rel(root, d))
            for s in hits:
                m = pat.search(s)
                after = s[m.end():]
                if DEFINES.search(after[:60]) and link not in s:
                    findings.append(Finding(
                        "high", "competing_definition", rel(root, d),
                        f"Defines '{term}' outside its canonical artifact `{canonical}`",
                        f"Replace the definition with a link to {link}. If the difference is real and "
                        f"intentional, give it a distinct governed name.",
                        [f"“{s[:220]}”"],
                    ))
            if link not in text and canonical not in d.list_field("depends_on"):
                findings.append(Finding(
                    "low", "unlinked_mention", rel(root, d),
                    f"Uses '{term}' but never links its canonical definition",
                    f"Link {link} at the first mention.",
                    [f"“{hits[0][:160]}”"],
                ))
        review_sets[term] = [canonical] + mentioned_in

    write_report(root, "semantic-integrity", "Semantic integrity report (deterministic pass)", findings,
                 {"review_sets": review_sets})
    return exit_code(findings, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
