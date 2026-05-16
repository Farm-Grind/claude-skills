# Gate 8b — Adversarial Self-Review Challenges

Loaded before Gate 8b confirmation block fires. Six challenges. Each must
produce CLEAR or FAIL with named reason. The confirmation block in SKILL.md
must reflect actual challenge output, not pasted boilerplate.

---

## Challenge 1 — Trigger Precision

**Question:** Could this skill's description fire on a request it should not
handle, or fail to fire on a request it should?

**Pass condition:** 10+ paraphrase variations of legitimate trigger phrases
all match. 3+ near-miss negative phrases (adjacent domains explicitly out of
scope) all do NOT match.

**Common fail:** Description uses generic words ("help with X") that overlap
with sibling skills. Fix: name specific quoted phrases users actually say.

---

## Challenge 2 — Scope Bleed

**Question:** Does the skill body extend into territory owned by a sibling
skill?

**Pass condition:** Out of Scope section names every adjacent sibling skill
and what it owns. No body section duplicates content from a sibling.

**Common fail:** Body contains "for context" methodology that lives in
another skill. Fix: remove the duplication; cite the sibling in SEE ALSO.

---

## Challenge 3 — Hard Fail Completeness

**Question:** Is every step that can be skipped under task pressure
explicitly marked HARD FAIL?

**Pass condition:** The highest-skip-risk step (typically: classification
block, BEHAVIORAL ADDITION stop, post-write verification, delivery manifest)
has explicit HARD FAIL wording with stop-condition.

**Common fail:** A step is described as "required" without naming the
consequence of skipping. Fix: rewrite as HARD FAIL with explicit block.

---

## Challenge 4 — Mechanism Survival

**Question:** Will the enforcement mechanism actually fire in the contexts
where the failure mode occurs?

**Pass condition:** Skill is loaded (auto-trigger) in every session where
the relevant failure could happen. Enforcement is an explicit step in the
body, not an aspirational note.

**Common fail:** Rule lives in body but skill doesn't auto-load in the
context where the failure happens. Fix: adjust trigger signals OR move the
rule to a different layer (user preferences, project instructions).

---

## Challenge 5 — Overhead Check

**Question:** Does the gate added this session actually change Claude's
behavior, or is it organizational/decorative?

**Run condition:** Only when a gate is added or removed this session.
SKIPPED otherwise.

**Pass condition:** Two options:
- Option A: gate has a documented failure mode it prevents. Keep.
- Option B: gate is new; evidence is being gathered. Mark as
  PROVISIONAL — re-evaluate after 2 confirming sessions.

**Common fail:** Gate exists "for completeness" with no failure mode.
Fix: drop the gate or convert to a recommendation in SEE ALSO.

---

## Challenge 6 — Change Impact

**Question:** Is every change classified correctly per Gate 0.5 Step B?

**Pass condition:** All changes are STRUCTURAL FIX (with named failure mode)
OR all BEHAVIORAL ADDITIONs were confirmed by the user this session.

**Common fail:** A change marked STRUCTURAL FIX has no documented failure
mode in loaded materials. Fix: re-classify as BEHAVIORAL ADDITION and stop
for user confirmation.

---

## Output Format

The Gate 8b confirmation block (in skill-publisher SKILL.md) must reflect
ACTUAL challenge results, not pasted boilerplate. Each challenge produces
CLEAR or FAIL with one-line reason. Status: CLEAR to deliver / BLOCKED with
reason.
