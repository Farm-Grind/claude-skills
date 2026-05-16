---
name: utility-ops-scaffolder
description: >
  Bootstraps new Claude projects from a domain brief. Conducts a targeted
  domain scan, then generates seven lean artifacts: project instructions,
  boundaries, skill registry, document register, starter glossary (conditional),
  research synthesis, and a session 1 starter prompt. Prioritizes token
  efficiency — every artifact is designed to stay small, load only what's
  needed, and be trimmed as the project matures. Asks 4–5 clarifying questions
  before generating. Adapts to domain type (creative, technical, research,
  product). Invokes the utility-core-researcher skill for domain grounding; does not
  duplicate it. Use automatically — do not wait to be asked. Trigger on ANY
  of these signals: "scaffold this project", "set up a project for X",
  "help me start a new project around Y", "new Claude project". Do NOT use
  to modify an existing project — that is iteration, not scaffolding. Load
  once per session.
---
SKILL_VERSION: v1.2

# Project Scaffolder

Bootstraps new Claude projects. Lean and efficient by design — the goal is
the minimum scaffold that makes the first session productive and the first
month coherent. Every artifact has a ceiling. Nothing is generated that
doesn't earn its token cost every session it's loaded.

---

## PART 1 — CLARIFYING QUESTIONS

Ask all in a single message. Skip any with obvious answers from the brief.
Do not proceed to domain scan until answered.

**Q1 — Purpose** *(skip if brief answers this)*
"One or two sentences — what is this project for?"

**Q2 — Primary output**
"What will Claude mainly produce? (code / design docs / narrative content /
research / game design / other)"

**Q3 — Your role and expertise**
"How would you describe yourself in this domain?
(e.g., 'solo developer, intermediate' / 'writer, new to this genre')"

**Q4 — Existing material or locked decisions**
"Anything already decided that Claude should know from session one?"

**Q5 — Interaction style**
"How should Claude behave by default? (e.g., 'push back hard' / 'be brief' /
'explore freely')"

**Q5a — Input method** *(ask only if not obvious from brief or Q5 answer)*
"Will input arrive via voice dictation?" If yes, the generated Style block
includes a voice input directive automatically — no further questions needed.

---

## PART 2 — DOMAIN SCAN

Invoke the utility-core-researcher skill in scoping mode — not a full pass, a targeted
sweep. Scope to exactly four questions:

1. What are the canonical references and established best practices? (3–5 sources max)
2. What do people consistently get wrong in this domain?
3. Any adjacent domain worth a glance?
4. What does a good working process look like for this type of project?

Present findings as a correction-window block before generating artifacts:

```
DOMAIN SCAN — [domain]
───────────────────────────────────────────────────
References:  [3–5 sources, one line each]
Pitfalls:    [2–3 bullets]
Adjacent:    [1–2 if genuinely useful, else omit]
Process:     [1–2 sentences]
───────────────────────────────────────────────────
Anything to correct before I generate the scaffold?
```

---

## PART 3 — SEVEN ARTIFACTS

Generate all seven in one response after the domain scan is confirmed.
Each artifact has a defined ceiling. Stay within it.

---

### ARTIFACTS 1+2 — PROJECT INSTRUCTIONS + BOUNDARIES
*Destination: paste this entire block into Claude project custom instructions. One copy-paste. Loaded every session.*

**Instructions are the only artifact loaded automatically every session — every word must earn its place.** Nothing goes in that Claude would do anyway. Nothing that can be handled by a knowledge file or skill instead. Boundaries follow immediately in the same block so both travel together.

```
# [Project Name]

## Role
[Who Claude is. 2 sentences max. Domain expertise + working relationship.]

## Context
[What the project is. Key constraints. Existing materials. 3 sentences max.]

## Outputs
[Bulleted list of what Claude produces here. Specific, not generic.]

## Style
[3–4 bullets. Directness, pushback, format, ask-vs-execute threshold.]

## Rules
[3–5 bullets. Non-negotiables from the domain scan — only things that
would otherwise go wrong. No obvious rules. No positive restatements
of default behavior.]

## Priority
[One sentence. What to work on first.]

---

BOUNDARIES — [Project Name]

ALWAYS (no confirmation needed)
  • [action Claude should take autonomously]
  • [action Claude should take autonomously]

ASK FIRST (confirm before executing)
  • [action that needs user sign-off]
  • [action that needs user sign-off]

NEVER (do not do regardless of request)
  • [hard prohibition from domain scan or user preference]
  • [hard prohibition]
```

