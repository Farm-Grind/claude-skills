#!/usr/bin/env python3
"""
Shared skill validator (relocated from utility-skill-publisher/scripts/validate.py).

Runs all deterministic Gate 7 checks against a target SKILL.md and emits
a single PASS/FAIL block. CI runs this against every SKILL.md in the repo.

v4 additions:
  1. Every references/*.md cited in a SKILL.md must exist on disk.
  2. No line may cite arxiv 2605.06445 or arxiv 2601.22025.

Usage:
    python3 ci/validate.py <path-to-SKILL.md>

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

BANNED_ARXIV = ["2605.06445", "2601.22025"]


def run_grep(label: str, pattern: str, path: Path) -> tuple[str, list[str]]:
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
    return ("PASS" if n <= 1024 else "FAIL", f"{n} chars (limit: 1024)")


def check_name(content: str) -> tuple[str, str]:
    m = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if not m:
        return ("FAIL", "name field not found")
    name = m.group(1).strip()
    n = len(name)
    return ("PASS" if n <= 64 else "FAIL", f'"{name}" ({n} chars; limit: 64)')


def check_line_count(path: Path) -> tuple[str, str]:
    n = sum(1 for _ in path.open())
    if n > 500:
        return ("FAIL", f"{n} lines (HARD LIMIT: 500)")
    if n > 400:
        return ("WARN", f"{n} lines (target: 400, hard limit: 500)")
    return ("PASS", f"{n} lines")


def check_reference_files(content: str, skill_dir: Path) -> tuple[str, list[str]]:
    """All references/*.md cited in the skill body must exist on disk."""
    cited = re.findall(r"references/[\w\-]+\.md", content)
    missing = [f for f in cited if not (skill_dir / f).exists()]
    if missing:
        return ("FAIL", missing)
    return ("PASS", [])


def check_banned_arxiv(content: str) -> tuple[str, list[str]]:
    hits = [a for a in BANNED_ARXIV if a in content]
    return ("FAIL" if hits else "PASS", hits)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 ci/validate.py <path-to-SKILL.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FAIL — file not found: {path}", file=sys.stderr)
        return 1

    content = path.read_text()
    skill_dir = path.parent
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

    status, missing = check_reference_files(content, skill_dir)
    if status == "FAIL":
        fails += 1
        print(f"  reference files: FAIL — missing: {missing}")
    else:
        print(f"  reference files: PASS")

    status, hits = check_banned_arxiv(content)
    if status == "FAIL":
        fails += 1
        print(f"  banned arxiv: FAIL — {hits}")
    else:
        print(f"  banned arxiv: PASS")

    print("-" * 60)
    if fails:
        print(f"OVERALL: FAIL ({fails} check(s) failed)")
        return 1
    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
