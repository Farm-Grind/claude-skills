# utility-core-output-gate — Examples

Failure-mode examples referenced by SKILL.md Sub-check A and B gates.

## Table of Contents

- Example 1 — Factual confidence (A1)
- Example 1b — VERIFY-FIRST claim stated without search (A1)
- Example 1c — VERIFY-FIRST: current role/position (A1)
- Example 1d — STABLE-KNOWN: no search needed (A1)
- Example 2 — Evasion (A2)
- Example 3 — Position drift under pressure (A3)
- Example 4 — Unsolicited hedge (A4)
- Example 5 — Handoff format (B1)
- Example 6 — Mandatory process skipped (B4)
- Example 7 — Specification drift (B7)
- Example 8 — Constraint pre-check (B8)
- Example 9 — Scope creep (B9)
- Example 10 — Catalog completeness (B11)
- Example 11 — Search snippet treated as complete source (A1)
- Example 12 — Conditional action executed without verifying condition (A7)
- Example 13 — NEXT block collapsed into prose (B10b)
- Example 14 — Replacement content without placement instruction (B13)
- Example 15 — Handoff block delivered mid-session (B14)
- Example 16 — Half-handoff, chat block without Notion write (B16)
- Example 17 — Bloated OPEN CONTEXT (B17)
- Example 18 — Wrong-layer fix proposal in NEXT block (B18)

---


### Example 1 — Factual confidence (A1)

Situation: User asks whether a skill can be auto-installed. utility-core-skill-gate
SKILL.md with packaging automation instructions is loaded in context.

**Bad:** "Claude cannot install skills — that's a platform limitation."
A1 fails: packaging automation instructions exist in loaded context.
Fix: read the relevant section; answer from what is actually there.

---

### Example 1b — VERIFY-FIRST claim stated without search (A1)

Situation: User asks when a mobile game daily reset occurs.

**Bad:** "Daily reset is at midnight Pacific Time."
A1 fails: reset times are VERIFY-FIRST — live-service-configured, time-
sensitive, and numerically specific. No search ran before asserting.
Fix: search first. State the result with source. If inconclusive, say so.

---

### Example 1c — VERIFY-FIRST: current role/position (A1)

Situation: User asks who the current CEO of a company is.

**Bad:** "[Name] is the CEO of [Company]."
A1 fails: current roles are VERIFY-FIRST. Executive positions change.
Training data has a cutoff. No search ran.
Fix: search, then state the result. If the session's knowledge instruction
system has current date awareness, that context does not substitute for search.

---

### Example 1d — STABLE-KNOWN: no search needed (A1)

Situation: User asks what year WWII ended.

**Good:** "WWII ended in 1945."
A1 passes: this is STABLE-KNOWN — a well-established historical fact with
no ongoing dispute and no time-sensitivity. Search not required.

---

### Example 2 — Evasion (A2)

Situation: User asks why Claude got something wrong. The reason is
identifiable — Claude read a skill and did not apply it.

**Bad:** "I don't have a good explanation for why I got that wrong."
A2 fails: the explanation exists. Fix: "I read the skill and did not
retain or apply its content when answering a direct question about it."

---

### Example 3 — Position drift under pressure (A3)

Situation: Claude correctly identified a gap. User pushes back without
new evidence.

**Bad:** "You're right, it's probably fine as-is."
A3 fails: no new evidence introduced. Fix: hold the position and state why,
or ask what new information is being offered.

---

### Example 4 — Unsolicited hedge (A4)

Situation: User asks for the next task.

**Bad:** "Next task is X. Note that you may want to consider Y first."
A4 fails if Y was not asked about and does not change whether X is correct.
Fix: answer the question, stop.

---

### Example 5 — Handoff format (B1)

Situation: Session ending, user needs a handoff block.

**Bad:** "Here's your handoff — copy this: [indented block]"
B1 fails: not a fenced code block. Fix:

````
```
Resume from: skill built, next is Linear integration...
```
````

---

### Example 5b — B1 binary test failure (v1.6)

Situation: User asks for a complete replacement block for a section of the system prompt. Claude delivers:

**Bad:** "Here's the updated section — find the old version above and replace it with this:"
`[fenced block with new content]`

B1 fails: the fenced block references content outside itself ("find the old version above"). Binary test 1 fires: "as shown above" or equivalent phrase requiring the user to locate something not in the block.

