---
name: utility-data-analyst
description: >
  Universal public-source research and synthesis skill. Covers synthesis
  documents for skills, GDDs, reference docs, design decisions, AND consumer
  product/software purchase recommendations. Use automatically — do not wait
  to be asked. Trigger on: "research", "best practices for", "deep dive",
  "quick check", "triple pass", "live schema", "function reference", "MCP
  research", "landscape scan", "horizon scan", "session retrospective", "root
  cause"; coverage is thin or stale; tool/API/MCP needs reference docs.
  ALSO trigger for purchase/product signals: "recommend a [product]", "best X
  for", "should I get", "which is better", "I need a [thing]", "help me find",
  "shopping for", "compare [products]", user names product category without a
  model. Implicit: skill edit on changing-practice domain; design solution
  without prior research. Do NOT trigger for: factual lookups; locked
  decisions; lore canon checks; B2B procurement; services (not products).
  Load once per session.
---
gates_passed: 2026-05-22
SKILL_VERSION: v2.2

# Data Analyst — Public-Source Research and Synthesis

Routes research requests to the correct methodology reference file. Body =
routing and gate logic only. Full Pass methodology, synthesis format, citation
rules, adversarial review, verification, Quick Audit, Spot Check, and failure
patterns are in `references/full-pass-methodology.md`. Specialized patterns
(Triple Pass, Architecture Decision, Function Reference, Skill Audit, Creative
Synthesis, Landscape Scan, Session Retrospective) are in
`references/research-patterns.md`.

Type: dispatcher

---

## GOTCHAS

Failure modes Claude exhibits without this skill. Documented from session evidence in the loaded failure reference.

1. **Fake passes** — labels web searches as a methodology pass without running the gates. F1. Structural fix: SYNTHESIS MODE header + PRIOR CYCLE CHECK + VIABILITY SCREEN must all be visible before search results are evaluated.
2. **Research → document spin** — produces synthesis after synthesis with no implementation gate between cycles. F2 + NF1 (root cause: skill evaluates source quality, not outcome accountability). Structural fix: PRIOR CYCLE CHECK names whether prior output was implemented before any new pass proceeds.
3. **Non-viable options waste sessions** — researches candidates that fail hard constraints (e.g., GitHub-MCP-as-storage burned two sessions). F3. Structural fix: VIABILITY SCREEN runs before deep research; rule-out-worst-case-first.
4. **Wide net without narrowing** — generates many options, fails to apply elimination criteria until late. F4. Structural fix: hard-constraint elimination is a named block in the architecture-decision pattern.
5. **Vague recommendations** — "improve the process", "look at X" — not specific enough to act on. F5. Structural fix: per-finding `Implementation looks like:` sub-field. Absent field drops the confidence label to PARTIAL.
6. **Training knowledge as research** — synthesizes from training data in fast-moving domain without external verification, presents as researched. F6. Structural fix: SYNTHESIS MODE: TRAINING KNOWLEDGE header explicit. Training-knowledge findings cannot be labeled [VERIFIED].
7. **Pass independence theater** — verification pass reuses prior-pass sources in a different configuration. Structural fix: VERIFICATION PASS requires `New sources not in Pass 1: N` field with N>0 for any verification claim.
8. **Synthesis overclaim** — "established", "proven", "best practice" used on single-source findings. Structural fix: adversarial Challenge 1 blocks delivery until per-finding confidence tag matches the evidential chain.
9. **[Consumer Research] Defaulting to search-snippet prices** — snippets are cached and stale. Always fetch or label `[unverified — check live]`. Phase 3 Step 5 of consumer-research.md defines the exact protocol; running from memory produces wrong price data.
10. **[Consumer Research] Skipping activity-level intake for apparel** — "low activity" is not a safe default. A product suited for sedentary wear fails active use. Ask before Phase 2 routes to sources.
11. **[Consumer Research] Amazon fetch attempts** — Amazon robots.txt blocks Anthropic crawlers. Every Amazon fetch returns a 403 or robots error. Never attempt; redirect user to check the live page.
12. **[Consumer Research] Stale source articles** — "Best of [year]" lists older than 12 months produce outdated picks. Always verify publication date; search for a fresher version if stale.
13. **[Consumer Research] Not re-evaluating finalists after constraint refinement** — adding a constraint invalidates prior picks. Re-run Phases 3-5 in full; never assume existing finalists still qualify.
14. **Session-end flush silently skipped** — PART 13 fires on explicit commits but not at session close. Validated findings evaporate. Structural fix: PART 13 has two named trigger conditions; session-end auto-flush is the second. If no [VERIFIED] or [MULTI-SOURCE] findings were produced this session, the flush is a no-op.

