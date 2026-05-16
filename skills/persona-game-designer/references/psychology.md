# Psychology Reference — Player Motivation and Audience Design

Loaded by designer-games dispatcher when PSYCHOLOGY domain activates.

## Table of Contents

- [PART 1 — The Correct Foundation: Self-Determination Theory](#part-1)
- [PART 2 — The Loop's Audience Profile (Quantic Foundry)](#part-2)
- [PART 3 — Relatedness Through NPCs: The Parasocial Case](#part-3)
- [PART 4 — Bartle in Context](#part-4)
- [PART 5 — Cozy Game Psychology](#part-5)
- [PART 6 — Onboarding and First Session](#part-6)
- [Quick Reference: Player Type → What They Need](#quick-reference)
- [Examples](#examples)
- [Adversarial Self-Review](#adversarial-self-review)

---

## PART 1 — THE CORRECT FOUNDATION: SELF-DETERMINATION THEORY

### Why SDT, Not Bartle

Bartle (1996) describes behavioral patterns in *social* environments. Two
of his four types (Killers, Socializers) require other humans. His taxonomy
is descriptive, not explanatory — it tells you what players *do*, not *why*.

Self-Determination Theory (SDT) explains the *why*. It identifies three
universal psychological needs that, when satisfied by a game, predict
enjoyment, immersion, and continued play across every genre studied:

| Need | What it means | Frustrated by |
|---|---|---|
| **Autonomy** | My choices feel meaningful and self-directed | Forced paths, no real decisions, illusion of choice |
| **Competence** | I'm getting better at something that matters | Too easy (trivial), too hard (opaque), no feedback |
| **Relatedness** | I feel connected to something or someone | Isolation, characters who don't respond to me, no stakes |

All three must be present. A game that satisfies Autonomy and Competence
but not Relatedness produces skill mastery without emotional investment.
A game that satisfies Relatedness but not Competence produces attachment
without engagement.

### Mapping SDT to Session Phases

**Loop application:**

| Phase | Primary need served | Design requirement |
|---|---|---|
| **Dreaming** | Autonomy | Cards of Fate choices must be consequential, not cosmetic. Opt-out must be a genuine strategic option. |
| **Rift** | Competence | Elemental evolution and Ritual minigame must produce a visible mastery signal. Grade-ups = competence confirmation. |
| **Tower** | Autonomy + Competence | Crafting decisions must require optimization thought, not just execution. |
| **Familiar arc** | Relatedness | The primary long-form Relatedness engine — see Part 3. |
| **The Exchange** | Relatedness (secondary) | NPC relationships extend Relatedness beyond the Familiar. |

**For other projects:** Map each session phase to its primary SDT need and
confirm the design requirement is met.

### SDT Checklist for Any New Feature

1. Does this satisfy or frustrate **Autonomy**?
2. Does this satisfy or frustrate **Competence**?
3. Does this satisfy or frustrate **Relatedness**?

A feature that frustrates all three will be abandoned. A feature that
satisfies all three will be returned to.

---

## PART 2 — THE LOOP'S AUDIENCE PROFILE (Quantic Foundry)

The Quantic Foundry model identifies 12 motivations across 6 clusters,
derived from factor analysis of 500,000+ gamers.

### The Loop's Motivation Fingerprint

**Primary motivations:**

| Motivation | How The Loop serves it |
|---|---|
| **Fantasy** | Hero as summoned survivor, dark cosmic world, Familiar bond |
| **Story** | Eight-beat spine, Familiar arc, Ryszard conspiracy, lore revelation |
| **Discovery** | Codex unlocks, lore fragments, true history behind the Official Account |
| **Completion** | Elemental collection, Codex %, Workshop recipe completion, upgrade trees |
| **Strategy** | Cards of Fate, upgrade path choices, elemental archetype selection |

**Secondary motivations:** Power (elemental evolution, Workshop mastery),
Design (Loop aesthetic progression).

**Motivations not served:** Competition (single-player only), Community
(no multiplayer), Destruction (tone is calm/dark), Excitement (pace is
deliberate).

**For other projects:** Build an equivalent fingerprint. Identify 3–5
primary motivations, 2–3 secondary, and explicitly name what you are not
targeting — this prevents scope creep into mechanics your audience doesn't want.

### The 9 Quantic Gamer Types — Audience Map

**Loop primary audience:**

- **Architect** — Solo, slow-paced, planning-heavy, wants to build something
  enduring. Serves every Loop design pillar.
- **Gardener** — Quiet, relaxing task completion. Spontaneous and reactive.

**Loop secondary audience:**

- **Slayer** — Curated narrative, solo, slow-paced. Served by Familiar arc,
  eight-beat spine, Ryszard reveal.
- **Bounty Hunter (partial)** — Served by elemental evolution and Codex
  completion. Underserved by absence of open-world exploration.

**Not The Loop's audience:** Skirmisher, Ninja, Gladiator.

### Demographic Layer

Architect and Gardener types in QF data:
- **Gender:** Both skew female relative to the overall gamer population.
  Design, tone, and marketing should reflect this.
- **Age:** Both skew older (mid-20s through 40s). Less time per session,
  higher patience for complexity, respond to emotional sophistication.
- **Platform:** The Loop's 15–20 min cycle target is correctly calibrated
  for this cohort.

### The Architect/Gardener Design Tension

These two types share the Loop's playerbase but want different things.
The Architect wants strategic depth (Cards of Fate complexity, upgrade tree
planning). The Gardener wants reactive simplicity (clear signals, no
cognitive overhead).

**Resolution:** The Loop's two-speed design resolves this naturally:
Dreaming phase = Architect, Rift/Tower = Gardener. Protect this separation.
Never make the Dreaming reactive and pressured. Never make the Rift/Tower
require deep pre-planning.

---

## PART 3 — RELATEDNESS THROUGH NPCs: THE PARASOCIAL CASE

### Why Single-Player NPC Relationships Satisfy Social Needs

The mechanism is **parasocial interaction (PSI)**: one-sided social
engagement with a mediated persona. Multiple studies confirm these
relationships partially satisfy genuine social needs (Elvery 2022,
Tyack & Wyeth 2017, Frontiers 2022).

**The key SDT finding:** Players can experience Relatedness through NPC
interactions via **contingent responsiveness** — the NPC responding
*differently* based on what the player has specifically done.

**Additional finding:** NPC friendships positively predict harmonious
gameplay passion. A well-designed Familiar relationship is both an emotional
feature and a retention mechanic.

### Four Conditions for Meaningful NPC Attachment

1. **Distinct personality** — Recognizable, consistent voice
2. **Contingent responsiveness** — Reacts based on what *this* player did
3. **Narrative continuity** — Remembers the relationship's past
4. **Emotional expressiveness** — Communicates internal states

### The Familiar — Relatedness Engine Analysis

| Condition | Familiar's design status | Assessment |
|---|---|---|
| Distinct personality | Watchful, guarded, earned caution, curious | Strong — name and visual still unresolved |
| Contingent responsiveness | Intended but not yet designed mechanically | Critical gap — requires arc milestones tied to player actions |
| Narrative continuity | Every previous custodian is part of Familiar's history | Strong lore foundation in place |
| Emotional expressiveness | Currently locked — restraint is deliberate in early cycles | Strong — the restraint itself is expressive if the release is well-designed |

**The critical design gap:** How does the Familiar's guardedness
*mechanically* change over time? Without explicit triggers tied to player
actions — not cycle count — the relationship arc will feel static.

### The Exchange NPCs — Secondary Relatedness

- **Familiar**: Intimacy, history, mutual dependency, gradual trust
- **Ark NPCs**: Utility relationships that deepen into care —
  the coworker-who-becomes-a-friend arc

Ark NPCs should feel like they have lives independent of the player.
The Cult as inverted Relatedness: NPCs with moral complexity produce
stronger attachment than purely sympathetic characters (Elvery 2022).

---

## PART 4 — BARTLE IN CONTEXT

Use Bartle as quick shorthand for behavioral patterns. Use SDT and Quantic
Foundry for actual design decisions.

**Achiever** — Served by: Codex %, elemental collection, upgrade completion.
Churn risk: content exhaustion. Design implication: completion horizon must
never go dark.

**Explorer** — Served by: lore fragments, true history, Ritual symbol mastery,
Ryszard conspiracy arc. Churn risk: content starvation — exhausts content
fastest. Design implication: layer discovery so it rewards multiple passes.

**Socializer (via parasocial)** — Served by: Familiar arc, Ark NPC
relationships, Cult moral complexity. Requires contingent responsiveness.
Generic warmth does not satisfy Socializers — recognition of *this* player
does.

**Killer** — Not The Loop's audience. Single-player only. No design
resources should target this type.

---

## PART 5 — COZY GAME PSYCHOLOGY

### The Formal Framework: Safety, Abundance, Softness

Project Horseshoe (Daniel Cook, 2018) defines coziness as "how strongly a game evokes the fantasy of safety, abundance, and softness." These three properties are the design filter for every cozy mechanic decision:

- **Safety:** Absence of danger, risk, or impending loss. The player is never under threat. The Loop's no-failure-state is the mechanical expression of safety.
- **Abundance:** Base needs (resources, time, shelter) are already met. Players operate from a position of surplus, not scarcity. The Loop's mana economy must always feel generative, not starving.
- **Softness:** Visual warmth, slow-paced audio, gentle progression. The aesthetic is not decoration — it is the psychological signal that says "this is a safe space."

### Four Additional Cozy Design Properties (Cook 2018)

**Ritual:** Facilitating repeated, meaningful actions creates familiarity and contentedness. The Loop's cycle structure (Dreaming → Rift → Tower → Source) IS a ritual. Each cycle should feel like returning to something beloved, not replaying a level. Design implication: the ritual must vary enough to stay meaningful but remain recognizable enough to feel like home.

**Seasons:** The visual passing of seasons is deeply connoted with coziness — familiarity, cycles of community and abundance. The Loop's elemental structure and True Time NPC windows naturally support seasonal expression. Design implication: seasonal visual variation in the farm environment (even subtle) reinforces the cozy contract at zero narrative cost.

**Welcome:** When the player is explicitly positioned as a welcomed entity, they feel free to express themselves without obligation or pressure. The Familiar's role is partly this: not "you are the hero destined to save everything" but "I am glad you are here, specifically." Design implication: avoid hero-pressure framing in tutorial. The player is a custodian — a welcomed presence — not a chosen one under obligation.

**Intermezzo (retention framing):** Cook frames cozy games as "intermezzo" — the musical passage between major movements. Coziness helps retention by giving players control over pacing while maintaining engagement during periods of rest. For The Loop: the cycle IS the intermezzo. It should feel like a meaningful pause from the world's darkness, not a trivial distraction from it. This reframes the "why do players return" question — they return for the rest, not despite it.

### What Cozy Games Do Psychologically

- No threat, no failure state → safety + abundance mode
- Guaranteed progress → every action produces visible positive change
- Low-stakes mastery → Competence satisfaction without fear of failure
- World-tending → the game is something you care for, not conquer

**Loop application:** The no-failure-state design is psychologically
coherent with this genre. Failure states or punitive mechanics would break
the psychological contract with the Gardener audience.

### The Cozy-Dark Tension

The Loop occupies unusual psychological territory: cozy mechanics wrapped
in dark fantasy aesthetics. This is not a contradiction — it is the central
design asset. The safety of the cozy loop makes the dark lore *more*
affecting, not less.

The Loop replicates Animal Crossing's pandemic structure: a pocket of
safety (the farm, the cycle, the Familiar) surrounded by existential threat
(the Void, the Swarm, the Lord of Whispers). Players tend their farm while
the world ends.

**Design implication:** The Dreaming, Rift, and farm environment must always
feel safe — even beautiful. The danger lives in the lore, the Communications
Array, and the narrative beats. It must never intrude visually or
mechanically into the farm space itself.

---

## PART 6 — ONBOARDING AND FIRST SESSION

### Why the First Session Is Disproportionately Important

SDT research: players who do not experience all three needs within the first
session churn at significantly higher rates. **Loop application:** For a
mobile game with a $1.00 conversion gate at cycle 100, first-session
retention is the direct predictor of conversion cohort size.

**The Endowed Progress Effect:** Start cycle 1 with a small mana balance
(not zero). The Familiar's tutorial should give the player a small win
within the first 2 minutes. Show the full evolution path before unlocking it.

### First Session SDT Requirements

**Autonomy:** The first Cards of Fate draw must feel like a *decision* the
player made, not a cutscene they watched. Even a single opt-out moment
satisfies Autonomy more than a forced-flip tutorial.

**Competence:** The player must succeed at the Ritual minigame and Ascend
the tutorial elemental before the session ends. Make both events maximally
juiced — the first Ascension should feel remarkable even if the numbers are
small.

**Relatedness:** The Familiar must say something in the first session that
is specific — something that implies history, awareness, or personality.
Even a single line of restrained warmth that signals "I am watching you,
specifically" plants the Relatedness seed.

### Tutorial Scope Constraint

The tutorial is an arc (Daniel Cook: a one-way information delivery,
consumed once). Make it as short as possible. Get the player into cycle 1
with just enough to not be lost, then let the loops do the work.

---

## QUICK REFERENCE: Player Type → What They Need

| Player type | Primary need | Churn trigger | Loop design antidote |
|---|---|---|---|
| Architect | Strategic planning, enduring construction | Systems feel solved too early | Deepen upgrade tree; add Cards of Fate variants |
| Gardener | Calm task completion, clear feedback | Overwhelmed by complexity | Keep Rift/Tower reactive, not strategic |
| Slayer | Curated story, be the protagonist | Narrative stalls | Advance Familiar arc milestones consistently |
| Explorer | Hidden things, lore depth, mastery | Content exhausted | Layer lore reveals; gate true history behind investigation |
| Achiever | Visible completion, collectibles | Completion horizon goes dark | Always show next achievement; define post-100 goals |
| Socializer (parasocial) | NPC relationships that remember them | Familiar/NPCs feel generic | Contingent responsiveness — every interaction references history |

---

## Examples

**Example 1 — Evaluating a new feature against SDT**

User proposes adding a daily login streak reward.
Runs the SDT checklist:

- Autonomy: streak applies external pressure — obligation, not choice.
  Frustrates Autonomy for the Gardener.
- Competence: no skill expression, just showing up. Neutral.
- Relatedness: no NPC acknowledgment attached. Missed opportunity.
- Verdict: Replace streak reward with a "returned after absence" Familiar
  dialogue moment — satisfies Relatedness without pressuring Autonomy.

**Example 2 — Familiar dialogue tone review**

User asks: "Does this Familiar line land correctly for early cycles?"

Applies PART 3 (contingent responsiveness):
- Is this response generic, or specific to what the player just did?
- Does it signal awareness of history?
- Does it show Competence acknowledgment?
- Output: specific line edits with rationale tied to SDT and arc stage

**Example 3 — Architect vs. Gardener tension**

User proposes adding a second deck to Cards of Fate at cycle 5.

Applies PART 2:
- Architect: values the added strategic depth — wants this
- Gardener: second deck at cycle 5 may overwhelm — churn risk
- Recommendation: gate the second deck behind a visible milestone
  the player unlocks (Autonomy + Competence signal), not a cycle timer

---

## ADVERSARIAL SELF-REVIEW

**HARD FAIL:** MUST NOT deliver any psychology or audience design recommendation before this confirmation block is produced.

**Challenge 1 — Scope check**
Is the question about player motivation, emotion, or audience profiling? If
it is actually about economy balance, retention benchmarks, or mechanic
numbers — flag as IDLE-MATH or BALANCE scope and activate the appropriate
domain via dispatcher.

**Challenge 2 — SDT completeness**
Before delivering any feature evaluation or design recommendation: have all
three SDT needs (Autonomy, Competence, Relatedness) been assessed? Evaluating
only one or two needs produces incomplete advice. Flag which needs were not
assessed and why.

**Challenge 3 — Loop-specific label check**
Does the output apply Loop-specific frameworks (Familiar arc, Architect/Gardener
tension, cozy-dark design) to a non-Loop project without explicitly labeling
them as Loop-specific? If so — reframe as "For other projects:" equivalents
before delivering.

```
Psychology self-review:
  Challenge 1 — Scope: [player motivation/emotion — CLEAR / scope mismatch — activate IDLE-MATH or BALANCE]
  Challenge 2 — SDT completeness: [all 3 needs assessed / only [X,Y] assessed — [Z] skipped because [reason]]
  Challenge 3 — Loop-specific framing: [Loop labels used on Loop project — CLEAR / Loop labels applied to non-Loop project — reframed]
  Status: CLEAR to deliver / BLOCKED — [reason]
```
