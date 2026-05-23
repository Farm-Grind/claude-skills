# @briefing — Session Start Briefing Generator

**Purpose:** Generate session briefing from project config + D1 data.

**Trigger:** Session start, "where are we", "load briefing"

## Input
- project_id (from dispatcher)
- session_manager_briefing_format_[project_id] (D1 config)
- Source tables referenced in config

## Logic

1. **Parse config:** Extract field definitions (name, source table, filter, template)
2. **For each field:** Query D1, apply filter, format with template
3. **D1-WRITE GATE** (hard gate — runs before briefing output):
   Execute a write to sessions_log to confirm D1 write access is live.
   SQL: `INSERT INTO sessions_log (session_date, project_id, event) VALUES (datetime('now'), '[project_id]', 'SESSION_START')`
   - If write succeeds: proceed to step 4.
   - If write fails: ERROR — "D1 write unavailable. Check connection before proceeding. Briefing blocked per F-059."
   - Do NOT produce briefing output if write fails. No fallback to read-only mode.
   WHY: F-059 — decision logging failures were traced to D1 write access failing silently mid-session.
   Catching it at session start prevents 8+ decisions from going unlogged (documented session loss).
4. **For each conditional alert:** Check condition; if true, append alert
5. **Construct briefing block:** Combine fields in order

## Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Project] — Session Briefing  [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[field_1]
[field_2]
...
[alerts if any]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling
- Config missing: ERROR
- D1 fetch fails: ERROR (no fallback to memory)
- D1 write gate fails: ERROR — briefing blocked (see step 3)
- No rows match: Display as "0" or "none"

## Re-Fetch Discipline
Read-only for field queries; one write at gate (step 3). Fresh read every call.
