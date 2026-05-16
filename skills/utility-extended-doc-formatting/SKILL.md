---
name: utility-extended-doc-formatting
description: >
  Governs format, structure, and completeness for all project documents and
  skills. Three reader modes: CLAUDE-ONLY (skills, instructions, reference
  data), HUMAN-ONLY (marketing, store copy, press), DUAL (GDD, lore bible,
  design system, tech spec). Use automatically — do not wait to be asked.
  Trigger on ANY of these signals: any document or skill is being created;
  a docx is being generated; a skill file is being written; marketing or
  store copy is being drafted; user asks to "reformat", "clean up", "fix
  formatting", "review for completeness", or "audit this"; a skill is being
  reviewed; user says a document reads wrong for its audience; any output
  is being saved as a project file; user asks "is this complete?".
  On initial creation: run STEP 0 BEFORE writing. On audit/reformat: run
  STEP 3 then STEP 4 in order.
  Do NOT use for: lore consistency, code style, or file naming (those have
  dedicated project skills). Load once per session.
---
SKILL_VERSION: v2.1

# Document Formatting Skill

Governs format, structure, and completeness for all project documents and
skills across three reader modes: CLAUDE-ONLY, HUMAN-ONLY, and DUAL.

Where The Loop is referenced, it serves as the primary worked example.

**Reference files** (load only when needed):
- `references/modes.md` — Full MODE A and MODE B rules + checklists. Load
  when STEP 1 identifies CLAUDE-ONLY or HUMAN-ONLY.
- `references/examples.md` — Worked examples for all three modes. Load
  when a concrete example would clarify correct behavior.

---

## STEP 0 — PRE-GENERATION CHECKLIST (initial creation only)

Run before writing any new document or skill. Do not skip on creation.
On reformat/audit requests, go directly to STEP 3.

1. **Identify the mode** — apply STEP 1 before writing a single line.
2. **Identify the document type** — confirm it is in the mode table.
   If not, apply DUAL as default.
3. **Pull the required elements list** for the identified mode from STEP 2.
   Write these elements into the document structure before filling content.
4. **Confirm all required elements are planned:**

| Mode | Required elements confirmed before writing? |
|---|---|
| CLAUDE-ONLY | Frontmatter, trigger conditions, NOT-triggers, status markers, SEE ALSO |
| HUMAN-ONLY | Opening line, concrete specifics, brand voice, closing sentence, CTA |
| DUAL | Numbered headings, prose layer, callout block plan, OPEN/LOCKED flags, section order |

5. **Plan callout block placement** (DUAL only) — identify every known
   OPEN item and LOCKED decision that belongs in this document. List them
   before writing. Place each at the point of first relevance, not batched
   at the end.
6. **Write.** Apply mode rules throughout. Format as you go, not after.
7. **On completion, run STEP 3 (completeness audit) before presenting.**
   Self-audit every new document before delivery.

---

## STEP 1 — IDENTIFY THE READER MODE

Before formatting anything, determine the mode. Apply the mode's rules.

| Human reads it | Claude reads it | Mode |
|---|---|---|
| No | Yes | CLAUDE-ONLY |
| Yes | No | HUMAN-ONLY |
| Yes | Yes | DUAL |

**Default: DUAL when uncertain.** Over-serving both audiences is always
safe. Under-serving either is never safe.

### Mode by document type

| Document | Mode |
|---|---|
| Skill files (.md in /skills/) | CLAUDE-ONLY |
| System prompts / Claude instructions | CLAUDE-ONLY |
| Reference data (JSON, seed files, storage schemas) | CLAUDE-ONLY |
| Decisions log, build tracker state | CLAUDE-ONLY |
| Marketing copy, store listing, press kit | HUMAN-ONLY |
| Social media content, app store description | HUMAN-ONLY |
| Pitch decks, one-pagers for external audiences | HUMAN-ONLY |
| GDD, lore bible, tech spec, design system | DUAL |
| Documentation standards, internal design memos | DUAL |

### Section-level overrides within DUAL documents

A section inside a DUAL document may be effectively CLAUDE-ONLY if it
contains pure mechanical spec, data tables, or checklists with no narrative
value to human readers. Apply CLAUDE-ONLY formatting to that section.
Mark it with a comment: `<!-- Claude reference section -->`.
Do not change the document's overall mode classification.

**If mode is CLAUDE-ONLY or HUMAN-ONLY:** read `references/modes.md`
before proceeding to STEP 2.

---

## STEP 2 — APPLY MODE RULES

**CLAUDE-ONLY or HUMAN-ONLY:** rules are in `references/modes.md`.
Read it now.

---

