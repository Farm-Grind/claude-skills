---
name: loop-core-error-log
description: >
  Logs, tracks, and resolves Claude output errors for The Loop. Use
  automatically — do not wait to be asked. Trigger on ANY of these signals:
  user says output is wrong or needs correction ("that's wrong", "fix this",
  "that contradicts the lore", "you used the wrong X"); code-guardian or
  lore-checker catches a violation pre-output — self-report it; a skill fires
  a warning flag (⚠); user says "log that error" or "track this"; session ends
  where any error was caught or flagged; user asks to view or export the log.
  Do NOT trigger for: logging design decisions (loop-core-decisions),
  lore questions without an error context, or general task work with no output
  failure. Load once per session.
---
SKILL_VERSION: v1.7

# The Loop — Error & Failure Log Skill

Maintains a persistent record of Claude output errors, skill failures, and
recurring problems — with root cause and prevention for each. Storage is the
source of truth. The docx is a periodic export.

**Goal:** Pattern detection, not blame. An error logged twice without a
prevention action is a process failure — escalate to skill or doc update.

---

## Storage Key & Schema

```javascript
// Notion MCP only — window.storage is NOT used on this project
// Errors page ID: 33b3a41dd33d81da8923eb6ffcf6b833
// Format: JSON in ## Data block
// Read: Notion:notion-fetch on page ID, extract ## Data JSON block
// Write: notion-update-page update_content targeting ## Data block
```

```json
{
  "id": "E-001",
  "date": "2026-03-25",
  "category": "CODE | LORE | DESIGN | OPS | SKILL",
  "status": "OPEN | RESOLVED | WONT_FIX",
  "severity": "LOW | MEDIUM | HIGH",
  "title": "Short descriptive title (≤10 words)",
  "what_happened": "Plain-English description of what Claude produced incorrectly.",
  "expected": "What the correct output should have been.",
  "root_cause": "Why Claude got it wrong — missing context, skill gap, ambiguous instruction, wrong inference, etc.",
  "fix_applied": "What was done to correct the output this session. 'N/A' if caught pre-output.",
  "prevention": "What skill, document, or instruction change would prevent this recurring. 'None identified' if unknown.",
  "skill_action": "SKILL_UPDATE | DOC_UPDATE | INSTRUCTION_CHANGE | NONE — what follow-up is needed.",
  "source": "Which skill, task, or document category this originated from."
}
```

**ID format:** `E-XXX`, zero-padded, globally sequential. Auto-increment from
highest existing ID. IDs are permanent — never reassign or reuse.

**Category inference:**
- `CODE` — wrong token, wrong library, wrong pattern, wrong component structure
- `LORE` — canon contradiction, invented answer to OPEN item, wrong terminology
- `DESIGN` — wrong color, wrong font, wrong visual direction
- `OPS` — wrong filename, wrong version, wrong process
- `SKILL` — a skill failed to trigger, triggered incorrectly, or gave bad output

**Severity:**
- `HIGH` — shipped or nearly shipped incorrect output; would have caused real
  rework; contradicts confirmed canon or stack constraints
- `MEDIUM` — caught before use; would have caused confusion or inconsistency
- `LOW` — minor, stylistic, or edge-case deviation; caught by audit

---

## Operations

**Log new error:** load → construct all fields from conversation context →
**MUST NOT write if any required field is empty** — use `"None identified"` for
`prevention` and `"Unknown — requires investigation"` for `root_cause` when
context is insufficient, but never omit or blank these fields →
push → write → **re-fetch to verify** → confirm.
`✓ Logged E-012 [OPEN | HIGH] — CODE: Hardcoded hex value in ManaBar component.`

**Mandatory re-fetch after every write (HARD FAIL — no exceptions):**
After every `Notion:notion-update-page` call to the errors page:
1. Re-fetch immediately: `Notion:notion-fetch(id: "33b3a41dd33d81da8923eb6ffcf6b833")`
2. Confirm the written entry is present — verify the E-ID exists in the ## Data JSON block
3. If mismatch: report failure explicitly, retry once, then flag entry as UNVERIFIED — never report write complete until verification passes

HARD FAIL: never report `✓ Logged E-XXX` or `✓ Resolved E-XXX` without running the re-fetch and confirming the written content. Skipping re-fetch and reporting success is a process violation.

**Resolve error:** load → find by ID or title → set `status: "RESOLVED"` →
update `prevention` if better fix now known → prepend "Resolved YYYY-MM-DD:"
to `fix_applied` → write → re-fetch to verify → confirm.
`✓ Resolved E-012 — CODE: Hardcoded hex. Prevention: code-guardian hex scan updated.`

**Mark WONT_FIX:** load → find entry → set `status: "WONT_FIX"` → add reason
to `root_cause` → write → re-fetch to verify → confirm. Use only when error is non-reproducible,
context-specific, or out of scope to prevent.
`✓ E-008 marked WONT_FIX — one-off context issue, no pattern identified.`

