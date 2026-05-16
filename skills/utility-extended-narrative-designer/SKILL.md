---
name: utility-extended-narrative-designer
description: >
  Applies narrative design and transmedia standards to game content — lore,
  quest text, NPC dialogue, seasonal comics, and social media story sets.
  Knows world bible structure for content generation, canon tiers, two-layer
  narrative design, and mobile format briefs. Use automatically — do not wait
  to be asked. Trigger on ANY of these signals: lore content is being written
  or evaluated; quest text or NPC dialogue is being drafted; a story beat is
  being assessed; a comic, post set, or seasonal narrative is being planned;
  a two-layer narrative structure is being applied; user asks "will this work
  narratively", "does this fit the world", "how should I structure this story",
  "what content can we make from this lore"; the words "canon", "lore",
  "quest", "dialogue", "seasonal", "comic", "social", or "transmedia" appear
  in a narrative context. Do NOT trigger for: GDD audits
  (utility-game-gdd-enforcer), canon fact-checking, or code generation.
  Load once per session.
---
SKILL_VERSION: v2.1

# Narrative Designer Skill

Applies professional narrative design and transmedia storytelling standards
to game content. Covers story craft, world bible structure, canon management,
mobile-first lore delivery, and content generation across platforms.

Where The Loop is referenced, it serves as the primary worked example.
Apply equivalent structures from your project's lore documentation.

---

## PART 1 — THE WORLD BIBLE AS GENERATIVE ENGINE

A world bible's current function is often canon record: it documents what
exists. Its missing function is content generation engine: it should define
what's possible. The gap between these two is why lore can feel "not
buildable off of."

A generative world bible has four layers:

### Layer 1 — Canon Foundation
Established facts: cosmology, factions, characters, history, rules of the
world. Answers: "what is confirmed true?"

**Loop status:** EXISTS — Lore Bible v2.6+ covers this layer.

### Layer 2 — Story Seed Bank
Unexplored events, locations, and character moments that are established in
the world but not yet told. Each seed is a defined but unwritten moment:
- Historical events referenced but not dramatized
- Character backstories with known endpoints but unwritten middles
- World-state gaps (locations established but never shown from inside)
- Open-ended questions planted in the surface layer for players to discover

**Loop examples:** The original Loop creation event; the first Cultist
attack on an Ark supply line; Ryszard's first encounter with a custodian;
how the previous custodian's corruption began; what Deep Storage looks like
from inside.

Without this list, content generation requires re-reading the entire Lore
Bible each time. Build it once, maintain it as a living document.

**Loop status:** MISSING — build this.

### Layer 3 — Tone Reference Library
Worked examples of the world's voice at each register. Without worked
examples, new content defaults to the writer's natural voice rather than
the world's.

**Loop registers:** Official Account (warm, sincere, NPCs believe every
word), True Account (precise, clinical, no editorializing), Flavor Riff
(personality-forward, world-consistent).

**Loop status:** MISSING — build this. See
`references/tone-reference-library-build-spec.md`. Structure each register
around absences (what it never does) as well as patterns.

### Layer 4 — Designing Principle
Truby's concept: the abstract internal logic that makes all parts of the
story hang together organically. Distinct from premise (what concretely
happens). The designing principle is the organizing question the whole world
is answering.

**Loop designing principle (approximate):** *The same cycle, infinitely
repeated, slowly reveals what was always true.* Every piece of canonical
content should be checkable against this. If a story beat doesn't fit the
designing principle, it is off-brand even if canon-accurate.

**For other projects:** Define your designing principle before generating
content at volume. Test every piece of content against it.

**Loop status:** MISSING — define formally in the Lore Bible.

---

## PART 2 — CANON TIER SYSTEM

Every piece of content must be assigned a canon tier before production.
The tier determines how carefully it must be checked against the world
bible, whether it can contradict established facts, and where it can be
distributed.

| Tier | Name | Rules | Distribution |
|---|---|---|---|
| T1 | Core Canon | Establishes or expands established lore. Must be checked against world bible before production. Cannot contradict T1 content. Always free/accessible. | In-game (quests, codex, dialogue), official website, free comics |
| T2 | Canonical Expansion | Tells an established but unwritten story. Must not contradict T1. Expands the world without changing it. | Seasonal comics, patch-launch stories, free social content |
| T3 | Flavor Riff | Tonally consistent with the world but not narratively critical. Can reference canon loosely but doesn't advance it. | Instagram, TikTok, platform-native content |
| T4 | Non-Canon | Explicitly outside the main timeline. Alternate scenarios, "what if" content. Labeled as such. | Special events only |

