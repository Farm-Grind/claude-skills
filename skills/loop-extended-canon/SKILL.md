---
name: loop-extended-canon
description: >
  Maintains the atomic canonical statement registry for The Loop — a flat
  clause-by-clause source of truth for confirmed facts about the world,
  mechanics, characters, locations, and rules. Each entry is one falsifiable
  sentence with a status, category, source citation, and optional D-ID link.
  Use automatically — do not wait to be asked. Trigger on ANY of these signals:
  a canon fact is being verified or challenged; a new canonical statement needs
  to be registered; a lore or mechanic fact is referenced without a confirmed
  source; user says "is that canon", "register this", "add to canon", "check
  the registry", "what does canon say about X"; a skill catches a violation and
  needs to cite the source; registry is being seeded, audited, or exported.
  Do NOT trigger for: logging design decisions (loop-core-decisions),
  mid-generation content checks (loop-extended-lore-checker), or code generation.
  Load once per session.
---
SKILL_VERSION: v1.3

# The Loop — Canon Registry Skill

Maintains the authoritative flat registry of atomic canonical statements.
The registry is the clause library that all other skills cite when verifying
content. It is not a summary of the Lore Bible or GDD — it is a set of
single-sentence falsifiable facts.

The registry lives in Notion as a child page of the Lore Bible.
**Notion page ID:** `33f3a41dd33d81feb068e93c44fb4a5d` (same parent as taxonomy)

---

## What Goes in the Registry

Each entry is one falsifiable sentence. If a statement requires two sentences
to be complete, it is two entries.

**In scope:**
- Lore facts: "The Ark holds exactly 9 mortal race types."
- Mechanic rules: "All elemental actions are free — no mana cost."
- World rules: "The active elemental depletes its own element type in the Rift."
- Character facts: "The Familiar does not know about the Eye, Voice, Hand, or Master."
- Naming facts: "The three cycle phases are called The Waltz."
- Structural facts: "Each location has exactly one altar."

**Not in scope:**
- Design rationale (belongs in decisions log)
- Open/TBD items (flag as PLANNED or leave unregistered)
- Prose descriptions, atmospheric detail, flavor text
- Facts that are contested or unresolved

---

## Entry Schema

```json
{
  "id": "CR-001",
  "status": "CANON | PLANNED | DEPRECATED",
  "category": "LORE | MECHANIC | WORLD | CHARACTER | LOCATION | RULE | NAMING",
  "statement": "Single falsifiable sentence. Present tense. No hedges.",
  "source": "Document name + section (e.g. 'Lore Bible §3.2', 'D-061', 'GDD-mechanics §7')",
  "d_id": "D-XXX or null — links to the decision that established this fact",
  "date_added": "YYYY-MM-DD",
  "notes": "Optional. Disambiguation only — not a second sentence of the fact."
}
```

**Status definitions:**
- `CANON` — locked, confirmed, binding. Never contradict in generated content.
- `PLANNED` — decided but not yet present in in-world text or shipped code.
  Use as a drafting target; do not treat as established world fact.
- `DEPRECATED` — was canon, now retired (mechanic removed, lore retconned).
  Must not appear in new content. Keep for audit trail.

**ID format:** `CR-XXX`, zero-padded, globally sequential. Permanent.
Never reassign. Never reuse.

**Statement discipline:**
- Present tense: "The Familiar is a Mana Sprite." Not "was" or "will be."
- Falsifiable: if it cannot be proven wrong by a counterexample, it is not
  an atomic fact — it is flavor.
- No internal hedges: "mostly", "usually", "often" are banned in statements.
  If the rule has exceptions, register the exceptions as separate entries.

---

## Storage

Registry lives in Notion as structured content on the canon registry page.
Read via `Notion:notion-fetch` on page ID `33f3a41dd33d81feb068e93c44fb4a5d`.
Write via `Notion:notion-update-page` with `update_content`.

**On session load:** fetch the page via `Notion:notion-fetch` on page `3403a41dd33d81d3b781efdd0f41221d`. If no `## Data` block exists, the registry is empty — do not auto-seed. Surface as: `⚠ Canon Registry is empty — seeding required before any verification operations. Load seed sources manually.`

