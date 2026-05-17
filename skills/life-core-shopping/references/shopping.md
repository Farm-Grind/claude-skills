# Shopping Research Reference

All methodology, source routing, quality checks, and examples for
life-core-shopping. Loaded on demand — zero token cost until triggered.

---

## TOC

1. Phase 1 — Intake
2. Phase 2 — Source Routing
3. Phase 3 — Research Execution
4. Phase 3B — Retailer / SKU Drilldown
5. Phase 4 — Comparison Table
6. Phase 5 — Recommendation
7. Phase 6 — Drilldown / Refinement
8. Output Format
9. Quality Checks
10. Examples

---

## PHASE 1 — INTAKE

Before searching, establish:

**Required (infer from context if possible, ask only what's missing):**
- Product or software category (what type of thing)
- Primary use case or context (who/how/where it gets used)
- For software/apps: minimum functional requirements — what must it actually do,
  what platforms must it run on, what integrations matter. Ask these before
  searching; wrong assumptions here waste the entire research pass.
- Activity level if clothing/footwear (sedentary, light activity, active/sport)
- Budget range (hard ceiling vs. soft preference)
- Any known constraints (size, platform, brand preferences, avoid list)

**Optional but useful:**
- Specific products already on the radar
- What research the user has already done
- Whether they need it soon (affects recommending current stock)

If all required info is inferable from the user's message, skip to Phase 2.
Only ask when truly blocked. One question at a time if needed.

**Clothing-specific intake note:** For any apparel category, always establish
activity level before researching. A product suited for sedentary daily wear
may be wrong for light exercise, and vice versa. Never default to "low
activity" — ask if not stated.

---

## PHASE 2 — SOURCE ROUTING

Select primary sources based on category. Always run at least 3 sources;
cross-reference where possible.

| Category | Priority Sources |
|---|---|
| Electronics (general) | Wirecutter, RTINGS (displays/audio), PCMag (laptops/peripherals), The Verge, Consumer Reports |
| Consumer software / apps | PCMag, The Verge, Wirecutter, Zapier Blog (productivity apps), relevant subreddits (r/software, category-specific) |
| Displays / TVs / Monitors | RTINGS first, then Wirecutter |
| Audio (headphones, speakers) | RTINGS first, then Wirecutter, SoundGuys |
| Clothing / Apparel | Wirecutter, Gear Junkie (outdoor), GQ/Esquire (lifestyle), Strategist, Outdoor Gear Lab |
| Everyday Carry (EDC) | Everyday Carry (everydaycarry.com), Wirecutter, The Strategist |
| Kitchenware / Small appliances | America's Test Kitchen (atk.com) first, then Wirecutter, Serious Eats, Consumer Reports |
| Gardening tools / equipment | Fine Gardening, This Old House, Wirecutter, Consumer Reports |
| Spa / Wellness / Personal care | Wirecutter, Good Housekeeping, Strategist, Byrdie (skincare/beauty adjacent) |

**Source authority tiers:**

- **Tier 1 (independent testing, no affiliate pressure):** Consumer Reports,
  America's Test Kitchen, RTINGS, Outdoor Gear Lab (buys all products)
- **Tier 2 (editorial, affiliate-funded but strong methodology):** Wirecutter,
  PCMag, Serious Eats, Fine Gardening, Good Housekeeping
- **Tier 3 (supplemental, crowd-sourced or community):** Reddit category
  subreddits, verified Amazon reviews, enthusiast forums

Tier 1 sources weight more heavily on reliability claims. Tier 2 on usability
and value. Tier 3 only for real-world longevity signals and edge cases.
Consistent multi-owner failure reports in Tier 3 are disqualifying even when
Tier 1/2 sources are positive — real-world longevity data beats lab scores.

**Freshness rule:** Any "Best of [year]" list must have a publication or update
date within the last 12 months. Flag stale results; search for a fresher
version before including.

---

## PHASE 3 — RESEARCH EXECUTION

### Search sequence

**Step 1 — Category sweep:**
Search `best [category] [year]` and `[category] buying guide [year]` across the
priority sources for the category. Fetch the full pages of the top 1–2 results.

**Step 2 — Top picks extraction:**
From source results, extract the top 3–5 products mentioned most consistently
across sources. Note which sources recommend each.

**Step 3 — Head-to-head confirmation:**
For the top 3–4 candidates, search `[product A] vs [product B]` to surface
direct comparisons and any known failure modes or caveats not in the list
articles.

**Step 4 — Community signal check:**
For each finalist, run a quick Reddit or forum search for real-world reliability
reports, especially for products with limited lab testing (clothing durability,
gardening tool longevity, etc.).

**Step 5 — Price/availability check:**
Price data from search snippets is structurally unreliable — snippets are
cached, stale, and frequently wrong. Follow this protocol exactly:

**5a — Attempt direct fetch from a fetchable source.**
Use this retailer priority order (fetchable = confirmed accessible):

| Tier | Retailer type | Fetch approach |
|---|---|---|
| 1 — Brand direct | sportsresearch.com, thorne.com, pureformulas.com, vitacost.com | Fetch product page directly |
| 2 — Authorized retailers | iHerb, Vitacost, Walmart, Target | Fetch product page directly |
| 3 — Amazon | amazon.com | BLOCKED — never attempt; always returns robots.txt error |

Amazon is a hard block. Anthropic/Claude crawlers are explicitly disallowed
by Amazon's robots.txt. Never attempt Amazon fetches. If the user wants
Amazon pricing, direct them to check the live page themselves, or provide
the ASIN link and note the price must be verified.

**5b — If fetch succeeds:** Extract price from the rendered page. Note the
retailer and date fetched. This is the verified price.

**5c — If fetch fails (403, robots.txt, JavaScript gate):** State explicitly
that the price could not be verified for that retailer. Never substitute
a search snippet price. Either try a different fetchable retailer or flag
the price as unverified.

**5d — Never present unverified prices as fact.** If a price cannot be
fetched, label it `[unverified — check live]` in the comparison table.

**5e — Mandatory per-unit math block.** Before delivering any price, compute:
- Supply duration: count ÷ daily dose = days of supply
- Monthly cost: total price ÷ (days of supply ÷ 30)
- Show the arithmetic explicitly: `60 caps ÷ 1/day = 60 days; $23.95 ÷ 2 = $11.98/month`

Never state a monthly cost without showing the calculation. Never round
supply duration — use exact division.

---

## PHASE 3B — RETAILER / SKU DRILLDOWN

Triggered when the session shifts from brand comparison to navigating a specific
retailer's product line (e.g., "what does Brand X have in short inseam with a
pouch?"). Switch to this mode immediately when that signal appears.

**Step 1 — Map the product line:**
Search the retailer's site explicitly for all variants matching the user's
constraints. Never rely on memory of a brand's lineup — product lines change
and SKUs get discontinued without notice.

**Step 2 — Verify each candidate URL:**
Before delivering any product link, fetch the page and confirm:
- Price is rendering (not $NaN, blank, or clearly erroneous)
- Color/size selectors are populated and the user's preferred options are available
- Product is not marked discontinued or out of stock

**Step 3 — Flag gaps immediately:**
If a feature combination the user wants does not exist at that retailer, state
it directly on the first pass. Never keep searching for it across multiple
turns. Redirect immediately to the next-best option or a competing brand that
does offer the combination.

**Step 4 — Deliver only verified links.**
Never paste a product URL that has not been fetched and confirmed live this
session. Search snippets are not sufficient — retailer pages are volatile.

---

## PHASE 4 — COMPARISON TABLE

Deliver a markdown table with these columns:

| Product | Price | Best For | Strengths | Weaknesses | Source Consensus |
|---|---|---|---|---|---|

Guidelines:
- Include 3–5 products. Never fewer than 3.
- Price = current street price, not MSRP. Flag if price varies significantly.
- "Best For" = 1 sentence, specific use case this product wins at
- "Strengths" = 2–3 bullets, factual not marketing language
- "Weaknesses" = at least 1 real weakness per product. Never leave blank.
- "Source Consensus" = which Tier 1/2 sources recommend it

---

## PHASE 5 — RECOMMENDATION

After the table, deliver:

**Top Pick: [Product Name]**
1–2 sentences on why this wins for the user's stated needs, with the specific
evidence behind it (not generic praise).

**Runner-Up: [Product Name]**
When to choose this instead — what use case or constraint flips the pick.

**Budget Pick / Avoid: [as applicable]**
Flag the best option if budget is tight, and flag anything to avoid if a
highly-searched product has known quality issues.

**Key tradeoffs:**
Bullet list of the 2–3 decisions the user still needs to make themselves
(e.g. "if you prioritize X, get A; if you prioritize Y, get B").

---

## PHASE 6 — DRILLDOWN / REFINEMENT

After delivering the initial output, the session is open for:

- **Drilldown:** Fetch the full review for a specific product; surface specs,
  test methodology, and long-term ownership notes
- **Constraint refinement:** User adds a constraint (activity level, inseam
  length, feature requirement) → re-run Phases 3–5 with updated parameters.
  Re-evaluate all existing finalists against the new constraint — never assume
  prior picks still hold.
- **Retailer drilldown:** User wants to explore a specific brand's product line
  → switch to Phase 3B. Verify all SKUs before delivering links.
- **Alternative request:** "None of these feel right" → ask what's missing,
  then search a different angle
- **Specific product validation:** User has found a product elsewhere → research
  it against the current finalists

Stay in research/comparison mode until the user explicitly signals they're done.

---

## OUTPUT FORMAT

Always in this order:
1. Brief statement of what was researched and sources consulted (1–2 lines)
2. Comparison table
3. Recommendation block
4. Drilldown offer

Keep the intro line tight. No preamble about methodology. Lead with the table.

---

## QUALITY CHECKS (run before delivering)

- Every product in the table has a real weakness listed
- Price is either fetched-and-verified this session OR labeled `[unverified — check live]`
- No price stated from search snippets or training knowledge without that label
- Amazon prices never presented as verified — always flag as unverified
- Per-unit math shown explicitly for every price: count ÷ dose = days; price ÷ months = $/month
- Monthly cost calculation double-checked before delivery
- At least one Tier 1 source consulted for any reliability claim
- No product flagged as "discontinued" or "out of stock" recommended as top pick
- Freshness: all list articles dated within 12 months
- Budget constraints respected: no recommendation exceeds stated ceiling
- Any product URL delivered has been fetched and confirmed live this session
- After any constraint refinement, all prior finalists re-evaluated against new constraint

---

## EXAMPLES

**Trigger:** "I need a good chef's knife, around $100"
→ Research: Wirecutter, ATK, Serious Eats. Category sweep + top picks +
head-to-head. Deliver table of 4 knives, recommend ATK top pick with
Wirecutter runner-up.

**Trigger:** "Looking for wireless earbuds, use them at the gym, $150 max"
→ Research: RTINGS, Wirecutter. Gym/sport/sweat use case focus. Table of 4,
flag IPX rating as key spec, recommend sport-focused winner.

**Trigger:** "What's a good trowel for container gardening?"
→ Research: Fine Gardening, This Old House, Wirecutter. Narrow scope, may only
surface 3 products.

**Trigger:** "I already found the Victorinox Fibrox — is it worth it?"
→ Skip category sweep. Research Victorinox Fibrox specifically (ATK, Wirecutter)
and surface 1–2 competitors at same price to validate or reframe.

**Trigger:** "What does [brand] have in short inseam with a pouch?"
→ Switch to Phase 3B. Search brand's site, map all variants, fetch each
candidate page to verify price and availability. If the combination doesn't
exist, say so on the first pass and redirect.

**Constraint refinement:** User adds "I need this to hold up to light exercise"
→ Re-evaluate all current finalists against activity requirements. Demote or
remove cotton/modal-primary options. Rerank everything.

**Price verification:** Finalist is Sports Research D3+K2, 60ct, $23.95
→ Fetch sportsresearch.com/products/vitamin-d3-k2 directly. Price confirmed
$23.95. Math: 60 caps ÷ 1/day = 60 days = 2 months; $23.95 ÷ 2 = $11.98/month.
Never say "~$8/month" — always compute and show work.

**Amazon pricing:** User asks for Amazon price on any supplement.
→ "Amazon prices can't be verified by fetch — Amazon blocks AI crawlers.
Check live: amazon.com/dp/[ASIN]"
