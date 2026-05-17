---
name: utility-game-accessibility
description: >
  Applies accessibility standards to mobile game design and code. Covers
  five disability categories (visual, motor, cognitive, hearing, vestibular),
  with emphasis on colorblindness. Enforces color-is-never-the-sole-signifier
  across color-coded systems (elemental palettes, rarity tiers, status
  indicators). Provides React Native patterns for screen readers, reduced
  motion, font scaling, and accessible props. Extended Loop-specific coverage
  included as primary reference implementation. Use automatically — do not
  wait to be asked. Trigger on ANY of these signals: a UI element, color, or
  visual system is being designed or coded; a settings screen is specified; a
  minigame, feedback system, or notification is being designed; the words
  "color", "contrast", "font", "animation", "haptic", or "feedback" appear
  in a design context; any screen or component is being built.
  Do NOT trigger for: lore content or balance math. Load once per session.
---
gates_passed: 2026-05-17
SKILL_VERSION: v1.0

# Mobile Game Accessibility

Defines accessibility requirements for mobile games across all disability
categories. Single-domain: visual, motor, cognitive, hearing, vestibular.

Type: dispatcher

Canonical dispatcher reference: `persona-developer` — read before modifying
dispatcher body structure.

---

## GOTCHAS

1. **Color-as-sole-signifier** — the most common mobile game accessibility
   failure. Every color-coded system (elemental palette, rarity, status) must
   pair color with at least one non-color differentiator (shape, icon, text,
   pattern). Ask: "If all color were removed, is this still understandable?"
2. **Skipping the audit on "small" UI changes** — any color, icon, or feedback
   element added without an accessibility check can silently break CVD
   compliance. Every UI element triggers this skill.
3. **Treating motor as touch-target-only** — timing-critical minigames are a
   motor barrier. Speed reduction must be offered for any precision-timing
   mechanic. Touch target size is necessary but not sufficient.
4. **Accessible settings added post-launch** — all accessibility toggles must
   be present at v1 launch and surfaced at first run. Retrofitting is
   exponentially more expensive.
5. **OS reduced-motion not checked** — always implement
   `AccessibilityInfo.isReduceMotionEnabled()` in addition to the in-app
   toggle. Players who set it at OS level expect it to work app-wide.

---

## PART 0 — CLASSIFY

Single-domain accessibility skill. All triggers route to
references/accessibility.md. No sub-domain classification required — load
the reference and apply the relevant Part to the component being reviewed.

---

## PART 1 — REFERENCE LOAD

Reference files do not persist across turns — re-view each turn that uses them.

    view /mnt/skills/user/utility-game-accessibility/references/accessibility.md

HARD FAIL: Proceed to PART 2 only after accessibility.md is loaded and
visible in the current turn's output.

---

## PART 2 — SCOPE CHECK

Before applying any Part from the reference, confirm the element type:

| Element type | Primary Part |
|---|---|
| Color-coded system (elemental, rarity, status) | Part 2 — Visual, CVD section |
| Text, contrast, font size | Part 2 — contrast ratios, font scaling |
| Touch target, gesture, minigame timing | Part 3 — Motor |
| Tutorial, NPC text, UI complexity | Part 4 — Cognitive |
| Audio feedback, NPC dialogue | Part 5 — Hearing |
| Animation, particle effects, transitions | Part 6 — Vestibular |
| Settings screen structure | Part 7 — Settings |
| Full screen audit | Part 8 — Audit Checklist |

---

## PART 3 — EXECUTE

Apply the relevant Part(s) from the loaded reference. Produce an
ACCESSIBILITY AUDIT block (format defined in Part 8 of the reference)
whenever a complete screen or component review is requested.

HARD FAIL: Never skip the color-as-sole-signifier check (Part 2 CVD section)
on any UI that uses color to convey state.

---

## OUT OF SCOPE

- Lore content, balance math, NPC design — not accessibility concerns
- Full screen-reader-only gameplay design (audio game design) — out of scope;
  navigability is required, full blind playthrough is not
- Web accessibility (WCAG applies to UI components; this skill is mobile-first)

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-code-guardian | Enforces accessibility props in generated React Native code |
| loop-mobile-ux | Touch target sizes, haptic gating, motion sensitivity UX |
| gameaccessibilityguidelines.com | Industry gold standard — Basic tier is v1 must-have |
| WCAG 2.2 | Contrast and interaction standards |
| React Native Accessibility docs | accessibilityRole, accessibilityLabel, AccessibilityInfo API |
