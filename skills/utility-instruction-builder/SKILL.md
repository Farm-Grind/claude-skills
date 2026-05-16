---
name: utility-instruction-builder
description: >
  Fires on any proposed addition, update, or removal to user preferences
  or project instructions. Runs root-cause classification, 5-test filter,
  budget check, conflict check, format gate, and self-application check
  before producing a complete ready-to-paste replacement block with
  LAST_UPDATE header. Use automatically — do not wait to be asked.
  Trigger on ANY of these signals: "add this to instructions", "update
  my preferences", "add a rule", "I want Claude to always/never", "this
  keeps happening", "fix this in the instructions", "update project
  instructions", any session where a recurring failure is followed by
  discussion of prevention. Also triggers on removal audit: "prune my
  instructions", "audit my preferences", "too many rules", "clean up
  instructions", "instructions feel bloated". Do NOT trigger for: skill
  or knowledge base updates (use utility-skill-publisher), one-time
  in-session prompts, or in-session corrections not requiring a standing
  rule. Load once per session.
---
SKILL_VERSION: v1.0

# Instruction Builder — Update and Maintenance Gate

Governs every proposed change to user preferences and project instructions.
Prevents the additive spiral (T-03) that causes compliance collapse at scale.
Every update passes all parts before a delivery block is produced.

Type: encoded-preference

---

## GOTCHAS

Failure modes Claude exhibits without this skill.

1. **Symptom-only fix** — Rule addresses surface behavior; the producing
   mechanism lives in a different layer. HARD FAIL: CLASSIFICATION BLOCK
   must be visible before any instruction text is written.

2. **Negative priming** — "Never X" for naturally-occurring behavior. Naming
   the prohibited behavior activates it at 87.5% violation rate (arXiv
   2601.08070). Commission reframe required; BEHAVIORAL ADDITION block fires.

3. **Same-session self-violation** — Rule delivered in a way that itself
   violates the rule being added. Documented: partial-paste rule delivered
   as a partial paste (2026-03-31). HARD FAIL: self-application check runs
   before generating any delivery block.

4. **Silent classification** — Part 1 runs internally with no visible output;
   skipped under task pressure. HARD FAIL: CLASSIFICATION BLOCK required
   before any instruction text is written.

5. **BEHAVIORAL ADDITION without confirmation** — Adding a rule with no
   documented failure mode measurably harms task performance (arXiv
   2601.22047). HARD STOP: explicit user confirmation required.

6. **Capacity blind** — Adds without checking constraint count, lines, and
   token estimate. HARD FAIL: Part 4 budget block produced before
   CLASSIFICATION BLOCK.

7. **Discovery test treated as permanent** — Claude defaults change with model
   updates; a rule redundant today may be necessary after an update (arXiv
   2604.27789). Re-evaluate on model version changes.

8. **Missing LAST_UPDATE header** — Instructions without a version header
   make behavioral drift undetectable across sessions. Required on every
   delivery block.

---

## PART 0 — DESTINATION GATE

Run first. State destination explicitly before proceeding.

| Signal | Route |
|---|---|
| Behavioral/format rule for every conversation | User preferences |
| Behavioral/format rule for one project only | Project instructions |
| Applies to both | Both — produce separate delivery blocks |
| Procedure, schema, template, conditional logic, examples | STOP → utility-skill-publisher |
| Reference data, spec, design doc | STOP → knowledge base |
| One-time in-session instruction | STOP → inline prompt; no standing rule needed |
| "prune / audit / clean up / too many rules / feel bloated" | REMOVAL AUDIT PATH → run Parts 4, 5, 7 on all existing rules; skip Parts 1–3 |

---

## PART 1 — CLASSIFICATION BLOCK

HARD FAIL: produce this block before any instruction text is written. No exceptions.

```
CLASSIFICATION BLOCK — [proposed rule topic]
Failure observed:   [describe the behavior]
Recurrence:         [N occurrences / single — triggers BEHAVIORAL ADDITION]

Root cause:
  WRONG LAYER:           Mechanism in a skill or KB; rule would address
                         output not source.
  STRUCTURAL:            Behavioral text has failed or would predictably fail;
                         fix must change what is mechanically possible.
  BEHAVIORAL OK:         Judgment-requiring constraint genuinely absent.
  TEMPORAL:              Decays under session depth; omission framing fails
                         past ~turn 10; commission reframe required.
  NATURALLY-OCCURRING:   Model produces this naturally; prohibiting rule
                         primes the behavior (load references/instruction-
                         bloat-patterns.md to check against known patterns).

Classification:     [WRONG LAYER / STRUCTURAL / BEHAVIORAL OK /
                     TEMPORAL / NATURALLY-OCCURRING]

Mechanism survival: Would this fix fail where the original failure occurred?
                    [yes — wrong layer / no — survives in context]

Symptom/mechanism:  [SYMPTOM: states desired behavior without addressing why
                     it doesn't occur / MECHANISM: changes what is possible]

If BEHAVIORAL OK + MECHANISM → continue to Part 2
If WRONG LAYER / STRUCTURAL / NATURALLY-OCCURRING → STOP
  Present structural fix recommendation instead of writing instruction text.
```