**Also bad:** Claude delivers the block correctly but adds a separate note: "The block above replaces lines 45–67 of the project instructions."

B1 fails: fenced block PLUS separate note explaining where to put it. Binary test 2 fires.

**Correct:** Wrap complete replacements in structural delimiters:
```
=== COMPLETE REPLACEMENT — paste this entire block ===
[full section content here, nothing referenced externally]
=== END COMPLETE REPLACEMENT ===
```

---

### Example 6 — Mandatory process skipped (B4)

Situation: Skill written. Task transitions to "package it."

**Bad:** Delivers packaged skill without running utility-core-skill-gate.
B4 fails. Stop. Run Gates 0–8. Recheck all Sub-check B items before delivering.

---

### Example 7 — Specification drift (B7)

Situation: User asks for a complete replacement preferences block with
explicit placement instructions.

**Bad:** "Here's an updated snippet — add this to your preferences: [partial]"
B7 fails: requirement was complete replacement, not a snippet.
B1 also fails: no placement instruction.
Fix: full replacement block with "Select all, replace entirely, save."

---

### Example 8 — Constraint pre-check (B8)

Situation: Adding content to a skill near the 500-line limit.

**Bad:** Add content, hit Gate 6 at 520 lines, requiring trimming iterations.
B8 fails: line count was checkable before acting.
Fix: run `wc -l SKILL.md` before writing. Trim first if additions exceed limit.

---

### Example 9 — Scope creep (B9)

Situation: User asks to fix one formatting issue in a skill.

**Bad:** Fix the issue, also restructure two unrelated sections and add
an example.
B9 fails: only the formatting fix was in scope.
Fix: make only the requested change. Flag adjacent issues after delivery.

---

### Example 10 — Catalog completeness (B11)

Situation: User asks for all characters from a game. Search returns FAQ
results listing 10 selectable characters and a handful of named tournament
opponents. Claude writes them all and declares the task complete.

**Bad:** "OMF 2097 is now fully complete." — when 15+ tournament-only pilots
(Jahrod, Nathaniel, Marissa, Rolland, etc.) exist in the game's data files
and are findable via a primary source fetch.
B11 fails: declaration of completeness not supported by primary source read.
B7 also fails: "all characters" is a hard constraint, not an approximation.
Fix: fetch the primary source (decoded game text, wiki pilot page, or
complete roster reference). Only declare done when the source is exhausted
and no new names appear. If user names specific characters in their prompt,
those are scope signals — resolve them before calling the task complete.

---

### Example 12 — Conditional action executed without verifying condition (A7)

Situation: User asks "Are those tickets really done and the work logged
in the proper place? If so mark done."

**Bad:** Immediately calls save_issue to mark tickets Done without first
verifying whether the work is actually complete and logged correctly.
A7 fails: "if so" is a condition that must be verified before the action.
The tool call executed before the condition was confirmed.

**Fix:** First answer the question explicitly: "Yes — MAN-93 is complete.
The Atlas template and entry structure were created in Notion this session,
satisfying the acceptance criteria." Then execute the mark-done action.
The condition must be answered in the response text before the tool call.

---

### Example 11 — Search snippet treated as complete source (A1)

Situation: Task requires a complete list. Search result snippets show partial
data. Claude builds the answer from snippets and states it as complete.

**Bad:** Assert roster is complete based on what appeared in search snippets.
A1 fails: a complete roster is a numerically specific, falsifiable claim.
Snippets are previews, not sources. Fix: fetch the primary source document.
Read it fully. Cross-check against a second source when available. State
which sources were read before declaring completeness.

---

### Example 13 — NEXT block collapsed into prose (B10b)

Situation: Task just completed. Claude presents the next task inline as
a single paragraph with bold labels run together.

**Bad:**
> **NEXT:** D2 lore-checker — **CONTEXT:** Tier 2 Gate 8b delta review. **RECOMMENDATION:** Start in new session. **ACTION REQUIRED:** Confirm now or new chat.

B10b fails: fields run together on a single line. SCANNABILITY RULE
requires each labeled field on its own line with a blank line between
fields. Fix: render each field on its own line with a blank line between
labels. The schema is defined in user preferences; the format is not
optional.

---

### Example 14 — Replacement content without placement instruction (B13)

Situation: User asks for an updated preferences block. Claude delivers
a partial snippet with "add this to your preferences."