**The Fortnite failure mode to avoid:** Never gate T1 or T2 content behind
paid or hard-to-access distribution. Critical lore in inaccessible comics
punishes players who miss it when that lore affects the game.

**The Overwatch failure mode to avoid:** Telling backstories safely in the
past rather than advancing the present-day timeline. Players need to answer
"what is happening right now in this world?" If seasonal content never moves
the present-day needle, lore enthusiasm atrophies.

---

## PART 3 — THE TWO-LAYER MAINTENANCE CHECK

Projects using a dual-narrative structure (e.g., an "official" version of
events vs. the truth beneath it) must check every piece of content against
both layers before production. This is not optional for T1 and T2 content.

**Loop application — The Loop uses a dual account structure:**

| Layer | Player access | Writing standard | Failure mode |
|---|---|---|---|
| Official Account | Default — all players from game start | Warm, sincere, emotionally true. NPCs genuinely believe it. No winking, no hollow delivery. | Writing it as obviously false breaks the layer. NPC should sound like they mean it. |
| True Account | Gated — investigation arc, endgame | Precise, without editorial judgment. Does not call the Official Account "a lie." Presents facts. | Editorializing ("the sinister truth") breaks the tonal standard. |
| Breadcrumb | Both layers simultaneously | Officially explainable. Only introduced deliberately. Always label which shadow layer it hints at. | Accidental breadcrumbs — references that break the Official Account without intent — are lore errors. |

**The perceptibility gradient:** The darkness should not be perceptible
without digging. Surface play = bright colors, fun, minimum cognitive
dissonance. A casual player should be able to play 100 cycles and never
feel the dark foundation.

**Test any piece of content against:** If a casual player encounters this
and nothing else, does it feel tonally consistent with a cozy farming game?
If no, the dark layer is too visible at this depth.

**For other projects:** Adapt this table to your project's equivalent
layers. The key principle is identical — maintain a perceptibility gradient
that protects casual players from content they didn't opt into.

---

## PART 4 — STORY CRAFT STANDARDS

### Narrative beats must earn their emotional weight

A story beat that moves plot without producing emotion is a wasted beat.
Before writing any scene or quest, answer: what should the player feel at
the end of this?

Sylvester's framework applied to beat types:

| Beat type | Target emotion | Common failure |
|---|---|---|
| Tutorial / introduction | Curious, capable, not lost | Information delivery at the cost of feeling |
| Quest inciting event | Motivated, stakes understood | Abstract stakes instead of personal ones |
| NPC personal moment | Connected, like someone real is there | Exposition in character clothing |
| Investigation arc reveal | Unsettled, re-evaluating what they knew | Delivering truth too cleanly — the unsettling feeling requires the player to piece it together |
| Seasonal one-shot | Whatever the beat calls for — fully committed | Hedging tone to avoid committing to dark or light |

### NPC dialogue has four functions — know which one each line serves

From King/Candy Crush narrative research:

1. **Mechanic explanation** — Why is the player doing this?
2. **World context** — This action has meaning in the world beyond mechanics.
3. **Character personality** — One strong choice per scene over several weak ones.
4. **Quest framing** — What does the player need to do and why do they care?

Most weak dialogue tries to do all four at once. Assign each line a primary
function and edit against it.

### Character motivation must be comprehensible, not sympathetic

Every character's actions must have a comprehensible human reason. The
reason does not need to be sympathetic — it needs to be understandable.

Before writing any NPC or antagonist action: what does this character want,
and why is that want comprehensible given their position and history? If the
answer requires the reader to accept they are simply evil or simply good,
rewrite.

**Loop application:** Per the Lore Bible's No Explicit Good or Evil
directive — every faction (Peacekeepers, Cult, Heart, Syndicate) must
have a comprehensible answer to the world's central moral problem.

### The character web — every NPC expresses a facet of the same moral problem
(Truby, Anatomy of Story)

Every significant NPC should represent a different response to the world's
central moral problem. When designing a new NPC, identify which answer they
embody before writing their dialogue.

**Loop application:** The Loop's moral problem is approximately: *what do
you do when the system protecting you is also exploiting you?* The
Peacekeepers, Cult, Heart, and Syndicate each answer this differently.

