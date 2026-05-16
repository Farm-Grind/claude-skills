# Accessibility — Developer Reference

React Native accessibility implementation rules.
Design philosophy excluded — this covers what must be in code.

---

## THE NON-NEGOTIABLE RULE

> Information conveyed by color must also be conveyed by at least one other
> means: shape, icon, text label, pattern, position, or animation.

Apply everywhere. No exceptions. Audit question: "If all color were removed,
would this still be fully understandable?" If not, it fails.

---

## CONTRAST RATIOS (WCAG AA — mandatory)

| Text type | Required ratio |
|---|---|
| Body text / UI labels (<18pt) | 4.5:1 |
| Large text / headings (≥18pt) | 3:1 |
| UI components (icons, borders, interactive) | 3:1 |
| Status/semantic colors (success/error/warning) | 4.5:1 |
| Disabled/secondary text | 3:1 minimum — not exempt |

---

## FONT SCALING

Never hardcode font sizes. Always use theme tokens.

```javascript
// ❌ NEVER
fontSize: 16

// ✅ CORRECT
fontSize: fontSize.body  // from theme.js
```

- `allowFontScaling` defaults to `true` — never set it `false` on body or label text.
- `maxFontSizeMultiplier` is acceptable on display/heading text only (preserves layout).
- Never use `numberOfLines={1}` on text that carries essential information.
- Test at iOS maximum text size setting before shipping any screen.

---

## SCREEN READER PROPS

Every custom interactive element requires all applicable props:

```javascript
<TouchableOpacity
  accessible={true}
  accessibilityRole="button"        // or `role="button"` (New Architecture)
  accessibilityLabel="Draw Cards"   // what it IS — descriptive
  accessibilityHint="Opens Cards of Fate for this cycle"  // what it DOES
  accessibilityState={{ disabled: isDisabled }}
  onPress={handleDraw}
>
```

**New Architecture note:** `role` prop takes precedence over `accessibilityRole`.
Include both for backward compatibility during transition:
```javascript
role="button"
accessibilityRole="button"
```

### accessibilityRole reference

| Component | Role |
|---|---|
| Tappable button | `"button"` |
| Screen / section header | `"header"` |
| Progress bar, mana bar | `"progressbar"` |
| Settings toggle | `"switch"` |
| Decorative image | `"image"` |
| Image that is also tappable | `"imagebutton"` |
| Navigation link | `"link"` |

### accessibilityState — required for stateful elements

```javascript
// Communicates disabled/selected/checked/expanded/busy to screen readers
accessibilityState={{
  disabled: isDisabled,    // button is not interactive
  selected: isSelected,    // item is selected in list
  checked: isChecked,      // checkbox/toggle state
  busy: isLoading,         // element is loading
  expanded: isExpanded,    // accordion/drawer is open
}}
```

### accessibilityValue — required for range-based elements

```javascript
// Progress bars, sliders, mana bars
accessibilityValue={{ min: 0, max: 100, now: currentMana }}
```

### Dynamic content announcements

```javascript
// Android: accessibilityLiveRegion on the updating element
<View accessibilityLiveRegion="polite">
  <Text>{statusMessage}</Text>
</View>

// iOS: programmatic announcement
import { AccessibilityInfo } from 'react-native';
AccessibilityInfo.announceForAccessibility('Mana gained: 240');
```

Use `"polite"` for non-urgent updates (mana gained, item received).
Use `"assertive"` for critical alerts (error, session ending).

### Grouping related elements

```javascript
// Collapse visual clusters into one announcement
<View accessible={true} accessibilityLabel="Fire elemental, Level 3, 240 mana per cycle">
  <ElementIcon />
  <ElementName />
  <ManaOutput />
</View>
```

Do not use `accessible={true}` on purely decorative elements — adds noise.

---

## REDUCED MOTION

```javascript
import { AccessibilityInfo } from 'react-native';
import { useEffect, useState } from 'react';

const [reduceMotion, setReduceMotion] = useState(false);

useEffect(() => {
  AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
  const sub = AccessibilityInfo.addEventListener('reduceMotionChanged', setReduceMotion);
  return () => sub.remove();
}, []);

// Gate all animations
const animDuration = reduceMotion ? 0 : 300;
```

Reduced motion must degrade to instant state change or single-frame crossfade.
Never remove informational transitions entirely — replace with opacity fade.

---

## TOUCH TARGET ACCESSIBILITY

Minimum 48×48pt. Use `hitSlop` to expand without changing visual size:
```javascript
hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
```

Provide tap alternatives everywhere hold gestures are used.

---

## ACCESSIBILITY SETTINGS (PlayerSettings Schema)

Settings stored in `PlayerSettings` (Supabase) + `loop:settings_cache` (MMKV).
Applied before first frame renders.

Required settings fields:
- `colorblind_mode` — enum: deuteranopia / protanopia / tritanopia / none
- `high_contrast` — boolean
- `text_size` — enum: normal / large / extra_large
- `reduce_motion` — boolean (also auto-detects OS)
- `reduce_background_animations` — boolean
- `accessibility_speed_reduction` — enum: off / 75pct / 50pct
- `haptic_enabled` — boolean
- `sfx_enabled` — boolean
- `music_enabled` — boolean

---

## ACCESSIBILITY AUDIT CHECKLIST

```
ACCESSIBILITY AUDIT — [Screen/Component]

Color-as-sole-signifier: [Pass / Fail — describe violation]
Contrast ratios: [Pass / Fail — list failing elements]
Font scaling: [Pass / Fail at max text size]
Touch targets: [Pass / Fail — minimum 48×48pt]
accessibilityRole: [Complete / Missing — list elements]
accessibilityLabel: [Complete / Missing — list elements]
accessibilityState: [Complete / Missing — list stateful elements]
Reduced motion gated: [Pass / Fail]
Dynamic content announced: [Pass / Fail — list update events]
Verdict: [Accessible / Needs work — specific gaps]
```

---

## COMMON FAILURE PATTERNS

| Pattern | Correct behavior |
|---|---|
| Color-only state indicator | Pair color with icon, text label, or shape |
| Elemental color with no icon | Always pair element color with dedicated element icon |
| Unlabeled icon button | `accessibilityLabel` describing the action |
| Missing accessibilityState | Add disabled/selected/busy as applicable |
| Animation with no reduced motion path | Gate via `isReduceMotionEnabled()` |
| Text truncated at large font | Remove `numberOfLines={1}`; allow wrapping |
| `accessible={true}` on decorative element | Remove — adds screen reader noise |
| Testing only on simulator | Test on real device — screen readers behave differently |
