---
name: utility-core-session-monitor
description: >
  Monitors conversation length, MCP tool-call accumulation, and behavioral
  drift signals to warn before context quality degrades. Tracks explicit session
  state (IN_SESSION / SESSION_ENDING / SESSION_ENDED) and enforces which actions
  are valid per state. Two-tier escalation: WARNING (advisory) when risk is
  emerging; HANDOFF ALERT (hard stop) when quality is at real risk. Accounts
  for passive token load from connected MCP servers. Universal across projects.
  Use automatically — do not wait to be asked. Trigger on ANY of these signals:
  5 or more tool calls this session (any tool type); session at 15 or more turns; behavioral
  drift detected (dropped constraint, re-asked question, contradicted decision,
  increased hedging); user asks "is this getting long", "should we start a new
  chat", "are we close to the limit", "do you still have context",
  "generate handoff prompt". Do NOT trigger for: sessions under 10 turns with
  no tool calls; single-lookup sessions; [explore] turns with no deliverable.
  Load once per session.
---
SKILL_VERSION: v2.5

# Session Monitor

Detects context length risk and emits two-tier escalation: WARNING (advisory)
and HANDOFF ALERT (hard recommendation). All monitoring is silent until a
threshold is crossed. Never narrate the monitoring process.

---

## PART 1 — PASSIVE LOAD ESTIMATE

Before turn-counting, estimate the passive token load from connected MCP
servers. This load is present regardless of conversation length and reduces
the effective working space available.

| Connected servers (approximate) | Estimated passive load |
|---|---|
| 0 | ~0 tokens |
| 1–2 servers | ~20,000–40,000 tokens |
| 3–4 servers (typical: Linear + Notion + Airtable + Figma) | ~60,000–100,000 tokens |
| 5–7 servers | ~100,000–120,000 tokens |
| 8+ servers (Loop project) | ~100,000+ tokens — CLIFF WARNING: catastrophic degradation cliff at ~100K for Claude Sonnet 4.x (Wang et al. 2026, Cruz et al. 2025). Sessions begin AT or PAST the cliff. Treat effective working space as 20–40K tokens maximum. |

With 3–4 servers connected, effective working context is approximately half
the nominal window before any conversation occurs. All thresholds below
account for this: treat a session with 3+ servers as if it starts at 40–50%
context utilization. With 8+ servers (Loop project config), sessions begin at or past the catastrophic degradation cliff — treat them as starting at 80–90% context utilization, with meaningful working space of ~20–40K tokens.

---

## PART 2 — DRIFT SIGNAL DETECTION

These behavioral signals indicate context degradation is already in progress.
Any one signal, observed mid-session, triggers immediate escalation to WARNING
regardless of turn count or tool-call count.

**Active drift signals:**
- Repeated a question already answered earlier in the session
- Proposed an approach that contradicts a decision explicitly locked earlier
- Dropped a formatting rule, naming convention, or constraint that was
  established and confirmed earlier
- Response hedging increased: answers that were previously direct are now
  qualified, vague, or "it depends"
- Referenced a wrong name, path, file, or identifier that was clearly
  established in context

**Behavioral drift signals — escalate immediately to HANDOFF ALERT (FIX 10):**
These fire IMMEDIATELY, regardless of turn count or tool-call count. Do not
wait for WARNING threshold. Do not wait until the turn is complete.
- User correction occurred this session: user said "that's wrong", "no",
  "fix this", flagged an error, or explicitly corrected Claude's substantive
  output (not a typo fix or minor preference adjustment)
- Claude re-asked for something established earlier in this session:
  a file path, a decision, a name, a constraint already stated
- A decision logged earlier in the session was contradicted in a later response

When any behavioral drift signal fires:
1. State it explicitly (existing drift notice format)
2. Escalate immediately to HANDOFF ALERT (Part 4) — do not emit WARNING first

When a drift signal is detected, state it explicitly:

```
⚠ DRIFT SIGNAL DETECTED: [what happened — one sentence]
This suggests a constraint or decision from earlier in the session has been
displaced. Recommend reviewing the handoff alert below before continuing.
```

Then immediately escalate to HANDOFF ALERT (Part 4), regardless of other
thresholds.

