#!/usr/bin/env python3
"""Check 1 — Schema integrity (run daily).

Verifies that the knowledge base still matches the live warehouse:
  1. Every table mentioned anywhere in the knowledge base still exists.
  2. Every column documented for a key table still exists.
  3. Every column that exists in a key table is documented somewhere.

The warehouse catalog is one information_schema query (see system/config.json →
warehouse.catalog_query). In production, the job runner fetches it through the
warehouse MCP or CLI and passes it here as JSON. Everything after that is
deterministic, so results are reproducible and cheap.

Usage:
    python3 tools/checks/schema_integrity.py <kb_root> --catalog catalog.json [--strict]

catalog.json: {"columns": [[schema, table, column], ...]}
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import defaultdict
from pathlib import Path

from common import Finding, exit_code, full_text, load_config, load_docs, rel, write_report

HEADING = re.compile(r"^#{2,4}\s+`?([a-z0-9_]+\.[a-z0-9_]+)`?\s*$", re.M)
COLUMN_ROW = re.compile(r"^\|\s*`([a-z0-9_]+)`\s*\|", re.M)
BACKTICKED = re.compile(r"`([a-z][a-z0-9_]*)`")


def load_catalog(path: Path) -> dict[str, set[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    tables: dict[str, set[str]] = defaultdict(set)
    for schema, table, column in data["columns"]:
        tables[f"{schema}.{table}".lower()].add(column.lower())
    return tables


def key_table_docs(text: str) -> dict[str, set[str]]:
    """Parse '### schema.table' sections followed by '| `column` |' rows."""
    docs: dict[str, set[str]] = {}
    matches = list(HEADING.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        docs[m.group(1).lower()] = set(COLUMN_ROW.findall(text[m.end() : end]))
    return docs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kb_root", type=Path)
    ap.add_argument("--catalog", type=Path, required=True)
    ap.add_argument("--strict", action="store_true", help="exit 1 if any high-severity finding")
    args = ap.parse_args()

    root = args.kb_root
    config = load_config(root)
    catalog = load_catalog(args.catalog)
    docs = load_docs(root)
    schemas = config["warehouse"]["schemas"]
    table_ref = re.compile(r"\b(" + "|".join(map(re.escape, schemas)) + r")\.([a-z0-9_]+)\b")
    findings: list[Finding] = []

    # 1. Every referenced table still exists.
    refs: dict[str, list[str]] = defaultdict(list)
    for d in docs:
        for lineno, line in enumerate(full_text(d).splitlines(), 1):
            for schema, table in table_ref.findall(line):
                refs[f"{schema}.{table}"].append(f"{rel(root, d)}:{lineno}")
    for table, places in sorted(refs.items()):
        if table in catalog:
            continue
        schema = table.split(".")[0]
        candidates = [t for t in catalog if t.startswith(schema + ".")]
        close = difflib.get_close_matches(table, candidates, n=1, cutoff=0.75)
        findings.append(
            Finding(
                severity="high",
                kind="missing_table",
                where=table,
                message=f"`{table}` is referenced in the knowledge base but no longer exists in the warehouse",
                proposed_fix=(f"It looks like it was renamed to `{close[0]}`. Update the references and re-validate."
                              if close else "Find what replaced it (check recent pipeline PRs) or deprecate the references."),
                evidence=[f"referenced at `{p}`" for p in places],
                recommended_action="accept" if close else "refine",
                confidence="medium" if close else "high",
            )
        )

    # 2 + 3. Key tables: documented columns exist, and existing columns are documented.
    register_id = config.get("key_tables_register")
    register = next((d for d in docs if d.id == register_id), None)
    if register is None:
        findings.append(Finding("medium", "no_key_tables", register_id or "(unset)",
                                "No key-tables register found, so column coverage can't be checked",
                                "Create a register listing key tables and their columns."))
    else:
        documented_anywhere = set()
        for d in docs:
            documented_anywhere |= set(BACKTICKED.findall(full_text(d)))
        for table, documented in sorted(key_table_docs(register.body).items()):
            where = rel(root, register)
            live = catalog.get(table)
            if live is None:
                continue  # already reported as missing_table
            for col in sorted(documented - live):
                close = difflib.get_close_matches(col, sorted(live - documented), n=1, cutoff=0.5)
                findings.append(Finding(
                    "high", "missing_column", f"{table}.{col}",
                    f"Documented column `{table}.{col}` no longer exists",
                    f"Looks renamed to `{close[0]}`; update the register and any queries." if close
                    else "Remove it from the register, and check queries that use it.",
                    [f"documented in `{where}`"],
                    recommended_action="accept" if close else "refine",
                ))
            for col in sorted(live - documented):
                if col in documented_anywhere:
                    continue
                findings.append(Finding(
                    "medium", "undocumented_column", f"{table}.{col}",
                    f"Key table column `{table}.{col}` exists in the warehouse but isn't documented anywhere",
                    f"Add a row for `{col}` under `### {table}` in `{where}`, with a description.",
                ))

    write_report(root, "schema-integrity", "Schema integrity report", findings,
                 {"tables_referenced": len(refs), "tables_in_catalog": len(catalog)})
    return exit_code(findings, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
