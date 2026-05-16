# Gate 8c — Delivery Pre-Send Check

Loaded before delivery. Five checks. All HARD FAIL. Delivery stops until all
pass.

---

## Check A — Post-Write Verification

**Run:** After Gate 8 filesystem install, before .skill packaging.

**Bash:**
```bash
ls /mnt/skills/user/<skill-name>/SKILL.md
grep "^name:" /mnt/skills/user/<skill-name>/SKILL.md
grep "^SKILL_VERSION:" /mnt/skills/user/<skill-name>/SKILL.md
grep "Type: dispatcher" /mnt/skills/user/<skill-name>/SKILL.md
ls /mnt/skills/user/<skill-name>/references/
```

**Pass condition:** Each command returns expected output. SKILL.md exists,
name matches, version present, Type: dispatcher present, references/ contains
expected files.

**HARD FAIL:** Any command returns empty or error.

---

## Check B — Optional Resource Verification

**Run:** Only if Gate 2.5 RESOURCE PLACEMENT declared scripts/ or assets/.

**Bash:**
```bash
[ -d /mnt/skills/user/<skill-name>/scripts ] && ls /mnt/skills/user/<skill-name>/scripts/
[ -d /mnt/skills/user/<skill-name>/assets ] && ls /mnt/skills/user/<skill-name>/assets/
```

**Pass condition:** Declared resources are present at install location.

**HARD FAIL:** Gate 2.5 declared a resource that's not on disk after install.

---

## Check C — Registry Write

**Run:** After filesystem install confirmed.

**Mechanism:** Project-specific. May be D1 query, Notion update, or registry
file edit. Skill-publisher does not own the registry mechanism — it produces
the registry-write block; the operator (or connected tool) executes.

**Pass condition:** Registry entry created/updated AND verification query
confirms the new entry is present.

**HARD FAIL:** Registry write fails AND retry fails. Mark registry as not
completed in Gate 9 delivery block; record intended update in fenced block
for next session.

---

## Check D — Gate 9 Block Present Before present_files

**Pass condition:** Gate 9 delivery confirmation block (Clean pass or Gate
failure format) appears in the conversation BEFORE `present_files` is
called.

**HARD FAIL:** `present_files` called without preceding Gate 9 block.

---

## Check E — present_files Called

**Pass condition:** `present_files` invoked with the .skill output path as
the primary file. Filesystem install is the primary delivery; .skill file
is the secondary delivery artifact for backup/sharing.

**HARD FAIL:** Gate 9 block produced but `present_files` not called.

---

## Output Format

After all 5 checks run:
```
Gate 8c:
  Check A — post-write verification: [PASS / FAIL: reason]
  Check B — optional resource verification: [PASS / N/A / FAIL: reason]
  Check C — registry write: [PASS / FAIL: reason]
  Check D — Gate 9 block present: [PASS / FAIL: reason]
  Check E — present_files called: [PASS / FAIL: reason]
```
