---
name: utility-failure-analyst
description: >
  Diagnoses Claude response failures across past conversations. Produces
  severity-ranked findings, specific root causes, and classified fix proposals
  (STRUCTURAL/TEMPORAL/BEHAVIORAL). Routes to correct triage pattern based on
  request signal. Use automatically — do not wait to be asked. Trigger on ANY
  of these signals: "what went wrong", "run a diagnostic", "audit last N
  sessions", "this keeps happening", "did the fix hold", "triage session
  failures", "failures in [domain]", "post-implementation check", session ends
  with multiple user corrections, repeated frustration with Claude behavior,
  user says "that was wrong" / "you got that wrong" / "that's incorrect" mid-session,
  Claude catches its own error pre-output via output-gate or any internal check (self-reporting).
  Do NOT use for: single isolated one-off correction with no recurrence signal;
  lore canon checks; pre-delivery quality gate; real-time session monitoring.
  Load once per session.
---
gates_passed: 2026-05-24
SKILL_VERSION: v1.8.0

# utility-failure-analyst

Project-agnostic diagnostic tool for identifying, classifying, and systematically
fixing Claude response failures. Routes to one of 5 triage patterns.

Type: dispatcher

---

## GOTCHAS

1. **Step E skipped** — DUP-vs-HB routing breaks silently; all recurrence findings misclassify as DUP. HARD FAIL is the only structural prevention.
2. **Root cause labeled "skill not loaded"** — symptom, not mechanism. Must name why: trigger mismatch, session length, wrong skill domain. Stub root causes block Fix Block generation.
3. **Fix Block self-review absent** — required output field. A report missing it is malformed.
4. **Q-RC1/2/3 not produced visibly** — absence is a format error that blocks Fix Block generation.
5. **Reference files not loaded** — running taxonomy, heuristics, or D1 queries from memory = silent degradation. Always load via explicit `view` before the relevant pass.
6. **Self-reporting skipped when skill not loaded** — PART 5b fires only if issue-triage is already in context. If output-gate catches an error in a session where issue-triage hasn't loaded, fix silently and log in the next triage session.

---

## PART 0 — TRIAGE PATTERN ROUTING

This skill is a triggered tool, not an autonomous monitor. LLMs cannot reliably
detect session quality in the same generation context that produced the failures
[arxiv 2512.20578]. Explicit invocation is correct.

| Signal | Pattern |
|---|---|
| "what went wrong in that session", single session | Pattern 1 — Post-mortem |
| "this keeps happening", "last N sessions", recurrence | Pattern 2 — Cross-session |
| "is this skill working", "audit this skill", methodology | Pattern 3 — Methodology |
| "did the fix hold", "post-implementation check" | Pattern 4 — Verification (CAPA) |
| recurrence signal after a prior fix was applied | Pattern 4 first — verify implementation before new diagnosis |
| "failures in [domain]", named subsystem failure | Pattern 5 — Domain-scoped |

Load `references/triage-patterns.md` for per-pattern protocol detail and window selection table.

**Pre-session open-findings gate (required before any triage pattern):**
Before any pass starts, run from the claude-skills repo:
1. `python3 /home/claude/cs-work/ci/check_open_findings.py --emit-sql`
2. Execute the emitted SQL via Cloudflare MCP on claude-config D1 (afd78e0e-583e-4e78-87fc-dd6bc8150ce9)
3. `python3 /home/claude/cs-work/ci/check_open_findings.py --json '<D1 results>'`

Exit 0 → proceed. Exit 1 → OPEN blocking findings — resolve each or pass `--override "<justification>"` before proceeding. Exit 2 (P-07-class only) → proceed.
Repo absent: `git clone https://<PAT>@github.com/Farm-Grind/claude-skills.git /home/claude/cs-work` — PAT from `SELECT value FROM secrets WHERE key = 'GITHUB_PAT'` (D1 above).

---

## PART 1 — FAILURE TAXONOMY

Load `references/failure-taxonomy.md` before Pass 2 classification. Running from memory is not permitted.

