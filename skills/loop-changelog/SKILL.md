---
name: loop-changelog
description: >
  Generates player-facing release notes and store changelog entries for The
  Loop in the correct voice register, within platform character limits, from
  git history or a list of completed tasks. Use automatically — do not wait
  to be asked. Trigger on ANY of these signals: user says "release notes",
  "changelog", "what's new", "app store update", "store copy for this build",
  "what changed since last release"; a build phase is completing and store
  submission is upcoming; user provides a list of completed tasks and asks for
  player-facing copy. Do NOT trigger for: internal technical documentation,
  decisions log entries, or build tracker updates — those are not player-facing.
  Load once per session.
---
SKILL_VERSION: v1.0

# The Loop — Changelog Skill

Generates player-facing release notes and store changelog entries. Operates
at the intersection of The Loop's voice system and app store requirements.

---

## PART 1 — WHAT THIS SKILL PRODUCES

Two outputs per release, always both:

**1. Google Play "What's New"** — 500 Unicode characters max (binding constraint).
Written first. Everything else is a longer version of this.

**2. iOS App Store "What's New"** — 4,000 characters max.
Expanded version of the Google Play copy. Same opening, more detail where
the content warrants it.

Also optionally: an **internal changelog entry** for the decisions log and
build tracker — technical summary for your own records, not player-facing.

---

## PART 2 — PLATFORM RULES

### Character limits (hard)

| Platform | Field | Limit | Notes |
|---|---|---|---|
| Google Play | What's New | 500 Unicode chars | Per language. Binding constraint — write to this first |
| iOS App Store | What's New | 4,000 chars | Same field as description; write expanded version |
| iOS App Store | Promotional Text | 170 chars | Optional, appears without expanding — first impression |

Always count characters before delivering. Google Play's 500-char limit is
unforgiving. 501 characters will be rejected.

### Who reads this and why

**Existing players** see What's New before screenshots — it's prime real estate
for re-engagement: "should I update?" not "should I install?".

**New users** see it below the description. Less prominent. Acquiring new
players is not what this section is for.

Write for the player who already loves the game and wants to know what's
changed. Never write for acquisition.

### What store platforms reject

Both App Store and Google Play will flag or reject:
- Performance metrics: "Most downloaded", "#1 game", "Best of 2026"
- Award claims: "Winner of..."
- Pricing information: "Free this week", "50% off"
- CTAs: "Rate us!", "Leave a review!", "Share with friends!"
- Promotional language: "Biggest update ever", "You won't believe this update"
- Spam repetition: copying previous release notes verbatim

---

## PART 3 — THE LOOP VOICE IN RELEASE NOTES

Release notes are player-facing public content. The Loop's Official Account
register applies. The True Account layer must never surface here.

### Voice register: Official Account

Warm, sincere, world-consistent. Reads as a living game communicating with
its players — not a developer publishing patch notes.

**Appropriate voice patterns:**
- Describing gameplay changes in terms of their effect on the player's experience
- Referencing The Loop's world lightly (the Ark, the cycle, the Dreaming)
- Warmth without being saccharine
- Brevity that feels considered, not dismissive

**Wrong patterns:**
- Technical jargon: "fixed null reference exception", "optimised render pipeline"
- Developer-facing language: "refactored mana store", "migrated to FlashList v2"
- Generic non-content: "bug fixes and performance improvements" with no specifics
- Revealing True Account content: nothing about the investigation arc, the shadow
  factions, or the Collapse backstory belongs in release notes
- Invented lore: no new character names, locations, or events unless confirmed canon

### Tone calibration by update size

| Update type | Tone | Example opening |
|---|---|---|
| Major content release | Warm narrative, hint of significance | "The Dreaming shifts. Something new stirs beneath the surface of the Ark." |
| Feature addition | Grounded, specific, world-adjacent | "The Ritual now remembers your elemental affinities between cycles." |
| Balance / feel pass | Honest, light | "The mana flow feels smoother now. A few rough edges, sanded down." |
| Bug fixes only | Brief, warm, no overselling | "Some small corrections to how the Loop behaves. Nothing dramatic." |
| First launch | Welcoming, sets the world's register | "The Loop opens. The Ark stirs. The Familiar is waiting." |

Never write "Bug fixes and performance improvements" alone. If only bugs were
fixed, say what category of experience improved and in one sentence why it matters.

---

## PART 4 — GENERATION PROCESS

