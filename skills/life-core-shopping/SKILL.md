---
name: life-core-shopping
description: >
  Researches and compares consumer products and consumer software using
  authoritative multi-source web research, then delivers a structured comparison
  table and ranked recommendation with tradeoff analysis. Supports drilldown and
  refinement. Use automatically — do not wait to be asked. Trigger on ANY of
  these signals: user says "I need a", "help me find", "looking for a",
  "shopping for", "recommend a", "what's a good", "compare", "best X for",
  "should I get", "which is better"; user names a product or software category
  without a specific model ("blender", "headphones", "note-taking app", "jacket",
  "trowel"); user names a specific product or app and asks for comparison or
  alternatives; user says "research this for me" or "do some research on".
  Do NOT trigger for: product research with no purchase intent (e.g. industry
  analysis), enterprise or B2B software procurement, internal project tools, or
  academic products. Consumer apps with a clear personal purchase decision ARE
  in scope. Load once per session.
---
gates_passed: 2026-05-17
SKILL_VERSION: v1.0

# Shopping Assistant

Single-domain consumer product and software research skill. Covers electronics,
apparel, kitchenware, software/apps, gardening, wellness, and everyday carry.

Type: dispatcher

Canonical dispatcher reference: `persona-developer` — read before modifying
dispatcher body structure.

---

## GOTCHAS

1. **Defaulting to search-snippet prices** — snippets are cached and stale.
   Always fetch or label `[unverified — check live]`. Phase 3 Step 5 defines
   the exact protocol; running from memory produces wrong price data.
2. **Skipping activity-level intake for apparel** — "low activity" is not a
   safe default. A product suited for sedentary wear fails active use. Ask
   before Phase 2 routes to sources.
3. **Amazon fetch attempts** — Amazon robots.txt blocks Anthropic crawlers.
   Every Amazon fetch returns a 403 or robots error. Never attempt; redirect
   user to check the live page.
4. **Stale source articles** — "Best of [year]" lists older than 12 months
   produce outdated picks. Always verify publication date; search fresher
   version if stale.
5. **Not re-evaluating finalists after constraint refinement** — adding a
   constraint (inseam length, activity level, platform) invalidates prior
   picks. Re-run Phases 3-5 in full; never assume existing finalists still
   qualify.

---

## PART 0 — CLASSIFY

All triggers route to this skill. Single-domain: no sub-domain classification
required. Confirm the request has a personal purchase decision (not industry
analysis, B2B procurement, or internal tooling) — if unsure, proceed; Out of
Scope cases are rare.

---

## PART 1 — REFERENCE LOAD

Reference files do not persist across turns — re-view each turn that uses them.

    view /mnt/skills/user/life-core-shopping/references/shopping.md

HARD FAIL: Proceed to PART 2 only after shopping.md is loaded and visible
in the current turn's output.

---

## PART 2 — INTAKE

Run Phase 1 from the loaded reference. Infer required fields from context where
possible. Ask only what is genuinely missing. One question at a time.

HARD FAIL: Never skip activity-level intake for any apparel or footwear request.

---

## PART 3 — EXECUTE

Run Phases 2-6 from the loaded reference in sequence. Phase selection:

| Signal | Phase |
|---|---|
| New product research request | Phases 2, 3, 4, 5, 6 |
| User drills into specific brand/retailer SKUs | Phase 3B |
| User adds constraint after initial table delivered | Re-run Phases 3, 5 with updated parameters |
| User asks to validate a specific product they found | Phase 3 (targeted) then Phase 5 comparison |

---

## PART 4 — QUALITY CHECK

Run the Quality Checks block from the loaded reference before delivering any
table or recommendation. All checks must pass. No recommendation delivered
with a blank Weaknesses column or unverified price presented as fact.

HARD FAIL: Any product URL delivered without being fetched and confirmed live
this session is a delivery error.

---

## OUT OF SCOPE

- Enterprise or B2B software and SaaS procurement
- Services (not products or software)
- Investment or financial products
- Real estate, vehicles, major appliances over $2,000 (without explicit request)
- Industry analysis with no purchase decision

Consumer apps and personal software with a clear purchase decision ARE in scope.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| utility-data-analyst | General-purpose research synthesis for non-purchase topics |
| utility-core-output-gate | Pre-delivery self-check before finalizing any deliverable |