Contains: 15 failure categories (SK, LC, DR, HL, FMT, IH, A7, SY, DUP, MCP-W, CTX, VOI, WL, HB, CI), 4 severity levels (CRITICAL/HIGH/MEDIUM/LOW), fix category taxonomy (STRUCTURAL/TEMPORAL/BEHAVIORAL), HB fix_category_floor rule.

---

## PART 2 — SCAN PROTOCOL

**Step E — Error log baseline (run before Pass 1):**

Load `references/d1-queries.md` and run the Step E query. Classify results into three buckets (CONFIRMED OPEN / IMPLEMENTED STILL FAILING / RESOLVED) per the bucket table in that file.

If D1 unavailable or error_log empty: note it, skip DUP-vs-HB routing — all recurrence findings default to DUP.
HARD FAIL: Step E must be attempted before Pass 1.

**Pass 1 — Broad scan:**

Load `references/failure-heuristics.md` to guide flagging.

1. Read full exchange — both human and Claude turns.
2. Flag turns where output does not match system prompt, preferences, corrections, or prior sessions.
3. Mark each: conversation ID, turn number, suspected category, one-line anomaly.
4. Do not deep-dive. Flag and move on.

**Pass 2 — Deep classification:**

Before confirming any root cause, produce visibly (absence = format error, blocks Fix Block):
```
Q-RC1: [Visible symptom — the observable wrong output, one sentence]
Q-RC2: [Mechanism — why it happened. "Skill not loaded" is NOT a mechanism.]
Q-RC3: [Architectural layer: system prompt / user preferences / skill / inline]
```
For compound failures: one Q-RC1/2/3 block per mechanism.

For DR findings, classify before proposing fix:
```
Rule type: [OMISSION ("never X") / COMMISSION ("always Y")]
```
Omission rules decay under context depth [arxiv 2604.20911]. Fix: rewrite as commission-type OR add structural enforcement. Adding another omission rule is prohibited.

DUP-vs-HB routing: check Step E bucket results before classifying any recurrence as DUP.

**Pass 3 — Pattern synthesis:**
1. Group findings by category. Identify 2+ in same category — systemic, not isolated.
2. For each systemic pattern: identify single intervention most likely to prevent recurrence.
3. Distinguish one-off fixes vs. structural fixes.
4. **Layer execution order:** If Fix Block has multi-layer fixes, append: `Fix sequence: [layer1] (1st) → [layer2] (2nd)`. Omit if all independent.

If any reference file is missing: `⚠ [filename] not found — running degraded. Queue skill maintenance item.` Always proceed.

Reference files do not persist across turns — re-view each turn that uses them.

---

## PART 3 — OUTPUT FORMAT

**Clean scan:**
```
DIAGNOSTIC  [date]  [N] convos  Nc:0  Nh:0  Nm:0
Scanned    [convo IDs or date range]
Result     No failures identified in window.
Queue      none
Log        none
```

**Standard output block:**
```
DIAGNOSTIC  [date]  [N] convos  Nc:X  Nh:X  Nm:X
Scanned    [convo IDs or date range]
Blocker    none  (or: F-001 -- [what it prevents])
Patterns
  P-001  [Name]: [mechanism] (F-001, F-005)
Critical
  F-001  CTX  [Title]  --  root: [cause]  --  ref: [convo title]
High
  F-002  SK   [Title]  --  root: [cause]  --  ref: [convo title]
Fixes
  P-001  [verb: specific action -- skill name / §number]
Fix Block self-review:  [per Part 4b — or "all one-off fixes, no structural changes"]
Queue  [N new ops_queue items written — IDs: OPS-XXX]
Log    [N new error_log entries written — IDs: ERR-XXX]
```

**Fix Block self-review is a required output field. A report missing it is malformed.**

