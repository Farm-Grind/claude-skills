---
name: loop-npc-designer
description: >
  Designs NPCs for The Loop at implementation level: identity, elemental
  affinity, faction placement, personality register, relationship depth meter,
  and gift profile. Output seeds the Notion NPC Name Reference DB and GDD
  roster entries. Enforces canon rules — faction structure, elemental
  sympathies, gender-neutral language, second-person player address — and
  flags OPEN decisions rather than inventing. Use automatically — do not
  wait to be asked.
  Trigger on ANY of these signals: an NPC is being designed or reviewed;
  NPC roster entry is being created or audited; "NPC identity", "NPC affinity",
  "faction placement", "NPC profile", "design an NPC", "build the NPC roster";
  MAN-70 or MAN-41 work is active.
  Do NOT trigger for: writing NPC dialogue (loop-dialogue-writer); lore
  canon checks (loop-extended-lore-checker); balance math. Load once per session.
---
SKILL_VERSION: v1.3

# The Loop — NPC Designer

Designs NPCs from scratch or audits existing NPC profiles against The Loop's
confirmed canon and data requirements. Output is implementation-ready.

---

## PART 1 — CANON CONSTRAINTS (non-negotiable)

**HARD FAIL:** MUST NOT generate any NPC profile field before reviewing all constraints in this section. Profile generation is blocked until all constraints are loaded and applied.

Apply before generating any NPC field.

**Factions and Divisions:**
Divisions (official Ark orgs): Logistics, R&D, Peacekeepers, Social Services,
Fleet, Council, Central Command.
Factions (independent groups): Syndicate, Cult, Heart.
Guild is removed from canon. Spirit Animal is removed from canon.
Syndicate is actively suppressed — never officially acknowledged.
The Heart uses codenames only (D-028 OPEN — do not assign real names).
Council leadership names OPEN (D-027).

**Elemental affinities:**
The five affinities are: Fire, Air, Water, Earth, Mana.
Elemental sympathetic pairs: Fire↔Air (both active), Water↔Earth (both
receptive). Mana is sympathetic to all four equally.
Every NPC has one personal elemental (individual character affinity).
Faction elementals per Division/Faction are NOT yet assigned — flag as
[OPEN: faction elemental assignments not confirmed per-Division] until locked.
Do not assign an affinity that contradicts a character's personality register.

**Language rules:**
Gender-neutral language throughout all NPC descriptions.
Player address is always second person ("you") in dialogue-facing fields.
GDD and lore entries use third person ("the player", "the custodian").

**Relationship system:**
NPCs use a Stardew-style individual depth meter. This is not a currency.
Spending renown never reduces the depth meter.
Familiar passive delivery unlocks at first relationship milestone (per MAN-70).

---

## PART 2 — NPC PROFILE STRUCTURE

Each NPC requires all fields below. Flag any field that cannot be filled
without resolving an OPEN decision — never invent.

```
NPC PROFILE — [Name or placeholder]

IDENTITY
  Canonical name:         [name or OPEN if D-027/028 applies]
  Role / title:           [role within their division or faction]
  Division / Faction:     [one of the 10 confirmed entities]
  Tier:                   [1 = accessible early / 2 = mid / 3 = late]
  First contact trigger:  [what makes this NPC available to the player]

AFFINITY
  Personal elemental:     [Fire / Air / Water / Earth / Mana]
  Faction elemental:      [OPEN: per-Division assignments not yet confirmed]
  Affinity rationale:     [1 sentence explaining the personal elemental fit]

PERSONALITY
  Register:               [formal / informal / clinical / guarded / warm / etc.]
  Core trait (primary):   [one defining trait — active or receptive spectrum]
  Core trait (secondary): [one supporting trait]
  Trust arc:              [how tone shifts as depth meter increases — 2 sentences]

GIFT PREFERENCES
  Loved:                  [1–2 item types or categories — TBD if catalog incomplete]
  Liked:                  [1–2 item types or categories]
  Disliked:               [1 item type or category]

RELATIONSHIP DEPTH METER
  Stage 1 label:          [acquaintance / stranger / contact / etc.]
  Stage 2 label:
  Stage 3 label:
  Milestone 1 unlock:     [what changes for the player at first milestone]
  Familiar delivery:      [UNLOCKS at milestone 1 — do not omit]

EXCHANGE BEHAVIOR
  Request type:           [what this NPC asks for in The Exchange]
  Reward type:            [what they offer in return — renown / item / info]
  Via Relay bonus:        [×1.5 confirmed — surface in UI before player commits]

LORE HOOK
  One sentence:           [lore-light description for GDD reference]
  Open items:             [list any OPEN decisions blocking this profile]
```

---

## PART 3 — BATCH DESIGN WORKFLOW

When designing multiple NPCs in one session (MAN-41, roster work):

**Step 1 — Faction distribution.**
Map the roster against the 10 Divisions/Factions. Confirm representation is
distributed — not all NPCs should cluster in Logistics/R&D.

**Step 2 — Elemental distribution.**
Check that all five affinities appear across the roster with rough balance.
Personal elementals should reflect personality — do not assign mechanically.

**Step 3 — Tier distribution.**
Tier 1 NPCs must be accessible to a new player. Tier 3 NPCs require quest
gating or faction pipeline progression. Flag any Tier 3 that accidentally
describes Tier 1 behavior.

