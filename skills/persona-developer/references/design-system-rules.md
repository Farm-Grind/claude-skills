# Design System Rules — The Loop

Source: loop-extended-code-guardian v1.1

---

## COLOR TOKENS — CRITICAL

All colors MUST be imported from `theme.js`. Hardcoded hex values are a
code error, not a style preference.

```javascript
// ✅ CORRECT
import { void_, dreaming, fire, mana, rarity } from '../theme';
backgroundColor: void_[900]

// ❌ NEVER — hardcoded hex
backgroundColor: '#010202'
```

If `theme.js` doesn't have a token for what's needed, add a comment:
```javascript
// TODO: add to theme.js — needs a token for [description]
```

---

## TYPOGRAPHY — CRITICAL

Two fonts only. No exceptions.

| Use | Font token |
|---|---|
| Game titles, section headers, item names, location labels | `fonts.display` (MedievalSharp) |
| Everything else — body, labels, buttons, tooltips, UI text | `fonts.body` / `fonts.bodyBold` / `fonts.bodyItalic` (Cardo) |

```javascript
import { fonts, fontSize } from '../theme';
// ✅ fontFamily: fonts.display, fontSize: fontSize.heading
// ✅ fontFamily: fonts.body, fontSize: fontSize.body
// ❌ NEVER: fontFamily: 'Arial', fontSize: 16
```

---

## BACKGROUND COLORS — CRITICAL

| Screen type | Background |
|---|---|
| Default / hub / menus | `void_[900]` |
| The Dreaming / farm screens | `dreaming[900]` |
| The Tower | `tower[900]` |
| The Rift (neutral) | `rift[900]` |
| The Rift (elemental active) | Element palette `[900]` |
| The Void | `void_[400]` (lightest usable) |

---

## COLOR SYSTEM RULES — HIGH

- **Mana colors** — only on mana bars and mana counters. Never decorative.
- **Rarity colors** — only on item name text. Never backgrounds, borders, icons.
- **Semantic colors** (`semantic.success/error/warning/info`) — only for
  notification banners and toast messages. Never gameplay elements.
- **No mixing location palettes** on the same screen.

---

## ACCESSIBILITY — HIGH

Every interactive element requires accessibility props. Non-negotiable.

```javascript
<TouchableOpacity
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel="Draw Cards"
  accessibilityHint="Opens Cards of Fate for this cycle"
  onPress={handleDraw}
>
```

**accessibilityRole reference:**

| Component type | Role |
|---|---|
| Any tappable button | `"button"` |
| Screen/section header | `"header"` |
| Mana bar, progress indicator | `"progressbar"` |
| Settings toggle | `"switch"` |
| Decorative image | `"image"` |
| Informational text | `"text"` |

**Color-as-sole-signifier — CRITICAL:**
Information conveyed by color must also be conveyed by icon, text label,
shape difference, or position difference. Never color alone.

**Reduced motion — required on all animations:**

```javascript
import { AccessibilityInfo } from 'react-native';
const [reduceMotion, setReduceMotion] = useState(false);
useEffect(() => {
  AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
  const sub = AccessibilityInfo.addEventListener('reduceMotionChanged', setReduceMotion);
  return () => sub.remove();
}, []);
const animDuration = reduceMotion ? 0 : 300;
```

**Minimum touch target:** 48×48pt. Use `hitSlop` to expand without visual change.

---

## AUTO-FIX PATTERNS

| Violation | Fix |
|---|---|
| `color: '#CCBA8E'` | `color: dreaming[400]` + add theme import |
| `fontSize: 16` | `fontSize: fontSize.body` + add theme import |
| `fontFamily: 'Georgia'` | `fontFamily: fonts.body` |
| `backgroundColor: 'black'` | `backgroundColor: void_[900]` |

---

## POST-GENERATION AUDIT

1. Hex scan — search output for `#` followed by 3 or 6 hex chars outside comments
2. Font scan — search for any font family string not in the approved set
3. Import check — `theme` imported and all visual values reference it
4. Accessibility scan — every interactive element has role, label, hint
5. Color-only signifier scan — no state/identity conveyed by color alone
