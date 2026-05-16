# Cross-Domain Conflict Map

Loaded by persona-game-designer dispatcher for any multi-domain question.
Defines known interaction points between activated domain pairs and
resolution rules.

## Contents

- [BALANCE + PSYCHOLOGY](#balance--psychology)
- [IDLE-MATH + BALANCE](#idle-math--balance)
- [PROGRESSION + IDLE-MATH](#progression--idle-math)
- [BALANCE + PROGRESSION](#balance--progression)
- [Any domain + GDD](#any-domain--gdd)
- [MONETIZE + PSYCHOLOGY](#monetize--psychology)
- [LIVE-OPS + PSYCHOLOGY](#live-ops--psychology)
- [LIVE-OPS + IDLE-MATH](#live-ops--idle-math)
- [MONETIZE + PROGRESSION](#monetize--progression)
- [MONETIZE + IDLE-MATH](#monetize--idle-math)
- [Priority Rules](#priority-rules)

---

## Domain Pair Interactions

### BALANCE + PSYCHOLOGY

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Challenge design | BALANCE may recommend increasing difficulty (fun = mastery at edge); PSYCHOLOGY may flag this as Competence threat for Gardener audience | SDT check takes priority for audience-identified mechanics. Name the target player type first; set difficulty to their Competence ceiling, not the designer's. |
| Feedback frequency | BALANCE wants strong feedback on every meaningful action (juice); PSYCHOLOGY cautions against external pressure loops (autonomy threat) | Positive feedback = no conflict. Punitive feedback or streak mechanics require explicit SDT Autonomy check. Default to positive reinforcement. |
| Failure states | BALANCE requires readable failure states that teach; PSYCHOLOGY (cozy game contract) requires no-failure-state design | Check confirmed design constraints first (Loop: no-failure-state is LOCKED). If confirmed, BALANCE failure state check skips to "readability of sub-optimal outcomes" — player understands what to do better next time without progress loss. |
| Tutorial length | BALANCE wants players in loops as fast as possible (arc = consumed); PSYCHOLOGY wants first-session SDT satisfaction on all three needs | Compress tutorial to minimum. But verify PSYCHOLOGY first-session requirements are met before declaring tutorial complete. SDT requirement is non-negotiable for first-session retention. |

### IDLE-MATH + BALANCE

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Cost curve feel | IDLE-MATH produces mathematically correct cost curve (triangular default, 1.12 growth rate); BALANCE evaluates whether that curve produces the right emotional arc | Arc target named first. Idle-math validates the curve fits within the arc's pacing window. A "correct" curve that peaks too early or too late is a balance failure regardless of math. |
| Multiplier breakthroughs | IDLE-MATH requires 2–3 breakthroughs per session at calibrated intervals; BALANCE requires each breakthrough to feel like a step-change (not incremental) | Both constraints apply. Breakthrough timing is IDLE-MATH work; breakthrough feel is BALANCE work. Run both and verify the breakthrough timing matches the target emotional phase. |
| Variance and randomness | IDLE-MATH uses variable ratio schedules for engagement; BALANCE warns that high variance can produce frustration without readable cause | Variable ratio is correct. But if variance produces outcomes the player cannot attribute to their actions, add a readable signal (BALANCE Challenge 5). |

### PROGRESSION + IDLE-MATH

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Gate timing | PROGRESSION defines gates in cycles; IDLE-MATH defines cycle duration via mana rates | All cycle-count gates flagged RATE-UNVALIDATED until IDLE-MATH confirms the mana rate. PROGRESSION Challenge 4 mandates this check. Never present a cycle threshold as calibrated without IDLE-MATH validation. |
| Content horizon endpoint | PROGRESSION defines when all content is accessible; IDLE-MATH calculates how long that takes in real session time | Content horizon map must include real-time estimates, not cycle counts alone. Derive real time from IDLE-MATH session pacing before marking progression design complete. |

### BALANCE + PROGRESSION

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Elder game mechanic balance | BALANCE checks whether a mechanic remains meaningful in the elder game; PROGRESSION checks whether elder game has sufficient goals | These are complementary, not conflicting. Both must pass before elder game is considered designed. A mechanically meaningful elder game with no visible goals = PROGRESSION Challenge 1 fail. Meaningful goals with a mechanically solved system = BALANCE "boredom diagnosis" trigger. |
| Parallel paths | BALANCE wants decision space at every stage; PROGRESSION requires ≥2 simultaneous active tracks in elder game | Same constraint from different angles. Verify both: BALANCE for each track's decision quality, PROGRESSION for the count of simultaneous active tracks. |

### Any domain + GDD

| Interaction point | Rule |
|---|---|
| Design question + readiness check | GDD DoR audit cannot pass for a section that depends on unresolved domain questions. Run domain work first; flag open items; then run GDD audit. A section with OPEN domain items is L0 or L1 by definition — do not attempt L2 audit until domain items are resolved or explicitly deferred. |
| Value without formula | Any numeric value in a GDD section that was not validated by IDLE-MATH must carry ⚠ CALIBRATE: flag. GDD does not invent or confirm values — it audits whether they exist and are flagged appropriately. |
| Lore gap in GDD section | GDD does not fill lore gaps — flags as `[OPEN: lore — route to Lore Bible]`. Do not route to PSYCHOLOGY. Psychology covers player emotion, not in-world narrative explanation. |

### MONETIZE + PSYCHOLOGY

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Cozy contract compatibility | MONETIZE proposes a purchase touchpoint; PSYCHOLOGY must verify it doesn't violate the cozy contract (safety, abundance, no pressure) | Run PSYCHOLOGY cozy contract check on every proposed touchpoint before designing the purchase. FOMO-inducing, expiring, or obligatory purchases fail the check regardless of revenue potential. |
| Audience willingness to pay | MONETIZE needs to know whether the target audience will convert; PSYCHOLOGY holds the Architect/Gardener WTP profile | Women in the Architect/Gardener demographic have a 79% higher install-to-purchase rate than average. Design for reciprocity (player chooses to give), not extraction (player must pay). |
| Ethical monetization and Relatedness | MONETIZE designs purchase triggers; PSYCHOLOGY warns that monetizing the Familiar arc directly risks instrumentalizing the Relatedness bond | Familiar arc stages must not be directly gated behind payment. Cosmetics and supplements that express an existing bond are acceptable. Paying to unlock arc stages is not. |
| Supporter pack framing | MONETIZE designs supporter packs; PSYCHOLOGY frames the purchase as an expression of investment, not a transaction | Supporter pack copy must use "support the game" framing, not "get more content" framing. Reciprocity psychology is the conversion mechanism — the purchase is a gift, not a fee. |

### LIVE-OPS + PSYCHOLOGY

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| FOMO vs. cozy contract | LIVE-OPS uses limited-time events to drive engagement; PSYCHOLOGY (cozy contract) requires no-FOMO design | Non-expiring rewards are the resolution. Palia's Lunar Path (battle pass with no expiration date) is the reference implementation. If a reward expires, it violates the cozy contract. |
| Event urgency vs. Autonomy | LIVE-OPS creates urgency signals to drive returns; PSYCHOLOGY warns urgency threatens SDT Autonomy for Gardener players | Time-limited VISIBILITY is acceptable (the event is available for N weeks); time-limited EXCLUSIVITY is not (miss it and it's gone forever). Always-available in the future = cozy. Never-available again = FOMO. |
| Event complexity vs. Gardener | LIVE-OPS may introduce complex event mechanics for engagement; PSYCHOLOGY (Gardener type) requires events that don't add cognitive overhead to the base loop | Events must be BACKGROUND LAYERS on the existing loop, not new systems requiring planning or strategy. Milestone rewards earned while playing normally = cozy-compatible. New modes requiring dedicated sessions = Gardener-hostile. |
| Return trigger design | LIVE-OPS designs notification/return triggers; PSYCHOLOGY warns that obligation-based triggers (daily streaks, expiring rewards) frustrate Autonomy | Positive return triggers only: "something new is available for you" (discovery framing), not "you'll miss out if you don't log in" (loss framing). True Time NPC events should notify with invitation language, not deadline language. |

### LIVE-OPS + IDLE-MATH

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Event pacing and session economy | LIVE-OPS adds rewards to sessions; IDLE-MATH must verify event rewards don't break the economy or render upgrade costs trivial | Any event reward denominated in mana or premium currency must be validated against the IDLE-MATH session economy. An event that floods the player with mana collapses the cost wall. Reward in non-mana currencies (cosmetics, lore fragments) avoids this conflict. |
| Return cadence and DAU/MAU | LIVE-OPS designs event spacing; IDLE-MATH holds DAU/MAU benchmarks and return trigger architecture | True Time NPC windows should fire at 22–26 hour intervals (IDLE-MATH habit loop architecture). Event cadence should reinforce this rhythm, not compete with it. Multiple simultaneous return triggers fragment attention and reduce each one's signal strength. |
| Event multipliers and breakthrough feel | LIVE-OPS may offer mana multipliers or yield boosts during events; BALANCE/IDLE-MATH must validate these don't compress or skip breakthrough moments | Multiplier events must be calibrated to produce the same number of breakthrough moments per session, not more. An event that provides +50% mana compresses the session and eliminates the cost wall — it removes the breakthrough feel rather than enhancing it. |

### MONETIZE + PROGRESSION

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Cycle 100 gate and progression design | MONETIZE owns the $1.00 unlock at cycle 100; PROGRESSION defines what happens before and after that gate | The cycle 100 gate is a LOCKED progression anchor (D-011). MONETIZE designs the conversion moment; PROGRESSION ensures something visible unlocks simultaneously (false floor prevention applies). The gate must feel like a progression milestone, not a toll. |
| Post-gate monetization and elder game | MONETIZE designs post-v1 revenue; PROGRESSION must ensure elder game content isn't gated behind payment | Elder game goals (numerical, milestone, narrative) must remain achievable without additional purchases. Paid content (supporter packs, narrative supplements) is additive, not required for elder game progression to feel satisfying. |
| Supporter pack timing and progression milestones | MONETIZE places conversion touchpoints; PROGRESSION identifies the emotional peak moments | Supporter pack offers should surface at Familiar arc milestones — the highest-emotional-investment moments — not at arbitrary cycle intervals. Conversion trigger = peak Relatedness moment (PSYCHOLOGY) + visible progress achievement (PROGRESSION). |

### MONETIZE + IDLE-MATH

| Interaction point | Conflict | Resolution rule |
|---|---|---|
| Rewarded video and session economy | MONETIZE proposes rewarded video as revenue; IDLE-MATH must validate the mana reward doesn't break session pacing | Rewarded video reward must be sized at ≤10% of expected cycle mana income. It accelerates Trickle for one cycle — it does not skip the cost wall. If the reward is large enough to eliminate the mana-scarce phase, it undermines the loop structure. |
| D2C web shop and IAP parity | MONETIZE uses web shop to improve margins; no gameplay conflict, but pricing parity must be maintained | Web shop prices must equal in-app prices. Undercutting the in-app price violates platform agreements. The margin improvement comes from the fee difference, not from lower player-facing prices. |

---

## Priority Rules (when domains conflict on the same recommendation)

1. **Confirmed project decisions (LOCKED)** take priority over all domain recommendations. Do not override LOCKED decisions with domain advice — flag the conflict and present to user.
2. **SDT Autonomy** takes priority over balance difficulty increases when the target audience is identified as Gardener type.
3. **Idle-math rate validation** takes priority over progression gate estimates when D-026 (mana rates) is OPEN — gates are RATE-UNVALIDATED regardless of cycle count confidence.
4. **GDD DoR audit** takes priority over "the design feels complete" — if the section fails DoR, it is not production-ready regardless of design confidence.
5. **No-failure-state constraint (Loop LOCKED)** takes priority over balance failure state design — redirect to "readability of sub-optimal outcomes" as the substitute mechanism.
6. **Cozy contract** takes priority over MONETIZE and LIVE-OPS revenue optimization — a monetization touchpoint or live ops mechanic that violates the cozy contract (FOMO, urgency, obligation) is redesigned or removed, regardless of projected revenue gain.
7. **Reciprocity framing** takes priority over extraction framing in all MONETIZE decisions — every purchase must feel like a choice to give, not a fee to continue. If it cannot be framed this way, it is redesigned.
