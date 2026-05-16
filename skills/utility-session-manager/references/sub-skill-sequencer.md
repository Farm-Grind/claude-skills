# @sequencer — Next Task Identifier

**Purpose:** Identify next task based on dependency order + current status.

**Trigger:** "What's next?", "what should we work on", "what's blocking"

## Input
- project_id
- session_manager_sequencer_mode_[project_id] (D1 config)
- design_dependencies table + task status table

## Logic

1. **Load state:** Fetch tables; join on configured keys. If fetch fails → ABORT
2. **Find current level:** Lowest level with incomplete items
3. **Identify next task:** First incomplete task at current level
4. **Check blockers:** Prerequisites met?
5. **Generate SEQUENCER block:** STATE | LEVEL | NEXT TASK | WHY | WHAT COMES AFTER
6. **Run exit gates:** Task specificity, alternatives, uncertainty
7. **Output:** Final block or abort

## Exit Gates

**Gate 1: Task Specificity**
- Must name specific deliverable, not level/category
- FAIL if: "Level 3", "continue X"

**Gate 2: Alternatives**
- Evaluate ≥1 alternative OR state "only viable"
- FAIL if: single candidate unchecked

**Gate 3: Uncertainty**
- Surface judgment calls explicitly
- FAIL if: false confidence

## Output
```
SEQUENCER — [date]
─────────────────────────────────────────────
STATE: [N] blockers, [N] open decisions
CURRENT LEVEL: [N] — [Name]
NEXT TASK: [Specific name]
READY: [Yes/No — list blockers if No]
WHY THIS TASK: [1–3 sentences, grounded in dependency]
WHAT COMES AFTER: [Next 2–3 tasks]
─────────────────────────────────────────────
```

## Error Handling
- Config missing: ERROR
- Dependency table missing: ABORT
- Task status fetch fails: ABORT
- Never sequence from memory

## Re-Fetch Discipline
Read-only; no verification.
