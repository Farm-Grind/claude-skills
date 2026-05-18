# Failure Audit System — Operating Procedures

**Location:** ci/OPERATING-PROCEDURES.md  
**Scope:** Universal — applies to all sessions using the failure audit system  
**Last updated:** 2026-05-18 (session 3)

These procedures cover operational gaps not encoded in CI scripts or D1 schema.
Machine-enforced rules live in CI scripts. Human-judgment decisions live here.

---

## PROC-01 — P-06 Facsimile: Turn-Splitting Procedure

**Trigger:** Any task requiring a skill that is loaded via SKILL.md (utility-issue-triage,
utility-skill-publisher, persona-developer, etc.).

**Problem:** A facsimile response is produced when Claude generates skill output from memory
without actually loading the SKILL.md. This looks correct but bypasses all gates encoded
in the skill file. Logged as F-036 (P-06, OPEN).

**Definition of turn 1 and turn 2:**

Turn 1 — LOAD ONLY. Claude's output in turn 1 must be:
- The `view` tool call on the SKILL.md path (and any reference files the skill specifies)
- A one-line acknowledgment that the skill is loaded: "Loaded [skill name]. Proceeding."
- Nothing else. No analysis, no output, no gate pre-emption.

Turn 2 — EXECUTE. Claude applies the skill exactly as specified, starting from PART 0 or
the equivalent entry point. All gates run in the order the skill defines them.

**Hard rule:** If the SKILL.md view call does not appear in the tool call log for this
session before skill output is generated, the output is a facsimile. Start over with turn 1.

**Verification test:** After any skill output is delivered, check: does the session tool
call log contain a `view` on the SKILL.md path earlier in the same session? If no → facsimile.

---

## PROC-02 — ACCEPTED_LIMITATION Classification

**Trigger:** A finding is proposed with fix_type = ACCEPTED_LIMITATION.

**When to use:** A finding documents a real failure, but the fix is either:
- Impossible given the current architecture (R-074: no post-hoc fix for non-omission failures)
- Already mitigated by an existing structural mechanism
- A known platform constraint (P-07 class: external dependency, not agent behavior)

**When NOT to use:** Do not classify ACCEPTED_LIMITATION to avoid doing work. If a STRUCTURAL
fix exists, it must be implemented. ACCEPTED_LIMITATION is not a lower-effort alternative.

**Required fields for every ACCEPTED_LIMITATION finding:**

| Field | Required content |
|---|---|
| fix_type | ACCEPTED_LIMITATION |
| fix_applied | Must contain: (1) the rule or reference justifying acceptance (e.g. "R-074"), (2) what the existing mitigation is (e.g. "A1 in prefs is the mitigation"), (3) why a structural fix is unavailable |
| status | OPEN — ACCEPTED_LIMITATION does not mean RESOLVED. These findings stay OPEN as permanent audit trail entries unless the underlying constraint changes. |

**Example (F-025):**
```
fix_type: ACCEPTED_LIMITATION
fix_applied: "ACCEPTED_LIMITATION (R-074 basis). R-074 VERIFIED: post-hoc artifact
validation is insufficient for non-omission failures. A1 in user preferences is the
active mitigation. No structural fix is available within current architecture."
status: OPEN
```

**Where to document the mitigation:** In fix_applied (D1), not in a separate document.
The finding is the audit record. If a separate structural change is made as a partial
mitigation, create a second finding for that change with fix_type = STRUCTURAL.

---

## PROC-03 — New Pattern Creation

**Trigger:** A new recurring failure pattern is proposed for addition to failure_patterns.

**Required fields:**

| Field | Requirement |
|---|---|
| pattern_code | Next sequential P-XX. Check MAX(CAST(SUBSTR(pattern_code,3) AS INTEGER)) FROM failure_patterns first. |
| name | Short noun phrase (≤ 6 words). Must be distinct from all existing pattern names. |
| description | Must contain: (1) what the failure looks like, (2) the mechanism (not just the symptom), (3) what distinguishes it from the nearest existing pattern, (4) at least one external evidence reference if available (arXiv, practitioner source) |
| severity | CRITICAL / HIGH / MEDIUM. Default HIGH for new patterns without recurrence data. Upgrade to CRITICAL only if a known-bad-violation rate exists (e.g. P-15 → DriftBench KBV 99%). |
| recurrence_count | Set to actual confirmed instances found in conversation history. Minimum 2 before creating a pattern — single-instance observations belong in granular_findings under the nearest existing pattern. |

