#!/usr/bin/env python3
"""
Fix Type Classifier Gate — ci/check_fix_type.py

Enforces that recurring failures (recurrence_count > 1) are addressed with
STRUCTURAL or TEMPORAL fixes, never BEHAVIORAL ones. Closes the enforcement
gap on P-03 (Behavioral Fix for Structural Problem), CRITICAL, recurrence 10.

Grounds: R-019 (STRUCTURAL fixes only for recurring patterns), R-020
(self-attribution bias), R-021 (self-evaluation misses own reasoning).

Usage:
    # With D1 live query (requires Cloudflare MCP at session time):
    python3 ci/check_fix_type.py --pattern P-09 --fix-type BEHAVIORAL

    # Offline (supply recurrence count directly):
    python3 ci/check_fix_type.py --pattern P-09 --fix-type BEHAVIORAL --recurrence-count 12

    # Validate a finding JSON (same format as validate_research.py):
    python3 ci/check_fix_type.py --json '{"pattern_code":"P-09","fix_type":"BEHAVIORAL"}'

    # Batch validate a JSON file with multiple proposed fixes:
    python3 ci/check_fix_type.py --file fixes.json

Exit codes:
    0 = PASS  — fix type is acceptable for this pattern
    1 = FAIL  — BEHAVIORAL fix proposed for a pattern with recurrence > 1
    2 = WARN  — recurrence count not available, manual review required

Gates:
    FC-01  fix_type must be one of: STRUCTURAL, TEMPORAL, BEHAVIORAL
    FC-02  if pattern recurrence_count > 1 and fix_type == BEHAVIORAL → FAIL
    FC-03  if pattern recurrence_count > 3 and fix_type != STRUCTURAL → WARN
           (TEMPORAL may be insufficient for high-recurrence patterns)
    FC-04  if pattern severity == CRITICAL and fix_type == BEHAVIORAL → FAIL
           regardless of recurrence count

Fix type definitions (from D1 failure_patterns schema):
    STRUCTURAL  Environment or tool refuses — reliable. Does not drift.
                Examples: CI check, schema constraint, script gate.
    TEMPORAL    Skill or instruction updated — reliable within scope.
                Examples: skill body rewrite, gate added to process doc.
    BEHAVIORAL  Claude self-attests — unreliable for recurring issues.
                Examples: "Claude will remember to...", "gate added to output-gate text".

Known pattern metadata (fallback when D1 not available):
    Sourced from failure_patterns table as of last corpus sync.
"""

import argparse
import json
import sys
from dataclasses import dataclass


# ── Known pattern registry ────────────────────────────────────────────────────
# Primary source: ci/failure-audit-rules.json (synced from D1 after every write).
def _load_known_patterns() -> dict[str, dict]:
    """
    Load pattern registry from ci/failure-audit-rules.json.

    Reads from the "patterns" section (full metadata: name, severity, recurrence_count)
    added in the 2026-05-18 schema extension. Falls back to pattern_recurrence-only
    if the patterns section is absent (pre-extension JSON).

    failure-audit-rules.json is the canonical offline source — synced from D1 after
    every recurrence_count change or pattern INSERT via ci/sync-failure-rules.py.
    No hardcoded fallback dict.
    """
    import json
    from pathlib import Path

    candidates = [
        Path(__file__).parent / "failure-audit-rules.json",
        Path("ci/failure-audit-rules.json"),
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text())

            # Primary path: "patterns" section with full metadata
            patterns_list = data.get("patterns", [])
            if patterns_list:
                out = {}
                for row in patterns_list:
                    code = row["pattern_code"]
                    out[code] = {
                        "name": row.get("name", code),
                        "severity": row.get("severity", "UNKNOWN"),
                        "recurrence": row.get("recurrence_count", 0),
                    }
                return out

            # Fallback path: pattern_recurrence only (pre-2026-05-18 schema)
            recurrence = data.get("pattern_recurrence", {})
            if recurrence:
                print(
                    "WARNING: failure-audit-rules.json has pattern_recurrence but not patterns section. "
                    "Re-run sync to get full metadata: python3 ci/sync-failure-rules.py ...",
                    file=__import__("sys").stderr,
                )
                out = {}
                for code, count in recurrence.items():
                    out[code] = {"name": code, "severity": "UNKNOWN", "recurrence": count}
                return out

            print(
                "WARNING: failure-audit-rules.json found but missing both 'patterns' and "
                "'pattern_recurrence' blocks. Run: python3 ci/sync-failure-rules.py ...",
                file=__import__("sys").stderr,
            )
            return {}
        except (json.JSONDecodeError, KeyError) as e:
            print(f"WARNING: could not parse {path}: {e}", file=__import__("sys").stderr)
            return {}

    print(
        "WARNING: ci/failure-audit-rules.json not found. "
        "Run sync to generate it before using check_fix_type.py.",
        file=__import__("sys").stderr,
    )
    return {}


