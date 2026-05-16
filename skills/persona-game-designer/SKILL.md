---
name: persona-game-designer
description: >
  Covers mechanic feel, player psychology, economy math, progression
  sequencing, documentation completeness, monetization design, and live
  ops design. Dispatches to relevant sub-domains simultaneously for any
  game design question. Use automatically — do not wait to be asked.
  Trigger on ANY of these signals: a mechanic is being designed, balanced,
  or evaluated; "will this be fun", "will players care", "how should this
  feel", "what's the cost curve", "what unlocks when", "is this progression
  right", "is this spec complete", "what does the player do after X"; any
  new system, generator, upgrade, NPC arc, or achievement is discussed;
  monetization or IAP design discussed; live ops or event design discussed;
  a GDD readiness question is raised. Do NOT trigger for: lore canon
  (loop-extended-lore-checker); code generation (loop-extended-code-
  guardian); visual direction (loop-extended-visual); audio design
  (suno-prompter, loop-sfx-designer); UI layout (loop-mobile-ux). Load
  once per session.
---
SKILL_VERSION: v1.1

# Game Designer — Multi-Domain Dispatcher

Covers any game design question across mechanic feel (BALANCE), player
psychology (PSYCHOLOGY), economy math (IDLE-MATH), progression sequencing
(PROGRESSION), documentation completeness (GDD), monetization design
(MONETIZE), and live ops design (LIVE-OPS). Routes each question to the
relevant domain(s), activates multiple simultaneously when needed, and
synthesizes integrated output.

Replaces: utility-game-balance, utility-game-psychology, utility-game-idle-math,
utility-game-progression, utility-game-gdd-enforcer.

Type: dispatcher

---

## GOTCHAS

1. **Routing to one domain when the question spans several** — intake classification catches this; never skip it on "obvious" questions. A "fun" question always requires BALANCE; it often requires PSYCHOLOGY; if it involves costs it requires IDLE-MATH. Run the full table.

2. **Loading reference files without reading them** — the `view` call must produce visible output before that domain's content is used. No output = running from memory = HARD FAIL. If a reference file is not in the current turn's context, re-issue `view`.

3. **Concatenating per-domain sections instead of synthesizing** — output with headers like "BALANCE FINDINGS:" and "PSYCHOLOGY FINDINGS:" as separate blocks is concatenation, not synthesis. Synthesis produces one integrated recommendation where cross-domain interactions are explicitly named and resolved.

4. **Declaring a domain activated but not loading its reference file** — domain declaration is the commitment to load and use that reference's content. If a domain code appears in the declaration block but its `view` call is missing, the domain is not actually active.

5. **Leaving reference files loaded past the synthesis output** — progressive disclosure should not become progressive accumulation. Once synthesis output is delivered, reference files from this question are spent. Do not carry them forward to the next question in the session unless the question explicitly continues the same topic.

---

## PART 0 — INTAKE CLASSIFICATION

Run before any reference file loads. Classify every question. Multiple domain
codes activate simultaneously when any row matches.

