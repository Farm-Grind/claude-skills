# Gate 8c — Delivery Pre-Send Checks

All checks run after Gate 8b passes. Every check is a HARD FAIL — delivery stops until all pass.
Load with `view` before running. Confirm load by quoting the H1 header: `# Gate 8c — Delivery Pre-Send Checks` must appear in the response.

---

## Checks

| # | Check | Pass condition | HARD FAIL condition |
|---|-------|---------------|---------------------|
| 0 | gates_passed written to frontmatter | `gates_passed: YYYY-MM-DD` present in SKILL.md frontmatter; run the command below before packaging | Field absent after packaging command runs |
| 1 | Filesystem install confirmed | `ls /mnt/skills/user/<skill-name>/` output visible this turn | Output absent or from a prior turn |
| 2 | SKILL.md present in install path | File visible in ls output | SKILL.md missing from installed directory |
| 3 | references/ present and populated | `ls /mnt/skills/user/<skill-name>/references/` shows ≥ 1 file | Directory absent or empty |
| 4 | Validator re-run inline | Run `python3 ci/validate.py skills/<skill-name>/SKILL.md` as the first action of Gate 8c; output shows OVERALL: PASS | Stale output referenced from prior turn; any FAIL in output |
| 5 | Line count confirmed ≤ 500 | wc -l output visible; value ≤ 500 | Count exceeds 500 or output absent |
| 6 | Package succeeded | "Skill is valid!" in packaging output | Packaging output absent or contains error |
| 7 | .skill file copied to outputs | `cp` command ran; file visible at `/mnt/user-data/outputs/<skill-name>.skill` | File absent from outputs |
| 8 | Registry written and verified | D1 re-query confirmed entry present (install/update) or absent (delete) | Query result absent or contradicts expected state |
| 9 | present_files called with .skill | present_files fired in Gate 8 Step 2 this session | Tool not called — user cannot download |
| 10 | Gate 9 clean pass block present | Delivery block visible with all required fields | Block absent or incomplete |

---

## Check 0 — gates_passed Write Command

```bash
python3 -c "
import re, datetime
path = '/tmp/<skill-name>/SKILL.md'
today = datetime.datetime.utcnow().date().isoformat()
content = open(path).read()
if 'gates_passed:' in content:
    content = re.sub(r'^gates_passed:.*$', f'gates_passed: {today}', content, flags=re.MULTILINE)
else:
    content = content.replace('---\nSKILL_VERSION', f'---\ngates_passed: {today}\nSKILL_VERSION', 1)
open(path, 'w').write(content)
print('gates_passed written:', today)
"
```
Use `datetime.datetime.utcnow().date()` — CI runs on UTC; local `date.today()` fails
SGC-04 when local timezone is behind UTC at packaging time.
Re-run Gate 7 after this write. CI WARNs if absent; becomes HARD FAIL after corpus sweep.

---

## Sequence

Run checks in order 1 → 10. Stop at first HARD FAIL. Name the failed check in Gate 9 failure block.

No check may be skipped. If a step was not executed this session (e.g., registry write for a MECHANICAL fix), that is a planning error — not a skip exception.

---

## MECHANICAL Fix Exception

MECHANICAL fixes (targeted line edits with no gate sequence) still require:
- Check 4 (validator re-run inline)
- Check 5 (line count)
- Check 6 (package succeeded) — unless packaging was explicitly deferred

All other checks apply in full. "MECHANICAL" does not mean "skip delivery verification."

