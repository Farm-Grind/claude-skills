---
name: life-core-boxing
description: >
  Guides at-home boxing fitness and technique development — footwork, head
  movement, shadowboxing, conditioning, round structure, and equipment
  progression. Use automatically — do not wait to be asked. Trigger on ANY of
  these signals: user asks about boxing sessions, boxing drills, footwork,
  head movement, slipping, weaving, dodging, shadowboxing, punch combinations,
  boxing conditioning, jump rope for boxing, round structure, what to work on
  in boxing, how to improve boxing technique, or what equipment to buy; user
  says "boxing session", "boxing workout", "boxing drill", "what should I
  practice", "how do I slip", "how do I move my feet", "what's my boxing
  schedule", or any variant; a session involves boxing planning or technique
  review. Load once per session. Do NOT trigger for: strength programming,
  nutrition, recovery, or weekly scheduling (life-core-fitness owns those).
---
gates_passed: 2026-05-17
SKILL_VERSION: v1.0

# Boxing Trainer

At-home boxing technique and conditioning for a fitness-focused practitioner.
Single-domain: footwork, head movement, shadowboxing, conditioning, equipment.

Type: dispatcher

Canonical dispatcher reference: `persona-developer` — read before modifying
dispatcher body structure.

---

## GOTCHAS

1. **Skipping foundation levels** — head movement before stance is solid
   bakes in compensations. Always confirm current level before prescribing
   advanced drills. Level 1-2 fix most "clunky feeling" complaints.
2. **Prescribing "skip it" on low-motivation days** — never correct. Prescribe
   micro tier (15 min) instead. The habit is the training outcome.
3. **Head movement from the waist** — this is the single most common error.
   All slips and ducks drive from legs. A correction that doesn't name the
   error ("bend from legs, not waist") will not stick.
4. **Heavy bag too early** — prescribe Tier 1 equipment only until 4-8 weeks
   of consistent shadowboxing exist. Bag before fundamentals = reinforced
   bad technique.
5. **Same focus every session** — ADHD-relevant: rotate A (footwork) / B
   (head movement) / C (conditioning) across sessions for novelty and
   full-domain development.

---

## PART 0 — CLASSIFY

Single-domain boxing skill. All triggers route to references/boxing.md.
Head movement specifics may additionally need references/head-movement.md —
load both when the question is about slipping, weaving, or defensive movement.

---

## PART 1 — REFERENCE LOAD

Reference files do not persist across turns — re-view each turn that uses them.

    view /mnt/skills/user/life-core-boxing/references/boxing.md

For detailed slip mechanics and combination integration, additionally view:

    view /mnt/skills/user/life-core-boxing/references/head-movement.md

HARD FAIL: Proceed to PART 2 only after boxing.md is loaded and visible
in the current turn's output.

---

## PART 2 — INTAKE

Establish before prescribing:
- Available time this session (determines tier)
- Last session type (A/B/C — prevents same-focus repetition)
- Current foundation level (1-5) if unclear or if a complaint signals regression

One question if genuinely blocked. Infer from context first.

---

## PART 3 — EXECUTE

Route to the appropriate Part in the loaded reference:

| Signal | Reference section |
|---|---|
| "What should I work on today" | Part 8 — session rotation A/B/C |
| Footwork complaint or drill request | Parts 1-2 — foundation and drills |
| Head movement or slipping | Part 3 + references/head-movement.md |
| Shadowboxing structure | Part 4 |
| Conditioning plan or round structure | Part 5 |
| Equipment question | Part 6 |
| Integration with strength days | Part 7 |
| Short session / limited time | Part 8 — flexible session tiers |
| Low motivation | Part 8 — low-motivation sessions (micro tier) |
| Return from break | Part 1 Level 1, micro tier only |

---

## PART 4 — QUALITY CHECK

Before delivering any prescription:
- Available time matched to session tier (micro/short/standard/extended)
- Foundation level appropriate for prescribed drills
- No heavy bag prescribed before 4-8 weeks of consistent shadowboxing
- "Skip it" never prescribed — always replace with micro tier
- Head movement correction always names the error mechanism

HARD FAIL: Never prescribe sparring, competition prep, or contact work —
this skill covers non-contact fitness boxing only.

---

## OUT OF SCOPE

- Strength programming, nutrition, recovery, weekly scheduling —
  life-core-fitness
- Sparring, competition preparation, ring strategy — out of scope entirely
- MMA, Muay Thai, kickboxing — some footwork overlap but this skill is
  boxing-specific

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| life-core-fitness | Strength programming, nutrition, recovery, periodization |
| utility-ops-project-manager | Session and project planning infrastructure |