**Fix Block format:**
```
FIX-XXX: [Title]
Addresses:           [PATTERN-XXX / F-XXX]
Action:              [Skill name + section + new behavior]
Fix category:        [STRUCTURAL / TEMPORAL / BEHAVIORAL]
Research basis:      [Citation. If none: UNVERIFIED — must be DEFERRED.]
STRUCTURAL note:     [Required if BEHAVIORAL — STRUCTURAL option considered and why rejected]
Regression assertion:
  Target behavior changes: [specific behavior this fix changes]
  Must NOT change:         [1-3 behaviors at same layer that must be unaffected]
  Validation scenario:     [conversation scenario to confirm fix worked]
Priority:            [IMMEDIATE / NEXT SESSION / DEFERRED]
Status:              PROPOSED
```

Status is always PROPOSED at delivery. A different session advances it to VALIDATED.

For D1 write patterns (IMMEDIATE items, queue depth check, error_log INSERT): load `references/d1-queries.md`.

---

## PART 4 — FIX GENERATION RULES

**Rule 1 — Root cause, not symptom.** Fix must address the mechanism that produced the failure, not the visible output error.
**Rule 2 — Structural over one-off.** 2+ occurrences of same failure type → fix must be structural.
**Rule 3 — Holistic synthesis.** Check for conflicts. Group related fixes. Never propose conflicting instructions.
**Rule 4 — Specificity gate.** Every fix names: what changes, where (skill / rule / section), new behavior. Any fix claiming to address a named failure path (citing a specific F-XXX, a session failure, or a named pattern instance) MUST include: (a) exact failure path quoted from the source finding, (b) mechanism trace — the execution step where the fix intercepts the failure. Missing either field → fix is malformed; HARD FAIL.
HARD FAIL: Never deliver a Fix Block with any fix that fails the specificity gate.
**Rule 5 — Priority assignment.** IMMEDIATE = prevents active failure or blocks work. NEXT SESSION = quality improvement, no active incident. DEFERRED = low-severity or needs more data.
**Rule 6 — Layer specification.** Every fix names its architectural layer. Verify the rule lives there.
HARD FAIL: Never deliver a Fix Block with an unverified target layer.
**Rule 7 — STRUCTURAL-first mandate.** For recurring failures or HB: (a) enumerate STRUCTURAL option; (b) if feasible STRUCTURAL exists: BEHAVIORAL is PROHIBITED; (c) if no STRUCTURAL: state why explicitly, then use TEMPORAL before BEHAVIORAL. Required visible: `STRUCTURAL considered: [evaluated / why rejected or adopted]`.
Before generating any fix for a finding: query `SELECT severity FROM failure_patterns WHERE pattern_code = '[code]'` (claude-config D1). If severity = CRITICAL: emit `⛔ CRITICAL PATTERN — BEHAVIORAL fix PROHIBITED. Structural option must be documented and explicitly rejected before any other fix type is accepted.` This banner must appear in the Fix Block before Part 4c runs. Absence = HARD FAIL.
**Rule 8 — HB fresh-context protocol.** HB requires a SEPARATE EVALUATION SESSION. (a) Produce Q-RC1/2/3. (b) Produce DIAG-handoff with transcript segments, prior fix implementation, diagnostic questions. (c) DO NOT propose new fix for HB in same session. Visible: `HB finding — fix proposal deferred to fresh-context session per Rule 8.`
**Rule 9 — CI script mechanism analysis.** Any proposed fix involving a CI script, validation script, or post-hoc output check MUST include a visible mechanism analysis block before Part 4c:
```
CI MECHANISM ANALYSIS
Failure mode targeted: [what fails]
Emission type: [OMISSION (never-X rule missed) / NON-OMISSION (confident incorrect claim, scope misrepresentation)]
CI intercept point: [pre-emit / post-emit / commit-time]
Viable: [YES — CI fires before failure / NO — post-hoc, cannot intercept non-omission]
Citation: [R-074 or equivalent]
```
HARD FAIL: NON-OMISSION + post-emit intercept = CI cannot catch this failure. BEHAVIORAL or ACCEPTED_LIMITATION only. [R-074]
**Rule 10 — Infrastructure domain check.** Any fix proposing changes to storage, platform capabilities, or tool integrations MUST include a visible prior-failure check before fix generation:
```sql
SELECT finding_id, title, fix_applied FROM granular_findings
WHERE fix_applied LIKE '%[domain keyword]%' OR root_cause LIKE '%[domain keyword]%'
ORDER BY finding_id
```
(claude-config D1 — afd78e0e-583e-4e78-87fc-dd6bc8150ce9). All matching findings must be cited and addressed before the proposal proceeds. Absence of query = HARD FAIL.
Triggered-tool note: if not explicitly invoked, verify signal before proceeding [arxiv 2512.20578].
**Rule 11 — Skill registry and prior-findings gate.** Before generating any Fix Block that names a specific skill or fix target, two queries are MANDATORY — results must be visible in the same response turn as the Fix Block:
1. Skill existence check:
```sql
SELECT name, status FROM skills WHERE name = '[named skill]'
```
(claude-config D1). If no row returns or `status ≠ ACTIVE`: named target is invalid. HARD FAIL — do not propose changes to a non-existent or retired skill. Reclassify fix target before proceeding.
2. Prior-findings deduplication check:
```sql
SELECT finding_id, title, status FROM granular_findings
WHERE root_cause LIKE '%[pattern keyword]%' OR pattern_code = '[code]'
ORDER BY finding_id
```
(claude-config D1). All matching prior findings must be cited in the Fix Block. If an existing OPEN finding covers the same mechanism: cross-reference it (`"Recurrence of F-XXX"`) rather than inserting a duplicate.
HARD FAIL: Any Fix Block naming a specific skill target without both query results visible this turn.