---

## Operations

**Query — verify a statement:**
Load registry → search by keyword or category → return matching entries.
If no matching entry exists: report as unregistered, not as false.
`CR-014 [CANON] MECHANIC — "All elemental actions are free — no mana cost." Source: D-007`

**Add new entry:**
Pre-add check — **HARD FAIL:** MUST NOT write a new entry without completing all three checks below. Registry write is blocked until all pass:
(a) Does an existing CANON entry contradict this statement? → resolve conflict
    first. Do not add a contradicting entry without superseding the prior one.
(b) Is the source document loaded and verified this session? → if not, load it
    before registering. Never add from memory.
(c) Is this truly atomic? → if the statement contains "and" connecting two
    independent facts, split into two entries.

Then: load → construct entry → append → write → confirm.
`✓ Registered CR-031 [CANON] LORE — "The Ark holds exactly 9 mortal race types." | Total: 31`

**Supersede / deprecate:**
When a canon fact changes: load → find entry → update status to DEPRECATED →
prepend "DEPRECATED YYYY-MM-DD: [reason]" to notes → register new CANON entry
referencing deprecated CR-ID in notes. Never silently overwrite.
`✓ CR-014 → DEPRECATED. CR-047 registered as replacement.`

**Audit — find unregistered facts:**
When asked to audit a document section: load registry + load document section →
identify claims in the document that have no matching registry entry →
report as a list of candidates for registration. Do not auto-register —
present candidates and wait for confirmation.

**Export:**
Load all entries → group by category → produce markdown table or docx per
user request. DEPRECATED entries shown in separate section at bottom.

---

## Verification Protocol (for other skills)

When loop-extended-lore-checker, loop-npc-designer, loop-dialogue-writer,
or any other skill needs to verify a claim:

1. Load registry (fetch Notion page).
2. Search by keyword or category.
3. If matching CANON entry found: cite it by CR-ID. Claim is verified.
4. If matching PLANNED entry found: note content is aspirational, not yet
   established in-world. Flag to author before including in player-facing text.
5. If no entry found: report as unregistered. Do not assert the claim. Flag
   as [OPEN: not in canon registry — verify against source before using].
6. If matching DEPRECATED entry found: the claim is retired. Do not use it.
   Cite the replacement CR-ID if one exists.

---

## Seeding

On first load, if registry is empty, present the seed candidate list derived from the sources below for author review before writing any entries. Never auto-seed without confirmation. The registry must reflect confirmed facts only — never inferred or assumed ones.

**Seed sources (in priority order):**
1. taxonomy.md (entity names, capitalization rules, category definitions)
2. Decisions log (all LOCKED entries — extract the canonical fact, not the rationale)
3. GDD-core (core loop rules, elemental action rules, cycle structure)
4. Lore Bible (confirmed races, factions, cosmology, Half-life state)

---

## Relationship to Other Skills

| Skill | Relationship |
|---|---|
| loop-extended-lore-checker | Lore-checker calls registry to verify claims before and after generation |
| loop-core-decisions | Decisions log is a source for registry entries — D-IDs are cited in `d_id` field |
| loop-npc-designer | NPC designer calls registry to confirm race, affinity, and faction facts |
| the-loop-taxonomy | Taxonomy governs naming and capitalization — registry entries must comply |
| utility-game-gdd-enforcer | GDD enforcer calls registry to verify mechanic facts in document sections |

---

## ADVERSARIAL SELF-REVIEW

Run after any registry operation (add, verify, audit, export) before delivering
the result. Block delivery until the confirmation block is produced.

---

### Challenge 1 — Falsifiability check

**Failure mode:** An entry is registered with a statement that appears factual
but is actually untestable — containing scope qualifiers, relative language,
or intent-based claims that cannot be proven wrong by a counterexample.

**FAIL examples:**

```
"The Familiar generally behaves with reserve toward the Hero."
(Not falsifiable — "generally" allows any behavior as compliant.)

"The Council is primarily a public-facing body."
("Primarily" cannot be disproven.)

"Ryszard's decisions are driven by strategic survival."
(Intent claims are unfalsifiable — we cannot verify internal motivation.)
```

**PASS examples:**

