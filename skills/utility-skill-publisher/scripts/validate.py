#!/usr/bin/env python3
"""
Skill-publisher Gate 7 validator.

Runs all deterministic Gate 7 checks against a target SKILL.md and emits
a single PASS/FAIL block. Replaces inline grep+python in skill-publisher
SKILL.md per resource-placement rule R1 (deterministic procedures live
in scripts/, not skill bodies).

Usage:
    python3 scripts/validate.py <path-to-SKILL.md>

Exit code 0 if all checks pass, 1 otherwise.
"""

import re
import subprocess
import sys
from pathlib import Path


GREP_CHECKS = [
    ("blockquotes",       r"^> "),
    ("double separator",  r"^---$"),
    ("hedged language",   r"it is recommended\|you might\|you may\|feel free\|consider "),
    ("bad version refs",  r"_v[0-9]\+\.[0-9]\+"),
    ("second-person",     r"\bI can\b\|\bI will\b\|\bYou can\b\|\bYou should\b"),
    ("dated content",     r"before [0-9]\{4\}\|after [0-9]\{4\}"),
]

# Structural presence checks — HARD FAIL if absent.
# These catch cognitive omission of required body elements (Gate 3 / Gate 5).
# Note: grep confirms string presence, not semantic correctness — a skill that
# includes "Type: dispatcher" but puts domain expertise in the body still
# violates 5d; that remains a self-assessed check.
STRUCTURAL_CHECKS = [
    ("type dispatcher",      r"^Type: dispatcher",               "HARD FAIL"),
    ("gotchas section",      r"^## GOTCHAS",                     "HARD FAIL"),
    ("skill version",        r"^SKILL_VERSION:",                 "HARD FAIL"),
    ("use automatically",    r"Use automatically",               "HARD FAIL"),
    ("reference reload",     r"do not persist across turns",     "HARD FAIL"),
]


def run_grep(label: str, pattern: str, path: Path) -> tuple[str, list[str]]:
    """Returns (status, matched_lines). status is 'PASS' or 'FAIL' or 'NOTE'.
    Double-separator is informational only (--- is valid markdown for section
    breaks); reported as NOTE with count."""
    result = subprocess.run(
        ["grep", "-n", pattern, str(path)],
        capture_output=True, text=True
    )
    lines = [l for l in result.stdout.strip().split("\n") if l]
    if label == "double separator":
        return ("NOTE", [f"{len(lines)} occurrences (informational)"])
    return ("PASS" if not lines else "FAIL", lines)


def check_description(content: str) -> tuple[str, str]:
    m = re.search(r"description:\s*>\n(.*?)^---", content, re.MULTILINE | re.DOTALL)
    if not m:
        return ("FAIL", "description block not found")
    desc = " ".join(line.strip() for line in m.group(1).strip().splitlines())
    n = len(desc)
    status = "PASS" if n <= 1024 else "FAIL"
    return (status, f"{n} chars (limit: 1024)")


def check_name(content: str) -> tuple[str, str]:
    m = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if not m:
        return ("FAIL", "name field not found")
    name = m.group(1).strip()
    n = len(name)
    status = "PASS" if n <= 64 else "FAIL"
    return (status, f'"{name}" ({n} chars; limit: 64)')


def check_line_count(path: Path) -> tuple[str, str]:
    n = sum(1 for _ in path.open())
    if n > 500:
        return ("FAIL", f"{n} lines (HARD LIMIT: 500)")
    if n > 400:
        return ("WARN", f"{n} lines (target: 400, hard limit: 500)")
    return ("PASS", f"{n} lines")


