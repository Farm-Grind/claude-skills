# GDD Standards Reference — Documentation Completeness and Production Readiness

Loaded by designer-games dispatcher when GDD domain activates.

## Table of Contents

- [PART 1 — The Document Ecosystem](#part-1)
- [PART 2 — The Production-Ready Test](#part-2)
- [PART 3 — Completeness Standards (per section type)](#part-3)
- [PART 3A — Question-Based Completeness Model](#part-3a)
- [PART 3B — Propagation Check](#part-3b)
- [PART 7 — The Ludonarrative Dissonance Check](#part-7)
- [PART 8 — Mobile-Specific Pre-Production Requirements](#part-8)
- [PART 9 — Quick Audit Protocol](#part-9)
- [Common Failure Patterns](#common-failure-patterns)
- [Examples](#examples)
- [Adversarial Self-Review](#adversarial-self-review)

---

## PART 1 — THE DOCUMENT ECOSYSTEM

A complete game requires six distinct document types. None can substitute
for another.

| Document | Primary audience | Function |
|---|---|---|
| GDD (Game Design Document) | Designers, developers, artists, producers | Defines what the game is: mechanics, systems, content, rules, scope |
| Lore Bible / Narrative Bible | Writers, designers, artists, marketing | Defines the world: history, characters, tone, lore, dialogue standards |
| Technical Design Document (TDD) | Developers | Defines how the game is built: architecture, data structures, APIs, state management |
| Design System / Art Bible | Artists, UI developers | Defines visual direction: tokens, typography, palettes, component rules |
| Sound Design Document (GSDD) | Audio, developers | Defines audio: pillars, asset inventory, implementation, technical constraints |
| Screen Inventory & Navigation Map | Developers, designers | Defines every screen, its contents, and all navigation flows |

**Loop application:** Load the current doc-register via loop-core-tracker to
get current versions and status for each document before auditing any section.

---

## PART 2 — THE PRODUCTION-READY TEST

**The single test for any GDD section:**
"Is this section complete enough that a developer could implement it without asking any design questions?"

If the answer is no, the section is a design stub. A stub that looks
complete is more dangerous than an obvious TODO — it misleads the implementer.

### What a production-ready section contains

| Element | Description |
|---|---|
| Player input | What the player does to trigger this mechanic |
| System response | What the system does in response |
| Output values/ranges | Specific numbers, ranges, or formulas — or explicit scaffolding flags |
| Edge cases | What happens at the boundaries (zero resources, max level, offline) |
| Failure states | What happens when the mechanic cannot complete |
| Integration points | Which other systems this mechanic connects to and how |
| Open items | Every TBD explicitly flagged with a ⚠ TODO, not left implicit |

### What a design stub looks like

| Stub pattern | Example | What's missing |
|---|---|---|
| Name + description only | "The Factory produces items automatically over cycles" | Queue size, cycle count, output calculation, interaction with Maintenance Panel |
| Values deferred without flag | "The player earns renown from requests" | How much? What formula? What's the range? |
| Integration not specified | "Consumables augment elemental performance" | Which parameters? What multiplier range? How do they interact with evolution boosts? |
| Edge case absent | "Progress floors at 0" | What happens at 0 when a penalty hits? Does the game still respond? |
| Implicit open item | A section with no TODO that references systems not yet designed | The open item must be flagged explicitly |

### The implementability levels (LoQ framework)

| Level | State | What it means |
|---|---|---|
| L0 — Design stub | Concept described | Developer cannot build without design sessions |
| L1 — Spec draft | Inputs, outputs, parameters defined | Developer can prototype but will have questions |
| L2 — Implementation-ready | All elements complete, edge cases covered, integration points specified | Developer can build to spec without design sessions |
| L3 — Integration-ready | Supporting systems (SFX, VFX, narrative, UI) specified | Feature can be polished |
| L4 — Ship-ready | Tuned from playtesting, values confirmed | Feature is complete |

**Target before coding starts: L2 for all core loop sections.** L3/L4 are
post-prototype activities.

### Definition of Ready vs. Definition of Done

**Definition of Ready (DoR):** Conditions a section must meet before it is
handed to a developer. A section fails DoR if it is missing any element
from the production-ready checklist above.

**Definition of Done (DoD):** Conditions that must be met for an
implementation to be considered complete. The GDD must specify what DoD
looks like for each mechanic.

Every GDD section at L2 should include a one-line DoD statement.
**Loop example:** "Foraging minigame is complete when: all zone configurations
render correctly, indicator speed scales per rarity tier, completion/cancel
flows both return to correct game state, and SFX/VFX integration points
are wired."

### IEEE SRS quality properties applied to GDD sections

**Unambiguous:** Open to only one interpretation. If two developers could
build different things from a section, it fails. Vague language ("the game
responds appropriately") is an automatic fail.

**Verifiable:** There is a way to confirm the implementation matches the
spec. "The indicator reverses direction on tap" is verifiable. "The minigame
feels engaging" is not.

**Traceable:** Every mechanic is traceable to its design purpose — the
player experience goal it serves. If you cannot state what player experience
goal a mechanic serves, question whether it belongs in v1.

### The script breakdown test

A GDD mechanic section is production-ready when it can be fully decomposed
into its implementation requirements. For any mechanic, enumerate:
- UI states required (idle, active, loading, success, cancel, error)
- Data required (what needs to be read from or written to the database)
- Sound events required (trigger conditions, asset names if known)
- Animation/VFX required (even as stubs)
- Cross-system dependencies
- Save/load behavior

### Design scaffolding vs. confirmed values

Every numeric value in a pre-prototype GDD is a calibration placeholder,
not a confirmed spec. Mark these explicitly:

- ⚠ TODO: — Design decision not yet made. Blocks implementation.
- ⚠ CALIBRATE: — Value specified but requires tuning after prototype.
  Does not block implementation; blocks balance pass.

**Loop application:** Treat all Loop balance values (cycle counts, mana
yields, renown amounts, foraging zone sizes, minigame speeds) as
⚠ CALIBRATE: until confirmed by a prototype session.

---

## PART 3 — COMPLETENESS STANDARDS (per section type)

**See:** `references/completeness-standards.md` in your project's reference
folder (if present). Contains per-section standards for: core loop mechanics,
minigames, economy, factions/NPCs, Lore Bible entries, Sound Design Document
sections, Design System checklist.

Load only the relevant part for the current audit task.

---

## PART 3A — QUESTION-BASED COMPLETENESS MODEL

A section is production-ready when it answers all the questions a developer
would ask before starting implementation.

**Derivation method — eight questions:**
1. What does the player do to enter/trigger this?
2. What does the system do in response?
3. What are all the output values or value ranges?
4. What happens when the player cancels or exits early?
5. What happens at the limits (zero, max, offline)?
6. Which other systems depend on or affect this?
7. How does the game state persist across sessions?
8. What does "this is done" look like for QA?

If the section cannot answer all eight, it is below L2. Surface each
unanswered question as a specific gap — never as a generic "needs work."

**Adversarial stress-test:** After drafting or auditing a section:
- Two systems both valid simultaneously — which wins?
- Player action during a transition state — is it handled?
- Value at boundary (0, 1, max−1, max) — is each case specified?
- Mechanic running while another system interrupts — what happens?

---

## PART 3B — PROPAGATION CHECK

When a section is updated, additions to one document often require updates
to others. Before marking any section production-ready:

- Does this section reference a mechanic also described in another GDD section?
  → Both sections must be consistent.
- Does this section introduce or change a named entity?
  → Check: Lore Bible, Sound Design, Screen Inventory, canon registry.
- Does this section affect the economy model?
  → Verify the economy GDD section is consistent.
- Does this section change a value specified elsewhere?
  → Find all prior references and mark them for update.

```
⚠ PROPAGATION: This change requires updates to:
  - [Document/section] — [what needs to change]
```

---

## PART 7 — THE LUDONARRATIVE DISSONANCE CHECK

Every core mechanic must have an in-world explanation consistent with the lore.

Apply this check to any mechanic:
1. What is the player doing mechanically?
2. What is the player doing in the fiction of the world?
3. Do these tell the same story?

**Loop examples:**
- The Ritual minigame: Player inputs symbols → Hero performs elemental
  conjuration. ✓ Aligned.
- Save scumming: Player reloads the app → The time loop resets partially.
  ✓ Deliberately aligned.
- Factory Golems: Automated production → Magical constructs built for
  repetitive labor. ✓ Aligned.
- Cards of Fate: Player draws cards → Hero reads fortune for the cycle.
  ✓ Aligned.

Flag any mechanic where the fictional explanation is absent or weak. Route
to lore documentation for resolution — do not invent in-world explanations
inline.

---

## PART 8 — MOBILE-SPECIFIC PRE-PRODUCTION REQUIREMENTS

These are frequently absent from indie GDDs and cause late-production rework.

| Requirement | Loop status |
|---|---|
| Bundle size target | Confirmed: under 100MB initial download |
| Min iOS/Android versions | Confirmed: iOS 15, Android 8.0 |
| Offline behavior fully specified | Confirmed: no offline accumulation |
| Audio format and compression strategy | OPEN — not in sound design doc |
| Accessibility settings | Partially addressed — speed reduction TBD |
| GDPR/CCPA data handling | Confirmed in §18.6 |
| Age rating target | Confirmed: 12+/Teen |
| In-app purchase compliance | Confirmed: $1.00 unlock, no IAP at launch |
| Save conflict resolution | Confirmed: last-write-wins |
| Push notification opt-in | Confirmed: daily login reminder opt-in only |

**For other projects:** Verify each row against your tech spec. Flag any
OPEN item before marking mobile requirements as addressed.

---

## PART 9 — QUICK AUDIT PROTOCOL

1. **Identify section type** — core loop / minigame / economy / faction / other
2. **Derive the question set** (PART 3A)
3. **Score LoQ level** — L0/L1/L2/L3/L4
4. **Apply IEEE properties** — unambiguous, verifiable, traceable
5. **Adversarial stress-test** (PART 3A)
6. **Propagation check** (PART 3B)
7. **Mobile requirements** (PART 8)
8. **Ludonarrative check** (PART 7) — if mechanic-facing
9. **Post-audit comment:** If result is below Production-ready, post a
   comment to the GDD page:
   ```
   ⚠ GDD FLAG [YYYY-MM-DD]: [Section name] — L[N] [label]
   DoR: [Pass / Fail — missing elements]
   Gaps: [one sentence per gap]
   Verdict: Needs work before implementation.
   ```

**Report format:**
```
AUDIT — [Section name]
Level: L[0-4] — [label]
DoR: Pass / Fail — [missing elements]
IEEE: Unambiguous / Verifiable / Traceable
Stress-test: Pass / Fail — [failure if any]
Propagation: [required updates or "none"]
Verdict: Production-ready / Needs work — [specific gaps]
```

---

## COMMON FAILURE PATTERNS

| Pattern | What it looks like | Correct behavior |
|---|---|---|
| Stub presented as complete | Prose description but no values, edge cases, or integration points | Apply DoR test; flag as L0/L1; list missing elements |
| Open items left implicit | References systems not yet designed with no TODO | Add explicit ⚠ TODO for every undefined dependency |
| Scaffolding presented as confirmed | Pre-prototype numbers with no CALIBRATE flag | Mark all unvalidated values as ⚠ CALIBRATE: |
| Ambiguous spec | Two developers would build different things | Apply IEEE unambiguous test; rewrite until one implementation is possible |
| No verifiable criterion | Spec describes feel but not behavior | Add at least one testable Given-When-Then scenario per mechanic |
| Sunny day only | Cancel, empty, offline, cap states not documented | Document all interaction states |
| No DoD statement | Section lacks a definition of when implementation is complete | Add one-line DoD to every L2 section |
| Ecosystem gap ignored | Asking about GDD sections while Screen Inventory has missing critical sections | Flag the ecosystem gap before proceeding |
| Mobile requirements missed | Audio format, accessibility, bundle size not addressed | Check Part 8 before any section is marked production-ready |
| Ludonarrative disconnect | Mechanic designed without checking fictional explanation | Run Part 7 check on every new mechanic |
| Lore Bible used as GDD | Mechanics described in Lore Bible but not GDD | Lore Bible owns canon; GDD owns mechanics |

---

## Examples

**Example 1 — Section scored L1, not L2**

Section reviewed: "Factory queue mechanic — items are produced over cycles."

```
AUDIT — Factory queue mechanic
Level: L1 — Spec draft
DoR: Fail — missing: output values, edge cases (queue full / empty), cancel behavior, failure state
IEEE: Unambiguous ✗ (queue size undefined) / Verifiable ✗ (no success criterion) / Traceable ✓
Stress-test: Fail — player queues item while Factory is full: unhandled
Propagation: check Workshop queue for consistency; flag Save/load behavior OPEN
Verdict: Needs work — answer all 8 PART 3A questions before L2 target met
```

Challenge 1: no L2 verdict issued — section is L1.
Challenge 2: DoR Fail confirmed against all 7 elements.
Challenge 3: Lore explanation absent → flagged `[OPEN: lore — route to Lore Bible]`, not invented.

**Example 2 — Scope routing catch**

Auditor identifies that Ritual section lacks an in-world explanation.

```
GDD enforcer self-review:
  Challenge 3 — Scope routing: BLOCKED — in-world explanation is lore, not GDD.
    Flagged as [OPEN: lore — route to Lore Bible] rather than filled inline.
  Status: BLOCKED — rerouted lore gap before delivering
```

---

## ADVERSARIAL SELF-REVIEW

Run this section after every audit output, before delivering results.

### Challenge 1 — Implementability

**Failure mode:** Audit passes a section as L2 when it is actually L1.

**FAIL example:**
```
"The Crucible minigame section is complete. It describes the progress bar,
the indicator, and the tap mechanic." ← L2 verdict issued.
(But: cancel behavior? Minimum acceptable result? Success threshold?
None answered — this is L1 at best.)
```

**FIX:** Before issuing any L2 verdict, run the full PART 3A eight-question
set explicitly. If any question returns "not answered," the section is not
L2. Name the specific unanswered questions.

Severity: CRITICAL.

### Challenge 2 — DoR completeness

**Failure mode:** Audit confirms DoR Pass from overall impression, not
checklist.

**FIX:** Before writing "DoR: Pass," confirm each of the seven elements:
1. Player input ✓/✗
2. System response ✓/✗
3. Output values/ranges ✓/✗ (or ⚠ CALIBRATE: flag present)
4. Edge cases ✓/✗
5. Failure states ✓/✗
6. Integration points ✓/✗
7. Open items flagged ✓/✗

Severity: HIGH.

### Challenge 3 — Scope routing

**Failure mode:** Audit fills a gap inline when the gap belongs in a
different document.

**FAIL example:**
```
"The Ritual section is missing the in-world explanation for why the Hero
performs the ritual. Adding: 'The Hero channels elemental mana through
ancient Ark symbology...'" ← This is lore invention.
```

**FIX:** Before proposing a fill:
- Lore/canon question? → flag `[OPEN: lore — route to Lore Bible]`
- Balance/value question? → flag `⚠ CALIBRATE:`, activate IDLE-MATH domain
- Narrative question? → route to narrative design documentation
- Documentation completeness gap? → fill it here

Severity: HIGH.

### Confirmation block (required before delivering any audit output)

**HARD FAIL:** MUST NOT deliver any GDD audit output before this block is produced and all challenges clear.

```
GDD enforcer self-review:
  Challenge 1 — Implementability: [L2 verdict confirmed against all 8 PART 3A questions, or "no L2 verdict issued"]
  Challenge 2 — DoR completeness: [all 7 elements checked, or "DoR Fail — [missing elements]"]
  Challenge 3 — Scope routing: [gaps routed correctly, or "rerouted — [what and where]"]
  Status: CLEAR to deliver / BLOCKED — [reason]
```