The opponent rule: every antagonist must have a moral argument that is
comprehensible and, in context, defensible. No argument = no dramatic tension.

### Save the Cat applications
(Blake Snyder — three concepts applicable to episodic/cyclical game
structures)

**Earn investment before asking for it.** Before any NPC asks the player to
care about them, give the player one small, concrete action that makes that
character worth caring about. Not backstory — one observable moment. Apply
to NPC introductions, companion opening behavior, and the first thing any
new faction contact does.

**Loop application:** The Familiar's opening behavior and the first action
of any new Ark NPC must earn investment before the player is asked to care.

**The All Is Lost / Dark Night rhythm.** The deepest emotional lows produce
the most durable highs. Investigation arc reveals and seasonal climax moments
need a genuine low before any resolution lands. Apply to T1/T2 content with
climax beats, not to surface-layer cozy content.

**Deliver on your promise before introducing darkness.** Whatever the opening
of a piece promises, the middle must deliver. Any content that breaks the
cozy promise before the player has opted into the investigation arc is a
layer violation — the cozy contract must be honored before the darkness is
earned.

---

## PART 5 — MOBILE-FIRST LORE DELIVERY STANDARDS

### The 4 C's for mobile narrative (King/Candy Crush, adapted)

1. **Context** — Why is this happening? Every lore moment must anchor to
   something the player is doing or has done. Decontextualized lore floats.
2. **Clarity** — Scannable even if skipped. If a player skips the dialogue
   box, do the visuals and NPC expression still communicate the emotional
   gist?
3. **Consistency** — Same terms, same names, same voice everywhere.
   **Loop application:** The Familiar always says "cycle" not "loop."
   Ryszard is never named until the investigation arc earns it. Faction
   names are consistent across quest text, UI labels, and NPC dialogue.
4. **Charm** — Personality at every touchpoint. Even a loading screen tip
   can have character. The Loop's tone is dark and specific — bland neutral
   copy is a miss.

### In-game lore delivery mechanisms

| Mechanism | Loop status | Notes |
|---|---|---|
| Companion/Familiar dialogue | Confirmed | Primary early-game lore surface. Cycle-return awareness means no catch-up exposition. |
| NPC quest text | Confirmed | Large lore flavor component. Apply 4 C's. |
| Codex / Wiki | Confirmed (structure TBD) | Opt-in lore depth. Players who want it find it; others aren't forced. |
| Item descriptions | Confirmed (catalog TBD) | High-value low-cost lore surface. One strong detail per item. |
| Loading screen lore | Recommended — TBD | Low implementation cost. |
| Environmental storytelling | Recommended | Loop's disrepair tells the story before any dialogue fires. |
| The Exchange NPC messages | Confirmed | Every Ark NPC message is a lore touchpoint. Voice consistency critical. |
| Seasonal in-game events | Confirmed | Present-day timeline advances here. Must actually move something. |

---

## PART 6 — TRANSMEDIA CONTENT FRAMEWORK

### Content type taxonomy

Two content modes. Know which mode you're in before writing a word.

**Mode A — Official launch / announcement content**
Consistent story told in platform-appropriate ways. A patch comic and an
Instagram carousel from the same launch share the same story events, but
the comic dramatizes them and the Instagram carousel teases them.
Requires: canon tier assignment, two-layer check, tone consistency brief.

**Mode B — Riff content**
Platform-native, unique to the platform. Not required to align with a
specific launch. Adds texture, flavor, and world presence.
Requires: tone register assignment, platform format brief.

### Platform format briefs

**Vertical scroll comic (Webtoon / Dashtoon / mobile-first)**
- Each panel is a mini-reveal. Readers see one panel at a time.
- Place emotional beats and reveals at their own panel.
- Use blank/pause panels deliberately to control pace.
- Canon tier T1 or T2. Minimum 8–12 panels for a satisfying read.
- Script format: panel number / visual description / dialogue / emotional beat.

**Instagram carousel post (lore tease / character moment)**
- 5–10 swipeable panels. First panel is the hook.
- Last panel is the CTA or reveal. Text minimal — legible at phone size.
- Canon tier T2 or T3.

**Instagram story set (7-part serialized format)**
- One beat per day. Each story self-contained AND part of a running arc.
- Day 1: establishes character or situation. Days 2–6: escalation or depth.
- Day 7: payoff or cliffhanger driving to the next set.
- Canon tier T3 (flavor) or T2 (canonical expansion timed to a launch).

