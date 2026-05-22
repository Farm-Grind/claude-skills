# Dispatcher Skeleton — Canonical Pattern Reference

Loaded by skill-publisher Gate 3 when a new dispatcher is being designed, or
when an existing skill is being audited against the dispatcher pattern. The
canonical reference implementation is `/mnt/skills/user/persona-developer/SKILL.md`.
Read it before any new dispatcher work.

This file contains:
1. Frontmatter template
2. Body skeleton (5 parts)
3. Classification table template (with worked Example column)
4. Domain code naming convention
5. Cross-domain-map.md template
6. Reference file minimum structure
7. When to add scripts/
8. When to add assets/
9. Worked dispatcher example (compact)

---

## 1 — Frontmatter Template

```yaml
---
name: <kebab-case-name>
description: >
  <Third-person sentence: what the skill does.> Use automatically — do not
  wait to be asked. Trigger on ANY of these signals: <quoted phrase 1>,
  <quoted phrase 2>, <quoted phrase 3>, <named context signal>. Do NOT
  trigger for: <named adjacent domain> (use <sibling-skill>), <other
  exclusion>. Load once per session.
---
SKILL_VERSION: v1.0
```

Total description length: ≤ 1,024 characters. Run Gate 7 char count.

---

## 2 — Body Skeleton (5 Parts)

Multi-domain dispatcher required structure:

```
# <Skill Title> — Dispatcher

<One-line context: project, domain, or scope.>

Type: dispatcher

---

## GOTCHAS

<>=2 named failure modes Claude exhibits without this skill.>

---

## PART 0 — DOMAIN CLASSIFICATION

<Classification table with Code | Domain | Triggers | Example columns.>
<Multi-domain rules table.>

Classification block (visible output before any reference load):

    DOMAINS ACTIVATED: [codes]
    Active codes: [list]
    Reference files to load: [list paths]
    Multi-domain: [yes — load cross-domain-map.md / no]

---

## PART 1 — REFERENCE FILE LOADING

<Table: Active code | Reference file path.>

**Always reload reference files in each response turn that needs them.**
Reference file content does not persist between turns automatically.

---

## PART 2 — PRE-GENERATION PROTOCOL

<Ordered checklist drawn from loaded reference files.>
<Any HARD FAIL conditions.>

---

## PART 3 — SYNTHESIS PROTOCOL

When multiple domain codes are active:
1. Load cross-domain-map.md
2. Resolve conflicts per the map's priority rules before generating
3. Produce a single integrated response — no per-domain section headers
4. Apply all loaded reference rules simultaneously

---

## PART 4 — POST-GENERATION AUDIT

<Universal checks that apply to all output regardless of domain.>

---

## PART 5 — META-ADVERSARIAL REVIEW

<Dispatcher-specific challenges run before output is presented.>
1. Scope check
2. Integration check
3. Conflict check
4. Completeness check
```

Single-domain dispatcher: PARTS 0, 1, 2, 4 only. No synthesis, no
cross-domain map, no meta-adversarial review required.

---

## 3 — Classification Table Template

```markdown
| Code | Domain | Triggers | Example |
|---|---|---|---|
| `XX` | <Domain name> | keyword1, keyword2, "quoted phrase" | "User asks ..." |
| `YY` | <Domain name> | keyword3, keyword4 | "User says ..." |
```

The Example column is required (skill-publisher Gate 3). A worked example
per row materially improves routing accuracy at runtime.

---

## 4 — Domain Code Naming Convention

Preferred: 2–6 character ALL CAPS codes when domain count >= 5.
Examples from persona-developer: `DS`, `RN`, `DB`, `MUX`, `A11Y`, `SI`, `DM`.

Acceptable: full words when domain count < 5 OR when the word is the natural
identifier and no compact form is clearer.
Examples from persona-game-designer: `BALANCE`, `PSYCHOLOGY`, `IDLE-MATH`.

Avoid: mixed-case codes, hyphenated multi-word codes longer than 12 chars,
codes that collide with another skill's domain codes.

---

## 5 — Cross-Domain-Map.md Template

Required for multi-domain dispatchers. Structure:

```markdown
# Cross-Domain Interaction Map

Required reference for <skill name> when 2+ domain codes are active.

---

## Domain Priority Order (conflict resolution)

When domain rules conflict, apply in this order (highest to lowest):

1. **<CODE>** — <reason this domain wins>
2. **<CODE>** — <reason>
3. **<CODE>** — <reason>

---

## Known Cross-Domain Interactions

### <CODE_A> + <CODE_B>

**Interaction:** <how the two domains touch>
**Conflict / No conflict:** <named conflict or explicit non-conflict>
**Synthesis:** <how to produce one integrated answer>
**Watch for:** <specific pattern that signals the interaction needs handling>

### <CODE_A> + <CODE_C>

...
```