**Bad:** "Here's an updated section — add this in:" followed by a
paragraph-sized snippet.
B13 fails: partial block, no "Select all, replace entirely, save."
placement instruction. B1 also fails — not self-contained.
Fix: produce the complete preferences block in a fenced code block with
the verbatim instruction "Select all, replace entirely, save." stated
before or after the block.

---

### Example 15 — Handoff block delivered mid-session (B14)

Situation: Claude completes one task of a multi-task sprint chain.
Claude produces a handoff block anyway.

**Bad:** Handoff block appended to the response after task 1 of 4.
B14 fails: none of the session-end conditions apply — user did not say
"handoff", did not go quiet, did not ask for a new chat, and
session-monitor did not fire HANDOFF ALERT. Task 2 is the next step
in the same session.
Fix: remove the handoff block. Present the next task in NEXT-block format
and continue.

**Also allowed:** if session-monitor HAS fired HANDOFF ALERT this session
(FIX 14), handoff is required immediately — do not finish the current
task first. This is condition (4) under B14.

---

### Example 16 — Half-handoff, chat block without Notion write (B16)

Situation: Skill packaging session. Tool budget feels heavy. Claude produces
a fenced handoff block in chat with STOPPED AT / NEXT ACTION, notes
"registry update pending" in IN FLIGHT, and ends the response.

**Bad:** Chat block present, Notion write deferred, "will handle next session"
framing. User cannot distinguish this from a real handoff without auditing.
B16 fails on (a) — no Notion write this turn. B16 fails on (f) — task wasn't
complete and no session-end condition was met; handoff was a budget-pressure
reflex.

**Fix:** Either (1) commit to ending the session — execute Notion write
this turn, verify, produce matching chat block, stop. Or (2) do not
produce a handoff block — continue working, present next task in
NEXT-block format per B10b. No middle state.

The phrase "registry update pending" is the tell. If any handoff step is
pending, the handoff is not atomic — remove the block and either complete
the step or continue the session without the block.

---

### Example 17 — Bloated OPEN CONTEXT (B17)

Situation: Sprint-chain handoff. Claude writes OPEN CONTEXT with a nested
EXECUTION CONTEXT sub-block (4 file paths), a LAST VERIFIED STATE block
(4 process artifacts), a DO NOT ASSUME block (3 sprint-sequencing items),
and a THROUGHPUT RULE paragraph.

**Bad:** OPEN CONTEXT becomes 40+ lines of nested sub-blocks. User cannot
scan for the one item that actually matters next session.
B17 fails on multiple items:
- File paths exist in `/mnt/skills/user/` and `/mnt/user-data/outputs/` —
  next session can ls; fails part 1 (not conversation-only)
- Sprint ordering is in the sprint-chain handoff page body — fails part 1
- THROUGHPUT RULE is a process rule — belongs on a process reference page,
  not in a handoff
- DO NOT ASSUME items restate the sprint plan already in the handoff page

**Fix:** OPEN CONTEXT becomes 0–2 short items, each one line, each passing
both parts of the test. If there are no such items, omit the field entirely.
The reference page anti-pattern #1 is bloat. Shorter is correct when shorter
is complete.

---

### Example 18 — Wrong-layer fix proposal in NEXT block (B18)

Situation: User reports that the lore-checker skill keeps missing a specific
canon violation pattern. Claude analyzes and proposes a fix in a NEXT block.

**Bad:** Claude writes "RECOMMENDATION: Add a check in `loop-extended-lore-checker`
that catches X violation pattern." — but the actual rule belongs in the system
prompt because the same check needs to fire across `loop-extended-canon`,
`loop-dialogue-writer`, and `loop-npc-designer`. A skill-level edit will not
fire when those other skills run.

B18 fail conditions hit:
- "behavioral rule that must apply across all skills proposed as a single-skill
  edit"
- Target layer (skill) named, but rule actually lives at a higher precedence
  layer (system prompt) that would override the fix

**Fix:** Layer-verification step before delivery. State target layer as system
prompt, name the orchestration concern (rule must fire across N skills), and
either propose the system prompt edit or flag the multi-skill scope explicitly.

```
RECOMMENDATION: Add a layer-1 (system prompt) check requiring canon-violation
pattern X to be flagged before any in-world content is generated. Skill-level
edit insufficient because the check must fire in lore-checker, canon, dialogue-
writer, and npc-designer — orchestration belongs at the system prompt layer.
```

---
