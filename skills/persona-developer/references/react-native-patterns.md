# React Native Patterns — Expo + New Architecture

Source: Expo official skills, Callstack react-native-best-practices (Feb 2026),
Expo performance blog, Reanimated official docs, Shopify FlashList v2 engineering post.

---

## CRITICAL SETUP — verify once per project

### React Compiler (enable it)

```json
// babel.config.js
module.exports = { presets: ['babel-preset-expo'], plugins: ['babel-plugin-react-compiler'] };

// app.json
{ "expo": { "experiments": { "reactCompiler": true } } }
```

If React Compiler fails on a specific component: add `'use no memo'` at the
top of that component only. Never disable globally.

### Hermes — confirm enabled

```json
// app.json
{ "expo": { "jsEngine": "hermes" } }
```

JSC is 20% slower cold start and uses more memory. Never ship with JSC.

### New Architecture — confirm enabled

```json
// app.json
{ "expo": { "newArchEnabled": true } }
```

Required for FlashList v2, Reanimated 4, synchronous layout measurements.

---

## LIST RENDERING — CRITICAL

Never use FlatList or `.map()` in a ScrollView for lists with more than 5 items.

| Scenario | Correct | Never use |
|---|---|---|
| Inventory, achievement, log lists | `FlashList` (v2) | `FlatList`, `.map()` in ScrollView |
| Simple 2-3 item display | `ScrollView` + `.map()` acceptable | — |

```tsx
// ✅ CORRECT — FlashList v2 (no estimatedItemSize required)
import { FlashList } from '@shopify/flash-list';
<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={(item) => item.id}
  contentInsetAdjustmentBehavior="automatic"
/>

// ❌ NEVER
import { FlatList } from 'react-native';
```

FlashList v2: no `estimatedItemSize` needed — New Architecture provides
synchronous layout measurements. Remove it from any v1 code encountered.

---

## REANIMATED — CRITICAL

### Worklet rules

| Rule | Correct | Never |
|---|---|---|
| Read shared values | Inside `useAnimatedStyle`, `useAnimatedProps`, or `'worklet'` function | Directly in React component body |
| Update from JS | `sharedValue.value = newValue` | — |
| Cross UI→JS thread | `runOnJS(myFunction)(args)` | Direct call from worklet |
| Gesture objects | Wrap in `useMemo` (or enable React Compiler) | Inline in JSX |

```tsx
// ✅ CORRECT
const offset = useSharedValue(0);
const animatedStyle = useAnimatedStyle(() => ({ transform: [{ translateX: offset.value }] }));

// ❌ NEVER — JS thread read
const currentOffset = offset.value;
```

### Animated counters (mana display, cycle count)

Never use React state for animated counters. Use `useAnimatedProps`:

```tsx
const AnimatedText = Animated.createAnimatedComponent(Text);
const animatedProps = useAnimatedProps(() => ({ text: String(Math.round(manaValue.value)) }));
<AnimatedText animatedProps={animatedProps} />
```

### Game tick — frame callback

```tsx
useFrameCallback(useCallback(() => {
  'worklet';
  // game tick logic using shared values only
}, []));
```

---

## RE-RENDER PREVENTION

Without React Compiler, manual memoization needed. With React Compiler (project default), skip.

```tsx
// ✅ CORRECT — Zustand minimum selector
const mana = useGameStore((state) => state.mana);

// ❌ NEVER — whole store
const store = useGameStore();
```

### Barrel exports — banned in game state modules

```tsx
// ❌ NEVER — barrel exports add 200-800ms cold startup
// src/stores/index.ts: export { useGameStore } from './gameStore';

// ✅ CORRECT — direct import
import { useGameStore } from '../stores/gameStore';
```

Never create barrel `index.ts` files in `stores/`, `components/game/`, or
any module with 3+ exports.

---

## SCROLL CONTAINERS

```tsx
// ✅ CORRECT — handles safe area automatically
<ScrollView contentInsetAdjustmentBehavior="automatic">

// ❌ NEVER
import { SafeAreaView } from 'react-native'; // deprecated
```

Always use `react-native-safe-area-context` or `contentInsetAdjustmentBehavior`.

---

## EXPO ROUTER CORRECTNESS

- Routes in `app/` only — never co-locate components, stores, or utilities there
- Navigation stacks defined in `_layout.tsx` files
- Use `Stack` from `expo-router/stack`, never from `@react-navigation/stack`
- Delete orphaned route files — they remain discoverable and cause runtime errors

### Library preferences

| Use | Never use |
|---|---|
| `react-native-safe-area-context` SafeAreaView | `react-native` SafeAreaView |
| `expo-image` | `react-native` Image (for anything above basic) |
| `expo-audio` | `expo-av` for audio |
| `expo-video` | `expo-av` for video |
| `useWindowDimensions()` | `Dimensions.get()` |

---

## PERFORMANCE TESTING — CRITICAL

Never profile in development builds. Dev builds are 2–5× slower.

```bash
npx expo run:ios --configuration Release
npx expo run:android --variant release
```

Frame rate target: 60 FPS on mid-range device (iPhone SE, Pixel 6a equivalent).
Cold start target: first interactive frame under 2 seconds.

---

## COMMON FAILURES

| Pattern | Fix |
|---|---|
| FlatList for inventory | Replace with FlashList v2 |
| Shared value read on JS thread | Move into `useAnimatedStyle` |
| Barrel exports in stores | Direct imports from source files |
| `useState` for animated counter | `useSharedValue` + `useAnimatedProps` |
| Profiling in dev build | Always test in release build |
| Missing `contentInsetAdjustmentBehavior` | Add to all scroll containers |
| No React Compiler | Enable in babel.config.js + app.json |