### MODE C — DUAL (Claude + Human)

**Optimize for:** serving both readers without compromising either.

**Mechanism: layered formatting.** Human prose layer reads coherently
without Claude callout blocks. Claude callout blocks are embedded at
decision points as scannable anchors.

#### Test for valid DUAL formatting

Read the document skipping all callout blocks. If the prose layer reads
as a coherent standalone document — pass. If it requires callout blocks
to make sense — fail; the human layer is incomplete.

#### Required elements

| Element | Requirement |
|---|---|
| Numbered headings | All sections use `# N.` / `## N.N` / `### N.N.N` (3 levels max) |
| Human prose layer | Complete, coherent, navigable without callout blocks |
| Callout blocks | Consistent format (see below); never ad-hoc |
| OPEN items | Flagged at decision point AND consolidated at end of document |
| LOCKED decisions | Flagged at decision point with `✓ LOCKED` callout |
| Section order | Human reading order, not Claude's optimal retrieval order |
| Version increment | Reformatting without content change = minor increment (v1.0 → v1.1) |

#### Callout block formats — use exactly these, no variations

**Locked decision:**
```
| ✓ LOCKED — [topic] | [Decision in one sentence.] |
| --- | --- |
```

**Open item:**
```
| ⚠ OPEN — [topic] | [What is unresolved. What decision is needed.] |
| --- | --- |
```

**Instructions for Claude:**
```
| Instructions for Claude | [Imperative instruction.] |
| --- | --- |
```

**Design gap (TODO):**
```
📌 TODO: [What must be defined before this section is complete.]
```

**Do-not-invent warning:**
```
⚠ DO NOT INVENT: [topic] — [What to do instead.]
```

#### AI-readiness metadata block (DUAL documents in Notion)

Every DUAL document stored in Notion must open with an AI-readiness
metadata block as a callout. This block is Claude's orientation header —
it tells Claude what the document is, its current state, and what it
governs, without requiring Claude to read the full document first.

**Required block format:**

```
| 📘 AI-READINESS | |
| --- | --- |
| Document | [short name — e.g. "gdd-mechanics v1.0"] |
| Status | [DRAFT / IN PROGRESS / PRODUCTION-READY / SUPERSEDED] |
| Last reviewed | [YYYY-MM-DD] |
| Review trigger | [Condition that should prompt re-review] |
| Governs | [What this document controls — e.g. "All minigame specs"] |
| Key open items | [1–3 line summary of highest-priority unresolved items, or "None"] |
```

**Rules:**
- Block appears at the very top of the document, before any content sections
- `Status` reflects implementability: DRAFT = not buildable from,
  PRODUCTION-READY = L2 or better
- `Last reviewed` updates whenever a decision that affects this document
  is made
- `Review trigger` is milestone-based (Linear issue closes, phase starts)
  — not calendar-based
- `Key open items` is a scan aid — not a substitute for inline ⚠ OPEN flags
- Block is CLAUDE-ONLY metadata — human readers skip it; it does not
  substitute for the human prose layer

**What it is not:** not a version header, not a changelog, not a summary.
It is an orientation block for Claude at session load time.

#### Required document structure order

1. Summary / overview (human-facing, brief, no callout blocks)
2. Core content sections (both audiences, callouts embedded at decision
   points)
3. Open items consolidated list (end of document or end of major section)
4. Claude quick-reference block (optional, for documents over 20 sections)

#### Tables in DUAL documents

Use for: attribute/value data, decision records, phase/mechanic mappings,
anything with 3+ parallel properties.

Do not use for: flowing prose, narrative descriptions, content where cell
relationships are not parallel.

#### Strip these from DUAL documents

| Remove | Why |
|---|---|
| Orphaned callout blocks | Callouts without human-readable context surrounding them leave humans without rationale |
| Filler intros and summary restatements | Token weight for Claude, reading time for humans |
| Inconsistent callout formats | Mix of `⚠`, `**NOTE:**`, `> blockquotes` breaks Claude's ability to scan by pattern |
| Mixed numbered/unnumbered headings | Breaks Claude's section-anchor parsing |

---

## STEP 3 — COMPLETENESS AUDIT

**HARD FAIL:** MUST NOT present any new document without running this checklist first. Run on every new document before delivery (triggered from STEP 0).
Run on any existing document when a review or audit is requested.
Run before STEP 4 on any reformat task — fix gaps before fixing format.

**CLAUDE-ONLY or HUMAN-ONLY checklists:** in `references/modes.md`. Read
it now if mode is not DUAL.

### DUAL completeness checklist

