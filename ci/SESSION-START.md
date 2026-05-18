# Failure Audit System — Session Start & Architecture

**Location:** ci/SESSION-START.md  
**Last updated:** 2026-05-18 (session 3)

This document is the authoritative reference for bootstrapping a failure audit session
and understanding the enforcement architecture. It is the fallback when the handoff
document chain is broken.

---

## SESSION START PROCEDURE

Run in order. Do not skip steps.

**Step 1 — Fetch PAT and clone repo:**
```sql
-- Via Cloudflare MCP (D1: afd78e0e-583e-4e78-87fc-dd6bc8150ce9)
SELECT value FROM secrets WHERE key = 'GITHUB_PAT';
```
```bash
git clone https://<PAT>@github.com/Farm-Grind/claude-skills.git /home/claude/cs-work
```

**Step 2 — Check for open sync PRs:**
Check GitHub for any open PRs with head branch matching `sync/failure-audit-*`.
If found: wait for CI, merge before proceeding. The repo JSON must be on main
before running the open findings gate.

**Step 3 — Emit open findings SQL:**
```bash
cd /home/claude/cs-work
python3 ci/check_open_findings.py --emit-sql
```
Execute the emitted SQL via Cloudflare MCP against D1: afd78e0e-583e-4e78-87fc-dd6bc8150ce9.

**Step 4 — Run gate with D1 results:**
```bash
python3 ci/check_open_findings.py --json '<results from Step 3>'
```

**Step 5 — Handle exit code:**

| Exit | Meaning | Action |
|---|---|---|
| 0 PASS | No blocking open findings | Proceed |
| 2 WARN | Open findings present, override(s) applied | Check override justifications; proceed if all blocking findings have valid overrides in D1 fix_applied |
| 1 FAIL | Blocking findings without override | Must resolve or override each blocking finding before starting new audit work |

**Override procedure (for findings with valid justification already in D1):**
```bash
python3 ci/check_open_findings.py --json '<results>' \
  --override "F-XXX: <paste justification from D1 fix_applied>"
```
Apply one `--override` flag per finding. Override is audit-trail logging, not suppression —
the finding remains OPEN. See ci/OPERATING-PROCEDURES.md PROC-02 for ACCEPTED_LIMITATION rules.

---

## ENFORCEMENT ARCHITECTURE — 5 LAYERS

The system enforces correct failure handling through five independent layers.
Each layer catches failures that the layer above misses.

### Layer 1 — Activation Gate
**Script:** ci/check_open_findings.py  
**When:** Session start, before any new audit work  
**What it does:** Queries the open findings list and blocks new work if blocking findings
are unresolved. Prevents audit debt accumulation.

### Layer 2 — Execution Gates
**Scripts:** ci/check_fix_type.py, ci/validate_research.py, ci/validate_constraints.py, ci/check_scope_inflation.py  
**When:** During fix proposal, research validation, and task execution  
**What they do:**
- check_fix_type.py: rejects BEHAVIORAL fixes for recurring patterns (recurrence > 1)
- validate_research.py: enforces research requirements before skill packaging
- validate_constraints.py: verifies corpus ceiling and constraint compliance
- check_scope_inflation.py: STRUCTURAL fix for P-15 (Complexity Inflation). Declares task scope
  as a manifest before work starts; validates git diff against manifest at commit time.
  Out-of-scope file changes → FAIL → commit blocked via pre-commit hook.
  Usage: `--init --task "..." --files "a,b"` before work; `--check --staged` to validate.
  Manifest lives at ci/scope-active.json (gitignored).

### Layer 3 — Delivery Gates
**Scripts:** ci/validate_handoff.py, ci/validate.py  
**When:** Before handoff prompts are produced; before skills are committed  
**What they do:**
- validate_handoff.py: enforces handoff block structure (required fields, no nested fenced blocks)
- validate.py: validates skill files against corpus rules (references dir WARN, line ceiling, etc.)

### Layer 4 — Persistence
**Script:** ci/sync-failure-rules.py  
**Data:** D1 granular_findings + failure_patterns; ci/failure-audit-rules.json (repo snapshot)  
**When:** After every D1 write that changes open findings or pattern recurrence  
**What it does:** Syncs D1 state to repo JSON so CI scripts have offline access to pattern metadata.
See ci/OPERATING-PROCEDURES.md PROC-04 for sync gate procedure and PROC-05 for force-push gap.

### Layer 5 — Repo Integrity
**Scripts:** .githooks/pre-commit, ci/check_ceiling.py, ci/check_scope_inflation.py  
**When:** Every commit (pre-commit hook)  
**Config:** `git config core.hooksPath .githooks` (set at clone time or once per session)  
**What it does:** Runs scope inflation gate (SCI-00–03) if ci/scope-active.json exists;
runs corpus ceiling check on every commit. Commit blocked on scope violation or ceiling breach.

---

## KEY REFERENCES

| What you need | Where to find it |
|---|---|
| SQL templates for all D1 writes | skills/utility-issue-triage/references/d1-queries.md |
| Operational procedures (PROC-01–05) | ci/OPERATING-PROCEDURES.md |
| Triage process (PART 0 through PART 5) | skills/utility-issue-triage/SKILL.md |
| Failure taxonomy (all categories) | skills/utility-issue-triage/references/failure-taxonomy.md |
| Pattern definitions (live) | D1: SELECT * FROM failure_patterns ORDER BY pattern_code |
| Open findings (live) | D1: SELECT * FROM granular_findings WHERE status='OPEN' |
| Offline pattern snapshot | ci/failure-audit-rules.json |

---

## DATABASES

| Resource | Value |
|---|---|
| D1 database ID | afd78e0e-583e-4e78-87fc-dd6bc8150ce9 |
| D1 database name | claude-config |
| GitHub repo | Farm-Grind/claude-skills |
| PAT location | D1: SELECT value FROM secrets WHERE key = 'GITHUB_PAT' |