**Update prevention:** When a skill or document is updated in response to an
error, update `prevention` and `skill_action` on the entry to reflect what
was done.

**View / search:** load → display grouped by status (OPEN · RESOLVED · WONT_FIX)
then by severity (HIGH first). Always show OPEN HIGH items at top.

**Never blind-write** — always load → modify → write. **One entry per error
instance** — if the same error recurs, add a new entry and cross-reference the
original in `root_cause`: "Recurrence of E-012."

---

## Self-Reporting Protocol

When Claude catches its own error before the user sees it (via code-guardian
post-generation audit, lore-checker post-generation audit, or any internal
check):

1. Fix the error silently in the output (per skill rules — present clean output)
2. Log to `the-loop:errors` with `fix_applied: "Caught pre-output and corrected"`
3. Add a brief note after the output:
   `⚠ E-013 self-logged — caught hardcoded hex in ManaBar; corrected before output.`

---

## Pattern Summary

Append to every log display as a trailing section. Also fires standalone on
explicit pattern requests ("show patterns", "any recurring issues?").

```
OPEN ERRORS — REVIEW REQUIRED
──────────────────────────────
[E-XXX] [HIGH]    [title]
                  Root cause: [root_cause]
                  Prevention: [prevention]
                  Action needed: [skill_action]

RECURRING PATTERNS
──────────────────
[Category]: [N] errors — most common: [most frequent title]
```

If any category has 3+ errors, flag it explicitly as a systemic issue requiring
a skill or document update, not just individual fixes.

---

## Examples

**Example 1 - User catches a lore error**

User: "That's wrong — you called the Heart a Cult splinter group."
Error log fires immediately:

```
Logged E-007 [OPEN | HIGH] — LORE: The Heart described as Cult splinter group.
Root cause: Lore-checker did not fire on this UI copy task.
Prevention: Ensure lore-checker triggers on all NPC and faction references.
Action needed: SKILL_UPDATE
```

**Example 2 - Self-reported code violation**

Code-guardian post-gen audit catches hardcoded hex `#CCBA8E` in generated component.
Guardian fixes it silently; error-log fires after clean output is presented:

```
Logged E-008 [OPEN | LOW] — CODE: Hardcoded hex in DreamingCard component.
Root cause: Missing theme import in initial scaffold.
Fix applied: Caught pre-output — replaced with dreaming[400].
Prevention: Code-guardian hex scan — already running. No additional action.
Action needed: NONE
```
Brief note appended to output:
`E-008 self-logged — caught hardcoded hex in DreamingCard; corrected before output.`

**Example 3 - Recurring pattern flagged**

Log display shows CODE category with 4 entries. Pattern summary fires:

```
RECURRING PATTERNS
──────────────────
CODE: 4 errors — most common: Hardcoded hex value
SYSTEMIC ISSUE: 3+ CODE errors detected. Skill or document update required.
Recommended action: Audit loop-extended-code-guardian hex scan coverage.
```

---

## Out of Scope

This skill does NOT:

- Log design decisions (use `loop-core-decisions`)
- Track document versions or skill registry changes (use `loop-core-tracker`)
- Generate or fix code itself — only logs errors that other skills produced (use `loop-extended-code-guardian` for code fixes)
- Diagnose past sessions retrospectively (use `loop-core-diagnostic`)
- Make decisions about when an error is unfixable — only records the WONT_FIX status the human or skill author confirms

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-code-guardian | When post-gen audit catches a violation → log `category: CODE`. If it recurs despite guardian running → log `category: SKILL`. |
| loop-extended-lore-checker | When it catches a canon contradiction → log `category: LORE`. If it missed a violation the user caught → log `category: SKILL` for lore-checker. |
| loop-core-decisions | Errors do not go in the decisions log. If an error reveals a decision needs revisiting, log the decision change there and cross-reference: "See E-XXX." |
| loop-core-diagnostic | Retrospective scan of past conversations — different scope: log records errors as they happen; diagnostic finds patterns across sessions. |

---

## Export to DOCX

1. Load all errors from storage
2. Read `/mnt/skills/public/docx/SKILL.md`
3. Generate `the-loop_ops_error-log_v[N].docx`
4. Open items summary at top · grouped by category · sorted HIGH → MEDIUM → LOW
   · Arial font · dark header rows
5. Status badges: ⚠ OPEN · ✓ RESOLVED · — WONT_FIX
6. Each entry: ID, title, severity, status, date, category, what happened,
   expected, root cause, fix applied, prevention, skill action, source
7. Append "Recurring Patterns" section: count by category, flag any with 3+
8. Increment version from last known docx · save to `/mnt/user-data/outputs/` · present
