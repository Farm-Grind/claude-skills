# Full Pass Methodology — Research Execution and Synthesis

Reference for `utility-data-analyst`. Load this file when mode is Full Pass,
Quick Audit, or Spot Check. Do not execute any methodology step from memory —
`view` this file first.

## Contents

- § PART 3 — Prior Reference Scan
- § PART 4 — Rapid Review Scope Declaration
- § PART 5 — Viability Screen
- § PART 6 — Search Execution
- § PART 7 — Synthesis Output Format
- § PART 8 — Citation Format
- § PART 9 — Adversarial Self-Review
- § PART 10 — Verification Pass
- § PART 11 — Quick Audit and Spot Check
- § PART 12 — Common Failure Patterns

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
