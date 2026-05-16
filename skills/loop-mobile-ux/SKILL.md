---
name: loop-mobile-ux
description: >
  Applies mobile game UX principles to The Loop's screen and interaction
  design. Covers touch targets, thumb zones, gesture hierarchy, feedback
  systems (visual/audio/haptic), session pacing, progressive disclosure,
  idle game UI conventions, React Native-specific performance constraints,
  safe area handling, and portrait-mode layout rules. Use automatically —
  do not wait to be asked. Trigger on ANY of these signals: a screen or
  interaction is being designed or reviewed; a component layout is being
  specified; tap targets, gestures, or animations are discussed; onboarding
  or tutorial flow is being designed; a screen feels "off" or unclear;
  user asks "where should this button go", "how should this feel", "is this
  too many taps", "what happens when the player taps X"; the words "button",
  "gesture", "animation", "feedback", "haptic", "tap", "layout", "portrait",
  or "safe area" appear in a UI context.
  Do NOT trigger for: lore, balance math, or document creation. Load once
  per session.
---
SKILL_VERSION: v1.0

# The Loop — Mobile UX Skill

Applies mobile game UX principles to screen and interaction design for
The Loop. Knows what mobile idle game players expect, where React Native
creates UX constraints, and how to design for short-burst sessions without
sacrificing depth.

---

## PART 1 — THE MOBILE IDLE PLAYER CONTEXT

This is the foundational insight that shapes every UX decision in The Loop.

**Mobile idle players are not hardcore gamers.** They are experienced users
of non-gaming mobile apps — email, maps, social media, banking. Their mental
model is built from those apps, not from console games. Design to that mental
model, not to gaming conventions they may never have encountered.

Implications:
- Navigation must follow app conventions (back = left swipe or arrow, dismiss
  = tap outside or X, settings = gear icon). Do not invent novel navigation.
- Session length averages 1–2 minutes for mobile games, but The Loop is
  primarily played at home, not on the go. Design for both: a 90-second check-
  in should feel complete, and a 10-minute session should feel rewarding.
- Players pick up and put down frequently. Every screen must communicate its
  state at a glance. No screen should require more than 2 seconds to orient.
- The game's dark fantasy depth is conveyed through atmosphere, not UI
  complexity. The interface itself must feel simple even when the world is not.

**The Loop's specific session contract:**
Each cycle is the natural session unit. A player can enter, complete a
location action, and exit feeling like they did something meaningful — in
under two minutes. The Dreaming (draw cards, check comms) and Rift (forage,
habitat action) are the natural short-session entry points. The Tower is
slightly longer. Design each location to support the short-session case.

---

## PART 2 — TOUCH TARGETS AND THUMB ZONES

### Minimum tap target sizes

| Platform | Minimum | Recommended |
|---|---|---|
| Apple HIG | 44×44pt | 48×48pt |
| Material Design | 48×48dp | 56×56dp |
| The Loop rule | 48×48pt | 56×56pt for primary actions |

Never place two tappable elements with less than 8pt of padding between
them. On a 375pt canvas, this is a strict constraint — plan layout around
it, not after it.

### Thumb zone map (portrait, 375pt canvas)

```
┌─────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  ← Hard reach — secondary info only
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │    (NPC names, cycle count display)
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │  ← OK reach — secondary actions
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │    (Codex button, back nav)
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │
│ ███████████████████████████████ │  ← Natural thumb zone — primary actions
│ ███████████████████████████████ │    (Advance cycle, confirm actions,
│ ███████████████████████████████ │     primary interactive elements)
│ ███████████████████████████████ │
└─────────────────────────────────┘
  [Safe area bottom — do not place interactive elements here]
```

**The Loop layout rule:** Primary interactive elements (cycle advance,
foraging tap zone, altar confirm, workshop queue submit) belong in the
natural thumb zone. Navigation controls and status displays can live
higher. Never place a primary action in the top 40% of the screen.

### Safe area handling

Always wrap game screens in `SafeAreaView` or use `useSafeAreaInsets()`.
The Loop's dark full-bleed backgrounds make safe area violations invisible
in testing but obvious on notched/punch-hole devices in production.

- Status bar: use `expo-status-bar` with `style="light"` on dark backgrounds
- Bottom inset: add bottom padding equal to `insets.bottom` on screens with
  bottom-anchored controls
- Home indicator area on iPhones: never place tap targets within 34pt of
  the physical bottom edge

---

## PART 3 — GESTURE HIERARCHY

The Loop uses a specific gesture map. Never introduce a gesture that
conflicts with this hierarchy.

