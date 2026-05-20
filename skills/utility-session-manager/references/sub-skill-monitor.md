# @monitor — Context Health Monitor

**Purpose:** Track session health silently from first message. Emit WARNING and
HANDOFF ALERT at thresholds. Enforce session state machine. Route to @handoff
when state is SESSION_ENDING.

**Trigger:** Auto-invoked at start of every turn (Step 0 of INTAKE CLASSIFICATION).
Explicit invocation for context status reports ("how long is this session", etc.)

---

## Part 1 — Passive Load Estimate

Run once at session start. Estimate before counting turns or tool calls.

| Connected MCP servers | Estimated passive load | Effective working space |
|---|---|---|
| 0 | ~0 tokens | Full window |
| 1–2 | ~20,000–40,000 tokens | ~75% of window |
| 3–4 | ~60,000–100,000 tokens | ~50% of window |
| 5–7 | ~100,000–120,000 tokens | ~25% of window |
| 8+ | ~100,000+ tokens | 20–40K max — sessions begin at or past degradation cliff |

With 3+ servers: treat session as starting at 40–50% context utilization.
With 8+ servers: treat as starting at 80–90%. Effective space ~20–40K.

---


## Part 2 — Session State Machine

### States

| State | Meaning |
|---|---|
| `IN_SESSION` | Normal work. No session-ending condition fired. |
| `SESSION_ENDING` | HANDOFF ALERT fired, or drift signal detected and not resolved. Handoff is the only valid next action. |
| `SESSION_ENDED` | Handoff block delivered in chat. No further work valid. |

### State Inference (run at start of every response)

Evaluate in order — assign first match:

1. Has a handoff block been delivered this session (block containing STOPPED AT / IN FLIGHT / NEXT ACTION fields)? → `SESSION_ENDED`
2. Has HANDOFF ALERT fired this session, OR was a drift signal detected and not resolved? → `SESSION_ENDING`
3. Otherwise → `IN_SESSION`

### State Declaration

- `IN_SESSION`: silent — no declaration needed.
- `SESSION_ENDING` or `SESSION_ENDED`: first line of response must be `[STATE: SESSION_ENDING]` or `[STATE: SESSION_ENDED]`.

### Valid Actions Per State

| State | Valid | Forbidden |
|---|---|---|
| `IN_SESSION` | All normal work | — |
| `SESSION_ENDING` | Generate handoff block only | New tasks, deliverables, scope expansion, continuing in-flight work |
| `SESSION_ENDED` | Acknowledge only — direct user to paste handoff | All work |

---

## Part 3 — Drift Signal Detection

Any signal below → immediate HANDOFF ALERT, regardless of turn/tool count.

**Behavioral drift (HANDOFF ALERT immediately):**
- User said "that's wrong", "no", "fix this", or explicitly corrected substantive output
- Claude re-asked for something established earlier in the session (a path, decision, name, constraint)
- A decision logged earlier in the session was contradicted in a later response

**Context drift (WARNING first, then escalate if continues):**
- Repeated a question already answered earlier in the session
- Proposed an approach that contradicts a decision explicitly locked earlier
- Dropped a formatting rule, naming convention, or constraint established and confirmed earlier
- Response hedging increased: answers that were previously direct are now qualified or vague

Drift notice format:
```
⚠ DRIFT SIGNAL DETECTED: [what happened — one sentence]
Escalating to HANDOFF ALERT.
```

---

## Part 4 — Thresholds

| Condition | Output | State transition |
|---|---|---|
| Tool calls ≥ 5 OR turns ≥ 15 | Emit WARNING once | Stays IN_SESSION |
| Tool calls ≥ 15 OR turns ≥ 25 | HANDOFF ALERT | → SESSION_ENDING |
| Behavioral drift signal detected | HANDOFF ALERT immediately | → SESSION_ENDING |
| §5b sprint active (skill packaging session): tool calls ≥ 8 | Treat as WARNING threshold | — |

**§5b sprint signal:** When a skill sprint is active, tool-call accumulation is structurally
higher. Treat ≥ 8 tool calls as WARNING threshold. Treat ≥ 12 as HANDOFF ALERT.

**Per-project overrides:** Check D1 `session_config` for entries matching
`session_manager_monitor_*_[project_id]`. If present, use project values. If absent, use
above defaults.

---

## Part 4.5 — WARNING Checkpoint Write (structural fix for F-027)

Fires once, at the same turn WARNING emits. Guards against D1 write failure when
HANDOFF ALERT fires with insufficient tool-call budget remaining.

**Step 1 — Derive workstream key**
Apply sub-skill-handoff.md Part 2 derivation rules. If key is not derivable (workstream
name unknown and project_id unset): skip checkpoint; append
`Checkpoint: skipped — workstream key not yet known` to WARNING output.

**Step 2 — Write checkpoint row**
```sql
INSERT OR REPLACE INTO session_handoff
  (key, workstream, content, stopped_at, next_action, version, updated_at)
VALUES
  ('[key]-checkpoint',
   '[workstream name or "unset"]',
   '[in-flight task — 1-2 sentences from conversation context]',
   '[current task approximate state]',
   'Resume from checkpoint — run @briefing for full state',
   0, datetime('now'))
```
DB: same target @handoff would use (GENERAL mode: claude-config; PROJECT mode: project DB).

**Step 3 — Report in WARNING block**
Append one line: `Checkpoint: saved to [key]-checkpoint` or `Checkpoint: skipped — [reason]`.

**Rules:**
- No HANDOFF_CONTENT_GATE required — checkpoint is best-effort, not an authoritative handoff.
- No re-fetch required — @handoff remains the authoritative write with full verification.
- Do not fire if WARNING has already fired this session (once-only).
- Checkpoint write failure (D1 unavailable): note in WARNING output; do not block WARNING emit.



**WARNING:**
```
⚠ SESSION WARNING
Tool calls: [N] | Turns: [N] | MCP servers: [N]
Passive load: [estimate from Part 1]
Recommendation: finish the current task, then consider a handoff.
Checkpoint: [saved to [key]-checkpoint / skipped — workstream key not yet known]
```

**HANDOFF ALERT:**
```
⛔ HANDOFF ALERT
[Reason: threshold / drift signal — one sentence]
Producing handoff now. Do not continue task work.
```

After emitting HANDOFF ALERT: immediately load `references/sub-skill-handoff.md`
and execute @handoff. Do not wait for user confirmation. Do not finish the
in-flight task first.

**Explicit status report** (user asked "how long is this session"):
```
Session status: [IN_SESSION / SESSION_ENDING / SESSION_ENDED]
Tool calls: [N] | Turns: [N] | MCP servers: [N (estimated)]
Passive load: [estimate]
Context tier: [Safe / Warning zone / Handoff recommended]
```

---

## Part 6 — Escalation Summary

| Condition | Output | State |
|---|---|---|
| Under WARNING threshold, no drift | Silent | IN_SESSION |
| WARNING threshold crossed | Emit WARNING + write D1 checkpoint (Part 4.5) | IN_SESSION |
| HANDOFF ALERT threshold | HANDOFF ALERT + execute @handoff | SESSION_ENDING |
| Behavioral drift | HANDOFF ALERT + execute @handoff immediately | SESSION_ENDING |
| Handoff block delivered | Instruct to paste into new chat | SESSION_ENDED |
| Explicit status request | Report current status | unchanged |

---

## Re-Fetch Discipline

@monitor is read-only for session state inference. The one write it performs is the
WARNING checkpoint (Part 4.5) — best-effort, no verification required.
Never assume state from a prior turn; re-infer each time.