---

## PART 0 — DESTINATION GATE

Run first, before anything else.

| Destination | Route |
|---|---|
| Synthesis document for skill, GDD, reference doc, or design decision | Continue to Part 0.5 |
| Purchase or product/app recommendation | Consumer Research mode — continue to Part 0.5, declare mode at Part 1 |
| Lore canon verification on a project with a lore-checker | Stop — load the project lore-checker |
| Single-fact lookup answerable from current chat context | Stop — answer directly |
| Unclear | Ask once: "Is this feeding into a document, a purchase decision, or a different kind of decision?" |

Purchase signals: "which product", "what should I get", "which is best for me", "help me find a [thing]", "recommend a [thing]", user names a product category without a model.

---

## PART 0.5 — PRIOR CYCLE CHECK

HARD FAIL: produce this block before any research begins. Missing = pass blocked.

```
PRIOR CYCLE CHECK — [topic]
Prior research on this topic this session: [yes — [output name] / no]
If yes — was that output implemented? [yes / no / unknown]
Reason for this new pass:
  (a) Prior output superseded by new information — [what changed]
  (b) Prior output was implemented and a new problem emerged — [what]
  (c) Prior output was not implemented — [state why new research is
      needed rather than implementation of the prior output]
  (d) First pass on this topic — confirm
```

If (c): flag before proceeding. New research on an unimplemented finding is the primary mechanism of research spin.

---

## PART 1 — MODE GATE

Mode determines depth, source requirements, and output structure. Mode declaration is mandatory in the synthesis header.

| Mode | When to use | Reference |
|---|---|---|
| Full Pass | No prior coverage; thin or stale existing coverage; first pass on complex topic | `references/full-pass-methodology.md §Full Pass` |
| Quick Audit | Substantive prior coverage; checking for updates | `references/full-pass-methodology.md §Quick Audit` |
| Spot Check | Single targeted question; 1 search; binary output | `references/full-pass-methodology.md §Spot Check` |
| Triple Pass | High-stakes synthesis; architectural or design decision; user requests | `references/research-patterns.md §1` |
| Architecture Decision | Choosing between tools, platforms, frameworks | `references/research-patterns.md §2` |
| Function Reference | Documenting tool/API/MCP capabilities from live schemas | `references/research-patterns.md §3` |
| Skill/Document Audit | Verifying accuracy of an existing skill or document | `references/research-patterns.md §4` |
| Creative Synthesis | Training-knowledge synthesis (lore, archetype, taxonomy, stable concepts) | `references/research-patterns.md §5` |
| Landscape Scan | Orientation without a decision; mapping a space | `references/research-patterns.md §6` |
| Session Retrospective | Root-cause analysis of recurring session problems | `references/research-patterns.md §7` |
| Consumer Research | Purchase or product/app recommendation; consumer goods comparison | `references/consumer-research.md` |

Ambiguous signal → default to Quick Audit. Surface prior coverage; ask whether to escalate.

### Stale/thin flag (used by Full Pass triggers)

```
⚠ STALE/THIN FLAG: [section or skill name]
Issue: [thin — no citations / stale — primary sources from YYYY in fast-moving domain]
Recommendation: Full pass on this section before proceeding
Proceed? [yes = full pass / no = skip and note in output]
```

---

## PART 1.5 — REFERENCE FILE LOADING

