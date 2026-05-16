# Session Continuity — Developer Reference

Maintains build phase state and task continuity across coding sessions.
Every session starts by loading where the last ended.
Every session ends by saving what was completed and what comes next.

---

## STORAGE

Read/write via Notion MCP on the project's Build Phase page.
Extract the `## Data` section and parse the JSON block.

```json
{
  "phase": 1,
  "phaseName": "Scaffolding",
  "phaseStarted": "YYYY-MM-DD",
  "currentTask": "Description of active task",
  "lastCompleted": null,
  "completedTasks": [],
  "notes": "Blockers, decisions, or context for next session."
}
```

---

## BUILD PHASES

| # | Name | What gets built |
|---|---|---|
| 1 | Scaffolding | Expo project, navigation structure, Supabase connection, auth screens |
| 2 | Core Game Loop | Primary screens, game state, inventory, tick/cycle logic |
| 3 | Content & Progression | Item database, quest system, story flags, economy |
| 4 | Polish & Feel | Animations, sound, visual effects, transitions |
| 5 | Live Features | Push notifications, cloud save sync, settings, onboarding |
| 6 | Launch Prep | EAS Build, store listings, privacy policy, beta testing |

Always derive current phase from storage — never assume from memory.

---

## SESSION START PROTOCOL

Before generating any code:

1. Fetch current build phase from project storage (Notion Build Phase page).
2. **Key missing** → first coding session. Initialize Phase 1:
   ```
   Starting Phase 1 — Scaffolding. First task: [task]. Ready?
   ```
3. **Key exists** → surface handoff block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUMING — Phase [N]: [Phase Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last completed:  [lastCompleted or "nothing yet"]
Current task:    [currentTask]
Notes:           [notes or "none"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pick up with [currentTask], or something else first?
```

If user says "just start coding": surface one-liner
`Phase [N] — [currentTask]. Going.` then proceed.

**HARD FAIL:** Any code generation that occurs before the handoff block
(or one-liner equivalent) is surfaced is a process failure. Implicit
coding starts ("fix this bug") still trigger Session Start Protocol.

---

## SESSION END PROTOCOL

After any coding session:

1. Ask: "What should I mark as completed from this session?"
2. Update storage: add completed items to `completedTasks` (with date),
   set `lastCompleted`, set `currentTask` to what comes next, set `notes`.
3. Confirm:

```
✓ Session saved — Phase [N]: [Phase Name]
  Completed: [task]
  Up next:   [nextTask]
```

**HARD FAIL:** Any response ending a coding session without running
Session End Protocol is a process failure.

---

## PHASE ADVANCEMENT

When all tasks in current phase are complete:

1. Confirm: "Phase [N] looks complete. Advance to Phase [N+1]: [name]?"
2. On confirmation: increment `phase`, update `phaseName`, reset `currentTask`
   to first task of new phase, clear `notes`, write back.
3. Log phase advancement as LOCKED OPS decision via decisions logger.
4. Confirm: `✓ Advanced to Phase [N+1]: [name]`

Never advance a phase without explicit user confirmation.

---

## LINEAR TICKET TIMING

- **In Progress:** set when work on that ticket begins — first substantive
  action, not at close-out.
- **Done:** set at close-out when work is confirmed complete.

Confirmation format:
- `✓ In Progress: MAN-XX [title]` (on first action)
- `✓ Done: MAN-XX [title]` (at close-out)

Do not batch all status updates to close-out.

---

## CRITICAL RULES

- Never generate code before surfacing the handoff block.
- Never skip the session end update — it is the only continuity mechanism.
- Never advance a phase without explicit user confirmation.
