# Balance Reference — Mechanic Feel, Fun, and Flow

Loaded by designer-games dispatcher when BALANCE domain activates.

## Table of Contents

- [PART 1 — What Makes Something Fun (Koster / Sylvester)](#part-1)
- [PART 2 — Loops, Arcs, and Retention (Daniel Cook)](#part-2)
- [PART 3 — Numeric Balance (Schreiber)](#part-3)
- [PART 4 — Juice and Feedback (Jonasson & Purho)](#part-4)
- [PART 5 — Progression and Elder Game (Schreiber / Cook)](#part-5)
- [PART 6 — Metrics and Iteration (Schreiber)](#part-6)
- [Quick Reference: Balance Checklist](#quick-reference)
- [Examples](#examples)
- [Adversarial Self-Review](#adversarial-self-review)

---

## PART 1 — WHAT MAKES SOMETHING FUN (Koster / Sylvester)

### The Learning Loop is the Fun Loop

Koster's central thesis: **fun is the act of mastering a system.** Boredom
occurs when a system is fully understood. Frustration occurs when it is
incomprehensible. The designer's job is to keep the player in the middle:
always learning, never lost.

Applied generally:
- Each new system or content unit should introduce something the player
  hasn't fully mapped yet — a new interaction, branch, or yield mechanic
- Skill-based minigames should feel learnable, not random — players must
  feel clever when they improve, not lucky
- Upgrade trees that reveal their logic over time are more fun than ones
  that are transparent immediately — preserve some discovery

**Loop application:** Each new elemental introduces a system the player
hasn't fully mapped (new yield mechanic, evolution branch, new interaction).
The Ritual minigame's symbol pattern should feel learnable — players should
feel clever when they improve, not lucky.

**Boredom diagnosis:** If a player says "I know exactly what I'll do every
cycle," the system has been solved. Introduce variance, branching, or
a new mechanic to restore the learning gradient.

### Emotions Are the Product, Mechanics Are the Tool (Sylvester)

Sylvester: games are systems for generating *emotional experiences*. The
correct evaluation of any mechanic is not "is it balanced?" but "does it
produce the intended emotional state?"

Define your game's target emotional arc per phase or session structure, then
evaluate every mechanic against it. A mechanic that disrupts the arc is
misplaced regardless of whether it is numerically balanced.

**Loop application — target emotional arc per cycle:**
1. **Dreaming** → calm deliberation, strategic anticipation (Cards of Fate)
2. **Rift** → patient tending, light curiosity (elemental growth)
3. **Tower** → focused efficiency, satisfying completion (crafting/Workshop)
4. **Source activation** → earned release, loop closure

Any mechanic that disrupts this arc — frustration in the Dreaming, boredom
in the Tower, anxiety in the Rift — is misplaced regardless of numeric balance.

**Sylvester's emotion triggers:**
- Learning (a system reveals new behaviour — elemental evolution)
- Acquisition (accumulation, collection, crafting)
- Challenge (Ritual minigame, Crucible precision)
- Spectacle (Ascension FX, cycle-end Source animation)
- Beauty / environment (aesthetics are functional, not decoration)

### Fiction and Mechanics Must Form One System (Sylvester)

Fiction that sits on top of mechanics is decoration. Fiction that *is* the
mechanic creates resonance.

For any project, ask:
- [ ] Do narrative elements have mechanical expression, or are they only flavor?
- [ ] Does each phase *feel* like its narrative description?
- [ ] Do character personalities manifest in their mechanical behavior?
- [ ] Does the game's central premise produce a mechanical texture?

**Loop application checklist:**
- [ ] Does the Familiar's guardedness have a mechanical expression, or is
      it only narrative flavor?
- [ ] Does the Dreaming *feel* like planning/dreaming (calm, predictive)?
- [ ] Do elemental personalities manifest in their yield behavior, not just
      their sprite?
- [ ] Does the Loop's "trapped in repetition" concept produce a mechanical
      texture — cycles feeling slightly different each time?

---

## PART 2 — LOOPS, ARCS, AND RETENTION (Daniel Cook / Lost Garden)

### Loops vs. Arcs

Two fundamental structures:

**Loop:** Player model → Action → System → Feedback → updated model →
repeat. Delivers *wisdom* through repeated engagement. Value compounds.

**Arc:** A one-way information delivery. Read once, consumed. Delivers
*knowledge*. Arcs do not retain players — loops do.

**The critical insight:** Players who churn are usually stuck in arcs, not
loops. If a player says "I've seen everything this game has to offer," they
have consumed all arcs and found no loops worth repeating.

Applied generally:
- The core session loop must feel *different* each time through variance,
  progression, and player decisions. If it feels the same, it's an arc.
- Tutorial and intro content are arcs — deliver efficiently, then move
  players into loop engagement as fast as possible.
- **Content treadmill risk:** if new content is the primary retention driver,
  the game is arc-dependent. Build loops deep enough to sustain play first.

**Loop application:** The Waltz cycle (Dreaming → Rift → Tower) must function
as a loop, not an arc. It must feel *different* each time through Cards of
Fate variance, elemental progression, and crafting decisions. The intro
cinematic and Familiar's opening dialogue are arcs — deliver once, efficiently.

**Nested loops (Cook's fractal structure):**

| Level | The Loop example | Generic equivalent |
|---|---|---|
| Micro | tap → gesture → feedback (Ritual, Crucible) | single input → gesture → feedback |
| Mid | Summon → Mature → Transform → Ascend | session objective (character lifecycle) |
| Macro | Dreaming → Rift → Tower → Source | full session structure |
| Meta | cycle N → permanent upgrade → cycle N+1 | session N → upgrade → session N+1 |

Each loop level must provide its own satisfaction signal.

---

## PART 3 — NUMERIC BALANCE (Schreiber)

### Relationships: Choose the Curve Before the Numbers

| Relationship | Formula | Loop use case | Generic use case |
|---|---|---|---|
| Linear | +1 in = +N out | Simple mana → item output | Simple resource → output |
| Triangular | 1, 3, 6, 10, 15… | Upgrade cost default | Upgrade cost default |
| Exponential | ×N per step | Avoid — breaks fast | Avoid — breaks fast |
| Custom stepped | Designer-defined | Rarity gates, cycle thresholds | Rarity gates, progression thresholds |

Triangular numbers are the correct first guess for most upgrade costs.
Exponential doubling in any mechanic is high-risk — nearly always breaks
balance at scale.

### Costs and Benefits Must Be Equal

Every item, upgrade, and elemental action has costs (everything limiting or
spent) and benefits (everything positive). The balance target is equality.

- Overpowered = benefits exceed costs → add costs or reduce benefits
- Underpowered = costs exceed benefits → reduce costs or increase benefits
- Overcosted ≠ underpowered — diagnose before fixing

Conditional benefits (only fire on a Critical, only apply in the Rift) are
worth less than unconditional ones. Price them accordingly.

### Solvability and Meaningful Decisions

A game is trivially solvable when optimal play is always obvious.

**Loop application:**
- Elemental evolution path choices must not have a "correct" answer
- Cards of Fate must have configurations where opting out is genuinely right
- Upgrade purchase order must require thought, not just "buy the next one"
- The Ritual's symbol codes risk determinism if sequence order is always
  fixed — vary the code sequence per instance

### Flow Theory (Schreiber / Sylvester)

Too easy → boredom. Too hard → frustration. Flow = challenge at the peak of
the player's current ability.

**Loop application:**
- Minigame difficulty scales with elemental Form (Ritual: 8s/6s/4s timer
  by Form is a correct implementation)
- Workshop complexity increases as the player's elemental roster grows
- Cards of Fate complexity (more decks, more cards) should unlock gradually

---

## PART 4 — JUICE AND FEEDBACK (Jonasson & Purho)

### Definition

```
"A juicy game feels alive and responds to everything you do — tons of
cascading action and response for minimal user input."
```

Juice is functional feedback that confirms the game's state changed,
rewards the player's action, and creates desire to act again.

**Principle:** Maximum output for minimum input. Every player tap must
produce disproportionate sensory response.

### The Loop's Juice Priority List

| Moment | Juice requirement |
|---|---|
| Ritual successful code entry | Satisfying snap/lock — each symbol confirm |
| Elemental Ascension | The highest-impact moment in a cycle — FX, sound, number reveal |
| Critical hit on yield | Must feel dramatically different from a normal roll |
| Cards of Fate flip | Reveal should feel ceremonial — not just a number update |
| Source activation (cycle end) | The Loop's "save point" moment — must feel earned and complete |
| Item craft completion | Tactile, weighted — not a menu transaction |
| Grade-up (elemental evolution) | Visual transformation, not just a stat update |

For other projects: identify the highest-impact moments in each session
structure and apply these same principles to those moments.

### Juice Principles Applied

**Squeeze and stretch:** On significant events (Ascension, Critical, Source),
make elements momentarily bigger/smaller before settling.

**Particle cascades:** Mana particles, elemental FX, crafting sparks. Every
particle is a unit of feedback.

**Screen response:** Subtle screenshake or camera push on high-impact moments.

**Sound layering:** Sound is 50% of juice. Audio and visual feedback must
arrive simultaneously.

**Easing curves:** All animations ease — not linear. Ease-out on arrivals,
ease-in on departures. Elastic/bounce easing for rewards and number reveals.

**The anti-juice warning:** Juice without substance is empty. Build the loop
first, juice second.

---

## PART 5 — PROGRESSION AND ELDER GAME (Schreiber / Cook)

### Three Pacing Questions

1. Is current challenge appropriate for current player power? (flow)
2. Does capability grow fast enough to feel rewarded but not so fast nothing
   feels earned?
3. After all systems are mastered, is there something left? (elder game)

### The Elder Game Problem

Cook's framework: when all arcs are consumed and all loops are solved,
players leave. The elder game must be designed before launch, not after.

**Loop application — elder game options:**
- **Codex completion** (lore discovery — arc-heavy, low dev cost)
- **The Exchange narrative** (True Time events — ongoing arcs)
- **Elemental collection** (new elementals as future content — content
  treadmill risk — requires sustainable production)
- **Cycle efficiency optimization** (speed-running the Waltz — loop-based,
  self-sustaining, no new content required) ← strongest candidate

For other projects: design at least one loop-based elder game activity that
works without new content.

### Progression Rate Tuning

Sylvester: progression should reveal new strategic options, not just make
numbers bigger. Each evolution grade, Workshop unlock, or upgrade tier
should open a decision space that didn't exist before.

If an upgrade tier only makes an existing choice more powerful (not
different), it is power inflation, not progression.

---

## PART 6 — METRICS AND ITERATION (Schreiber)

### What to Track (Priority Order Post-Launch)

1. Cycle completion rate (do players finish cycles or abandon mid-cycle?)
2. Mana at cycle end (too high = economy too generous; zero = starved)
3. Upgrade purchase distribution (unpurchased upgrade = broken price or
   weak effect)
4. Minigame completion rate per minigame (frustration signal)
5. Churn point by cycle number (should be well past cycle 50)
6. Session length mean vs. median (outliers reveal abuse cases or pain points)

For other projects: substitute your project's session unit, primary currency,
and minigame names into this tracking list.

### The 95% Problem

A playtest sample of 5–10 people cannot confirm balance. Target 20–30
playtests before making any balance change permanent.

---

## QUICK REFERENCE: Balance Checklist for New Mechanics

Before finalizing any value or system:

- [ ] What emotional state should this mechanic produce? (Sylvester)
- [ ] Is the core interaction a loop or an arc? (Cook)
- [ ] What is the central resource? (The Loop: mana)
- [ ] What is the expected value of output? (calculate, don't estimate)
- [ ] What curve governs cost? (triangular default; justify departures)
- [ ] Is there a genuine trade-off, or does one choice dominate?
- [ ] Does the value hold at extremes? (early cycle, late cycle, min/max)
- [ ] Is variance sized appropriately? (not so high a bad roll ruins a session)
- [ ] What happens in the elder game when this is fully upgraded?
- [ ] Does every player action produce sufficient juice? (Jonasson/Purho)
- [ ] Does the fiction and the mechanic say the same thing? (Sylvester)

---

## Examples

**Example 1 — Costing a new upgrade tier**

User asks: "What should the cost be for the third Familiar trust upgrade?"

Applies PART 3:
- Relationship: triangular default (1, 3, 6, 10…) — apply unless justified
- Evaluate conditional vs. unconditional benefit: if benefit only fires on
  Critical yields, discount cost accordingly
- Check: does this tier open new decision space, or only inflate power?
- Output: suggested cost with curve formula, flag if power inflation risk

**Example 2 — Mechanic producing wrong emotional arc**

User asks: "Players are reporting the Workshop feels stressful."

Applies PART 1 (Sylvester):
- Target emotional arc for Tower phase: focused efficiency, satisfying completion
- Stressful = flow disrupted; challenge exceeds current player power
- Diagnostic: Does complexity scale with roster size? Is any step opaque?
- Output: adjustments mapped to emotional target, not just number tweaks

**Example 3 — New mechanic audit**

User introduces the Crucible (a new precision minigame).
Run the Quick Reference checklist:

```
Emotional target: focused challenge, earned satisfaction
Core interaction: loop (repeatable, skill-based)
Central resource: time window + input precision
Variance: moderate (window size varies by Form)
Elder game: Crucible efficiency run — loop-based, no new content needed
Fiction/mechanic alignment: precision = control over unstable elemental energy
```

**Example 4 — Challenge 5 catches opaque failure state**

User asks: "The Ritual minigame feels frustrating. Players keep failing and giving up."

Challenges 1–3 pass (mechanic feel, not rate math; emotional target = focused challenge;
loop-based with elder game replay). Running Challenge 5:

Failure state audit: player fails symbol sequence → mana yield reduced → cycle ends with
deficit. But the failure feedback only shows "Ritual incomplete" — no indication which
symbol was wrong, what the correct sequence was, or whether the failure was timing-based
or sequence-based.

Challenge 5 result: BLOCKED — failure state is opaque. Player experiences consequence with
no readable cause. This is frustration without instruction, not challenge with stakes.

Fix before delivering: surface which symbol failed and highlight the correct window on
failure. The frustration signal is not difficulty — it is opacity. Difficulty with
readable cause produces learning; opacity produces only churn.

---

## ADVERSARIAL SELF-REVIEW

**HARD FAIL:** MUST NOT deliver any balance recommendation before this confirmation block is produced.

Run before delivering any balance output:

**Challenge 1 — Scope check**
Is the question about mechanic feel, fun, flow, or juice? If it is actually
about income rates, scaling, session pacing, or upgrade cost curves — flag
as IDLE-MATH scope and activate IDLE-MATH domain via dispatcher.

**Challenge 2 — Emotion-first check**
Before stating any balance number or curve: has the target emotional state
been named? A balance recommendation without an emotional target is numeric
guesswork.

**Challenge 3 — Elder game check**
Does the mechanic being balanced remain meaningful in the elder game, or does
it become irrelevant after all arcs are consumed?

**Challenge 4 — Feedback Loop Identification**
Does this mechanic contain a complete feedback loop: player action → visible
state change → feedback signal → updated mental model → repeat?

Fail signals:
- The mechanic produces a state change the player cannot observe or connect to their action
- Feedback is delayed past the point where the player can attribute it to a specific action
- The mechanic only delivers information once (arc) while being presented as a repeatable system (loop)

Pass requirement: Name the feedback loop explicitly — what action, what state change, what
feedback signal, what mental model update. If the mechanic is intentionally arc-based,
confirm that is deliberate and that adjacent loops provide retention.

**Challenge 5 — Failure State Design**
Does this mechanic have a failure state, and does that failure state teach rather than
merely punish?

Fail signals:
- There is no failure state — the mechanic cannot produce a losing outcome, eliminating
  challenge and learning
- The failure state is opaque — the player fails but cannot identify why (frustration
  without instruction)
- The failure state strips progress without providing a readable cause the player can
  act on next time

Pass requirement: Name the failure state and confirm it is readable — the player understands
what they did wrong and what to try differently. If no failure state exists, confirm this
is intentional (idle mechanic, not skill-based) and that the mechanic sources its challenge
from elsewhere.

**Challenge 6 — Teach / Test / Challenge Arc**
Does this mechanic sequence through teach (introduce the concept), test (let the player
demonstrate mastery), and challenge (extend or stress-test that mastery)?

Fail signals:
- The mechanic jumps straight to challenge without a teach phase — new players encounter
  maximum difficulty with no scaffolding
- The mechanic only teaches and tests but never challenges — experienced players find no
  depth and disengage
- The teach phase is a disconnected tutorial blob rather than the mechanic's own
  early-difficulty ramp

Pass requirement: Name where each phase (teach / test / challenge) appears in the player's
encounter with this mechanic. For a proposed change to an existing mechanic, confirm the
sequence remains intact.

```
Balance self-review:
  Challenge 1 — Scope: [mechanic feel — CLEAR / economy/rates question — activate IDLE-MATH]
  Challenge 2 — Emotion-first: [emotional target named: X / NOT NAMED — must name before proceeding]
  Challenge 3 — Elder game: [loop-based / arc-based — elder game consideration stated]
  Challenge 4 — Feedback loop: [action → state change → signal → model update named / INCOMPLETE]
  Challenge 5 — Failure state: [failure state named + readable / none — confirmed intentional / opaque — fix before delivering]
  Challenge 6 — Teach/test/challenge: [all three phases located / MISSING: [phase] — fix before delivering]
  Status: CLEAR to deliver / BLOCKED — [reason]
```
