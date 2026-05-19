---
name: persona-developer
description: >
  Developer skill for The Loop — dispatcher across all development domains:
  code quality, mobile UX, accessibility, design system, screen inventory,
  data modeling, build planning, session continuity, and scripting/automation.
  Use automatically — do not wait to be asked. Trigger on ANY of these signals:
  any React Native code written or reviewed; Supabase query, migration, RLS,
  or Edge Function; color, font, or token in code; "FlashList", "Reanimated",
  "supabase", "migration", "RLS", "MMKV", "Zustand", "Expo Router", "theme.js",
  "test", "safe area", "gesture", "accessibilityRole" in a dev context; screen
  inventory or data model being designed; coding session starting or ending;
  implementation plan needed; bug reported; screen, component, store, or
  migration file created; any Python script or bash automation; ".py" file;
  "d1_database_query"; "github_pat"; CI validation script. Do NOT trigger for:
  lore questions, art direction, balance math, or skill authoring.
  Load once per session.
---
gates_passed: 2026-05-18
SKILL_VERSION: v2.2
# Replaces: loop-extended-code-guardian, utility-mobile-react-native,
# utility-build-supabase, loop-screen-inventory, loop-data-model,
# loop-build-tracker, loop-build-planner, loop-mobile-ux,
# utility-game-accessibility, loop-extended-design-system

# Developer Skill — Dispatcher

Routes every development request to the correct reference files and synthesizes
an integrated response. The body is routing and synthesis only. All domain
expertise lives in `references/`.

Type: dispatcher

---

## GOTCHAS

1. **Classifying without loading** — domain code assigned but reference file not `view`'d; skill responds from memory instead of loaded content. Always load every file matching active codes before generating output.
2. **Skipping build phase check** — code generated before reading build phase from D1; implementation targets wrong phase. SC and LOOP codes always load `loop-specific.md` and query D1 first.
3. **Concatenated multi-domain output** — separate DESIGN SYSTEM: / ACCESSIBILITY: sections instead of one integrated response. Part 3 synthesis protocol resolves conflicts before output; result must read as one answer.
4. **Post-generation audit skipped under time pressure** — hex values or missing accessibilityRole slip through; caught only in QA. Part 4 universal checks run silently on every response turn.
5. **Reference files assumed persistent** — loaded content from a prior turn treated as still available; stale rules applied. Reference files do not persist across turns — re-view each turn that uses them.

---

## PART 0 — DOMAIN CLASSIFICATION

Classify the request before loading any reference file. Use the domain codes
below. A request may activate multiple codes.

| Code | Domain | Triggers |
|---|---|---|
| `DS` | Design system (enforcement) | color, font, token, theme.js, visual style, background, hex value |
| `DST` | Design system (token spec) | token value, token naming, elemental palette, rarity color, typography scale, spacing, animation duration |
| `RN` | React Native patterns | FlashList, FlatList, Reanimated, gesture, worklet, re-render, Hermes, New Architecture, React Compiler, Expo Router, contentInsetAdjustment |
| `DB` | Supabase correctness | migration, RLS, auth.uid, service_role, edge function, anon key, supabase-js, realtime, RPC |
| `TDD` | Test and debug | test file, red/green/refactor, bug, crash, failing, unexpected behavior |
| `MUX` | Mobile UX | touch target, safe area, gesture conflict, tap feedback, thumb zone, portrait layout, hitSlop, InteractionManager |
| `A11Y` | Accessibility | accessibilityRole, accessibilityLabel, accessibilityState, contrast, colorblind, screen reader, reduced motion, VoiceOver, TalkBack |
| `SI` | Screen inventory | screen inventory, navigation map, Expo Router structure, screen entry, what screens, what goes on this screen |
| `DM` | Data model | data model, schema, entity, MMKV key, storage split, sync conflict, True Time, RLS policy map |
| `SC` | Session continuity | session start, session end, build phase, where did we leave off, what phase, what's next in build |
| `BP` | Build planning | write a plan, plan this out, what do we build, implementation plan, session plan |
| `LOOP` | Loop-specific rules | lore naming, The Dreaming, The Rift, The Tower, The Void, the Ark, Familiar, void_[900], dreaming[900] |
| `PS` | Python/scripting | .py file, python3, argparse, subprocess, pip install, bash script, shell automation, validate_handoff, sync-skills, pre_package_check, d1_database_query, granular_findings, failure_patterns, github_pat, git clone, git commit, git push, sync-failure-rules |

**Classification format (produce before loading any reference):**

```
DOMAIN: [codes]
Active codes: [list]
Reference files to load: [list paths]
Multi-domain: [yes/no — if yes, check cross-domain-map.md]
```

---

