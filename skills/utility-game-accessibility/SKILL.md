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

# Mobile Game Accessibility Skill

Defines accessibility requirements for mobile games across all disability
categories. Distinguishes between what is built correctly by default vs.
what is exposed as a user-controlled setting. Contains extended Loop-specific
implementation details as the primary reference implementation.

---

## PART 1 — PREVALENCE AND SCOPE

Understanding who is affected grounds every design decision.

| Disability category | Prevalence in gamers | The Loop risk areas |
|---|---|---|
| **Color vision deficiency** | ~8% of male players (red-green most common) | Elemental palette, rarity system, status indicators |
| **Motor/physical** | Largest disability group among gamers (survey data) | Touch target size, timing-critical minigames, hold gestures |
| **Cognitive/learning** | Includes ADHD, dyslexia, processing differences | Text legibility, tutorial pacing, UI complexity |
| **Hearing** | ~17% of gamers have some hearing loss | Audio-only feedback events, NPC dialogue |
| **Visual (low vision)** | Second largest group; distinct from colorblindness | Contrast ratios, font scaling, icon legibility |
| **Vestibular/photosensitive** | Affects response to motion and flicker | Animations, screen transitions, particle effects |

**Key principle:** Disabled players account for approximately 31% of US
gamers. Accessibility is not an edge case — it is the default player base.
Additionally: features built for accessibility benefit all players. Subtitles
turned off by default in Assassin's Creed Origins — 60% of players turned
them on; defaulted on in Odyssey — 95% left them on. Design accessible
by default wherever possible.

**Two-tier structure:**
- **By default** — built in, always active, no player action required
- **Settings toggle** — available in the Accessibility section of Settings,
  off by default but surfaced clearly at first launch

---

## PART 2 — VISUAL ACCESSIBILITY

### 2.1 Color vision deficiency (CVD)

Red-green colorblindness (deuteranopia/protanopia) affects ~8% of male
players. Blue-yellow (tritanopia) is rarer (~0.01%) but should be considered.

**The Loop's CVD risk points — require explicit fixes:**

| System | Risk | Required fix |
|---|---|---|
| Elemental palette (Fire/Water/Earth/Air) | Fire=red, Earth=green are indistinguishable for deuteranopes | Every element must have a secondary differentiator: icon shape, symbol, or pattern — never color alone |
| Rarity system (item name colors) | Common/uncommon/rare distinction is color-only | Add rarity tier label text or icon badge alongside color |
| Mana bars | Element-specific mana colors may be indistinguishable | Mana bar must also show element icon; color is accent not sole identifier |
| Foraging minigame zones | Success/failure zones may use red/green | Use shape or position as primary differentiator; color as secondary |
| Status indicators | Any state communicated by color alone (e.g., available/unavailable) | Add icon, pattern, or text state indicator |

**The non-negotiable rule — apply everywhere:** Information conveyed by color must also be conveyed by at least one other means (shape, icon, text label, pattern, position, or animation).

This rule applies to every system in the game. No exceptions. When auditing
any screen or component, ask: "If all color were removed, would this still
be fully understandable?" If not, it fails.

**CVD-safe default palette approach:**
- Avoid red+green as paired signals (the most common failure pattern)
- Prefer blue+orange as a safe high-contrast pair for binary states
- Use distinctive shapes or icons alongside any color-coded system
- A colorblind mode toggle (Settings) can offer alternative palettes, but
  the default experience must be functional without it

**Colorblind mode (Settings toggle):**
Offer at minimum a filter setting: deuteranopia / protanopia / tritanopia /
achromatopsia. This shifts accent colors while preserving The Loop's dark
fantasy visual identity. The mode adjusts `theme.js` tokens — it does not
redesign the UI.

### 2.2 Contrast ratios

**By default — mandatory compliance:**

| Text type | Required ratio | Standard |
|---|---|---|
| Body text / UI labels (Cardo, <18pt) | 4.5:1 | WCAG AA |
| Large text / headings (MedievalSharp, ≥18pt) | 3:1 | WCAG AA |
| UI components (icons, borders, interactive elements) | 3:1 | WCAG AA |
| Status/semantic colors (success/error/warning) | 4.5:1 | WCAG AA |

The Loop's dark void/900 background is inherently high-contrast for light
text — this is a natural advantage. The risk is mid-tone text on mid-tone
backgrounds (e.g., dimmed labels, secondary text, disabled states). Every
disabled/secondary text color must still pass 3:1 minimum.

**High contrast mode (Settings toggle):**
Increases all text to pure white on void/900, removes decorative gradients
on text, and increases icon stroke weight. Maps to OS-level high contrast
if enabled.

### 2.3 Font scaling

iOS Dynamic Type and Android font scaling must be respected. The Loop's UI
must not break at large text sizes.

**By default:**
- Never use hardcoded font sizes in `StyleSheet`. Always use `fontSize`
  tokens from `theme.js`.
