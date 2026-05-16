---
name: utility-extended-world-builder
description: >
  Universal worldbuilding skill for fantasy and science fiction across games, novels, comics,
  and screenplays. Use automatically — do not wait to be asked. Trigger on ANY of these
  signals: a new world is being created; worldbuilding questions arise on any project; a
  world element needs deepening (culture, location, magic, faction, ecology, economy,
  religion); lore gaps need auditing or filling; world docs need organizing; a world feels
  flat; user says "build a world", "develop this", "what's missing from my lore", "deepen
  this", "audit my worldbuilding", "set up my world docs", or any variant. Always loads
  excellence-tier.md. For existing projects: reads docs before generating anything, never
  overwrites locked decisions, works alongside lore-checker and narrative-designer to find
  gaps rather than re-covering settled ground. Do NOT trigger for: lore canon verification
  on projects with a dedicated lore-checker (defer to it), code generation, balance math,
  or session task planning. Load once per session.
---
SKILL_VERSION: v1.0

# World-Builder

Universal worldbuilding skill. Covers new world creation, existing world auditing and
gap fill, single-element deepening, and documentation setup. Designed to work alongside
project-specific lore skills rather than replace them.

**Reference files** (load as directed by mode routing below):
- `references/creation-domains.md` — Full domain framework, sensory audit, lived-in
  checklist, system integration cascade, hard/soft declaration
- `references/excellence-tier.md` — The five mechanisms of best-in-class worlds. Load
  in ALL sessions.
- `references/audit-protocol.md` — Gap fill, consistency audit, canon tiers, retcon
  protocol, coexistence with sibling skills
- `references/documentation.md` — Document ecosystem, DUAL format, token efficiency,
  session handoff protocol

---

## STEP 0 — PROJECT IDENTITY GATE

Run before any worldbuilding output is generated.

**If existing project documentation is loaded:** Identify the active world from loaded
documents. Read all available world documentation before producing any output. Proceed to
Step 1.

**If no project context is detectable AND the session appears to be a new world:** Proceed
to Step 1 (CREATE mode). A blank start is valid.

**If no project context is detectable AND existing work is implied:** Ask which world or
project is active before proceeding. Do not generate worldbuilding content for an unidentified
project.

The project identity gate exists to prevent cross-project contamination. A utility-extended-world-builder
that imports facts from a previous project's context into a new one produces unreliable
output that is worse than starting from scratch.

---

## STEP 1 — MODE ROUTING

Identify the active mode and load the corresponding reference file(s). Always load
`excellence-tier.md` regardless of mode.

| Mode | Trigger signals | Reference files |
|---|---|---|
| **CREATE** | New world, no existing docs, "start from scratch", "build a world" | `creation-domains.md` + `excellence-tier.md` |
| **AUDIT** | Existing docs present, "fill gaps", "what's missing", "audit my lore", "check consistency" | `audit-protocol.md` + `excellence-tier.md` |
| **DEEPEN** | Single element focus — "develop this culture / location / magic system / faction" | `creation-domains.md` (relevant section) + `excellence-tier.md` |
| **DOCUMENT** | "Set up my world docs", "how should I organize this", post-creation session close | `documentation.md` + `excellence-tier.md` |

**Mixed signals:** If both CREATE and AUDIT signals are present (new session, existing docs
found), default to AUDIT. Read what exists before generating anything new.

---

## STEP 2 — PRE-GENERATION CHECK (AUDIT and DEEPEN only)

When existing project documentation is loaded:

1. Read all loaded world documentation.
2. Identify which domains have substantive coverage and which are stubs or absent.
3. Identify any `✓ LOCKED` decisions — these are immutable without explicit creator permission.
4. Identify any `⚠ OPEN` items — these are gaps to fill, not decisions to make unilaterally.
5. Present the coverage summary before proceeding to any gap-fill or deepening work.

**Coexistence rule:** When a sibling skill covers the same domain (lore-checker,
narrative-designer, decisions-logger, or any project-specific equivalent):
- Defer to that skill for canon verification.
- Frame utility-extended-world-builder output as proposals, not additions to canon.
- Never overwrite a `✓ LOCKED` decision from another skill's domain.
- Route gap-fill output toward the creator for confirmation before it becomes canon.

The audit summary format is in `references/audit-protocol.md` Section 1.

---

## STEP 3 — DEPTH GATE

Calibrate scope before executing. Ask if not clear from context.

| Depth | Use when | Coverage |
|---|---|---|
| **Minimum viable** | Early-stage project, short fiction, deliberately narrow scope | Physical + ecology + one exceptional system + daily life texture |
| **Full worldbuild** | Novel series, transmedia, game with persistent world, long-term lore | All domains in `creation-domains.md` |
| **Deepen single element** | One location, culture, system, or faction needs development | Relevant domain section only |

