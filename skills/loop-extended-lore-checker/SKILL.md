---
name: loop-extended-lore-checker
description: >
  Checks lore content, NPC dialogue, item descriptions, location copy, and
  world-building text against The Loop confirmed canon. Catches contradictions,
  invented answers to OPEN items, and naming errors before they propagate.
  Use automatically - do not wait to be asked. Trigger on ANY of these signals:
  in-world text is being written (NPC dialogue, item names, descriptions,
  location names, faction names, ability names, quest text, tutorial text,
  UI labels with lore weight); a lore question is asked ("what is X", "how
  does Y work", "who is Z"); new world-building content is developed or
  proposed; a new entity is being named for the first time; any content
  references the Hero, Familiar, Ryszard, the Ark, the Swarm, the Collapse,
  the Dreaming, or the Loop; design exploration generates a world-state claim,
  even without explicit in-world text. Do NOT trigger for: pure coding
  sessions, balance math, checklist or planning work, or mechanic design
  generating no world-state claim. Load once per session.
---
SKILL_VERSION: v1.6

# The Loop — Lore Consistency Checker

Runs a pre-generation check on any lore-adjacent content to catch
contradictions, naming errors, and attempts to fill OPEN items before they
propagate into documents or code.

---

## Pre-Generation Protocol

Before writing any lore content, dialogue, or in-world copy — and before
responding in any design exploration turn where this skill was triggered:

0. **DESIGN EXPLORATION CHECK:** Ask internally — does any claim in this
   response assert something as true about the Loop world? A world-state
   claim is any assertion about how the Loop world is structured, functions,
   or is governed — including implications from mechanic proposals (e.g.
   "the Loops are agricultural infrastructure" implies something about the
   world economy). MUST run this check before responding in any design
   exploration turn where this skill was triggered. Skipping this check
   when a world-state claim is present is a HARD FAIL — do not respond
   until the check runs. If a world-state claim is found: proceed with
   steps 1–5. Label any claim not confirmed in a loaded source as
   `[INFERENCE: description]` rather than stating it as fact.

1. Identify all lore elements the content will touch (characters, locations,
   factions, mechanics, history)
2. Cross-reference the Canon Quick Reference section below. When the canon
   registry (loop-extended-canon) is loaded this session, query it by
   keyword for any fact you're about to assert — a registry hit is a verified
   citation; a miss means unregistered, not false. For complex content also
   check the current lore bible (most recent CURRENT version in doc-register).
3. For each element, verify:
   - Is it confirmed canon? → Use it exactly as defined
   - Is it OPEN/unresolved? → Flag it, do not invent an answer
   - Is it PLANNED (decided but not yet in-world text)? → Flag it as aspirational,
     do not treat as established world fact in player-facing content
   - Is it a new element? → Flag it for naming review before committing
4. If any element is OPEN, surface it before generating:

```
⚠ OPEN ITEMS — cannot generate this content without inventing answers:
  - [Item]: [what is unknown and why it matters]

Resolve these first, or proceed with [OPEN: description] placeholder markers
so you can fill them in later.
```

5. Only generate content if all lore elements are either confirmed or can be
   handled with explicit placeholders.

---

## Canon Quick Reference

Key facts most likely to be needed in lore generation, dialogue, and copy.
For exhaustive detail, check the current lore bible (most recent CURRENT
version in doc-register).

### Confirmed names and terminology

| Element | Confirmed name | Never use |
|---|---|---|
| The ship | the Ark | "the ship", "the vessel", "The Ark" (lowercase "the") |
| Farming location | The Dreaming | "the farm", "the fields" |
| Combat/elemental location | The Rift | "the arena", "the chamber" |
| Hidden endgame location | The Void | "the darkness", "the abyss" |
| Arcane location | The Tower | "the castle", "the spire" |
| Player character | the Hero | "the player", "the protagonist" |
| Player's companion | the Familiar | "the guide", "the spirit" |
| The Familiar's kind | Sprite (a Sprite) | "fairy", "sprite" (lowercase) |
| Governing body | the Council | "the government", "the leaders" |
| Military force | the Fleet | "the army", "the military" |
| Primary antagonist species | the Swarm | "the demons", "the monsters" |
| Antagonist mastermind | the Lord of Whispers | "the Demon God", "the Dark One" |
| Corrupted dragon | the World Dragon | "Leviathan" (Leviathan is its pre-corruption name) |
| Human-like mortals | Humans | "people", "mortals" (generic) |
| The repeating cycle | the Loop | "the cycle", "the simulation" |
| Refined magical resource | Aether | "mana crystals", "pure mana" |
| Base magical resource | mana | "magic", "energy" (in mechanical context) |

### The five elements (always capitalized in UI text)

Fire · Water · Earth · Air · Mana

Classical opposing pairs (classical four): Fire/Water, Earth/Air — map to
Council tension. Mana is the Familiar's element and the base economy resource;
it does not map to Council faction alignment.

---

### Factions — confirmed existence and operating logic

| Faction | Role | Operating logic |
|---|---|---|
| the Council | Public governing body of the Ark | Theater — real power sits with Ryszard's inner org |
| the Fleet | Military arm | Commanded by Admirals (Fire/Air/Water confirmed; Earth Admiral name TBD) |
| the Cult | Fanatical faction, antagonist | Pipeline: low-tier recruits → radicalization → Void contact → corruption |
| the Heart | Anti-shadow-layer resistance | Anonymous, uses dead drops; entirely separate from and opposed to the Cult |
| the Eye | Shadow layer — intelligence arm | Monitors and alters inter-Loop mail freely, no authorization required |
| the Voice | Shadow layer — narrative arm | Controls official information and propaganda |
| the Hand | Shadow layer — intervention arm | Direct action, last resort only |

**NEVER write:** the Eye/Voice/Hand as known to ordinary citizens, the Familiar,
or the Hero at game start. Their existence is the shadow layer reveal.
**NEVER write:** the Heart as part of or allied with the Cult — they are opposed.
**NEVER write:** the Hand as the primary control mechanism — information
asymmetry (Eye) and narrative control (Voice) are the primary tools.

### What the Hero is — and is not

- CONFIRMED: Exists in "Half-life" — not dead, not alive. Physical form almost
  entirely destroyed by the Swarm during the Collapse, but high mana content
  prevented full consumption. Drifted through the Void in dreamless stasis,
  severed from the Dreaming. Summoning reconstitutes them from residual matter.
- CONFIRMED: Recovers mana manipulation only at game start — cannot generate
  mana. Arc is recovery (rebuilding power), not redemption.
- CONFIRMED: Does not know the full nature of their situation at game start.
- CONFIRMED: The Hero IS the player. No visual representation, no avatar, no
  in-game name input. Platform account display name used if a name is required.
- OPEN: The Hero's specific element, magical specialty, and pre-Collapse backstory.
- NEVER write: the Hero as willing, informed, or free. They are none of these.
- NEVER write: the Hero as a separate character from the player — no pronouns,
  no physical description, no named identity.

### What the Familiar is — and is not

- CONFIRMED: A Mana Sprite. Shapeshifter — starting forms limited to
  primal-mythical variants (natural creature base + eldritch features).
  Element: Mana (locked). Player assigns nickname; true name unpronounceable
  by mortals.
- CONFIRMED: Permanently bound to this Loop since its creation. Irreplaceable —
  if the Familiar dies, the Loop collapses permanently. Cannot leave the Loop.
- CONFIRMED: Emotional arc — quietly polite, functional, standoffish. Watchful
  and guarded with the new Hero due to previous custodian trauma. Earned trust
  expressed through dialogue and progressively unlocked form variants.
- CONFIRMED: Has Comms Array access and inter-Loop mail. Instantly aware of all
  cycle events at Dreaming entry. Partially reduced state until Loop is restored.
- CONFIRMED: Entirely unaware of the Eye, Voice, Hand, or Master. Knows the
  Heart only as the most fanatical Cult sect. Discovers the shadow layer truth
  alongside the player.
- CONFIRMED: Knows all previous custodians but is constrained in discussing them.
- OPEN: The Familiar's nickname (player-assigned). Visual design lock.
- NEVER write: the Familiar as a simple friendly guide, a servant, or someone
  who volunteers information freely. They are constrained, complicated, and
  carry unresolved grief from the previous custodian.
- NEVER write: the Familiar as aware of the three-layer conspiracy (Eye/Voice/
  Hand/Master). They are as ignorant of it as the player at game start.

### Ryszard

- CONFIRMED: Human-origin post-human. Self-ascended to god-tier power through
  dimensional merge — unprecedented in setting history. They/them pronouns.
  Full name: Ryszard Von Levy.
  Inspirations: Rick Sanchez, Doctor Doom, Angstrom Levy, The God Emperor.
- CONFIRMED: Controls the Ark through a classified inner organization, not
  the Council directly. The Council is public theater.
- NEVER write: Ryszard as benevolent, transparent, or acting for others'
  benefit. Their calculus is purely strategic survival.

### The Collapse

- CONFIRMED: The Lord of Whispers used Cult rituals across multiple dimensions
  to seize the World Dragon's mind and body, releasing its barrier. The Cult's
  ancestors caused the Collapse.
- CONFIRMED: Not a single event — a prolonged unraveling. Recent history,
  within living memory of older survivors.
- OPEN: Origin of the Void itself. Origin of the Lord of Whispers.

---

## OPEN Items — Never Invent These

Load the live open items from the decisions log via Notion MCP before checking:

```
Fetch Notion decisions log (page ID: 33b3a41dd33d811ea614c06aa9cb646e)
Filter for entries where status = "OPEN" or status = "DEFERRED"
```

Use the live OPEN/DEFERRED entries as the authoritative list. Do not rely on
any hardcoded list — the decisions log is the source of truth.

If the decisions log is unavailable, flag it explicitly rather than proceeding:
`⚠ Cannot verify OPEN items — decisions log unavailable. Proceed with caution
  or resolve before generating lore content.`

If content touches any active open item, use an explicit placeholder:
`[OPEN: Familiar's name]` — never invent.

---

## Post-Generation Audit

After generating any lore content:

1. Scan for any names, terms, or facts not in the canon reference
2. Scan for any OPEN items that appear to have been answered implicitly
3. Scan for any contradictions with confirmed canon
4. **Temporal consistency gate:** If content describes a state, relationship,
   or condition that changes over narrative time (before/after an event, early
   vs. late game, pre/post-Collapse), verify the temporal anchor is correct.
   A fact confirmed for one point in the timeline is not valid for all points.
   Flag temporal mismatches as violations even if the underlying fact is canon.
5. **Design reference document rule:** When the output is a design reference
   document, internal archive, or any document not flagged as narrative fiction —
   scan every claim about NPC behavior, faction behavior, institutional behavior,
   named character behavior, and cultural practices. Each such claim must be
   either (a) directly sourced from loaded canon, or (b) flagged as
   [OPEN: invented — needs review] before inclusion. Atmospheric flavor, worker
   quotes, institutional opinions, and undocumented cultural practices are lore
   invention. Do not include them in design reference documents without explicit
   author confirmation.
6. If issues found: list ALL issues first, then present the content below a
   clear separator — never interleave issues with content
7. If clean: `✓ Lore check passed.`
8. **Post-flag comment:** For any OPEN item or lore violation flagged, post a
   comment to the relevant GDD or Lore Bible Notion page using `notion-create-comment`.
   Comment format:
   ```
   ⚠ LORE FLAG [YYYY-MM-DD]: [Issue type — OPEN ITEM / VIOLATION / NAMING ERROR]
   [One sentence describing what was flagged and why]
   Logged: D-[XXX] (if a decision ID exists) / Decisions log (if no D-ID yet)
   ```
   Target the most specific page relevant to the content being checked.
   Known GDD/Lore page IDs are in the tracker skill.
   If the page ID is unknown, skip the comment rather than guessing.
   This step is best-effort — a comment failure must not block the lore check output.

---

## Partial-Lock Handling

Most lore tasks touch both confirmed and OPEN elements simultaneously. When
this happens:

- Generate freely on confirmed elements — do not block the whole task
- Insert `[OPEN: description]` placeholders exactly where OPEN elements would
  appear — do not skip those beats or write around them
- List the placeholders inserted at the end of the output so the human knows
  exactly what needs to be resolved
- Never let a confirmed element's presence imply permission to fill an adjacent
  OPEN element

---

## Placeholder Format

When content must reference an OPEN item, use this format consistently
so it's easy to find and fill later:

```
[OPEN: Familiar's name]
[OPEN: Hero's element]
[OPEN: inciting incident summary]
[OPEN: Fire Admiral's name]
```

When a design exploration turn makes a claim about the world not confirmed
in a loaded source, label it with an INFERENCE marker:

```
[INFERENCE: the Loops are agricultural infrastructure — confirm against lore bible]
[INFERENCE: the Fleet patrols the Rift perimeter — source not verified this session]
```

INFERENCE markers mean: plausible given context, not yet canon. Do not treat
as confirmed in any subsequent session without loading the source.

These markers should survive into documents and code comments so they're
never accidentally shipped as final content.

---

## Examples

**Example 1 - Pre-generation block on OPEN item**

User asks Claude to write the Familiar's introduction dialogue.
Lore checker fires before generating:

```
OPEN ITEMS - cannot generate this content without inventing answers:
  - Familiar nickname: player-assigned, not yet determined

Resolve these first, or generate with [OPEN: Familiar's name] placeholder.
```

**Example 2 - Canon violation caught post-generation**

Generated text refers to "the Heart" as a Cult splinter group.
Post-generation audit catches the contradiction:

```
LORE ISSUES FOUND:
  - "the Heart" described as a Cult sect - INCORRECT. The Heart is an
    anti-Cult resistance group, entirely opposed to the Cult.

Corrected content below:
---
[corrected text]
```

**Example 3 - Clean pass**

NPC dialogue references the Ark, the Council, and the Swarm, all confirmed
canon with no OPEN items touched:

```
Lore check passed.
```

**Example 4 - Design exploration lore implication (step 0 trigger)**

Session is a mechanic design exploration. Claude proposes: "the Loops could
serve as the agricultural base for the Ark population." No in-world text is
being written. Lore checker fires at step 0:

Step 0 fires: this claim asserts something about how the world works.
Source not loaded this session — cannot confirm against lore bible.

Output includes:

```
[INFERENCE: the Loops function as agricultural infrastructure for the Ark —
confirm against lore bible before treating as design constraint]
```

The design exploration continues with the claim labeled. It does not propagate
as established fact.

**Example 5 - Design exploration claim verified against loaded source**

Session is a mechanic design exploration. Lore bible is loaded this session.
Claude step 0 fires on "the Loops could serve as the agricultural base for
the Ark population." Source is loaded — the claim is confirmed in the lore
bible. Output:

```
Lore check passed.
```

Design exploration continues without labels. The claim is treated as confirmed
for this session.

---

## Out of Scope

This skill does NOT:

- Answer design questions or make lore decisions - only check against confirmed canon
- Log decisions (use `loop-core-decisions`)
- Track document versions or skill registry changes (use `loop-core-tracker`)
- Apply balance math, player psychology, or idle mechanics (use dedicated skills)
- Generate code (use `loop-extended-code-guardian`)
- Invent answers to OPEN items under any circumstances - flag and defer always

---

## ADVERSARIAL SELF-REVIEW

Run this section after every lore check output, before delivering content. Block
delivery until the confirmation block is produced.

---

### Challenge 1 — Canon sourcing

**Failure mode:** Lore check passes content that cites no loaded source — relying
on Claude's training-knowledge impression of the canon rather than a verified
document or registry entry.

**FAIL example:**

```
"The Heart is confirmed as anti-Cult — check passes."
(No source cited. Could be correct, could be stale from training.)
```

**FIX:** Every assertion in the lore check output must trace to one of: (a) a
row in the Canon Quick Reference above, (b) a registry entry from
loop-extended-canon fetched this session, or (c) a direct quote/section
from the lore bible or GDD fetched this session. If the source is none of these,
treat the fact as UNVERIFIED and flag it — do not pass silently.

**Severity:** HIGH — unsourced passes can ship lore errors as confirmed canon.

---

### Challenge 2 — OPEN discipline

**Failure mode:** The lore check implicitly answers an OPEN item by choosing one
interpretation and proceeding, rather than flagging and deferring.

**FAIL example:**

```
Content describes the Familiar calling the player "Custodian."
The lore check passes because "Custodian" is a known term.
(But the Familiar's specific form of address at game start is OPEN — this
invents a precise answer without flagging it.)
```

**FIX:** Before passing any content that relies on a detail not explicitly LOCKED
in the decisions log, check whether that detail is OPEN. Subtle cases: tone,
specific phrasing, relationship depth at a particular game moment, and any
specific NPC behavior not documented as confirmed. When in doubt: flag as
`[OPEN: confirm before shipping]` rather than passing silently.

**Severity:** CRITICAL — silent OPEN-item answers propagate into shipped content.

---

### Challenge 3 — Temporal consistency

**Failure mode:** The lore check verifies that a fact is canon, but does not
verify that the fact is canon *at the narrative moment the content depicts*.

**FAIL example:**

```
Content shows the Familiar freely sharing information about previous custodians
early in the game. The lore check confirms custodian history is canon — passes.
(But the Familiar is confirmed as constrained in discussing previous custodians.
The fact exists; the access condition is wrong for early game.)
```

**FIX:** After confirming a fact is canon, verify its temporal/conditional access
rules: Is this fact available to the player at this point in the game? Is this
behavior consistent with the Familiar's trust arc at this narrative moment?
Is this NPC interaction appropriate to the player's faction standing at this stage?
A fact being true does not mean it's accessible at all game points.

**Severity:** HIGH — temporally misplaced canon creates continuity errors that are
hard to detect until late in development.

---

### Confirmation block (required before delivering any lore check output)

```
Lore check self-review:
  Challenge 1 — Canon sourcing: [source cited for each assertion, or "unverified — flagged"]
  Challenge 2 — OPEN discipline: [all OPEN items flagged, or "no OPEN items touched"]
  Challenge 3 — Temporal consistency: [temporal anchors verified, or "flagged — [detail]"]
  Status: CLEAR to deliver / BLOCKED — [reason]
```

If any challenge result is BLOCKED: revise the lore check output to address the
issue before delivering. Never deliver a lore check result with an open block.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-canon | Atomic canonical statement registry — query before asserting any lore fact |
| loop-core-decisions | Logs confirmed decisions; source of truth for OPEN/LOCKED status |
| loop-core-tracker | Document register; locates current lore bible version |
| utility-extended-doc-formatting | Document structure and format standards for lore documents |
| utility-game-psychology | Emotional design and NPC relationship arcs |
