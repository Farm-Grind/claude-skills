#!/usr/bin/env python3
"""
ci/check_skill_gate.py — Skill publisher gate bypass detector

Checks every modified skills/*/SKILL.md for:
  1. A current gates_passed date (F-035 STRUCTURAL fix — P-12)
  2. A SKILL_VERSION increment vs the base branch (F-036 STRUCTURAL fix — P-06)

Runs in two modes:
  pre-commit (default)  — diffs staged index vs HEAD; invoked by .githooks/pre-commit
  --ci                  — diffs HEAD of PR branch vs origin/main; invoked by GitHub Actions

Exit codes:
  0 = PASS  — all modified skill files pass all checks
  1 = FAIL  — one or more modified skill files fail a check
  2 = WARN  — no modified skill files found (gate not applicable)

Checks:
  SGC-00  gates_passed == today AND SKILL_VERSION incremented     PASS per skill
  SGC-01  no modified skill files staged/changed                  WARN (gate skipped)
  SGC-02  skill file content unreadable                           FAIL (git error)
  SGC-03  gates_passed key absent from frontmatter                FAIL
  SGC-04  gates_passed date is stale (not today)                  FAIL
  SGC-05  SKILL_VERSION not incremented vs base                   FAIL

Only fires on Modified (M) diff-filter — new skills (A) are excluded because
they go through skill-creator before skill-publisher.

Patterns: P-12 (Finding F-035), P-06 (Finding F-036)
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

TODAY = str(date.today())

SKILL_PATH_RE = re.compile(r"^skills/[^/]+/SKILL\.md$")


# ── Git helpers ───────────────────────────────────────────────────────────────

def get_modified_skill_files(ci_mode: bool) -> list[str]:
    """Return list of skills/*/SKILL.md paths modified vs base."""
    if ci_mode:
        cmd = ["git", "diff", "origin/main...HEAD", "--name-only", "--diff-filter=M"]
    else:
        cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=M"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ERROR: git diff failed: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return [p for p in r.stdout.splitlines() if SKILL_PATH_RE.match(p)]


def get_new_content(path: str, ci_mode: bool) -> str | None:
    """Return the new (post-change) content of a skill file."""
    if ci_mode:
        # In CI, checked-out files are at PR head — read from disk.
        try:
            return Path(path).read_text()
        except OSError:
            return None
    else:
        # Pre-commit: read from git index (staged content).
        r = subprocess.run(["git", "show", f":{path}"], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None


def get_base_content(path: str, ci_mode: bool) -> str | None:
    """Return the base (pre-change) content of a skill file."""
    base_ref = "origin/main" if ci_mode else "HEAD"
    r = subprocess.run(
        ["git", "show", f"{base_ref}:{path}"], capture_output=True, text=True
    )
    return r.stdout if r.returncode == 0 else None


# ── Field parsers ─────────────────────────────────────────────────────────────

def parse_gates_passed(content: str) -> str | None:
    """Extract gates_passed date from the first 50 lines."""
    for line in content.splitlines()[:50]:
        m = re.match(r"^gates_passed:\s*(\S+)", line)
        if m:
            return m.group(1)
    return None


def parse_skill_version(content: str) -> tuple[int, ...] | None:
    """Extract SKILL_VERSION as a comparable tuple, e.g. (3, 4) for 'v3.4' or '3.4'."""
    for line in content.splitlines()[:50]:
        m = re.match(r"^SKILL_VERSION:\s*v?(\S+)", line)
        if m:
            raw = m.group(1)
            try:
                return tuple(int(x) for x in raw.split("."))
            except ValueError:
                return None
    return None


# ── Gate runner ───────────────────────────────────────────────────────────────

def run_gate(ci_mode: bool) -> int:
    mode_label = "CI" if ci_mode else "pre-commit"
    paths = get_modified_skill_files(ci_mode)

    print(f"SKILL GATE  [{mode_label}]")
    print("=" * 60)

    if not paths:
        print("  SGC-01  ⚠  no modified skills/*/SKILL.md found — gate skipped")
        print("\nVERDICT: WARN (gate not applicable)")
        return 2

    failures: list[str] = []

    for path in paths:
        skill_name = path.split("/")[1]
        new_content = get_new_content(path, ci_mode)

        if new_content is None:
            print(f"  SGC-02  ✗  {skill_name}: could not read new content")
            failures.append(path)
            continue

        skill_failed = False

        # SGC-03 / SGC-04: gates_passed check
        gp = parse_gates_passed(new_content)
        if gp is None:
            print(f"  SGC-03  ✗  {skill_name}: gates_passed missing from frontmatter")
            failures.append(path)
            skill_failed = True
        elif gp != TODAY:
            print(
                f"  SGC-04  ✗  {skill_name}: gates_passed={gp} (expected {TODAY})"
                " — skill-publisher Gate 9 not run"
            )
            if path not in failures:
                failures.append(path)
            skill_failed = True

        # SGC-05: SKILL_VERSION increment check (F-036 STRUCTURAL fix)
        new_ver = parse_skill_version(new_content)
        base_content = get_base_content(path, ci_mode)

        if base_content is None:
            # No base version — new skill or untracked; skip version increment check.
            print(f"  SGC-05  ⚠  {skill_name}: no base version found — increment check skipped")
        elif new_ver is None:
            print(
                f"  SGC-05  ✗  {skill_name}: SKILL_VERSION absent in new content"
                " — skill-publisher did not run or facsimile detected"
            )
            if path not in failures:
                failures.append(path)
            skill_failed = True
        else:
            base_ver = parse_skill_version(base_content)
            if base_ver is None:
                print(
                    f"  SGC-05  ⚠  {skill_name}: SKILL_VERSION absent in base — increment check skipped"
                )
            elif new_ver <= base_ver:
                print(
                    f"  SGC-05  ✗  {skill_name}: SKILL_VERSION not incremented"
                    f" (base={'.'.join(str(x) for x in base_ver)},"
                    f" new={'.'.join(str(x) for x in new_ver)})"
                    " — skill-publisher Gate 9 not run or facsimile detected (F-036)"
                )
                if path not in failures:
                    failures.append(path)
                skill_failed = True
            else:
                print(
                    f"  SGC-05  ✓  {skill_name}: SKILL_VERSION incremented"
                    f" {'.'.join(str(x) for x in base_ver)}"
                    f" → {'.'.join(str(x) for x in new_ver)}"
                )

        if not skill_failed:
            print(f"  SGC-00  ✓  {skill_name}: gates_passed={gp}")

    if failures:
        print(
            f"\nVERDICT: FAIL ({len(failures)} skill(s) failed gate check)"
        )
        print(
            "  Each modified SKILL.md requires:\n"
            "    gates_passed updated to today (Gate 9)\n"
            "    SKILL_VERSION incremented vs base branch\n"
            "  Run the skill-publisher gate sequence, or revert direct edits to SKILL.md.\n"
            "  Facsimile invocation (P-06 / F-036): ensure SKILL.md was loaded before output."
        )
        return 1

    print(f"\nVERDICT: PASS ({len(paths)} skill(s) verified)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Skill publisher gate bypass detector"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: diff origin/main...HEAD instead of staged index vs HEAD",
    )
    args = parser.parse_args()
    sys.exit(run_gate(ci_mode=args.ci))
