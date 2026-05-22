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


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate.py <path-to-SKILL.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FAIL — file not found: {path}", file=sys.stderr)
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