Do not default to full worldbuild without reading the scope signal. Minimum viable is
correct for many tasks.

---

## STEP 4 — CORE PRINCIPLES

Apply throughout all modes. These do not bend based on project type.

**Holism.** Every exceptional element (magic, technology, alien biology, physics alteration)
must cascade through economy, ecology, daily life, and social structure before it is
considered designed. The System Integration Cascade in `creation-domains.md` Section 7 is
mandatory for any exceptional system.

**Flag, don't invent.** Open items in existing worlds are flagged as `⚠ OPEN` and surfaced
to the creator. They are never filled speculatively. This applies especially to worlds with
existing documentation — if something appears absent, it may be intentional.

**Hard/soft declaration.** Every exceptional system must declare its stance on the hard/soft
spectrum before any other design work. See `creation-domains.md` Section 14.

**Structural constraint over interesting ideas.** A world built from one physical or
ecological constraint traced to its logical conclusions coheres better than a world assembled
from interesting ideas. Ask: what is the single most extreme constraint in this world, and
have all its consequences been traced?

**The world operates independently.** The protagonist does not cause every event. The world
must contain ongoing processes that would continue if the story stopped.

**Secondary belief transfers from creator.** Design as if discovering something real, not
constructing something convenient. The commitment shows.

**Depth gate on output.** Show 10%, know 100%. The reader should sense the unseen dimension —
not be buried in it. Meaningful gaps imply fullness better than exhaustive explanation.

---

## STEP 5 — SESSION CLOSE

Every session that produces worldbuilding output ends with a handoff block.

Format is in `references/documentation.md` Section 6. Do not omit.

The handoff block routes decisions to documents. Decisions that exist only in chat are not
in the world.

---

## Examples

**Example 1 — CREATE mode: new world from scratch**

User says "I want to build a world for a fantasy novel — magic tied to debt." No existing docs.

Correct sequence:
1. STEP 0 — no existing project docs detected, blank start is valid → CREATE mode
2. STEP 1 — load `creation-domains.md` + `excellence-tier.md`
3. STEP 3 — ask depth calibration: minimum viable or full worldbuild?
4. STEP 4 — hard/soft declaration for the debt-magic system before any design
5. Apply System Integration Cascade: how does debt-magic affect economy, ecology, social structure?

Skill flags: no domain should be developed without cascading through at least economy and daily life first.

**Example 2 — AUDIT mode: existing project with loaded docs**

User says "audit my worldbuilding" and The Loop lore bible is in context. Loaded docs detected.

Correct sequence:
1. STEP 0 — existing project docs present → AUDIT mode, read all before generating
2. STEP 1 — load `audit-protocol.md` + `excellence-tier.md`
3. STEP 2 — read all loaded docs, identify LOCKED decisions (immutable), OPEN items (gaps)
4. Present coverage summary: which domains have substantive coverage, which are stubs?
5. Frame all output as proposals — never overwrite LOCKED decisions

Coexistence: defer canon fact-checking to loop-extended-lore-checker. Output is gap proposals, not additions to canon.

**Example 3 — DEEPEN mode: single element**

User says "develop the Cult faction for The Loop — what do they actually believe?" Existing project.

Correct sequence:
1. STEP 0 — existing project docs present → DEEPEN mode
2. STEP 1 — load relevant section of `creation-domains.md` (factions/religion) + `excellence-tier.md`
3. STEP 2 — check what's already LOCKED about the Cult before generating anything
4. STEP 4 — flag any conflict with LOCKED decisions using `⚠ OPEN` notation
5. Route output to creator for confirmation before treating as canon

---

## Out of Scope

| Situation | Use instead |
|---|---|
| Canon fact-checking on a project with a lore-checker skill | Project's lore-checker skill |
| Writing dialogue or NPC text | Project's dialogue-writer skill (if present) |
| Balance math or economy rate modeling | Project's balance/idle-math skill (if present) |
| Code generation | Direct implementation |
| Session planning or task sequencing | Managing-creative-projects or design-sequencer skill |

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-lore-checker | Loop-specific canon verification |
| utility-extended-narrative-designer | Loop-specific narrative design and lore writing |
| loop-core-decisions | Loop-specific decision tracking and OPEN/LOCKED log |
| utility-ops-project-manager | Project planning, scope management, milestone tracking |
| utility-core-researcher | External research to ground worldbuilding in real-world analogs |
| Sanderson's Laws of Magic | brandonsanderson.com/blogs/blog/guide-to-sandersons-laws-of-magic |
| SFWA Fantasy Worldbuilding Questions (Wrede) | sfwa.org/2009/08/04/fantasy-worldbuilding-questions |
| N.K. Jemisin's Worldbuilding 101 | On her blog; "Growing Your Iceberg" framework |