## PART 1 — REFERENCE FILE LOADING

Load ONLY the reference files matching active domain codes.

| Active code | Reference file |
|---|---|
| `DS` | `references/design-system-rules.md` |
| `DST` | `references/design-system-tokens.md` |
| `RN` | `references/react-native-patterns.md` |
| `DB` | `references/supabase-correctness.md` |
| `TDD` | `references/tdd-and-debug.md` |
| `MUX` | `references/mobile-ux.md` |
| `A11Y` | `references/accessibility.md` |
| `SI` | `references/screen-inventory.md` |
| `DM` | `references/data-model.md` |
| `SC` | `references/session-continuity.md` |
| `BP` | `references/build-planning.md` |
| `LOOP` | `references/loop-specific.md` |
| `PS` | `references/python-scripts.md` |
| Multi-domain (2+ codes) | Also load `references/cross-domain-map.md` |

**Always reload reference files in each response turn that needs them.**
Reference files do not persist across turns — re-view each turn that uses them.

### Loop build phase (on every SC or LOOP code activation)

Load current build phase from D1 before generating any code.
D1: `the-loop-storage` (afd78e0e: use `a2af54f4-6385-45dd-92e7-edc45fa5b8bd`) — table: `build_phase`
Query: `SELECT content FROM build_phase WHERE key = 'current'`
Parse returned `content` as JSON.

If no data exists, ask: "Which build phase are we in? (1-6)" before proceeding.

---

## PART 2 — PRE-GENERATION PROTOCOL

Before writing any code, run pre-generation checklists from loaded reference
files in this order:

**Design phase (if active):** DST → DS → SI → DM
**Session management (if active):** SC → BP
**Project context:** LOOP
**Implementation:** MUX → A11Y → RN → DB → TDD
**Scripting/automation (if active):** PS

If any reference file requires a check that cannot be satisfied (missing
design token, OPEN schema decision, OPEN lore item), flag it before generating.

**HARD FAIL — SC code active:** Any code generation that occurs before the
session handoff block (or one-liner equivalent) is surfaced is a process
failure. See `session-continuity.md` for full protocol.

**HARD FAIL — BP code active:** Any plan content presented in chat before
the plan file exists on disk at `docs/plans/` is a process failure.
Verify via `ls` before presenting.

---

## PART 3 — SYNTHESIS PROTOCOL

When multiple domain codes are active:

1. Load `cross-domain-map.md`
2. Check for known conflicts between active domains
3. Resolve conflicts per the map's priority rules before generating output
4. Produce a single integrated response — no per-domain section headers
5. Apply all loaded reference file rules simultaneously, not sequentially

**Cross-domain conflict checks (mandatory, silent — fix before presenting):**

- `DS` + `RN` active: does component structure satisfy both token rules and
  RN performance rules?
- `DS` + `DST` active: are token values from DST consistent with enforcement
  rules in DS?
- `DB` + `LOOP` active: check build phase before any Supabase query.
- `SI` + `DM` active: screen inventory must be complete before data model;
  if SI is incomplete, flag before DM work proceeds.
- `SC` + `BP` active: session continuity loads phase state; build planning
  consumes it — load SC first.
- `MUX` + `A11Y` active: touch target size and reduced motion rules in MUX
  must align with A11Y minimums (48×48pt, hitSlop, reduceMotion gating).
- `A11Y` + `DS` active: verify all color tokens satisfy contrast ratios
  defined in A11Y before approving token values.
- `PS` + `DB` active: Supabase (DB code) and D1 (PS code) are different backends
  — confirm which target is in scope; never conflate RLS/Supabase patterns with
  D1 query patterns.
- `PS` + `SC` active: if session-continuity code is being written, confirm
  `validate_handoff.py` path resolves before referencing it.
- `PS` + `TDD` active: Python scripts get syntax validation pre-delivery
  (`python3 -m py_compile`); this is separate from the RN/TS TDD protocol.

---

## PART 4 — POST-GENERATION AUDIT

After generating any code, run post-generation checks from each loaded
reference file before presenting output. Fix violations silently. Flag
only what requires a judgment call.

**Universal post-generation checks (all code, all domains):**
- No hardcoded hex values (`#RRGGBB`) anywhere except inside comments
- No font strings that aren't from the design system
- No banned imports (AsyncStorage, React Navigation, Firebase)
- Every interactive element has `accessibilityRole` and `accessibilityLabel`
- Stateful elements have `accessibilityState`
- Color is never the sole signifier of state, type, or identity
- No `SafeAreaView` from React Native core — `useSafeAreaInsets` only
- No `FlatList` or `ScrollView` + `.map()` for lists longer than 5 items

