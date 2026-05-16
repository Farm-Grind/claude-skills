# Supabase Correctness — Implementation Reference

Source: Supabase official docs (2026), Supabase RLS performance guide,
Supabase Performance Advisor, makerkit.dev production patterns (Jan 2026),
marmelab Edge Functions + RLS deep dive.

---

## MIGRATION PROTOCOL

Every schema change is a migration file. Never apply changes through the
dashboard in production — no version control, no replication.

### File naming — strict

```
supabase/migrations/YYYYMMDDHHmmss_short_description.sql
```

- UTC timestamp, underscores + lowercase, one logical change per file
- ✅ `20260415143022_create_player_states.sql`
- ❌ `changes.sql` / `20260415_PlayerStates.sql`

### Migration file structure

```sql
-- Migration: YYYYMMDDHHmmss_short_description
-- Purpose: [what this does]
-- Affected tables: [list]
-- Notes: [special considerations or destructive operations]

-- [SQL body — lowercase reserved words throughout]

-- RLS (if new table)
alter table public.[table_name] enable row level security;
```

### Generate migrations with db diff

```bash
supabase db diff -f migration_name
```

**Known limitation:** Views created with `security_invoker=on` have this
clause dropped by `db diff`. After generating migrations containing views,
manually verify and restore `with (security_invoker=on)` before committing.

### Deployment order

Local → `supabase db push` to staging → verify → push to prod.
Never edit schema through the Supabase dashboard in production.

---

## RLS IMPLEMENTATION RULES

### TO clause — always specify the role

Always include `TO authenticated` on player-data policies. This prevents
the policy from running for `anon` users — execution stops at the role check.

```sql
-- ✅ CORRECT — stops before evaluating policy for anon users
create policy "authenticated_select_own"
  on public.player_states
  for select
  to authenticated
  using ((select auth.uid()) = player_id);

-- ❌ NEVER — evaluates for anon users too (role omitted)
create policy "player_own_data"
  on public.player_states
  using (auth.uid() = player_id);
```

### auth.uid() — always wrap in (select ...)

**CRITICAL performance rule.** Without the subquery, Postgres calls
`auth.uid()` on every row. With it, Postgres caches the result per statement
(initPlan) — evaluated once regardless of table size.

```sql
-- ✅ CORRECT — cached per statement (initPlan)
using ((select auth.uid()) = player_id)

-- ❌ NEVER — evaluated per row; 100k rows = 100k calls
using (auth.uid() = player_id)
```

Applies to all `auth.uid()` and `auth.jwt()` in policies.

### Index every column in RLS policies

Every column in a USING or WITH CHECK clause must be indexed unless already a PK.

```sql
create index on public.player_states (player_id);
create index on public.cycle_records (player_id);
-- Repeat for every player_id column
```

Missing indexes cause full table scans on every authenticated request.

### Granularity — one policy per operation per role

```sql
-- ✅ CORRECT — granular
create policy "authenticated_select_own" on public.player_states
  for select to authenticated using ((select auth.uid()) = player_id);

create policy "authenticated_insert_own" on public.player_states
  for insert to authenticated with check ((select auth.uid()) = player_id);

-- ❌ NEVER — combined
create policy "player_own_data" on public.player_states
  using (auth.uid() = player_id);  -- no role, no operation
```

### UPDATE policies require USING + WITH CHECK

UPDATE operations need both USING (which rows to apply) and WITH CHECK
(which new values are allowed). If no WITH CHECK is defined, USING is
reused for both — but be explicit to avoid confusion:

```sql
create policy "authenticated_update_own"
  on public.player_states
  for update
  to authenticated
  using ((select auth.uid()) = player_id)
  with check ((select auth.uid()) = player_id);
```

A SELECT policy is also required for UPDATE to work as expected.

### Special cases

**Insert-only tables (ManaLedger):**
```sql
create policy "authenticated_insert_mana_ledger"
  on public.mana_ledger for insert to authenticated
  with check ((select auth.uid()) = player_id);
-- No update/delete policies — intentionally omitted
```

**Definition tables — read-only for all authenticated:**
```sql
create policy "authenticated_select_definitions"
  on public.item_definitions for select to authenticated using (true);
-- No insert/update/delete — server-side only via service_role
```

**Hard rules:**
- Never disable RLS on any table in the public schema
- Never use `service_role` key in client-side code
- Never rely on `user_metadata` in RLS — users can modify it
- Use `auth.uid()` or `auth.jwt() -> 'app_metadata'` (server-set, immutable)

### Supabase Performance Advisor

Run the Performance Advisor (Dashboard → Database) before shipping. Key codes:
- `0003_auth_rls_initplan` — `auth.uid()` called without (select ...) wrapper
- `0001_unindexed_foreign_keys` — missing policy column indexes
- `0006_multiple_permissive_policies` — multiple policies where one would do

---