Load the reference file matching the declared mode before executing any
methodology step. Explicit load required — no implicit loading.

```bash
# Full Pass, Quick Audit, Spot Check:
view /mnt/skills/user/utility-data-analyst/references/full-pass-methodology.md

# Triple Pass, Architecture Decision, Function Reference, Skill/Document Audit,
# Creative Synthesis, Landscape Scan, Session Retrospective:
view /mnt/skills/user/utility-data-analyst/references/research-patterns.md

# Consumer Research:
view /mnt/skills/user/utility-data-analyst/references/consumer-research.md
```

Also load at first synthesis output (all modes):
```bash
view /mnt/skills/user/utility-data-analyst/references/source-authority.md
```

For D1 commits (PART 13 gate only):
```bash
view /mnt/skills/user/utility-data-analyst/references/d1-validation.md
```

Reference files do not persist across turns. Re-issue `view` at each turn
that needs them. No view output = running from memory = HARD FAIL.

---

## PART 2 — CLARIFYING QUESTIONS (conditional)

Ask ONLY when one of these is genuinely unclear from context:
- Destination: what will the synthesis feed into?
- Mode: which Part 1 mode applies?

If destination and mode are clear — proceed directly to PART 1.5. Never ask
about citation format, thoroughness level, or domain constraints already
stated. Maximum 2 questions, in a single message.

---

## PART 13 — RESEARCH DATABASE GATE

Two triggers — run on either:
1. **Explicit commit:** user requests a specific finding be written to D1.
2. **Session-end auto-flush:** at session close (user says "wrap up", "close out",
   "save handoff", or session-manager fires @handoff), collect every [VERIFIED]
   or [MULTI-SOURCE] finding produced this session and run this gate for each
   in sequence. If no qualifying findings exist: no-op, skip silently.

Default behavior: **prefer UPDATE over INSERT**. Run Step 3 (dedup) first to
find the nearest existing entry in the same category. UPDATE if the finding
substantively overlaps an existing entry. INSERT only when the finding is
genuinely novel — no existing row covers the same mechanism with similar guidance.

HARD FAIL: INSERT or UPDATE must not execute without the visible gate block below.

Load `references/d1-validation.md` first. Run Step 1 (validate_research.py),
Step 2 (failure pattern check), Step 3 (dedup check) in order.

```
RESEARCH DB GATE — [research_id]
Step 1 RQG script:    [PASS / WARN (confirmed) / FAIL — blocked]
Step 2 pattern check: [no matches / P-XX flagged — warning updated]
Step 3 dedup:         [N in category, no near-duplicates / duplicate — decision]
Decision:             [INSERT new entry / UPDATE R-XXX (fields: <list>) / DISCARD]
```

HARD FAIL if this block is absent or any step shows FAIL before INSERT or UPDATE runs.

---

## Out of Scope

This skill does NOT:
- Handle enterprise or B2B software procurement or SaaS licensing decisions
- Verify lore canon on projects with a dedicated lore-checker
- Generate GDD sections, dialogue, or design docs directly — synthesis feeds those
- Answer factual lookups answerable from chat context with no synthesis required
- Conduct private-dataset statistical analysis — public-source synthesis only
- Handle services (not products or software), investment/financial products, or real estate

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| references/full-pass-methodology.md | Full Pass methodology, synthesis format, citation rules, adversarial review, verification pass, Quick Audit, Spot Check, common failure patterns |
| references/research-patterns.md | 7 specialized research patterns — triple-pass, architecture-decision, function-reference, skill-audit, creative-synthesis, landscape-scan, session-retrospective |
| references/source-authority.md | Source authority scoring framework, labels, red flags |
| references/consumer-research.md | Consumer Research mode — purchase decisions, product comparison, source tiers, price verification, comparison table format (absorbed from retired life-core-shopping) |
| references/d1-validation.md | Research database validation protocol — PART 13 gate steps, SQL patterns, RQG script usage |
| utility-skill-builder | Consumes research output during Gate 0 of new skill creation |
| AGENTIF benchmark | Multi-constraint instruction compliance |
| AutoVerifier — arxiv 2604.02617 | Structured claim verification methodology |
| Deep Researcher Sequential Plan Reflection — arxiv 2601.20843 | Sequential pass validity |
| Ask or Assume? — arxiv 2603.26233 | Conditional clarification methodology |
| PRISMA-ScR / Cochrane Rapid Reviews | Rapid review reporting framework |

