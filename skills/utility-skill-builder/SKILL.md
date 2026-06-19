---
name: utility-skill-builder
description: >
  Enforces quality standards for all skill creation and updates across any
  project. Use automatically — do not wait to be asked. Trigger on ANY of
  these signals: a new skill is being written; an existing skill is being
  updated, edited, or reformatted; a skill is being audited; the words
  "skill", "SKILL.md", or "package" appear in a skill-creation context;
  user says "create a skill", "update this skill", "audit this skill",
  "package this skill", "fix this skill", "change the trigger", "add an
  example to", "update the description on"; str_replace/create_file on a
  SKILL.md; direct edit to SKILL.md. Runs a research audit on new
  skills and substantial updates before design work begins. Classifies every
  proposed change before execution. Enforces quality gates BEFORE packaging
  — never after. Do NOT trigger for: non-skill documents (GDD, README,
  changelog, Notion pages), code generation, or content creation tasks
  unrelated to skill authoring (game ability design, lore writing, marketing
  copy). Load once per session.
---
gates_passed: 2026-05-24
SKILL_VERSION: v3.6

# Skill Publisher — Quality Gate

Applies to all projects. Governs creation, update, packaging, and removal of
every Claude skill across the workspace. Every skill must pass all gates before
packaging. No exceptions.

Type: dispatcher

Canonical reference implementation: `/mnt/skills/user/persona-developer/SKILL.md`.
Read it before designing any new dispatcher. Its 5-part body structure
(PART 0 classification → PART 1 reference loading → PART 2 pre-generation
→ PART 3 synthesis → PART 4 post-generation → PART 5 meta-adversarial) is
the canonical pattern this skill enforces.

---

## GOTCHAS

Failure modes Claude exhibits without this skill. This is why the skill exists.

1. **Rationalizing "minor fix" to skip Gate 0** — every update feels minor; use the binary table.
2. **Applying BEHAVIORAL ADDITIONs without user confirmation** — rules added "because they seem useful" measurably degrade task-specific performance; SkillReducer (arxiv 2603.29919) documents 38.5% body actionability loss from unconfirmed additions.
3. **Reference file missing silently** — CI (validate.py) now catches this as HARD FAIL, but only at push time. Gate 8 catches it before push.
4. **Running Gate 7 grep from a prior turn** — results go stale after any edit. Re-run after every edit batch.
5. **Skipping Gate 8b under task load** — it's the last gate before packaging and the most likely to be dropped. Block is required in conversation before `present_files`.
6. **Assuming reference files persist across turns** — they don't. Re-issue `view` at each step that needs a reference file. No view output = running from memory = HARD FAIL.
7. **Adding gates to feel thorough** — gates that don't change Claude's behavior add overhead without value. Challenge 5 catches these.
8. **Dispatcher without synthesis protocol** — intake classification and reference loading work, but output is concatenated per-domain sections (BALANCE FINDINGS: ... PSYCHOLOGY FINDINGS: ...) rather than one integrated answer. Fix: verify synthesis protocol step is present in body with explicit cross-domain conflict check before output.
9. **Delivering to Skills UI instead of filesystem** — Skills UI only stores SKILL.md; reference files are silently dropped. Filesystem at `/mnt/skills/user/<skill-name>/` is the primary delivery target.
10. **Type-taxonomy escape hatch** — declaring `encoded-preference` or `capability-uplift` to avoid dispatcher body constraints. All skills are `Type: dispatcher`. Domain expertise in the body (not in a reference file) causes routing competition and parsing errors.
11. **Domain expertise in body** — reference files cost zero tokens until loaded; skill bodies load in full on every trigger. Interleaving process and knowledge forces parsing-which-is-which before acting; that parsing introduces errors. Single-domain skills with no reference file always violate this.
12. **Steps marked complete without executing** — gates run but produce no visible output block, or packaging runs but `present_files` is not called in the same response. Both are the same failure mode: step logged as done without the required artifact appearing. Fix: every gate produces a visible named output block; every packaging sequence ends with `present_files` firing in the same turn (see arxiv 2604.20911 in SEE ALSO).
13. **Resource taxonomy under-considered** — corpus reality: zero skills use `scripts/`, `assets/`, or `evals/`. Some skills encode deterministic procedures as inline bash that belong in `scripts/`; some produce file artifacts that belong in `assets/`. Gate 2.5 forces explicit consideration of all four resource types.
14. **Generalization failure** — body contains project-specific names. CI (VR-11) warns on this; Gate 5e is the pre-push catch.
15. **Trigger fires on file path, not task description** — any tool call targeting `/mnt/skills/user/**/*.md` or `cs-work/skills/**/*.md` triggers this skill regardless of task framing. Labels like "scrub mentions", "remove references", or "clean up" are not exemptions. Match the tool-call path, not the task label.