### Confirmed gesture assignments

| Gesture | Action | Available on |
|---|---|---|
| Swipe right | Open Inventory overlay | All Tier 2 screens (Dreaming, Rift, Tower, Source) |
| Swipe left | Open Codex overlay | All Tier 2 screens |
| Tap | Primary interaction (forage tap, card draw, confirm) | Context-dependent |
| Tap & hold | Secondary info (item detail on long press) | Inventory items |
| Swipe down / tap dim | Dismiss modal | All Tier 4 modals |

### Gesture conflict rules

- Swipe right and swipe left are consumed by the game loop navigation.
  **No horizontal scroll containers** can exist on Tier 2 screens — they
  will conflict. Use vertical scroll or pagination only.
- Minigames with tap mechanics (Foraging dial) must not trigger swipe
  navigation accidentally. Use `PanGestureHandler` with a directional
  threshold — horizontal velocity > 50% of vertical must not register as
  a tap on the minigame element.
- The Inventory and Codex overlays arrive as slide-in panels, not full
  screen replacements. The player should feel they are overlaying the game
  world, not leaving it.

### New gesture checklist

Before adding any new gesture to The Loop:
1. Does it conflict with swipe-right (Inventory) or swipe-left (Codex)?
2. Does it use a gesture type already assigned to another action?
3. Is there a tap equivalent for players who avoid gestures?
4. Is it discoverable without a tutorial (visible affordance)?

---

## PART 4 — FEEDBACK SYSTEMS

Every player action must produce a response. Silence after a tap is a bug,
not a design choice.

### The three feedback layers

**Visual feedback** — always required
- Button press: scale down to 0.95 on press, release to 1.0 (Reanimated
  `withSpring`). Duration: 80–120ms. Never skip this.
- State change: any persistent state change (item collected, mana gained,
  action consumed) requires a visible animation — particle burst, number
  float, icon pulse. Even subtle.
- Loading state: any async operation (Supabase fetch, True Time check)
  requires a skeleton or spinner. A blank screen is never acceptable.
- Empty state: every list or dynamic content area needs a designed empty
  state. "No requests yet" with the Familiar's silhouette beats a blank gap.

**Audio feedback** — required for primary actions
See sound design document for asset names. Key trigger moments:
- Card draw (Cards of Fate)
- Successful forage zone tap
- Altar use confirmation
- Cycle advance (Source activation)
- Item receive / mana gain
- NPC message arrival
Audio must be optional — respect `settings.audio_enabled` flag.

**Haptic feedback** — required for high-value moments, optional elsewhere
Use `expo-haptics` (available in Expo SDK, no additional install):

| Moment | Haptic type |
|---|---|
| Successful foraging tap (in zone) | `impactAsync(Heavy)` |
| Card draw reveal | `impactAsync(Medium)` |
| Cycle advance / Source activation | `notificationAsync(Success)` |
| Failed foraging tap (missed zone) | `impactAsync(Light)` |
| Error / rejected action | `notificationAsync(Error)` |
| Button press (standard) | `selectionAsync()` — use sparingly |

Haptics must be gated on platform capability and user preference. Always
wrap in try/catch — haptics fail silently on some Android devices.

### Pop-up and modal feedback rules

- Animate modals from their trigger button, not from screen center.
  Scale up from the tapped element → player retains spatial context.
- Always dim the background behind modals (semi-transparent dark overlay,
  ~60% opacity). This communicates "session paused, not lost."
- Positive confirmations (primary action) go on the **right** side of
  two-button dialogs. Destructive or cancel actions go **left**. This is
  a widely documented convention from +250 games analysis.
- Avoid X buttons for dismissing modals where possible. "Tap outside to
  dismiss" or a labeled "Close" / "Done" button is less ambiguous.

---

## PART 5 — PROGRESSIVE DISCLOSURE AND COMPLEXITY LAYERING

The Loop has significant depth — multiple minigames, faction systems,
achievement tiers, investigation arcs. The UX must protect new players
from this depth until they are ready for it.

### The onion model for The Loop

**Layer 1 (Cycles 1–5):** The three locations, one action each, cycle
advance. Nothing else visible. No inventory tab, no Codex, no Comms Array.
The Familiar introduces each element as it unlocks.

**Layer 2 (Cycles 6–20):** Inventory becomes accessible. Codex unlocks.
Factory and Workshop appear in the Tower. Cards of Fate introduced.

**Layer 3 (Cycles 20+):** NPC requests arrive. Faction renown becomes
visible. Achievement panel accessible.

