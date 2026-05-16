# Research Patterns — Specialized Methodologies

Reference for `utility-data-analyst`. Load the specific section when the corresponding Part 1 mode is declared. Do not execute a pattern from memory — `view` the section first.

## Contents

- § 1 — Triple-Pass Methodology
- § 2 — Architecture Decision Research
- § 3 — Function Reference Research
- § 4 — Skill/Document Audit Research
- § 5 — Creative Synthesis Research
- § 6 — Landscape / Horizon Scan Research
- § 7 — Session Retrospective Research

---

## § 1 — Triple-Pass Methodology

**Applicable when:** destination is a synthesis document feeding a significant architectural or design decision; OR user explicitly requests "triple pass" / "deep dive"; OR prior research is absent and topic is high-stakes.

**Research basis:** Sequential scaling outperforms parallel scaling for synthesis tasks (Chopra 2025, "The Sequential Edge"; arxiv 2601.20843). Cross-source verification mandatory in production-quality research agents (AutoVerifier, arxiv 2604.02617).

### PASS 1 — FIND (breadth over depth)

Goal: cast widest possible net. No quality filter yet.

1. Run 6–10 searches across all 5 facets
2. Accept any source that addresses the question, regardless of quality
3. Record everything found, including weak findings
4. Identify 3–5 primary sources for deeper follow-up
5. Produce raw finding list (not yet synthesized)

Output: raw findings list — complete, unfiltered.

### PASS 2 — VERIFY (depth over breadth)

Goal: test every Pass 1 finding against new sources. Pass independence rule applies — sources must be new, not Pass 1 reordered.

1. For each Pass 1 finding: trace evidential chain
2. For single-source claims: search for corroboration or contradiction
3. For widely-cited claims: verify origin (trace to primary)
4. Flag confidence per finding: VERIFIED / PARTIAL / UNVERIFIED / CONTESTED
5. Identify conflicts — do not flatten
6. Cross-source verification: do independent sources agree?

Output: confidence-labeled findings with conflicts named. VERIFICATION PASS must show `New sources not in Pass 1: N>0`.

### PASS 3 — SYNTHESIZE (integration)

Goal: build actionable findings from verified base. Resolve conflicts. Identify destination implications.

1. For VERIFIED and PARTIAL findings: integrate into synthesis
2. For CONTESTED findings: present both sides with conflict named
3. For UNVERIFIED findings: find supporting evidence or cut
4. Combine convergent findings from different sources into single claim
5. Derive RECOMMENDED INTEGRATION from verified finding set
6. Identify open questions: what would change this synthesis if answered

Output: complete synthesis per Part 7 format. Parts 9 and 10 of SKILL.md run after Pass 3, before delivery.

### Stopping criterion

A Pass is complete when no new facets are being covered and the last 2 searches return no new findings. Do not add searches to reach a count.

---

## § 2 — Architecture Decision Research

**Applicable when:** choosing between competing tools, platforms, frameworks, or approaches for a significant project decision.

**Research basis:** Comparative analysis framework (Thesify 2026); multi-criteria decision-making for technology selection (MDPI 2025). Differential diagnosis methodology (medicine) and FMEA (engineering) converge on the same two-step structure: candidates upfront, then eliminate via pre-specified criteria.

### Step 1 — CONSTRAINT DEFINITION

Before searching, define hard requirements (must-have, binary eliminators) and quality criteria (nice-to-have):
- Hard: "must work without API credentials", "must persist across sessions", "must run in current operating environment"
- Quality: "error recovery", "call latency", "maintenance burden"

Document the constraint set before evaluating any option.

### Step 2 — CANDIDATE IDENTIFICATION

Identify all plausible options. Cast wide. Do not pre-filter on priors. Include unlikely options — they provide useful contrast.

### Step 3 — HARD CONSTRAINT ELIMINATION

For each candidate, evaluate against every hard requirement. Candidates failing any hard requirement are eliminated immediately. Document the elimination reason — this is the decision audit trail.

Output: `ELIMINATED: [option] — [specific constraint failed]`

This is the structural prevention of the GitHub-MCP-as-storage failure (F3 — non-viable options consumed 2 sessions). Worst-case-first: catastrophically non-viable candidates (architecture-incompatible, requires unavailable infrastructure) screened first.

### Step 4 — SURVIVING CANDIDATE RESEARCH

For options surviving Step 3: run deep research on each. Cover:
- Documented capabilities
- Documented limitations
- Failure modes from practitioners
- Error recovery patterns
- Total cost of use (time, complexity, tokens, maintenance)

Do not accept vendor documentation as complete — check practitioner and community sources for gaps the vendor does not document.

### Step 5 — COMPARATIVE ANALYSIS

Map each surviving candidate against quality criteria from Step 1. Use a constraint matrix — rows = candidates, columns = quality criteria. Provide evidence per cell, not assertions.

### Step 6 — OPEN QUESTIONS

What cannot be determined from available sources? For each open question, specify what test or verification would resolve it. The decision is not final until open questions are resolved or explicitly deferred. Decisions with unresolved open questions carry a risk flag.

### Step 7 — RECOMMENDATION

