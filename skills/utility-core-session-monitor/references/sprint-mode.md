# Sprint Mode — §5b Session Monitor Reference

Loaded by `utility-core-session-monitor` when a §5b skill sprint is detected.

A §5b sprint is active when the conversation contains explicit signals of a skill
creation or update session: skill file paths loaded, utility-core-skill-gate
invoked, §5b referenced in the session preamble or user instruction, or a skill
packaging task is underway. Infer from conversation context; do not require an
explicit announcement.

---

## Threshold adjustments for §5b sprints

During §5b sprints, tool-call accumulation is structurally higher than normal
sessions. Every edit requires bash verification, every packaging step requires
multi-step execution, and every registry write requires pre/post confirmation.
This is expected overhead, not drift — but it compresses the window.

| Threshold | Standard | §5b Sprint |
|---|---|---|
| WARNING | ≥ 5 tool calls | ≥ 8 tool calls |
| HANDOFF ALERT | ≥ 10 tool calls | ≥ 12 tool calls |
| 8+ server WARNING | ≥ 6 tool calls | ≥ 6 tool calls (unchanged) |
| 8+ server HANDOFF | ≥ 8 tool calls | ≥ 8 tool calls (unchanged) |

The SESSION POSITION CHECK clause in §5b (system prompt §5b) independently gates
continuation at turn count ≥ 10 OR tool-call count ≥ 15 — that clause takes
precedence over this skill's thresholds within a sprint session.

---

## Sprint Status Display — Mandatory Checkpoints

MUST emit a brief status block at three checkpoints. Skipping any checkpoint
is a hard fail.

**Checkpoint 1 — Step 1 (sprint start):**
MUST emit once, after loading skill files and before executing any edits:

```
⚙ SPRINT STATUS [step 1/10]
Tool calls so far: [N] | Sprint threshold: 12 | Remaining: [12–N]
Session turns: [N] | Position check gate: ≥ 10 turns OR ≥ 15 calls
```

**Checkpoint 2 — Step 5 (mid-sprint, post-Gate 8b):**
MUST emit once, after Gate 8b adversarial review completes and before registry write.
Evaluate the condition and emit only the quoted text when true:

```
⚙ SPRINT STATUS [step 5/10]
Tool calls so far: [N] | Sprint threshold: 12 | Remaining: [12–N]
[If N ≥ 8: emit → ⚠ Approaching sprint WARNING threshold — proceed, but watch for gate failures]
[If N ≥ 12: emit → 🔴 Sprint HANDOFF ALERT — stop here, handoff before registry write]
```

**Checkpoint 3 — Step 8 (post-packaging, pre-delivery):**
MUST emit once, after .skill file is packaged and before present_files.
Evaluate condition and emit only the quoted text when true:

```
⚙ SPRINT STATUS [step 8/10]
Tool calls so far: [N] | Sprint threshold: 12 | Remaining: [12–N]
[If N ≥ 12: emit → 🔴 Session at capacity — deliver gate block and present_files only, then close out]
```

**Mini-example — Checkpoint 2 at 9 tool calls:**
```
⚙ SPRINT STATUS [step 5/10]
Tool calls so far: 9 | Sprint threshold: 12 | Remaining: 3
⚠ Approaching sprint WARNING threshold — proceed, but watch for gate failures
```

Status blocks are brief and non-disruptive. They do not replace WARNING or
HANDOFF ALERT — they are supplementary visibility for sprint sessions. If
HANDOFF ALERT fires at any checkpoint, it takes precedence and the sprint stops.
