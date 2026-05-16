# Mobile UX — Developer Reference

React Native implementation rules for touch, gesture, feedback, and layout.
Design philosophy excluded — this covers what must be true in code.

---

## TOUCH TARGETS

| Standard | Minimum | Use |
|---|---|---|
| Apple HIG | 44×44pt | iOS minimum |
| Material Design | 48×48dp | Android minimum |
| Project rule | 48×48pt | Use this everywhere |

Primary actions (primary CTA, confirm buttons): 56×56pt recommended.
Minimum 8pt padding between adjacent tappable elements.

Use `hitSlop` to expand tap area without changing visual size:
```javascript
<TouchableOpacity hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}>
```

---

## SAFE AREA

**Use `useSafeAreaInsets` from `react-native-safe-area-context` exclusively.**
React Native's built-in `SafeAreaView` is deprecated. Do not mix the
component and hook — causes flickering on orientation change.

```javascript
import { useSafeAreaInsets } from 'react-native-safe-area-context';

function Screen() {
  const insets = useSafeAreaInsets();
  return (
    <View style={{
      flex: 1,
      paddingTop: insets.top,
      paddingBottom: insets.bottom,
    }}>
      {/* content */}
    </View>
  );
}
```

App must be wrapped in `<SafeAreaProvider>` at root.
For scrollable content on iOS: `contentInsetAdjustmentBehavior="automatic"`
on `ScrollView` handles safe area automatically.
Never hardcode status bar height or home indicator offsets.

---

## GESTURE HIERARCHY

Confirm before implementing any gesture that it does not conflict with
globally-reserved gestures. Reserved gestures must be documented per project.

**Conflict prevention:**
- No horizontal scroll containers on screens that use horizontal swipe navigation —
  they will conflict with `PanGestureHandler`.
- Minigames with tap mechanics: use `PanGestureHandler` with directional threshold
  so horizontal velocity > 50% of vertical does not register as a tap.
- Every gesture must have a tap alternative.

```javascript
// PanGestureHandler directional threshold
const gestureHandler = useAnimatedGestureHandler({
  onActive: (event) => {
    const isHorizontalSwipe = Math.abs(event.velocityX) > Math.abs(event.velocityY) * 2;
    if (isHorizontalSwipe) {
      // handle swipe navigation, not tap
    }
  },
});
```

---

## FEEDBACK — EVERY TAP REQUIRES A RESPONSE

Silence after a tap is a bug.

**Button press animation (Reanimated — UI thread):**
```javascript
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';

const scale = useSharedValue(1);

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ scale: scale.value }],
}));

const onPressIn = () => { scale.value = withSpring(0.95, { duration: 80 }); };
const onPressOut = () => { scale.value = withSpring(1.0, { duration: 120 }); };
```

All animations must run on the UI thread (Reanimated worklets), not the JS thread.
JS thread animations cause visible stutter during any JS activity.

**Heavy operations during animations:**
```javascript
import { InteractionManager } from 'react-native';

// Defer MMKV writes and Supabase calls until animation completes
InteractionManager.runAfterInteractions(() => {
  saveCurrentCycleState();
});
```
Never call Supabase, write MMKV, or run heavy computation during an animation.

---

## LIST PERFORMANCE

Any scrollable list of more than 5 items must use `FlashList` from
`@shopify/flash-list`. Never `FlatList` or `ScrollView` wrapping `.map()`.

```javascript
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  // No estimatedItemSize needed with New Architecture
/>
```

`ScrollView` + `.map()` renders all items at once — invisible in dev,
painful on production devices with large lists.

---

## PORTRAIT LAYOUT CONSTRAINTS

Lock orientation in `app.json`:
```json
"orientation": "portrait"
```

**Design width:** 375pt (iPhone SE minimum). Test at 390pt and 412pt.

**Canvas budget (iPhone 14, 844pt total):**
- Header zone: ~80–100pt
- Primary interactive area: ~400–480pt
- Action bar: ~60–80pt
- Bottom safe area: 34pt+ (variable by device)

**One primary action per screen state.** At any moment, one visually dominant
action. If two actions appear equally prominent, the layout has failed.

**Primary actions belong in the bottom 60% of the screen.** Never place
a primary CTA in the top 40% — thumb reach on a 375pt canvas.

---

## PROGRESSIVE DISCLOSURE

- Never hide locked content entirely — grey it out with a lock indicator.
- Visible but locked elements motivate continued play.
- Players should always see what is coming next.

```javascript
// Locked element pattern
<TouchableOpacity
  disabled={!isUnlocked}
  style={[styles.element, !isUnlocked && styles.locked]}
  accessibilityState={{ disabled: !isUnlocked }}
>
  {!isUnlocked && <LockIcon />}
  <ElementContent />
</TouchableOpacity>
```

---

## STATUS BAR

```javascript
import { StatusBar } from 'expo-status-bar';
<StatusBar style="light" />  // For dark full-bleed backgrounds
```

---

## COMMON FAILURE PATTERNS

| Pattern | Correct behavior |
|---|---|
| Primary action in top 40% | Move to lower 60% of canvas |
| Horizontal scroll on swipe-nav screen | Replace with vertical scroll |
| Silent tap | Add minimum: scale animation + haptic |
| JS thread animation | Use Reanimated worklet (UI thread) |
| API call during animation | `InteractionManager.runAfterInteractions` |
| Missing loading state | Skeleton / spinner on every async element |
| Missing empty state | Design empty state for all dynamic content areas |
| Safe area violation | `useSafeAreaInsets` throughout |
| Mixed SafeAreaView + hook | Hook only — mixing causes flickering |
| FlatList for long list | FlashList for >5 items |
