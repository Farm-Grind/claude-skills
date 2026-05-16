#!/usr/bin/env python3
"""
Corpus ceiling enforcer.

Reads ci/corpus-ceiling.txt and verifies:
  - Total skill count <= MAX_SKILLS
  - Total SKILL.md line count <= MAX_TOTAL_SKILL_LINES

corpus-ceiling.txt format (user-owned; CI never edits it):
  MAX_SKILLS=34
  MAX_TOTAL_SKILL_LINES=9002

Exit code 0 if within ceiling, 1 otherwise.
"""

import sys
from pathlib import Path


def load_ceiling(ceiling_path: Path) -> dict:
    ceiling = {}
    for line in ceiling_path.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            ceiling[k.strip()] = int(v.strip())
    return ceiling


def main() -> int:
    ceiling_path = Path("ci/corpus-ceiling.txt")
    if not ceiling_path.exists():
        print("FAIL — ci/corpus-ceiling.txt not found. Create it with MAX_SKILLS and MAX_TOTAL_SKILL_LINES.")
        return 1

    ceiling = load_ceiling(ceiling_path)
    max_skills = ceiling.get("MAX_SKILLS")
    max_lines = ceiling.get("MAX_TOTAL_SKILL_LINES")

    if max_skills is None or max_lines is None:
        print("FAIL — corpus-ceiling.txt missing MAX_SKILLS or MAX_TOTAL_SKILL_LINES.")
        return 1

    skill_files = list(Path("skills").glob("*/SKILL.md"))
    skill_count = len(skill_files)
    total_lines = sum(sum(1 for _ in f.open()) for f in skill_files)

    fails = 0
    print("CORPUS CEILING CHECK")
    print("-" * 40)
    print(f"  Skill count:  {skill_count} / {max_skills}")
    print(f"  Total lines:  {total_lines} / {max_lines}")

    if skill_count > max_skills:
        print(f"  FAIL — skill count exceeds ceiling ({skill_count} > {max_skills})")
        fails += 1
    if total_lines > max_lines:
        print(f"  FAIL — total lines exceed ceiling ({total_lines} > {max_lines})")
        fails += 1

    print("-" * 40)
    if fails:
        print(f"OVERALL: FAIL ({fails} ceiling(s) exceeded)")
        return 1
    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
