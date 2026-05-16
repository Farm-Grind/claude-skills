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
3. **For each conditional alert:** Check condition; if true, append alert
4. **Construct briefing block:** Combine fields in order

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
- No rows match: Display as "0" or "none"

## Re-Fetch Discipline
Read-only; fresh read every call.