- All text containers must allow wrapping — no `numberOfLines={1}` truncation
  on text that carries essential information.
- Test the UI with iOS Accessibility → Larger Text set to maximum.
  If any screen breaks, it fails.

**Accessible font size toggle (Settings):**
Offer a text size multiplier (Normal / Large / Extra Large) that scales all
Cardo body text up by 1.15× and 1.35× respectively. MedievalSharp display
text scales at 1.1× and 1.2× (more conservative — preserves atmosphere).

### 2.4 Screen reader support (VoiceOver / TalkBack)

**By default — required on all interactive elements:**

```javascript
// Every custom interactive element requires:
<TouchableOpacity
  accessible={true}
  accessibilityRole="button"           // tells screen reader: this is a button
  accessibilityLabel="Draw Cards"      // what it is — descriptive, not generic
  accessibilityHint="Opens Cards of Fate for this cycle"  // what it does
  onPress={handleDraw}
>
```

**Required accessibilityRole values for The Loop's component types:**

| Component | accessibilityRole |
|---|---|
| Action buttons (Draw, Forage, Advance) | `"button"` |
| Location navigation (Dreaming/Rift/Tower) | `"button"` |
| Item cards (Inventory) | `"button"` (if tappable) |
| Screen headers | `"header"` |
| Mana bar / progress indicators | `"progressbar"` |
| Toggle switches (Settings) | `"switch"` |
| Images / elemental art | `"image"` |

**Rules:**
- `accessibilityLabel` must describe the element, not its visual appearance.
  "Fire elemental, Level 3, generating 240 mana per cycle" not "Flame image."
- Group related elements: use `accessible={true}` on a wrapper View to
  collapse a visual cluster into one screen reader announcement.
- Do not use `accessible={true}` on decorative elements — they add noise.
- Dynamic content changes (mana earned, cycle advancing) must use
  `accessibilityLiveRegion="polite"` so screen readers announce updates.

**The Loop does not require full screen-reader-only gameplay** (that would
require audio game design). But every UI element must be navigable and
describable by screen readers. A blind player cannot play the minigames but
must be able to navigate every menu, read every notification, and access
all settings.

---

## PART 3 — MOTOR ACCESSIBILITY

**By default:**
- Minimum touch target: 48×48pt on all interactive elements (enforced in
  code-guardian)
- No required multi-finger gestures — every action achievable by single tap
  or single swipe
- Swipe navigation (Inventory, Codex) must have button alternatives for
  players who cannot use swipe gestures

**Settings toggles:**
- **Tap-hold alternatives:** Anywhere a hold gesture is used (item long-press
  for detail view), offer a tap-then-tap alternative
- **Minigame timing assistance:** Speed reduction for the Foraging dial and
  any other timing-critical mechanics. Store as `accessibility_speed_reduction`
  in PlayerSettings (already in the data model)
- **Haptic toggle:** Already required by mobile-ux skill; confirm it gates
  all haptic events, not just some

**Minigame-specific — timing:**
The Foraging minigame requires precision timing. This is a motor barrier.
The speed reduction setting directly addresses this. The game accessibility
guidelines (GAG) classify "do not make precise timing essential" as an
advanced guideline — The Loop addresses it via the speed reduction toggle
rather than eliminating timing entirely, which is an acceptable balance.

---

## PART 4 — COGNITIVE ACCESSIBILITY

**By default — these must be true at launch, no toggle required:**

- Tutorial can be replayed at any time via Settings → Tutorial
- All NPC dialogue advances at player pace (tap to continue — never
  auto-advancing text)
- Simple clear language throughout UI copy (Familiar's guidance text must
  be readable at approximately Grade 8 level)
- No information conveyed by icon alone — all icons have text labels or
  accessible tooltips
- Separate volume controls for SFX, music, and ambient audio

**Settings toggles:**
- **Reduce background motion:** Disables ambient animations on location
  screens (floating particles, breathing effects). Uses
  `AccessibilityInfo.isReduceMotionEnabled()` to respect OS setting and
  additionally offers an in-app toggle.
- **Tutorial reminders:** Re-surface contextual help hints for systems
  the player hasn't interacted with recently

**Dyslexia note:**
Cardo is a serif font — serifs are generally considered harder to read for
dyslexic players. A dyslexia-friendly font option (e.g., OpenDyslexic) is
an advanced feature. Flag as a post-launch improvement, not a v1 blocker.
The minimum requirement is: ensure adequate line height (1.5× minimum),
adequate letter spacing, and sufficient contrast. These are in-scope for v1.

---

## PART 5 — HEARING ACCESSIBILITY

The Loop is not audio-dependent — the core loop functions without sound.
However, audio events carry information that should have visual equivalents.

**By default:**
- All audio feedback events (successful forage, cycle advance, NPC arrival)
  must have a visual equivalent. Not an optional subtitle — a native visual
  response. The visual feedback is primary; audio is layered on top.
- NPC communications arrive as text — no hearing accessibility barrier for
  the core NPC system.