KNOWN_PATTERNS: dict[str, dict] = _load_known_patterns()

VALID_FIX_TYPES = {"STRUCTURAL", "TEMPORAL", "BEHAVIORAL"}
CRITICAL_SEVERITY = {"CRITICAL"}


# ── Gate implementations ──────────────────────────────────────────────────────

@dataclass
class PatternMeta:
    code: str
    name: str
    severity: str
    recurrence: int
    source: str  # "live" | "local-registry" | "unknown"


def resolve_pattern(pattern_code: str, recurrence_override: int | None) -> PatternMeta:
    """Resolve pattern metadata from local registry or override."""
    if pattern_code in KNOWN_PATTERNS:
        p = KNOWN_PATTERNS[pattern_code]
        rec = recurrence_override if recurrence_override is not None else p["recurrence"]
        src = "recurrence-override" if recurrence_override is not None else "local-registry"
        return PatternMeta(pattern_code, p["name"], p["severity"], rec, src)
    # Unknown pattern
    rec = recurrence_override if recurrence_override is not None else -1
    return PatternMeta(
        pattern_code, "UNKNOWN", "UNKNOWN",
        rec, "unknown"
    )


def fc_01_valid_fix_type(fix_type: str) -> tuple[bool, str]:
    if fix_type.upper() not in VALID_FIX_TYPES:
        return False, f"fix_type '{fix_type}' is not valid — must be one of {sorted(VALID_FIX_TYPES)}"
    return True, f"fix_type '{fix_type}' is a recognised class"


def fc_02_behavioral_recurrence(pattern: PatternMeta, fix_type: str) -> tuple[str, str]:
    """
    Returns (status, message) where status is PASS | FAIL | WARN.
    WARN when recurrence is unknown (cannot confirm or deny).
    """
    ft = fix_type.upper()
    if ft != "BEHAVIORAL":
        return "PASS", f"fix_type '{fix_type}' is not BEHAVIORAL — no recurrence constraint"
    if pattern.recurrence == -1:
        return "WARN", (
            f"pattern '{pattern.code}' not in local registry and no --recurrence-count supplied — "
            "cannot confirm recurrence. Provide --recurrence-count or query D1 before proceeding."
        )
    if pattern.recurrence > 1:
        return "FAIL", (
            f"BEHAVIORAL fix proposed for '{pattern.code}' ({pattern.name}) "
            f"with recurrence_count={pattern.recurrence}. "
            "BEHAVIORAL fixes are insufficient for recurring failures — "
            "must escalate to STRUCTURAL or TEMPORAL. (R-019)"
        )
    return "PASS", f"recurrence_count={pattern.recurrence} — BEHAVIORAL acceptable for first occurrence"


def fc_03_temporal_high_recurrence(pattern: PatternMeta, fix_type: str) -> tuple[str, str]:
    """
    WARN when TEMPORAL is proposed for a pattern with recurrence > 3.
    TEMPORAL may be insufficient at high recurrence — STRUCTURAL preferred.
    """
    ft = fix_type.upper()
    if ft != "TEMPORAL":
        return "PASS", "n/a"
    if pattern.recurrence == -1:
        return "PASS", "recurrence unknown — skipping high-recurrence check"
    if pattern.recurrence > 3:
        return "WARN", (
            f"TEMPORAL fix for '{pattern.code}' with recurrence_count={pattern.recurrence} "
            "— at recurrence > 3 a TEMPORAL fix (skill/instruction update) may be insufficient. "
            "Confirm whether a STRUCTURAL gate is feasible. (R-019)"
        )
    return "PASS", f"recurrence_count={pattern.recurrence} — TEMPORAL acceptable"