```
"The Familiar does not volunteer information about previous custodians
without prompting."
(Falsifiable — a counterexample is a scene where the Familiar does this.)

"The Council is described as the governing body in all official Ark
communications."
(Falsifiable against document evidence.)
```

**FIX:** Before confirming any new entry, read the statement and ask: "What
would a counterexample look like?" If no counterexample is conceivable — if
the statement cannot in principle be proven wrong — it fails falsifiability.
Rewrite until the counterexample is clear, or reclassify as flavor and decline
to register it.

**Severity:** HIGH — unfalsifiable entries pollute the registry with
non-verifiable claims, degrading its usefulness as a verification tool.

---

### Challenge 2 — Existing entry conflict scan

**Failure mode:** A new entry is added without checking whether an existing
CANON entry contradicts it — producing a registry with two conflicting CANON
facts that other skills cannot resolve.

**FAIL example:**

```
Existing: CR-014 [CANON] — "All elemental actions are free — no mana cost."
New entry added: CR-055 [CANON] — "Summoning an elemental costs 50 mana."
(Direct contradiction. Both are CANON. Skills querying either will get
conflicting guidance with no resolution path.)
```

**FIX:** The pre-add check in the Operations section already requires this —
but it is the step most likely to be skipped when adding in bulk or under
time pressure. This challenge enforces it as a hard gate:

Before writing any new entry to the registry:
1. Search the existing registry for entries in the same category as the new one
2. Search by the key noun(s) in the new statement
3. For each potential conflict: resolve it explicitly — deprecate the old entry
   if the new one supersedes it, or split into non-conflicting claims
4. Only after zero unresolved conflicts exist: write the new entry

If a conflict is found and resolution is unclear: flag it for author
confirmation rather than resolving silently. Never silently overwrite.

**Severity:** CRITICAL — conflicting CANON entries corrupt the registry's
authority and cause unpredictable behavior in downstream skills that cite it.

---

### Confirmation block (required before delivering any registry operation result)

```
Canon registry self-review:
  Challenge 1 — Falsifiability: [all new entries verified falsifiable, or "N rewritten — [what changed]"]
  Challenge 2 — Conflict scan: [existing entries checked for conflicts, or "N conflicts found — [how resolved]"]
  Status: CLEAR to deliver / BLOCKED — [reason]
```

If any challenge result is BLOCKED: resolve before delivering.
Never deliver a registry result with an open conflict.

---

## Out of Scope

This skill does NOT:
- Replace the Lore Bible or GDD as authoritative documents — it indexes them
- Make design decisions — it only records confirmed facts
- Log open or unresolved items — use loop-core-decisions for OPEN items
- Catch code correctness — use loop-extended-code-guardian
- Generate lore content — use loop-extended-lore-checker + utility-extended-narrative-designer

---

## Examples

**Example 1 — Verifying a claim mid-generation**

loop-extended-lore-checker is about to generate NPC dialogue referencing the Relay.
It needs to confirm the multiplier.

```
Registry query: "Relay multiplier"
→ CR-019 [CANON] MECHANIC — "Completing The Relay applies a ×1.5 flat multiplier
   to all gift effects." Source: D-019
Verified. Proceed.
```

**Example 2 — Registering a new fact after a session decision**

Author confirms that the Farm delivers at Source activation.

```
Pre-add check: No contradiction in registry. Source: D-071 (loaded this session). Atomic: yes.
✓ Registered CR-052 [CANON] MECHANIC — "Farm output is delivered when the player
  activates the Source at cycle transition." d_id: D-071 | Total: 52
```

**Example 3 — Unregistered claim**

loop-npc-designer asks whether Dragonkin have a confirmed cultural trait.

```
Registry query: "Dragonkin culture"
→ No matching entries.
Report: "Dragonkin cultural traits are not registered in canon.
Do not assert cultural specifics. Flag as [OPEN: not in canon registry]."
```

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| loop-extended-lore-checker | Canon consistency during content generation |
| loop-core-decisions | Source for LOCKED decisions → registry entries |
| the-loop-taxonomy | Naming and capitalization rules — governs statement phrasing |
| Notion canon registry page | `33f3a41dd33d81feb068e93c44fb4a5d` |
