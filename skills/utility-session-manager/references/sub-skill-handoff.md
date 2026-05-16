# @handoff — Handoff Generator & Writer

**Purpose:** Collect handoff content, validate, gate, write to D1, verify.

**Trigger:** Session end, "save handoff", "close out", "wrap up"

## Input
- project_id
- session_manager_handoff_schema_[project_id]
- session_manager_gates_*_[project_id]
- User-provided content

## Logic

1. **Load schema + gates** from D1
2. **Validate required fields:** Non-empty + constraints met
   - If fail: ERROR
3. **Run gates (in order):**
   - HALT gate fails: ERROR
   - WARN gate fails: warn + confirm
4. **Construct handoff:** Combine fields + generate LAST_SYNCED
5. **Write to D1:** INSERT with optimistic locking
   - If changes=0: concurrent write → HALT
   - If changes=1: proceed to verify
6. **Re-fetch verification (MANDATORY):**
   - Read back record
   - Compare all fields against intended content
   - If mismatch: UNVERIFIED flag
   - If all match: confirm success
7. **Output:** Rename block + handoff block OR error

## Key Gates

**RENAME_BLOCK_GATE:**
- Format: [WORKSTREAM] · S[N] · [TASK_ID]
- Exactly 4 backticks
- Fields from D1 only
- Failure: HALT

**HANDOFF_CONTENT_GATE:**
- All required fields non-empty
- Min length constraints
- No silent thinning
- Failure: HALT or confirm

## Output Format
```
RENAME BLOCK
───────────────────────────────────────
[WORKSTREAM] · S[N] · [TASK_ID]
───────────────────────────────────────

HANDOFF — [date]
WORKSTREAM: [value]
STOPPED AT: [text]
IN FLIGHT: [task or None]
NEXT ACTION: [step]
OPEN CONTEXT: [constraints]
LAST SYNCED: [tables + datetime]

✓ Handoff stored
```

## Error Handling
- Schema missing: ERROR
- Required field empty: ERROR
- Constraint violated: ERROR
- Gate fails: HALT
- Re-fetch mismatch: UNVERIFIED

## Re-Fetch Discipline
MANDATORY. Read back. Compare all. HARD FAIL if unverified.
