---
name: utility-core-output-gate
description: >
  Runs a pre-delivery self-check against documented failure modes before any
  substantive output is finalized. Two-tier structure: Sub-check A covers the
  conditional execution gate (A7) only — universal response quality checks
  (A1-A5) have moved to system prompt Layer 1; Sub-check B fires on
  deliverables (completeness, mandatory processes, sycophancy, specification
  drift, scope creep, repeat failures, layer verification of fix proposals).
  Use automatically — do not wait to be asked. Trigger on ANY of these
  signals: a skill, document, file, or handoff is being delivered; a
  multi-step task is completing; a mandatory process is attached to the task
  type; an irreversible tool call is about to execute. Do NOT trigger for:
  explicit brainstorm/explore turns, single-word or single-fact lookups with
  no reasoning, or turns where the user is speaking and no output is
  requested. Load once per session.
---
SKILL_VERSION: v1.7

# Output Quality Gate

Applies to: all sessions. All checks are silent — do not narrate them.
If a check fails, fix before sending. Never deliver a failing version.

---

## ROUTING — Which Sub-Check Fires

| Output type | Sub-check A | Sub-check B |
|---|---|---|
| Deliverable: skill, document, file, handoff, paste block | ✓ | ✓ |
| Completion of multi-step task or mandatory process | ✓ | ✓ |
| Response containing conditional tool call | A7 only | — |

Do NOT fire for: explicit [explore]/brainstorm turns, single-word lookups,
or turns where no output from Claude is requested.


---

## SUB-CHECK A — Conditional execution gate

NOTE: A1-A5 universal response quality checks (factual confidence,
direct answer, position integrity, hedges, preference compliance) are
enforced at Layer 1 (system prompt §9 REASONING GATES — GATE A3, GATE A4,
and GATES 0-3). They no longer live here. Sub-check A covers A7 only.

Run A7 before any irreversible tool call. Binary pass/fail. Fix before
executing.

**A7 — Conditional gate check**
Before any irreversible tool call (write, status change, file modification,
API action), verify the triggering message contains no unanswered question
or unverified condition gating that action.
- Fail if: message contains "if so", "are those really", "assuming X",
  "once verified", "if that's correct" and the condition has not been
  explicitly confirmed in this response before the tool call executes
- Fail if: a question and an action appear in the same message and the
  action was executed without first stating the answer to the question
- Required: state the verified answer explicitly in the response before
  executing any conditional action. The answer must appear in the response
  text, not just be implied by proceeding.
- Referent resolution: when "that", "it", or "the result" points to output
  already produced in this conversation, deliver that output in a fenced
  block — do not reinterpret the referent as the prompt that triggered it.

---

## SUB-CHECK B — Deliverables

Run in addition to Sub-check A when output is a deliverable.

**B1 — Complete and self-contained paste**
Every actionable piece of content must be complete and structurally
self-contained — verifiable by binary test, not semantic judgment.

**Binary tests (run each mechanically before sending):**
- Fail if: the fenced block references content outside itself ("see above",
  "replace lines X–Y", "find and replace X with Y", or any phrase requiring
  the user to locate something not in the block)
- Fail if: the response contains a fenced block PLUS a separate explanatory
  note about where to put it — placement must be embedded or the block
  must be structurally self-contained as a full replacement
- Fail if: handoff prompt not in a fenced markdown code block
- Fail if: fenced block contains nested triple-backtick fences — use 4-space
  indentation for any inner code samples instead
- Fail if: raw output contains more than 2 triple-backtick delimiters when a
  single handoff or paste block is being delivered — count before sending

**Structural delimiter format for complete replacements:**
When delivering a block that fully replaces a section or file, wrap it:
```
=== COMPLETE REPLACEMENT — paste this entire block ===
[full replacement content here]
=== END COMPLETE REPLACEMENT ===
```
Use when the block must stand alone without surrounding context. Do not use
for partial additions — use str_replace or line-range instructions instead.

**B2 — No preamble before deliverable**
Deliver the artifact first. Explanation after, only if needed.
- Fail if: response opens with explanation before the requested artifact
- Fail if: file or content preceded by "Here it is" or similar framing

**B3 — Complete output, not truncated**
The deliverable must be the full artifact, not a summary or excerpt.
- Fail if: skill body abbreviated or contains "[continues...]" markers
- Fail if: document summarized rather than delivered in full

**B4 — Mandatory process compliance**
Confirm any mandatory process attached to this task type has run in full.
The enumeration of which gates apply to which task lives in the defining
skill (e.g. utility-core-skill-gate for skill work) and in system prompt
§5b — this check enforces execution, not definition.
- Fail if: task type has a mandatory process attached and any step of that
  process was skipped before delivery