State the recommendation with the constraint matrix as evidence. Name the next-best alternative and the conditions under which it would be preferred.

---

## § 3 — Function Reference Research

**Applicable when:** building a technical reference for tools, APIs, MCPs, or platform capabilities.

**Research basis:** AutoVerifier multi-layer verification (arxiv 2604.02617); citation auditing zero-assumption protocol (arxiv 2511.04683) — 91.7% verification rate with <0.5% false positives.

### Step 1 — LIVE SCHEMA DISCOVERY

Use tool_search or direct schema fetch to get live tool definitions. Record: tool names, parameters (required vs. optional), return types. This is the ground truth. Never assume schema from training knowledge.

### Step 2 — OFFICIAL DOCUMENTATION VERIFICATION

For each tool/function in the schema:
- Find official documentation (vendor docs, official GitHub, release notes)
- Verify each schema claim against docs — is the parameter truly optional?
- Flag discrepancies between schema and docs explicitly

### Step 3 — PRACTITIONER/COMMUNITY GAP-FILL

For behaviors not covered by official docs:
- Search practitioner accounts, community reports, issue trackers
- Look for: edge cases, rate limits, known bugs, workarounds
- Weight recent sources heavily — tool behavior changes with releases

### Step 4 — CLASSIFICATION

Classify each finding:
- ✅ CONFIRMED — verified against official documentation
- 🔬 SCHEMA-ONLY — present in live schema, no official doc coverage
- ⚠️ CORRECTED — prior claim was wrong; here is the correct behavior
- ❌ INVALIDATED — schema claim is false per official docs
- 🚧 UNVERIFIED GAP — cannot be resolved without live testing

### Step 5 — OPEN GAPS LIST

For every behavior that could not be verified:
- State the gap explicitly
- State what test would resolve it
- Note the risk if the gap is load-bearing for production use

No papering over gaps. If it cannot be verified, say so.

---

## § 4 — Skill/Document Audit Research

**Applicable when:** auditing an existing skill, reference document, or project artifact for factual accuracy, especially when the document may contain time-sensitive or post-cutoff claims.

**Research basis:** Internal audit methodology — accuracy, completeness, integrity of data (eCampus Ontario); AutoVerifier structured audit pipeline (arxiv 2604.02617); AI citation auditing zero-assumption protocol.

### Step 1 — FULL READ

Read the complete artifact before making any claims about it. No partial reads. No assumptions about content from filenames or descriptions.

### Step 2 — CLAIM CLASSIFICATION

For every claim, classify:
- **Type A** — Timeless mechanics: rules, relationships that do not change
- **Type B** — Time-sensitive: post-cutoff facts, version-specific behavior, prices, patch notes, current states
- **Type C** — Domain-specific: technical claims about a specific field
- **Type D** — Inferences/extrapolations: logical conclusions, not sourced facts

Only Type B and Type C claims require external verification. Type A and D require internal consistency checking.

### Step 3 — TARGETED VERIFICATION

For each Type B and Type C claim:
- Run a targeted web search to verify or contradict
- Look for: (a) official source confirming, (b) official source correcting, (c) community consensus if no official source
- Do not accept a single source as sufficient for a correction

### Step 4 — SEVERITY CLASSIFICATION

For each verified error:
- **CRITICAL** — would cause incorrect action if followed
- **MAJOR** — wrong behavior or significant inaccuracy
- **MINOR** — outdated detail, phrasing issue, edge case

### Step 5 — CORRECTION LIST

Document each correction:
- Original claim: [verbatim from artifact]
- Correct claim: [replacement]
- Source: [URL or citation]
- Severity: [CRITICAL / MAJOR / MINOR]

Internal consistency issues (Type A/D errors) are documented separately as logical inconsistencies, not factual corrections.

---

## § 5 — Creative Synthesis Research

**Applicable when:** building a cross-source synthesis of archetypes, patterns, tropes, or structures from training knowledge (mythology, fantasy, narrative design, world-building, stable taxonomies).

**Research basis:** Lévi-Strauss structural analysis of myth; Campbell's monomyth structural framework; Computable Structuralism (arxiv 2601.15078) confirming cross-tradition analysis across 80 narratives from 4 categories.

External web search is typically NOT needed. Source material is training knowledge — cultural and narrative patterns across mythology, games, literature, media. External search is appropriate only to verify a specific factual claim or find a specific source.

### Step 1 — DEFINE THE COMPOSITE PROFILE

Before research begins:
- What functional role or pattern does this composite serve?
- What dimensions differentiate instances of this pattern? (form, mechanism, cost, power axis)
- What would disqualify something from being this pattern?

This definition is the filter for Step 2.

### Step 2 — SOURCE SWEEP (by domain)

Sweep each source domain separately before combining:
- Mythology: Norse, Greek, Celtic, Egyptian, Hindu, Arthurian, Slavic, Japanese, Mesoamerican
- D&D/TTRPGs: canonical artifacts, published modules, system sourcebooks
- Video games: genre-defining titles, landmark entries
- Fantasy literature: canonical authors in the genre
- Mass media: film, TV, anime — cultural penetration matters
- Tabletop/CCGs if relevant