---

## PART 4b — FIX BLOCK ADVERSARIAL SELF-REVIEW

Run after completing Fix Block, before delivering the report. Block delivery until confirmation block is produced.
For each fix:
1. **What is the failure mechanism?** (Not symptom — mechanism.)
2. **What layer does this fix target?**
3. **Is that layer reachable when the failure mechanism is active?** If No: mark WL; rewrite before delivering.
**HB special rule:** Run Part 4c before this sequence. BEHAVIORAL for HB = hard fail at 4c. Once 4c passes, this sequence is mandatory — prior analyst already answered Q3 as Yes and was wrong.

**Q4 — Counterfactual test:**
```
Q4: If this fix had been in place, would the diagnosed conversation have produced correct output?
  Yes       → proceed.
  No        → fix addresses different mechanism. Reanalyze with Q-RC1/2/3.
  Uncertain → flag explicitly. For HB: Uncertain = defer to fresh-context per Rule 8.
```
For BEHAVIORAL/TEMPORAL fixes: mark UNCERTAIN by default unless specific transcript evidence shows mechanism was addressable in-context.
**Confirmation block (required for any Fix Block with structural fixes):**
```
Fix Block self-review:
  [Fix ID]  Mechanism: [stated]  Layer: [named]  Survives mechanism: [Yes/No]
            Q4: [Yes / No / Uncertain — reason]
  Status: CLEAR to deliver / BLOCKED — [reason]
```
HARD FAIL: Do not deliver a Fix Block with structural fixes without this block.
---

## PART 4c — FIX QUALITY GATE

Run before Part 4b for every fix. Mandatory for HB; required for structural fixes.

| Q1: Model judgment required? | Q2: External tool / format constraint / bash? | Q3: Visible output in separate turn? | Category |
|---|---|---|---|
| YES | NO | NO | BEHAVIORAL |
| YES | NO | YES | TEMPORAL |
| YES | YES | — | STRUCTURAL |
| NO | YES | — | STRUCTURAL |
| NO | NO | YES | TEMPORAL |
| NO | NO | NO | Insufficient evidence — rewrite |

"Better criteria" or "clearer language" fails Q1 regardless — self-attribution bias operates within generation context [arxiv 2603.04582].
HB gate: Proposed category must be ≥ TEMPORAL. BEHAVIORAL for HB = hard fail.
HARD FAIL: Never run Part 4b on a BEHAVIORAL fix for an HB finding.

**Output block (required for every fix):**
```
Fix Quality Gate:
  [Fix ID]  Q1: [Y/N]  Q2: [Y/N]  Q3: [Y/N]  → [STRUCTURAL / TEMPORAL / BEHAVIORAL]
  HB gate: [PASS / HARD FAIL — rewrite required]
```

