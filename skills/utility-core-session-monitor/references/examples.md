# Session Monitor — Worked Examples

Loaded on demand. Contains five examples covering all state transitions and
failure modes.

---

**Example 1 — Normal work, state stays IN_SESSION**

Session is 8 turns in. 2 MCP calls made. No drift signals. User asks a
design question.

State inference: no handoff delivered → check signal 2 → no session-end
signals → state = `IN_SESSION`.

Response behavior: answer the question normally. No state declaration.
Silent monitoring continues.

---

**Example 2 — HANDOFF ALERT mid-task triggers SESSION_ENDING**

Session is 22 turns in. 8 MCP calls made. User asks Claude to continue a
code refactor. On evaluating thresholds, HANDOFF ALERT fires (turn count
+ MCP calls combined).

State inference: HANDOFF ALERT just fired → state = `SESSION_ENDING`.

Response behavior — FAIL case: Claude completes the refactor, then appends
the HANDOFF ALERT at the end. This violates the immediate-handoff rule and
the forbidden-action rule for SESSION_ENDING.

Response behavior — PASS case:

```
[STATE: SESSION_ENDING]

🔴 HANDOFF ALERT

Session length has reached a point where context quality is at real risk.
Stopping the refactor mid-way. The handoff block below captures current
state so the next session can resume cleanly.

[handoff block follows with current file, line number, what was done,
what remains]
```

No further task work is performed this turn. The refactor resumes in a new
session with the handoff as context.

---

**Example 3 — SESSION_ENDED enforcement**

Handoff block was delivered in the previous Claude turn. User replies
"thanks, also one more quick question — can you just fix this one line?"

State inference: handoff block present in conversation → state =
`SESSION_ENDED`.

Response behavior — FAIL case: Claude answers the question. This violates
the SESSION_ENDED forbidden-action rule.

Response behavior — PASS case:

```
[STATE: SESSION_ENDED]

This session already closed with a handoff. Paste the handoff block into
a new conversation and I'll pick up the question there — starting fresh
keeps the next session clean and the handoff accurate.
```

---

**Example 4 — User-initiated handoff mid-sprint**

User is in the middle of a multi-sprint chain. They say "generate handoff
prompt" — explicit session-end signal, but no HANDOFF ALERT threshold fired.
Sprint is incomplete.

State inference: signal 1 no handoff delivered yet → signal 2 user said
"generate handoff prompt" → state = `SESSION_ENDING`.

Response behavior — FAIL case: Claude completes the current sprint task first,
then produces the handoff. This violates SESSION_ENDING forbidden-action rules
(no new task work beyond the handoff).

Response behavior — PASS case:

```
[STATE: SESSION_ENDING]

Sprint stopping here per your request. Handoff captures current state — next
session resumes with the remaining work.

[handoff block with IN FLIGHT: current sprint — exact file, line, and
remaining edits; EXECUTION CONTEXT for next session; THREAD field set]
```

No additional task work is attempted. The sprint resumes in a new session.

---

**Example 5 — Explicit close signal, no interrupt (D-125 direct path)**

Session is 8 turns in. No HANDOFF ALERT fired. No tool-use-limit interrupt.
User says "end session" — an explicit session-end signal.

State inference: no handoff delivered → user said "end session" → state = `SESSION_ENDING`.

Response behavior — FAIL case: Claude outputs "Close-out pending. Say continue
to run it." and stops. This is a process failure — the "Close-out pending" pause
exists ONLY for §7.0 tool-use-limit interrupt recovery. For a clean explicit
close signal with no prior interrupt, the pause is pure overhead. (D-125)

Response behavior — PASS case: Claude loads the Session Handoff Format Reference,
runs §7.2 close-out (Notion write, Linear fetch, verification), and produces the
fenced handoff block in the same response:

```
[STATE: SESSION_ENDING]

Here's the handoff block — paste this at the start of your next session to resume.

[fenced handoff block — all fields populated from verified session state]
```

The format reference load, Notion write, and Linear fetch all happen before the
handoff block is produced. No user prompt required between session-end signal and
handoff delivery.
