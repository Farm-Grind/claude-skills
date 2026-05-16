---
name: loop-dialogue-writer
description: >
  Writes player-facing text for The Loop at implementation level: NPC dialogue,
  Familiar lines, quest text, notification copy, and UI labels with lore weight.
  Enforces canon voice rules — second person for player-facing content, third
  person for lore/GDD, gender-neutral language, no hero name, earned-trust
  Familiar arc. Flags OPEN items rather than inventing. Use automatically —
  do not wait to be asked.
  Trigger on ANY of these signals: dialogue lines are being written; NPC or
  Familiar text is needed; quest text, notification copy, or tutorial text is
  requested; "write this line", "what would X say", "draft dialogue",
  "notification copy", "quest description"; MAN-19 or MAN-21 work is active.
  Do NOT trigger for: NPC identity design (loop-npc-designer); lore canon
  checks (loop-extended-lore-checker); sound design briefs (suno-prompter).
  Load once per session.
---
SKILL_VERSION: v1.2

# The Loop — Dialogue Writer

Produces implementation-level written copy for all player-facing text in
The Loop. All output is canon-compliant and ready for the GDD, Airtable, or
direct implementation.

---

## PART 1 — CANON VOICE RULES (apply to every output)

**Person rules:**
- Dialogue (NPC lines, Familiar lines, notifications, tutorial): second person
  ("You haven't checked the Rift today." / "Your elemental is ready.")
- Lore, GDD, and internal docs: third person ("The custodian returns to find...")
- Never use the hero's name — no in-game name input exists.
- Never use gendered pronouns for the player.

**Familiar voice rules:**
- True name is unpronounceable by mortals — never write it.
- Player assigns a nickname. When writing generic Familiar lines, use "I" from
  Familiar's perspective and "you" for the player.
- Default register: quietly polite, slightly standoffish.
- Trust arc is earned, not given. Early lines are helpful but emotionally flat.
  Mid-arc lines show curiosity. Late-arc lines show genuine warmth.
- The Familiar does not know about the Eye, Voice, Hand, or Master.

**NPC register:**
- Each NPC has a locked register (formal / informal / clinical / guarded / warm
  / etc.) defined in their NPC profile.
- Never write an NPC warmer than their current depth meter stage permits.
- Quest text uses the NPC's register, not a generic authorial voice.
- **Profile check (mandatory before writing any NPC line):** If the NPC's profile
  (register, depth stage, elemental affinity, faction) is not already present in
  this session's context, invoke `loop-npc-designer` to load or generate it first.
  **HARD FAIL:** MUST NOT write any NPC line without a confirmed register and depth stage.
  Never invent a register or depth stage — always derive from the profile.

**General copy rules:**
- No exclamation points in NPC lines unless the register explicitly calls for it.
- No "Greetings, Custodian" or similar fantasy-game clichés.
- Keep notification copy under 80 characters. Subject line + single action.
- Achievement names: terse, evocative, lore-grounded.
- UI labels: prefer one noun or verb phrase over a full sentence.

---

## PART 2 — TEXT TYPE TEMPLATES

### NPC dialogue line (at depth stage)

```
NPC: [Name]  |  Depth Stage: [1 / 2 / 3]  |  Register: [register]
Context: [when does this line trigger]
---
LINE: "[dialogue text]"
ALT 1: "[variant — same meaning, different phrasing]"
ALT 2: "[variant — optional emotional variant]"
Notes: [any implementation notes — e.g. "plays only once", "loops", "gated"]
```

### Familiar line

```
Familiar line
Context: [trigger state — idle / first ritual / relationship milestone / etc.]
Trust arc stage: [early / mid / late]
---
LINE: "[line text]"
ALT: "[variant]"
```

### Quest text

```
Quest: [quest name or ID]
NPC issuer: [name]  |  Register: [register]
---
DESCRIPTION: [2–4 sentences max. Present tense. Second person if addressing
player, third person if describing world events.]
OBJECTIVE: [plain one-line task statement — no register, purely functional]
COMPLETION: [1–2 sentences. NPC voice. Acknowledges player success in register.]
```

### Push notification

```
Trigger: [what game state fires this]
---
HEADLINE: [under 40 chars — the hook]
BODY: [under 80 chars — the action]
```

### Achievement name + description

```
Achievement: [ID or category]
---
NAME: [terse, evocative — 2–4 words]
DESCRIPTION: [one sentence. Third person. Lore-grounded.]
```

---

## PART 3 — WRITING STYLE LIBRARY INTEGRATION

MAN-74 defines five voice categories. Until that ticket is complete, use these
placeholder registers drawn from confirmed canon context:

