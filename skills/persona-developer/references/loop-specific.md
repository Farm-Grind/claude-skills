# Loop-Specific Rules

Project: The Loop — mobile idle/RPG, React Native + Expo, Supabase backend.
Source: loop-extended-code-guardian v1.1, loop-build-tracker.

---

## D1 STORAGE — PROJECT STATE

Database: `a2af54f4-6385-45dd-92e7-edc45fa5b8bd` (Cloudflare D1)

**Read build phase at session start:**
```sql
SELECT content FROM session_handoff WHERE key = 'build-phase'
```

**Write build phase:**
```sql
INSERT OR REPLACE INTO session_handoff (key, content, updated_at)
VALUES ('build-phase', '{"phase": 1, "name": "Scaffolding"}', datetime('now'))
```

If no record exists, ask: "Which build phase are we in? (1-6)" and write before
generating any code.

---

## BUILD PHASES

```
Phase 1 — Scaffolding: project setup, navigation, Supabase connection, auth
Phase 2 — Core Game Loop: farm grid, crops, inventory, game time/tick
Phase 3 — Content & Progression: items, quests, economy
Phase 4 — Polish & Feel: animations, sound, effects, transitions
Phase 5 — Live Features: push notifications, cloud save, settings, onboarding
Phase 6 — Launch Prep: EAS Build, store listings, beta testing
```

If user requests Phase 4+ work during Phase 1, generate it but add:
```javascript
// Phase 4 — implement after core game loop is stable
```

---

## CONFIRMED STACK

| Layer | Correct choice |
|---|---|
| Framework | React Native + Expo |
| Navigation | Expo Router (file-based) |
| State | Zustand |
| Backend | Supabase |
| Local storage | React Native MMKV |
| Animations | React Native Reanimated + Lottie |
| Build | EAS |

Never suggest alternatives. If the stack is wrong for a use case, flag it as
a decision for the human — do not silently substitute.

**Banned:**
- `AsyncStorage` → use MMKV
- React Navigation → use Expo Router
- Firebase → use Supabase
- `localStorage`, `sessionStorage`

---

## NAMING CONVENTIONS

| File type | Convention | Example |
|---|---|---|
| Screen files | `[LocationName]Screen.tsx` | `DreamingScreen.tsx` |
| Component files | PascalCase | `ManaBar.tsx`, `ItemCard.tsx` |
| Store files | camelCase + Store | `gameStore.ts`, `inventoryStore.ts` |
| Supabase table names | snake_case | `player_profiles`, `crop_instances` |

No abbreviations that obscure meaning.

---

## LORE AND NAMING CONSISTENCY

Never invent:
- Familiar name or Hero backstory details
- Faction names beyond those established
- Answers to any OPEN lore item

**Established location names — exact only, no variants:**
- **The Dreaming** (farm/home area)
- **The Rift** (elemental challenge area)
- **The Tower** (progression area)
- **The Void** (endgame/dangerous area)
- **the Ark** — lowercase "the" in body text, capital "Ark"

**Element names in UI text:** Fire, Water, Earth, Air — always capitalized.

If generating UI text requires an OPEN lore item, use a placeholder:
```
"Welcome back, [OPEN: Familiar's name]"
```
Do not invent a name.

---

## FLAG vs. FIX

**Fix silently:** wrong color token, wrong font, wrong import, wrong storage library.

**Flag explicitly:**
- Feature that's Phase 3+ being requested in Phase 1
- Missing token (add `// TODO: add to theme.js`)
- OPEN lore item required by UI copy
- Import of a library not in the confirmed stack that can't be directly substituted

Flags appear after the code block:
```
⚠ Note: [brief description]
```