---

## GATE 0 — RESEARCH AUDIT

Run before any design or editing work. One row match → SUBSTANTIAL; run research.

| Any of these true → SUBSTANTIAL (run utility-data-analyst) |
|---|
| New skill being created |
| New gate being added |
| Workflow steps changed or reordered |
| Trigger conditions (description) being changed |
| Examples section being changed |
| Output format being changed |
| Any existing section replaced rather than added to |
| Proposed addition has no documented failure mode in loaded materials |
| Skill last researched more than 4 weeks ago |

If none → MINOR. Skip Gate 0. Proceed to Gate 0.5.

**Research output block (required when research runs):**
```
RESEARCH AUDIT — [skill name]
Sources: [N] — [titles/URLs]
Gaps: 1. [Finding] — Source: [title] — Action: [what to change]
Confirmed complete: [topics checked, no gaps found]
```

---

## GATE 0.5 — CONTENT PLACEMENT & CHANGE CLASSIFICATION

Two steps. Both run before any editing begins.

### Step A — Content Routing

| Content type | Correct home |
|---|---|
| Standing behavioral rules across all sessions | User preferences |
| Project-specific constraints, stack rules, locked decisions | Memory or project files |
| Session orchestration (skill ordering, token efficiency) | Project instructions |
| Authoritative reference data for a specific project | Project files |
| Reusable workflow or domain expertise applied on-demand | Skill — correct home |
| Multiple overlapping/complementary sub-domains where multi-domain questions are expected; ≥3 sub-domain skills with shared trigger space | Dispatcher skill — body = routing/synthesis only; reference files = all domain expertise, one file per sub-domain |
| One-time task instructions | Inline prompt — not a skill |

Flag misrouted content. Act now if writable; flag to Next Steps if manual placement required. Produce PLACEMENT AUDIT block before proceeding.

### Step B — Change Classification

Classify every proposed change before executing:

**STRUCTURAL FIX:** Corrects a failure mode documented in this session's loaded materials.
→ Proceed. Name the failure mode in Gate 9 delivery block.

**BEHAVIORAL ADDITION:** Adds a gate, rule, or check with no failure evidence in loaded materials.
→ STOP. Present:
```
BEHAVIORAL ADDITION — [change description]
Evidence: [none found / what was found]
No documented failure mode. Proceed? [user decides]
```
Only continue after explicit user confirmation.

**DEGRADATION RISK:** Conflicts with an existing gate or workflow step.
→ STOP. Name the conflict. Present to user before proceeding.

HARD FAIL: Any BEHAVIORAL ADDITION executed without user confirmation blocks Gate 8b Challenge 6.

**Next Steps block** — append to Gate 9 when misrouted content was not actioned:
```
NEXT STEPS — action required before this skill is fully operational:
1. [Content] → Add to [correct location] manually
```

---

## GATE 1 — FULL READ BEFORE ANY EDIT

Read every line before any changes — never from memory or partial read; re-read if edited this session; truncated output must be expanded; `view_range` calls do NOT satisfy this gate. Required output (HARD FAIL if absent before any edit): `FULL READ: [filename] — [N lines]`

