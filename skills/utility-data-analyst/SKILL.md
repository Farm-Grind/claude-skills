---
name: utility-data-analyst
description: >
  Universal public-source research and synthesis skill. Produces synthesis
  documents for skills, GDDs, reference docs, and design decisions.
  Integrates papers, vendor docs, practitioner blogs, MCP schemas, and
  community consensus. Use automatically — do not wait to be asked.
  Trigger on ANY of these signals: "research", "best practices for",
  "deep dive", "quick check", "is this current", "triple pass", "live
  schema", "function reference", "MCP research", "tool research",
  "landscape scan", "horizon scan", "session retrospective", "root
  cause"; section needs grounding; coverage is thin or stale;
  cross-industry analogue needed; a tool, API, or MCP needs reference
  documentation. Implicit triggers: skill edit on a changing-practice
  domain; design solution proposed without confirming prior research.
  Do NOT trigger for: factual lookup answerable from training data with
  no synthesis needed; locked project decisions; lore canon checks;
  purchase recommendations (use life-core-shopping). Load once per
  session.
---
SKILL_VERSION: v1.1

# Data Analyst — Public-Source Research and Synthesis

Conducts structured research that produces synthesis documents ready to fold directly into skills, GDDs, reference sections, and design decisions. Sources are public — papers, vendor docs, practitioner blogs, MCP schemas, community consensus. Applies consistent methodology across all project domains.

Type: encoded-preference

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

---

## PART 0 — DESTINATION GATE

Run first, before anything else.

| Destination | Route |
|---|---|
| Synthesis document for skill, GDD, reference doc, or design decision | Continue to Part 0.5 |
| Purchase or product/app recommendation | Stop — load life-core-shopping |
| Lore canon verification on a project with a lore-checker | Stop — load the project lore-checker |
| Single-fact lookup answerable from current chat context | Stop — answer directly |
| Unclear | Ask once: "Is this feeding into a document, or a different kind of decision?" |

Purchase signals to redirect: "which product", "what should I get", "which is best for me", "help me find a [thing]", "recommend a [thing]".

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

| Mode | When to use | Pattern reference |
|---|---|---|
| Full Pass | No prior coverage; thin or stale existing coverage; first pass on complex topic | inline (this skill) |
| Quick Audit | Substantive prior coverage; checking for updates | inline (Part 11) |
| Spot Check | Single targeted question; 1 search; binary output | inline (Part 11) |
| Triple Pass | High-stakes synthesis; architectural or design decision; user requests | references/research-patterns.md §1 |
| Architecture Decision | Choosing between tools, platforms, frameworks | references/research-patterns.md §2 |
| Function Reference | Documenting tool/API/MCP capabilities from live schemas | references/research-patterns.md §3 |
| Skill/Document Audit | Verifying accuracy of an existing skill or document | references/research-patterns.md §4 |
| Creative Synthesis | Training-knowledge synthesis (lore, archetype, taxonomy, stable concepts) | references/research-patterns.md §5 |
| Landscape Scan | Orientation without a decision; mapping a space | references/research-patterns.md §6 |
| Session Retrospective | Root-cause analysis of recurring session problems | references/research-patterns.md §7 |

Ambiguous signal → default to Quick Audit. Surface prior coverage; ask whether to escalate.

Specialized patterns (Triple Pass, Architecture Decision, Function Reference, Skill/Document Audit, Creative Synthesis, Landscape Scan, Session Retrospective) are defined in `references/research-patterns.md`, loaded with the skill. Apply the section matching the declared mode.

### Stale/thin flag (used by Full Pass triggers)

```
⚠ STALE/THIN FLAG: [section or skill name]
Issue: [thin — no citations / stale — primary sources from YYYY in fast-moving domain]
Recommendation: Full pass on this section before proceeding
Proceed? [yes = full pass / no = skip and note in output]
```

---

## PART 2 — CLARIFYING QUESTIONS (conditional)

Ask ONLY when one of these is genuinely unclear from context:
- Destination: what will the synthesis feed into?
- Mode: which Part 1 mode applies?

If destination and mode are clear — proceed directly to Part 3. Never ask about citation format, thoroughness level, or domain constraints already stated. Maximum 2 questions, in a single message.

