# Cross-Domain Interaction Map

Required reference for persona-developer dispatcher when 2+ domain codes are active.
Load alongside the domain-specific reference files. Do not use as a substitute for them.

---

## Domain Priority Order (conflict resolution)

When domain rules conflict, apply in this order (highest to lowest priority):

1. **LOOP** — phase gate blocks all other domains; lore naming overrides any generated text
2. **DB** — security rules (RLS, service_role) override convenience choices
3. **DS** — visual rules override structural choices
4. **RN** — performance rules override convenience choices
5. **TDD** — test requirement applies to state/logic regardless of domain

---

## Known Cross-Domain Interactions

### DS + RN

**Interaction:** Both apply to UI components.
**No conflict:** DS owns visual tokens (colors, fonts, accessibility); RN owns
  performance structure (FlashList, Reanimated, re-render prevention).
**Synthesis:** RN determines the component architecture; DS determines
  the visual properties within that architecture.
**Watch for:** Reanimated `useAnimatedProps` on Text — must use `fontSize`
  from theme.js token, not a hardcoded value.

### DB + LOOP

**Interaction:** Supabase queries are phase-gated.
**Rule:** Check loop-specific.md build phase before implementing any
  Supabase query. Phase 1 queries are auth/profile only. Phase 2+ unlock
  game data tables.
**Watch for:** Requesting a `cycle_records` or `mana_ledger` table query
  during Phase 1 — generate it with a phase comment.

### RN + DB

**Interaction:** React Native client + Supabase query patterns.
**No conflict:** RN owns component architecture; DB owns query correctness.
**Synthesis:** supabase-js uses the HTTP API in React Native — the
  `MMKV` storage adapter for auth (from supabase-correctness.md) is the
  only point where these two files intersect.
**Watch for:** Any attempt to use a direct Postgres connection in RN —
  use supabase-js only (PostgREST HTTP API).

### DS + LOOP

**Interaction:** Design system is Loop-specific.
**No conflict:** DS IS the Loop design system. These files are complementary.
**Synthesis:** DS provides the rules; LOOP provides the context (current
  phase, lore naming constraints). Load both on any visual component request.

### TDD + DB

**Interaction:** Supabase queries require test files.
**Rule:** Any new stored procedure (RPC), new query helper, or Zustand
  store that wraps Supabase requires a test file first (tdd-and-debug.md).
  The DB reference file confirms what the query should do;
  the TDD reference file confirms how to test it.

### TDD + RN

**Interaction:** State and game logic in RN components require tests.
**Rule:** Any Zustand store, game tick function, or Reanimated worklet
  that encodes game logic (mana, cycles, progression) requires a test file.
  UI-only components (layout, visual) do not.

### PS + DB

**Interaction:** D1 (PS code) and Supabase (DB code) are distinct backends.
**No conflict:** DB owns Supabase/PostgREST patterns; PS owns D1/Cloudflare MCP patterns.
**Synthesis:** Confirm which backend is in scope before writing any query. Never apply
  RLS or service_role patterns to D1 ops; never apply D1 INSERT OR REPLACE to Supabase.
**Watch for:** Session where both Supabase and D1 work is happening — explicitly
  label each code block with its target backend.

### PS + SC

**Interaction:** CI scripts reference session-continuity toolchain paths.
**Rule:** Before writing any code that calls `validate_handoff.py`, confirm path
  resolves: `find /home/claude/cs-work -name validate_handoff.py`. If absent, bootstrap
  the script before referencing it. SC loads session state; PS writes/validates it.

### PS + TDD

**Interaction:** Both cover code correctness, but at different layers.
**No conflict:** TDD covers TS/React Native test protocol; PS covers Python syntax
  validation and CI script correctness.
**Synthesis:** `python3 -m py_compile` for Python scripts; `.test.ts` TDD protocol for
  RN/Zustand code. Never apply RN TDD protocol to Python scripts or vice versa.

---

## Multi-Domain Synthesis Protocol

When producing output with 2+ active domains:

1. Identify all domain rule sets loaded
2. Check this map for each active domain pair
3. Apply the priority order for any real conflict
4. Write a single integrated output — no section headers per domain
5. Post-generation: run audits from ALL loaded domain reference files

**Failure pattern to avoid:** Concatenation — producing separate sections
("Design System: [rules applied here]" + "React Native: [rules applied here]").
The output must be integrated so the code or explanation is coherent as a whole.
