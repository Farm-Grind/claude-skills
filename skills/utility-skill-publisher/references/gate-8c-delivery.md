# Gate 8c — Delivery Pre-Send Checks

All checks run after Gate 8b passes. Every check is a HARD FAIL — delivery stops until all pass.
Load with `view` before running. Confirm load with visible bash output.

---

## Checks

| # | Check | Pass condition | HARD FAIL condition |
|---|-------|---------------|---------------------|
| 1 | Filesystem install confirmed | `ls /mnt/skills/user/<skill-name>/` output visible this turn | Output absent or from a prior turn |
| 2 | SKILL.md present in install path | File visible in ls output | SKILL.md missing from installed directory |
| 3 | references/ present and populated | `ls /mnt/skills/user/<skill-name>/references/` shows ≥ 1 file | Directory absent or empty |
| 4 | Validator ran this turn | Gate 7 output visible in current response | Gate 7 output from prior turn — results stale |
| 5 | Validator exit code 0 | "OVERALL: PASS" in Gate 7 output | Any FAIL in Gate 7 output |
| 6 | Line count confirmed ≤ 500 | wc -l output visible; value ≤ 500 | Count exceeds 500 or output absent |
| 7 | Package succeeded | "Skill is valid!" in packaging output | Packaging output absent or contains error |
| 8 | .skill file copied to outputs | `cp` command ran; file visible at `/mnt/user-data/outputs/<skill-name>.skill` | File absent from outputs |
| 9 | Registry written and verified | D1 re-query confirmed entry present (install/update) or absent (delete) | Query result absent or contradicts expected state |
| 10 | present_files called with .skill | Tool called with correct path | Tool not called — user cannot download |
| 11 | Gate 9 clean pass block present | Delivery block visible with all required fields | Block absent or incomplete |

---

## Sequence

Run checks in order 1 → 11. Stop at first HARD FAIL. Name the failed check in Gate 9 failure block.

No check may be skipped. If a step was not executed this session (e.g., registry write for a MECHANICAL fix), that is a planning error — not a skip exception.

---

## MECHANICAL Fix Exception

MECHANICAL fixes (targeted line edits with no gate sequence) still require:
- Check 4 (validator ran this turn)
- Check 5 (validator pass)
- Check 6 (line count)
- Check 7 (package succeeded) — unless packaging was explicitly deferred

All other checks apply in full. "MECHANICAL" does not mean "skip delivery verification."
