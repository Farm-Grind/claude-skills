# Instruction Bloat Patterns

Catalog of common instruction additions that fail the 5-test filter.
Load when Part 1 fires BEHAVIORAL ADDITION or NATURALLY-OCCURRING.
Each pattern: name, failure mode, what it looks like, which test it fails.

---

## Category 1 — Default Restatement (Discovery Test fail)

Rules that restate behavior Claude already produces without being told.
Adding them actively harms performance by diverting attention from task
execution to constraint-checking (arXiv 2601.22047).

| Pattern | What it looks like | Fails |
|---|---|---|
| Generic quality check | "Double-check your work before responding" | Discovery — Claude already reasons iteratively |
| Accuracy instruction | "Always be accurate and avoid errors" | Discovery — accuracy is a baseline model objective |
| Helpfulness reminder | "Try to be as helpful as possible" | Discovery — restates training objective |
| Source citation default | "Cite your sources when using facts" (for a user who never asks for citations) | Discovery — Claude cites when relevant by default |
| Clarity instruction | "Write clearly and concisely" (without a specific format failure to address) | Discovery — default behavior unless instructed otherwise |

**Detection:** If you cannot name a specific session where this behavior failed,
it is likely a Discovery test fail. Do not add.

---

## Category 2 — Naturally-Occurring Prohibition (Negative Priming)

Rules that say "never X" for behaviors the model produces naturally.
Naming the forbidden behavior activates it at 87.5% violation rate (arXiv 2601.08070).

| Pattern | What it looks like | Risk level |
|---|---|---|
| Sycophancy prohibition | "Never validate my ideas — always challenge them" | High — model is trained toward validation; priming severe |
| Preamble prohibition | "Never start with 'Certainly!' or 'Great question!'" | Medium — listing the phrases names them |
| Hedging prohibition | "Never use filler phrases like 'I think' or 'it seems'" | Medium — enumerating hedges activates them |
| Apology prohibition | "Never apologize unnecessarily" | Low — less naturally-occurring, lower priming risk |

**Commission reframe examples:**
- "Never validate" → "Challenge every stated position with the strongest counter-argument first."
- "Never start with 'Certainly!'" → "Lead every response with the direct answer."
- "Never use filler phrases" → "State every claim directly without qualifiers unless uncertainty is material."

---

## Category 3 — Single-Session Bandage (Necessity test fail)

Rules added after one failure that has not recurred. High noise-to-signal ratio.
Most single-failure events do not reflect a systematic gap; they reflect
task-switching context loss or an unusual session condition.

**Detection questions:**
1. Has this happened more than once across different session types?
2. Can you name two specific sessions where the failure occurred?
3. If yes to both → may be necessary. If no → defer; watch for recurrence.

**Common single-bandage patterns:**
- Rules added mid-session immediately after a failure (high emotion, low signal)
- Rules that address a failure that occurred only in long or heavily multi-tasked sessions
- Rules addressing a failure that the task sequencing rule already covers in principle

---

## Category 4 — Wrong-Layer Content (Toolchain / Duplication test fail)

Content that belongs in a skill or knowledge base, not in instructions.
Loading it in instructions consumes per-turn budget for every conversation,
not just the conversations where it's relevant.

| Content type | Correct home | Why wrong in instructions |
|---|---|---|
| Procedural workflow ("When doing X, first do A, then B, then C") | Skill | Triggered on demand; not needed every turn |
| Output schema or template | Skill | Loaded when producing that output type |
| Conditional decision tree | Skill | Loads only when the condition is relevant |
| Domain-specific reference data | Knowledge base | Queried per topic; never needs full-turn load |
| Tool-specific API details ("Use update_content not replace_content for Notion") | Skill | Brittle in instructions; changes with the tool |

**Detection:** "Does this instruction only matter in specific task types?"
If yes → skill. "Does this instruction reference a specific tool, API, or
version?" → skill (F-006: tool-API coupling in instructions breaks on updates).

---

## Category 5 — Emphasis Inflation (Format / Structure failure)

Instructions lose signal when too many rules are marked CRITICAL, YOU MUST,
IMPORTANT, or similar. Diminishing returns begin at 2 such markers; beyond 3,
no rule is privileged.

**Diagnostic:** Count CRITICAL/MUST/IMPORTANT occurrences in the instruction set.
- 0–1: acceptable
- 2: limit reached — do not add more
- 3+: inflation present — audit which rules genuinely require emphasis;
  demote the rest to standard formatting

**Fix:** Reserve emphasis language for rules where violation would be
catastrophic (irreversible action, security concern, direct user harm).
Everything else runs without emphasis or is better placed in a skill gate.

---

## Category 6 — Cascade Conditions (Conflict test fail)

Rules with multiple conditions stacked on one directive. Each additional
condition increases the probability of conflict with other rules.

**Pattern:** "If A, and B is true, and C applies, then do X unless Y."
**Problem:** The intersection of A+B+C is rarely tested; the exceptions
create unpredictable behavior when only some conditions are met.

**Fix:** Decompose into separate, orthogonal rules. If they cannot be
decomposed without overlapping, the underlying policy is too complex for
instruction text — it belongs in a skill with examples.

---

## Category 7 — Safety Ceremony (Necessity test fail)

Rules that exist to signal thoroughness rather than change behavior.
Common in instruction sets that have grown through repeated diagnostic cycles.

**Recognition:**
- The rule describes an ideal outcome ("Ensure recommendations are comprehensive")
  rather than a specific behavioral constraint
- Removing the rule would not change any specific output in any specific session
- The rule duplicates a constraint already enforced by a skill gate

**Test:** "What specific output would change if this rule were absent?"
If the answer is vague or requires imagining an unusual scenario → remove.
