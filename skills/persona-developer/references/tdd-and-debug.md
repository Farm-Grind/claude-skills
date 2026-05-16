# TDD and Bug Investigation

Source: loop-extended-code-guardian v1.1 — extracted from body into reference file.

---

## PRE-IMPLEMENTATION TEST REQUIREMENT

Before writing any Zustand store, game state function, Supabase query, or
game mechanic logic, a test file must exist first.

**Files requiring a test file first:**
Any new Zustand store, game tick/cycle/mana function, Supabase query, or
Cards of Fate/Ritual/evolution logic.

**Not required for:** UI components and screen layout.

Test file: `[filename].test.ts` co-located with source file.

### Red/green/refactor — enforce strictly

1. Write the test. Confirm it fails.
2. Write minimum implementation to make it pass.
3. Refactor without changing behavior.

**Never skip to step 2.** If asked to skip, write `// TODO: implement test`
stubs so the debt is visible. A test that cannot be written means the
requirement is not yet understood — clarify before implementing.

---

## BUG INVESTIGATION PROTOCOL

Never propose a fix before completing this investigation. Proposing a fix
before diagnosing the cause is a critical failure mode.

| Phase | Action | Gate |
|---|---|---|
| 1 Define | State in one sentence: what is wrong, what was expected | Cannot proceed without this |
| 2 Evidence | Exact file/function/line; deterministic or intermittent; existed before last change? | Cannot proceed without this |
| 3 Hypothesize | Most likely cause in one sentence. Confidence: High/Med/Low | If Low: return to Phase 2 |
| 4 Verify | Write a failing test that reproduces the bug | If test can't be written: problem not understood — return to Phase 2 |
| 5 Fix | Minimum change that makes the test pass. No unrelated refactors. | Confirm test passes |

**Flag format:**
```
BUG INVESTIGATION — [brief description]
Phase 1: [what is wrong / what was expected]
Phase 2: [evidence — file, line, reproduction steps]
Phase 3: [hypothesis — confidence: High/Medium/Low]
Phase 4: [test written: yes / not yet]
Phase 5: [fix applied: yes / pending]
```

Never present a fix without completing Phases 1–3 first.