---

## PART 3 — PRIOR REFERENCE SCAN

HARD FAIL: do not execute any Part 6 searches before completing this scan.

| Source | Check |
|---|---|
| Project documents | Sections covering topic — content, citations, source dates |
| Installed skills | SEE ALSO sections and inline citations |
| Project storage | Decisions log, open items, prior synthesis output |
| Loaded reference files | Any prior synthesis in current session context |

Output (visible before searching):

```
PRIOR COVERAGE SCAN — [topic]
Found in: [doc/skill name, section]
Coverage: [substantive / thin / none]
Sources cited: [list with years if visible, or "none"]
Stale risk: [yes — domain moves fast and sources are from YYYY / no]
Verdict: [Full pass / Quick audit / Spot check / mode escalation]
Gaps identified: [what existing coverage does not address]
```

---

## PART 4 — RAPID REVIEW SCOPE DECLARATION

HARD FAIL: do not execute searches before producing this block. Required for Full Pass and Triple Pass. Skip for Quick Audit, Spot Check, and Creative Synthesis.

```
RAPID REVIEW SCOPE — [topic]
In scope: [5 mandatory facets + domain-specific additions]
Out of scope: [what is not covered and why — token budget, session scope]
Constraint acknowledgment: [what constraints mean for completeness]
```

---

## PART 5 — VIABILITY SCREEN

HARD FAIL: do not evaluate search results before producing this block. Applies to Full Pass, Triple Pass, and Architecture Decision.

```
VIABILITY SCREEN — [topic]
For each candidate option, hypothesis, or fix in the research brief:

Candidate: [name]
  (A) Feasible in current operating environment? [Y/N — cite evidence]
      If N: ELIMINATED — document reason; do not research further.
  (B) Success/failure verifiable within session timeframe? [Y/N]
      If N: candidate labeled [SPECULATIVE] in findings.
  (C) Failure mode this addresses confirmed in session record? [Y/N — cite]
      If N: candidate labeled [PREVENTIVE — unconfirmed recurrence].
```

ELIMINATION RULE: any candidate scoring N on (A) is eliminated before deep research. Document the elimination; never silently drop. Rule-out-worst-case-first: catastrophically non-viable candidates (architecture-incompatible, requires unavailable infrastructure, costs multiple sessions) are screened first.

---

## PART 6 — SEARCH EXECUTION

### Mandatory facet checklist (Full Pass + Triple Pass)

A pass is not complete until all 5 facets have been searched. Minimum 6 searches total. Facet diversity is the primary criterion — 6 searches across 3 facets is insufficient; 10 across all 5 is correct.

| # | Facet | What to find |
|---|---|---|
| 1 | Primary domain | What the field says — best practices, established approaches |
| 2 | Failure/critique | What goes wrong; postmortems; critics |
| 3 | Cross-industry | How adjacent domains solve the analogous problem |
| 4 | Platform/primary-source | What the vendor, institution, or authority says directly |
| 5 | Recency check | What has changed since older sources |

### Mandatory domains for Facets 2 and 3

Facets 2 and 3 are mandatory for: game design, LLM/platform architecture, UX/product, cognitive science, skill authoring. Omitting either requires explicit justification with a named reason.

For other domains: run Facets 1, 4, 5 by default. Add 2 and 3 when the primary domain lacks established best practices or an adjacent industry has solved the analogous problem.

### Pass independence rule

Required for any verification pass (Triple Pass Pass 2, audit verification, contested-claim re-check).

Every source cited in a verification pass must be independent of the prior pass. Reusing prior sources in a different configuration is rearrangement, not verification.

Required field in VERIFICATION PASS:

```
New sources not in Pass 1: [N] — [list titles]
```

If N = 0 on a stated verification pass: the pass is invalid. Re-run with independent sources, or downgrade Pass 2 findings to [PARTIAL] or [TRAINING KNOWLEDGE].

### Search execution rules

- Use specific terminology, not generic descriptions
- Vary phrasing — same topic, different entry points
- Seek original sources over aggregators
- When a secondary cites a compelling primary, fetch the primary
- Note when a claim traces to one unverified origin (flag the chain)
- For game development: GDC talks, postmortems, academic game studies, shipped-game developer blogs
- For cross-industry Facet 3: target industries with demonstrated rigor in the analogous problem

