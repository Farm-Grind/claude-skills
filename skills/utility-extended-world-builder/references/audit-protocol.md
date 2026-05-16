# Audit Protocol — Gap Fill & Consistency

This file is loaded in AUDIT mode and when existing project documentation is detected.
It governs how world-builder operates on worlds that already exist.

---

## TABLE OF CONTENTS

1. Pre-Audit Read Requirement
2. Wolf's Three Factors
3. Gap Classification
4. Consistency Audit
5. Canon Tier Setup
6. Retcon Protocol
7. Coexistence with Sibling Skills

---

## 1. PRE-AUDIT READ REQUIREMENT

Read all loaded project documentation before producing any output. This is non-negotiable.

Do not apply a generic template over an existing world. Do not invent to fill gaps. Do not
suggest changes to LOCKED decisions. The world exists; the audit's job is to map it, not
redesign it.

After reading, produce a summary of what is confirmed before identifying what is missing:

```
WORLD AUDIT — [Project Name]
Status: Existing documentation loaded.

Confirmed coverage:
- [List domains with substantive existing content]

Thin or absent coverage:
- [List domains with minimal or no content]

Open items identified in documentation:
- [List any ⚠ OPEN or TBD flags found]

Potential gaps (not confirmed open — require review):
- [List areas where coverage appears incomplete]
```

Present this before proceeding to any gap-fill work.

---

## 2. WOLF'S THREE FACTORS

Mark J.P. Wolf's framework for evaluating any secondary world:

**Invention** — how much differs from primary-world reality. Too little: the world feels
like a renamed version of Earth. Too much simultaneously: the reader loses footing.
The balance point is project-specific, but most worlds are under-invented in daily life
and over-invented in exceptional systems.

**Completeness** — how fully developed the world is across all domains. Most worlds have
strong coverage in two or three domains and stubs everywhere else. The audit identifies
which domains are production-ready and which are design stubs.

Production-ready: a developer, writer, or artist could work from this section without
asking design questions.
Design stub: the section names something but doesn't define it fully enough to act on.

**Consistency** — internal logical coherence. Elements that contradict each other, systems
that violate their own stated rules, or history that doesn't add up to the current state.

The audit scores each domain against all three factors and prioritizes gaps accordingly.

---

## 3. GAP CLASSIFICATION

Not all gaps are equal. Classify before recommending action.

| Type | Description | Action |
|---|---|---|
| **Intentional mystery** | Gap is deliberate — ambiguity is a design choice | Flag, respect, do not fill |
| **Oversight gap** | Something that should have been decided but wasn't | Flag as OPEN, surface to creator |
| **Stub** | Section exists but has no substantive content | Flag as incomplete, offer to develop |
| **Contradiction** | Two elements conflict | Surface both, defer to creator for resolution |
| **Missing cascade** | Exceptional system exists but cascade wasn't run | Offer to run Section 7 |

Never fill an oversight gap speculatively. Never resolve a contradiction unilaterally.
The creator decides what is OPEN vs. intentional mystery. The audit surfaces; it does not resolve.

---

## 4. CONSISTENCY AUDIT

### First-appearance tracking

For each exceptional element (magic creature, technology, cultural practice, rule):
- When was it first established?
- Is it described consistently in every subsequent mention?
- Does any later mention contradict the initial establishment?

### Timeline coherence

- Do historical events lead logically to the current state?
- Does the timeline contain gaps that imply events that weren't documented?
- Are gaps intentional (history the characters don't know) or oversight gaps?

### Cascade coherence

For each exceptional system:
- Was the System Integration Cascade run? If not, are there visible inconsistencies in
  how the system affects adjacent domains?
- Common failure: magic exists but the economy doesn't reflect it. Technology exists but
  warfare hasn't changed. The cascade catches these.

### The Tatooine test

Star Wars: Tatooine is a desert planet whose ability to sustain life is never explained
in the films. This is an oversight gap — not a fatal one for a space opera, but one that
requires retcon in expanded material.

For any world element that seems load-bearing: could a reader ask "but how does that work?"
and have no answer available? If so, is that intentional mystery or oversight gap?

---

## 5. CANON TIER SETUP

For new projects or projects planning transmedia expansion, establish canon tiers early.

**Minimal useful model (solo projects):**

| Tier | Description |
|---|---|
| Primary canon | What the main work establishes — the game, the novel, the core series |
| Extended canon | Spinoffs, tie-ins, supplementary material — canon unless contradicted by primary |
| Development notes | OPEN design decisions, scrapped ideas, rejected drafts — explicitly non-canon |

**Decision tracking:**

Every design decision is either:
- `✓ LOCKED` — decided, do not reinvent, do not contradict
- `⚠ OPEN` — unresolved, do not fill speculatively, surface to creator
- `⚠ DO NOT INVENT` — high-risk open item; hallucination especially likely here

These markers apply regardless of project type (game, novel, comic, screenplay). The
vocabulary is neutral — "LOCKED" means decided, not published or final.

For projects with existing lore documentation: if a sibling skill (lore-checker,
narrative-designer, decisions-logger) tracks these, defer to that skill's canonical record.
Do not maintain a parallel record that could diverge.

---

## 6. RETCON PROTOCOL

When a LOCKED decision is overturned:

1. Document what changed, why, and when.
2. Identify all downstream decisions that depended on the overturned item.
3. Surface those downstream items to the creator — do not resolve them automatically.
4. Update the canon record (through the relevant decisions-tracking skill if one exists).

The timeline document (if one exists) should log retcons explicitly. Intentional gaps
("the historian forgot") are different from oversight gaps ("we never decided this") —
both are different from retcons ("we decided this, then changed it"). All three need
different handling in production.

---

## 7. COEXISTENCE WITH SIBLING SKILLS

When a project has existing worldbuilding skills (lore-checker, narrative-designer,
decisions-logger, or project-specific equivalents):

- **Read first.** Load and review sibling skill outputs or documentation before generating
  any world content. The existing world state is authoritative.
- **Defer on canon.** If a lore-checker skill exists, any canon verification question routes
  to that skill. World-builder does not adjudicate canon.
- **Complement, don't duplicate.** World-builder's role is to identify gaps in coverage and
  develop them — not to re-cover settled ground.
- **Flag, don't fill.** If an apparent gap could be intentional in context of the sibling
  skill's established canon, flag it as a question rather than filling it.
- **Route output.** Gap-fill output should be framed as proposals for the creator to confirm,
  not as additions to the canon record. The lore-checker or decisions-logger locks it;
  world-builder surfaces it.

This applies specifically to The Loop and any other project with established project
documentation: world-builder never overwrites a LOCKED decision in another skill's domain.