def fc_04_critical_behavioral(pattern: PatternMeta, fix_type: str) -> tuple[str, str]:
    """FAIL when BEHAVIORAL is proposed for a CRITICAL-severity pattern."""
    ft = fix_type.upper()
    if ft != "BEHAVIORAL":
        return "PASS", "n/a"
    if pattern.severity in CRITICAL_SEVERITY:
        return "FAIL", (
            f"BEHAVIORAL fix proposed for CRITICAL-severity pattern '{pattern.code}' "
            f"({pattern.name}). CRITICAL patterns require STRUCTURAL or TEMPORAL fixes "
            "regardless of recurrence count. (R-019, R-020)"
        )
    return "PASS", f"severity '{pattern.severity}' — BEHAVIORAL not blocked by FC-04 alone"


# ── Runner ────────────────────────────────────────────────────────────────────

def _status_char(status: str) -> str:
    return {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}.get(status, "?")


def validate_one(pattern_code: str, fix_type: str, recurrence_override: int | None) -> int:
    pattern = resolve_pattern(pattern_code, recurrence_override)

    print(f"\nFIX TYPE CLASSIFIER — {pattern_code} / fix_type={fix_type}")
    print(f"  Pattern : {pattern.name}")
    print(f"  Severity: {pattern.severity}")
    print(f"  Recurrence: {pattern.recurrence if pattern.recurrence >= 0 else 'unknown'} "
          f"(source: {pattern.source})")
    print("=" * 60)

    hard_fails = []
    warnings = []

    # FC-01
    ok, msg = fc_01_valid_fix_type(fix_type)
    status = "PASS" if ok else "FAIL"
    print(f"  FC-01  {_status_char(status)}  Valid fix_type: {msg}")
    if not ok:
        hard_fails.append(msg)
        # Cannot continue without a valid fix_type
        print()
        print(f"VERDICT: FAIL ({len(hard_fails)} error(s))")
        return 1

    # FC-02
    status, msg = fc_02_behavioral_recurrence(pattern, fix_type)
    print(f"  FC-02  {_status_char(status)}  Recurrence gate: {msg}")
    if status == "FAIL":
        hard_fails.append(msg)
    elif status == "WARN":
        warnings.append(msg)

    # FC-03
    status, msg = fc_03_temporal_high_recurrence(pattern, fix_type)
    print(f"  FC-03  {_status_char(status)}  High-recurrence TEMPORAL check: {msg}")
    if status == "WARN":
        warnings.append(msg)

    # FC-04
    status, msg = fc_04_critical_behavioral(pattern, fix_type)
    print(f"  FC-04  {_status_char(status)}  CRITICAL severity gate: {msg}")
    if status == "FAIL":
        hard_fails.append(msg)

    print()
    if hard_fails:
        print(f"VERDICT: FAIL ({len(hard_fails)} error(s)) — fix type must change before logging")
        for e in hard_fails:
            print(f"  ✗ {e}")
        return 1
    if warnings:
        print(f"VERDICT: WARN ({len(warnings)} warning(s)) — proceed with caution")
        for w in warnings:
            print(f"  ⚠ {w}")
        return 2
    print("VERDICT: PASS — fix type is acceptable for this pattern")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate fix type before logging to D1 granular_findings (P-03 enforcement)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pattern", help="Pattern code (e.g. P-09)")
    group.add_argument("--json", help='Inline JSON: {"pattern_code":"P-09","fix_type":"BEHAVIORAL"}')
    group.add_argument("--file", help="JSON file with one or more {pattern_code, fix_type} entries")

    parser.add_argument("--fix-type", help="Fix type: STRUCTURAL | TEMPORAL | BEHAVIORAL")
    parser.add_argument("--recurrence-count", type=int, default=None,
                        help="Override recurrence count (bypasses local registry)")

    args = parser.parse_args()

    if args.json:
        try:
            data = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid JSON — {e}", file=sys.stderr)
            sys.exit(1)
        entries = [data] if isinstance(data, dict) else data

    elif args.file:
        try:
            with open(args.file) as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        entries = [data] if isinstance(data, dict) else data

    else:
        if not args.fix_type:
            parser.error("--fix-type is required when using --pattern")
        entries = [{"pattern_code": args.pattern, "fix_type": args.fix_type}]

    worst_exit = 0
    for entry in entries:
        code = entry.get("pattern_code", "UNKNOWN")
        ft = entry.get("fix_type", "")
        rec = entry.get("recurrence_count", args.recurrence_count)
        result = validate_one(code, ft, rec)
        worst_exit = max(worst_exit, result)

    sys.exit(worst_exit)


if __name__ == "__main__":
    main()
