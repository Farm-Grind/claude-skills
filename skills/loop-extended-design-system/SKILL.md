---
name: loop-extended-design-system
description: >
  Generates, audits, and extends The Loop Design System content: color token
  decisions for all confirmed elementals, rarity tiers, UI system colors, typography
  scale, spacing rules, component inventory, and icon/animation principles.
  Distinct from loop-extended-code-guardian (code compliance) and
  loop-extended-visual (art direction). Outputs token values, naming
  conventions, and doc-ready specs — not code. Use automatically — do not
  wait to be asked.
  Trigger on ANY of these signals: a color token is being decided or audited;
  typography scale is being set; component inventory is being built; icon or
  animation principles are being written; "design system token", "color token",
  "rarity color", "elemental palette", "typography scale", "spacing system",
  "component inventory"; MAN-22, MAN-32, MAN-33, or MAN-34 work is active.
  Do NOT trigger for: enforcing tokens in code (loop-extended-code-guardian);
  art direction (loop-extended-visual); accessibility audit
  (utility-game-accessibility). Load once per session.
---
SKILL_VERSION: v1.2

# The Loop — Design System Builder

Produces and audits all design token content for The Loop Design System
document. Every output is doc-ready and code-guardian-compatible.

---

## PART 1 — LOCKED DESIGN SYSTEM RULES

**HARD FAIL:** MUST NOT generate any token or specification before reviewing all rules in this section.

Apply before generating any token or specification.

**Fonts (LOCKED):**
- MedievalSharp: headings and display only. Never body, label, button, or UI.
- Cardo: all body, label, button, and UI text.

**Backgrounds (LOCKED):**
- Default: void/900 or void/800.
- Never use rarity colors on backgrounds or borders.

**Rarity color rule (LOCKED):**
- Rarity colors appear on item name text only.

**Mana bars (LOCKED):**
- Always use element-specific mana color token for the bar.

**Rift palette rule (LOCKED):**
- Rift uses neutral palette until an elemental is summoned. Once summoned,
  transitions to the elemental's color register.

**Semantic colors (LOCKED):**
- Semantic colors (success/warning/error/info) appear only as notification
  banners or toasts.

---

## PART 2 — COLOR TOKEN ARCHITECTURE

The Loop uses a three-tier token system: Primitive → Semantic → Component.

**Primitive tokens** — raw color values, named by family and scale:
Format: `[family]/[scale]` e.g. `void/900`, `fire/500`, `earth/300`
Scale: 50–950 (50 = lightest, 950 = darkest). Void scale is the background
family. Each elemental family needs a full working range (50–900 minimum).

**Semantic tokens** — roles, never raw values:
Format: `[role]` e.g. `surface/primary`, `text/primary`, `mana/fire`
Map to primitives. These are what code imports.

**Component tokens** — element-specific overrides:
Format: `[component]/[variant]` e.g. `mana-bar/fire`, `card-border/rarity-rare`
Only create when a component genuinely diverges from semantic defaults.

### Elemental palette requirements

Each elemental needs a minimum set of semantic tokens:
- `mana/[element]` — the mana bar fill color
- `element/[element]/glow` — the summoned state ambient glow
- `element/[element]/text` — accent text when the elemental is active
- `element/[element]/bg-subtle` — a background-safe tinted surface

Fire and Air: warm/active hue range (orange-red-gold, yellow-cyan).
Water and Earth: cool/receptive hue range (blue-teal, green-brown).
Mana/Aether: neutral liminal — no dedicated tarot suit. Lavender or soft white.
Shadow, Light, Void, Nature, 11th: TBD pending MAN-31. Flag as OPEN.

### Rarity tier tokens (item name text only)

Rarity tier count is OPEN — not confirmed in the decisions log. Do not lock
token names or count until a decision is made. When confirmed, token names
follow the pattern: `rarity/[tier-name]` (e.g. `rarity/common`,
`rarity/rare`, `rarity/legendary`).

Rarity colors must be WCAG AA compliant against void/900 background.
Check contrast ratio before assigning any rarity hex value.

### Accessibility requirements on all color tokens

- Minimum 4.5:1 contrast ratio for text tokens against their expected background.
- Color is never the sole signal — every elemental color token must pair with
  a symbol identifier (the elemental symbols from the Ritual system).
- Colorblindness check: fire (red-orange) and earth (green-brown) must be
  distinguishable in both Deuteranopia and Protanopia simulations.
- Rarity token colors: at minimum distinguish common/rare/legendary without
  relying on red/green differentiation.

---

## PART 3 — TYPOGRAPHY SCALE

Produce the full scale before any coding begins (MAN-33). Required roles:

| Role | Font | Size range | Weight | Usage |
|---|---|---|---|---|
| Display | MedievalSharp | 28–40sp | Regular | Screen titles |
| Heading 1 | MedievalSharp | 22–26sp | Regular | Section headers |
| Heading 2 | MedievalSharp | 18–20sp | Regular | Subsection headers |
| Body | Cardo | 14–16sp | Regular | All body text |
| Label | Cardo | 12–14sp | Regular | UI labels, captions |
| Button | Cardo | 14–16sp | Bold | Buttons, CTAs |
| Notification | Cardo | 12sp | Regular | Toasts, banners |