**Layer 4 (Investigation arc):** True Account content surfaced only after
specific story flags are set. Never surface dark lore UI elements before
the player has found the breadcrumb.

### Implementation rules

- Locked content: visually present but greyed out / locked icon. Player
  can see what is coming. Never hide locked content entirely — anticipation
  is a retention mechanic.
- New system introduction: the Familiar delivers a short contextual message
  the first time a system unlocks. Max 2 sentences. No modal blocker.
- Tooltip onboarding: new interactive elements get a subtle pulsing
  highlight for one session after unlock. Tap the element = highlight gone.
  Never persist tutorials past first interaction.
- Tab/section locking pattern: grey out with a padlock glyph and cycle
  count ("Unlocks at cycle 6"). Use the same visual language throughout.

---

## PART 6 — REACT NATIVE PERFORMANCE RULES FOR UX

React Native has specific constraints that affect UX quality. These are
not optional — violating them produces visible jank.

### Animation thread rule

All animations in The Loop must run on the UI thread, not the JS thread.
JS thread animations stutter when state updates fire.

**Always use Reanimated for:**
- Screen transitions
- Interactive elements (foraging dial, card flip, button press)
- Any animation tied to a gesture
- Any animation longer than 200ms

**Never use the basic `Animated` API for motion.** Use `Animated` only for
opacity on simple show/hide where Reanimated is overkill.

### Heavy operations rule

Never perform API calls, MMKV writes, or heavy computation during an
animation. Use `InteractionManager.runAfterInteractions()` to defer:

```javascript
InteractionManager.runAfterInteractions(() => {
  // Safe to write to MMKV or call Supabase here
  saveCurrentCycleState();
});
```

This prevents location transition animations from stuttering due to
simultaneous save operations — a very common React Native idle game bug.

### FlashList / ScrollView rule

Any scrollable list of items (Inventory, Codex entries, achievement list)
must use `FlashList` (v2, from `@shopify/flash-list`). Never use `FlatList`
or a `ScrollView` wrapping a `.map()` for lists longer than 5 items.
FlashList v2 requires New Architecture (confirmed enabled for The Loop) —
no `estimatedItemSize` needed. The memory cost of `ScrollView`+map is
invisible in dev, painful in prod.

### Image loading rule

Pre-load images for screens the player is about to visit. The Tower always
follows the Rift — begin loading Tower assets during Rift session. Use
`Image.prefetch()` during location transitions.

---

## PART 7 — PORTRAIT MODE AND LAYOUT CONSTRAINTS

The Loop is portrait-only. This is confirmed. Lock orientation in app.json:
```json
"orientation": "portrait"
```

### Portrait layout rules

**Design width:** 375pt (iPhone SE minimum). Test at 390pt (iPhone 14)
and 412pt (common Android). Never assume a wider canvas.

**Vertical real estate is precious.** The Loop's location screens must
fit: location atmosphere header, primary interactive area, action/status
bar, and navigation affordances. That's roughly:
- Header zone: ~80–100pt (atmosphere visual, location name)
- Primary interactive area: ~400–480pt (the main game surface)
- Action bar: ~60–80pt (primary CTA or status)
- Bottom safe area: variable (34pt+ on modern iPhones)

Total canvas: ~780–844pt on iPhone 14. Budget deliberately.

**Text legibility:** Cardo body text minimum 14pt. MedievalSharp display
text minimum 18pt. On dark void/900 or void/800 backgrounds, ensure text
contrast ratio ≥ 4.5:1 (WCAG AA). Test Cardo at small sizes — it is a
serif with fine strokes that can wash out on lower-resolution Android screens.

**One primary action per screen state.** At any moment, there should be
one visually dominant action available. Secondary actions should be visually
subordinate. If the player must choose between two equally prominent actions,
the layout has failed.

---

## PART 8 — IDLE GAME UI CONVENTIONS

These patterns are established across the idle/farming genre. Deviating
from them requires a specific reason grounded in The Loop's design.

**Always visible: current resource balance.** Mana balance must be visible
on every Tier 2 screen. It is the player's primary decision-making input.
Top-right or top-center are conventional positions.

**Progress must feel active.** Even passive states (waiting for next cycle
action, Factory queue running) should show animated indicators. A progress
bar that moves is more engaging than a static number. Floating "+mana"
numbers on yield events are expected by the genre.

**Introduce complexity gradually; grey out, don't hide.** Players should
always be able to see what is coming. Lock icons with unlock conditions
visible motivate continued play.

