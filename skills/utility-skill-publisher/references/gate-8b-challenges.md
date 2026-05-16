# Gate 8b — Adversarial Self-Review Challenges

Six challenges run before any delivery. Every FAIL blocks `present_files`.
Load this file with `view` before running any challenge. Confirm load with visible bash output.

---

## Challenge 1 — Trigger Precision

**Question:** Do the trigger conditions in the description precisely identify when this skill fires — and only then?

**Test:** Read the description's trigger list. For each trigger phrase, ask: "Could a session occur where this phrase appears but the skill is not needed?" If yes → over-broad.

**Pass:** Every trigger phrase is necessary and sufficient. No trigger fires this skill when a sibling skill handles it better.

**Fail signals:**
- Trigger phrase is a single generic word ("skill", "update")
- Trigger overlaps entirely with a sibling skill's trigger set
- Trigger is a meta-word that could appear in any session ("improve", "fix", "write")

---

## Challenge 2 — Scope Bleed

**Question:** Does this skill duplicate content that already lives in a sibling skill, user preferences, or project instructions?

**Test:** For each gate or rule in the body, ask: "Does this appear verbatim or near-verbatim in another loaded document?" If yes → duplication.

**Pass:** Every gate in this skill is absent from sibling skills. SEE ALSO references sibling coverage correctly.

**Fail signals:**
- A gate step repeats a user-preference rule already applied universally
- A domain rule in the body matches a reference file from another skill
- The skill re-implements a deterministic check already in `scripts/validate.py`

---

## Challenge 3 — Hard Fail Completeness

**Question:** Are all documented failure modes covered by a HARD FAIL condition? Are all HARD FAILs reachable — i.e., is the condition that triggers them actually possible?

**Test:** For each HARD FAIL in the body, trace back: what input produces it? Is that input possible in a real session?

**Pass:** Every HARD FAIL maps to a reachable condition. No HARD FAILs are orphaned. No documented failure mode in GOTCHAS lacks a corresponding HARD FAIL.

**Fail signals:**
- HARD FAIL condition requires a state that can never occur
- A GOTCHA entry describes a failure mode with no corresponding gate or HARD FAIL
- "HARD FAIL" label applied to a soft check (one where delivery proceeds anyway)

---

## Challenge 4 — Mechanism Survival

**Question:** Do the mechanisms described actually work when executed? Would a different Claude instance running this skill produce the same outcome?

**Test:** Pick the two most complex mechanisms in the body. Trace them step by step. At each step, ask: "Could Claude interpret this differently and still believe it passed?"

**Pass:** Each mechanism has a determinate output. Steps are imperative and unambiguous. Confirmation blocks produce visible strings Claude cannot fake.

**Fail signals:**
- A gate says "verify X" without specifying what verification looks like
- A confirmation block has fields Claude could fill with any string (no pass/fail anchors)
- A step requires Claude to "ensure" or "consider" rather than produce a named output
- Two plausible readings of a step exist and produce different behavior

---

## Challenge 5 — Overhead Check

**Question:** Do all gates change Claude's behavior? Does any gate add process without changing output?

**Test:** For each gate: "If this gate were removed, would any delivery differ?" If not → overhead.

**Pass:** Every gate produces either a visible output block or a HARD FAIL. No gate is purely advisory with no enforcement path.

**Fail signals:**
- A gate says "consider X" with no fail condition
- Two gates check the same condition (deduplication failure)
- A gate runs but its output block is never referenced downstream
- A gate was added "to be thorough" with no documented failure mode it prevents

Run only when gate changes occurred this session. Mark SKIPPED otherwise.

---

## Challenge 6 — Change Impact

**Question:** Are all changes made this session correctly classified, and do no BEHAVIORAL ADDITIONs appear without user confirmation?

**Test:** List every change made this session. Classify each as STRUCTURAL FIX or BEHAVIORAL ADDITION. For any BEHAVIORAL ADDITION, confirm user approval was explicit.

**Pass:** Every change is listed and classified. All BEHAVIORAL ADDITIONs have a confirmation record (date + user signal). No changes are unclassified.

**Fail signals:**
- A change appears in the delivery that was not discussed before execution
- A BEHAVIORAL ADDITION is listed but has no confirmation record
- A change is classified as STRUCTURAL FIX but no prior failure mode is cited
- More changes appear in the delivery block than were discussed in the session

---

## Confirmation Block Template

```
Gate 8b self-review:
  Challenge 1 — Trigger precision: [CLEAR / FAIL: reason]
  Challenge 2 — Scope bleed: [CLEAR / FAIL: reason]
  Challenge 3 — Hard fail completeness: [CLEAR / FAIL: reason]
  Challenge 4 — Mechanism survival: [CLEAR / FAIL: reason]
  Challenge 5 — Overhead check: [RAN: result / SKIPPED: no gate changes this session]
  Challenge 6 — Change impact: [all STRUCTURAL FIX / BEHAVIORAL ADDITIONs confirmed: list]
  Status: CLEAR to deliver / BLOCKED — [reason]
```