**Does new pattern creation trigger a CI sync?** Yes. Two D1 writes are required:
1. INSERT into failure_patterns (new pattern) — SYNC TRIGGER
2. INSERT into granular_findings for each confirmed instance — SYNC TRIGGER

Run Step 4 (CI sync per SKILL.md) once after both writes, not twice.

**Pattern investigation procedure before creation:**
1. Run conversation_search with domain keywords for the proposed failure type
2. Confirm at least 2 distinct instances from different sessions or conversations
3. Verify the mechanism is not already covered by an existing pattern (check all 15 descriptions in D1)
4. If evidence is insufficient: create a granular_finding under the nearest existing pattern with status=RESOLVED and fix_type=ACCEPTED_LIMITATION, noting the investigation result in fix_applied. Do not create a pattern.

---

## PROC-04 — Sync Gate Procedure

**Trigger:** After any of the following D1 write types.

| D1 write type | Triggers sync? |
|---|---|
| INSERT new finding into granular_findings | Yes |
| UPDATE finding to RESOLVED | Yes |
| UPDATE failure_patterns.recurrence_count | Yes |
| INSERT new pattern into failure_patterns | Yes |
| UPDATE fix_applied or fix_type only | No (no schema change to audit JSON) |
| SELECT only | No |

**Full sync gate sequence:**

Step 1 — Verify the D1 write committed. Re-fetch the row just written:
```sql
SELECT * FROM granular_findings WHERE finding_id = 'F-XXX';
-- or for patterns:
SELECT * FROM failure_patterns WHERE pattern_code = 'P-XX';
```
If the row is absent or values differ from what was written → D1 write failed. Do not proceed to sync.

Step 2 — Fetch current sync inputs from D1:
```sql
SELECT pattern_code, name, severity, recurrence_count FROM failure_patterns ORDER BY pattern_code;
-- → /tmp/patterns.json

SELECT finding_id, pattern_code, title, artifact_affected, project_scope
FROM granular_findings WHERE status = 'OPEN' ORDER BY pattern_code, finding_id;
-- → /tmp/open_findings.json

SELECT COUNT(*) as total FROM granular_findings;
-- → note as <COUNT>
```

Step 3 — Run sync-failure-rules.py:
```bash
cd /home/claude/cs-work
git checkout main && git pull origin main
python3 ci/sync-failure-rules.py \
  --patterns /tmp/patterns.json \
  --open-findings /tmp/open_findings.json \
  --total-findings <COUNT> \
  --last-synced $(date +%Y-%m-%d) \
  --commit --push
```

Step 4 — Handle push result per PROC-05 (force-push gap).

Step 5 — Open PR from `sync/failure-audit-YYYY-MM-DD` → main. Wait for CI. Merge.

**HARD FAIL:** Skipping the sync after a D1 write leaves the repo JSON stale. The CI
check_open_findings.py reads from the JSON — stale JSON = invisible findings = silent
enforcement bypass.

---

## PROC-05 — sync-failure-rules.py Force-Push Gap

**Problem:** sync-failure-rules.py uses `git push origin <branch>` without `--force`.
When a prior sync branch with the same date name was squash-merged into main, the remote
branch head diverges from what the script creates locally. The push fails:

```
ERROR: git push failed: ! [rejected] sync/failure-audit-YYYY-MM-DD -> sync/failure-audit-YYYY-MM-DD
       (non-fast-forward)
```

**Why this happens:** Squash-merge rewrites history — the remote branch tip no longer
matches the local tip after `git checkout main && git pull`. The script has no
`--force-push` flag to handle this case.

**Workaround (until script is patched):**

```bash
# After sync-failure-rules.py exits with push error:
cd /home/claude/cs-work
git push origin sync/failure-audit-YYYY-MM-DD --force
```

**When this triggers:** Any time PROC-04 runs on the same calendar date as a prior
sync that was squash-merged. This is common when multiple D1 writes occur in one day.

**Fix status:** Needs `--force-push` flag added to sync-failure-rules.py git_push().
Tracked in item 8e of open work queue. When patched, remove this workaround note and
update the script docstring.

**Detection:** sync-failure-rules.py will print `ERROR: git push failed:` with the
rejection message. The error is not silent — it exits with code 2.