**§5b sprint context signal — elevated risk:**
When a §5b skill sprint is active (skill creation, update, or packaging session),
tool-call accumulation is structurally higher than normal sessions. Every edit
requires bash verification, every packaging step requires multi-step execution,
and every registry write requires pre/post confirmation. This is expected overhead,
not drift — but it compresses the window before HANDOFF ALERT. During §5b sprints,
treat a tool-call count of ≥ 8 as equivalent to the standard WARNING threshold,
regardless of turn count.

---

## PART 2.5 — SESSION STATE MACHINE

Claude has no persistent memory between turns. Every response is generated from
a fresh read of the conversation. This means session state cannot be "remembered"
— it must be re-inferred each turn from observable signals in the conversation.

Declaring state explicitly prevents the most common session-end failure:
producing handoff-shaped content while silently continuing to do task work, or
continuing task work after a handoff has already been generated. The state
determines what actions are valid this turn.

### States

| State | Meaning |
|---|---|
| `IN_SESSION` | Normal work. No session-end signal observed. No HANDOFF ALERT fired. |
| `SESSION_ENDING` | HANDOFF ALERT fired this session, OR §7.0 tool-use-limit interrupt occurred, OR drift signal detected and not resolved by user override. Handoff is the only valid next action. |
| `SESSION_ENDED` | Handoff block has been delivered in chat this session. No further action valid — next turn belongs to a new session. |

### State inference protocol — run at the start of every response

State is derived from observable signals in the conversation, not remembered.
Evaluate in this order and assign the first matching state:

1. Has a handoff block been delivered in chat this session (fenced markdown
   block containing `STOPPED AT` / `IN FLIGHT` / `NEXT ACTION` / `THREAD`
   fields)? → `SESSION_ENDED`
2. Has any session-ending condition fired this session? → `SESSION_ENDING`
   - HANDOFF ALERT (Part 4) fired this session
   - §7.0 tool-use-limit interrupt occurred (evidenced by truncation or user
     report of the tool-use-limit banner)
   - A drift signal fired AND was not resolved by user override