One `###` section per relevant pair. Pairs that never co-occur in practice
can be omitted. SkillRouter (arxiv 2603.22455) classifies multi-skill queries
into three structural types — complementary (43%), substitute/overlap, and
conflicting — this template covers all three.

---

## 6 — Reference File Minimum Structure

Required for every reference file:
- H1 matches the filename (without `.md`)
- Imperative rule voice — same as body
- No nested references (do not cite other reference files from within)
- TOC required when file > 100 lines (skill-publisher Gate 6)

Recommended sections (when applicable):
- Purpose / when loaded
- Methodology / procedure
- Output format
- Failure modes / what to flag

---

## 7 — When to Add scripts/

Scripts hold executable code. Source code NEVER enters context — only stdout/
stderr does. Add `scripts/` when ANY of these are true:

- The same procedure is rewritten as inline bash repeatedly across skill runs
- Deterministic reliability matters (validation, char counts, regex sweeps,
  file packaging, schema introspection, query construction)
- The procedure has no judgment step — same inputs always produce same outputs
- Conversion: file format, encoding, structure transformation

Do NOT use scripts/ for:
- Judgment calls or interpretive decisions
- Reasoning the model needs to do
- Routing logic (that lives in the body)

Reference example: `/mnt/skills/public/pdf/scripts/` — 8 Python scripts for
deterministic PDF manipulation. The PDF SKILL.md doesn't describe HOW to
rotate a page; it calls `scripts/rotate_pdf.py` and gets the result back.

Naming: lowercase, hyphen or underscore separated, language extension
(`.py`, `.sh`, `.js`).

---

## 8 — When to Add assets/

Assets hold output resources. Never loaded into context. Claude sees only
the path. Add `assets/` when ANY of these are true:

- Skill produces a file artifact (docx, pptx, html) that uses a fixed template
- Skill output includes fonts, logos, images, or other binary resources
- Skill copies a boilerplate codebase or scaffolding structure into a target
  location

Do NOT use assets/ for:
- Text content the model must read to follow a pattern (that is references/)
- Documentation or examples (that is references/)
- Anything where the model needs to parse the file contents

Naming: descriptive filename with extension matching content type.

---

## 9 — Worked Compact Dispatcher Example

Three-domain dispatcher with cross-domain conflicts:

```markdown
---
name: example-dispatcher
description: >
  Routes UI work across three domains: layout, typography, color. Use
  automatically — do not wait to be asked. Trigger on ANY of these signals:
  "design this screen", "what color should X be", "what font size",
  "layout for", named UI component being designed. Do NOT trigger for:
  code generation (use persona-developer). Load once per session.
---
SKILL_VERSION: v1.0

# Example Dispatcher

Routes UI design questions across three domains.

Type: dispatcher

## GOTCHAS
1. Routing without classification — output mixes layout/typography/color
   without committing to which domain dominates.
2. Reference files not re-viewed across turns — second-turn answers run
   from stale memory.

## PART 0 — DOMAIN CLASSIFICATION

| Code | Domain | Triggers | Example |
|---|---|---|---|
| `LAY` | Layout | grid, spacing, columns | "How should X sit next to Y?" |
| `TYP` | Typography | font, size, weight, line | "What size for headings?" |
| `COL` | Color | color, contrast, palette | "What color for the CTA?" |

Multi-domain rules:
| Combination | Trigger | Why |
|---|---|---|
| LAY + TYP | "How should the headline area work" | Layout grid drives type scale |
| TYP + COL | "Make this readable" | Contrast intersects font weight |

Classification block:
    DOMAINS ACTIVATED: [LAY] [+ TYP] [+ COL]
    Reference files to load: [references/layout.md, references/typography.md, references/color.md]
    Multi-domain: yes — load cross-domain-map.md

## PART 1 — REFERENCE FILE LOADING

| Active code | Reference file |
|---|---|
| `LAY` | `references/layout.md` |
| `TYP` | `references/typography.md` |
| `COL` | `references/color.md` |
| Multi-domain (2+) | Also load `references/cross-domain-map.md` |

Always reload reference files each turn that needs them.

## PART 3 — SYNTHESIS PROTOCOL
1. Load cross-domain-map.md
2. Apply priority order: COL contrast rules win over TYP size, TYP rules
   win over LAY whitespace.
3. Produce single integrated answer.

## PART 5 — META-ADVERSARIAL REVIEW
1. Scope check — did codes cover the full request?
2. Integration check — single answer, not three?
3. Conflict check — name any rule conflict and resolution?
4. Completeness check — every loaded ref's checks ran?
```

Required references for this example: `layout.md`, `typography.md`,
`color.md`, `cross-domain-map.md`. Four files in `references/`. No scripts/,
no assets/ — pure judgment skill.
