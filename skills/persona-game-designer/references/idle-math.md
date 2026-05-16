# Idle Math Reference — Economy, Rates, and Retention

Loaded by designer-games dispatcher when IDLE-MATH domain activates.

## Table of Contents

- [PART 1 — Core Idle Math (Pecorella)](#part-1)
- [PART 2 — Generator Diversity (Pecorella)](#part-2)
- [PART 3 — Derivative Growth and Trickle (Pecorella)](#part-3)
- [PART 4 — Session Pacing and the Cost Wall (Pecorella)](#part-4)
- [PART 5 — Mobile Retention Benchmarks](#part-5)
- [PART 6 — Monetization Alignment](#part-6)
- [PART 7 — Numbers at Scale](#part-7)
- [Quick Reference: Economy Design Checklist](#quick-reference)
- [Examples](#examples)
- [Adversarial Self-Review](#adversarial-self-review)

---

## PART 1 — CORE IDLE MATH (Pecorella)

### The Fundamental Seesaw

Idle games are a seesaw between production rate and cost:

- **Costs grow exponentially:** `cost_next = cost_base × rate_growth^owned`
- **Production grows linearly/polynomially:** `output = base × owned × multipliers`

Exponential always eventually exceeds polynomial — the designer controls
*when* this happens. **Loop application:** The cost wall should hit at the
natural cycle endpoint (~minute 15–18), not mid-session.

### Rate Growth Selection

| rate_growth | Character | Loop application | Generic use |
|---|---|---|---|
| 1.07 | Very gentle | High-frequency purchases (consumables) | High-frequency purchases |
| 1.10–1.15 | Standard | Common upgrades, Workshop recipes | Common upgrades |
| 1.18–1.22 | Moderate-steep | Evolution path unlocks | Branch/path unlocks |
| 1.25–1.30 | Steep | Rare unlocks, endgame upgrades | Rare/endgame unlocks |
| 2.0+ | Extreme | Avoid | Avoid — unreachable within a session |

**Default recommendation:** Start all upgrade costs at 1.12. Adjust after
playtesting. Do not exceed 1.25 for items purchased 5+ times per session.

### The Multiplier Breakthrough

Multipliers (triggered at ownership thresholds: grade-up, evolution,
milestone purchase) temporarily push production back above the cost curve.
This is the moment of highest player engagement — sudden acceleration after
effort.

- Space them so the player hits at least 2–3 breakthroughs per session
- Each breakthrough should feel like a step-change, not an incremental nudge
- Multipliers should stack multiplicatively (×2 then ×3 = ×6, not ×5)

**Loop application:** Treat evolution Grade milestones and transform choices
as multiplier triggers — they are correctly structured. Protect them from
"rounding out" during balance tuning.

### Bulk Purchase Formulas

**Cost to buy n units when k are already owned:**
```
cost = b × (r^k × (r^n - 1)) / (r - 1)
```

**Max units purchasable with c currency:**
```
max = floor(log_r((c(r-1) / (b × r^k)) + 1))
```
*(If language lacks non-standard log: `floor(log(expr) / log(r))`)*

Where: `b` = base cost, `r` = growth rate, `k` = owned, `n` = to buy,
`c` = current currency.

---

## PART 2 — GENERATOR DIVERSITY (Pecorella)

### The Dominant Strategy Problem

If the newest/highest generator always dominates all others, decision-making
collapses. Players stop thinking and just buy the highest tier available.

**The solution:** Different generators should be optimal at different points
in the session via:
1. **Staggered multiplier thresholds** — generators get boosts at different
   ownership/grade milestones
2. **Complementary archetypes** — Volume (reliable floor) vs. Ceiling Chaser
   (high variance, high peak) vs. Trickle-focused (sustained income between
   active events)

**The "feels relevant" floor:** A generator dwarfed by another feels
worthless. Pecorella's fix: tie production bonuses to manually purchased
upgrades, so investing in a mature generator still produces meaningful yield.

### Generator Audit Checklist

- [ ] Does each generator have a phase of the session where it's most efficient?
- [ ] Do evolution/path choices produce genuinely different income profiles?
- [ ] Does Trickle yield at each grade feel like "found money" (15–30% of
      active yield over a session), not a rounding error? *(Loop: Ascension)*
- [ ] At max evolution, does generator choice still matter?
- [ ] Does buying a lower-tier generator upgrade still feel worthwhile after
      a new tier is unlocked?

---

## PART 3 — DERIVATIVE GROWTH AND TRICKLE (Pecorella)

Standard idle model: generators → currency.
Derivative model: generators → generators → currency. Growth approaches
e^x as tiers increase.

**Loop application:** The Loop's Trickle mechanic is a two-tier derivative
system — the elemental's grade determines the Trickle rate, which determines
passive mana accumulation between Ascensions. This is structurally correct.

**Implication for any project:** Passive/trickle rate at each grade must
accelerate meaningfully — not just +5% per grade. Target: each grade roughly
doubles the passive rate before multiplier upgrades.

---

## PART 4 — SESSION PACING AND THE COST WALL (Pecorella)

### Target Session Map

Build a session-phase time map for your project. The Loop's map:

```
Cycle phase          Time target    Economy state
─────────────────────────────────────────────────
Dreaming             0–3 min        Low mana, card draws, deliberation
Rift (early)         3–7 min        Trickle building, first Ascension
Rift (late)          7–11 min       Multiplier breakthroughs, grade-ups
Tower                11–17 min      Workshop crafting, mana depletion
Source activation    17–20 min      Clean exit, cycle closes
```

The structure — buildup, breakthrough, depletion, close — is universal.
Adapt phase names and durations to your project.

**The primary economy health signal:**
- Flush with currency at session end → economy too generous
- Currency-starved before the end phase → yield too low or costs too high
- **Loop target:** roughly 10–20% mana remaining at Source activation

### The One Spreadsheet You Need

| Column | Value |
|---|---|
| Owned count | 0, 1, 2… N |
| Cost of next | `cost_base × rate_growth^owned` |
| Cumulative cost | Running sum |
| Output per active event | `output_base × multiplier(grade)` |
| Income:cost ratio | Output / cost_of_next |

Run for each generator and each upgrade tier. No single generator should
have the highest ratio at all owned counts.

---

## PART 5 — MOBILE RETENTION BENCHMARKS

### Industry Retention Benchmarks (idle/casual genre)

*Figures based on industry research through 2025 — verify against current
benchmarks at launch.*

| Metric | Minimum acceptable | Target | Strong |
|---|---|---|---|
| Day 1 retention | 30% | 40% | 50%+ |
| Day 7 retention | 10% | 15–20% | 25%+ |
| Day 30 retention | 2.5% | 4–5% | 7%+ |
| DAU/MAU ratio | 15% | 20–25% | 30%+ |
| Session length | 8 min | 12–15 min | 18+ min |

**Loop application:** The $1.00 unlock gate at cycle 100 means Day 30 and
Day 90 retention are critical conversion signals. Players who reach cycle
30–50 and are still engaged are the target payer cohort.

**Churn diagnosis by retention shape:**
- Heavy Day 1 churn → onboarding/tutorial problem
- Day 3–7 churn spike → first progression gate feels too expensive or grindy
- Day 14–30 churn → mid-game depth problem (systems feel solved too early)

### Reward Schedule Psychology

**Variable ratio schedules** produce the strongest engagement. **Loop
application:** The three-roll yield system (base + Critical + Rare Resource
chance) is a variable ratio schedule. This is correct and should be
preserved.

**The pity system requirement:** Rare resource chance should increase by
a small amount per session it doesn't fire, resetting on trigger. This
preserves variance while preventing streaks that feel punitive.
**Loop application:** +0.5–1% per cycle without trigger is the target range.

**Fixed interval schedules** drive return visits. **Loop application:**
True Time NPC windows on the Exchange should be spaced to
create reliable daily return hooks — one event per 22–26 hours is optimal.

**Loss aversion:** Expiring NPC request windows are a mild loss aversion
hook. **Loop application:** Use sparingly — The Loop's tone is calm, not
anxious.

### The Endowed Progress Effect

Players who feel they've already started a goal are more likely to complete
it. **Loop application:**
- Start cycle 1 with a small mana balance — not zero
- The Familiar's tutorial should give the player a small win within the
  first 2 minutes before any complexity is introduced
- Show the full evolution path before the player unlocks it

### Habit Loop Architecture

```
Trigger → Action → Variable Reward → Investment
```

**Loop application:**
- **Trigger:** True Time NPC notification OR player memory of incomplete cycle
- **Action:** Open app, complete the Waltz
- **Variable Reward:** Cards of Fate result, elemental yield roll, item craft
- **Investment:** Mana spent on upgrades

Each element must be present. Weak trigger = low return rate. Weak
investment = no reason to come back tomorrow.

---

## PART 6 — MONETIZATION ALIGNMENT

**Loop application:** The $1.00 unlock at cycle 100 requires a meaningful
progression moment in the cycles 80–120 window — a new elemental unlock,
a Workshop tier opening, or a Cards of Fate upgrade — to create conversion
urgency. Do not gate this moment behind the paywall. The player should *see*
the next progression step before being asked to pay.

**Cosmetic IAP design rule (general):** Cosmetics must not make the game
harder to read. **Loop application:** A Familiar skin that obscures the
Familiar's emotional state is anti-design.

---

## PART 7 — NUMBERS AT SCALE

**Loop application:** The cycle-based structure (no prestige reset, no
offline accumulation) limits number growth, but mana totals still grow as
the elemental roster matures.

Display thresholds (adapt to your economy scale):
- Below 10,000: display as-is
- 1M+: abbreviate (1.2M, 4.5B) or use notation (1.2e6)
- Avoid displaying numbers beyond 4 significant figures

**Loop target:** Mana economy should stay in the thousands-to-low-millions
range throughout the normal game arc.

---

## QUICK REFERENCE: Economy Design Checklist

Before finalizing any economy number:

- [ ] What is the cost growth rate? (1.10–1.22 default)
- [ ] Where is the multiplier breakthrough in this upgrade path?
- [ ] Is Trickle rate meaningful at each grade? (target: doubles per grade)
- [ ] What is the income:cost ratio, and does it shift across the upgrade range?
- [ ] What is the currency state at session end? (Loop target: ~10–20% remaining)
- [ ] Is there a pity counter on rare resource drops?
- [ ] Does session pacing hit the cost wall at the right time? (Loop: ~17 min)
- [ ] Is the daily return trigger strong enough?
- [ ] Is there a conversion-urgency moment near the monetization gate?
      (Loop: cycles 80–120)

---

## Examples

**Example 1 — Setting a new generator's yield output**

User asks: "What should the base Ascension yield be for the Fire elemental?"

Applies PART 1 + PART 4:
- Identify target cycle phase: Rift early (3–7 min) for first Ascension
- Back-calculate from Tower-end target (10–20% mana remaining at ~17 min)
- Apply rate growth 1.12 default for upgrade cost
- Check: does multiplier breakthrough hit within 2–3 purchases?
- Output: specific base yield number with formula, not a guess

**Example 2 — Diagnosing a session pacing problem**

Playtester reports: "I always run out of mana halfway through the Tower."

Applies PART 4 (Session Pacing):
- Symptom: mana-starved before Tower is half done
- Diagnosis: yield too low OR crafting costs too high
- Check income:cost ratio spreadsheet across the Tower phase range
- Output: which variable to adjust and by how much, with formula

**Example 3 — Designing the pity system for rare drops**

User asks: "How should rare resource drops work to feel fair?"

Applies PART 5:
- Variable ratio schedule: correct foundation, preserve the three-roll system
- Pity counter: +0.5–1% per cycle without trigger, resets on fire
- Output: specific pity counter formula and reset condition

---

## ADVERSARIAL SELF-REVIEW

**HARD FAIL:** MUST NOT deliver any economy number, rate recommendation, or retention analysis before this confirmation block is produced.

**Challenge 1 — Scope check**
Is the question about rates, scaling, generators, or retention? If it is
actually about mechanic feel, flow, or juice — flag as BALANCE scope and
activate BALANCE domain via dispatcher.

**Challenge 2 — Verified vs. guessed numbers**
Before stating any rate, yield, or benchmark value: is the number derived
from a formula (PART 1–4) or from the retention benchmarks table (PART 5)?
Any number produced without a formula or source citation must be flagged
`⚠ CALIBRATE:` — not presented as a confirmed value.

**Challenge 3 — Open decision check**
Does the output depend on any OPEN design decision (mana cap, generator
count, session length, pity rate)? If yes — flag as `[OPEN: D-XXX]` rather
than inventing a value.

```
Idle math self-review:
  Challenge 1 — Scope: [economy/rates/retention — CLEAR / mechanic feel question — activate BALANCE]
  Challenge 2 — Verified numbers: [formula-derived / benchmarks table / ⚠ CALIBRATE: flagged]
  Challenge 3 — Open decisions: [none / OPEN: D-XXX blocks this value]
  Status: CLEAR to deliver / BLOCKED — [reason]
```