---

## GATE 2 — FRONTMATTER COMPLETENESS & VALIDITY

| Check | Pass condition |
|---|---|
| `name` | kebab-case, lowercase, numbers, hyphens only; ≤ 64 chars |
| `name` reserved words | Must NOT contain "anthropic" or "claude" |
| `name` no XML | No `<>` characters |
| `description` | Non-empty, no XML, ≤ 1,024 chars — run char count (Gate 7) |
| `description` voice | Third person: "Processes X" not first-person voice |
| `description` structure | States WHAT it does AND WHEN to trigger |
| Quoted keywords | Specific quoted trigger terms users will actually say |
| Trigger signals | "Trigger on ANY of these signals:" with named phrases |
| NOT-triggers | At least one explicit scope exclusion with named adjacent domain |
| Auto-trigger | "Use automatically — do not wait to be asked." |
| `Load once per session` | Required on all skills with bodies > 100 lines |
| `allowed-tools` | claude.ai chat skills: not applicable — remove if present. Claude Code skills: valid — leave if intentional. |
| Paraphrase test | 10+ variations verified trigger correctly; 3 near-miss negatives verified do NOT fire |

HARD FAIL: Any check fails → packaging blocked. Fix before Gate 2.5.

**YAML remediation:** Strip to `name` + `description` only → test → add optional fields one at a time.

---

## GATE 2.5 — RESOURCE PLACEMENT DECISION

Run before Gate 3. For every piece of content the skill needs, classify the resource type. Mandatory consideration of all four Anthropic-canonical resource types: do not default to references/ for every non-body item.

**Resource routing table:**

| Content type | Resource | Token model |
|---|---|---|
| Workflow logic, classification, routing, judgment, behavioral imperatives | `SKILL.md` body | Loaded every trigger |
| Domain knowledge, large examples, taxonomies, conditional content Claude reads sometimes | `references/*.md` | Zero until `view`'d |
| Deterministic procedure: validation, formatting, conversion, queries, char counts, regex sweeps, packaging | `scripts/*.py|*.sh` | Source NEVER enters context; only stdout/stderr |
| Output template Claude COPIES or FILLS: docx/pptx templates, HTML boilerplate, fonts, logos, sample documents | `assets/*` | Zero, ever — path only |
| Regression test, behavior eval | `evals/evals.json` + test files | Loaded only by eval runner |

**Decision questions — ask each before Gate 3 runs:**

1. Is any procedure in the proposed body deterministic (same logic every time, no judgment)? → script candidate.
2. Does the skill produce file output that would benefit from a template? → asset candidate.
3. Is any reference content > 100 lines or rarely-loaded? → reference file split candidate.
4. Could a deterministic procedure currently expressed as inline bash become a script? → script candidate.

**Output block (required):**
```
RESOURCE PLACEMENT — [skill name]
Body content: [one-line summary of body responsibility]
references/: [list of files + why each]
scripts/: [list + deterministic procedure replaced — or "none, no deterministic procedures"]
assets/: [list + output use — or "none, no file artifact output"]
evals/: [recommended for INSTALLED promotion / not yet required]
```

HARD FAIL: Output block absent → Gate 3 cannot proceed.

See `references/dispatcher-skeleton.md` for decision criteria and worked examples.

---

## GATE 3 — BODY COMPLETENESS