### Stopping criterion

A pass is complete when ALL of:
- All required facets have been covered
- The last 2 searches returned no findings not already in the synthesis
- Internal consistency at Part 4 scope is satisfied

Never add searches to reach a count. Stop when coverage is genuinely complete.

### Thin coverage handling

State it plainly. Output: "Primary domain coverage is limited. Cross-industry returned [N] relevant sources. Recommend [alternative or acknowledge underdeveloped area]." Never manufacture breadth.

---

## PART 7 — SYNTHESIS OUTPUT FORMAT

```
SYNTHESIS MODE: [TRAINING KNOWLEDGE — claims not externally verified
                / WEB-SEARCH GROUNDED]
RESEARCH MODE: [Full Pass / Quick Audit / Spot Check / Triple Pass / ...]
Date: [YYYY-MM-DD]
Feeds into: [destination]
Coverage: [facets searched] / [facets skipped — reason if any]

PRIOR COVERAGE
[What existed before this pass, or "None found"]

CORE FINDINGS
[Each finding states:]
  Claim: [specific, falsifiable claim]
  Evidence: [what supports it — study, data, primary source]
  Confidence: [VERIFIED / PARTIAL — reason / SPECULATIVE / UNVERIFIED]
  Implementation looks like: [specific action + observable outcome that
    confirms the finding was actioned]
  Source(s): [citation numbers]

CROSS-INDUSTRY FINDINGS
[Present only if cross-industry pass was run]
[Each names source industry and the analogue being drawn]
[Explicitly flag where analogue holds vs. breaks down]
[Critical-point breakdowns downgrade to "partial analogue — apply with caution"]

GAPS AND OPEN QUESTIONS
[What this research did not find]
[Questions the synthesis raises but cannot answer]
[Where best sources disagree, named — not flattened]

RECOMMENDED INTEGRATION
[How findings fold into the destination]
[Specific language or principles to carry forward]
[Decisions or calibration flags implied]

SOURCES
[Per Part 8 citation format]
```

### Finding rules

- **Findings, not summaries.** "Source X discusses Y" is a summary. "Players lose engagement when feedback loops exceed 45 seconds (Source X, data from Y)" is a finding.
- **Convergence and divergence.** Where sources agree, state convergence. Where they conflict, name the conflict — never flatten.
- **Confidence per finding is mandatory.** A finding without a label is not deliverable.
- **No padding.** Three strong findings → three findings.
- **If `Implementation looks like:` cannot be completed:** label [PARTIAL — implementation criteria unclear] regardless of source quality. Cannot be [VERIFIED].

---

## PART 8 — CITATION FORMAT

### Default (minimal)

```
[N] Title — Author/Org — URL (Year)
```

### Standard (on request)

```
[N] Title — Author/Org — Publication — URL — Year
Key finding: [one sentence on what this source contributes]
Authority: [Primary / Industry / Academic / Practitioner / Secondary]
```

### Rules

- Number sources in order of first appearance in findings
- Multiple sources supporting same claim: cite all
- Secondary used because primary unavailable: `[via N]` — flag for replacement if load-bearing
- Commercially conflicted sources: `[⚠ commercial interest]`

Apply source authority scoring per `references/source-authority.md`. Confidence labels ([VERIFIED] / [PARTIAL] / [UNVERIFIED]) must appear in SOURCES section, not only on findings.

---

## PART 9 — ADVERSARIAL SELF-REVIEW

Run after the synthesis is drafted, before delivery. Block delivery until the confirmation block is produced.

### Challenge 1 — Synthesis overclaim

For each finding, the confidence label must match the evidential chain:
- Single source, no corroboration → [SPECULATIVE] or "suggested by [source]"
- Multiple independent sources agreeing → [PARTIAL] or "convergent evidence"
- Controlled study, meta-analysis, or N≥3 independent sources → [VERIFIED]
- Widely repeated but tracing to one origin → flag the chain; not [VERIFIED]

Never use "established", "proven", or "best practice" without ≥2 independent high-authority sources.