**Hard ceiling — Instructions: 200–350 words; Boundaries: ≤3 items per tier.** If instructions run long, cut Rules first — knowledge files carry that load. Boundaries grow through friction, never upfront.

---

### ARTIFACT 3 — SKILL REGISTRY
*Destination: action list. Not loaded into the project.*

```
SKILL REGISTRY — [Project Name]

P1 — Before first working session (2–4 max)
  [name]: [one sentence — what it does and why it can't wait]

P2 — Within first 3 sessions
  [name]: [one sentence]

P3 — When scope demands it
  [name]: [one sentence]

INSTALL FROM EXISTING LIBRARY
  utility-core-researcher / utility-ops-scaffolder / [others already built that apply]
```

**P1 ceiling is hard.** If a skill isn't critical to the quality of
session 1, it belongs in P2. Ruthless prioritization here pays off
across every session.

---

### ARTIFACT 4 — DOCUMENT REGISTER
*Destination: action list. Not loaded into the project.*

```
DOCUMENT REGISTER — [Project Name]

CRITICAL — create before meaningful work begins (1–3 max)
  [name_v1.ext] — [purpose, 1 sentence]

HIGH — create within first month
  [name_v1.ext] — [purpose]

DEFER — create when scope demands it
  [name_v1.ext] — [purpose]

NAMING: [project]_[category]_[name]_v[N].[N].[ext]
Categories: [list relevant ones for this domain]
```

---

### ARTIFACT 5 — STARTER GLOSSARY
*Destination: download and upload as a project knowledge file.*

**Generate only for: creative/narrative, technical/engineering, and
research/knowledge projects.** Skip for product/design projects unless
the brief introduces specialized terminology. If skipped, omit this artifact entirely from the output — do not mention it.

**Hard ceiling: 10 terms.** A glossary with more than 10 entries at
scaffold time is premature — it either covers terms that are obvious
or invents vocabulary the project hasn't earned yet.

Generate as a named `.md` file using the project naming convention:
`[project]_reference_glossary_v1.md`

File contents:

```
# [Project Name] — Glossary v1.0

[Term]: [Definition as it applies in this project specifically.
         1 sentence. Not a dictionary definition — a usage note.]
```

**Token note:** Trim or split as the project grows. When terms become
second nature, remove them rather than letting the file accumulate.

---

### ARTIFACT 6 — RESEARCH SYNTHESIS
*Destination: download and upload as a project knowledge file.*

The domain scan from Part 2, reformatted for persistent reference.
Load selectively — not every session, only when making decisions that
depend on domain grounding.

Generate as a named `.md` file using the project naming convention:
`[project]_reference_domain_v1.md`

File contents:

```
# [Project Name] — Domain Reference v1.0
[date]

## References
  [1] [Title — Source — URL] — [what it contributes, 1 line]
  [2] ...

## Best Practices
  - [practice — why it matters in this project]

## Failure Patterns
  - [failure — how to avoid it]

## Adjacent Insights
  - [domain]: [the transferable idea]

## Open Questions
  [What the scan couldn't answer. Where deeper research is needed.]
```

**Token note:** Reference document only — do not load every session.
Archive by replacing with v2.0 rather than expanding indefinitely.

---

### ARTIFACT 7 — SESSION 1 STARTER PROMPT
*Destination: copy and paste directly into the chat to open Session 1. Not a file — not uploaded.*

**Hard ceiling: 80–120 words.** The project instructions carry the
context. This prompt is just a precise task framing and one unblocking
question. Nothing else.

```
# [Project Name] — Session 1

Goal: [The first priority item. One specific, executable sentence.]

Success condition: [What "done" looks like for this session. One sentence.]

Starting question: [The one decision that, if answered, unblocks the
most subsequent work. Must be a genuine user decision — not something
Claude can resolve from existing material.]
```

---

