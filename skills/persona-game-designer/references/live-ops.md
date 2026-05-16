# Live Ops Reference — Event Design and Post-Launch Operations

Loaded by persona-game-designer dispatcher when LIVE-OPS domain activates.

## Table of Contents

- [PART 0 — The Live Ops Contract (Cozy Edition)](#part-0)
- [PART 1 — Event Taxonomy](#part-1)
- [PART 2 — FOMO vs. The Cozy Contract](#part-2)
- [PART 3 — True Time as Live Ops Primitive](#part-3)
- [PART 4 — Minimal Viable Event Design (Solo Dev Scale)](#part-4)
- [PART 5 — Event Calendar Design](#part-5)
- [Examples](#examples)
- [Adversarial Self-Review](#adversarial-self-review)

---

## PART 0 — THE LIVE OPS CONTRACT (COZY EDITION)

Live ops in cozy games operates under a different contract than in competitive
or midcore mobile games. The standard live ops toolkit (FOMO, expiring rewards,
urgency-based return triggers) directly violates the cozy contract. Every live
ops decision must satisfy the same Safety/Abundance/Softness framework that
governs the core game.

**The non-negotiable constraint:** A cozy game player has accepted a contract
that says: this game will never make me anxious. A live ops event that produces
urgency, pressure, or fear of missing out is a contract violation — documented
to cause direct community backlash even in successful cozy titles. (Palia's
Maji Market event: community backlash after it required near-constant play to
complete within the event window. Developers subsequently introduced a
"FOMO-free" Lunar Path with no expiration date.)

**The cozy live ops principle:** Events should feel like seasonal rituals —
recurring, familiar, low-pressure enrichments of an existing loop. Not
limited-time tests of commitment.

---

## PART 1 — EVENT TAXONOMY

### Always-On Events

Content that is permanently available and accumulates over time. No time limit,
no expiration, no FOMO.

| Type | Description | Cozy compatibility | Loop application |
|---|---|---|---|
| Seasonal themes | Visual/audio changes tied to real-world or in-game seasons | ✅ COMPATIBLE | Farm environment shifts per season (autumn harvest aesthetic, winter stillness) |
| Evergreen reward tracks | Progression paths with no expiration — player completes at own pace | ✅ COMPATIBLE | Waltz Pass model: cosmetics + lore, never expires |
| Codex expansion | New lore fragments added in updates, available forever | ✅ COMPATIBLE | Post-update Codex entries unlock for all players |
| NPC storyline chapters | New Exchange NPC narrative added in patches | ✅ COMPATIBLE | Exchange NPC arc chapters added per update cycle |

### Limited-Time Events (Cozy-Compatible)

Content available for a defined window but designed to avoid FOMO.

| Type | Design rule | Cozy compatibility |
|---|---|---|
| Seasonal festival (visual only) | Cosmetic changes, no exclusive rewards unavailable later | ✅ COMPATIBLE — if rewards return in future seasons |
| Community milestone | Server-wide goal; ALL players receive reward regardless of session count | ✅ COMPATIBLE — no individual obligation |
| Weekly hidden discovery | Slime Rancher Party Gordo model: weekly secret available Fri–Sun, not permanently required | ✅ COMPATIBLE — players who miss it miss a bonus, not essential content |
| Narrative event | Story chapter available for N weeks, then permanently archived in Codex | ✅ COMPATIBLE — time-limited access window, permanent archive |

### Limited-Time Events (Cozy-Incompatible)

| Type | Why incompatible |
|---|---|
| Exclusive cosmetics that expire and never return | Permanent FOMO — players who miss them are permanently excluded |
| Events requiring hourly engagement to complete | Obligation and anxiety — direct cozy contract violation |
| Leaderboard events with competitive scoring | Competitive pressure = cozy contract violation for Gardener audience |
| Streak-based event rewards | Streak mechanics apply external pressure — Autonomy threat |

---

## PART 2 — FOMO VS. THE COZY CONTRACT

### The Documented Failure

Palia (cozy MMO) launched Maji Market (2023): players needed to play nearly every
hour for 15 days to feasibly complete the event. Community response: "Maji Market
is not cozy or non-FOMO." Developer acknowledgment: "We've noted that Community
Events have received cold feedback." Subsequent redesign: Lunar Path — a battle
pass with no expiration date, where players progress at their own pace over any
timeframe.

This is the canonical case study. The failure mechanism: time-limited rewards +
high session requirement = obligation = anxiety = cozy contract broken.

### The Resolution Pattern

**Palia Lunar Path model (verified):** Battle pass with no expiration. Free and
paid tracks. Progression unlocks naturally through core gameplay. Player can
purchase the pass at any time and complete it whenever. Revenue is generated
through pass purchase, not through time pressure.

**Slime Rancher Party Gordo model (verified):** Weekly event active
Friday–Sunday. Simple engagement (find gordo, feed it 10 items). Rewards:
decorative ornaments, not progression-essential items. No permanent exclusivity:
ornament types repeat on a cycle. No streak requirement. Miss a week → no
consequence beyond missing that week's decorations.

### The Design Test

Before finalizing any limited-time event element, answer:
1. If a player misses this event entirely, do they lose something they cannot recover? → If yes: FAIL.
2. Does completing this event require more than one normal session per real-world day? → If yes: FAIL.
3. Does the event surface a notification with deadline language ("ends in 3 days!")? → If yes: rewrite as invitation language ("available through Sunday").
4. Does a player who never participates in any event still have a complete game experience? → If no: FAIL.

---

## PART 3 — TRUE TIME AS LIVE OPS PRIMITIVE

The Loop's True Time NPC system is a live ops mechanic — it creates
structured return windows tied to real-world time. It should be designed
as live ops from the start, not bolted on post-launch.

### True Time Design Rules

**Spacing:** 22–26 hours between NPC event windows. This is the optimal
fixed-interval schedule for creating reliable daily return habits without
producing obligation (IDLE-MATH validated).

**Framing:** Invitation, not deadline. The NPC is "available now" not
"leaving in 2 hours." Players who miss a window should encounter a natural
re-entry point, not a punitive gap.

**Reward structure:** NPC window rewards (renown, Exchange items) should be
completable within a single normal session. A player who engages for their
standard 15–20 min cycle should be able to complete all active NPC events
in that session.

**Miss penalty:** Zero. A player who misses an NPC window should simply see
the next available window when they return. No "you missed it" messaging.
No degraded reward. The NPC had "other things" — they'll be available again.

**Live ops expansion path:** Post-launch, True Time events can be enriched:
- Seasonal variant dialogue (NPC reacts to the current seasonal theme)
- Community events (all players contributing to a shared goal via NPC windows)
- Special appearance windows (rare NPC visits that add lore, not pressure)

---

## PART 4 — MINIMAL VIABLE EVENT DESIGN (SOLO DEV SCALE)

Standard live ops infrastructure (real-time analytics, server-side event
configuration, A/B testing pipelines) is beyond solo developer scope.
The Loop's live ops must be achievable within a solo development workflow.

### Solo-Scale Event Patterns

**Hardcoded seasonal themes:** Visual asset swap on a calendar trigger.
No server infrastructure. Implementation: check device date, apply seasonal
skin pack. Cost: asset creation + one date-check conditional.

**App update as event:** New content in an app update is the primary live ops
vehicle for a solo developer. Frame updates as events: "The Exchange welcomes
a new visitor" (new NPC in an update). Players who update see new content.
No server infrastructure required.

**Static True Time:** NPC windows triggered by device clock, not server.
No personalization. All players see events at the same times. Predictable,
zero infrastructure, sufficient for v1.

**Seasonal pass via IAP:** One-time purchase that unlocks a set of content
delivered over time (or all at once). No server-side configuration needed —
the pass content is shipped in the update, the IAP unlocks access.

### Infrastructure Investment Decision Tree

```
Is the event content personalized to individual player behavior? → If yes: needs server
Is the event triggered by real-time analytics? → If yes: needs server
Is the event time-limited on a server clock (not device clock)? → If yes: needs server
Is the event a visual/audio swap on a calendar date? → Device clock sufficient
Is the event a reward track with no expiration? → In-app sufficient
Is the event a community milestone (all players)? → Server required, but minimal
```

For v1: all events should be device-clock or update-delivered. Server-side
event configuration becomes worth the engineering cost when DAU exceeds
~10,000 active daily players.

---

## PART 5 — EVENT CALENDAR DESIGN

### Calendar Structure Principles

**Predictable rhythm over volume.** Players value consistent cadences over
frequent novelty. One reliable weekly event beats three inconsistent monthly
ones. Appodeal 2025: "A predictable rhythm likely helped players form a habit."

**Seasonal anchors + evergreen baseline:**
- Evergreen (always-on): True Time NPC windows, Waltz Pass track
- Seasonal (quarterly): Visual farm theme swap, seasonal NPC dialogue variants
- Special (ad hoc): Major narrative updates, new Exchange NPC additions

**The event density ceiling:** For a 15–20 minute session game, never run
more than two active event types simultaneously. More than two creates
cognitive overhead that conflicts with the cozy experience.

**Cozy calendar example:**

| Cadence | Event | Player action required | FOMO risk |
|---|---|---|---|
| Daily (22–26h) | True Time NPC windows | 1 session to complete | None — repeats |
| Weekly | Seasonal discovery (Gordo model) | Optional — find hidden element | None — misses only a decoration |
| Quarterly | Farm seasonal theme | None — automatic | None — visual only |
| Per update | New Exchange NPC / narrative chapter | Optional — engage on own timeline | None — always available |
| Per major milestone | Custodian community event | Opt-in — contribute to shared goal | None — all players receive reward |

---

## Examples

**Example 1 — Designing a seasonal winter event**

Question: "We want a winter event for cycle 50+. What should it look like?"

LIVE-OPS activates. PSYCHOLOGY activates (cozy contract check).

Classification: seasonal event design + cozy contract → LIVE-OPS + PSYCHOLOGY.

Run PART 1 (event taxonomy): seasonal festival. Run PART 2 (FOMO test):
- Exclusive rewards that expire? → No: cosmetics return in future winters.
- Obligation level? → One session sufficient to see all content.
- Notification language? → "Winter has come to the farm" (invitation), not "Event ends in 3 days."

Cross-domain check (LIVE-OPS + PSYCHOLOGY): FOMO vs. cozy contract. Resolution: no
expiring exclusives, invitation framing, one-session completability. Pass.

Output: Farm visual theme switches to winter palette. Familiar has seasonal dialogue
variant (10–15 unique lines). True Time NPC windows have seasonal gift exchange option.
One hidden discovery element available each weekend (Party Gordo pattern). All cosmetics
from winter event return the following winter.

**Example 2 — Evaluating a proposed FOMO mechanic**

Proposal: "24-hour flash sale on a Familiar cosmetic — creates urgency."

LIVE-OPS activates. MONETIZE activates. PSYCHOLOGY activates.

PART 2 FOMO test: Does missing this mean permanent loss? → YES. Expiring exclusive.
FAIL. Cozy contract violation.

Cross-domain: LIVE-OPS + PSYCHOLOGY (FOMO vs. cozy contract). Priority rule 6
applies: cozy contract takes priority over revenue optimization.

Output: BLOCKED. Redesign as non-expiring sale — "This week's featured cosmetic
is discounted." The discount expires; the cosmetic remains purchasable at full price
afterward. Urgency is for the price, not the access.

---

## ADVERSARIAL SELF-REVIEW

**HARD FAIL:** MUST NOT deliver any live ops design recommendation before this confirmation block is produced.

**Challenge 1 — FOMO test**
Does any element of this event design produce permanent exclusivity (content
the player can never access if they miss the event)?
FAIL: Any reward or content that expires permanently.
PASS: All rewards are eventually available through another path or return in
future events.

**Challenge 2 — Obligation test**
Does completing this event require more than one standard session per day?
FAIL: Event requires daily check-ins, streak maintenance, or hourly play.
PASS: One normal 15–20 minute session completes all active event participation.

**Challenge 3 — Solo-scale test**
Does this event design require server-side infrastructure not yet built?
FAIL: Design assumes real-time analytics, personalization, or server-side
event triggers that aren't available.
PASS: Event is achievable via device clock, app update delivery, or static
content unlock.

**Challenge 4 — Cozy tone test**
Does the event's framing language and UX pattern feel like an invitation or
like a deadline?
FAIL: Countdown timers, "limited time only," "don't miss out" language.
PASS: Seasonal discovery language, "available while the season lasts," arrival
and departure framed as natural cycles, not commercial pressure.

```
Live ops self-review:
  Challenge 1 — FOMO: [no permanent exclusivity — CLEAR / expiring exclusive found — redesign]
  Challenge 2 — Obligation: [one session sufficient — CLEAR / daily requirement found — reduce]
  Challenge 3 — Solo scale: [device clock or update delivery — CLEAR / server infrastructure assumed — flag]
  Challenge 4 — Cozy tone: [invitation framing — CLEAR / deadline language found — rewrite]
  Status: CLEAR to deliver / BLOCKED — [reason]
```
