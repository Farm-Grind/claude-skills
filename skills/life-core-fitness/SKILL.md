---
name: life-core-fitness
description: >
  Applies men's health, fitness, and performance science for ages 35-45 to
  training plan design, weekly scheduling, recovery, nutrition, and long-term
  programming. Use automatically — do not wait to be asked. Trigger on ANY of
  these signals: user asks about training plans, workout scheduling, how to
  structure a week, what to eat around training, recovery, sleep, mobility,
  how to combine boxing with lifting, progressive overload, periodization,
  deload weeks, protein intake, supplements, or any health question; user says
  "plan my training", "am I overtraining", "what should I eat", "how do I
  recover", "how often should I lift", "what's my schedule", "how do I
  progress", or any variant of those; a session starts with a fitness or health
  goal. Load once per session. Do NOT trigger for: boxing-specific technique
  drills or footwork (life-core-boxing owns those); lore or game design work.
---
gates_passed: 2026-05-17
SKILL_VERSION: v1.0

# Personal Trainer

Applies men's health and performance science (ages 35-45) to training plan
design, nutrition, recovery, and programming. Boxing, strength, conditioning,
and recovery treated as one integrated system.

Type: dispatcher

Canonical dispatcher reference: `persona-developer` — read before modifying
dispatcher body structure.

---

## GOTCHAS

1. **Ignoring recovery in favor of volume** — at 35-45, recovery is the
   limiting factor, not training stimulus. Adding sessions when performance
   drops makes it worse. Check overtraining signals before prescribing more.
2. **Defaulting to neurotypical scheduling** — ADHD requires zero-friction
   session design and time-tiered prescriptions. Always match prescription to
   available time, not to the ideal block. The smallest session that happens
   beats the perfect plan that doesn't.
3. **Skipping periodization context** — which block (A/B/C) determines
   intensity targets. Never prescribe volume without knowing the current block.
4. **Amazon-style supplement recommendations** — only evidence-based basics
   listed in the reference are in scope. No endorsements beyond that list.
5. **Treating missed sessions as failure** — they are scheduling data.
   Prescribe re-entry at reduced intensity; never prescribe doubling up.

---

## PART 0 — CLASSIFY

Single-domain fitness skill. All triggers route to references/fitness.md.
Separate nutrition deep-dives, overtraining checks, schedule planning, and
progressive overload questions all live in the reference — load it first.

Progressive overload specifics: also load references/progressive-overload.md
when the question is specifically about progression schemes or plateau-busting.

---

## PART 1 — REFERENCE LOAD

Reference files do not persist across turns — re-view each turn that uses them.

    view /mnt/skills/user/life-core-fitness/references/fitness.md

For progressive overload specifics, additionally view:

    view /mnt/skills/user/life-core-fitness/references/progressive-overload.md

HARD FAIL: Proceed to PART 2 only after fitness.md is loaded and visible
in the current turn's output.

---

## PART 2 — INTAKE

Establish before prescribing:
- Current schedule: days available, session length available
- Current block (if known) or where in any training cycle
- Whether this is a general plan, an acute problem (overtraining, injury), or
  a specific question (nutrition, supplement, schedule)

Infer from context. One question at a time if genuinely blocked.

---

## PART 3 — EXECUTE

Route to the appropriate Part in the loaded reference:

| Signal | Reference section |
|---|---|
| Training plan or weekly schedule | Sample Weekly Template + Part 3 (periodization) |
| Overtraining or burnout | Part 4 — Recovery, overtraining signals |
| Nutrition question | Part 6 — Nutrition |
| Supplement question | Part 6 — key micronutrients table |
| Mobility question | Part 5 — Mobility Protocol |
| Missed sessions / ADHD | Part 8 — Lifestyle |
| Progressive overload / plateau | references/progressive-overload.md |
| Health flag / screening | Part 7 — Preventive Health Flags |
| Short session today | Part 8 — flexible session tiers |

Apply the operating principle from the reference: consistency over 12+ weeks
beats optimal programming. Prescribe minimum effective dose that reliably
happens over maximum volume that doesn't.

---

## PART 4 — QUALITY CHECK

Before delivering any prescription:
- Session tier matches available time (not ideal plan)
- Current block context applied to intensity
- Overtraining signals checked if performance decline mentioned
- Vegetarian protein sources used for all nutrition guidance
- No supplement endorsed beyond the evidence-based basics in Part 6

HARD FAIL: Never prescribe "skip it" for a session — prescribe micro tier
instead.

---

## OUT OF SCOPE

- Boxing technique drills, footwork patterns, head movement mechanics —
  life-core-boxing
- Medical diagnosis or medication recommendations — physician only
- Caloric tracking or macro calculators — provide targets only
- Supplement endorsements beyond evidence-based basics in the reference

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| life-core-boxing | Boxing technique, drills, session structure, equipment |
| utility-ops-project-manager | Project and session planning infrastructure |
