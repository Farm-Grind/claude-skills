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

---

## Failure Audit INSERT (claude-config DB: afd78e0e-583e-4e78-87fc-dd6bc8150ce9)

These write to the **universal** failure audit DB, not the-loop-storage. Always use the claude-config DB UUID for these queries.

**Pre-INSERT: fix type gate (required before any INSERT with fix_type field)**

Run before every INSERT that sets fix_type. Bypassing this gate allows P-03 (BEHAVIORAL fix for recurring pattern) to recur through direct writes:

```bash
python3 /home/claude/cs-work/ci/check_fix_type.py --pattern <P-XX> --fix-type <STRUCTURAL|TEMPORAL|BEHAVIORAL>
```

Exit 1 = HARD FAIL — reclassify fix_type before INSERT. Exit 2 = WARN — document justification inline before INSERT. Repo absent: clone Farm-Grind/claude-skills via PAT below.

To supply live recurrence count instead of local registry (recommended for patterns added after 2026-05-17):

```sql
-- Run on claude-config DB: afd78e0e-583e-4e78-87fc-dd6bc8150ce9
SELECT recurrence_count FROM failure_patterns WHERE pattern_code = 'P-XX'
```

Then pass: `python3 ci/check_fix_type.py --pattern P-XX --fix-type BEHAVIORAL --recurrence-count <N>`

**Get next finding ID:**
```sql
SELECT 'F-' || printf('%03d', MAX(CAST(SUBSTR(finding_id,3) AS INTEGER)) + 1)
FROM granular_findings
```

**INSERT new finding:**
```sql
INSERT INTO granular_findings
  (finding_id, pattern_code, title, source_conversation, symptom,
   root_cause, fix_applied, fix_type, status, artifact_affected, project_scope)
VALUES
  ('F-XXX', 'P-XX', 'Short title', 'https://claude.ai/chat/...', 'Symptom: what wrong output looked like',
   'Root cause: mechanism not symptom', NULL, 'STRUCTURAL', 'OPEN', 'skill or file affected', 'UNIVERSAL')
```
⚠ **SYNC TRIGGER** — run Step 4 (CI sync) after this write.

**UPDATE finding to RESOLVED:**
```sql
UPDATE granular_findings
SET status = 'RESOLVED', fix_applied = 'What was done', fix_type = 'STRUCTURAL'
WHERE finding_id = 'F-XXX'
```
⚠ **SYNC TRIGGER** — run Step 4 (CI sync) after this write.

**Increment pattern recurrence count:**
```sql
UPDATE failure_patterns
SET recurrence_count = recurrence_count + 1, updated_at = datetime('now')
WHERE pattern_code = 'P-XX'
```
⚠ **SYNC TRIGGER** — run Step 4 (CI sync) after this write.

**Get current OPEN findings (for CI JSON sync):**
```sql
SELECT finding_id, pattern_code, title, artifact_affected, project_scope
FROM granular_findings WHERE status = 'OPEN'
ORDER BY finding_id
```

**Get PAT for CI sync:**
```sql
SELECT value FROM secrets WHERE key = 'GITHUB_PAT'
```

Pattern code mapping (use closest match):
- P-01 Self-referential audit loop
- P-02 Additive-only / no budget enforcement
- P-03 Behavioral fix for structural problem
- P-04 Missing reference files / orphaned citations
- P-05 Gate sequence violation
- P-06 Wrong skill triggered / routing failure
- P-07 Platform constraint discovery through failure
- P-08 Unbounded meta-work / recommendation queue debt
- P-09 Partial paste / incomplete deliverable
- P-10 Position drift / specification drift
- P-11 Skill scope contamination
- P-12 Context-switch momentum overrides procedural gates
- P-13 Context compression loss (long-context rule degradation)
- P-14 Tool write without verification (write without read-back confirm)
- P-15 Complexity inflation under iterative pressure