**Step 4 — Trust arc variety.**
Not all NPCs should have the same warmth trajectory. Include at least one NPC
per tier whose trust arc involves earning through action, not just time.

**Step 5 — Notion NPC Name Reference check.**
The Notion NPC Name Reference (DS: 9953acca-3d2b-4c0b-8b54-c8d3b73dd3e2, MAN-41)
is a *fictional character inspiration* table — source material (games, novels, TV)
used to inform NPC naming and personality. It is not a roster of Loop NPCs. When
seeding it, map each inspiration character to: Character Name, Source, Source Type,
Archetype/Role, Elemental Affinity (as a personality signal, not a Loop assignment),
Faction Alignment (closest Loop analogue), Personality Keywords (3),
Tone Register. Do not enter Loop NPC profiles directly into this table.

---

## PART 4 — AFFINITY ASSIGNMENT GUIDE

Affinity should feel like a natural extension of personality, not a mechanical
label. Use the following as a guide, not a formula.

| Elemental | Personality signals |
|---|---|
| Fire | Driven, impulsive, confrontational, active leadership |
| Air | Intellectual, quick, restless, communicative, mercurial |
| Water | Empathetic, adaptive, intuitive, emotionally deep |
| Earth | Steady, patient, grounded, loyal, resistant to change |
| Mana | Balanced, liminal, hard to place, rare — use sparingly |

Faction elementals may not match personal elementals. A Peacekeeper (likely
Earth or Water faction affinity) may have a Fire personal affinity — this
creates interesting internal conflict.

---

## PART 5 — OPEN ITEM HANDLING

When a profile field cannot be completed because a decision is OPEN, use:
`[OPEN: D-XXX description]`

Never substitute a plausible invented value. The open item blocks the field.
Surface blocked fields prominently at the bottom of the profile under
"Open items".

---

## Out of Scope

This skill does NOT:
- Write actual NPC dialogue lines (use loop-dialogue-writer)
- Verify NPC details against confirmed lore canon (use loop-extended-lore-checker)
- Decide faction or elemental canon — flag OPEN and surface to loop-core-decisions
- Apply balance math to NPC mechanics or gift economy
- Design the relationship meter system itself — only applies the confirmed spec

---

## Examples

**Example 1 — Single NPC design request**

User: "Design a Tier 1 NPC from the Peacekeepers Division."

Skill fires. Part 1 canon constraints loaded first. Output:

```
NPC PROFILE — [Name TBD]

IDENTITY
  Canonical name:         [placeholder — no OPEN blocking name selection]
  Role / title:           Field Officer, Peacekeepers
  Division / Faction:     Peacekeepers
  Tier:                   1
  First contact trigger:  Available from Day 1 of Ark cycle

AFFINITY
  Personal elemental:     Earth
  Faction elemental:      [OPEN: per-Division assignments not yet confirmed]
  Affinity rationale:     Peacekeepers attract steady, rule-bound personalities — Earth's grounded loyalty fits.

PERSONALITY
  Register:               Formal / measured
  Core trait (primary):   Patient — receptive spectrum
  Core trait (secondary): Loyal
  Trust arc:              Starts stiffly professional; first milestone unlocks dry humor and candid assessments of Ark politics.

GIFT PREFERENCES
  Loved:                  [TBD — gift catalog incomplete]
  Liked:                  [TBD]
  Disliked:               [TBD]

RELATIONSHIP DEPTH METER
  Stage 1 label:          Contact
  Stage 2 label:          Trusted Contact
  Stage 3 label:          Ally
  Milestone 1 unlock:     Peacekeeper patrol schedules (gameplay hint) + Familiar delivery active

EXCHANGE BEHAVIOR
  Request type:           Supply runs (material-type requests)
  Reward type:            Renown + security clearance hints
  Via Relay bonus:        ×1.5 confirmed — surface in UI before player commits

LORE HOOK
  One sentence:           Seasoned Peacekeeper who knows which Ark rules are worth enforcing and which ones have quiet exceptions.
  Open items:             Gift catalog incomplete (awaiting D-catalog-lock); faction elemental unconfirmed.
```

**Example 2 — Batch roster audit (Part 3 workflow)**

User: "Audit the 8 NPCs in the existing roster for elemental and faction distribution."

Skill fires. Part 3 batch workflow:
- Step 1: Faction distribution checked — 3 NPCs in Logistics, 1 in R&D, 1 in Peacekeepers, 1 in Syndicate, 2 in Social Services. Flag: Fleet and Council unrepresented — roster gap noted.
- Step 2: Elemental distribution — Fire ×3, Air ×2, Water ×1, Earth ×2, Mana ×0. Flag: Mana absent — roster skews active-spectrum.
- Step 3: Tier distribution — 5 Tier 1, 2 Tier 2, 1 Tier 3. Acceptable.
- Step 4: Trust arc variety — 6 of 8 follow warmth-over-time arc. Flag: need at least 1 earn-through-action arc in Tier 1 cohort.
- Step 5: Notion NPC Name Reference check — confirm inspiration table is source material, not a Loop NPC roster.

Output: structured gap report with recommended additions.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-dialogue-writer | Writing actual dialogue lines for NPCs |
| loop-extended-lore-checker | Verifying NPC details against confirmed canon |
| loop-core-decisions | Logging NPC design decisions when confirmed |
