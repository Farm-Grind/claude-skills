---
name: persona-glowmoon-doll
description: >
  Dispatcher for all work on Glowmoon Doll (glowmoondoll.com) — an artist BJD
  and vinyl doll business. Routes queries to three domains: Shopify operations
  (listings, variants, metafields, Liquid/Dawn theme, migration, admin tasks),
  product copy writing (listing structure, community conventions, brand voice,
  Boudi/Rune templates), and BJD/collector community knowledge (history,
  terminology, recast, Den of Angels, market dynamics). Use automatically — do
  not wait to be asked. Trigger on ANY of these signals: any Shopify admin task,
  product listing or copy question, Liquid code, metafields, Dawn/Debut/OS2,
  "write a product description", "update the listing", Boudi, Rune, accessories
  copy, BJD community or hobby questions, collector culture, recast, faceup,
  hybrid dolls, vinyl dolls, sofubi, Glowmoon market context, or any
  glowmoondoll.com question. Do NOT trigger for: newsletter drafting, general
  Shopify questions unrelated to this store. Load once per session.
---
SKILL_VERSION: v1.0

# persona-glowmoon-doll — Dispatcher

All Glowmoon Doll work routed through this dispatcher. Routes to three reference domains.

Type: dispatcher

---

## GOTCHAS

1. **Domain conflation** — Without routing, Shopify admin guidance and copy writing guidance
   bleed together: listing structure questions get both mechanics and copy advice without
   a clear division, producing output that serves neither task. Route SHOP and COPY separately;
   synthesize only when both are needed.

2. **Generic Shopify advice** — Without store context, Claude generates advice for a generic
   Shopify store. All Shopify guidance MUST load references/shopify.md — it contains
   store-specific details (boudi-doll.myshopify.com, current Debut theme, target Dawn migration)
   that change every recommendation.

3. **Community terminology errors** — Without BJD domain loaded, Claude uses mass-market
   language ("makeup" instead of "faceup", "unpainted" instead of "blank") that signals
   inexperience to the organized collector community. Load BJD domain for any copy or
   community-facing content.

4. **Single-domain routing on multi-domain queries** — "Set up the Rune listing" spans
   SHOP (creating the product in Shopify) and COPY (writing the description) and potentially
   BJD (community context for the listing). Check for cross-domain signals before routing.
   Consult references/cross-domain-map.md when ≥2 domains fire.

---

## INTAKE CLASSIFICATION

Classify the query before loading any reference file. Use domain codes: SHOP, COPY, BJD.

| Signal type | Domain code |
|---|---|
| Shopify admin tasks, theme editing, Liquid code, variants, collections, metafields, navigation, checkout settings, "add to store", Dawn/Debut/OS2 | SHOP |
| "write a description", "update the listing", "new doll copy", brand voice, Boudi copy, Rune copy, accessories copy, "how should I describe X", product templates | COPY |
| BJD history, community norms, terminology, recast, Den of Angels, collector culture, secondary market, vinyl dolls, sofubi, market context, "what do collectors care about" | BJD |
| New product setup — admin config + writing | SHOP + COPY |
| Copy writing requiring community conventions or legitimacy signals | BJD + COPY |
| Collection or tag organization using community terminology | BJD + SHOP |
| Full product launch — listing creation end to end | SHOP + COPY + BJD |

---

## DOMAIN DECLARATION

State before every response on a Glowmoon task:

```
DOMAINS ACTIVATED: [SHOP / COPY / BJD — list all that apply]
```

---

## REFERENCE FILE LOAD PATHS

Load ONLY the domains activated for this query. Never pre-load all three.

```
SHOP  → view /mnt/skills/user/persona-glowmoon-doll/references/shopify.md
COPY  → view /mnt/skills/user/persona-glowmoon-doll/references/product-copy.md
BJD   → view /mnt/skills/user/persona-glowmoon-doll/references/bjd-community.md
MULTI → view /mnt/skills/user/persona-glowmoon-doll/references/cross-domain-map.md
        (Required when ≥2 domains activated)
```

HARD FAIL: Responding to a Glowmoon query without loading the relevant reference file is
a domain expertise failure — running from memory rather than authoritative source.

---

## SYNTHESIS PROTOCOL

Single-domain query: answer directly from loaded reference file.

Multi-domain query:
1. Load all activated reference files and cross-domain-map.md.
2. Check cross-domain-map.md for any conflicts or priority rules between domains.
3. Produce a single integrated response — no section headers per domain.
4. Where domains address different aspects of the same question (e.g., SHOP handles
   the mechanics, COPY handles the language), answer each aspect naturally without
   labeling them by domain.
5. Where a domain conflict exists, apply the resolution rule from cross-domain-map.md.

NEVER produce concatenated per-domain sections. Output is integrated prose or structured
content that combines all loaded domains.

---

## META-ADVERSARIAL REVIEW

Before delivering any multi-domain response, check:
- Did I load cross-domain-map.md? If no, load it now before continuing.
- Is there a conflict between domains on this query? If yes, apply the resolution rule.
- Is my output integrated (single voice) or concatenated (per-domain sections)? If the
  latter, rewrite to integrate before sending.

---

## OUTPUT FORMAT

Single-domain: answer in the format appropriate to the task (Shopify how-to, copy
template, community explanation). No domain label required.

Multi-domain: integrated response. State DOMAINS ACTIVATED at top.

---

## Out of Scope

This skill does NOT cover:
- Newsletter drafting (no newsletter skill currently installed — handle ad hoc)
- General Shopify questions unrelated to glowmoondoll.com
- Isabel's confirmed voice rules (pending intake — stub in product-copy.md)
- Custom order flow beyond what is in shopify.md draft orders section

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| references/shopify.md | Shopify operations, theme, Liquid, store config |
| references/product-copy.md | Listing copy, templates, brand voice |
| references/bjd-community.md | BJD history, community, terminology, market |
| references/cross-domain-map.md | Multi-domain conflict and integration rules |
| glowmoondoll.com | Live store |
| Shopify Help Center | help.shopify.com |
| Den of Angels Wiki | denofangels.com/doawiki |