| Element | Requirement |
|---|---|
| H1 title | Matches skill purpose |
| Context line | One line: project, domain, or scope |
| Canonical reference | `persona-developer` named as canonical pattern (read before design) |
| Skill type | `Type: dispatcher` — all skills; no other types permitted |
| Reference files | ≥ 1 reference file required for all skills; single-domain = 1 file; multi-domain = 1 per domain |
| Gotchas section | ≥ 2 entries from real failure modes Claude exhibits without this skill |
| Behavioral rules | All imperatives: "Always X" / "Never Y" — no hedged language |
| Structured data | 3+ attribute data in tables, not prose |
| Numbered steps | Procedures use numbered lists, not bullets |
| Classification table | Each domain row includes a worked Example column |
| Reference reload imperative | Body states: "Reference files do not persist across turns — re-view each turn that uses them" |
| Examples section | ≥ 2 concrete examples; for complex skills, longer than the rules section |
| Out of Scope | Explicit list of what this skill does NOT do; name sibling skills |
| Output format | Labels, structure, field names, confirmation strings defined |
| SEE ALSO | Table of sibling skills at end of file |
| Sourced assertions | Numerical values or "confirmed" claims need citation or `[OPEN: source not verified]` |
| Enforcement | Checks use hard-fail conditions (table of fail states), not passive checklists |

**Skill type guidance:**
All skills are `Type: dispatcher`. Body contains routing logic and process steps only — zero domain expertise. Domain content lives in reference files, which cost zero tokens until loaded (Anthropic engineering blog 2025; SkillReducer 2603.29919; MindStudio 2026).

**Generalization principle (HARD FAIL when violated):**
The skill body is a portable routing/synthesis skeleton. Project-specific names, paths, schemas, constants, and IDs live in reference files — never in the body. Test: "Could this body be cloned to another project by replacing references only?" If no, the offending content moves to a reference. References themselves MAY be project-specific (e.g. `loop-specific.md`); the body never is.

**Required elements — all skills (HARD FAIL if absent):**

| Element | Single-domain | Multi-domain |
|---|---|---|
| Body contains ZERO domain expertise | Required | Required |
| ≥ 1 reference file | Required (exactly 1) | Required (1 per domain) |
| Explicit `view` path per reference file | Required | Required |
| Intake classification table | Optional | Required — ≥1 example per domain code |
| Domain declaration block (`DOMAINS ACTIVATED: [code list]`) | Optional | Required — visible, not internal |
| Cross-domain conflict map (`references/cross-domain-map.md`) | Not required | Required |
| Multi-domain synthesis protocol | Not required | Required — integration, not concatenation |
| Meta-adversarial review | Not required | Required — dispatcher-level challenges |

HARD FAIL: Any element absent → packaging blocked.

For full dispatcher skeleton, classification-table template, domain code naming convention, cross-domain-map.md template, frontmatter template, and worked dispatcher example: load `references/dispatcher-skeleton.md`.

---

## GATE 4 — BANNED ELEMENTS

| Banned element | Fix |
|---|---|
| Blockquotes (start of line: greater-than space) | Convert to code block or bold rule |
| Double separators (start of line: three hyphens) | Remove duplicate |
| Motivational framing | Strip entirely |
| Narrative/attribution intro | Strip or convert to imperative |
| Summary restatements | Strip entirely |
| Transition phrases | Strip entirely |
| Hedged behavioral rules | Convert to imperative |
| Passive voice behavioral rules | Convert to "Always..." |
| Time-sensitive information | Move to legacy section |
| Inconsistent terminology | One term per concept |
| Stale references | Update to current state |
| Hardcoded version numbers in doc references | Replace with "current version" |
| Prose SEE ALSO | Convert to table |
| Nested references (SKILL.md to A.md to B.md) | Keep all references one level from SKILL.md |
| Content Claude already knows | Remove — only add what Claude lacks |

---

## GATE 5 — REQUIRED PATTERNS

**Frontmatter voice:** Must include "Use automatically — do not wait to be asked.", "Trigger on ANY of these signals:" with named phrases, third-person phrasing throughout.

**Rule voice:** MUST, ALWAYS, NEVER, or imperative. "Should" only for external system behavior — never for Claude's actions.

**SEE ALSO format:** Table with columns `Skill / Resource` and `Domain` — no prose SEE ALSO.

**Output format:** Labels, structure, field names, and confirmation strings defined explicitly.

**Dispatcher body content sub-checks (all skills, all HARD FAIL):**

