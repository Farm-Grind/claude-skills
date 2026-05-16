# Build Planning — Developer Reference

A session implementation plan is a persistent markdown file written before
any code. It is the contract between design and implementation.
Nothing gets coded until the plan exists and is approved.

**Context window = RAM (volatile). Filesystem = disk (persistent).**
A plan in chat is lost when context clears. A plan in a file survives.

---

## WHEN TO WRITE A PLAN

Write a plan when:
- A coding session is starting with no existing plan for the current task
- The task requires more than one file change
- A new build phase begins

Do NOT write a plan for: trivial single-file fixes (typo, rename, one-liner change).

**HARD FAIL:** Never present plan content in chat until the plan file exists on disk.
Verify with `ls` before presenting. Chat-only plans do not survive `/clear`.

**HARD FAIL:** "Don't implement yet" MUST appear in the same response that
presents any plan for approval. Approval = explicit words ("approved", "go",
"implement"). Silence is not approval.

---

## PLAN FILE LOCATION

```
docs/plans/YYYY-MM-DD_[task-slug].md
```

Examples:
```
docs/plans/2026-04-15_phase1-project-setup.md
docs/plans/2026-04-22_cycle-end-rpc.md
```

Create the file before presenting. The plan lives on disk from the moment
it is written — not after approval.

---

## PLAN STRUCTURE

Required sections in order:

```markdown
# [Task Name] — Implementation Plan
> Phase: [N] — [Phase Name]
> Date: YYYY-MM-DD
> Status: DRAFT | APPROVED | IN PROGRESS | COMPLETE

**Goal:** [One sentence — what this plan produces]
**Phase context:** [Why this task comes now in the build sequence]
**Stack:** [Relevant technologies for this plan]

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `src/stores/gameStore.ts` | CREATE | Zustand store for active cycle state |

---

## Tasks

### Task 1: [Short title]
- [ ] Step 1: [Exact action with exact file path]
    ```typescript
    // Complete code — not a sketch
    ```
- [ ] Verify: [Exact command or observable outcome]

---

## Verification: Full Session
- [ ] [Observable outcome — not "it compiles"]
- [ ] Build tracker updated with completed tasks

---

## Acceptance Criteria
- [ ] [Observable, testable condition — not "it works"]

---

## Blocked On
- [D-XXX] [Decision needed before implementing]
```

---

## TASK QUALITY RULES

**Required in every task:**
- Exact file paths (not "the store file")
- Code blocks for any step writing or modifying code
- Verification step with exact command or observable outcome
- Dependency order — no task references a file that doesn't exist yet in the plan

**Prohibited patterns:**

| Prohibited | Why |
|---|---|
| "TBD", "TODO", "implement later" | Executor has no context |
| "Add appropriate error handling" | Write the handler |
| "Handle edge cases" | Name them; write the handling |
| "Write tests for the above" without test code | Write the test |
| Prose description of code with no code block | Code block is required |
| Reference to type/function not defined in any task | Phantom dependency |

---

## ANNOTATION LOOP

After presenting draft plan:
```
Plan saved to docs/plans/[filename].md. Review and add inline notes where
you see gaps, wrong approaches, or missing constraints. Say "address notes"
to update. Don't implement yet.
```

On "address notes": re-read the plan file from disk (never from session memory),
update per annotations, present PLAN UPDATE block showing changes.

---

## CONFIRMATION BLOCK

```
Write plan self-review:
  OPEN decision dependency: [decisions log checked, or "no OPEN dependencies"]
  Acceptance criteria: [all ACs observable and testable, or "N rewritten"]
  Dependency order: [all task dependencies verified in order, or "N reordered"]
  Rollback documentation: [hard-to-reverse tasks have rollback steps, or "none"]
  Scope completeness: [every deliverable maps to a task, or "N gaps resolved"]
  Status: CLEAR to present / BLOCKED — [reason]
```

If BLOCKED: resolve before presenting. "Don't implement yet" still required.
