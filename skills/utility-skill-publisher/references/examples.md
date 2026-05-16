# Skill-Publisher — Worked Examples

Loaded by skill-publisher when builders need a concrete reference for gate
sequencing across common scenarios. Each example traces a request through
every applicable gate.

---

## Example 1 — New single-domain dispatcher

Gate 0 SUBSTANTIAL (new skill). Research runs, AUDIT block produced.
Gate 0.5 all STRUCTURAL.
Gate 1: N/A (new skill).
Gate 2: description precise.
Gate 2.5 RESOURCE PLACEMENT: body + 1 reference; no scripts/assets needed.
Gate 3: `Type: dispatcher`, >=1 reference file present, explicit `view`
  path in body, zero domain expertise in body, generalization passes.
Gate 5 5a–5e all PASS.
Gate 7: grep clean.
Gate 8: `ls references/` confirms 1 reference file. No cross-domain-map
  required (single domain).
Gate 8b all challenges. Gate 8c all checks. Gate 9: STAGED.

---

## Example 2 — Gate added to INSTALLED skill

Gate 0 SUBSTANTIAL (new gate). Research finds documented failure mode.
Gate 0.5: STRUCTURAL FIX.
Gate 2.5: no resource change.
Gates 1–7.
Gate 8.
Gate 8b: Challenge 5 RUNS (gate added → Option B). Challenge 6 STRUCTURAL.
Gate 9: STAGED.

---

## Example 3 — Description trim on INSTALLED skill

Gate 0 MINOR (trim only).
Gate 0.5: STRUCTURAL FIX (char count exceeded 1,024).
Gate 2.5: skipped (no resource change).
Gates 1–7.
Gate 8.
Gate 8b: Challenges 1–4; Challenge 5 SKIPPED; Challenge 6 passes.
Gate 9: INSTALLED.

---

## Example 4 — BEHAVIORAL ADDITION blocked

User requests gate with no documented failure mode. Gate 0.5 fires
BEHAVIORAL ADDITION block. User declines. Change discarded.

---

## Example 5 — New multi-domain dispatcher

Gate 0 SUBSTANTIAL. Research pre-run.
Gate 0.5: all STRUCTURAL FIX per research.
Gate 1: N/A (new skill).
Gate 2: description covers all sub-domains broadly.
Gate 2.5: body + N references + cross-domain-map.md; no scripts/assets.
Gate 3: `Type: dispatcher`; intake classification table with worked
  Example column per domain; domain declaration block defined; explicit
  reference file load paths; cross-domain-map.md in references/;
  synthesis protocol present; meta-adversarial review present. Body
  contains ZERO domain expertise.
Gate 5: 5a–5e PASS, domain declaration format present.
Gate 7: grep clean.
Gate 8: `ls references/` confirms all named reference files exist
  including cross-domain-map.md.
Gate 8b: Challenge 5 RUNS (new skill).
Gate 9: STAGED. Read `references/dispatcher-skeleton.md` before designing.

---

## Example 6 — Body content violation caught at Gate 5

Skill body contains methodology section ("Algorithm: binary search,
O(log n)..."). Gate 5d body content check fires: "Could this body
section appear in a reference file? Yes." Content moved to
references/algorithms.md; explicit `view` path added to body. Gate 5
re-run: PASS.

---

## Example 7 — Resource routed to scripts/ at Gate 2.5

Skill proposes inline bash for deterministic file-format validation
(regex check, line count, char count). Gate 2.5 RESOURCE PLACEMENT
identifies this as deterministic procedure → `scripts/validate.py`.
Body reduces by ~30 lines. Gate 8 packaging adds `scripts/` directory.