| # | Sub-check | Pass condition |
|---|---|---|
| 5a | Classification step present | Body has explicit step that classifies the request before any reference load |
| 5b | Reference files `view`'d explicitly | Each reference load is named with path; not implied |
| 5c | Synthesis/routing protocol present | Body states how multiple loaded references combine into one output |
| 5d | Zero non-routing behavioral rules | Body contains no methodology, framework, or domain rule — only routing |
| 5e | Generalization passes | Body has no project-specific names, paths, schemas, or IDs |

Test for each: "Could this body section appear in a reference file?" If yes, it must be there instead.

**Domain declaration display format (HARD FAIL when multi-domain dispatcher):**
```
DOMAINS ACTIVATED: [code1] [+ code2] [+ code3]
Reference files to load: [list exact paths]
Multi-domain: [yes — load cross-domain-map.md / no]
```
This block must be visible to the user before any reference content is loaded.

HARD FAIL: Any required pattern absent → packaging blocked.

---

## GATE 6 — ARCHITECTURE & SIZE

| Check | Pass condition |
|---|---|
| SKILL.md body | ≤ 400 lines internal target; ≤ 500 hard limit |
| Reference depth | All references one level from SKILL.md only |
| No nested references | Reference files must not reference other reference files |
| Oversize content | Detailed docs, large examples, challenge specs → separate reference files |
| Reference file TOC | Required for any reference file > 100 lines |

**Body vs reference splitting threshold:** Any methodology, framework, named rule set, table > 5 rows, or content block > 20 lines → reference file. Body retains only: classification, routing table, view paths, synthesis protocol, post-gen audit, hard fails.

**Reference file minimum structure:**
- H1 matches filename
- Imperative rule voice (same as body)
- Optional TOC when > 100 lines (Gate 6 hard rule)
- No nested references to other reference files

**Cross-skill deduplication:** Content already in a sibling skill → remove and add sibling to SEE ALSO. Intentional duplication → add inline comment explaining why.

HARD FAIL: Body exceeds 500 lines → move content to reference files before Gate 7.

---

## GATE 7 — VALIDATION

Run after all edits are complete. Re-run after every edit batch before packaging.

```bash
python3 /mnt/skills/user/utility-skill-builder/scripts/validate.py /tmp/<skill-name>/SKILL.md
```

The validator runs all deterministic Gate 7 checks: 6 grep sweeps (blockquotes, hedged language, bad version refs, second-person voice, dated content; double-separator is informational), 5 structural presence checks (Type dispatcher, GOTCHAS, SKILL_VERSION, Use automatically, reference reload imperative), description char count (limit 1,024), name length (limit 64), and line count (target 400, hard limit 500).

Exit code 0 means all checks pass. Exit code 1 means at least one FAIL. Fix before packaging.

Gate 7 output must be produced in this response turn — not referenced from a prior turn.

For validator source, see `scripts/validate.py`. Resource placement rule R1 (deterministic procedures live in scripts/, not skill bodies) is self-applied here — earlier versions of skill-publisher inlined this logic as a 30-line bash + python block in the body.

---

## GATE 8 — PACKAGING PROTOCOL

Execute only after all gates above have passed.

**Reference file existence check (before packaging command):**
```bash
ls /tmp/<skill-name>/references/
# HARD FAIL if any expected reference file is absent — do not package.
# HARD FAIL if references/ directory is empty or missing — all skills require >= 1 reference file.
```

**Optional resource existence check (when declared in Gate 2.5):**
```bash
ls /tmp/<skill-name>/scripts/ 2>/dev/null   # only if scripts/ declared
ls /tmp/<skill-name>/assets/ 2>/dev/null    # only if assets/ declared
# HARD FAIL if Gate 2.5 declared scripts/ or assets/ and the directory is absent.
```