Record instances domain by domain. Do not start combining yet.

### Step 3 — CROSS-TRADITION THRESHOLD CHECK

A pattern qualifies as a dimensional constant only if it appears in N≥3 independent source domains with recognizably the same functional role.

"Recognizably the same" — an observer unfamiliar with both sources would describe the function using the same vocabulary.

Single-domain patterns are noted but not elevated to composite status.

### Step 4 — COMPOSITE FORMATION

For each pattern meeting the threshold:
- Name it (functional description, not source-specific name)
- Define the invariant: what is always true across instances
- Define the variant: how different traditions express it differently
- Identify the structural slot it fills in its containing system

### Step 5 — CLASSIFICATION TABLE

Organize composites into a structured table:
- Columns: Composite name / Invariant core / Primary axis / Cost structure
- Design-signal column: what makes it usable for the destination

Avoid: one-entry "composites" (these are references, not patterns); over-specifying the invariant (tighter is better than broader).

### Adversarial review override

For Creative Synthesis mode, Challenge 1 (synthesis overclaim) is replaced with the cross-tradition threshold check: does each composite meet N≥3 independent domain threshold? Flag any that do not.

All findings carry [TRAINING KNOWLEDGE — not externally verified] label. No finding labeled [VERIFIED].

---

## § 6 — Landscape / Horizon Scan Research

**Applicable when:** exploring an unfamiliar domain to understand what exists, who the players are, where the edges are — WITHOUT a specific decision. Goal is orientation, not selection.

**Research basis:** Horizon scanning methodology — OECD definition: "systematic examination of potential threats and opportunities, with emphasis on new technology and its effects." Bibliometric horizon scanning (arxiv 2202.13480); NIHR scoping review of horizon scanning approaches (2025). Distinct from architecture decision research (which makes a choice) and function reference research (which documents capabilities).

### Step 1 — SCOPE ANCHORS

Define the space boundary. What is inside / outside the scan? Define the time horizon: current state only, or emerging developments? Name the scan output type — landscape map, trend list, player/tool inventory, gap map, or synthesis narrative.

### Step 2 — ANCHOR SOURCES FIRST

Find 2–3 authoritative sources defining the landscape's current state: official bodies, standards organizations, survey papers, state-of-the-art reviews. These anchor the center of the space.

### Step 3 — PERIPHERY SWEEP

After anchoring the center, sweep the edges:
- Emerging approaches not yet in the mainstream
- Adjacent domains that intersect with this space
- Counter-positions or alternative framings

Do not flatten edge cases. Edge is often where the most useful signal is.

### Step 4 — TAXONOMY / MAP

Organize findings into a structure:
- Categories or clusters of approaches
- Relationships between them (competing / complementary / sequential)
- Whitespace: where is the space NOT covered?

### Step 5 — SIGNAL IDENTIFICATION

For each category or cluster: mature/stable or emerging/volatile? For emerging areas: what would accelerate or block maturation? For stable areas: what would disrupt them?

Output: a map with signal labels, NOT a recommendation. The scan informs future research or decisions; it does not make them.

---

## § 7 — Session Retrospective Research

**Applicable when:** a series of similar sessions has produced recurring frustration, confusion, or errors. Goal: identify the root cause through structured retrospective analysis.

**Research basis:** Internal audit methodology; root cause analysis (Six Sigma, AAQ Auburn, Tableau convergent); AutoVerifier cross-source verification pattern. Proximate vs. root cause distinction is the most commonly skipped step in applied fix design (NF1).

### Step 1 — INCIDENT INVENTORY

List every session where the problem occurred:
- What was the symptom?
- What was the expected outcome vs. actual outcome?
- Was the same underlying cause present across all sessions?

### Step 2 — ROOT CAUSE HYPOTHESIS

For each symptom cluster, form a testable hypothesis about the root cause.

Good: "The GitHub connector is connected but provides no callable tools in chat sessions because it is a first-party integration, not an MCP."
Bad: "Something is wrong with the GitHub connector."

### Step 3 — HYPOTHESIS VERIFICATION

Search for evidence that confirms or contradicts each hypothesis. Target: official documentation, community reports, GitHub issues. Zero-assumption protocol: do not assume any prior understanding is correct.

### Step 4 — ROOT CAUSE CONFIRMATION

A root cause is confirmed when:
- It explains all documented symptoms
- It is supported by at least one authoritative external source
- No documented symptom is left unexplained

### Step 5 — RESOLUTION SPECIFICATION

For the confirmed root cause:
- What is the correct behavior?
- What specific change prevents recurrence?
- Is this a knowledge gap (update a skill), a process gap (update a protocol), or a configuration gap (change settings)?

Output: root cause statement + resolution specification. Never just "do not do X" — always "do Y instead because [reason]."

### 5-Whys validity check

The 5-whys chain stops at root cause when the next "why" would point to a structural property of the system rather than a behavioral choice. If the chain bottoms out at "the skill was designed to evaluate source quality, not outcome accountability" — that is root. If it bottoms out at "Claude should have done X" — that is symptom; ask why one more level.
