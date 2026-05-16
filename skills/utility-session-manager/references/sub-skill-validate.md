# @validate — Handoff Audit

**Purpose:** Audit handoff completeness without writing.

**Trigger:** "Check handoff", "validate state", "handoff report"

## Input
- project_id
- session_manager_handoff_schema_[project_id]
- Current session_handoff from D1

## Logic

1. **Load schema + handoff** from D1
2. **Field-by-field audit:**
   - Missing: flag "⚠ [field]: MISSING"
   - Too short: flag "⚠ [field]: TOO SHORT"
   - Constraint fail: flag "⚠ [field]: CONSTRAINT FAILED"
   - OK: flag "✓ [field]: OK"
3. **Summarize:** Count missing; report COMPLETE or INCOMPLETE

## Output
```
HANDOFF AUDIT — [date]
─────────────────────────────────────────────
✓ WORKSTREAM: OK
⚠ STOPPED_AT: TOO SHORT
✓ IN_FLIGHT: OK
✓ NEXT_ACTION: OK
✓ OPEN_CONTEXT: OK
✓ LAST_SYNCED: OK

Status: INCOMPLETE — 1 issue
─────────────────────────────────────────────
```

## Error Handling
- Handoff not found: "No handoff — session starting fresh"
- D1 fetch fails: "Cannot audit — D1 issue"
- Never infer from memory

## Re-Fetch Discipline
Read-only; fresh read every call.