**Step 1 — Session install (always execute first):**
Makes the skill available in the current session. Session-local only — resets on next session start.
```bash
mkdir -p /mnt/skills/user/<skill-name>/
cp /tmp/<skill-name>/SKILL.md /mnt/skills/user/<skill-name>/SKILL.md
cp -r /tmp/<skill-name>/references/ /mnt/skills/user/<skill-name>/references/ 2>/dev/null || true
cp -r /tmp/<skill-name>/scripts/ /mnt/skills/user/<skill-name>/scripts/ 2>/dev/null || true
cp -r /tmp/<skill-name>/assets/ /mnt/skills/user/<skill-name>/assets/ 2>/dev/null || true
ls /mnt/skills/user/<skill-name>/
```
HARD FAIL: output must be visible before Step 2 runs.

**Step 2 — Package, copy, and present (one atomic action):**
```bash
cd /mnt/skills/examples/skill-creator
python3 -m scripts.package_skill /tmp/<skill-name>/ /tmp/pkg-output/
cp /tmp/pkg-output/<skill-name>.skill /mnt/user-data/outputs/
```
MUST call `present_files` with the .skill path immediately after cp — Step 2 is not complete until the `present_files` tool call appears in this response turn.
HARD FAIL: packaging output does not contain `Skill is valid!`.
HARD FAIL: `present_files` not called before Gate 8b begins.

**Self-application rule:** When this skill's SKILL.md is edited, always run both steps and present the .skill file without being asked.

---

## GATE 8b — ADVERSARIAL SELF-REVIEW

Load `references/gate-8b-challenges.md` before running any challenge. Confirm load by quoting the file's H1 verbatim: `# Gate 8b — Adversarial Self-Review Challenges` must appear in the response — cannot be produced from memory without loading the file. `present_files` and Gate 9 MUST NOT execute until the confirmation block is visible.

**Confirmation block (must appear before present_files):**
```
Gate 8b self-review:
  Challenge 1 — Trigger precision: [CLEAR / FAIL: reason]
  Challenge 2 — Scope bleed: [CLEAR / FAIL: reason]
  Challenge 3 — Hard fail completeness: [CLEAR / FAIL: reason]
  Challenge 4 — Mechanism survival: [CLEAR / FAIL: reason]
  Challenge 5 — Overhead check: [RAN: result / SKIPPED: no gate changes this session]
  Challenge 6 — Change impact: [all STRUCTURAL FIX / BEHAVIORAL ADDITIONs confirmed: list]
  Status: CLEAR to deliver / BLOCKED — [reason]
```

---

## GATE 8c — DELIVERY PRE-SEND CHECK

Load `references/gate-8c-delivery.md` before running any check. Confirm load with visible bash output.

All checks are HARD FAIL conditions. Delivery stops until all pass.

---

## GATE 9 — DELIVERY CONFIRMATION

After Gate 8b and 8c pass, confirm delivery and write the registry.

**Registry write (HARD FAIL if any step fails — runs on create, update, and remove):**
```
REGISTRY_WRITE — [skill name] — [version] — [INSTALLED / STAGED]
D1: claude-config (afd78e0e-583e-4e78-87fc-dd6bc8150ce9) — table: skills
New skill ceiling: SELECT value FROM secrets WHERE key IN ('max_skills','max_total_lines') then SELECT COUNT(*) cnt, COALESCE(SUM(lines),0) ttl FROM skills WHERE status='INSTALLED'
  HARD FAIL if cnt >= max_skills OR ttl + this_skill_lines > max_total_lines — report [N/50 — L/17500]
Install/Update: INSERT OR REPLACE INTO skills (name,version,status,lines,updated_at) VALUES (...)
Remove: DELETE FROM skills WHERE name = '<skill-name>'
Verify: re-query — entry present (install/update) or absent (remove) — HARD FAIL if wrong
```
**gates_passed write (HARD FAIL if skipped — runs on every create and update):**
Write today's date to SKILL.md frontmatter before packaging. See `references/gate-8c-delivery.md` Check 0 for the exact command.