## PART 4 — DOMAIN TYPE MODIFIERS

Apply to all artifacts when generating.

**Creative / Narrative** (games, novels, worldbuilding, scripts)
- Document register Critical: world bible or design document
- Rules must include: canon protection ("flag invented answers, never fill")
- Glossary: generate — lock world-specific nouns early
- P1 skill: lore/canon checker

**Technical / Engineering** (software, hardware, pipelines)
- Document register Critical: technical specification
- Rules must include: stack enforcement ("flag deviations, never substitute")
- Glossary: generate — lock terminology for stack, patterns, naming
- P1 skill: code-guardian or spec-enforcer
- Project Context must name platform, language, key dependencies

**Research / Knowledge** (literature review, analysis, strategy)
- Document register Critical: source register
- Rules must include: source quality ("flag secondary sources, distinguish primary")
- Glossary: generate — define key concepts and contested terms
- P1 skill: utility-core-researcher (likely already installed)

**Product / Design** (apps, products, UX/UI)
- Document register Critical: product brief or PRD
- Rules must include: user-first ("every decision traces to a user need")
- Glossary: skip unless domain is highly specialized
- P1 skill: spec-enforcer or review-protocol skill

**Voice input modifier** (apply to ANY domain type when Q5a answer is yes)
- Add to Style section of generated instructions:

```
Input frequently arrives via voice dictation. Prompts will contain
transcription artifacts, filler words, mid-sentence restarts, and
stream-of-consciousness structure. Extract the core task intent — do not
treat verbal filler as meaningful instruction. If intent is clear enough
to act on, act — state your interpretation in one sentence only if a
non-obvious inference was made, then execute. Only ask a clarifying
question if genuinely two different tasks could be intended. Never ask
more than one clarifying question per turn. Verbal filler to ignore:
"um", "uh", "I mean", "you know", "like", "so", "anyway", repetition
of the same phrase, trailing incomplete sentences.
```

---

## PART 5 — TOKEN EFFICIENCY PRINCIPLES

These govern every output decision. Apply when in doubt.

**Project instructions are the only automatic load.** Everything else
is staged: knowledge files load on demand, skill files load when their
trigger fires. Design the instructions to be small and self-contained.

**Artifacts 3 and 4 are action lists, not knowledge files.** They are
not uploaded to the project. They live outside it as a to-do list.

**The glossary and research synthesis are reference files — not
context.** They should not appear in every session. Load them when
a decision depends on them. Trim or replace them as the project matures.

**Ceiling enforcement:**
- Instructions: 200–350 words
- Boundaries: ≤9 items total (3 per tier)
- Combined instructions + boundaries block: one copy-paste into project custom instructions
- Skill registry P1: ≤4 skills
- Document register Critical: ≤3 documents
- Glossary: ≤10 terms
- Session 1 starter: 80–120 words

**The test for any instruction or rule:** "If I removed this, would
something go wrong?" If the answer is "probably not" or "Claude would
figure it out," remove it.

---

## PART 6 — DELIVERY AND ITERATION

After all seven artifacts, output this block — once. It is a tearaway:
read it, act on it, then discard it (or trim it to a 3-line note).

The tearaway uses real filenames and action verbs — not artifact numbers.
If Artifact 5 (glossary) was not generated, omit its upload step entirely.

```
SCAFFOLD DELIVERED

FIRST ACTIONS (in order):
  1. Copy the Instructions + Boundaries block → paste into project custom instructions
  2. Download [project]_reference_domain_v1.md → upload as project knowledge file
  3. Download [project]_reference_glossary_v1.md → upload as project knowledge file
     [omit this line if glossary was not generated]
  4. Build P1 skills: [list names from Skill Registry]
  5. Create Critical documents: [list names from Document Register]
  6. Copy the Session 1 Starter Prompt → paste into first chat to begin

ITERATION TRIGGERS:
  Wrong output repeatedly → add a Rule to Instructions
  Keeps asking obvious questions → raise the ALWAYS ceiling in Boundaries
  Tone is off → revise Style in Instructions
  A section never gets used → delete it

OPEN ITEMS: [unresolved questions from the clarifying session or domain scan]
```

---