| Signal type | Object signals (any of these) | Domain codes | Example question |
|---|---|---|---|
| Feel / emotion / fun | mechanic, minigame, interaction, system, feedback, challenge, difficulty, frustration, boredom, flow, juice | BALANCE | "Will this feel rewarding?" |
| Emotional arc / design | phase, session, arc, emotional target, Dreaming, Rift, Tower | BALANCE | "Does this match the Tower's emotional tone?" |
| Player motivation / SDT | player (as person), autonomy, competence, relatedness, motivation, why players return | PSYCHOLOGY | "Will players care about this?" |
| Audience / profiling | audience, demographic, who plays, Architect, Gardener, Slayer, Explorer | PSYCHOLOGY | "Who would enjoy this mechanic?" |
| NPC / companion | Familiar, NPC, companion, relationship, attachment, parasocial, contingent | PSYCHOLOGY | "Does this Familiar line land correctly?" |
| Cozy / genre | cozy, safety, no-failure, psychological safety, genre fit | PSYCHOLOGY | "Does this match the cozy game contract?" |
| Rates / math / numbers | rate, cost, scaling, generator, yield, income, formula, mana, upgrade curve | IDLE-MATH | "What should the base yield be?" |
| Session pacing | session length, cost wall, breakthrough, depletion, pacing, Tower end | IDLE-MATH | "Why does the player run out of mana early?" |
| Retention metrics | Day 1/7/30, churn, DAU/MAU, pity, variable ratio, habit loop, unlock gate | IDLE-MATH | "Is our Day 7 retention target realistic?" |
| Unlock / sequencing | unlock, sequence, order, when does X appear, onboarding order, gate | PROGRESSION | "What should unlock first?" |
| Elder game | elder game, what after X, content endpoint, false floor, achievement vacuum | PROGRESSION | "What does the player do at cycle 200?" |
| Achievement calibration | achievement, Custodian tier, milestone threshold, completion horizon | PROGRESSION | "Is the Tier I threshold set correctly?" |
| GDD completeness | ready to implement, complete, stub, TBD, DoR, what's missing, production-ready | GDD | "Is this mechanic spec complete?" |
| GDD section audit | L0/L1/L2, unambiguous, verifiable, traceable, edge case, failure state | GDD | "Can a developer build from this section?" |
| Monetization design | IAP, in-app purchase, monetization model, revenue model, supporter pack, cosmetics store, pricing, willingness to pay, ethical monetization, pay-to-win, D2C, web shop, cozy monetization | MONETIZE | "What should we charge for this?" |
| Conversion design | conversion trigger, first purchase, paywall design, cycle 100 gate, spender cohort | MONETIZE | "How do we design the $1.00 unlock moment?" |
| Live ops design | live ops, event design, seasonal event, event calendar, update cadence, limited-time, FOMO-free, evergreen rewards, Waltz Pass | LIVE-OPS | "How should we structure seasonal events?" |
| True Time / NPC events | True Time, NPC window, exchange event, return trigger, event spacing | LIVE-OPS | "How do we design the True Time NPC windows?" |

**Multi-domain rules (activate both codes when ANY row in each code matches):**

| Combination | Trigger | Why |
|---|---|---|
| BALANCE + PSYCHOLOGY | "will players enjoy/love/care about this mechanic" | Feel questions have SDT implications |
| IDLE-MATH + BALANCE | "is this cost fair/right/fun" | Cost questions have emotional arc implications |
| PROGRESSION + IDLE-MATH | "is this gate correctly timed/reachable" | Timing gates require rate validation |
| BALANCE + PROGRESSION | "does this work in the elder game" | Elder game balance requires content horizon |
| Any domain + GDD | "is this [domain topic] ready to spec/implement" | Completeness check on any design topic |
| MONETIZE + PSYCHOLOGY | "is this purchase cozy-compatible" or "will our audience pay for this" | Cozy contract and audience WTP are psychology questions |
| LIVE-OPS + PSYCHOLOGY | "will this event create FOMO" or "is this live event cozy-compatible" | FOMO vs. cozy contract is a documented design conflict |
| LIVE-OPS + IDLE-MATH | "how does this event affect retention" or "event pacing and session length" | Event cadence has direct retention metric implications |
| MONETIZE + PROGRESSION | "where does the $1.00 gate fit in progression" or "monetization gate design" | Cycle 100 gate is a progression anchor that requires both domains |
| MONETIZE + IDLE-MATH | "rewarded ad mana bonus" or "does this purchase affect the economy" | Reward-for-purchase mechanics must be validated against session economy |

---

## PART 1 — DOMAIN DECLARATION

After running PART 0, produce this block (visible to user):

    DOMAINS ACTIVATED: [code1] [+ code2] [+ code3]
    Reference files to load: [list exact paths]
    Question type: [single-domain / multi-domain]
    Cross-domain check required: [yes — load cross-domain-map.md / no]

HARD FAIL: Deliver any output before this block appears = gate failure.
The declaration is not internal — it is the commitment to load and use the
named reference files.

---

## PART 2 — REFERENCE FILE LOADING

Load each activated domain's reference file via explicit `view` call.
Confirm load with visible output before using any content from it.

| Domain code | File path | Load command |
|---|---|---|
| BALANCE | references/balance.md | `view references/balance.md` |
| PSYCHOLOGY | references/psychology.md | `view references/psychology.md` |
| IDLE-MATH | references/idle-math.md | `view references/idle-math.md` |
| PROGRESSION | references/progression.md | `view references/progression.md` |
| GDD | references/gdd-standards.md | `view references/gdd-standards.md` |
| MONETIZE | references/monetization-design.md | `view references/monetization-design.md` |
| LIVE-OPS | references/live-ops.md | `view references/live-ops.md` |
| Multi-domain (any combination ≥2) | references/cross-domain-map.md | `view references/cross-domain-map.md` |

