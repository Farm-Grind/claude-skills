# Gate-Sequence Worked Examples

Seven scenarios covering the full gate sequence. Load when designing or auditing a skill.

---

## Example 1 — New Single-Domain Dispatcher

**Scenario:** Creating `life-core-boxing` from scratch.

**Gate 0:** New skill → SUBSTANTIAL. Research runs: boxing training literature, session-structure best practices, at-home conditioning without equipment.

**Gate 0.5:**
- Content routing: domain knowledge (footwork, conditioning, round structure) → reference file. Routing logic → body.
- Change classification: all new content → no classification needed; BEHAVIORAL ADDITION path not triggered.

**Gate 1:** N/A — no existing skill to read.

**Gate 2:** name = `life-core-boxing` (valid). Description states what + when. Trigger phrases: "boxing session", "boxing drills", "footwork", "shadowboxing". NOT-trigger: "strength programming (life-core-fitness owns those)". Auto-trigger present. Load once per session present.

**Gate 2.5:**
- Body: routing logic and session structure only.
- references/boxing-reference.md: all technique and conditioning content.
- scripts/: none — no deterministic procedures.
- assets/: none.

**Gate 3:** All required elements present. Reference file declared. Gotchas section ≥ 2 entries. Out of Scope names `life-core-fitness`. SEE ALSO table present.

**Gate 6:** Body 160 lines — within target.

**Gate 7:** OVERALL: PASS.

**Gate 8b:** All 6 challenges CLEAR.

**Gate 9:**
```
life-core-boxing  v1.0  STAGED  (160 lines)
Changes  1: created new single-domain dispatcher
FixType  N/A — new skill
Gates    all passed
Done     written  verified  packaged  registry  present_files
Next     adversarial review required to promote to INSTALLED
```

---

## Example 2 — Gate Added to INSTALLED Skill

**Scenario:** Adding Gate 8c (delivery pre-send check) to `utility-skill-publisher`.

**Gate 0:** New gate being added → SUBSTANTIAL. Research runs: delivery verification patterns in LLM agent workflows.

**Gate 0.5:**
- Content routing: Gate 8c checks are a reusable workflow → correct home is skill body + reference file.
- Change classification: BEHAVIORAL ADDITION — new gate with documented failure mode (deliveries skipping verification). User confirms before proceeding.

**Gate 1:** Full read of existing skill body before any edit.

**Gate 7:** Re-run after edits. Line count checked.

**Gate 8b:** Challenge 6 — Gate 8c is BEHAVIORAL ADDITION; confirmation record: "user confirmed [date]".

**Gate 9:**
```
utility-skill-publisher  v3.1  INSTALLED  (487 lines)
Changes  1: added Gate 8c — delivery pre-send check
FixType  BEHAVIORAL ADDITION: confirmed by user on [date]
Gates    all passed
Done     written  verified  packaged  registry  present_files
```
Status INSTALLED because addition is additive (no workflow steps removed).

---

## Example 3 — Description Trim (MINOR)

**Scenario:** Shortening `utility-data-analyst` description from 1,043 chars to under 1,024.

**Gate 0:** No row matches → MINOR. Skip Gate 0. Proceed to Gate 0.5.

**Gate 0.5:**
- Change classification: STRUCTURAL FIX — description exceeds Gate 2 hard limit.
- No behavioral change; routing unchanged.

**Gate 1:** Read current description. Identify redundant phrases.

**Gate 7:** Re-run. Description char count verified ≤ 1,024.

**Gate 8b:** Challenge 5 — SKIPPED (no gate changes). Challenge 6 — STRUCTURAL FIX, no confirmation needed.

**Gate 9:**
```
utility-data-analyst  v2.1  INSTALLED  (479 lines)
Changes  1: trimmed description from 1043 → 998 chars
FixType  STRUCTURAL FIX: Gate 2 description char limit exceeded
Gates    all passed
Done     written  verified  packaged  registry  present_files
```

---

## Example 4 — BEHAVIORAL ADDITION Blocked

**Scenario:** Proposing to add a "tone audit" gate to `utility-extended-doc-formatting` because responses feel verbose.