**Official announcement post (single image / short caption)**
- Tone consistent with the surface account unless in investigation territory.
- Never breaks the perceptibility gradient for casual players.
- Caption voice matches the world — not generic marketing language.

### The ritual dimension — design for repeated audience behavior

Durable IPs create rituals — repeated behaviors audiences perform in
relation to the world. Seasonal returns, community theorizing, anniversary
events, recurring content formats. Rituals convert passive players into
invested participants. They must be designed, not assumed.

**Loop application:** The investigation arc needs deliberate mystery
touchpoints for community theorizing; seasonal content should create
anticipation patterns; the Familiar's evolving behavior is a ritual anchor;
T3 social content benefits from recurring formats players recognize.
The Overwatch Sombra ARG is the industry benchmark — designed mystery that
generated organic community engagement for months.

### The Overwatch/Fortnite reference model

| Overwatch did well | Avoid from Overwatch |
|---|---|
| Free comics accessible to all players | Lore stagnating in the past — move the present |
| Character-specific deep dives | Inconsistent update rhythm killing momentum |
| Emotional shorts establishing character in minutes | Keeping relationships static across years |

| Fortnite did well | Avoid from Fortnite |
|---|---|
| Live events that visibly change the world | Critical lore gated in paid comics |
| Seasonal narrative that actually advances | Inconsistent tonal swings season to season |
| Players feel the world is alive | Story weight varying arbitrarily |

---

## PART 7 — THE STORY SEED BANK PROTOCOL

When building new content, check the Story Seed Bank before inventing new
material. When the bank doesn't contain what's needed, add a new seed first.

### Seed format

```
SEED — [ID: SS-XXX]
Type: Historical event / Character moment / World texture / Investigation
Canon tier: T1 / T2 / T3
Summary: [One sentence — what is this about?]
World Bible reference: [Which Lore Bible section establishes this?]
What's unwritten: [What happened that we've never dramatized?]
Formats it could work in: [comic / quest / social / dialogue]
Status: AVAILABLE / IN PRODUCTION / COMPLETE
```

### Story Spine — rapid seed validation
(Kenn Adams / improv theater; used by Pixar as a story testing tool)

Every seed must be expressible as a Story Spine before it is
production-ready. The Story Spine forces causality — it catches seeds that
are premises without stories:

```
Once upon a time, [world state / character situation]...
Every day, [the normal pattern that is about to be disrupted]...
Until one day, [the disruption]...
Because of that, [consequence 1]...
Because of that, [consequence 2]...
Until finally, [resolution or new equilibrium]...
And ever since then, [what changed permanently].
```

A seed that cannot complete the Story Spine is a premise, not a story.
Either develop it further or mark it INCOMPLETE in the bank.

---

## PART 8 — CONTENT GENERATION AUDIT

**HARD FAIL:** MUST NOT begin production on T1/T2 content before completing all 6 steps. When evaluating any piece of narrative content, run in this order:

1. **Canon tier assignment** — What tier? Is the distribution plan appropriate?
2. **Two-layer check** — Which account layer does this operate in? Is the
   perceptibility gradient maintained?
3. **Emotional beat check** — What should the player/reader feel at the end?
4. **4 C's check** (mobile content only) — Context, Clarity, Consistency, Charm.
5. **Platform format check** (transmedia content) — Written for the correct
   format's constraints?
6. **Present-day timeline check** (T1/T2 only) — Does this advance the
   present-day narrative, or only deepen the past?

```
NARRATIVE AUDIT — [Content title]
Canon tier: T[1-4]
Layer: Official / True / Breadcrumb / Riff
Emotional target: [What the reader should feel]
4 C's: [Pass / Flag — specific issue]
Format fit: [Pass / Flag — specific issue]
Present-day advancement: [Yes / No / N/A]
Verdict: [Ready / Needs work — specific gaps]
```

---

## COMMON FAILURE PATTERNS