## TRANSACTIONS

`supabase-js` does NOT support transactions. PostgREST has no transaction capability.

### Atomic multi-table writes — use PostgreSQL stored procedure via RPC

```sql
-- migration: [timestamp]_create_cycle_end_function.sql
create or replace function complete_cycle(
  p_cycle_number int, p_mana_earned bigint,
  p_dreaming_state jsonb, p_rift_state jsonb, p_tower_state jsonb
)
returns void language plpgsql
security invoker  -- runs as calling user; RLS applies
as $$
begin
  insert into public.cycle_records (player_id, cycle_number, completed_at)
    values ((select auth.uid()), p_cycle_number, now());
  insert into public.mana_ledger (player_id, cycle_number, delta, source_type)
    values ((select auth.uid()), p_cycle_number, p_mana_earned, 'cycle_complete');
  -- additional writes here — all atomic
end;
$$;
```

Client call:
```typescript
await supabase.rpc('complete_cycle', { p_cycle_number: n, p_mana_earned: m, ... });
```

**Never chain `.insert()` calls for multi-table writes** — partial writes on
network failure are real and produce corrupted state.

---

## EDGE FUNCTIONS

### Directory structure

```
supabase/functions/
  _shared/
    supabase-client.ts
    cors.ts
    auth.ts
  complete-cycle/index.ts
```

### Edge Function structure

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders });

  try {
    // Pass user JWT — preserves RLS
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    );
    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  }
});
```

**Deno import rules:** Use `npm:package@version` or `jsr:package@version`.
No bare import specifiers — they fail to bundle.

**Cold start rules:** Keep imports minimal; no persistent module-level state;
design for idempotency.

**service_role in Edge Functions:** Acceptable ONLY for admin operations
(backups, analytics), cross-user reads (push notification targeting), or
server-authoritative writes (anti-cheat). Document WHY above the call. Always.

---

## REACT NATIVE CLIENT SETUP

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();
const MMKVStorageAdapter = {
  getItem: (key: string) => storage.getString(key) ?? null,
  setItem: (key: string, value: string) => storage.set(key, value),
  removeItem: (key: string) => storage.delete(key),
};

export const supabase = createClient(
  process.env.EXPO_PUBLIC_SUPABASE_URL!,
  process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY!,
  {
    auth: {
      storage: MMKVStorageAdapter,
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: false,  // Required for React Native
    },
  }
);
```

**Environment variables:**
```
EXPO_PUBLIC_SUPABASE_URL=...        # Safe: no RLS bypass
EXPO_PUBLIC_SUPABASE_ANON_KEY=...   # Safe: RLS enforces access
# NEVER: EXPO_PUBLIC_SUPABASE_SERVICE_ROLE_KEY — exposed in app binary
```

Note: `supabase-js` uses the PostgREST HTTP API — it does NOT use a direct
Postgres connection. Connection pooling (Supavisor/pgBouncer) is relevant only
for server-side code (Edge Functions, direct connections), not mobile clients.

### Query optimization

For list views, select only needed columns — avoid `select('*')`:

```typescript
// ✅ List view — specific columns only
const { data } = await supabase.from('inventory_items')
  .select('id, name, rarity, quantity, icon_key')
  .eq('player_id', userId);

// For detail view, select all
const { data } = await supabase.from('inventory_items').select('*').eq('id', itemId);
```

PostgreSQL evaluates RLS policies before column filtering — you still scan the
same rows. Column selection reduces network overhead and deserialization time.

### Realtime subscriptions — always filter

```typescript
// ✅ CORRECT — filtered
const channel = supabase.channel('player-changes')
  .on('postgres_changes', {
    event: 'UPDATE', schema: 'public', table: 'player_states',
    filter: `player_id=eq.${userId}`,
  }, handleStateChange)
  .subscribe();

// ❌ NEVER — unfiltered overwhelms connections
supabase.channel('all').on('postgres_changes', { table: 'player_states' }, ...)

// Always unsubscribe on unmount:
useEffect(() => {
  const channel = supabase.channel(...)...subscribe();
  return () => { supabase.removeChannel(channel); };
}, []);
```

---

## COMMON FAILURES

| Pattern | Fix |
|---|---|
| `auth.uid()` without (select ...) | Full table scan per request — add wrapper |
| Missing TO clause | Anon users trigger policy evaluation — add `to authenticated` |
| Missing policy index | Slow queries at scale — index every player_id column |
| Combined policies | One policy per operation per role |
| Multi-table write without RPC | Partial writes — use stored procedure via rpc() |
| `security definer` on player RPCs | RLS bypassed — use `security invoker` |
| Bare import in Deno | Edge Function fails to bundle |
| service_role in Expo env | API key exposed in binary |
| No WITH CHECK on UPDATE | Writes bypass the user-owned row check |
| `select('*')` on list views | Unnecessary network payload |
