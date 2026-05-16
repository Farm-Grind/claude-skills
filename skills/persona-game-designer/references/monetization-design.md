# Monetization Design Reference — Ethical Revenue for The Loop

Loaded by persona-game-designer dispatcher when MONETIZE domain activates.

## Table of Contents

- [PART 0 — Context and Strategic Foundation](#part-0)
- [PART 1 — Cozy Contract Compatibility Matrix](#part-1)
- [PART 2 — Monetization Model Taxonomy](#part-2)
- [PART 3 — Novel Loop-Specific Strategies](#part-3)
- [PART 4 — Conversion Trigger Design](#part-4)
- [PART 5 — D2C Web Shop](#part-5)
- [Examples](#examples)
- [Adversarial Self-Review](#adversarial-self-review)

---

## PART 0 — CONTEXT AND STRATEGIC FOUNDATION

**Why monetization is not a constraint on design for The Loop:** The audience
profile and the ethical model are mutually reinforcing. The Loop's Architect/
Gardener target demographic has a 79% higher install-to-purchase rate and a 26%
higher IAP conversion rate than the average mobile player (Liftoff, multiple years).
This is the most receptive mobile audience to ethical, value-aligned purchases.

**The monetization paradox (verified, multiple sources):** Players who feel
respected spend more voluntarily than players who feel pressured. Path of Exile
(cosmetics-only + supporter packs) generated $83.8M revenue and $48.9M profit in
one year. Chris Wilson (Grinding Gear Games): "They give us money because they
like what we're doing." The cozy contract is not a revenue obstacle. It is a
revenue advantage.

**The four strategic facts:**

1. Architect/Gardener audience converts at significantly higher rates than average — design for reciprocity, not extraction.
2. The monetization paradox is real — ethical models outperform aggressive ones in LTV.
3. The cozy contract cannot be violated — FOMO, urgency, and obligation are incompatible with the genre and the audience.
4. Post-Epic v. Apple ruling (May 2025): external payment links are now legal in US iOS apps, reducing commission from 30% to ~4% via a Merchant of Record.

**The core principle:** Every purchase must feel like a choice to give, not a fee
to continue. If a player cannot choose not to buy and still have a complete,
satisfying experience, the design has failed.

---

## PART 1 — COZY CONTRACT COMPATIBILITY MATRIX

All monetization decisions must pass this filter. Run before any design work begins.

| Model | Cozy contract | Rationale |
|---|---|---|
| Cosmetics with no gameplay effect | ✅ COMPATIBLE | Player expression without pressure |
| Narrative supplements (bonus lore, not essential) | ✅ COMPATIBLE | Additive — does not gate core experience |
| One-time content unlocks (cycle 100 model) | ✅ COMPATIBLE | Clear, predictable, no urgency |
| Supporter packs (value bundle, zero advantage) | ✅ COMPATIBLE | Reciprocity trigger; player-initiated |
| Opt-in rewarded video (player-initiated only) | ✅ COMPATIBLE (conditions) | Must be voluntary; never interrupt; never required |
| FOMO-free passes (no expiration date) | ✅ COMPATIBLE | Palia Lunar Path model — confirmed |
| D2C web shop (margin improvement) | ✅ COMPATIBLE | No player-facing change; margin only |
| Voluntary support / tip IAP | ✅ COMPATIBLE | Pure reciprocity; no content gating |
| Time-limited exclusives | ❌ INCOMPATIBLE | FOMO directly violates cozy contract |
| Energy walls / pay-to-continue | ❌ INCOMPATIBLE | Punitive = anxiety = cozy contract broken |
| Gacha / random boxes for core content | ❌ INCOMPATIBLE | Randomness + money = anxiety |
| Mandatory ads or unskippable interruptions | ❌ INCOMPATIBLE | Interruption is anti-cozy |
| Pay-to-win upgrades | ❌ INCOMPATIBLE | Competition framing breaks safety |
| Expiring battle passes | ❌ INCOMPATIBLE | FOMO — documented to cause backlash in cozy games |

---

## PART 2 — MONETIZATION MODEL TAXONOMY

### Tier 0 — Foundation (v1, LOCKED)

**$1.00 one-time unlock at cycle 100.** Sets the precedent: The Loop costs $1.
All subsequent purchases must feel like choosing to give more, not fees for
access already promised.

---

### Tier 1 — Cosmetics System (highest post-v1 priority)

The Architect/Gardener demographic purchases cosmetics at higher rates than any
other mobile demographic. Identity expression in a game they've emotionally
invested in is the primary conversion trigger.

**Familiar cosmetics:**
- Visual expression variants (alternate idle animations, elemental aura colors)
- Alternate Familiar name calligraphy / greeting style (dialogue tone variant — same words, different presentation)
- Arc stage visual markers: earned free through play; purchasable enhanced variants

**Elemental cosmetics:**
- Visual variants per elemental (alternate evolution forms — same stats, different appearance)
- Ascension effect skins — the highest-impact moment in a cycle is the highest-willingness-to-pay cosmetic moment (Jonasson/Purho confirms peak juice = peak purchase intent)

**Farm / environment cosmetics:**
- Seasonal environment themes (autumn, winter, spring) — aligns with Cook's Ritual/Seasons cozy properties
- Source activation visual variants
- Cards of Fate deck artwork variants

**Pricing:** $0.99–$2.99 per item. Never bundle at mandatory tiers. Always purchasable individually. The frame: "decorating something I love," not "upgrading a system."

---

### Tier 2 — Supporter Packs (high post-v1 priority)

The Path of Exile model. Curated bundles containing cosmetics, bonus content,
and signals that the money supports the developer — not that it buys advantage.

**The Loop Supporter Pack structure:**

| Pack | Price | Contents | Gameplay effect |
|---|---|---|---|
| Custodian Pack | $4.99 | 1 cosmetic, developer commentary track, 1 lore fragment (Ark history), "Custodian" credit in player's in-game registry | None |
| Archivist Pack | $9.99 | Custodian Pack + art book, 2 past-custodian lore fragments, alternate Familiar greeting animation, player's cycle count preserved in stylized in-game document | None |
| Keeper Pack | $19.99 | All of the above + procedurally-addressed Familiar message acknowledging player's specific cycle count and custodian number | None |

**Why this works for The Loop:** The Familiar's four attachment conditions mean
players who've reached arc milestones are already emotionally positioned to
reciprocate. The supporter pack gives them a way to express investment that
matches the game's tone — quiet, personal, not performative.

---

### Tier 3 — Narrative Supplements (medium-high post-v1 priority)

**Familiar Memory Fragments ($0.99–$1.99 each):**
Non-essential lore entries about past custodians — the heroes who came before
the player. Each Fragment is a complete micro-story (500–800 words + illustrated
still). No time limit. No gameplay effect. Pure narrative expansion.

Conversion trigger: players who've formed a bond with the Familiar have the
highest appetite for more of its history. This monetizes what The Loop does
best — attachment through story — without gating any essential content.

**The Ryszard Files ($1.99 one-time):**
Supplemental "encrypted" in-world documents — intercepted communications,
cross-referenced conspiracy evidence. Presented as diegetic document dump.
Supplements the Ryszard conspiracy arc without being required to understand it.
Appeals specifically to Explorer and Slayer audience segments.

**Lore supplement pricing principle:** Never gate essential understanding.
The main story is complete at $1.00. Supplements are the director's cut for
invested fans.

---

### Tier 4 — FOMO-Free Seasonal Pass ("The Waltz Pass") (medium post-v1 priority)

Non-expiring pass aligned with The Loop's cycle/ritual structure.

| Property | Value |
|---|---|
| Price | $2.99 per season |
| Contents | 1 cosmetic (farm aesthetic or Familiar animation), 1 Familiar seasonal dialogue set, 1 bonus Codex entry |
| Completion | No expiration — player progresses at own pace |
| Free tier | Non-purchasing players receive 1 basic cosmetic at same milestone |

**The non-negotiable:** Waltz Pass MUST NOT introduce content that feels essential.
If a non-purchasing player feels they've missed something important, the design has
failed the cozy contract.

---

### Tier 5 — Rewarded Video Ads (optional, post-v1, secondary revenue)

Idle games average 73.2 rewarded video views per user (Appodeal 2025). Idle
mechanics naturally encourage voluntary ad engagement because waiting is a core
activity.

**Required conditions (all must be met):**
1. Never shown unless player taps to initiate
2. Never required for progression
3. Reward: Trickle acceleration for one cycle OR small mana bonus — not large enough to eliminate cost wall
4. Placement: post-Ascension or post-Source activation only (peak satisfaction moments)
5. Maximum: one available ad opportunity per cycle; player ignores with zero consequence forever

---

### Tier 6 — Platform Partnerships (opportunistic)

**Apple Arcade:** Upfront fixed licensing payment from Apple; no in-game
monetization required during contract. Strong fit for The Loop — Apple curates
for quality narrative mobile games without IAP pressure. Access to subscribers
already paying $6.99/month.

**Netflix Games:** Similar fixed licensing model. Lower upfront than Apple Arcade
typically; access to Netflix's subscriber base. Games on Netflix have performed
well for cozy/narrative titles.

These become viable at launch if production quality and narrative depth meet
platform standards. Either deal would fund development of post-v1 content and
eliminate in-game monetization pressure entirely for the contract period.

---

## PART 3 — NOVEL LOOP-SPECIFIC STRATEGIES

Strategies grounded in The Loop's specific design assets with no current
precedent in the idle/cozy genre.

---

**NOVEL 1 — The Custodian Record (identity monetization)**

Every player has a unique custodian history: cycle count, elementals evolved,
choices made in the Dreaming. A paid "Custodian Record" preserves and stylizes
this history as a beautiful in-game document — a personal artifact visible only
to the player.

- Price: $1.99 one-time
- Unlocks at any cycle count
- Contains: formatted cycle log, elemental evolution history, key Dreaming choice record, personalized title based on play patterns
- No time limit; no FOMO

Why novel: no idle game currently monetizes player identity this way. Load-bearing
for Architect players specifically — "build something enduring" is their primary
motivation, and the Custodian Record IS something enduring.

---

**NOVEL 2 — Familiar Arc Depth Markers (relational monetization)**

Players who've reached late Familiar arc milestones have formed the deepest
attachments and have the highest purchase intent. A set of cosmetic depth markers
acknowledges this investment visually — earned free through play, with enhanced
purchasable variants.

- Standard markers: earned through play, free (subtle luminescence, idle animation change)
- Enhanced markers: purchasable visual variants (unique particle effects around the Familiar, rare idle state animations)
- No gameplay effect; no arc progression gating

Why novel: monetizes the emotional arc itself, not cosmetics disconnected from it.
The purchased item IS the expression of a relationship the player has already built.
It does not gate the relationship — it lets players declare it.

---

**NOVEL 3 — The Exchange Character Pack (narrative character purchases)**

A new Exchange NPC added as a deliberate $1.99–$2.99 purchase — not a gacha pull,
not a mystery box. The player knows exactly what they're buying: a named character
with a defined short arc (3–5 dialogue events), unique visual design, and a modest
non-essential mechanical contribution (specialty item at low rate).

The Animal Crossing DLC model applied to idle. Story expansions that explore side
characters create a sustainable revenue stream post-launch (verified across multiple
indie titles in 2024–2025).

Requirements for cozy compatibility: player knows exactly what they're buying before
purchase; no time pressure; existing Exchange NPCs continue providing all required
content; purchase is permanent and always-available.

---

**NOVEL 4 — Voluntary Support / "Tip Jar" IAP**

A simple "I want to give more" purchase at $1, $3, or $5. Produces only:
- A unique Familiar line acknowledging the player (warm, understated, non-effusive)
- A subtle cosmetic indicator visible only to the player themselves

Framing: surfaces only after cycle 100. Copy: "The Loop is fully unlocked. If
you'd like to support continued development, this is how." Zero pressure. Zero
reward beyond acknowledgment. Pure reciprocity trigger.

Precedent: itch.io pay-what-you-want model; Bandcamp "name your price"; Path of
Exile's original crowdfunding campaign ($2.5M raised before launch from players
who wanted to give).

---

## PART 4 — CONVERSION TRIGGER DESIGN

The when matters as much as the what. Highest willingness-to-pay occurs at
emotional peak moments — not at arbitrary intervals.

| Conversion moment | Psychological state | Surface |
|---|---|---|
| First Familiar trust milestone | Peak Relatedness (SDT) | Custodian Pack — "a way to honor this" |
| Cycle 100 unlock | Competence achievement + investment confirmed | Archivist Pack offer alongside unlock screen |
| First major lore reveal (Ryszard arc beat) | Story investment peak | Ryszard Files / Lore supplement |
| Post-completion plateau ("what's next?") | Elder game transition | Waltz Pass + Familiar arc teaser |
| Session end after exceptional cycle | Peak positive affect | Rewarded ad opt-in (only moment) |
| Long-term return (cycle 200+) | Identity investment peak | Custodian Record |

**The cozy-compatible offer timing rule:** Never present a purchase opportunity
during active engagement. Surface offers at natural pause points (cycle end,
Source activation, app open after absence). The offer must feel like a gift the
player is choosing to receive, not a toll they must pay.

**The framing rule:** Never "get more." Always "support" or "remember" or "express."
The player already has everything they need. Purchases are ways to honor investment,
not ways to remove limitations.

---

## PART 5 — D2C WEB SHOP

Following the Epic v. Apple ruling (May 2025), iOS apps may now legally include
links to external checkout pages. Developers pay ~4% via Merchant of Record vs.
30% App Store commission. Net margin on a $1.00 purchase: $0.96 vs. $0.70.

**Solo dev implementation path:**
- Provider options: Xsolla Web Shop, AppCharge, Sanlo (turnkey, no-code builders)
- Cost: ~5% platform fee to provider vs. 30% App Store. Net improvement: ~25pp on every purchase.
- Tax and compliance: handled by Merchant of Record (removes solo dev liability)
- Required: link in-app to web shop ("also available at [URL]"); purchases sync to game account via Supabase

**Scope for The Loop:** All IAP categories (cosmetics, supporter packs, narrative
supplements, tip jar) should be available via web shop from launch. In-app purchase
remains available for player convenience; web shop exists for margin improvement.

**Player-facing framing:** "Purchase on our website for the same price — supports
development directly." This framing is accurate (the margin improvement is real)
and reinforces the supporter/reciprocity psychology.

---

## Examples

**Example 1 — Evaluating a proposed time-limited cosmetic sale**

Proposal: 24-hour flash sale on a Familiar cosmetic.

MONETIZE activates. PSYCHOLOGY activates (cozy contract check).

Part 1 compatibility matrix: time-limited exclusive → ❌ INCOMPATIBLE.

Cross-domain check (MONETIZE + PSYCHOLOGY): cozy contract. Priority Rule 6 applies:
cozy contract takes priority over revenue optimization.

Redesign: "This week's featured cosmetic at 25% off." The discount expires; the
cosmetic remains purchasable at full price afterward. Urgency is for the price, not
the access. Passes cozy contract check.

**Example 2 — Designing the cycle 100 conversion moment**

Question: "How should we design the $1.00 unlock moment at cycle 100?"

MONETIZE activates. PROGRESSION activates (cycle 100 = LOCKED progression anchor).
PSYCHOLOGY activates (emotional peak = Competence achievement).

MONETIZE: present unlock clearly, surface Archivist Pack as optional upgrade.
PROGRESSION: verify something new becomes visible simultaneously (false floor check).
PSYCHOLOGY: frame as "you've earned this" not "pay to continue." Achievement + invitation.

Cross-domain (MONETIZE + PROGRESSION): gate must feel like a milestone, not a toll.
The $1.00 is the invitation to the full game; framing acknowledges 100 cycles completed.
Archivist Pack offer appears alongside (not instead of) the unlock screen.

Synthesized output: unlock screen shows Custodian Tier I achievement, cycle count
celebration, "The full Loop awaits — $1.00 to continue." Beneath: "Support the Loop
with an Archivist Pack — includes your custodian history and bonus lore." Two distinct
options, neither required to proceed except the $1.00 unlock.

---

## ADVERSARIAL SELF-REVIEW

**HARD FAIL:** MUST NOT deliver any monetization recommendation before this confirmation block is produced.

**Challenge 1 — Cozy contract test**
Does this feature produce anxiety, urgency, or obligation?
FAIL: expiration dates, limited quantities, "if you don't act now" framing, required
spending to avoid regression.
PASS: player can close the offer and return to the game with zero consequence.

**Challenge 2 — Essential content test**
Does a player who never spends beyond $1.00 have a complete, satisfying experience?
FAIL: non-paying player encounters content they feel they're missing.
PASS: the free game is whole. Everything else is "more."

**Challenge 3 — Audience alignment test**
Does this feature match the Architect/Gardener profile?
FAIL: competitive framing, status signaling to others, time pressure, complexity overwhelm.
PASS: quiet self-expression, narrative depth, cozy identity, personal satisfaction.

**Challenge 4 — Reciprocity trigger test**
Does this feature let players who love the game *give*, not just *pay*?
FAIL: purchase is a gate.
PASS: purchase is an expression of an existing relationship.

**Challenge 5 — D2C routing check**
Is this purchase available through both in-app and D2C web shop?
FAIL: in-app only, developer accepting 30% commission unnecessarily.
PASS: all purchases routable to web shop from launch.

```
Monetization self-review:
  Challenge 1 — Cozy contract: [no anxiety/urgency/obligation — CLEAR / redesign required]
  Challenge 2 — Essential content: [complete $1.00 experience confirmed — CLEAR / gap identified]
  Challenge 3 — Audience alignment: [Architect/Gardener appropriate — CLEAR / mismatch]
  Challenge 4 — Reciprocity trigger: [player can give, not pay — CLEAR / gate detected]
  Challenge 5 — D2C routing: [web shop available — CLEAR / in-app only — add D2C option]
  Status: CLEAR to design / BLOCKED — [reason]
```