---

## Examples

**Example 1 — Full Pass for a new GDD mechanic.** Idle game economy mechanic, no prior coverage. Part 0.5 PRIOR CYCLE = (d). Mode = Full Pass. PART 1.5 load: `references/full-pass-methodology.md`. Part 3 PRIOR COVERAGE SCAN runs (none found). Part 4 scope declared. Part 5 VIABILITY SCREEN run on three candidate approaches; one eliminated as architecturally incompatible. Part 6 all 5 facets searched (12 queries). Part 7 synthesis with 4 CORE FINDINGS, 1 CROSS-INDUSTRY, GAPS with 2 open questions plus search terms; each finding carries `Implementation looks like:` field. Part 9 challenges PASS. Part 10 VERIFICATION PASS produced. Deliver.

**Example 2 — Triple Pass for an architecture decision.** Storage alternatives for a mobile game project. Mode = Triple Pass; load `references/research-patterns.md §1`. Pass 1 (FIND) executes Full Pass methodology, raw findings list. Pass 2 (VERIFY) searches for independent corroboration — VERIFICATION shows "New sources not in Pass 1: 4". Confidence labels updated. Pass 3 (SYNTHESIZE) integrates verified findings, produces RECOMMENDED INTEGRATION. Parts 9 and 10 run on final synthesis.

**Example 3 — Function Reference for a new MCP.** "triple pass on the Notion MCP and all its functions". Mode = Function Reference; load `references/research-patterns.md §3`. Step 1 live schema discovery via tool_search. Step 2 official docs verification per tool. Step 3 community gap-fill. Step 4 classification (CONFIRMED / SCHEMA-ONLY / CORRECTED / INVALIDATED / UNVERIFIED GAP). Step 5 open gaps list. Synthesis structured by tool, not by domain.

**Example 4 — Creative Synthesis from training knowledge.** Cross-tradition relic archetype synthesis. Mode = Creative Synthesis; load `references/research-patterns.md §5`. Header: SYNTHESIS MODE: TRAINING KNOWLEDGE — claims not externally verified. Parts 3 and 6 skipped. Per-domain sweep, N≥3 threshold for composite formation. No finding labeled [VERIFIED]; all carry [TRAINING KNOWLEDGE]. Challenge 1 replaced with cross-tradition threshold check.

**Example 5 — Misroute caught at Part 0.** User: "what blender should I buy". Part 0 DESTINATION GATE: purchase intent → Consumer Research mode. Continue to Part 0.5. Declare mode = Consumer Research. PART 1.5: load `references/consumer-research.md`. Prior Cycle Check: (d) first pass. Phase 1 intake: budget, use case (daily smoothies vs. heavy-duty). Phase 2 source routing: Wirecutter, ATK, Consumer Reports. Execute Phases 3–5. Deliver comparison table and Top Pick with confidence label.

**Example 6 — Consumer Research mode full pass.** User: "recommend wireless earbuds for the gym, $150 max". Part 0: purchase intent → Consumer Research mode. PRIOR CYCLE CHECK: (d) first pass. PART 1.5 load: `references/consumer-research.md`. Phase 1 intake: gym/sport use, sweat exposure, no codec preference stated. Phase 2: RTINGS first, Wirecutter, SoundGuys. Phase 3 Steps 1–4. Price fetch attempted on top picks — two verified, one labeled `[unverified — check live]`. Phase 4 table: 4 earbuds. Phase 5: Top Pick `[VERIFIED]` — both RTINGS and Wirecutter recommend for active/sport at this price range. Runner-up flagged for better call quality. Deliver.
