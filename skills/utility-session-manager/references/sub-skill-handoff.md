# @handoff — Handoff Generator & Writer

**Purpose:** Collect handoff content, validate, gate, write to D1, verify.
Supports PROJECT mode (full config from D1) and GENERAL mode (inline schema,
claude-config DB). Workstream-keyed storage prevents concurrent session collisions.

**Trigger:** Session end, "save handoff", "close out", "wrap up". Also called
by @monitor when HANDOFF ALERT fires.

---

## Step 0 — DB and Mode Routing

```
IF project_id is set AND session_config exists for project_id:
  mode    = PROJECT
  db      = project DB (look up key 'session_manager_db_[project_id]' in secrets;
             if absent, use the-loop-storage as default for loop-v2)
  schema  = session_config WHERE config_type='session_manager_handoff_schema_[project_id]'
  gates   = session_config WHERE config_type='session_manager_gates_*_[project_id]'

ELSE:
  mode    = GENERAL
  db      = claude-config (afd78e0e-583e-4e78-87fc-dd6bc8150ce9)
  schema  = GENERAL_SCHEMA (inline — Part 1 below)
  gates   = HANDOFF_CONTENT_GATE only
```

---

## Part 1 — GENERAL Schema (inline, no D1 lookup)

```
RENAME_BLOCK| required | format: [WORKSTREAM] · [YYYY-MM-DD] · [plain-English session topic 5-10 words]
             |          | placed before HANDOFF line between ─── separator lines (see Step 7 template)
             |          | no S[N] or TASK_ID — not applicable to GENERAL mode
SUMMARY     | required | 1-sentence plain English — what this session did and what comes next.
             |          | No F-XX/P-XX codes. Appears before NEXT in the user-pasteable block.
WORKSTREAM  | required | prompt if absent: "What's the workstream name for this session?"
STOPPED_AT  | required | min 2 sentences — what is done, what is not
IN_FLIGHT   | required | task in progress or "None"
NEXT_ACTION | required | specific and actionable — the single first step to take
OPEN_CONTEXT| optional | facts that live only in this conversation; "None" if nothing passes
DB          | required | carry-forward DB section — IDs, PAT retrieval key, repo path
             |          | format: see Step 7 template; "None" if no DB or repo used this session
```

---

## Part 2 — Workstream Key Derivation

Run before any D1 read or write. The key is the stable identifier for this
workstream's storage row across all sessions.

```
IF WORKSTREAM field is known (from handoff content or session context):
  key = workstream.lower()
            .replace(' ', '-')
            .replace('/', '-')
            .strip('-')[:50]
  Examples:
    "Loop v2 Sprint 4 — Sequencer rebuild" → "loop-v2-sprint4-sequencer-rebuild"
    "Session manager skill retirement"     → "session-manager-skill-retirement"

ELSE IF project_id is set:
  key = "[project_id]-current"   (e.g., "loop-v2-current")

ELSE:
  ASK: "What should this workstream be called? (used as the persistent key)"
  key = user_answer.lower()[:50]
```

**Key stability rule:** Once a workstream key is written, it must not change
across sessions — the key IS the workstream identity. If the user renames a
workstream, archive the old key first.

---

## Part 3 — Logic

**Step 1: Validate required fields**
For each required field in schema: if empty → ERROR. No write proceeds.

**Step 2: Run gates (order matters)**
PROJECT mode: RENAME_BLOCK_GATE → HANDOFF_CONTENT_GATE P1 → write → P2 → P3
GENERAL mode: RENAME_BLOCK_GATE (WARN) → DB_BLOCK_GATE (WARN) → HANDOFF_CONTENT_GATE P1 → write → P2 → P3

**Step 3: Read current row + capture version**
```sql
SELECT version, updated_at FROM session_handoff WHERE key = [workstream_key]
```
If no row: first handoff for this workstream → INSERT path.
If row found: captured_version = version → UPDATE path.

**Step 4: HANDOFF_CONTENT_GATE P1 (before write)**
```
[HANDOFF_CONTENT_GATE P1]
workstream:   [value]
stopped_at:   [first 80 chars]
in_flight:    [value]
next_action:  [first 80 chars]
key:          [workstream_key]
db_mode:      [PROJECT / GENERAL]
path:         [INSERT (new) / UPDATE version=[N]]
```
HARD FAIL if this block is absent before any write executes.

**Step 5: Write to D1 with optimistic locking**

First handoff (INSERT):
```sql
INSERT INTO session_handoff
  (key, workstream, project_id, content, stopped_at, next_action, version)
VALUES ([key], [workstream], [project_id], [content], [stopped_at], [next_action], 1)
```

Subsequent handoffs (UPDATE with version check):
```sql
UPDATE session_handoff
SET content=[content], stopped_at=[stopped_at], next_action=[next_action],
    version=version+1, updated_at=datetime('now')
WHERE key=[workstream_key] AND version=[captured_version]
```
If changes=0 → CONCURRENT_WRITE_GATE fires. Never auto-proceed.

**Step 5b: Update CURRENT alias (PROJECT mode only)**

After a successful workstream key write (changes=1), update CURRENT as a
convenience pointer so briefing and INTAKE CLASSIFICATION can find the latest
state without knowing the workstream key.

```sql
-- If CURRENT row exists:
UPDATE session_handoff
SET content=[content], updated_at=datetime('now')
WHERE key='CURRENT'

-- If no CURRENT row:
INSERT INTO session_handoff (key, content, updated_at, version)
VALUES ('CURRENT', [content], datetime('now'), 0)
```

No optimistic lock on CURRENT — it is a convenience alias only. Last writer
wins is acceptable; workstream keys hold the isolated, versioned records.
No re-fetch required for CURRENT.