**Gate 0.5:**
- Change classification: BEHAVIORAL ADDITION — no documented failure mode for tone in loaded materials. Verbosity is an observation, not a measured failure.

**Mandatory stop:**
```
BEHAVIORAL ADDITION — add tone audit gate to utility-extended-doc-formatting
Evidence: none found — verbosity observed but not measured; no failure mode documented
No documented failure mode. Proceed? [user decides]
```

User says no. Gate sequence ends. No changes made.

**Gate 9:**
```
utility-extended-doc-formatting  vX.X  FAIL
GATE 0.5  change classification — BEHAVIORAL ADDITION blocked by user
Action  no changes made; proposed gate rejected
```

---

## Example 5 — New Multi-Domain Dispatcher

**Scenario:** Creating `persona-game-designer` with domains: mechanics, economy, progression, monetization, live ops.

**Gate 0:** New skill → SUBSTANTIAL. Research runs per domain.

**Gate 0.5:** Multi-domain skill → reference file required per domain. Cross-domain-map.md required.

**Gate 2.5:**
- Body: classification table, routing logic, synthesis protocol — zero domain content.
- references/mechanics.md, economy.md, progression.md, monetization.md, live-ops.md — one per domain.
- references/cross-domain-map.md — required for multi-domain.
- scripts/: none.

**Gate 3:** Intake classification table present with Example column per domain. DOMAINS ACTIVATED block defined. Synthesis protocol present (explicit cross-domain conflict check step). Meta-adversarial review section present.

**Gate 5:** 5a–5e all checked. 5e — body has no Loop-specific names (generalization passes).

**Gate 9:**
```
persona-game-designer  v1.0  STAGED  (325 lines)
Changes  1: created new multi-domain dispatcher (5 domains)
FixType  N/A — new skill
Gates    all passed
Done     written  verified  packaged  registry  present_files
Next     adversarial review required to promote to INSTALLED
```

---

## Example 6 — Body Content Violation

**Scenario:** Editing `loop-extended-lore-checker` and discovering 80 lines of Loop-specific faction names and elemental rules embedded in the body.

**Gate 0.5:** STRUCTURAL FIX — body contains project-specific content (Gate 5e violation). Move to reference file.

**Gate 1:** Full read confirms: faction rules in body lines 120–200; body is otherwise correct.

**Fix:** Extract faction rules → `references/loop-canon-reference.md`. Body retains routing logic only.

**Gate 5e:** Re-run after extraction. "Could this body be cloned to another project by replacing references only?" → now yes. CLEAR.

**Gate 7:** Line count after extraction: 483 → 310. PASS.

**Gate 9:**
```
loop-extended-lore-checker  v2.3  INSTALLED  (310 lines)
Changes  2: extracted Loop faction rules to references/loop-canon-reference.md; removed body lines 120–200
FixType  STRUCTURAL FIX: Gate 5e body content violation — project-specific content in body
Gates    all passed
Done     written  verified  packaged  registry  present_files
```

---

## Example 7 — Resource Routed to scripts/

**Scenario:** `utility-skill-publisher` body contains 30-line inline bash block for blockquote detection, char counting, and line counting.

**Gate 0.5:** STRUCTURAL FIX — deterministic procedure (no judgment, same logic every time) embedded in body; belongs in `scripts/`.

**Gate 2.5:** Decision: extract to `scripts/validate.py`. Script stdout/stderr enters context; source never does. Body retains only: `python3 scripts/validate.py <path>` invocation line.

**Fix:** Write `scripts/validate.py` with all 6 checks. Remove 30-line bash block from body. Add script invocation and description line.

**Gate 7:** Validator is now self-applying. Run on own SKILL.md as proof of mechanism.

**Gate 9:**
```
utility-skill-publisher  v3.0  INSTALLED  (440 lines)
Changes  2: extracted validation logic to scripts/validate.py; replaced 30-line body block with 2-line invocation
FixType  STRUCTURAL FIX: Gate 2.5 resource placement — deterministic procedure belonged in scripts/
Gates    all passed
Done     written  verified  packaged  registry  present_files
```
