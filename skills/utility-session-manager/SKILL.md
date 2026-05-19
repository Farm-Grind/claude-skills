---
name: utility-session-manager
description: >
  Always-active session lifecycle manager and context health monitor for any
  project. Fires silently at the start of every session — runs @monitor on
  first message, then tracks tool calls, turns, and behavioral drift
  throughout. Routes explicit signals to five sub-skills: @monitor (context
  health, drift detection, escalation), @briefing (session start briefing),
  @sequencer (next task), @handoff (save state), @validate (audit state). All
  project-specific configuration lives in D1 tables — skill body is
  project-agnostic. Use automatically — do not wait to be asked. Trigger on
  ANY session first message OR these explicit signals: "where are we", "load
  briefing", "what's next", "what should we work on", "what's blocking",
  "save handoff", "close out", "wrap up", "check handoff", "validate state",
  "how long is this session", "should we start a new chat", "generate handoff
  prompt". Do NOT trigger for: design work, lore creation, or coding with no
  session lifecycle signal. Load once per session.
---
gates_passed: 2026-05-19
SKILL_VERSION: v2.2
Type: dispatcher

# Universal Session Manager

Always-active dispatcher for session lifecycle management and context health
monitoring across any project. All project-specific logic lives in D1
configuration — zero project IP in this skill.

---

## GOTCHAS

Failure modes Claude exhibits without this skill.

1. **Routing to sub-skill without reading D1 config first** — the briefing format, sequencer mode, and handoff schema differ per project. Routing before config load causes the wrong format, wrong table joins, or wrong field names to be used. Always query session_config before executing any sub-skill.

2. **Inferring project_id from conversation context instead of explicit signal** — project names appear in many places (handoff blocks, workstream fields, topic text). The intake classification step exists to detect the authoritative signal. Guessing bypasses it and causes silent cross-project routing failures.

3. **Executing sub-skill logic from body knowledge instead of loading the reference file** — each sub-skill has distinct field schema, gate sequence, and error handling defined in its reference file. Running from memory produces missing gates (especially HANDOFF_CONTENT_GATE and re-fetch verification).

4. **Treating D1 fetch failure as an empty result** — a failed query returns no rows AND may indicate a connection issue. Always distinguish "query ran, no rows" from "query failed" and error explicitly on failure.

5. **Skipping the re-fetch verification step in @handoff** — the write returning `changes=1` confirms the write succeeded but does not verify content correctness. The re-fetch is mandatory; omitting it violates HANDOFF_CONTENT_GATE.

6. **Continuing task work after HANDOFF ALERT fires** — HANDOFF ALERT immediately sets state to SESSION_ENDING. No further task work, deliverables, or scope expansion is valid. Produce the handoff immediately — a partial task with an accurate handoff is recoverable; a completed task with a fabricated handoff at 90% context is not.

7. **Not re-inferring session state at the start of each response** — @monitor has no memory between turns. State (IN_SESSION / SESSION_ENDING / SESSION_ENDED) must be re-derived each turn from observable signals. Running from prior-turn state assumptions causes forbidden actions in SESSION_ENDING or SESSION_ENDED states.

8. **Silently continuing after a drift signal fires** — when a behavioral drift signal fires (user correction, re-asked question, contradicted decision), escalate to HANDOFF ALERT immediately. Do not finish the current task first. Do not defer the handoff.

---

## INTAKE CLASSIFICATION

**Step 0: Auto-monitor (runs silently on every turn)**

```
Load references/sub-skill-monitor.md
Re-infer session state from conversation (IN_SESSION / SESSION_ENDING / SESSION_ENDED)
If SESSION_ENDED: declare state, instruct user to paste handoff — no further work
If SESSION_ENDING: route to @handoff immediately — skip Steps 1–3
If IN_SESSION and no HANDOFF ALERT: run threshold check silently
  If threshold crossed: emit WARNING or HANDOFF ALERT per monitor reference
  If no threshold crossed: silent — proceed to Steps 1–3
```

**Step 1: Detect project context**

```
IF user explicitly names project (e.g., "for loop-v2"):
  project_id = user input
ELSE IF session_handoff.workstream exists:
  project_id = extract prefix from workstream (e.g., "LOOP-v2-..." → "loop-v2")
ELSE:
  ASK: "Which project? (e.g., loop-v2, novel-project)"
```

**Step 2: Load configuration from D1**

Query `session_config` for all entries matching project_id. If config missing → ERROR.

**Step 3: Classify user intent**