For Creative Synthesis mode: Challenge 1 is replaced with the cross-tradition threshold check — does each composite meet N≥3 independent domain threshold? Flag any that do not.

### Challenge 2 — Cross-industry analogue validity

For every cross-industry finding, state explicitly:
1. What problem the source industry solved
2. What the analogous problem in the target domain is
3. Where the analogue holds
4. Where it breaks down — peripheral or critical

Critical-point breakdown → downgrade to "partial analogue — apply with caution."

### Challenge 3 — Gap completeness

Answer explicitly:
- What did this research look for and not find?
- What questions does this synthesis raise that it cannot answer?
- Where do the best sources disagree, and is the disagreement live or resolved?
- What primary study or controlled experiment would change confidence on load-bearing findings?

Minimum: 2 specific open questions with concrete follow-up search terms.

### Confirmation block

```
Research self-review:
  Challenge 1 — Synthesis overclaim: [confidence verified per finding, or "N flagged — what"]
  Challenge 2 — Cross-industry validity: [breakdown points named, or "no cross-industry findings"]
  Challenge 3 — Gap completeness: [2+ open questions with search terms, or "expanded — what"]
  Status: CLEAR to deliver / BLOCKED — [reason]
```

HARD FAIL: no delivery without this block. Revise if any challenge is BLOCKED.

---

## PART 10 — VERIFICATION PASS

HARD FAIL: produce this block immediately before delivery. Visible to user.

```
VERIFICATION PASS — [topic]
Coverage complete: [yes / no — what is missing]
Internal consistency: [conflicting findings named, or "none identified"]
Confidence per finding: [e.g., "3 VERIFIED, 2 PARTIAL, 0 UNVERIFIED"]
Integration actionability: [Recommended Integration specific enough to act on? yes / no + fix]
New sources not in prior pass: [N — list, or N/A for first pass]
Delivery-ready: [yes / blocked — reason]
```

Address any "no" or "blocked" field before delivery.

---

## PART 11 — QUICK AUDIT and SPOT CHECK

### Quick Audit (2–3 targeted searches)

1. Load prior references (Part 3)
2. Run 2–3 targeted searches for significant new developments
3. Identify superseded or contradicted prior sources
4. Output:

```
QUICK AUDIT — [topic]
Date: [YYYY-MM-DD]
Prior coverage: [adequate / thin — recommend full pass]
New developments: [yes — summary / none found]
Stale sources: [list / "none"]
Verdict: [Coverage holds / Update needed — specific gaps]
```

Escalate to Full Pass if audit reveals more deficiency than expected.

### Spot Check (1 search, binary output)

Single targeted search. 5-minute time box.

```
SPOT CHECK — [question]
Search: [query used]
Output: [Coverage holds — reason] OR [Update needed — specific gap]
```

Escalate to Quick Audit if result is ambiguous.

---

## PART 12 — COMMON FAILURE PATTERNS

| Pattern | What it looks like | Correct behavior |
|---|---|---|
| Quota filling | Weak sources added to reach a count | Stop at strong sources; name thin coverage |
| Summary not synthesis | Output lists what each source says | Rewrite as claims with evidence |
| Skipping prior scan | External search runs first | Always run Part 3 before Part 6 |
| Flattening conflicts | Sources disagree; output presents one view | Name conflicts explicitly |
| Unverified chains | Claim traces to one unvalidated origin | Flag the chain |
| Scope drift | Searches wander from brief | Reference Part 4 to reanchor |
| Stale coverage unflagged | Existing section is old, no flag | Run prior scan; flag stale |
| Skipping clarifying | Pass launched before destination known | Complete Part 2 first |
| Facet-thin pass | 6+ queries but only 2–3 facets covered | Verify all 5 facets before declaring complete |
| Pass independence theater | Pass 2 reuses Pass 1 sources | Pass 2 sources must be new — N>0 in VERIFICATION |
| Implementation gap | Findings correct but vague on action | Per-finding `Implementation looks like:` required |

---

## Examples