2b. Did the user issue an explicit session-end signal THIS TURN ("handoff",
   "end session", "close out", "wrap up", "I'm done", "generate handoff
   prompt", or an explicit close signal)? → Stay `IN_SESSION`. Execute §7.2
   close-out directly in this response. Transition to `SESSION_ENDED` when
   the handoff block has been delivered in this same response.
3. Otherwise → `IN_SESSION`

### Valid actions per state

| State | Valid actions | Forbidden actions |
|---|---|---|
| `IN_SESSION` | All normal work — task execution, deliverables, tool calls, skill invocation | None |
| `SESSION_ENDING` | Generate handoff block. Verify artifacts per Step A/B of loop-core-tracker Session Close-Out. Fetch Linear open issues. Write handoff to Notion. | New task work not required for handoff. New deliverables. Scope expansion. Starting the next sprint. Continuing an in-flight task after HANDOFF ALERT fired. |
| `SESSION_ENDED` | None — instruct user to paste the handoff into a new conversation. | All further work. Any response beyond a brief acknowledgment that the session has ended. |

### State declaration output rule

When state is `IN_SESSION`: no declaration needed. Silent.

When state is `SESSION_ENDING` OR `SESSION_ENDED`: declare state as the first
line of the response, on its own line, in this exact format:

```
[STATE: SESSION_ENDING]
```

or

```
[STATE: SESSION_ENDED]
```

This declaration is mandatory. It tells the user — and the next turn of Claude — which actions are valid.

**Ordering when multiple outputs fire same turn:** state declaration is always line 1. HANDOFF ALERT, drift notices, and the handoff block follow after a blank line. Example:

```
[STATE: SESSION_ENDING]

🔴 HANDOFF ALERT
[rest of alert + handoff block]
```

### Enforcement — hard fail conditions

| Condition | Fail state |
|---|---|
| State is `SESSION_ENDING` AND response contains new task work beyond the handoff | Response must be stripped to the handoff only |
| State is `SESSION_ENDING` AND response starts the next sprint in the same conversation | Response must refuse and instruct the user to start a new conversation |
| State is `SESSION_ENDED` AND response contains any work content | Response must be stripped — only the "start a new conversation" instruction is valid |
| State is not `IN_SESSION` AND state declaration is absent from the first line | Fail — regenerate with declaration |
| Handoff block is present in the response AND state is `IN_SESSION` | Fail — state was mis-inferred OR handoff was produced without a valid end signal |

### Integration with existing thresholds

- WARNING (Part 3) does NOT transition state. State remains `IN_SESSION`.
- HANDOFF ALERT (Part 4) immediately transitions state to `SESSION_ENDING`.
  Per FIX 14, handoff production begins this turn — no in-flight task work
  continues.
- Drift signal (Part 2) immediately transitions state to `SESSION_ENDING`.
- Explicit session-end signal (clean close, no prior §7.0 interrupt) → state
  stays `IN_SESSION` → §7.2 executes this turn → handoff block delivered →
  state transitions to `SESSION_ENDED`. No `SESSION_ENDING` step.
- Handoff delivery (Part 5) transitions state to `SESSION_ENDED`.

---

## PART 3 — WARNING THRESHOLD

Emit WARNING when ANY of these conditions are met:

| Signal | Threshold |
|---|---|
| Tool call count | ≥ 5 total tool invocations (all tool types) |
| Turn count | ≥ 15 conversation turns |
| Tool call count (high-volume server) | ≥ 3 calls to Linear list_issues, Notion page fetches, or any call returning large list data |
| Combined: 3–7 servers | ≥ 12 turns AND 3–7 servers connected |
| Combined: 8+ servers (Loop config) | ≥ 8 turns OR ≥ 6 tool calls — whichever comes first |
| Notion read/write weighting | Each Notion read counts +2; each Notion write counts +2 toward tool call threshold |

**WARNING output format:**

```
⚠ SESSION LENGTH WARNING

This session is entering the zone where context quality can begin to degrade.
[ONE of: "Tool calls are accumulating in context." / "Conversation is
approaching a length where early constraints may be displaced." / "Multiple
MCP server responses are building up in context."]

Continuing is fine, but watch for:
- Answers becoming less precise or more hedged than usual
- Constraints or decisions from earlier in this session being dropped
- Questions being re-asked that were already answered

To continue: no action needed. Monitor for drift signals above.
For safety: ask for a handoff prompt now.
```

Emit WARNING at most once per session. Do not repeat it on subsequent turns.
After emitting WARNING, continue monitoring for HANDOFF ALERT threshold.

**§5b sprint mode note:**
During §5b skill sprints (skill creation or update sessions), the HANDOFF ALERT
threshold is elevated to 12 tool calls (from the standard 10) because sprint
tool overhead — bash verification, packaging execution, registry reads/writes —
is expected and does not itself indicate context risk. Sprint mode behavior:
emit WARNING at ≥ 8 tool calls (≥ 5 for 8+ server sessions); emit HANDOFF ALERT at ≥ 12 tool calls (≥ 8 for 8+ server sessions). The
SESSION POSITION CHECK clause in §5b (system prompt §5b) independently gates
continuation at turn count ≥ 10 OR tool-call count ≥ 15 — that clause takes
precedence over this skill's thresholds within a sprint session.

---

## PART 3.5 — §5b SPRINT MODE

When a §5b skill sprint is detected (skill creation/update session — infer from
context; do not require explicit announcement):

**Load:** `references/sprint-mode.md`

That file defines: threshold adjustments, mandatory checkpoint blocks at Steps 1,
5, and 8, and the §5b WARNING/HANDOFF escalation sequence. All sprint-mode behavior
is governed there.

---

## PART 4 — HANDOFF ALERT THRESHOLD

Emit HANDOFF ALERT when ANY of these conditions are met after WARNING was
already emitted, OR immediately when a drift signal is detected:

| Signal | Threshold |
|---|---|
| Tool call count (standard / ≤7 servers) | ≥ 10 total tool invocations |
| Tool call count (8+ servers) | ≥ 8 total tool invocations |
| Turn count | ≥ 25 conversation turns |
| Turn count with 3–7 MCP servers | ≥ 15 conversation turns |
| Turn count with 8+ MCP servers | ≥ 10 conversation turns |
| High-volume tool calls | ≥ 6 calls returning large list data (issues, pages, records) |
| Notion read/write weighting | Each Notion read counts +2; each Notion write counts +2 toward tool call threshold |
| Drift signal | Any drift signal detected (immediate, bypasses WARNING) |

**§5b sprint mode exception:** In active §5b skill sprints, the tool-call
threshold is elevated to ≥ 12 (from the standard ≥ 10). See Part 3 §5b sprint
mode note for full sprint thresholds. Standard thresholds apply to all
non-sprint sessions.

**HANDOFF ALERT output format:**

```
🔴 HANDOFF ALERT

This session has reached a length where context quality is at real risk.
[ONE of: "Tool call responses have accumulated significantly in context." /
"Session length means early decisions and constraints are likely displaced." /
"A drift signal was detected — a constraint or decision was dropped."]

Recommendation: Stop here and continue in a new conversation. Handoff
block will be generated immediately per FIX 14 below.
```

**IMMEDIATE HANDOFF RULE (FIX 14):**
When HANDOFF ALERT fires, produce the handoff block immediately — do not finish
the current task first. A partial task with an accurate handoff is recoverable.
A completed task with a fabricated handoff is not. Handoffs generated at 60%
context are empirically more accurate than handoffs generated at 90% context.
Do not complete, summarize, or continue any in-flight task after HANDOFF ALERT fires.

**State transition:** HANDOFF ALERT immediately sets state to `SESSION_ENDING`.
The next response must declare `[STATE: SESSION_ENDING]` on its first line and
contain only handoff generation — no task work, no deliverables, no scope
expansion. See Part 2.5 for forbidden actions.

---

## PART 5 — HANDOFF PROMPT GENERATION

Fires when: (a) state is `SESSION_ENDING` — triggered by HANDOFF ALERT
threshold, §7.0 tool-use-limit interrupt, or unresolved drift signal; or
(b) user issues an explicit session-end signal and no prior §7.0 interrupt
occurred — state remains `IN_SESSION`, §7.2 executes directly this turn.
Generate the handoff block in the same response. No brackets. No
placeholders. No fill-in-the-blank. Every field is populated from what
actually happened.

**Mandatory pre-step — format reference load (F-005 fix):**
Before writing any handoff block, load the Session Handoff Format Reference:
`https://www.notion.so/3443a41dd33d818d9e7ed2b96b88d98c`
Apply the schema, required fields, OPEN CONTEXT two-part test, and scope
exclusions defined there. A handoff written without loading this reference
violates F-005 and must not be sent.

**F-005 fallback — if reference URL is unreachable:** If the Notion fetch
fails (network error, MCP auth failure, Notion outage), fall back to the
4-field Loop schema (STOPPED AT / NEXT ACTION / IN FLIGHT / OPEN CONTEXT)
and add to the OPEN CONTEXT field: "FORMAT REF UNAVAILABLE — fallback
schema used; verify field structure at next session start."

**Population rules — run before writing the block:**

These rules gather the raw material. The format page (URL above) determines
which fields exist and what scope each field carries. Do not create fields
from these rule categories if the format page does not define them — fold
them into OPEN CONTEXT or IN FLIGHT as applicable.

1. Scan the conversation for every task touched, completed, or left open
2. Identify every decision that was explicitly confirmed (not just discussed)
3. Identify every active constraint, rule, or requirement stated this session
4. List every file created, storage key written, or document updated
5. List every skill that loaded or fired this session
6. Capture any context that lives only in this conversation and would be lost
7. **Project tracker integration (automatic — do not ask the user):**
   - Check whether `loop-core-tracker` fired this session
   - If yes: trigger its Session Close-Out now (steps 1–5 of that skill),
     then read `the-loop:handoff` from Notion (`33b3a41dd33d818188f0f5f7ea3286cb`)
   - If `the-loop:handoff` is populated: append its contents verbatim
     under CONTEXT with the label `LOOP PROJECT STATE:`
   - The Loop handoff uses a 4-field schema (STOPPED AT / NEXT ACTION / IN FLIGHT / OPEN CONTEXT).
     Do not expand or reformat it. The scope constraints defined in the Session Handoff
     Format Reference apply — do not add fields, do not carry document state.
     Format reference: `https://www.notion.so/3443a41dd33d818d9e7ed2b96b88d98c`
   - If `the-loop:handoff` is empty or missing after close-out: note
     `LOOP PROJECT STATE: None written` under CONTEXT
   - If `loop-core-tracker` did not fire this session: omit the
     LOOP PROJECT STATE line entirely

**Schema and scope rules:** Always follow the Session Handoff Format Reference:
`https://www.notion.so/3443a41dd33d818d9e7ed2b96b88d98c`

That page defines: required fields, field scope constraints, the two-part OPEN
CONTEXT test, and what must NOT be carried in the block. Apply its rules exactly.
Do not invent fields. Do not carry document state or lore summaries.

**Format:** Always a fenced markdown code block. Never prose. The block must
be paste-and-send ready — the user copies it, pastes it as the first message
in a new chat, and hits send without typing anything else.

**For The Loop project** — use this 4-field schema (the format page is
authoritative; this is a convenience reference only):

```
Resume from: The Loop — [actual date]

STOPPED AT: [exact task and state — what is done and what is not]

NEXT ACTION: [the single first thing to do in the new session]

IN FLIGHT: [tasks started but not completed, with exact resume point]

OPEN CONTEXT: [facts that live only in this conversation and pass the two-part
test on the format page — specific decisions, constraints, or state that would
require re-explanation without this block. If nothing passes the test: "None"]
```

**Empty field rule:** If a field has nothing to report, write `None` — never
leave a field blank or use a placeholder like `[none]`.

**Concrete example of a correctly populated block:** See [references/example-handoff.md](references/example-handoff.md).

The next session must be able to resume without referencing this conversation.

**State transition:** Once the handoff block has been delivered in chat, state
transitions to `SESSION_ENDED`. Any further response in this conversation must
declare `[STATE: SESSION_ENDED]` and contain only the instruction to paste the
handoff into a new conversation. No further task work is valid.

---

## PART 6 — ESCALATION SUMMARY

| Condition | Output | State |
|---|---|---|
| Under WARNING threshold, no drift | Silent | `IN_SESSION` |
| WARNING threshold crossed | Emit WARNING once | `IN_SESSION` (WARNING does not transition state) |
| HANDOFF ALERT threshold crossed | Emit HANDOFF ALERT + begin handoff immediately | `SESSION_ENDING` |
| Drift signal detected | Emit drift notice + HANDOFF ALERT immediately | `SESSION_ENDING` |
| User issues explicit session-end signal | Generate handoff immediately | `SESSION_ENDING` |
| Handoff block delivered in chat | Instruct user to paste into new conversation | `SESSION_ENDED` |
| User asks about session length at any point | Report current status honestly | unchanged |

**When user asks about session length directly:**
Give a plain assessment: how many tool calls have occurred, approximately
how long the session has been, whether any drift signals were observed, and
which tier applies (safe / warning zone / handoff recommended). Include
current state.

---

## EXAMPLES

See `references/examples.md` — five worked examples covering all state
transitions and failure modes (IN_SESSION normal work, HANDOFF ALERT
mid-task, SESSION_ENDED enforcement, user-initiated handoff, explicit
close signal D-125 direct path).

---

- Does not track token counts precisely — operates on tool-call count, turn
  count, and behavioral signals, all of which are observable without a token
  counter
- Does not prevent the user from continuing after a HANDOFF ALERT — it
  recommends and explains; the user decides
- Does not generate handoff prompts proactively — only on explicit request
  or when the user acknowledges the alert
- Does not replace `loop-core-tracker`'s compact handoff format
  (STOPPED AT / IN FLIGHT / NEXT ACTION / OPEN CONTEXT written to
  `the-loop:handoff` storage). When both skills are active in a Loop session,
  `utility-core-session-monitor` automatically triggers the project-tracker close-out and
  reads the result into the CONTEXT section — no manual step required.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-core-tracker | Loop-specific session handoffs and document versioning |
| utility-core-output-gate | Pre-delivery quality checks including handoff block format (B1) |