**Post-generation checks when PS code is active (Python/bash scripts):**
- No `github_pat_` string in generated code outside a comment
- Every `pip install` includes `--break-system-packages`
- No writes to `/mnt/skills/` or `/mnt/user-data/uploads/` paths
- No bare `except:` in Python; no `os.system()` calls
- Exit conventions: `sys.exit(0)` pass, `sys.exit(1)` fail
- Syntax check block visible before delivery: `python3 -m py_compile`

---

## PART 5 — META-ADVERSARIAL REVIEW (dispatcher-specific)

Before presenting output when 2+ domain codes are active:

1. **Scope check:** Did the active domain codes cover everything in the
   request? If a domain was missed, classify it and load its reference file.

2. **Integration check:** Does the output read as a single answer, or as
   separate per-domain answers concatenated? If the latter, rewrite.

3. **Conflict check:** Name any point where two loaded reference files gave
   contradictory instructions. State which rule took priority and why.

4. **Completeness check:** Did every loaded reference file's pre-generation
   checklist and post-generation audit run? If any was skipped, run it now.

---

## Out of Scope

This skill does NOT:
- Answer lore questions (loop-extended-lore-checker)
- Log design decisions (loop-core-decisions)
- Define art direction or visual aesthetic (loop-extended-visual)
- Generate non-code content: documents, skills, lore copy
- Override confirmed stack decisions — flag mismatches as human decisions

---

## Examples

**Example 1 — Code generation (DS + LOOP)**

Request: "Write a ManaBar component."
Classification: `DS`, `DST`, `A11Y`, `LOOP`
Reference files: `design-system-rules.md`, `design-system-tokens.md`,
  `accessibility.md`, `loop-specific.md`, `cross-domain-map.md`
Pre-generation: check phase, load mana token values (DST), confirm
  accessibility rule (element icon alongside color, not color alone).
Post-generation: hex scan, font scan, accessibilityRole + accessibilityValue
  on progress bar, color-sole-signifier check.
Output: integrated component, no per-domain sections.

**Example 2 — Multi-domain (RN + DB + MUX)**

Request: "Build an inventory screen that loads items from Supabase."
Classification: `DS`, `RN`, `DB`, `MUX`, `A11Y`, `LOOP`
Reference files: all six + `cross-domain-map.md`
Pre-generation: check phase, confirm FlashList for item list, confirm RLS
  query pattern, confirm safe area handling (useSafeAreaInsets).
Cross-domain: MUX touch targets + A11Y accessibilityRole on item cards.
Post-generation: all audits; single integrated screen component.

**Example 3 — Session start (SC + BP)**

Request: "Let's start coding the Dreaming screen."
Classification: `SC`, `BP`, `SI`, `DS`, `RN`, `MUX`, `A11Y`, `LOOP`
SC fires first: load D1 build phase, surface handoff block.
BP fires: write plan file to `docs/plans/YYYY-MM-DD_dreaming-screen.md`,
  present with "Don't implement yet."
SI: verify Dreaming screen entry has three-state coverage before coding.
After plan approval: DS + RN + MUX + A11Y enforce code quality.

**Example 4 — Schema design (SI + DM)**

Request: "Design the data model for inventory."
Classification: `SI`, `DM`, `DB`, `LOOP`
SI check: confirm Inventory screen entry is complete (three-state coverage).
DM: identify inventory entities from screen content, assign storage tier
  (MMKV session + Supabase sync), design RLS policy (Pattern A).
DB: migration SQL with RLS policy before any code.
Output: entity definitions, MMKV key spec, RLS policy — no code yet.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| references/design-system-rules.md | Token enforcement in code |
| references/design-system-tokens.md | Token values, naming, palette spec |
| references/react-native-patterns.md | RN/Expo performance patterns |
| references/supabase-correctness.md | Supabase migrations, RLS, Edge Functions |
| references/tdd-and-debug.md | TDD protocol, bug investigation |
| references/mobile-ux.md | Touch targets, safe area, gesture, feedback, layout |
| references/accessibility.md | Screen reader props, contrast, reduced motion |
| references/screen-inventory.md | Screen catalog, Expo Router structure, completeness |
| references/data-model.md | Storage architecture, entity design, RLS patterns |
| references/session-continuity.md | Build phase tracking, session start/end protocols |
| references/build-planning.md | Implementation plan structure and quality rules |
| references/loop-specific.md | Build phases, lore naming, confirmed stack |
| references/cross-domain-map.md | Cross-domain conflict resolution |
| references/python-scripts.md | Python scripting, bash automation, D1 ops, GitHub, CI toolchain |
| loop-extended-lore-checker | Canon consistency for UI copy and in-world text |
| loop-extended-visual | Art direction — visual language and aesthetic |