**The cycle count is a permanent progress marker.** Always visible. It is
the player's sense of long-term progress. Treat it with the same priority
as the mana balance.

**Return rewards.** When the player reopens the app, show what changed
since their last session (NPC requests arrived, Factory output ready,
achievements unlocked). This should be the first thing they see, not a
loading screen. The Dreaming is the natural landing screen — design it to
surface "what's new" at a glance.

---

## COMMON UX FAILURE PATTERNS

| Pattern | What it looks like | Correct behavior |
|---|---|---|
| Primary action out of thumb reach | "Advance cycle" button at top of screen | Move to lower 40% of canvas |
| Conflicting horizontal gesture | Horizontal scroll gallery on Rift screen | Replace with vertical scroll — swipe-right is reserved |
| Silent tap | Button press with no visual/audio/haptic response | Add at minimum a scale animation and sound |
| JS thread animation | Transition stutter when saving state | Wrap save in `InteractionManager.runAfterInteractions` |
| Missing empty state | Blank Communications Array before first NPC request | Design empty state with Familiar contextual message |
| Missing loading state | Blank screen during True Time fetch on app open | Add skeleton / loading indicator on Dreaming |
| Complexity dumped on new player | Faction renown panel visible from cycle 1 | Gate behind progressive disclosure (cycle 20+) |
| Too many equal-priority actions | Three equally prominent buttons on one screen | Establish clear primary / secondary / tertiary hierarchy |
| Safe area violation | Buttons behind home indicator on iPhone | Use `useSafeAreaInsets()` throughout |
| X to dismiss modal | Close button labeled with X icon only | Use labeled "Close" or "tap outside" pattern |

---

## Examples

**Example 1 — Touch target placement review**

Designer places the "Advance Cycle" button at the top of the Dreaming screen for visual balance. Skill fires on "button" / layout review context.

Skill catches:
- Primary action in top 40% of screen → HARD rule violation: move to lower 40%
- Button at 375pt width with no padding check → verify ≥ 48×48pt, ≥ 8pt gap from adjacent elements
- Safe area bottom not applied → add `useSafeAreaInsets().bottom` padding if near bottom edge

Correct output: "Advance Cycle" in the natural thumb zone (~bottom 40%), mana display top-right (hard reach zone is fine for status display).

**Example 2 — Gesture conflict check**

Developer proposes a horizontal swipe to cycle through active NPCs on the Dreaming screen. Skill fires on "gesture" keyword in UI design context.

Skill catches:
- Horizontal swipe on a Tier 2 screen → CONFLICT: swipe-right is Inventory, swipe-left is Codex. This gesture is already consumed.
- Replacement options: vertical swipe, tap-to-cycle with visible arrow affordance, or dedicated NPC panel accessible via tap

New gesture checklist applies: conflict with reserved gestures → redesign before implementation.

**Example 3 — Progressive disclosure audit**

Screen design spec shows faction renown bar visible from the start screen. Skill fires on layout spec review.

Skill catches:
- Faction renown is a Layer 3 element (Cycles 20+) — must not be visible from cycle 1
- Correct behavior: grey out with padlock glyph and "Unlocks at cycle 20" label
- Familiar intro message spec required for when the element first unlocks

---

## Out of Scope

This skill does NOT:
- Implement animations or gestures in code (utility-mobile-react-native)
- Enforce accessibility standards — colorblindness, screen readers, reduced motion (utility-game-accessibility)
- Define design system tokens, colors, or typography (loop-extended-code-guardian)
- Review lore accuracy or narrative tone (loop-extended-lore-checker)
- Apply balance math or retention curve design (utility-game-idle-math)

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-screen-inventory | Screen catalog — primary source for what each screen contains |
| loop-extended-code-guardian | Code quality — enforces design tokens in implementation |
| loop-extended-visual | Art direction — visual language governing layout aesthetics |
| utility-game-balance | Mechanic feel — complements UX when discussing feedback loops |
| utility-game-psychology | Audience profiling — why players respond to these patterns |
| objc.io — Designing Elegant Mobile Games | Nested feedback loops, session length, mobile game verb design |
| UX Planet — Game Design UX Best Practices | Data-driven patterns from 250+ mobile games |
| Sumo Digital — UI/UX for Mobile Game Development | Touch targets, haptics, accessibility for mobile games |
| Apple HIG — Human Interface Guidelines | iOS tap target sizes, safe areas, gesture standards |
| Expo Haptics documentation | expo-haptics API for React Native haptic implementation |
| React Native Reanimated documentation | UI-thread animation for 60fps interaction feedback |