| Category | Register | Notes |
|---|---|---|
| Official Account | Formal, institutional, slightly propagandistic | Used for Ark announcements, official Division comms |
| True Account | Direct, understated, occasionally bleak | Used for lore text, Familiar late-arc, Heart comms |
| Trade and Commerce | Transactional, efficient, no warmth | Logistics, Supply requests, Exchange prompts |
| Underground | Oblique, coded, trust-gated | Syndicate, Cult, Heart operatives |
| Custodian-facing tutorial | Plain, orientation-focused | Onboarding, Familiar early-arc, UI guidance |

When MAN-74 is complete, replace this table with the five locked categories.

---

## PART 4 — OPEN ITEM HANDLING

Never invent answers for OPEN canon items. Specifically:
- If an NPC's name is OPEN (D-027, D-028), write the line with `[NPC NAME]`
  placeholder.
- If a location name is OPEN, use the area descriptor: "the storage level",
  not an invented name.
- If a faction mechanic is OPEN, write the line to be agnostic.

Flag OPEN items at the bottom of any output:
```
⚠ OPEN ITEMS blocking this copy:
- [D-XXX]: [what it controls in this text]
```

---

## PART 5 — PRE-DELIVERY GATE (run before delivering any copy)

Run these checks before presenting output. Fix failures before delivering.
Never deliver copy with an open failure.

| Check | Fail condition |
|---|---|
| Person rule | Wrong person for content type — NPC line uses third person, lore uses second |
| Hero name | Any proper name used for the player character |
| Gendered player pronouns | He/she/his/her used for the player |
| NPC register match | Line is warmer or colder than the NPC's profile register |
| Familiar trust arc | Line warmth doesn't match stated trust arc stage |
| Invented OPEN answers | Any field filled where the source decision is OPEN |
| Notification length | HEADLINE over 40 chars or BODY over 80 chars |
| Cliché register | "Greetings, Custodian", "Well met", or similar fantasy-game phrases |
| Achievement naming | Generic names ("First Blood", "Legendary") with no lore grounding |

---

## Out of Scope

This skill does NOT:
- Design NPC identity, faction, or elemental affinity (use loop-npc-designer)
- Verify lore canon accuracy of world facts referenced in copy (use loop-extended-lore-checker)
- Write Suno music prompts or sound design briefs (use suno-prompter)
- Generate story arc structure or transmedia content planning (use utility-extended-narrative-designer)
- Write lore bible entries or GDD documentation (third-person authorial content belongs in docs, not copy)

---

## Examples

**Example 1 — NPC dialogue at depth stage 1 (formal register)**

User: "Write a depth-stage-1 exchange line for a Peacekeepers officer who asks the player to run a supply check."

Skill fires. Part 1 voice rules loaded. Profile check: formal register, Stage 1 (Contact). Output:

```
NPC: [Officer Name TBD — D-027 OPEN]  |  Depth Stage: 1  |  Register: Formal
Context: Triggered when player interacts with Peacekeepers officer at The Exchange
---
LINE: "The supply manifest shows a discrepancy on level four. Confirm the count when you're next in that section."
ALT 1: "There's an inventory flag on the lower levels. If you pass through, verify the numbers against the posted list."
ALT 2: "I'd handle it myself, but the area's flagged. You'll need to check it."
Notes: One-time trigger per cycle. Delivers after first Exchange unlock.
```

⚠ OPEN ITEMS blocking this copy:
- D-027: Officer name not confirmed — [Officer Name TBD] placeholder used

**Example 2 — Familiar line, early trust arc**

User: "Write a Familiar idle line for early arc — player has just completed their first ritual."

Skill fires. Trust arc stage: early. Register: quietly polite, emotionally flat.

```
Familiar line
Context: Idle — first ritual complete
Trust arc stage: Early
---
LINE: "The resonance held. That's enough for now."
ALT: "You completed the pattern. I'll note it."
```

**Example 3 — Push notification**

User: "Write a notification for when the player's elemental is ready to harvest."

```
Trigger: Elemental harvest ready
---
HEADLINE: Your elemental is ready.
BODY: Return to the Source and collect before the cycle resets.
```

PRE-DELIVERY GATE check:
- Person rule: ✓ second person
- Hero name: ✓ none
- Notification length: HEADLINE 28 chars ✓, BODY 59 chars ✓

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-npc-designer | NPC identity, affinity, and depth meter structure |
| loop-extended-lore-checker | Canon accuracy for world facts referenced in copy |
| utility-extended-narrative-designer | Story arc structure and transmedia content |
