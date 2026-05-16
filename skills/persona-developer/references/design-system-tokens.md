# Design System Tokens — Developer Reference

Token specification for The Loop. Defines what tokens exist and their values.
For code enforcement (how to use tokens in components), see design-system-rules.md.

---

## TOKEN ARCHITECTURE

Three-tier system: Primitive → Semantic → Component.

**Primitive tokens** — raw values, never imported directly in components:
```javascript
// Format: [family]/[scale]  e.g. void/900, fire/500
// Scale: 50–950 (50 = lightest, 950 = darkest)
void_[900], fire[500], earth[300], dreaming[900]
```

**Semantic tokens** — roles, never raw values — what components import:
```javascript
// Format: role  e.g. surface.primary, text.primary, mana.fire
// These map to primitives in theme.js
```

**Component tokens** — element-specific overrides only when genuinely diverging:
```javascript
// Format: [component]/[variant]  e.g. manaBar.fire, cardBorder.rarityRare
// Only create when a component diverges from semantic defaults
```

**Performance rule:** All tokens must be defined in `theme.js` and imported via
`StyleSheet.create`. Never inline. Inline styles create new objects on every render
(30–50% performance degradation on lower-end devices).

---

## LOCKED RULES — APPLY BEFORE GENERATING ANY TOKEN

**Fonts (LOCKED):**
- `fonts.display` (MedievalSharp): headings and display only. Never body, label, button, or UI.
- `fonts.body` / `fonts.bodyBold` / `fonts.bodyItalic` (Cardo): all other text.

**Backgrounds (LOCKED):**
- Default: `void_[900]` or `void_[800]`.
- Never use rarity colors on backgrounds or borders.

**Rarity colors (LOCKED):**
- Appear on item name text only. Never backgrounds, borders, or icons.

**Mana bars (LOCKED):**
- Always use element-specific mana color token for bar fill.

**Semantic colors (LOCKED):**
- `semantic.success/error/warning/info` appear only as notification banners or toasts.
- Never on gameplay elements.

---

## BACKGROUND TOKEN MAP

| Screen / Context | Token |
|---|---|
| Default / hub / menus | `void_[900]` |
| The Dreaming | `dreaming[900]` |
| The Tower | `tower[900]` |
| The Rift (no elemental) | `rift[900]` |
| The Rift (elemental active) | `[element][900]` |
| The Void (intro) | `void_[400]` |

---

## ELEMENTAL PALETTE — REQUIRED TOKENS PER ELEMENT

Each elemental requires this minimum semantic token set:

```javascript
mana.[element]              // mana bar fill
element.[element].glow      // summoned state ambient glow
element.[element].text      // accent text when elemental is active
element.[element].bgSubtle  // background-safe tinted surface
```

**Hue direction:**
- Fire, Air: warm/active (orange-red-gold, yellow-cyan)
- Water, Earth: cool/receptive (blue-teal, green-brown)
- Mana/Aether: neutral liminal (lavender or soft white)
- Shadow, Light, Void, Nature, 11th: OPEN — flag as OPEN until confirmed

**Accessibility requirement on all elemental tokens:**
- Fire (red-orange) and Earth (green-brown) must be distinguishable in
  Deuteranopia and Protanopia simulations.
- Every elemental color token must pair with a symbol identifier.

---

## RARITY TIER TOKENS

Rarity tier count is OPEN — do not lock token names until confirmed.
When confirmed, pattern: `rarity.[tierName]` (e.g. `rarity.common`, `rarity.legendary`)

All rarity colors must achieve WCAG AA (4.5:1) against `void_[900]`.
Must distinguish tiers without relying on red/green differentiation.

---

## TYPOGRAPHY SCALE

React Native uses unitless numbers — not `px`, `sp`, or `rem`.

| Role | Token | Font | Size (logical px) | Weight |
|---|---|---|---|---|
| Display | `fontSize.display` | MedievalSharp | 28–40 | Regular |
| Heading 1 | `fontSize.h1` | MedievalSharp | 22–26 | Regular |
| Heading 2 | `fontSize.h2` | MedievalSharp | 18–20 | Regular |
| Body | `fontSize.body` | Cardo | 14–16 | Regular |
| Label | `fontSize.label` | Cardo | 12–14 | Regular |
| Button | `fontSize.button` | Cardo | 14–16 | Bold |
| Notification | `fontSize.notification` | Cardo | 12 | Regular |

**Font scaling implementation:**
```javascript
// allowFontScaling defaults true — never override for body/label
// maxFontSizeMultiplier acceptable for display/heading only
<Text style={{ fontFamily: fonts.display, fontSize: fontSize.display }}
  maxFontSizeMultiplier={1.3}  // Heading only — preserve layout
>
```

Test at 85%, 100%, 130%, and 200% system font scale.
Use `PixelRatio.getFontScale()` when computing scaled values at runtime.

---

## SPACING SYSTEM (BASE-8)

All spacing values are multiples of 4 or 8.

| Token | Value | Usage |
|---|---|---|
| `space[1]` | 4dp | Tight internal padding |
| `space[2]` | 8dp | Standard internal padding |
| `space[3]` | 12dp | Card internal padding |
| `space[4]` | 16dp | Standard section gap |
| `space[6]` | 24dp | Card gap |
| `space[8]` | 32dp | Major section separation |
| `space[12]` | 48dp | Screen edge margins |

---

## ICON SPEC

- Base size: 24×24dp
- Stroke weight: 2dp
- Line caps: rounded
- Fill: none (outline only for UI icons)
- Corner radius on containing shapes: 4dp
- Elemental icons: use canonical Ritual system symbols (secondary identifier
  required by accessibility constraint — color is not sole signal)
- Status icons: standard semantic shapes (check, X, alert triangle, info circle)
  — never use elemental symbols for semantic states

---

## ANIMATION DURATION TOKENS

| Type | Duration |
|---|---|
| Microinteractions (tap feedback, toggle) | 100–150ms |
| Panel transitions | 250–300ms |
| Reward animations (upgrade, evolution) | 400–600ms |
| Idle animations (breathing, ambient) | 2000–4000ms loop |

Standard easing: `cubic-bezier(0.4, 0.0, 0.2, 1.0)` (Material standard).

**Reduced motion fallback — required on all animations:**
All animations must degrade to instant state change or single-frame crossfade
when `prefers-reduced-motion` is active. Never remove informational transitions
entirely — replace with opacity fade.
