# D1 Query Patterns

D1 UUID: `a2af54f4-6385-45dd-92e7-edc45fa5b8bd` — never from memory. Always from session_handoff or cloudflare-storage_v1_3.

## Step E — Error Log Baseline

```sql
SELECT e.id, e.description, e.root_cause, e.severity, e.queue_item,
       o.status AS queue_status
FROM error_log e
LEFT JOIN ops_queue o ON e.queue_item = o.id
ORDER BY e.created_at DESC
```

Three-bucket classification:

| Bucket | Condition | Action |
|---|---|---|
| CONFIRMED OPEN | queue_item NULL or queue_status != 'DONE' | Retain as open; do not re-diagnose |
| IMPLEMENTED, STILL FAILING | queue_status = 'DONE' AND same category recurs | Classify HB; auto-escalate CRITICAL |
| RESOLVED | No recurrence AND queue_status = 'DONE' | Exclude; note count only |

## Queue Depth Check (before any IMMEDIATE insert)

```sql
SELECT COUNT(*) AS n FROM ops_queue WHERE status NOT IN ('DONE', 'DEFERRED')
```

If n ≥ 5: `[QUEUE AT CAP]` — note extras, do not insert.

## PROPOSED Backlog Check (run at P4 start)

```sql
SELECT e.id, e.description, e.root_cause, e.severity
FROM error_log e
WHERE e.status = 'OPEN'
AND e.queue_item IS NULL
ORDER BY e.created_at ASC
```

Any result with a category matching the current scan window → classify as HB-candidate. These are findings proposed but never actioned — same failure risk as IMPLEMENTED STILL FAILING. Log count in diagnostic header.

## ops_queue INSERT (IMMEDIATE fix items only)

```sql
-- First: get next ID
SELECT MAX(id) FROM ops_queue

-- Then insert (example: OPS-042)
-- params: ['OPS-042', '[QUEUED] P1 — description', 'QUEUED', 'P1-blocking',
--          'skill-edit', 'verbatim spec', 'context', 'DIAG-session-name', '', '2026-05-13']
INSERT INTO ops_queue VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
```

## error_log INSERT

```sql
-- params: ['ERR-id', 'description', 'root_cause', 'severity', NULL, 'OPEN', NULL]
INSERT INTO error_log (id, description, root_cause, severity, queue_item, status, fix_applied)
VALUES (?, ?, ?, ?, ?, ?, ?)
```

Note: error_log requires schema extension before status/fix_applied fields are available (Design Decision D1 — run ALTER TABLE migration first).

## Skill Registry Verification

```sql
-- All skills
SELECT skill_name, version, status, notes FROM skill_registry ORDER BY skill_name ASC

-- Specific skill
SELECT skill_name, version, status, notes FROM skill_registry WHERE skill_name = ?
```

## Decisions Log Check

```sql
SELECT d_id, title, status FROM decisions
WHERE status IN ('OPEN', 'LOCKED')
ORDER BY created_at ASC
```

## Session Handoff

```sql
SELECT content, updated_at FROM session_handoff WHERE key = 'CURRENT'
```
