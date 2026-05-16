# Cross-Domain Map — persona-glowmoon-doll

Documents interactions, shared topics, and resolution rules for queries
that activate multiple domains (SHOP, COPY, BJD).

## Contents
- § INTERACTION MATRIX
- § SHARED TOPIC RULES
- § MULTI-DOMAIN ACTIVATION TRIGGERS
- § SYNTHESIS RULES

---

## § INTERACTION MATRIX

| Domain pair | Interaction | When both activate |
|---|---|---|
| SHOP + COPY | Setting up a new product: Shopify mechanics + listing content | New product creation; "set up [product] listing" |
| BJD + COPY | Writing copy with community accuracy: community context informs vocabulary and audience trust signals | Any copy task where legitimacy language matters |
| BJD + SHOP | Organizing store using community terminology: collection names, tags, navigation | Collection strategy; store architecture decisions |
| All three | Full product launch: from community positioning through copy writing through Shopify implementation | "launch [product]", end-to-end product setup |

---

## § SHARED TOPIC RULES

These topics appear in multiple domains. Apply the rule to avoid conflation.

### faceup
- **BJD domain owns**: terminology (what a faceup is, cultural significance)
- **COPY domain owns**: how to write about faceup options in listings
- **SHOP domain owns**: how to configure faceup as a Shopify variant

Resolution: When all three activate on faceup, answer in order — terminology
(BJD) informs the language (COPY) used to describe the configuration (SHOP).

### resin color
- **BJD domain owns**: why resin color variance matters to collectors (community expectation)
- **COPY domain owns**: the disclaimer language and how to present color options in copy
- **SHOP domain owns**: how to set up resin color as a Shopify variant; metafield notes

Resolution: No conflict. Each domain handles a distinct aspect. Integrate naturally.

### product description / listing structure
- **COPY domain owns**: editorial structure, content decisions, voice, what to include
- **SHOP domain owns**: where and how the description is entered in Shopify admin;
  which fields are Shopify native (title, description, tags) vs. metafield

Resolution: COPY decides what to write. SHOP decides where it goes. When both active,
produce the content (COPY) and the implementation path (SHOP) together.

### blank doll
- **BJD domain owns**: what "blank" means to collectors; the blank doll buyer archetype
- **COPY domain owns**: how to write a blank doll listing
- **SHOP domain owns**: how to set up blank vs. faceup as a variant or separate SKU

Resolution: No conflict. Load all three for full-coverage answer on blank doll setup.

### Isabel's voice / brand
- **COPY domain owns**: Isabel's voice, tone defaults, intake flag

No other domain owns brand voice. Route all brand copy questions to COPY.

---

## § MULTI-DOMAIN ACTIVATION TRIGGERS

| User query pattern | Activate |
|---|---|
| "Set up [product] in the store" | SHOP + COPY |
| "Write the listing for [product]" | COPY + BJD (community conventions inform copy) |
| "Create the Rune listing end to end" | All three |
| "How should I organize my collections?" | SHOP + BJD (community norms inform structure) |
| "What do collectors look for?" | BJD only |
| "How do I add faceup as an option?" | SHOP + COPY |
| "Write copy that appeals to faceup artists" | COPY + BJD |
| "What's the resin color disclaimer?" | COPY + BJD |

---

## § SYNTHESIS RULES

1. Never produce section headers labeled by domain (e.g., "SHOPIFY SECTION:", "BJD CONTEXT:").
   Output is integrated prose or a single structured document.

2. When SHOP + COPY both active: produce a unified workflow that covers both the content
   decisions and the implementation steps in task order (write → configure → publish).

3. When BJD + COPY both active: BJD knowledge informs vocabulary and legitimacy signals;
   do not produce a separate BJD summary alongside the copy. Let the knowledge shape the copy.

4. When all three active: sequence is BJD context (audience/positioning) → COPY (content)
   → SHOP (implementation). Produce as a cohesive workflow, not three separate answers.

5. Cross-domain conflicts (if a future conflict arises not covered above): flag it explicitly,
   name which domain owns the decision, and update this file.