React Native font sizing note: React Native uses unitless numbers, not `sp`
or `px`. The values in the table above are reference targets in logical pixels.
Font scaling is controlled via the `allowFontScaling` prop (default true —
never set to false for body/label copy) and `maxFontSizeMultiplier` for
display/heading styles only. Test at 85%, 100%, 130%, and 200% system font
scale. Use `PixelRatio.getFontScale()` when computing scaled values at runtime.

---

## PART 4 — SPACING SYSTEM

Use a base-8 grid. All spacing values are multiples of 4 or 8.

| Token | Value | Usage |
|---|---|---|
| space/1 | 4dp | Tight internal padding |
| space/2 | 8dp | Standard internal padding |
| space/3 | 12dp | Card internal padding |
| space/4 | 16dp | Standard section gap |
| space/6 | 24dp | Card gap |
| space/8 | 32dp | Major section separation |
| space/12 | 48dp | Screen edge margins |

Touch targets: minimum 44×44dp per Apple HIG / Android minimum 48×48dp.
Safe area: always defer to SafeAreaView. Never hardcode status bar offsets.

---

## PART 5 — COMPONENT INVENTORY PROCESS

The component inventory must cover every screen in the Screen Inventory (MAN-11
must be complete first). Produce entries in this format:

```
COMPONENT: [name]
Used on screens: [list screen names]
Variants: [list variants — e.g. active/inactive, elemental-tinted/neutral]
Token dependencies: [list semantic tokens this component uses]
Accessibility: [any specific requirements beyond defaults]
```

Component categories required for v1:
- Navigation (tab bar, back controls, modal headers)
- Cards (elemental card, item card, NPC card, achievement card)
- Mana bars (per element, neutral state)
- Buttons (primary, secondary, destructive, disabled)
- Progress indicators (depth meter, upgrade progress)
- Notifications (toast, banner — semantic colors only)
- Modals (confirmation, info, exchange prompt)
- Input fields (Ritual code entry, nickname entry)

---

## PART 6 — ICON AND ANIMATION PRINCIPLES

### Icon style (MAN-34)

All icons use: 24×24dp base size, 2dp stroke weight, rounded line caps,
no fill (outline only for UI icons), 4dp corner radius on containing shapes.
Elemental icons: use the canonical Ritual system symbols — these are the
secondary identifier required by the accessibility constraint.
Status icons: use standard semantic shapes (check, X, alert triangle, info
circle) — never use elemental symbols for semantic states.

### Animation principles (MAN-34)

Standard easing: cubic-bezier(0.4, 0.0, 0.2, 1.0) — material standard.
Duration standards:
- Microinteractions (tap feedback, toggle): 100–150ms
- Panel transitions: 250–300ms
- Reward animations (upgrade, evolution): 400–600ms
- Idle animations (elemental breathing, mana flow): 2000–4000ms loop

Reduced motion fallback: all animations must degrade to instant state change
or a single-frame cross-fade when `prefers-reduced-motion` is active.
Never remove informational transitions entirely — replace with opacity fade.

---

## Out of Scope

This skill does NOT:
- Enforce design system tokens in React Native code (use loop-extended-code-guardian)
- Define art direction, visual influences, or reference aesthetics (use loop-extended-visual)
- Run full accessibility audits across five disability categories (use utility-game-accessibility)
- Make decisions about elemental count or rarity tier count — those are locked via decisions log
- Generate code output of any kind — tokens and specs only

---

## Examples

**Example 1 — Color token audit request**

User: "Audit the fire elemental tokens against the design system rules."

Skill fires. Part 1 LOCKED rules loaded first. Output:

```
FIRE ELEMENTAL TOKEN AUDIT

Primitive tokens required:
  fire/50  fire/100  fire/200  fire/300  fire/400  fire/500
  fire/600  fire/700  fire/800  fire/900

Semantic tokens required:
  mana/fire                  — mana bar fill
  element/fire/glow          — summoned state ambient glow
  element/fire/text          — accent text when fire elemental active
  element/fire/bg-subtle     — background-safe tinted surface

Accessibility checks:
  ✓ element/fire/text must achieve 4.5:1 against void/900
  ✓ fire vs earth: must be distinguishable in Deuteranopia and Protanopia
  ✓ fire symbol identifier required alongside any fire color token

OPEN: Rarity tier count not confirmed — rarity/fire-tier tokens deferred until D-rarity-lock.
```

**Example 2 — Component inventory entry**

User: "Write the component inventory entry for the mana bar."

Skill fires. Part 5 process loaded.

```
COMPONENT: mana-bar
Used on screens: Home (Ritual hub), Rift, Tower, Source, any screen showing active elemental
Variants: fire / air / water / earth / mana / neutral (no elemental summoned)
Token dependencies: mana/[element] (fill), void/900 (track background), element/[element]/glow (summoned pulse)
Accessibility: bar must use element symbol icon alongside color fill — color is not the sole signal (see utility-game-accessibility)
```

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-code-guardian | Enforcing tokens in React Native code |
| loop-extended-visual | Art direction, reference aesthetic, synthesis |
| utility-game-accessibility | Full accessibility audit against five disability categories |