---

## Examples

**Example 1 — Clean scan (P1):**
```
DIAGNOSTIC  2026-05-12  2 convos  Nc:0  Nh:0  Nm:0
Scanned    2026-05-11 to 2026-05-12
Result     No failures identified in window.
Queue      none
Log        none
```

**Example 2 — Standard finding with Fix Block (P2):**
```
DIAGNOSTIC  2026-05-12  4 convos  Nc:0  Nh:1  Nm:0
Scanned    2026-05-09 to 2026-05-12
Patterns
  P-001  FMT: fenced block omitted for copy-paste content (F-001, F-002)
High
  F-001  FMT  Fenced block missing  --  root: A7 rule absent from Q-RC3 scan scope  --  ref: "Design session"
  F-002  FMT  Same failure recurred  --  root: same mechanism, fix not applied  --  ref: "Code session"
Fixes
  P-001  Add: user preferences A7 to Q-RC3 scope in system prompt §3
Fix Block self-review:
  P-001  Mechanism: A7 absent from Q-RC3 scope  Layer: system prompt  Survives mechanism: Yes
         Q4: Yes  Status: CLEAR to deliver
Queue  OPS-041 (P2-blocking, skill-edit, QUEUED)
Log    ERR-014 (FMT, HIGH, OPEN)
```

**Example 3 — HB finding, fix deferred:**
```
DIAGNOSTIC  2026-05-13  3 convos  Nc:1  Nh:0  Nm:0
Step E     E-007 WL, queue_status = DONE — same WL recurs → HB
Critical
  F-001  WL(HB)  Wrong-layer fix recurred post-implementation
         root: B-check in skill not loaded during sprint sessions
         ref: "Sprint close-out"
Fixes
  HB finding — fix proposal deferred to fresh-context session per Rule 8.
DIAG-handoff:
  Failure segment: [transcript ref]  Prior fix: B-check added to output-gate skill §3 (now retired)
  Diagnostic question: What skill IS loaded in sprint sessions? Fix must target that layer.
Fix Block self-review:  HB — no fix proposed this session.
Queue  none
Log    ERR-007 updated (HB escalation)
```

---

## PART 5 — AUTO-WRITE PROTOCOL

Runs after PART 3 output whenever findings exist. Writes to **claude-config granular_findings only** — findings log, not fix queue. ops_queue and error_log writes remain gated; they execute only after a fix is validated by a separate session.

**Step 1 — Check MCP availability:**
Attempt `d1_database_query` on claude-config. If it fails: emit findings as SQL block (see d1-queries.md §Failure Audit INSERT) and stop. If it succeeds: proceed.

**Step 2 — Assign finding ID:**
```sql
SELECT 'F-' || printf('%03d', MAX(CAST(SUBSTR(finding_id,3) AS INTEGER)) + 1)
FROM granular_findings
```

**Step 2b — Fix type gate (required before Step 3):**
For each finding with a classified fix_type from Part 4c, run before INSERT:
```bash
python3 /home/claude/cs-work/ci/check_fix_type.py --pattern <pattern_code> --fix-type <fix_type>
```
Exit 1 = HARD FAIL — BEHAVIORAL fix for a recurring pattern; reclassify before proceeding to Step 3.
Exit 2 = WARN — document justification before INSERT.
Repo path: /home/claude/cs-work/ci/ (clone if absent — see PART 0 gate above).

**Step 3 — INSERT each new finding:**
Load `references/d1-queries.md` §Failure Audit INSERT. Execute for every finding produced in PART 3. Map fields:
- `pattern_code` — from failure taxonomy P-01 through P-12 (closest match; use P-12 if context-switch, P-03 if behavioral/self-attestation, P-09 if partial output, P-10 if position/spec drift)
- `fix_type` — from Fix Quality Gate output (STRUCTURAL / TEMPORAL / BEHAVIORAL)
- `status` — always OPEN on insert; only Claude that resolves it sets RESOLVED
- `project_scope` — UNIVERSAL unless finding is demonstrably project-specific (name the project)
- `source_conversation` — current conversation URL if known; else NULL