**Example 1 — Full Pass for a new GDD mechanic.** Idle game economy mechanic, no prior coverage. Part 0.5 PRIOR CYCLE = (d). Mode = Full Pass. Part 3 PRIOR COVERAGE SCAN runs (none found). Part 4 scope declared. Part 5 VIABILITY SCREEN run on three candidate approaches; one eliminated as architecturally incompatible. Part 6 all 5 facets searched (12 queries). Part 7 synthesis with 4 CORE FINDINGS, 1 CROSS-INDUSTRY, GAPS with 2 open questions plus search terms; each finding carries `Implementation looks like:` field. Part 9 challenges PASS. Part 10 VERIFICATION PASS produced. Deliver.

**Example 2 — Triple Pass for an architecture decision.** Storage alternatives for The Loop. Mode = Triple Pass; load research-patterns.md §1. Pass 1 (FIND) executes Full Pass methodology, raw findings list. Pass 2 (VERIFY) searches for independent corroboration — VERIFICATION shows "New sources not in Pass 1: 4". Confidence labels updated. Pass 3 (SYNTHESIZE) integrates verified findings, produces RECOMMENDED INTEGRATION. Parts 9 and 10 run on final synthesis.

**Example 3 — Function Reference for a new MCP.** "triple pass on the Notion MCP and all its functions". Mode = Function Reference; load research-patterns.md §3. Step 1 live schema discovery via tool_search. Step 2 official docs verification per tool. Step 3 community gap-fill. Step 4 classification (CONFIRMED / SCHEMA-ONLY / CORRECTED / INVALIDATED / UNVERIFIED GAP). Step 5 open gaps list. Synthesis structured by tool, not by domain.

**Example 4 — Creative Synthesis from training knowledge.** Cross-tradition relic archetype synthesis. Mode = Creative Synthesis; load research-patterns.md §5. Header: SYNTHESIS MODE: TRAINING KNOWLEDGE — claims not externally verified. Parts 3 and 6 skipped. Per-domain sweep, N≥3 threshold for composite formation. No finding labeled [VERIFIED]; all carry [TRAINING KNOWLEDGE]. Challenge 1 replaced with cross-tradition threshold check.

**Example 5 — Misroute caught at Part 0.** User: "what blender should I buy". Part 0 DESTINATION GATE catches purchase intent. Route to life-core-shopping. Exit.

---

## PART 13 — RESEARCH DATABASE GATE

Fires when any research finding is being committed to D1. HARD FAIL: INSERT
must not execute without the visible gate block below.

Load `references/d1-validation.md` first. Run Step 1 (validate_research.py),
Step 2 (failure pattern check), Step 3 (dedup check) in order.

```
RESEARCH DB GATE — [research_id]
Step 1 RQG script:    [PASS / WARN (confirmed) / FAIL — blocked]
Step 2 pattern check: [no matches / P-XX flagged — warning updated]
Step 3 dedup:         [N in category, no near-duplicates / duplicate — decision]
Decision:             [INSERT / UPDATE R-XXX / DISCARD]
```

HARD FAIL if this block is absent or any step shows FAIL before INSERT runs.

---

## Out of Scope

This skill does NOT:
- Recommend products or apps for purchase (use life-core-shopping)
- Verify lore canon on projects with a dedicated lore-checker
- Generate GDD sections, dialogue, or design docs directly — synthesis feeds those
- Answer factual lookups answerable from chat context with no synthesis required
- Conduct private-dataset statistical analysis — public-source synthesis only

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| references/research-patterns.md | 7 specialized research patterns — triple-pass, architecture-decision, function-reference, skill-audit, creative-synthesis, landscape-scan, session-retrospective |
| references/source-authority.md | Source authority scoring framework, labels, red flags |
| life-core-shopping | Product and app purchase recommendations |
| utility-skill-publisher | Consumes research output during Gate 0 of new skill creation |
| references/d1-validation.md | Research database validation protocol — PART 13 gate steps, SQL patterns, RQG script usage |
| AGENTIF benchmark | Multi-constraint instruction compliance |
| AutoVerifier — arxiv 2604.02617 | Structured claim verification methodology |
| Deep Researcher Sequential Plan Reflection — arxiv 2601.20843 | Sequential pass validity |
| Ask or Assume? — arxiv 2603.26233 | Conditional clarification methodology |
| PRISMA-ScR / Cochrane Rapid Reviews | Rapid review reporting framework |
