# Triage Pattern Reference

## Per-Pattern Capsules

**P1 — Post-mortem:** Single session review. Scope 1–2 convos. Pass 1 → Pass 2 only; skip Pass 3. Output cap 3 fix items. No D1 writes required if no structural fixes identified.

**P2 — Cross-session:** Recurrence detection. Scope 5+ convos / 3+ sessions. Step E mandatory. All 3 passes. Deliverable = patterns not individual findings. Output cap 5 fix items. Check queue depth before any insert.

**P3 — Methodology:** Skill audit. Load and read the target skill in full. Evaluate trigger accuracy, output quality, implementation rate across recent sessions. Fix block targets the skill file directly.

**P4 — Verification (CAPA):** Implementation check. Run Step E first to find IMPLEMENTED items (queue_status = DONE). Run PROPOSED backlog check (d1-queries.md) — any error_log item with status=OPEN and queue_item=NULL that has a category match in the current scan window is an HB-candidate; these are prior findings proposed but never actioned and carry the same risk class as IMPLEMENTED STILL FAILING. Scan since implementation date for recurrence of the same failure category. Recurs → classify HB, auto-escalate CRITICAL. Clear → advance error log status to VALIDATED. Run P4 before scanning for any new failures in the same window.

**P5 — Domain-scoped:** Named subsystem audit. Use conversation_search with domain-specific keywords. Findings scoped to that domain only. Fix block targets the domain's owning skill or layer.

## Window Selection

| Signal | Window |
|---|---|
| "last hour" / "last session" | 1–2 most recent conversations |
| "last day" / "today" | All conversations in last 24 hours |
| "last N conversations" | Exactly N most recent conversations |
| No window specified | Default: last 24 hours |

Load via `recent_chats`. Paginate if needed (max 20 per call). Stop at window boundary. Log the window used at the top of the report.