def _check_gate_token(skill_name: str) -> tuple[bool, str]:
    """
    Check that skill_gate_open.py was called for this skill today (P-12 / F-050 STRUCTURAL fix).

    Token path: /tmp/skill-gate-{name}-{date}.token
    Written by ci/skill_gate_open.py at Gate 0 entry.

    Returns (ok, message).
    """
    import re
    from datetime import date
    safe = re.sub(r"[^a-zA-Z0-9_-]", "-", skill_name)
    token = Path("/tmp") / f"skill-gate-{safe}-{date.today()}.token"
    if token.exists():
        return True, f"gate token present ({token.name})"
    return False, (
        f"gate token absent — skill-publisher gate sequence was not opened for '{skill_name}'.\n"
        f"  Run first: python3 ci/skill_gate_open.py --skill {skill_name}\n"
        f"  Then restart the gate sequence from Gate 0.\n"
        f"  Expected token: {token}\n"
        f"  (P-12 / F-050 STRUCTURAL gate — context-switch momentum bypass prevention)"
    )


def _skill_name_from_path(path: Path) -> str:
    """
    Infer skill name from SKILL.md path.
    /tmp/utility-data-analyst/SKILL.md -> utility-data-analyst
    /mnt/skills/user/utility-data-analyst/SKILL.md -> utility-data-analyst
    Falls back to parent dir name; if that is 'scripts' or '.', uses grandparent.
    """
    parent = path.parent.name
    if parent in ("scripts", ".", ""):
        parent = path.parent.parent.name
    return parent


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/validate.py <path-to-SKILL.md> [--skip-token-check]", file=sys.stderr)
        return 2

    skip_token = "--skip-token-check" in sys.argv
    skill_md_args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not skill_md_args:
        print("Usage: python3 scripts/validate.py <path-to-SKILL.md> [--skip-token-check]", file=sys.stderr)
        return 2

    path = Path(skill_md_args[0])
    if not path.exists():
        print(f"FAIL — file not found: {path}", file=sys.stderr)
        return 1

    # ── Gate token check (P-12 / F-050 STRUCTURAL gate) ──────────────────────
    # Blocks Gate 7 if skill_gate_open.py was not called for this skill today.
    # --skip-token-check is reserved for CI mode (pre-commit / GitHub Actions)
    # where gate sequence is not applicable. Never use in interactive sessions.
    if not skip_token:
        skill_name = _skill_name_from_path(path)
        token_ok, token_msg = _check_gate_token(skill_name)
        if not token_ok:
            print("GATE 7 VALIDATOR — TOKEN CHECK FAIL")
            print("-" * 60)
            print(f"  SGT-01  ✗  {token_msg}")
            print("-" * 60)
            print("OVERALL: FAIL (gate sequence not opened — packaging blocked)")
            return 1

    content = path.read_text()
    fails = 0

    print("GATE 7 VALIDATOR — " + str(path))
    print("-" * 60)

    for label, pattern in GREP_CHECKS:
        status, lines = run_grep(label, pattern, path)
        if status == "FAIL":
            fails += 1
            print(f"  {label}: FAIL")
            for line in lines:
                print(f"    {line}")
        elif status == "NOTE":
            print(f"  {label}: {lines[0]}")
        else:
            print(f"  {label}: PASS")

    status, msg = check_description(content)
    if status == "FAIL":
        fails += 1
    print(f"  description: {status} — {msg}")

    status, msg = check_name(content)
    if status == "FAIL":
        fails += 1
    print(f"  name: {status} — {msg}")

    status, msg = check_line_count(path)
    if status == "FAIL":
        fails += 1
    print(f"  line count: {status} — {msg}")

    for label, pattern, severity in STRUCTURAL_CHECKS:
        result = subprocess.run(
            ["grep", "-n", pattern, str(path)],
            capture_output=True, text=True
        )
        present = bool(result.stdout.strip())
        if present:
            print(f"  {label}: PASS")
        else:
            fails += 1
            print(f"  {label}: FAIL — '{pattern}' absent from body ({severity})")

    print("-" * 60)
    if fails:
        print(f"OVERALL: FAIL ({fails} check(s) failed)")
        return 1
    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
