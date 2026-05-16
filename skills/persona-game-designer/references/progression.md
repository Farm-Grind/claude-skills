# Progression Reference — Unlock Sequencing and Elder Game Design

Loaded by designer-games dispatcher when PROGRESSION domain activates.

## Table of Contents

- [PART 1 — Confirmed Progression Anchors](#part-1)
- [PART 2 — Progression Failure Modes (idle game specific)](#part-2)
- [PART 3 — Progression Design Framework](#part-3)
- [PART 4 — Output Format](#part-4)
- [Examples](#examples)
- [Adversarial Self-Review](#adversarial-self-review)

---

## PART 1 — CONFIRMED PROGRESSION ANCHORS

Before any progression work, identify and apply your project's fixed
constraints. **The Loop's confirmed anchors:**

**Pay Gate:** Cycle 100 is the one-time $1.00 unlock. Everything before
cycle 100 is the Trial. Do not design elder game content in the Trial window.

**Custodian Tier I:** Threshold = 100 cycles (aligned with Pay Gate by
design, D-011 LOCKED). Tier I is the first achievement gate — it should
feel earned at cycle 100, not arbitrary.

**Elemental scope:** All four classical elements (Fire, Air, Water, Earth)
at v1 launch. No post-launch element unlocks in the base game scope.

**No-failure-state principle:** Universal across all Loop minigames. Progress
floors at 0%, ends only at 100% or cancellation. Progression design cannot
contradict this.

**Economy:** Mana is the sole currency. No cap. Prestige/reset mechanics are
NOT confirmed for v1. Design elder game without it as the primary mechanism
unless a decision is made.

**For other projects:** Document equivalent anchors (monetization gate,
prestige model, content scope, currency constraints) before sequencing.

---

## PART 2 — PROGRESSION FAILURE MODES (idle game specific)

### False floor
The player reaches what appears to be a content endpoint but the game still
runs. They lose motivation because they cannot see what's next.
Prevention: always keep at least one visible "next thing" — even if distant.

### Achievement vacuum
Achievements stop arriving for long stretches. The player interprets silence
as "done." Prevention: tier achievements so frequency decreases gradually —
never drops to zero during active play.

### Prestige dilution (conditional — prestige NOT confirmed for v1 Loop)
Resetting without meaningful new content or visible power delta causes
drop-off. The narrative-framing model (giving each reset a story beat) is
the reference for using a cycle structure as a natural prestige beat. Do not
apply this failure mode to Loop v1 design unless a prestige decision has
been logged.

### Unlock clustering
Too many unlocks arrive at once (typically mid-game), causing overwhelm.
Then a long dry period follows. Prevention: map unlocks against a progression
curve before finalizing the system.

---

## PART 3 — PROGRESSION DESIGN FRAMEWORK

### Step 1 — Map the content horizon
List all player-accessible content categories and assign each a rough
session/cycle estimate for first access.

**Loop categories:** elementals, upgrade tiers, Exchange NPCs, faction
renown tiers, achievements, Cards of Fate variants, Maintenance Panel
unlocks.

**Generic categories:** generators, upgrade tiers, NPC types, faction/renown
tiers, achievements, card/event variants, system unlocks.

### Step 2 — Identify the elder game threshold
When does "all basic content accessible" occur? That cycle count is the
start of the elder game. Everything after it needs ongoing goals.

**BLOCKED:** Do not estimate the elder game threshold without completing
Step 1 first. A threshold stated without a content horizon map is a guess.
If Step 1 data is unavailable, flag as OPEN and state the blocker.

### Step 3 — Design elder game goals
Elder game must offer at least three goal types operating simultaneously:
- **Numerical:** A progress bar still moving (mana accumulation, cycle
  count, renown tracker)
- **Milestone-gated:** An achievement or unlock that is genuinely distant
  but visible
- **Narrative:** Familiar arc progression, faction storyline depth

### Step 4 — Achievement tier calibration
**Loop achievement categories (from confirmed scope, MAN-75):**
- Progression milestones (cycle count, elemental count, upgrade tiers)
- Elemental mastery (per-elemental thresholds)
- Faction renown (per-Division/Faction milestones)
- Familiar arc (depth meter stages)
- Economy (mana totals, exchange completions)
- Custodian tier (Tier I = 100 cycles — LOCKED)

**Calibration rules (universal):**
- Achievements requiring OPEN design decisions must be flagged and not
  finalized until those decisions are locked
- No two categories should produce overlapping milestones at the same cycle
- Elder game achievements should activate after the content horizon threshold

### Step 5 — Onboarding sequence gate
**Loop requirements (MAN-24):**
- Introduce the Familiar before any mechanic is revealed
- Gate each mechanic introduction to a natural first occurrence — let
  mechanics emerge from play, not "go try this" tutorials
- First cycle should end with exactly one thing unlocked

**Generic rule:** First session should end with exactly one thing newly
unlocked — not zero (nothing to return to) and not three (overwhelming).

---

## PART 4 — OUTPUT FORMAT

```
PROGRESSION DESIGN OUTPUT — [scope]

Content horizon map:
  [session/cycle range] → [what unlocks / becomes accessible]

Elder game threshold: cycle [N]

Elder game goal coverage:
  Numerical: [what's still moving]
  Milestone: [distant but visible target]
  Narrative: [Familiar / faction arc progress]

Achievement tier calibration:
  [category] → [threshold] → [cycle estimate for typical player]

Open items: [any OPEN decisions blocking this output]
```

---

## Examples

**Example 1 — Elder game audit catches false floor**

Design review for a project where the only content listed ends at cycle 100:

```
PROGRESSION DESIGN OUTPUT — Elder game audit

Content horizon map:
  Cycles 1–30 → generator unlocks, first NPC contact
  Cycles 31–70 → upgrade tier 2, second NPC type
  Cycles 71–100 → elemental mastery tier 1

Elder game threshold: cycle 100

Elder game goal coverage:
  Numerical: OPEN — no ongoing numerical tracker defined post-100
  Milestone: OPEN — no visible distant target exists
  Narrative: OPEN — Familiar arc depth stages not mapped to cycles

Open items: Challenge 1 FAIL — elder game goals missing.
  Content horizon ends at cycle 100 with no subsequent goals designed.
  Flag as OPEN until three simultaneous goal types are defined.
```

**Example 2 — Onboarding sequence with gate validation**

Mechanic introduction order for a project with mana as sole currency:

```
PROGRESSION DESIGN OUTPUT — Onboarding sequence

Content horizon map:
  Session 1 → core mechanic introduced, 1 generator unlocked
  Session 2 → second mechanic visible (gated), Familiar introduced
  Cycle 10 → first upgrade tier available

Elder game threshold: requires Step 1 completion across all categories

Elder game goal coverage:
  Numerical: mana accumulation (no cap — ongoing)
  Milestone: Custodian Tier I at cycle 100 (LOCKED)
  Narrative: Familiar arc depth stage 2

Open items: Challenge 2 — mana gate at upgrade tier requires rate validation.
  Flag to IDLE-MATH domain: confirm cycle estimate at current mana rate.
```

---

## ADVERSARIAL SELF-REVIEW

Run these challenges before delivering any progression design output.

**Challenge 1 — Elder game coverage**
FAIL: Output covers cycle 1–100 in detail but elder game goals are "TBD"
or omitted entirely.
FIX: If elder game goals cannot be designed (content horizon unknown), state
this explicitly as OPEN with the specific blocker named. Do not deliver an
output that treats cycle 100 as the endpoint.
Severity: HIGH.

**Challenge 2 — Gate interaction with economy**
FAIL: A gate requires X mana to reach, but the mana rate at that cycle is
unknown — so the gate may be hit in 5 minutes or 5 weeks.
FIX: Any gate with a currency threshold must flag this to the IDLE-MATH
domain for rate validation. If D-026 (mana rates) is OPEN, flag it rather
than inventing a number.
Severity: HIGH.

**Challenge 3 — False floor check**
FAIL: A milestone or content threshold is reached with no visible "what's
next" signal at that exact moment. The player sees the milestone resolve
(achievement pops, cycle counter ticks), then the screen returns to the
idle state with nothing new flagged as available. Even if more content exists
downstream, the player cannot see it — they interpret the silence as done.

```
FAIL example:
Cycle 100 achievement fires: "Custodian Tier I — 100 Cycles Complete."
After the pop, the screen returns to the Dreaming idle state.
No new goal, track, or unlock is surfaced.
Player opens the achievement list — all visible achievements are complete.
Player closes the app. Session ends.
(More content exists at cycle 150, but nothing made it visible at cycle 100.)
```

FIX: For every major milestone in the content horizon map, verify that
at the moment of milestone resolution, at least one new goal becomes
explicitly visible to the player — a next achievement, an unlock hint,
a Familiar line, a new exchange option, or a visible progress tracker.
If no content is designed for that "next" moment, flag it as a false
floor and log as OPEN with the milestone named.
Severity: HIGH — false floors are the primary cause of elder game dropout
in idle games. A false floor at the pay gate is a retention disaster.

**Challenge 4 — Velocity calibration**
FAIL: Progression gates are timed in cycles, sessions, or real-world hours
without reference to a calibrated progression rate. Stated thresholds are
guesses that may be wildly off for actual players.

```
FAIL example:
"Cycle 30 — first upgrade tier available."
Cycle 30 requires 30 completed cycles.
If a cycle takes 1 minute active + idle generation, cycle 30 = ~30 minutes.
If a cycle requires 50,000 mana and generation is 100/minute at cycle 1,
cycle 30 could take 8 hours of idle time.
The threshold "cycle 30" has no meaning without a mana rate anchor.
```

FIX: For any gate expressed in cycles, sessions, or real-world time,
verify there is a corresponding calibration in the IDLE-MATH domain.
A cycle-count gate without a known mana rate is uncalibrated. Uncalibrated
gates must be flagged to IDLE-MATH and listed as OPEN until validated.
Do not present cycle thresholds as calibrated when they are estimates.

If D-026 (mana rates) or equivalent is OPEN, all cycle-count gates are
unvalidated by definition — flag the entire content horizon map as
RATE-UNVALIDATED and note the blocking decision.
Severity: HIGH — uncalibrated gates produce either trivial progression
(players race through all content) or brick walls (players idle for days
with no visible progress), both of which kill retention.

**Challenge 5 — Parallel progression paths**
FAIL: The progression design creates a single mandatory linear sequence —
every player must complete A before B, B before C. This fails two ways:
(1) players who dislike or are blocked by A have no alternative path to
progress; (2) the elder game becomes a dead end when the linear sequence
ends with nothing branching.

```
FAIL example:
Unlock sequence: Fire → Air → Water → Earth → Custodian Tier I → [nothing]
This is a single path. A player who finds the Fire minigame tedious has no
alternative path. A player who completes all four elementals and Tier I has
no branch — they hit the endpoint simultaneously on all tracks.
```

FIX: Verify that at any major progression point, at least two distinct
activities are available simultaneously — different minigames, NPC
tracks, faction routes, elemental upgrade paths, or achievement categories.
This doesn't require fully parallel narratives — it requires that at no
point is there only one thing left to do.

For the elder game specifically: verify that when the "main sequence" ends,
at least two independent tracks remain active (e.g., Familiar arc + faction
renown + ongoing mana accumulation). If only one track remains, elder game
is effectively linear and will feel like a false floor when that track ends.

If only one path exists and alternatives are not yet designed, flag as OPEN
and name which categories need content before elder game is viable.
Severity: MEDIUM — linear-only progression becomes visible as a design flaw
in the elder game, not in early play. Players who reach it without alternatives
are typically invested and their disappointment is high-signal for reviews.

**Confirmation block — required before delivering any output:**
```
Adversarial review — progression:
  Challenge 1 — Elder game coverage: [confirmed present / OPEN: {blocker}]
  Challenge 2 — Gate interaction with economy: [rate-validated / flagged to IDLE-MATH / OPEN: D-026]
  Challenge 3 — False floor check: [next-goal visible at every major milestone / OPEN: {milestone name}]
  Challenge 4 — Velocity calibration: [cycle gates calibrated via IDLE-MATH / RATE-UNVALIDATED: {blocking D-ID}]
  Challenge 5 — Parallel progression paths: [≥2 simultaneous tracks at all major points / OPEN: {missing categories}]
  Fixes applied: [list or "none"]
```

**HARD FAIL:** MUST NOT deliver any progression design output before this block is produced and all challenges clear.
