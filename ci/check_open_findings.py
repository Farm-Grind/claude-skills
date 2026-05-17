#!/usr/bin/env python3
"""
Open Findings Queue Gate — ci/check_open_findings.py

Queries D1 granular_findings for OPEN items and blocks new audit/triage
sessions from starting while unresolved prior findings exist. Closes the
enforcement gap on P-08 (Unbounded Meta-Work, recurrence 8) and P-01
(Self-Referential Audit Loop, recurrence 6).

Grounds: R-023/R-024 (bounded vs unbounded work), R-047 (CAPA tracking —
proposed fixes that age without implementation), R-020 (self-referential
audit loop cannot return "the loop is the problem").

Usage:
    # Live D1 query (primary path — outputs SQL for Claude to run via MCP):
    python3 ci/check_open_findings.py --emit-sql

    # Offline with JSON input (from D1 query result pasted as JSON):
    python3 ci/check_open_findings.py --json '[{"finding_id":"F-016",...}]'

    # Offline with a JSON file:
    python3 ci/check_open_findings.py --file findings.json

    # Override: allow proceeding despite open findings (requires justification):
    python3 ci/check_open_findings.py --file findings.json --override "F-016 is blocked on upstream dependency X"

Exit codes:
    0 = PASS  — no OPEN findings (or override accepted)
    1 = FAIL  — OPEN findings exist; new audit must not start
    2 = WARN  — OPEN findings exist but all are blocked on external dependency

SQL to run in D1 (claude-config: afd78e0e-583e-4e78-87fc-dd6bc8150ce9):
    SELECT finding_id, pattern_code, title, status, artifact_affected
    FROM granular_findings
    WHERE status = 'OPEN'
    ORDER BY pattern_code, finding_id;

Gates:
    OFQ-01  No OPEN findings → PASS
    OFQ-02  OPEN findings present, no override → FAIL with finding list
    OFQ-03  OPEN findings present, override provided → WARN (logged, not blocked)
    OFQ-04  OPEN findings present, all pattern_code = P-07 or P-16 (external
            platform limits — cannot be internally resolved) → WARN not FAIL
"""

import argparse
import json
import sys


# ── Patterns that are exempt from blocking (external dependencies) ────────────
# These are patterns where "OPEN" status is expected to persist because
# resolution depends on external factors (platform changes, upstream fixes).
EXTERNAL_DEPENDENCY_PATTERNS = {
    "P-07",   # Platform Constraint Discovery — blocked on vendor changes
}


# ── Formatters ────────────────────────────────────────────────────────────────

def _fmt_finding(f: dict) -> str:
    fid = f.get("finding_id", "?")
    pcode = f.get("pattern_code", "?")
    title = f.get("title", f.get("symptom", "no title"))[:70]
    artifact = f.get("artifact_affected", "")
    artifact_str = f" [{artifact}]" if artifact else ""
    return f"  {fid}  {pcode}{artifact_str}  {title}"


# ── Gate implementations ──────────────────────────────────────────────────────

def classify_findings(findings: list[dict]) -> tuple[list, list]:
    """
    Split findings into:
      blocking    — must be resolved before new audit starts
      non_blocking — external dependency patterns (WARN not FAIL)
    """
    blocking = []
    non_blocking = []
    for f in findings:
        if f.get("pattern_code") in EXTERNAL_DEPENDENCY_PATTERNS:
            non_blocking.append(f)
        else:
            blocking.append(f)
    return blocking, non_blocking


def run_gates(findings: list[dict], override: str | None) -> int:
    open_findings = [f for f in findings if f.get("status", "").upper() == "OPEN"]

    print("\nOPEN FINDINGS QUEUE GATE")
    print("=" * 60)
    print(f"  Total OPEN findings: {len(open_findings)}")

    if not open_findings:
        print()
        print("VERDICT: PASS — no OPEN findings, new audit may proceed")
        return 0

    blocking, non_blocking = classify_findings(open_findings)

    if non_blocking:
        print(f"\n  Non-blocking (external dependency — P-07 class): {len(non_blocking)}")
        for f in non_blocking:
            print(_fmt_finding(f))

    if blocking:
        print(f"\n  Blocking (must resolve before new audit): {len(blocking)}")
        for f in blocking:
            print(_fmt_finding(f))

    print()

    if override:
        print(f"OVERRIDE PROVIDED: \"{override}\"")
        if blocking:
            print(f"VERDICT: WARN ({len(blocking)} blocking finding(s) — override accepted)")
            print("  ⚠ Override is logged. Ensure override justification is added to the")
            print("    finding record in D1 before starting the new audit.")
            return 2
        print("VERDICT: WARN (only external-dependency findings open — override not required but accepted)")
        return 2

    if not blocking:
        # Only non-blocking findings open
        print(f"VERDICT: WARN ({len(non_blocking)} external-dependency finding(s) open)")
        print("  These are P-07-class findings (platform constraints) — resolution depends")
        print("  on external factors. New audit may proceed but must not add new P-07 findings")
        print("  without first closing one.")
        return 2

    # Blocking findings, no override
    print(f"VERDICT: FAIL ({len(blocking)} blocking finding(s) must be resolved first)")
    print()
    print("  Resolution options:")
    print("  1. Implement the fix for each finding and update status to RESOLVED in D1")
    print("  2. Explicitly park a finding with --override \"<justification>\"")
    print("     (justification is logged; override is not a skip — it is an audit trail entry)")
    print()
    print("  D1 update query (per finding):")
    print("    UPDATE granular_findings SET status='RESOLVED' WHERE finding_id='F-XXX';")
    print()
    print("  D1 database: afd78e0e-583e-4e78-87fc-dd6bc8150ce9")
    return 1


# ── SQL emitter ───────────────────────────────────────────────────────────────

EMIT_SQL = """-- Run this query via Cloudflare MCP (D1: afd78e0e-583e-4e78-87fc-dd6bc8150ce9)
-- Then pass the results to: python3 ci/check_open_findings.py --json '<results>'

SELECT finding_id, pattern_code, title, status, artifact_affected
FROM granular_findings
WHERE status = 'OPEN'
ORDER BY pattern_code, finding_id;
"""


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check for OPEN findings before starting a new audit (P-08/P-01 enforcement)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit-sql", action="store_true",
                       help="Print the D1 SQL query to run, then exit 0")
    group.add_argument("--json", metavar="JSON",
                       help="JSON array of finding rows from D1 query")
    group.add_argument("--file", metavar="FILE",
                       help="JSON file containing array of finding rows")

    parser.add_argument("--override", metavar="JUSTIFICATION",
                        help="Override block with a justification string (audit trail)")

    args = parser.parse_args()

    if args.emit_sql:
        print(EMIT_SQL)
        sys.exit(0)

    if args.json:
        try:
            findings = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid JSON — {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            with open(args.file) as fh:
                findings = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(findings, list):
        # D1 MCP sometimes returns {"results": [...]}
        if isinstance(findings, dict) and "results" in findings:
            findings = findings["results"]
        else:
            print("ERROR: expected a JSON array of finding rows", file=sys.stderr)
            sys.exit(1)

    sys.exit(run_gates(findings, args.override))


if __name__ == "__main__":
    main()