**Recurrence rule:** If the same failure mechanism recurs (same category + root cause as an existing entry), add a new finding and cross-reference the original ID in notes: `"Recurrence of F-XXX."` Never overwrite the original entry.

**WONT_FIX status:** Valid only when root cause confirms no feasible prevention (non-reproducible, context-specific, or demonstrably out of scope). Set `status: WONT_FIX`, add justification to notes field. Never use to avoid investigation.

**Step 4 — Sync CI:**
Query D1 for PAT (see d1-queries.md §Failure Audit INSERT "Get PAT for CI sync"), then execute:
```bash
cd /home/claude/cs-push
git pull origin main
# Update only the open_findings array in ci/failure-audit-rules.json:
python3 - << 'EOF'
import json
from pathlib import Path
# Findings list comes from Step 4 D1 query result — substitute actual rows below
open_findings = []  # populated from D1 query output
p = Path("ci/failure-audit-rules.json")
data = json.loads(p.read_text())
data["open_findings"] = open_findings
data["_meta"]["last_synced"] = "YYYY-MM-DD"  # today's date
p.write_text(json.dumps(data, indent=2))
EOF
git add ci/failure-audit-rules.json
git commit -m "sync: failure audit findings [F-XXX added]"
git push origin main
```
HARD FAIL: if git push fails, emit the updated open_findings JSON as a fenced block for the next connected session.

**Step 5 — Report in diagnostic output:**
Append to the Log line: `[N findings written to claude-config granular_findings: F-XXX, F-YYY]`
If MCP unavailable: `[MCP unavailable — SQL blocks emitted for manual execution]`

**HARD FAIL:** Never skip Step 4 after a successful Step 3 write — findings in D1 that aren't in the CI JSON are invisible to static enforcement.

---

## PART 5b — SELF-REPORTING PROTOCOL

Fires in-session when Claude catches its own error pre-output (via output-gate, any internal post-generation audit, or any skill check that fires a warning flag). Only active if issue-triage is loaded in the current session — see GOTCHA 6.

1. Fix the error silently — present clean output only.
2. Write to error_log via D1 (load `references/d1-queries.md` §error_log INSERT):
   - `status: OPEN`
   - `fix_applied: "Caught pre-output and corrected"`
   - All other fields populated from context. Use `"Unknown — requires investigation"` for root_cause if mechanism is unclear; never omit.
3. Append a brief note after the output:
   `⚠ ERR-XXX self-logged — [short description of what was caught and corrected].`

Step 2b fix-type gate applies. Self-reported entries use the same INSERT pattern as PART 5 Step 3 (granular_findings writes are not required for self-reported entries — error_log only).

---



- Does NOT fix failures — diagnoses and proposes only.
- Does NOT auto-detect session quality — requires explicit invocation.
- Does NOT verify lore canon — use project lore-checker for LC findings.
- Does NOT generate code fixes — use project code-guardian.
- Does NOT monitor context length — @monitor in utility-session-manager handles this.
- DOES write findings to claude-config granular_findings automatically — see PART 5.
- Does NOT write to ops_queue or error_log autonomously — EXCEPT via self-reporting protocol (PART 5b); all other error_log writes execute only after fix is validated.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| error_log (D1: the-loop-storage) | Source for self-reporting, WONT_FIX, and recurrence cross-ref — table: error_log, columns: id, description, root_cause, severity, status, fix_applied |
| cloudflare-storage_v1_3 | D1 query patterns, schema, queue submission |
| triage-reference_v1 | Constraint budget, removal-before-addition protocol |
| diagnostic-process-research-synthesis_v1_0 | Research grounding for Changes 1–5 |
| references/failure-taxonomy.md | 15 failure categories, severity levels, fix taxonomy |
| references/triage-patterns.md | Per-pattern capsules, window selection |
| references/failure-heuristics.md | 14 Pass 1 detection heuristics |
| references/d1-queries.md | Step E SQL, D1 write patterns, queue submission |
