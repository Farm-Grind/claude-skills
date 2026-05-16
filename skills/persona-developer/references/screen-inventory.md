# Screen Inventory — Developer Reference

A Screen Inventory is a complete catalog of every screen in the app:
purpose, content, entry/exit points, state dependencies, and transitions.
A developer must be able to build the entire navigation scaffold from this
document alone — without guessing anything.

---

## EXPO ROUTER FILE STRUCTURE

Map every screen to its Expo Router path before writing any navigation code.

```
app/
├── index.tsx                    # Redirect to auth or game entry
├── (auth)/
│   ├── login.tsx
│   ├── register.tsx
│   └── guest.tsx
├── (onboarding)/
│   └── cinematic.tsx
├── (game)/
│   ├── _layout.tsx              # Game layout — gesture handlers live here
│   ├── dreaming.tsx
│   ├── rift.tsx
│   ├── tower.tsx
│   └── source.tsx
└── (overlays)/
    ├── inventory.tsx
    ├── codex.tsx
    └── settings.tsx
```

Modal screens: use `(modal)/` group with `presentation: 'modal'` in layout config.
Overlay panels (slide-in, not full-screen replace): implement as animated Views
within the game layout, not as separate routes.

---

## REQUIRED SCREEN ENTRY ELEMENTS

Every screen entry is production-ready only when all of these are defined:

| Element | Description |
|---|---|
| Screen ID | Unique identifier (e.g. SCR-012) |
| Screen name | Human-readable name |
| Expo Router path | The exact file path (`app/(game)/dreaming.tsx`) |
| Purpose | One sentence: what does the user accomplish here? |
| Primary content | Key UI elements visible on screen |
| Primary actions | Tap targets with their outcomes |
| Entry points | Every screen/event that leads here + transition type |
| Exit points | Every way to leave + destination |
| State dependencies | What data must be loaded for this screen to function |
| Conditional visibility | Conditions that show/hide this screen or elements on it |
| Overlay behavior | Does anything persist from previous screen? |
| First-run only? | Yes/No |

---

## THREE-STATE REQUIREMENT

Every dynamic element (reads from MMKV or remote storage) requires three states.
Missing any state = incomplete entry.

1. **Loading** — skeleton or spinner while data fetches
2. **Empty** — designed state when element has no content yet
3. **Error** — what the user sees when fetch or action fails

Static elements (fixed UI, non-data-driven buttons) are exempt.

---

## NAVIGATION COMPLETENESS CHECKLIST

For every screen entry, verify all four transition categories:

1. **All entry points** — including gesture, deep link, notification tap,
   and conditional paths (e.g., "only at cycle 100")
2. **All exit points** — including back/dismiss, forced transitions, error exits
3. **Back-stack behavior** — is back blocked, allowed, or contextual?
4. **Modal return behavior** — every modal documents where dismiss returns to

Any category with no documented answer = incomplete entry.

---

## GESTURE CONFLICT RULES

Before implementing any gesture on a screen, verify:
1. Does it conflict with any globally-reserved gestures (swipe-right, swipe-left)?
2. Does it duplicate a gesture already assigned to another action on this screen?
3. Is there a tap alternative for users who avoid gestures?
4. Is it discoverable (visible affordance — no tutorial required)?

**No horizontal scroll containers** on screens that use swipe gestures for
navigation — they will conflict with `PanGestureHandler`.

---

## CONFIRMATION BLOCK

Run before delivering any screen inventory output:

```
Screen inventory self-review:
  State completeness: [all dynamic elements have loading/empty/error states, or "N missing — [list]"]
  Navigation completeness: [all 4 transition categories addressed, or "N gaps — [screens]"]
  Expo Router paths: [all screens mapped to file paths, or "N missing"]
  Status: CLEAR / BLOCKED — [reason]
```

---

## COMMON FAILURE PATTERNS

| Pattern | Symptom | Fix |
|---|---|---|
| Missing loading state | Blank screen during async fetch | Skeleton or spinner on every data-dependent element |
| Missing empty state | Visual gap before first content arrives | Design empty state for every list and dynamic area |
| Missing error state | Silent failure — user sees nothing | Error UI + retry action for every remote call |
| Undocumented back behavior | Expo Router back press produces unexpected navigation | Document back behavior explicitly per screen |
| Horizontal scroll + swipe gesture | Gesture conflict; swipe navigation fires unintentionally | Replace with vertical scroll; swipe navigation is reserved |
| Deep link entry not documented | Push notification tap routes to undefined behavior | Document deep link entry path for every notifiable screen |