GENERAL mode: skip this step — no CURRENT key pattern in claude-config.

**Step 6: Re-fetch and verify (mandatory)**
```sql
SELECT content, version, updated_at FROM session_handoff WHERE key=[workstream_key]
```
Compare all fields. Confirm version = captured_version + 1.

**Step 7: Output**

The user-pasteable handoff block must follow this template exactly (field order
is mandatory; SUMMARY appears first, before NEXT):

```
**SUMMARY:** [1-sentence plain English — what this session did and what comes next. No codes.]

**NEXT:** [Plain-English task title — key noun or verb first, max 10 words] [(ticket ID if applicable)]

**CONTEXT:** [1–3 sentences — precedent, stakes, what depends on it]

**RECOMMENDATION:** [Why this matters — what breaks or degrades if not done. One sentence.]

**ACTION REQUIRED:**
  • [Specific action]

**BLOCKS:** [What cannot proceed until this is resolved. Omit if nothing downstream.]
```

PROJECT mode (full output with rename block):
```
RENAME BLOCK
────────────────────────────────────────
[WORKSTREAM] · S[N] · [TASK_ID]
────────────────────────────────────────
HANDOFF — [date]
WORKSTREAM: [value]
STOPPED AT: [text]
IN FLIGHT: [task or None]
NEXT ACTION: [step]
OPEN CONTEXT: [constraints or None]
LAST SYNCED: [tables + datetime]

✓ Stored — [db] / key=[key] / v[N]
```

GENERAL mode (stored block):
```
RENAME BLOCK
────────────────────────────────────────
[WORKSTREAM] · [YYYY-MM-DD] · [plain-English session topic — 5-10 words]
────────────────────────────────────────
HANDOFF — [date]
WORKSTREAM: [value]
STOPPED AT: [text]
IN FLIGHT: [task or None]
NEXT ACTION: [step]
OPEN CONTEXT: [constraints or None]

**DB:**
- [db-name]: [db-id]
- PAT: SELECT value FROM secrets WHERE key = 'GITHUB_PAT'
- cs-work: /home/claude/cs-work (clone if absent)

✓ Stored — claude-config / key=[key] / v[N]
  Paste this block as the first message to resume.
  Rename this chat: [WORKSTREAM] · [YYYY-MM-DD] · [session topic]
```

---

## Gates

**RENAME_BLOCK_GATE** (PROJECT mode — HALT on failure; GENERAL mode — WARN only)

PROJECT mode:
- Format: `[WORKSTREAM] · S[N] · [TASK_ID]`
- All fields from D1 — never inferred from memory
- Exactly 4 backticks (2 open, 2 close)
- Failure: HALT

GENERAL mode (HV-13W — warn, not halt):
- Format: `[WORKSTREAM] · [YYYY-MM-DD] · [plain-English session topic]`
- No S[N] or TASK_ID — not applicable to GENERAL mode
- Must appear as a standalone section header line between ─── separator lines
- Failure: WARN (not HALT — initial rollout; candidate for HALT promotion after audit cycle)
- Enforced by: validate_handoff.py HV-13W

**DB_BLOCK_GATE** (GENERAL mode — WARN only)
- DB carry-forward section must be present in the handoff block
- Must contain at least one DB entry, or explicit "None" if no DB used
- Failure: WARN (not HALT — initial rollout; candidate for HALT promotion after audit cycle)
- Enforced by: validate_handoff.py HV-14W

**HANDOFF_CONTENT_GATE** (both modes)
- P1: evidence block visible before write — HARD FAIL if absent
- P2: field comparison after re-fetch — UNVERIFIED if mismatch
- P3: version = captured+1 — LOCK_VIOLATION if wrong

**CONCURRENT_WRITE_GATE** (both modes — fires when UPDATE changes=0)
```
⚠ CONCURRENT WRITE DETECTED
Key: [workstream_key]
Expected version: [captured_version] — Found: [current_version] (updated: [ts])
DB content preview: [first 120 chars]

Options:
  A) Overwrite — write this session's content (discards DB version)
  B) Archive DB version first, then overwrite (safe)
  C) Abort — keep DB version, discard this session's content

Waiting for user decision. Do NOT proceed without explicit choice.
```
HARD FAIL: never auto-overwrite on collision.

---

## DB Routing Reference

| Mode | DB | D1 ID |
|---|---|---|
| GENERAL | claude-config | afd78e0e-583e-4e78-87fc-dd6bc8150ce9 |
| loop-v2 | the-loop-storage | a2af54f4-6385-45dd-92e7-edc45fa5b8bd |
| other projects | from secrets: `session_manager_db_[project_id]` | varies |

---

## Error Handling

| Condition | Response |
|---|---|
| Required field empty | ERROR — name the field; do not write |
| Schema missing (PROJECT only) | ERROR — config not found |
| P1 block absent | HARD FAIL — write aborted |
| P2 mismatch | UNVERIFIED — name the mismatched field |
| P3 lock violation | LOCK_VIOLATION — halt |
| Concurrent write (changes=0) | CONCURRENT_WRITE_GATE — user decision required |
| D1 unavailable | Output in-chat block only; note "not persisted" |

---

## F-027 (RESOLVED — v2.2)

D1 writes require 2–3 tool calls (write + re-fetch). @monitor WARNING fires
with enough budget remaining for @handoff to complete. Additionally, @monitor
now writes a D1 checkpoint at WARNING time (Part 4.5 of sub-skill-monitor.md),
so partial state is preserved before HANDOFF ALERT fires. Do not start @handoff
if fewer than 3 tool calls remain in session budget.

## Re-Fetch Discipline

Mandatory. Read back after every write. Compare all fields. HARD FAIL if
verification step is skipped or produces no visible output.
