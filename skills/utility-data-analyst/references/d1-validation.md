# Research Database Validation Protocol

Used by PART 13 of utility-data-analyst. Runs before any INSERT into
`research_findings` in D1 database `claude-config`
(UUID: `afd78e0e-583e-4e78-87fc-dd6bc8150ce9`).

The validation has three sequential steps. All three must pass before
the INSERT SQL is presented for execution. Any HARD FAIL blocks the
INSERT. Any WARN requires explicit human confirmation before INSERT.

---

## Step 1 — Mechanical Gate (validate_research.py)

Run the CI script via bash_tool. Script must exit 0 (PASS) or 2 (WARN,
with human confirmation) before Step 2 proceeds. Exit 1 = HARD FAIL,
block INSERT, fix the finding, re-run.

```bash
python3 /home/claude/cs-work/ci/validate_research.py --json '<finding_json>'
```

If the repo is not cloned, clone first:
```bash
. /mnt/skills/user/.github-credentials
git clone https://github.com/Farm-Grind/claude-skills.git /home/claude/cs-work
```

Required output block before Step 2:
```
RQG RESULT — [research_id]
Exit code: [0=PASS / 1=FAIL / 2=WARN]
[paste script output]
```

---

## Step 2 — Failure Pattern Cross-Check

Two checks: (a) structured lookup of research previously misapplied to each
pattern, (b) keyword check on the proposed finding's application_guidance.

**2a — Structured: which patterns have prior misapplication history?**

```sql
SELECT fp.pattern_code, fp.name, fp.validation_requirement,
       rf.research_id, rf.finding
FROM failure_patterns fp
JOIN research_findings rf ON rf.misapplied_pattern_code = fp.pattern_code
ORDER BY fp.pattern_code
```

Review the result. If the proposed finding is in the same category and makes
a similar guidance recommendation to any returned finding, it carries the
same misapplication risk. Set `misapplied_pattern_code` to match.

**2b — Keyword check on application_guidance:**

Does the proposed guidance tell Claude to: add gates, add rules, add checks,
self-audit, produce more diagnostic output, or research before implementing?
If yes, check against P-01 (self-referential loop) and P-02 (additive-only)
before inserting. Populate `misapplied_pattern_code` if a match exists.

**Useful reverse lookup (given a pattern, find all misapplied research):**

```sql
SELECT research_id, category, finding, misapplication_warning
FROM research_findings
WHERE misapplied_pattern_code = 'P-02'
ORDER BY research_id
```

Required output block:
```
FAILURE PATTERN CHECK — [research_id]
Patterns checked: [list of P-codes whose name keywords appear in finding]
Matches: [none / P-XX — reason]
misapplication_warning: [unchanged / updated to: "..."]
```

---

## Step 3 — Deduplication Check

Query for substantively similar existing findings before inserting.

```sql
SELECT research_id, category, finding
FROM research_findings
WHERE category = ?
ORDER BY research_id
```
(param: proposed category)

Review the returned list. If a finding already covers the same mechanism
with the same application guidance: do not insert a duplicate. Update
the existing row instead, or discard if the proposed finding adds nothing.

Required output block:
```
DEDUP CHECK — [research_id]
Category: [category]
Existing in category: [N findings]
Near-duplicates: [none / R-XXX — reason it differs enough to warrant
                  separate entry]
Decision: [INSERT new / UPDATE R-XXX / DISCARD — reason]
```

---

## Step 4 — INSERT (only after all three steps pass)

```sql
INSERT INTO research_findings
  (research_id, category, finding, confidence, primary_source,
   source_type, application_guidance, misapplication_warning,
   misapplied_pattern_code, conversation_url)
VALUES
  ('R-NNN', 'category', 'finding text', 'VERIFIED',
   'source', 'source_type', 'guidance', 'None.',
   NULL,
   'https://claude.ai/chat/...')
```

Set `misapplied_pattern_code` to the pattern code (e.g., `'P-02'`) if Step 2
identified a misapplication risk, or `NULL` if none.

Verify after INSERT:
```sql
SELECT research_id, category, confidence FROM research_findings
WHERE research_id = 'R-NNN'
```

---

## Required Visible Block (complete, before any INSERT executes)

```
RESEARCH DB GATE — [research_id]
Step 1 RQG script:    [PASS / WARN (confirmed) / FAIL — blocked]
Step 2 pattern check: [no matches / P-XX flagged — misapplication_warning updated]
Step 3 dedup:         [N in category, no near-duplicates / duplicate found — decision]
Decision:             [INSERT / UPDATE R-XXX / DISCARD]
```

HARD FAIL: INSERT must not execute if this block is absent or any step
shows FAIL.