- Fail if: a deliverable artifact (packaged skill, handoff block, document)
  is presented without the packaging/verification step its defining skill
  requires

**B5 — Task complete before switching**
Current task, including all attached gates and follow-up steps, must be
done before moving to a new task.
- Fail if: switching tasks while a gate, check, or required follow-up is open

**B7 — Specification drift**
Output must satisfy the literal requirement, not an approximation.
Treat every stated requirement as a hard constraint, not a target.
- Fail if: output is a "reasonable version" of what was asked rather than
  exactly what was asked
- Fail if: format, structure, or content requirement was softened, skipped,
  or reinterpreted without flagging it

**B8 — Constraint pre-check**
Before adding content to or modifying an existing artifact, check all
relevant constraints first.
- Fail if: content added to a skill or document without checking line/char
  limits first
- Fail if: change introduces a known constraint violation that was checkable
  before acting (token budget, file size, naming convention)

**B9 — Scope: only what was asked**
Deliver exactly what was requested. Do not add, modify, or remove things
not in scope.
- Fail if: response modifies content not mentioned in the request
- Fail if: advice or next steps added when the user asked for execution

**B10 — Repeat failure check**
After any user correction, the corrected behavior must hold for the rest
of the session.
- Fail if: user corrected a format failure and same format failure reappears
- Fail if: user corrected a content failure and same content failure reappears
- Fail if: user corrected a process failure and same process is skipped again

**B10b — Named block format pre-check (standing — fires before every delivery)**
These named block formats have defined schemas in their respective skills.
Before sending any response containing one of these blocks, verify format
matches the schema. This is a standing pre-check, not a repeat-failure rule —
it fires on first occurrence and every occurrence.

**SCANNABILITY RULE — applies to every named block without exception:**
Every labeled field in a named block must be on its own line, separated by a
blank line from the field above it. Fields must never be run together in a
single paragraph. Bold label, then content on the same or next line, then blank
line before the next field. A block that is correct in content but collapsed
into prose fails this check.

| Block name | Schema defined in | Key format rule |
|---|---|---|
| DECISION REQUIRED | loop-core-decisions | Each field on its own line; blank line between fields |
| Session Briefing | loop-core-tracker | Exact separator lines; each row its own line |
| NEXT task block | user preferences | Each of the 5 fields on its own line; blank line between fields |
| Handoff block | user preferences | Fenced markdown code block only — never prose |

- Fail if: any named block field runs into the next field on the same line
- Fail if: block fields are separated only by bold labels with no line breaks
- Fail if: DECISION REQUIRED block rendered as prose, inline bold, or widget
- Fail if: Session Briefing rendered as widget or missing separator lines
- Fail if: NEXT task block missing any of its five labeled fields
- Fail if: NEXT task block fields are not each on their own line with blank line separation
- Fail if: Handoff block not in a fenced markdown code block
- Fail if: any named block rendered via show_widget or create_file instead of inline markdown

**Correct NEXT block rendering:**
```
**NEXT:** [ID] [Title]

**CONTEXT:** [1–3 sentences.]

**RECOMMENDATION:** [One sentence.]

**ACTION REQUIRED:**
- [Action]

**BLOCKS:** [What is downstream.]
```

**Wrong — fails B10b:**
```
**NEXT:** MAN-94 — Title **CONTEXT:** Text here. **RECOMMENDATION:** Text. **ACTION REQUIRED:** ...
```

**B11 — Catalog/roster completeness**
When the request is "all X" (all characters, all pilots, all items, all
entries in a set), the deliverable is only complete when exhaustion is
verified — not when the most obvious sources are exhausted.
- Fail if: declared complete based on summary/FAQ sources without fetching
  the primary source (game file, wiki roster, decoded data, official list)
- Fail if: declared complete after one source without cross-checking a second
- Fail if: "all X" task declared done while named items from the user's
  own prompt remain unaccounted for (e.g. user names Jahrod and Nathaniel —
  these are scope signals, not trivia; resolve them before declaring done)
- Fail if: completion announced and then user surfaces additional items that
  were findable in sources already available
- Required: for any "all X" task, state the source(s) used and explicitly
  confirm no additional named items were found before declaring complete