| Skill state | Status |
|---|---|
| New skill (never INSTALLED) | STAGED — promote after one confirming session |
| Existing INSTALLED — additive update | INSTALLED — promote immediately. Additive: sections/examples added, no workflow steps removed. |
| Existing INSTALLED — structural rewrite | STAGED — promote after one confirming session. Structural: workflow changed, major sections replaced, trigger conditions changed. |

**Clean pass:**
```
[skill-name]  vX.X  [INSTALLED / STAGED]  (N lines)
Changes  N: [verb: what changed]
FixType  [STRUCTURAL FIX: failure mode / BEHAVIORAL ADDITION: confirmed by user on [date]]
Gates    all passed
[Next    adversarial review required to promote to INSTALLED]  STAGED only
[Redirect  [content] to [destination]]  Gate 0.5 misroutes only
```

**Gate failure:**
```
[skill-name]  vX.X  FAIL
GATE [N]  [gate name] — [reason <= 5 words]
Action  [what to fix and where]
```

**Rules:** `Changes` — count first, verb-first one-liner per fix. `FixType` — required whenever changes were made. Registry write failure: retry once; if still failing, mark registry not completed, record intended update in fenced block for next session.

---

## Examples

Seven worked examples (new single-domain dispatcher, gate added to INSTALLED skill, description trim, BEHAVIORAL ADDITION blocked, new multi-domain dispatcher, body content violation, resource routed to scripts/) are in `references/examples.md`. Load when designing or auditing a skill against the gate sequence.

---

## Out of Scope

This skill does NOT:
- Generate skills from scratch (use skill-creator for initial scaffolding)
- Enforce code quality or design system tokens (use persona-developer)
- Check lore canon (use loop-extended-lore-checker)
- Run evals or A/B comparisons (use skill-creator eval toolchain)
- Enforce project-specific skill requirements — those live in project instructions

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| persona-developer | Canonical dispatcher reference implementation — read before designing any new dispatcher |
| skill-creator | Base scaffolding — this skill adds the mandatory quality gate layer |
| references/dispatcher-skeleton.md | Dispatcher body skeleton, frontmatter template, classification table template, cross-domain-map template, scripts/assets decision criteria, worked example |
| references/gate-8b-challenges.md | Adversarial review challenge definitions (all 6 challenges) |
| references/gate-8c-delivery.md | Delivery pre-send check definitions |
| references/examples.md | Worked gate-sequence examples for 7 common scenarios |
| Anthropic skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| Anthropic Agent Skills engineering blog | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills |
| Agent Skills open standard | https://agentskills.io |
| SkillRouter — Skill Routing for LLM Agents at Scale | arxiv 2603.22455 — routing accuracy for overlapping skills |
| SkillReducer — Optimizing LLM Agent Skills for Token Efficiency | arxiv 2603.29919 — taxonomy-driven classification; 38.5% body actionability finding |
| SELECT-THEN-ROUTE — Taxonomy Guided Routing for LLMs | EMNLP 2025 — two-stage classify-then-route pattern |
| dotnet/skills Issue #35 — "Use fewer, larger skills" | GitHub — practitioner validation of dispatcher pattern |
| Trace2Skill — Distill Trajectory-Local Lessons into Transferable Agent Skills | arxiv 2603.25158 — skill fragmentation anti-pattern |
| MindStudio — Claude Code Skills Architecture | https://www.mindstudio.ai/blog/claude-code-skills-architecture-skill-md-reference-files |
| MindStudio — Code Scripts vs Markdown Instructions | https://www.mindstudio.ai/blog/claude-code-skills-code-scripts-vs-markdown-instructions — when to use scripts |
| Omission vs Commission Constraints — arxiv 2604.20911 | Basis for Gate 8 Step 2 collapse — commission holds 100% vs omission 33-73% under context load |
| Dotzlaw — Reusable Knowledge Packages | https://www.dotzlaw.com/insights/claude-skills/ — 3-tier progressive disclosure |