**Settings toggles:**
- **Subtitles/captions:** For any voiced content (if The Loop adds voice acting
  post-launch). Not applicable to v1 unless voiced tutorial is implemented.
- **Visual audio indicators:** On-screen flash or icon when an audio event
  fires (for players with audio off). Optional — audio off is already
  functional by design since all feedback has visual primacy.

---

## PART 6 — VESTIBULAR AND PHOTOSENSITIVE ACCESSIBILITY

**By default:**
- No flashing or rapidly strobing visual effects anywhere in the game.
  The Loop's aesthetic is slow and atmospheric — this is naturally aligned.
- Screen transitions must use smooth fades or dissolves, not rapid cuts
  or flashes.
- Particle effects (mana collection, elemental effects) must not include
  rapid strobing patterns.

**Settings toggle — reduce motion:**
- Disables all non-essential animations: ambient particle systems, location
  breathing effects, card flip animations (replace with instant state change),
  screen transition animations (replace with crossfade or cut).
- Implements `AccessibilityInfo.isReduceMotionEnabled()` to automatically
  apply this when the OS setting is on. Offer in-app toggle for players
  who want it without using the OS setting.

```javascript
import { AccessibilityInfo } from 'react-native';

// Check OS reduced motion preference
const isReduceMotion = await AccessibilityInfo.isReduceMotionEnabled();

// Subscribe to changes
AccessibilityInfo.addEventListener('reduceMotionChanged', (isEnabled) => {
  setReduceMotion(isEnabled);
});
```

---

## PART 7 — SETTINGS SCREEN REQUIREMENTS

The Accessibility section of Settings must surface all toggles cleanly.
Group by category. Surface at first launch as an optional step.

```
ACCESSIBILITY SETTINGS
─────────────────────
Vision
  [ ] Colorblind mode      [Deuteranopia / Protanopia / Tritanopia / None]
  [ ] High contrast text
  [ ] Text size            [Normal / Large / Extra Large]

Motion
  [ ] Reduce motion        (also auto-detects OS setting)
  [ ] Reduce background animations

Gameplay
  [ ] Speed reduction      [Off / 75% / 50%]  (affects minigame timing)
  [ ] Tap alternatives for hold gestures

Audio
  [ ] Sound effects
  [ ] Music
  [ ] Haptic feedback
  [ ] Ambient audio
```

All settings stored in `PlayerSettings` (Supabase) and cached in
`loop:settings_cache` (MMKV). Applied on app load before first frame renders.

---

## PART 8 — ACCESSIBILITY AUDIT CHECKLIST

Run this when auditing any screen or component for accessibility readiness.

```
ACCESSIBILITY AUDIT — [Screen/Component]

Color-as-sole-signifier: [Pass / Fail — describe violation]
Contrast ratios: [Pass / Fail — list failing elements]
Font scaling: [Pass / Fail at max text size]
Touch targets: [Pass / Fail — minimum 48×48pt]
Screen reader labels: [Complete / Missing — list elements]
Accessible roles: [Complete / Missing — list elements]
Motion/flicker: [Pass / Fail]
Audio has visual equivalent: [Pass / Fail — list events]
Verdict: [Accessible / Needs work — specific gaps]
```

---

## COMMON FAILURE PATTERNS

| Pattern | Loop-specific example | Correct behavior |
|---|---|---|
| Color-only rarity indication | Legendary item name in gold, no other differentiator | Add rarity badge icon or tier label text |
| Elemental color-only identity | Fire element displayed in red with no icon | Always pair element color with dedicated element icon |
| Unlabeled icon button | Codex swipe arrow with no accessibilityLabel | `accessibilityLabel="Open Codex"` + `accessibilityRole="button"` |
| Minigame timing with no accommodation | Foraging dial at fixed speed with no reduction option | Speed reduction setting must affect all timing mechanics |
| Animation with no reduced motion path | Card flip animation always plays | Gate via `AccessibilityInfo.isReduceMotionEnabled()` |
| Text that breaks at large sizes | Item name truncated with `numberOfLines={1}` | Allow wrapping; test at iOS maximum text size |
| Settings buried post-launch | Accessibility options added as afterthought | Accessibility section in Settings from launch; surface at first run |

---

## SEE ALSO

| Resource | Domain |
|---|---|
| gameaccessibilityguidelines.com — Full list | Industry gold standard; Basic tier = must-have for v1 |
| WCAG 2.2 guidelines | Web/app contrast and interaction standards |
| React Native Accessibility docs (reactnative.dev) | `accessibilityRole`, `accessibilityLabel`, `AccessibilityInfo` API |
| AbleGamers / Can I Play That? | Game accessibility advocacy and review resources |
| loop-extended-code-guardian | Enforces accessibility props in generated code |
| loop-mobile-ux | Touch target sizes, haptic gating, motion sensitivity |
| loop-data-model | PlayerSettings schema — accessibility fields |