### BEHAVIORAL ADDITION block

Fires on single-occurrence OR naturally-occurring classification.
HARD STOP: no instruction text written until user responds affirmatively.

```
BEHAVIORAL ADDITION — [rule description]
Evidence:    [session evidence / none found]
Basis:       [SINGLE OCCURRENCE (N=1) / NATURALLY-OCCURRING — frequency:
              high / medium / low]
Cost:        confirmed attention-budget penalty (arXiv 2601.22047)
Proceed?     Explicit user confirmation required before writing any text.
```

---

## PART 2 — 5-TEST FILTER

Applies to every proposed instruction line. Any test fails → do not add.

```
5-TEST FILTER — [proposed rule]
1. TOOLCHAIN:   Can a structural mechanism (visible block, schema, gate in a
                skill) enforce this instead? → omit
2. DUPLICATION: Exists in user prefs, project instructions, or an installed
                skill? → omit (one canonical home per rule)
3. DISCOVERY:   Would Claude do this correctly without it? Adding it actively
                harms performance if yes (arXiv 2601.22047). → omit
                Note: session-current only; re-evaluate on model updates.
4. NECESSITY:   Would wrong behavior occur without this? → omit if no
5. CONFLICT:    Can this create tension with any existing instruction?
                → consolidate or reject

Result: [PASS / FAIL — which test — action]
```

---

## PART 3 — FORMAT GATE

```
FORMAT GATE — [proposed rule]
Framing:        [COMMISSION: "always do X" / OMISSION: "never do Y"]
  If OMISSION:  Is this naturally-occurring behavior?
                → Yes: reframe as commission or accept probabilistic compliance
                → Commission reframe: [state it]
Counter-intuitive: [yes / no]
  → If yes: WHY required inline. Draft: "[rule]. WHY: [reason]."
Format match:   [consistent with surrounding instructions / mixed — fix before
                 adding; no mixed prose-and-lists in the same instruction set]
Position:
  → Behavioral constraint: front section (top 3–5 rules, primacy position)
  → Format requirement: end section (recency position)
  → Middle placement: >30% accuracy drop for judgment-requiring content
    (Liu et al. 2024) — avoid; restructure to front or end
```

---

## PART 4 — BUDGET CHECK

HARD FAIL: produce this block before the CLASSIFICATION BLOCK.

```
BUDGET CHECK — [target layer]
Constraint count:  [N] behavioral rules  (target ≤8; ceiling ≤15)
Line count:        [N] lines             (target ≤100; hard stop ≤150)
Token estimate:    ~[N×8] tokens         (sweet spot ≤800; absolute ≤1,200)
Current header:    [LAST_UPDATE: date | summary  OR  UNVERSIONED]
Status:            [within target / approaching / AT CEILING]

AT CEILING: a rule must be removed or consolidated before the new rule
  is written. No exceptions.
  Removal candidates: [rules that are redundant, stale, single-occurrence
                       additions that never recurred, or restate defaults]

UNVERSIONED: add LAST_UPDATE header as first action in the delivery block.
```

---

## PART 5 — CONFLICT CHECK

```
CONFLICT CHECK
Existing instructions reviewed: [N]
Conflicts: [none / conflict with "[existing rule]" — resolution: consolidate / reject]
Sovereignty note: instructions beat skills on conflict; skills beat task prompts.
```

---

## PART 6 — DELIVERY

### Self-application check

HARD FAIL: run this before generating the delivery block.

```
Self-application check:
  Rule being added requires:          [list behavioral requirements]
  Delivery is a complete block:       [yes / no — HARD FAIL]
  Explicit placement instructions:    [yes / no — HARD FAIL]
  No snippet without context:         [yes / no — HARD FAIL]
  Delivery does not violate the rule: [yes / no — HARD FAIL]
```

### Required delivery format

1. Complete fenced code block — entire instruction set, not just the addition
2. Explicit instruction line before the block:
   "Replace all content of [Settings → Profile → User Preferences /
   project instructions] with this block."
3. `LAST_UPDATE: YYYY-MM-DD | [one-line summary of what changed and why]`
   on the very first line of the block — before any section headers
4. One-sentence delivery note outside the block: what changed and the
   failure mode it addresses

### Delivery manifest

Required before presenting the delivery block. HARD FAIL if not CLEAR.

```
INSTRUCTION UPDATE MANIFEST — [rule topic]
  Part 0  Destination:        [user prefs / project instructions / both]
  Part 4  Budget check:       [N constraints] [N lines] [~N tokens]
  Part 1  Classification:     [root cause] [SYMPTOM / MECHANISM]
  Part 2  5-test filter:      [PASS / FAIL: which test]
  Part 3  Format gate:        [COMMISSION / OMISSION] [position: front / end]
  Part 5  Conflict check:     [none / conflict + resolution]
  Part 6  Self-application:   [PASS / FAIL: reason]
  LAST_UPDATE set:            [yes / no — add header if no]
  Overall: CLEAR / BLOCKED — [reason]
```

