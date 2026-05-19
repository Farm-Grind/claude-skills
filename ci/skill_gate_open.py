#!/usr/bin/env python3
"""
ci/skill_gate_open.py — Skill-publisher gate sequence entry point (P-12 F-050 STRUCTURAL fix)

Writes a session-scoped gate token to /tmp/skill-gate-{name}-{date}.token.
validate.py checks for this token before running Gate 7 checks; if absent,
validate.py exits 1 and blocks packaging.

This creates an in-session STRUCTURAL gate: validate.py cannot succeed unless
the gate sequence was explicitly opened via this script. Momentum-based
packaging that bypasses Gate 0 will be blocked at Gate 7, not at commit time.

Usage:
    python3 ci/skill_gate_open.py --skill <skill-name>

    # Or from the /tmp/<skill-name>/ workspace path (extracts name automatically):
    python3 ci/skill_gate_open.py --skill-path /tmp/<skill-name>/SKILL.md

Exit codes:
    0 = token written — gate sequence open
    1 = error (missing argument, write failure)

Token path: /tmp/skill-gate-{name}-{date}.token
Token is intentionally left on disk until /tmp is cleared — no cleanup required.
Scoped by name + date: cannot be reused across different skills or different days.

Pattern: P-12 (F-050) — Context-Switch Momentum Overrides Procedural Gates
Companion: skills/utility-skill-publisher/scripts/validate.py (token reader)
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path


TOKEN_DIR = Path("/tmp")
TODAY = str(date.today())


def token_path(skill_name: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "-", skill_name)
    return TOKEN_DIR / f"skill-gate-{safe}-{TODAY}.token"


def open_gate(skill_name: str) -> int:
    tpath = token_path(skill_name)
    try:
        tpath.write_text(f"skill={skill_name}\ndate={TODAY}\nopened_by=skill_gate_open.py\n")
    except OSError as e:
        print(f"ERROR: could not write gate token: {e}", file=sys.stderr)
        return 1

    print(f"GATE SEQUENCE OPEN — {skill_name}")
    print(f"  Token  : {tpath}")
    print(f"  Date   : {TODAY}")
    print(f"  Valid  : this session only (date-scoped)")
    print()
    print("  Gate sequence is now open. Run gates 0–6 before invoking validate.py.")
    print("  validate.py will exit 1 if this token is absent or stale.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open a skill-publisher gate sequence for the named skill."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--skill", help="Skill name (e.g. utility-data-analyst)")
    group.add_argument(
        "--skill-path",
        help="Path to SKILL.md — extracts skill name from parent directory",
    )
    args = parser.parse_args()

    if args.skill_path:
        skill_name = Path(args.skill_path).parent.name
        if not skill_name:
            print("ERROR: could not extract skill name from path", file=sys.stderr)
            return 1
    else:
        skill_name = args.skill

    return open_gate(skill_name)


if __name__ == "__main__":
    sys.exit(main())
