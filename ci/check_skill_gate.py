#!/usr/bin/env python3
"""
ci/check_skill_gate.py — Skill publisher gate bypass detector (F-035 STRUCTURAL fix)

Checks every staged modification to skills/*/SKILL.md for a current
gates_passed date in YAML frontmatter. A stale or absent date means
skill-publisher Gate 9 was not run — direct edit bypass detected.

Exit codes:
  0 = PASS  — all modified skill files have today's gates_passed date
  1 = FAIL  — one or more modified skill files have stale or missing date
  2 = WARN  — no modified skill files found (gate not applicable this commit)

Checks:
  SGC-00  gates_passed == today                         PASS per skill
  SGC-02  staged content unreadable                     FAIL (git error)
  SGC-03  gates_passed key absent from frontmatter      FAIL
  SGC-04  gates_passed date is stale                    FAIL

Only fires on Modified (M) diff-filter — new skills (A) are excluded because
they go through skill-creator before skill-publisher.

Pattern: P-12 (Context-Switch Momentum Overrides Procedural Gates)
Finding: F-035
"""

import re
import subprocess
import sys
from datetime import date

TODAY = str(date.today())

SKILL_PATH_RE = re.compile(r"^skills/[^/]+/SKILL\.md$")


def get_staged_skill_files() -> list[str]:
    """Return list of skills/*/SKILL.md paths staged as Modified."""
    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=M"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"ERROR: git diff failed: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return [p for p in r.stdout.splitlines() if SKILL_PATH_RE.match(p)]


def get_staged_content(path: str) -> str | None:
    """Return staged (index) content of a path via git show."""
    r = subprocess.run(["git", "show", f":{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def parse_gates_passed(content: str) -> str | None:
    """Extract gates_passed value from skill file header.

    gates_passed sits immediately after the closing --- of the YAML
    frontmatter block, not inside it. Search the first 50 lines.
    """
    for line in content.splitlines()[:50]:
        m = re.match(r"^gates_passed:\s*(\S+)", line)
        if m:
            return m.group(1)
    return None


def run_gate() -> int:
    paths = get_staged_skill_files()

    print("SKILL GATE")
    print("=" * 60)

    if not paths:
        print("  SGC-01  ⚠  no modified skills/*/SKILL.md staged — gate skipped")
        print("\nVERDICT: WARN (gate not applicable)")
        return 2

    failures: list[str] = []

    for path in paths:
        skill_name = path.split("/")[1]
        content = get_staged_content(path)

        if content is None:
            print(f"  SGC-02  ✗  {skill_name}: could not read staged content")
            failures.append(path)
            continue

        gp = parse_gates_passed(content)

        if gp is None:
            print(f"  SGC-03  ✗  {skill_name}: gates_passed missing from frontmatter")
            failures.append(path)
        elif gp != TODAY:
            print(
                f"  SGC-04  ✗  {skill_name}: gates_passed={gp} (expected {TODAY})"
                " — skill-publisher Gate 9 not run"
            )
            failures.append(path)
        else:
            print(f"  SGC-00  ✓  {skill_name}: gates_passed={gp}")

    if failures:
        print(
            f"\nVERDICT: FAIL ({len(failures)} skill(s) modified without skill-publisher)"
        )
        print(
            "  Each modified SKILL.md requires gates_passed updated to today by Gate 9.\n"
            "  Run the skill-publisher gate sequence, or revert direct edits to SKILL.md."
        )
        return 1

    print(f"\nVERDICT: PASS ({len(paths)} skill(s) verified)")
    return 0


if __name__ == "__main__":
    sys.exit(run_gate())