---

## PART 7 — POST-UPDATE REGRESSION CHECK

Runs when this skill is loaded in any session after an instruction update was
applied. Trigger: `LAST_UPDATE` header is present in the loaded instructions
with a date more recent than the current session. Also runs explicitly on the
REMOVAL AUDIT PATH (Part 0) and when the user asks "is that rule working?" or
"check if the last instruction change held."

This is not an autonomous session-start check — it requires either this skill
to be loaded (via an instruction-update signal) or an explicit user request.
The LAST_UPDATE header makes the check easy to run when invoked; it does not
run silently on its own.

```
REGRESSION CHECK — [rule topic from LAST_UPDATE]
Rule added:        [summary from LAST_UPDATE header]
Date applied:      [from LAST_UPDATE header]
Target behavior:   [what the rule was meant to change]
Observed:          [behavior has not recurred / behavior recurred — describe]

If recurred:
  ESCALATE — behavioral text is not addressing root cause.
  Do NOT re-state or strengthen the rule — this has already failed once.
  Required action: present structural fix options before any action.
```

---

## ONE-TIME BOOTSTRAP

When this skill is first used, if the target instruction layer has no
LAST_UPDATE header, add one before any other change:

```
LAST_UPDATE: YYYY-MM-DD | Initial version header — no rule changes this update
```

Use today's date. This is the baseline for all future regression checks.

---

## Examples

**Example 1 — Correct addition, user preferences.**
User reports: "Claude keeps adding preamble even though I've said not to."
Part 4: 7 constraints, 89 lines — within target. LAST_UPDATE: UNVERSIONED.
Part 1 CLASSIFICATION BLOCK: failure observed multiple times; BEHAVIORAL OK;
  MECHANISM (preamble behavior is learnable via instruction).
Part 2: passes all 5 tests — not a default Claude behavior; causes wrong output
  without the rule; no duplication found.
Part 3: OMISSION framing → commission reframe: "Lead every response with the
  direct answer." Position: front section.
Part 5: no conflict.
Part 6: self-application passes; full replacement block produced with LAST_UPDATE
  header and explicit replacement instruction.
Delivery note: Added commission-framed no-preamble rule; addresses repeated
  preamble behavior documented across N sessions.

**Example 2 — BEHAVIORAL ADDITION blocked.**
User requests: "Add a rule that Claude should double-check its logic."
Part 4: runs, 8 constraints — at target ceiling.
Part 1 CLASSIFICATION BLOCK: single occurrence; NATURALLY-OCCURRING (Claude
  already reasons through tasks).
BEHAVIORAL ADDITION block fires:
  Evidence: none — no documented failure of Claude skipping logic checks.
  Basis: NATURALLY-OCCURRING + adds self-evident constraint.
  Cost: arXiv 2601.22047 confirmed harm.
  Proceed? → Stop. Awaiting user confirmation.
If user declines: discard. If user confirms: proceed; flag as BEHAVIORAL ADDITION
  in manifest.

**Example 3 — Removal audit path.**
User says: "My preferences are getting long, help me prune them."
Part 0: REMOVAL AUDIT PATH → Parts 4, 5, 7 only.
Part 4: 14 constraints, 148 lines — AT CEILING; enumerate all rules.
Part 7 regression check on each rule: 3 rules identified as never-recurred
  single-occurrence additions; 1 rule identified as Discovery test fail
  (Claude already does this); 1 rule duplicates a skill trigger condition.
Part 5: 1 conflict between two rules identified — consolidate into one.
Delivery: complete replacement block with 9 fewer lines, LAST_UPDATE updated.

---

## Out of Scope

This skill does NOT:
- Update skills or knowledge base documents (use utility-skill-publisher)
- Diagnose root causes of Claude failures across sessions (use utility-issue-triage)
- Write initial project instructions from scratch (use utility-ops-scaffolder)
- Govern output format for deliverables (rules live in user prefs; this skill
  ensures they are correctly placed and formatted when added)

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| utility-skill-publisher | Skill creation and update — different target layer |
| utility-issue-triage | Diagnosing session failures before deciding to update instructions |
| utility-ops-scaffolder | Writing initial project instructions from scratch |
| references/instruction-bloat-patterns.md | Catalog of patterns that fail the 5-test filter — load when BEHAVIORAL ADDITION or NATURALLY-OCCURRING fires |
| MOSAIC — arXiv 2601.18554 | Constraint count compliance thresholds |
| IFScale — arXiv 2507.11538 | Constraint count decay zones |
| IBM Instruction Boosting — arXiv 2510.14842 | Conflict-as-mechanism explanation |
| Negative priming — arXiv 2601.08070 | 87.5% priming failure rate for prohibition rules |
| Paradoxical interference — arXiv 2601.22047 | Self-evident constraints harm performance |
| Constraint decay — arXiv 2604.20911 | Omission framing decays 73%→33% by turn 16 |
| Prompt defect taxonomy — arXiv 2509.14404 | Six dimensions of instruction defects |
| Model drift governance — arXiv 2604.27789 | Discovery test is model-version-specific |