HARD FAIL: Using any domain's content without visible `view` output for
that file in the current turn. Re-issue `view` if the file is not in context.

---

## PART 3 — DOMAIN WORK

For each activated domain, run its reference file's methodology and
adversarial challenges in order. Do not skip adversarial challenges —
they are in the reference files, not in this body.

For single-domain questions: produce the reference file's standard output
format (defined in each reference file).

For multi-domain questions: run all activated domains first, then proceed
to PART 4 (synthesis) before delivering any output.

---

## PART 4 — MULTI-DOMAIN SYNTHESIS (multi-domain questions only)

Runs after PART 3 completes all activated domains. Skipped for single-
domain questions.

Step 1 — Load cross-domain-map.md (if not already loaded).

Step 2 — For every activated domain pair, check the conflict map for
known interaction points. For each interaction point that applies:
  a. Name the conflict explicitly
  b. State which domain's constraint takes priority and why
  c. Produce the resolved recommendation

Step 3 — Produce a single integrated output:
  - One recommendation section (not one per domain)
  - Cross-domain interactions named and resolved inline
  - Domain-specific constraints that do not conflict folded in without
    being flagged as domain-specific
  - Open items that require cross-domain resolution flagged as OPEN

HARD FAIL: Output has per-domain section headers (e.g., "BALANCE
FINDINGS:", "PSYCHOLOGY FINDINGS:") = concatenation, not synthesis.
Rewrite as integrated output before delivering.

---

## META-ADVERSARIAL REVIEW

HARD FAIL: Deliver any output before this block is produced.

**Challenge 1 — Domain completeness**
Did all relevant domains activate? Re-run PART 0 against the question.
If any row in the classification table matches but that domain was not
activated, activate it now and load its reference file before delivering.
FAIL example: Question asks about the cost curve for a new mechanic. Only
IDLE-MATH activated. BALANCE not checked — but cost questions have emotional
arc implications (IDLE-MATH + BALANCE rule). Add BALANCE.

**Challenge 2 — Synthesis check**
Is the output a single integrated recommendation, or are domain findings
listed as separate sections?
FAIL: Output contains explicit domain headers.
PASS: Output addresses the question in one voice; domain contributions are
woven together, not stacked.

**Challenge 3 — Cross-domain conflict resolution**
For multi-domain outputs: were any cross-domain conflict points from
cross-domain-map.md applicable? If yes, were they resolved (not just named)?
FAIL: "BALANCE suggests X; PSYCHOLOGY suggests Y" with no resolution.
PASS: "X is recommended because [reason]; Y applies but is superseded
by [priority rule] in this context."

**Challenge 4 — Reference file confirmation**
Is every activated domain's reference file visible in the current turn's
context via explicit `view` output?
FAIL: Domain declared activated but no `view` output for its file.
PASS: Every activated domain has a `view` call with visible output in
this turn.

**Confirmation block (required before every output delivery):**

    Meta-review:
      Challenge 1 — Domain completeness: [all relevant domains activated, or domains added]
      Challenge 2 — Synthesis: [integrated output / headers present — rewrite before delivering]
      Challenge 3 — Conflict resolution: [applicable conflicts resolved / no multi-domain / no conflicts]
      Challenge 4 — Reference confirmation: [all view outputs visible / FAIL: [domain] not loaded]
      Status: CLEAR to deliver / BLOCKED — [reason]

---

## Examples

**Example 1 — Single-domain (BALANCE)**

User: "Players are reporting the Workshop feels stressful."

PART 0: "stressful" → feel/emotion → BALANCE. No other rows match.

    DOMAINS ACTIVATED: BALANCE
    Reference files to load: references/balance.md
    Question type: single-domain
    Cross-domain check required: no

Load references/balance.md → apply Sylvester emotional arc diagnosis (PART 1):
Tower target arc = focused efficiency, satisfying completion. Stressful ≠
focused efficiency → disrupted arc. Diagnostic: complexity scale with roster
size? Any step opaque? Output: arc-targeted adjustments.

    Meta-review:
      Challenge 1: BALANCE only — no additional rows match
      Challenge 2: single-domain — synthesis N/A
      Challenge 3: single-domain — no conflict resolution required
      Challenge 4: references/balance.md loaded with visible output
      Status: CLEAR to deliver

---

**Example 2 — Multi-domain (BALANCE + PSYCHOLOGY)**

User: "Will players enjoy the Cards of Fate system?"

PART 0: "enjoy" → feel question → BALANCE; "players" + motivation → PSYCHOLOGY.
Multi-domain rule fires: "will players enjoy/love/care about this mechanic."

    DOMAINS ACTIVATED: BALANCE + PSYCHOLOGY
    Reference files to load: references/balance.md, references/psychology.md, references/cross-domain-map.md
    Question type: multi-domain
    Cross-domain check required: yes

Load all three files. BALANCE: Sylvester emotional arc, loop/arc check, decision space.
PSYCHOLOGY: SDT — Autonomy for card choices, Competence for mastery signal. Cross-domain-map:
BALANCE + PSYCHOLOGY challenge design conflict — BALANCE may recommend complexity increase;
PSYCHOLOGY checks Architect/Gardener split.
PART 4 synthesis: Cards of Fate serves Autonomy (Architect) and Competence (visible mastery
on draws). Complexity increase approved for Architect but must be gated — Gardener's Competence
ceiling is lower. Integrated recommendation: add complexity behind a visible milestone unlock,
not at session start.

    Meta-review:
      Challenge 1: BALANCE + PSYCHOLOGY — no additional rows match
      Challenge 2: integrated output — no domain headers present
      Challenge 3: BALANCE/PSYCHOLOGY challenge design conflict resolved via SDT Autonomy priority rule
      Challenge 4: all three reference files loaded with visible output
      Status: CLEAR to deliver

---

**Example 3 — Multi-domain (IDLE-MATH + PROGRESSION + GDD)**

User: "Is the mana gate at cycle 30 correctly calibrated, and is the spec ready to implement?"

PART 0: "mana gate" + "cycle" → rates/math → IDLE-MATH; "gate" + "sequence" → PROGRESSION;
"ready to implement" → GDD completeness → GDD. Three domains activate.

    DOMAINS ACTIVATED: IDLE-MATH + PROGRESSION + GDD
    Reference files to load: references/idle-math.md, references/progression.md,
      references/gdd-standards.md, references/cross-domain-map.md
    Question type: multi-domain
    Cross-domain check required: yes

Load all four files. PROGRESSION: Challenge 4 fires — RATE-UNVALIDATED until IDLE-MATH
confirms mana rate. IDLE-MATH: rate check against cycle 30 — if D-026 is OPEN, gate is
uncalibrated. GDD: DoR audit on spec section.
Cross-domain-map: PROGRESSION + IDLE-MATH — gate flagged RATE-UNVALIDATED; Any domain + GDD
— DoR cannot pass until domain items resolved.
PART 4 synthesis: Gate calibration OPEN (cannot validate without confirmed mana rate). GDD
DoR fails because calibration value is unvalidated — section is L1, not L2. Resolve D-026
first, then re-run IDLE-MATH validation, then re-run GDD audit.

    Meta-review:
      Challenge 1: all three domains activated — cross-domain-map loaded for all pairs
      Challenge 2: integrated output — no domain headers present
      Challenge 3: PROGRESSION/IDLE-MATH rate conflict resolved; GDD DoR explicitly blocked by open item
      Challenge 4: all four reference files loaded with visible output
      Status: CLEAR to deliver

---

## Out of Scope

This skill does NOT:
- Check lore canon or NPC design specs (use loop-extended-lore-checker, loop-npc-designer)
- Generate production code (use loop-extended-code-guardian)
- Direct visual or audio design (use loop-extended-visual, suno-prompter, loop-sfx-designer)
- Design UI layout or mobile UX (use loop-mobile-ux)
- Produce research synthesis documents (use utility-data-analyst)

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-lore-checker | Lore canon verification |
| loop-extended-code-guardian | React Native code quality, design tokens |
| loop-extended-visual | Art direction, visual identity |
| loop-mobile-ux | Screen layout, touch targets, mobile UX |
| suno-prompter | Music and audio track generation |
| SkillRouter arxiv 2603.22455 | Routing accuracy for overlapping skills — primary research basis |
| SkillReducer arxiv 2603.29919 | Taxonomy-driven classification, less-is-more — primary research basis |
| SELECT-THEN-ROUTE EMNLP 2025 | Two-stage classify-then-route pattern |