| Check | Pass condition |
|---|---|
| AI-readiness metadata block present | Notion DUAL docs: block at top of page in correct format |
| Numbered headings throughout | All sections use `# N.` / `## N.N` / `### N.N.N` |
| Human prose layer coherent | Reads as standalone document without callout blocks |
| All known OPEN items flagged | At point of first relevance using `⚠ OPEN` callout |
| All LOCKED decisions flagged | At point of first relevance using `✓ LOCKED` callout |
| OPEN items consolidated | End-of-document or end-of-section list, in addition to inline flags |
| Callout block formats consistent | Only the five standard formats — no variations |
| No orphaned callout blocks | Every callout has human-readable prose context around it |
| Section order is human-readable | Summary → core content → open items → quick reference |
| No required element missing | All items from MODE C required elements table are present |
| No disallowed elements present | Nothing from the MODE C strip table remains |

### On audit failure

| Context | Action |
|---|---|
| Initial creation | Fix all failures before presenting output. Never present a document that fails its own completeness audit. |
| Explicit audit request | Report every failure with location and specific fix. Execute all fixes. Re-run checklist to confirm resolution. |
| Reformat task | Log all failures, then proceed to STEP 4. |

---

## STEP 4 — REFORMAT WORKFLOW

Use when reformatting an existing document. Always run STEP 3 first.

1. **Identify current mode** — apply STEP 1. Note any mismatch between
   apparent audience and actual formatting.
2. **Log all completeness failures** from STEP 3 audit.
3. **Identify callout block inconsistencies** (DUAL only) — list all
   existing status markers, map each to the five standard formats.
4. **Execute in this order:**
   a. Fix all callout block formats to standard
   b. Add all missing required elements
   c. Strip all disallowed elements
   d. Convert prose structures to tables where required
   e. Verify: layer test (DUAL) or 2-second description test (CLAUDE-ONLY)
   f. Re-run STEP 3 checklist — confirm all items pass
5. **Increment version** — reformatting without content change = minor
   increment (v1.0 → v1.1). Reformatting that also adds substantive
   content = major increment (v1.0 → v2.0). Ask if uncertain.
6. **Flag the change** — note in document register: document name,
   previous version, new version, reason for increment.

---

## Out of Scope

| Situation | Use instead |
|---|---|
| Lore accuracy in NPC dialogue or world-building | loop-extended-lore-checker (Loop) or project's lore-checking skill |
| Code style, token names, component structure | loop-extended-code-guardian (Loop) or project's code skill |
| File naming, version numbers, folder structure | loop-core-tracker (Loop) or project's tracker skill |
| Balance or economy system documentation content | utility-game-balance or utility-game-idle-math |

---

## QUICK REFERENCE

| Output type | Mode | Non-negotiable rule |
|---|---|---|
| Skill file | CLAUDE-ONLY | Frontmatter description scannable in 2 seconds |
| Claude instruction / system prompt | CLAUDE-ONLY | Every rule stated as imperative |
| Store listing / app description | HUMAN-ONLY | Lead with emotional core, not genre |
| Press kit / marketing one-pager | HUMAN-ONLY | Headlines carry full meaning independently |
| Notion DUAL document (GDD, lore, tech spec) | DUAL | AI-readiness metadata block at top; review trigger is milestone-based |
| GDD section | DUAL | Human prose readable without callout blocks |
| Lore bible section | DUAL | No invented answers; OPEN flagged at point of need |
| Design system | DUAL | Tables for tokens; callouts for usage rules |
| Tech spec | DUAL | Numbered headings; callouts for stack decisions |
| Reformatting an existing doc | Identify first | Run STEP 3 (audit) then STEP 4 (reformat) |

---

## Examples

**Example 1 — New document creation (STEP 0 path)**
User asks to create a lore bible section. Claude identifies DUAL mode, confirms numbered headings + AI-readiness block required, plans callout placement for known OPEN items, writes with prose layer coherent without callout blocks, then runs STEP 3 before presenting.

**Example 2 — Reformat audit (STEP 3 → STEP 4)**
User says "this GDD section reads wrong." Claude identifies DUAL mode, runs STEP 3, finds 2 failures (orphaned callout blocks, missing prose layer), executes STEP 4 fixes in order, re-runs checklist to confirm all pass, increments version v1.0 → v1.1.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-lore-checker | Lore accuracy and OPEN item enforcement (Loop) |
| loop-extended-code-guardian | Code style, design tokens, component rules (Loop) |
| loop-core-tracker | File naming enforcement, version tracking, document register (Loop) |
| loop-core-decisions | Logging and retrieving LOCKED/OPEN decisions (Loop) |
| utility-game-gdd-enforcer | GDD completeness and production-readiness standards |