| Pattern | What it looks like | Correct behavior |
|---|---|---|
| Official Account written with a wink | NPC dialogue sounds hollow or ironic | Write NPCs who genuinely believe what they're saying |
| Dark layer too visible | Casual player encounters unsettling content at surface depth | Test against perceptibility gradient |
| Lore stagnating in the past | All content is backstory; present-day timeline never moves | Seasonal content must advance something in the present |
| Canon tier not assigned | Content produced without clarity on whether it "counts" | Assign tier before writing, not after |
| Missing tone reference | New content defaults to writer's voice not the world's | Build Tone Reference Library before generating content at volume |
| Story seeds not maintained | Each session requires full Lore Bible re-read | Build and maintain Story Seed Bank as a living document |
| Platform format ignored | Instagram carousel written like a comic page | Brief specifies platform first |
| Critical lore gated | T1/T2 lore in inaccessible distribution | T1/T2 always free and accessible |

---

## PART 9 — NARRATIVE STRUCTURE SELECTION GUIDE

Select the structure that fits the content's layer and purpose.

### Kishōtenketsu — surface-layer and flavor content
(East Asian four-act: Ki / Shō / Ten / Ketsu — no conflict required)

The twist is not conflict — it's a recontextualization that reframes what
came before. The cozy loop is established, something is revealed, the world
settles into a new equilibrium.

**Apply to:** T3 riffs, surface-layer one-shots, NPC vignettes, companion
day-to-day moments, item descriptions, loading screen lore. Any content
where the cozy promise must be honored before anything darker appears.
**Not for:** Investigation arc, True Account reveals, content requiring stakes.

### Dan Harmon Story Circle — episodic and seasonal canonical content
(8 steps: You / Need / Go / Search / Find / Take / Return / Change)

Key property: protagonist ends in the same world but changed. Maps directly
onto The Loop's seasonal structure — the Ark's surface is restored each
season, but something has shifted underneath.

The Take beat is non-negotiable: the protagonist pays something real for
what they gained. A story that skips the cost has abandoned the circle at
step 6.

**Apply to:** T1/T2 seasonal arcs, patch-launch comics, canonical character
vignettes, social media 7-part story sets (scale to 7 beats).
**Not for:** T3 riffs (too heavyweight for flavor content).

### Western three-act structure — investigation and conflict content
Conflict-driven, linear.
**Apply to:** Investigation arc, True Account reveals, endgame quest chains
with active opposition.

### Structure selection quick reference

| Content type | Structure |
|---|---|
| Surface-layer cozy / flavor riff | Kishōtenketsu |
| Companion vignette / NPC slice-of-life | Kishōtenketsu |
| Seasonal arc / patch-launch comic | Dan Harmon Story Circle |
| Canonical character deep dive | Story Circle or three-act (depends on stakes) |
| Investigation arc / True Account | Western three-act |
| Social media story set (7-part) | Story Circle (scaled to 7 beats) |

---

## Examples

**Example 1 — Narrative audit**
User asks "will this work narratively?" — Claude runs Part 8 NARRATIVE AUDIT, assigns canon tier, checks two-layer gradient, returns verdict with specific gaps named.

**Example 2 — Transmedia routing**
User asks "can we post about the investigation arc?" — Claude assigns T2 tier, checks perceptibility gradient, routes to Instagram story set (7-part, Story Circle scaled to 7 beats).

---

## Out of Scope
- Write NPC dialogue lines — use `loop-dialogue-writer`
- Fact-check lore canon — use `loop-extended-lore-checker`
- Audit GDD documentation standards — use `utility-game-gdd-enforcer`
---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-lore-checker | Canon fact-checking — catches invented lore, enforces OPEN items |
| utility-game-gdd-enforcer | Documentation completeness — mechanic specs, production-readiness |
| utility-game-psychology | Audience motivation, SDT, companion relationship arc design |
| utility-extended-doc-formatting | Document format standards for any narrative doc produced |
| Henry Jenkins, Convergence Culture (2006) | Foundational transmedia theory — world-building as content engine |
| Overwatch transmedia case study | Comics + shorts + in-game events as parallel lore delivery |
| King/Tracey Watson, GDC — "Storytelling in Small Spaces" (2021) | 4 C's framework for mobile narrative design |
| Tynan Sylvester, Designing Games (2013) | Emotion-first design — mechanics as tools for emotional experience |
| John Truby, The Anatomy of Story (2007) | Character web, moral argument, designing principle |
| Blake Snyder, Save the Cat! (2005) | Earn investment early; All Is Lost rhythm; deliver on your promise |
| Dan Harmon, Story Circle | Episodic structure for self-contained-but-connected content |
| Kishōtenketsu / Kenn Adams Story Spine | Non-conflict structure; rapid story seed validation |