## COMMON FAILURE PATTERNS

| Pattern | What it looks like | Correct behavior |
|---|---|---|
| Instructions over ceiling | 500+ words, covering edge cases | Cut to 200–350; move domain detail to knowledge files |
| Instructions and Boundaries split | Two separate copy-paste operations | Always deliver as one merged block |
| Knowledge files as raw text | Glossary/research pasted inline with no filename | Generate as named `.md` files ready to download and upload |
| Tearaway uses artifact numbers | "Upload Artifact 5" with no filename | Use real filenames; user should never cross-reference the skill |
| Glossary step included when not generated | "Upload glossary [if generated]" confuses user | Omit the step entirely when glossary was skipped |
| P1 skill overload | 6 skills "critical" before session 1 | Hard cap at 4; if it can wait 3 sessions, it's P2 |
| Glossary as dictionary | 40 terms, general definitions | 10 terms max; project-specific usage notes only |
| Starter prompt as briefing | 300-word context dump | 80–120 words; instructions carry the load |
| Research synthesis as permanent context | Loaded every session via instructions reference | Reference document only — load when needed, not automatically |
| Boundaries omitted | No tier system, autonomy ambiguous | Always generate; 3 items per tier is enough to start |
| Domain scan skipped | Scaffold generated without research | Scan feeds Domain Rules and Boundaries directly; skip = weak scaffold |

---

## Examples

**Example 1 — Minimal brief, creative domain**

User: "Scaffold a project for writing a dark fantasy novel."

Q1 skipped (purpose clear from brief). Q2–Q5 answered. Domain scan: worldbuilding, character arc, and scene-structure refs; common failure = outline without sensory grounding. 7 artifacts generated. Instructions + Boundaries (one copy-paste block): Role = narrative co-author; Rules include canon-protection clause. Skill registry P1: lore-checker, worldbuilding skill. Document register Critical: world-bible_v1.md. Glossary generated (world-specific nouns, 10-term ceiling). Research synthesis as named .md file. Starter prompt 80–120 words. Tearaway uses real filenames; no artifact numbers.

**Example 2 — Technical project with voice input**

User: "Set up a project for a React Native workout tracker app. I use voice dictation."

Q5a confirmed — voice input. Domain scan: React Native, Expo docs; pitfall: component over-optimization before MVP. Instructions include voice input directive from Part 4 modifier. Glossary generated — stack terms locked early. P1 skill: code-guardian equivalent. Document register Critical: technical-spec_v1.md. Boundaries ALWAYS: scaffold components with full prop types; ASK FIRST: change stack decisions; NEVER: invent library behavior from memory. All 7 artifacts delivered in one response after domain scan confirmed.

**Example 3 — Glossary skip, product domain**

User: "Start a project for redesigning a SaaS onboarding flow."

Domain type: Product/Design → Part 4 modifier fires. Glossary skipped (no specialized terminology). Artifact 5 absent from output. Tearaway omits the upload step entirely — no "upload glossary [if generated]" ambiguity. Document register Critical: product-brief_v1.md. Skill registry P1: spec-enforcer. COMMON FAILURE PATTERN check: starter prompt ≤ 120 words; instructions + boundaries delivered as one block.

---

## Out of Scope

This skill does NOT:
- Modify or iterate on an existing project — this skill bootstraps only; ongoing iteration uses project-specific skills
- Replace domain-specific skills — P1/P2/P3 skills flagged in the registry must be built separately using utility-core-skill-gate
- Conduct a full research pass — invokes utility-core-researcher in scoping mode only (4 questions, 3–5 sources max)
- Manage ongoing project state — session continuity, decisions, and document versioning belong to project tracker skills

---

## SEE ALSO

| Resource | Domain |
|---|---|
| utility-core-researcher (skill) | Domain scan — invoke for Part 2 |
| utility-core-skill-gate (skill) | Run when building P1 skills post-scaffold |
| utility-ops-prompt-master (skill) | Refine starter prompt if needed |
| Addy Osmani — "How to write a good spec for AI agents" | Three-tier boundaries; spec as executable artifact |
| Anthropic — "Effective Harnesses for Long-Running Agents" | Session continuity; success conditions; clean state protocol |