### Step 1 — Gather inputs

Ask for or derive from context:
- List of changes in this build (tasks from write-plan, git log, or user list)
- Build phase and version number
- Any significant lore-adjacent features (verify against lore-checker before using)

### Step 2 — Categorise changes

Group by player-visible impact, not technical category:

| Player-visible impact | Example |
|---|---|
| New content | New location, new elemental form, new quest |
| Changed gameplay feel | Balance adjustments, flow improvements |
| Fixed frustrations | Crashes, misbehaving UI, incorrect calculations |
| Performance | Load times, animation smoothness |
| Accessibility | New settings, font scaling, reduced motion |

Drop anything invisible to players: refactors, dependency updates, test
improvements, internal tooling. These have zero value in release notes.

### Step 3 — Write Google Play version first (≤500 chars)

Lead with the most significant change. End with either a general warmth
note or let the most important change carry the whole entry.

Run character count before presenting. Fix if over.

### Step 4 — Expand to iOS version

Same opening. Add detail for secondary changes. iOS players have more to
read if they want it. Google Play players get the essentials.

### Step 5 — Lore check

If any in-world terminology appears (location names, NPC roles, faction
names, mechanic names), verify against the Loop canon before including.
Never introduce new lore in release notes — use confirmed terms only.

### Step 6 — Present both outputs with counts

```
GOOGLE PLAY — What's New ([N]/500 chars)
─────────────────────────────────────────
[copy]

iOS — What's New ([N]/4,000 chars)
────────────────────────────────────
[copy]

Promotional Text (optional, [N]/170 chars)
───────────────────────────────────────────
[copy — only if requested]
```

---

## Examples

### Example: Small update (bug fixes + one feel improvement)

**Input:** Fixed cycle counter display jumping on fast mana income; fixed
Rift transition hanging on old devices; improved mana bar animation smoothness.

**Google Play (87/500 chars):**
```
The mana bar breathes a little easier now. Fixed a counter glitch and a
stuck transition on the way to the Rift.
```

**iOS (same opening, slightly expanded):**
```
The mana bar breathes a little easier now. Fixed a counter glitch and a
stuck transition on the way to the Rift. A few older devices were having
trouble with that crossing — they shouldn't anymore.
```

---

### Example: Feature release (Cards of Fate variant added)

**Input:** Added elemental-affinity Cards of Fate draws; mana income scales
with elemental alignment; new visual effect on aligned draws.

**Google Play (198/500 chars):**
```
The cards know what you've built. Aligned draws now carry the weight of
your elemental choices — and the Dreaming responds. Look for the light
when your affinities align.
```

**iOS:**
```
The cards know what you've built. Aligned draws now carry the weight of
your elemental choices — and the Dreaming responds. When your elemental
affinity matches a drawn card, the mana flows differently. Watch for the
light. It means something.
```

---

### Example: First launch

**Google Play (98/500 chars):**
```
The Loop opens. The Ark stirs. Something in the Dreaming has been waiting
a long time. Welcome back.
```

---

## PART 6 — ANTI-PATTERNS

| Anti-pattern | Why | Instead |
|---|---|---|
| "Bug fixes and performance improvements" | Generic, says nothing | Name the category of experience that improved |
| Technical jargon | Players don't care about implementation | Describe the effect, not the cause |
| Copying previous notes | Signals a dead game | Write something new, even if small |
| True Account content | Release notes are Official Account layer only | Keep investigation arc and shadow factions out |
| Invented lore terms | Could contradict canon | Use confirmed terms only; check lore-checker |
| Promotional language | Store rejection risk | Warm and world-consistent, not salesy |
| "Best update ever" / superlatives | Store rejection risk, also embarrassing later | Let the content speak |
| CTAs ("Rate us!") | Store rejection risk | Never |

---

## Out of Scope

This skill does NOT:
- Write App Store descriptions or metadata (a separate task, not part of release notes)
- Update the decisions log or build tracker (use dedicated skills)
- Check canon consistency autonomously (defers to loop-extended-lore-checker for
  any in-world terminology)
- Generate social media posts about the release

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-lore-checker | Verify any in-world terminology before including in release notes |
| utility-extended-narrative-designer | Official Account register definition and tone standards |
| loop-build-tracker | Source of completed tasks for a given build |
| Google Play Console — Release notes | Official 500-char limit, formatting rules |
| App Store Connect — What's New | Official 4,000-char limit |