```
IF user trigger matches: "how long", "are we close", "should we start a new chat",
  "do you still have context", "generate handoff prompt", context status request
  → Route to @monitor (explicit status report)
ELSE IF user trigger matches: "where are we" OR "load briefing"
  → Route to @briefing
ELSE IF user trigger matches: "what's next" OR "what should we work on" OR "what's blocking"
  → Route to @sequencer
ELSE IF user trigger matches: session end OR "save handoff" OR "close out" OR "wrap up"
  → Route to @handoff
ELSE IF user trigger matches: "check handoff" OR "validate state" OR "handoff report"
  → Route to @validate
ELSE
  ASK: "Did you mean @monitor / @briefing / @sequencer / @handoff / @validate?"
```

---

## SUB-SKILL ROUTING

| Intent | Sub-Skill | Reference File |
|--------|-----------|-----------------|
| Context health, drift detection, escalation | @monitor | references/sub-skill-monitor.md |
| Generate session briefing | @briefing | references/sub-skill-briefing.md |
| Identify next task | @sequencer | references/sub-skill-sequencer.md |
| Save session state | @handoff | references/sub-skill-handoff.md |
| Audit session state | @validate | references/sub-skill-validate.md |

---

## EXECUTION PATTERN

For each sub-skill invocation:

1. Load reference file: `view references/sub-skill-[name].md`
2. Execute logic per reference file specification
3. Apply project config (loaded in Step 2 of intake)
4. Output result per reference file format
5. Handle errors per reference file rules

NEVER execute a sub-skill without a visible `view` output for its reference file in the current turn.

---

## ERROR HANDLING

| Condition | Response |
|---|---|
| Config missing | ERROR — "Configuration not found for [project_id]. Create entries in D1 session_config before use." |
| D1 fetch fails | ERROR — "Cannot connect to D1. Check database availability." |
| Ambiguous trigger | ASK — one clarification question; name the four sub-skills |
| Sub-skill execution error | Surface error with reason; no retry |

---

## EXAMPLES

**Example 1 — Session start, project named explicitly:**
User: "Load briefing for loop-v2"
→ Step 1: project_id = "loop-v2" (explicitly named)
→ Step 2: Query D1 `session_config` WHERE config_type LIKE 'session_manager_%_loop-v2'
→ Step 3: trigger = "load briefing" → route to @briefing
→ Load references/sub-skill-briefing.md, execute, output briefing block

**Example 2 — Session end, project inferred from handoff:**
User: "wrap up"
→ Step 1: project_id inferred from session_handoff.workstream ("LOOP-v2-MAN-XX" → "loop-v2")
→ Step 2: Query D1 session_config for loop-v2
→ Step 3: trigger = "wrap up" → route to @handoff
→ Load references/sub-skill-handoff.md, validate required fields, run RENAME_BLOCK_GATE, write D1, re-fetch, output handoff block

**Example 3 — Ambiguous trigger with no project context:**
User: "what should I work on"
→ Step 1: No project named; no session_handoff in context → ASK "Which project?"
→ User: "loop-v2"
→ Step 2: Query D1 session_config for loop-v2
→ Step 3: trigger matches @sequencer
→ Load references/sub-skill-sequencer.md, run dependency logic, output SEQUENCER block

**Example 4 — D1 config missing:**
User: "load briefing for novel-project"
→ Step 1: project_id = "novel-project"
→ Step 2: Query D1 → 0 rows returned for config_type LIKE '%novel-project'
→ ERROR: "Configuration not found for novel-project. Create entries in D1 session_config before use."

**Example 5 — Auto-trigger at session start, no lifecycle signal:**
First message: "Help me fix the FlashList perf issue in the Loop project"
→ Step 0: No prior turns — load references/sub-skill-monitor.md, run @monitor
  session-start check. 3 MCP servers connected → passive load ~60K tokens.
  State = IN_SESSION. Tool calls = 0, turns = 1 → no threshold crossed. Silent.
→ Step 1: "loop" in context → project_id = "loop-v2"
→ Step 2: Query D1 session_config for loop-v2
→ Step 3: no session lifecycle signal → no routing; proceed with user task normally

---

## OUT OF SCOPE

Does NOT: make design decisions, define project dependencies, create configuration,
enforce rules beyond what config specifies, generate project IP.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| references/sub-skill-monitor.md | Context health monitoring, drift detection, state machine, escalation |
| references/sub-skill-briefing.md | Session start briefing logic |
| references/sub-skill-sequencer.md | Next-task identification logic |
| references/sub-skill-handoff.md | Handoff collection, write, and verification logic |
| references/sub-skill-validate.md | Handoff audit logic |
| references/config-format.md | D1 configuration schema + key naming conventions |
| utility-ops-project-manager | Generic project dispatcher (reference pattern) |
