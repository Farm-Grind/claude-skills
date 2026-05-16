# Data Model — Developer Reference

The data model document defines every persistent entity, storage tier,
and sync behavior before any backend code is written. No schema = no coding.

---

## STORAGE ARCHITECTURE

### Two-storage split

| Storage | Technology | What lives here | Sync trigger |
|---|---|---|---|
| Local session cache | React Native MMKV | Active game state — fast reads, no network required mid-session | On location transition or app exit |
| Cloud persistence | Supabase (PostgreSQL) | Player profile, progression, cycle history, server-authoritative data | On cycle end, app exit, key save points |

**No offline accumulation.** When the app closes, game state is frozen.
Restore on open loads last saved state unchanged — no catch-up calculation.

**Cycle-based progress uses cycle counts, not timestamps.**
`cycles_remaining: 3` not a target completion date.

### Two time systems

| System | Governs | Storage |
|---|---|---|
| Loop Time (cycles) | All in-Loop progression | MMKV (session) + Supabase (sync) |
| True Time (wall clock) | Server-authoritative events (NPC windows, push notifications) | Supabase only — never MMKV |

True Time data must never be stored locally. Server-authoritative constraint
is unenforceable once a wall clock timestamp is in MMKV (device clock exploit).

---

## ENTITY IDENTIFICATION PROCESS

1. Start from the Screen Inventory — every piece of data displayed is an
   entity, entity attribute, or derived value.
2. Identify what persists — ask: if the player kills the app now, what must survive?
3. Assign storage tier — MMKV (session) vs. Supabase (cross-session cloud).
4. Group into entities — nouns: Player, Item, NPC, Cycle, Achievement.
5. Map relationships — cardinality: one-to-one, one-to-many, many-to-many.
6. Progress through three model levels:
   - Conceptual: named entities and relationships only
   - Logical: entities with attributes, primary keys, relationships
   - Physical: Supabase table definitions with types, constraints, indexes, RLS

---

## RLS POLICY PATTERNS

Every table requires an RLS policy before any code touches it.

**Pattern A — Standard player-owned data (read/write own rows):**
```sql
CREATE POLICY "player_owns_row" ON [table]
  USING (player_id = auth.uid())
  WITH CHECK (player_id = auth.uid());
```

**Pattern B — Read-only definition tables (global, non-player data):**
```sql
CREATE POLICY "public_read" ON [table]
  FOR SELECT USING (true);
```

**Pattern A insert-only — audit/ledger tables:**
```sql
CREATE POLICY "player_insert_only" ON [table]
  FOR INSERT WITH CHECK (player_id = auth.uid());
-- No UPDATE or DELETE policy — intentionally locked
```

Definition tables (item/NPC/achievement definitions) are global read-only.
Per-player state tables (inventory, progress, settings) use Pattern A.
Ledger/audit tables (mana_ledger, delete_requests) use insert-only Pattern A.

---

## MMKV KEY SPACE

Document every MMKV key before coding begins. Format:

```
KEY: loop:[domain]:[entity]
Type: string | number | boolean | JSON
Source of truth: MMKV (session only) | Supabase (sync target)
Stale behavior: [what happens if MMKV and Supabase diverge]
```

Every MMKV key that has a Supabase counterpart must document sync failure behavior:
- What does the app display when MMKV and Supabase diverge?
- Which is source of truth on conflict? (Always Supabase — MMKV is a cache)
- Is there a reconciliation on app open?

---

## CONFIRMATION BLOCK

```
Data model self-review:
  RLS coverage: [all tables have policies, or "N missing — [tables]"]
  MMKV/Supabase split: [True Time data Supabase-only confirmed, or "violation — [field]"]
  Sync conflict behavior: [documented for all MMKV keys with Supabase counterparts, or "N missing"]
  Status: CLEAR / BLOCKED — [reason]
```

---

## COMMON FAILURE PATTERNS

| Pattern | What it looks like | Correct behavior |
|---|---|---|
| Timestamp for cycle progress | `maturation_complete_at TIMESTAMPTZ` | `cycles_remaining INT` — no wall clock for Loop Time |
| True Time in MMKV | NPC window timestamps stored locally | Supabase-only — device clock manipulation exploit |
| Missing RLS | Table created without policy | Every table gets a policy before any code |
| MMKV undocumented | Developer adds cache key ad hoc | All MMKV keys in key space doc before coding |
| JSONB overuse | Every column is JSONB for "flexibility" | JSONB only for data read/written as a unit; normalize queryable data |
| Definition tables per-player | Item definitions duplicated per player | Definition tables are global read-only |
| Guest player missing | Schema assumes authenticated users only | All player data requires guest player path (anonymous auth) |
| Missing stale cache handling | MMKV and Supabase diverge after failed sync | Document reconciliation on app open |