**B12 — Pushback anticipation**
Before delivering any substantive output, identify the single most likely
reason a user would push back immediately after receiving it. State it
internally as a one-sentence premortem and confirm it is addressed.
- Fail if: the identified objection is valid and the output does not address it
- Fail if: no objection could be identified — this means the check was not run
- Required: the premortem must be a concrete named scenario (e.g. "user will
  ask why X was skipped"), not a generic phrase ("edge cases" or "unclear
  scope"). Generic phrases = check not run. If objection is valid, revise
  before sending; if not valid, proceed — be prepared to explain why.

**B13 — Replacement content must be complete and placed (FIX 6)**
When output is an edit to project instructions, a skill file (SKILL.md), or
user preferences — the output must be a complete replacement block with
explicit placement instructions.
- Fail if: output is a snippet without an instruction ("paste here / select all,
  replace entirely, save")
- Fail if: a partial block is delivered when the full document must be replaced
- Fail if: placement instruction is absent regardless of block length
- Required: "Select all, replace entirely, save." must appear verbatim before
  or after any full replacement block for project instructions, skills, or preferences

**B14 — Session-end condition check (FIX 3)**
Is a handoff block present in this response?
- Fail if: handoff block is present AND none of the four explicit session-end
  conditions is met:
  (1) user said "handoff", "end session", "close out", "wrap up", "I'm done"
  (2) user went quiet after final deliverable AND no open task remains in current sprint
  (3) user explicitly asked to start a new conversation
  (4) utility-core-session-monitor has fired a HANDOFF ALERT this session
      (FIX 14 — immediate handoff overrides task-completion state)
- Required: remove handoff block before delivering if no session-end condition is met
- Note: completing one task in a multi-task sequence is NOT a session-end condition
- Note: a sprint boundary (one sprint complete, next about to begin) IS a session-end
  condition per system prompt §7 FIX 9 — treat as condition (1)

**B15 — Handoff fenced block present (FIX 4)**
Was a handoff written to Notion this session?
- Fail if: a Notion handoff was written AND no fenced code block version of that
  handoff is present in this response
- Required: fenced code block must contain identical content to the Notion write —
  not a summary, not an excerpt
- Required: the fenced block must be the final element in the response — no prose after it

**B16 — Atomic handoff (FIX 15 — DIAG-001 Pattern-001)**
A handoff is atomic. It either completes every required step or produces nothing.
There is no half-handoff, no "chat block now / Notion later," no "going through the
motions." This gate fires on ANY response containing a fenced block whose first
line matches `Handoff` or containing a line starting with `STOPPED AT:`.

When this gate fires, ALL of the following must be true in THIS response turn:
- (a) A `Notion:notion-update-page` call to the correct thread's handoff page
      executed in this turn. The correct page is determined by the THREAD field
      in the block — default `sprint-chain` → page `33b3a41dd33d818188f0f5f7ea3286cb`
- (b) THREAD field is present in both the Notion write content and the chat block
- (c) Session Handoff Format Reference (`3443a41dd33d818d9e7ed2b96b88d98c`) was
      fetched in this session
- (d) loop-core-tracker SESSION CLOSE-OUT Steps A–D (or A–F if sprint chain)
      executed before the Notion write — including Linear verification for
      NEXT ACTION
- (e) NEXT ACTION text was derived from the Linear fetch in (d), not from
      conversation memory or the prior handoff OPEN CONTEXT
- (f) One of the four session-end conditions from B14 was met BEFORE the handoff
      was initiated — not constructed post-hoc to justify it

Fail conditions:
- Fail if: handoff-shaped content appears in the response and ANY of (a)–(f) is
  missing or uncertain — do not send the response; complete the missing steps first
- Fail if: the response contains the phrase "will write to Notion next" or
  "registry update pending" or any variant that defers a required handoff step
  to a future turn — handoff is atomic, nothing about it is pending
- Fail if: the response continues with additional work after the handoff block —
  handoff is the terminal response of the session
- Fail if: Claude produces a "ceremonial" handoff to mark a task boundary that
  is not a session-end — remove the block, use a NEXT-block format per B10b instead

The distinction between B16 and B14/B15:
- B14 checks that session-end was actually reached before writing
- B15 checks that a Notion write has a matching chat block
- B16 checks the whole operation is atomic — no step deferred, no step skipped,
  no partial states tolerated

**B17 — OPEN CONTEXT three-part test (FIX 15 — DIAG-001 Pattern-004)**
Before including anything under OPEN CONTEXT in a handoff, each item must pass
all three parts of the test or it is omitted:
- (1) Does this item exist ONLY in this conversation? If it is in Notion (any
      page), Linear, a skill file, the decisions log, the skill registry, the
      doc register, the checklist, a format reference page, or a persisted
      diagnostic page — it fails part 1. Omit it.
- (2) Would the next session FAIL or produce WRONG output without this specific
      item? If it is "nice to know" context, sprint ordering that is already in
      the sprint-chain page body, a throughput rule, a process rule, or a
      restatement of a skill's behavior — it fails part 2. Omit it.
- (3) Is the content of this item a behavioral rule, process rule, format
      constraint, or persistent instruction? If yes, it belongs at its proper
      architectural layer — system prompt for cross-skill rules, user
      preferences for cross-session preferences, memory for project-specific
      standing constraints, a skill file for on-demand workflows, or a format
      reference page for format schemas — NOT in OPEN CONTEXT. Fails part 3.
      See B18 for the full layer hierarchy.

All three parts must pass. Any single part failing = omit.

Fail conditions:
- Fail if: OPEN CONTEXT contains an item whose content exists in any persistent
  storage location named above
- Fail if: OPEN CONTEXT contains content that belongs at a higher architectural
  layer per the B18 layer hierarchy (system prompt, user preferences, memory,
  skill, or format reference page)
- Fail if: OPEN CONTEXT contains sub-blocks, nested headers, or multi-paragraph
  items — each item is one line, no sub-structure
- Fail if: OPEN CONTEXT contains sprint ordering or plan content when that plan
  is already in the thread's handoff page body or in a sprint-plan Notion page
- Fail if: OPEN CONTEXT length exceeds 5 items without explicit justification

The test is binary per item. "Probably useful" is a fail. If in doubt, omit.
Anti-pattern documented in Session Handoff Format Reference as failure mode #1.
**B18 — Fix proposal layer specification (parallel to loop-core-diagnostic Rule 6)**
Any fix proposal that adds, changes, or removes a behavioral rule, process, or
architectural element in a deliverable must name its target layer and verify
the rule actually lives at that layer before being presented. A fix targeting
a layer below where the rule lives cannot enforce the change — the
higher-precedence layer overrides it.

This gate fires on: "we should add a rule that...", "fix the [X] skill to...",
"change the workflow to...", proposals that introduce new gates or checks,
diagnostic Fix Blocks, and architectural recommendations in NEXT blocks. It
does NOT fire on: routine code fixes (typos, bugs, syntax), single-task
sequencing recommendations ("go with option A"), or non-rule-bearing
suggestions.

**HARD FAIL — B18:** Never deliver a response containing an in-scope fix
proposal whose target layer was not explicitly named and verified. If the
layer is uncertain, do not present the fix — flag for further analysis.

Architectural layers (highest precedence first):

| Layer | Scope |
|---|---|
| 1. System prompt | Read every turn — applies across all skills and tasks in a project |
| 2. User preferences | Read every turn — applies across all sessions and projects |
| 3. Memory | Persistent across sessions of this project |
| 4. Skill | Loaded on-demand when triggered |
| 5. Inline prompt | Single-turn instruction |

Wrong-layer signals (drawn from loop-core-diagnostic Part 6 → WL):
- Behavioral rule that must apply across all skills proposed as a single-skill edit
- Multi-skill process gap proposed as a one-skill edit
- System-prompt-level rule proposed as a skill update (system prompt overrides skill)
- One-off correction over-generalized to a permanent preference rule
- Standing project-specific constraint proposed as inline instruction

Diagnostic questions before delivery:
- At which layer does the rule actually live?
- Does the proposed fix change behavior at that layer or at a downstream one
  the higher layer overrides?
- If behavior must fire in N skills, does the fix touch the orchestration
  layer (system prompt / preferences) or just one skill?

Fail conditions:
- Fail if: fix proposal does not name its target layer explicitly
- Fail if: target layer is named but the rule actually lives at a higher
  precedence layer that would override the fix
- Fail if: behavioral rule that must apply across all skills proposed as a
  single-skill edit
- Fail if: multi-skill process gap proposed as a one-skill edit
- Fail if: one-off correction over-generalized to a permanent preference rule
- Fail if: standing constraint proposed as inline instruction
- Fail if: layer is uncertain and the fix is presented anyway — flag for
  further analysis instead, do not deliver

Required: every fix proposal in a deliverable must complete this layer-
verification check before being presented. This applies to fixes generated
by diagnostics, recommendations in NEXT blocks, architectural suggestions in
session output, and any "we should add a rule that..." proposal.

Cross-reference: loop-core-diagnostic Part 4 Rule 6 enforces the same layer
specification on diagnostic Fix Blocks. B18 enforces it on every output
deliverable across all projects — diagnostic and non-diagnostic alike.

---

## Examples

Full examples are in [references/examples.md](references/examples.md) — covers failure-mode
examples for Sub-check B and A7 (A7, B1, B4, B7–B9, B10b, B11, B13–B14,
B16–B18). Load when reviewing output that might hit one of these modes.

---

## Out of Scope
This skill does NOT:
- Catch domain-specific content errors (lore, code correctness, balance math)
- Replace utility-core-skill-gate for skill creation and editing workflows
- Log errors that reached the user (use loop-core-error-log)
- Fire on explicit [explore] or brainstorm turns with no deliverable

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| utility-core-skill-gate | Full gate protocol for skill creation and updates |
| loop-core-error-log | Post-delivery error logging when a failure reaches the user |
| loop-core-tracker | Mandatory process tracking for Loop project tasks |
