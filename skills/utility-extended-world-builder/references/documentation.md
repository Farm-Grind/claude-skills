# Documentation Architecture — World-Builder Outputs

This file is loaded in DOCUMENT mode and referenced during CREATE when outputs need to be
organized for long-term use. It governs how worldbuilding output is structured, formatted,
and maintained across sessions and projects.

---

## TABLE OF CONTENTS

1. Document Ecosystem
2. Project Identity Manifest
3. DUAL Format Rules
4. Claude-Readability Principles
5. Modular Loading — Token Efficiency
6. Session Handoff Protocol

---

## 1. DOCUMENT ECOSYSTEM

Never monolithic. Split worldbuilding output by audience and function.

| Document | Audience | Function |
|---|---|---|
| World Bible / Lore Bible | Writers, artists, designers | Canon facts: history, factions, characters, tone |
| World Design Document | Designers, developers | Rules: systems, magic/tech specs, economy |
| Geography & Atlas | All | Physical world: maps, climate, terrain, settlements |
| Culture Sheets | Writers, artists | Per-faction deep dives: customs, language, food, religion |
| Timeline | All | Chronological record; gaps and retcons tracked explicitly |
| Canon Reference Sheet | Claude + human | Quick-access facts for consistency checking |

The Canon Reference Sheet is a parallel fast-access layer — canonical facts in table form.
It is not a summary of the full bible. It is a separately maintained fast-lookup document
that is always loaded first when working on an existing world.

**Why split?**
A 200-page monolithic document loads its full token weight into every session, whether or
not the current task needs it. Splitting by topic means sessions load only what's relevant.
A monolithic document also serves no reader well — it conflates the precision needed for
implementation with the narrative texture needed for writing.

---

## 2. PROJECT IDENTITY MANIFEST

Every world maintained with Claude assistance needs a project identity manifest. This is a
small CLAUDE-ONLY document (1–2 pages) that declares:

```
PROJECT: [World name]
Type: [novel / game / comic / screenplay / other]
Active documents: [list of documents in this world, with brief description of each]
Sibling skills: [list of any project-specific skills that own specific domains]
Canon tier model: [primary / extended / development — see audit-protocol.md]
Quick constraints: [3–5 non-negotiable world facts for fast orientation]
```

This document is loaded at the start of any session involving this world. Its job is to
prevent context contamination in a multi-project workflow — Claude reads the manifest and
knows exactly which world is active and what canonical constraints apply.

The manifest is maintained by the creator, not auto-generated. Claude can draft it; the
creator confirms and updates it.

---

## 3. DUAL FORMAT RULES

Documents read by both humans and Claude use DUAL format. This is the standard for all
world documentation except the Canon Reference Sheet (CLAUDE-ONLY) and marketing/pitch
materials (HUMAN-ONLY).

**DUAL format core rules:**

- **Numbered headings throughout.** All sections use `# N.` / `## N.N` / `### N.N.N` (3
  levels max). This enables section-anchor parsing — Claude can reliably reference "section
  2.3" without ambiguity across long documents.
- **Human prose layer.** Read the document skipping all callout blocks. If it reads
  coherently as a standalone document — pass. If it requires callout blocks to make sense —
  the human layer is incomplete.
- **Decision callout blocks.** Five standard formats, no variations:

```
| ✓ LOCKED — [topic] | [Decision in one sentence.] |
| --- | --- |

| ⚠ OPEN — [topic] | [What is unresolved. What decision is needed.] |
| --- | --- |

| Instructions for Claude | [Imperative instruction.] |
| --- | --- |

📌 TODO: [What must be defined before this section is complete.]

⚠ DO NOT INVENT: [topic] — [What to do instead.]
```

- **OPEN items consolidated.** At the end of each major section AND at the end of the
  document, all OPEN items are listed in one place. Never leave an OPEN item only inline.
- **Section order:** Summary → core content → open items → Claude quick-reference (optional).

**DUAL format validity test:**
Read the document skipping all callout blocks. If the prose layer reads coherently — pass.
If it requires callout blocks to make sense — fail. Fix the human layer before delivery.

---

## 4. CLAUDE-READABILITY PRINCIPLES

World documentation read by Claude degrades in specific, predictable ways. Apply these
principles to all documents used in AI-assisted worldbuilding.

**"Lost in the middle" mitigation:**
Research finding: across all frontier models, early and late context achieves 85–95% recall
accuracy; middle sections drop to 76–82%. Canonical facts that must be reliably retrieved
belong at the beginning of a document or in the separate Canon Reference Sheet — not buried
in the middle of a 20,000-word lore bible.

**Size targets:**
- Any single document loaded into a session: under 20,000 words / ~25,000 tokens.
- Above this size: split into sub-documents. Use the document ecosystem from Section 1.
- The Canon Reference Sheet: under 2,000 words. It must be fully loadable with high recall.

**Atomic entries:**
One location, one faction, one character, one magic system per document entry. Do not
co-locate unrelated content because it fits on the same page. Links between entries (by
reference, not by embedding) preserve navigability.

**Index document:**
For worlds with five or more split documents, maintain a master index (CLAUDE-ONLY, 1 page)
that lists every document, what it covers, and its current status. Claude loads the index
first; it does not load everything simultaneously.

**Consistent callout vocabulary:**
Mixed marker styles break Claude's ability to scan by pattern. Once you commit to `✓ LOCKED`
and `⚠ OPEN`, use them everywhere and exclusively. Do not mix with `**NOTE:**`, `> blockquote`,
or ad-hoc bold.

---

## 5. MODULAR LOADING — TOKEN EFFICIENCY

The skill for modular loading: load only what the current task needs, not the whole world.

**Task → document mapping:**

| Task | Load |
|---|---|
| NPC or dialogue writing | Canon Reference Sheet + Culture Sheet for relevant faction |
| Magic system development | World Design Document (magic section) + creation-domains.md (Sections 6–7) |
| Location scene-setting | Atlas entry for that location + Canon Reference Sheet |
| Political intrigue | World Design Document (politics section) + Timeline |
| World audit | Manifest + Canon Reference Sheet + document register |
| Gap fill in specific domain | The relevant domain document + audit-protocol.md |

The Canon Reference Sheet loads in every session involving an existing world. Everything
else is loaded on-demand.

**Never load:**
- The full lore bible for a task that only touches one location
- The timeline for a task that only involves a single scene
- The full cast for a task that involves two characters

**The manifest gate:**
Before any worldbuilding output is generated for an existing world, the project identity
manifest is loaded and confirmed. This is the single mechanism that prevents cross-project
contamination in a multi-world workflow.

---

## 6. SESSION HANDOFF PROTOCOL

Every session that produces worldbuilding decisions, additions, or changes ends with a
handoff block. This applies to CREATE, AUDIT, DEEPEN, and DOCUMENT modes.

Format:

```
SESSION HANDOFF — [World Name] — [Date]

Documents updated this session:
- [Document name]: [What was added or changed]

New OPEN items created:
- [Item description] → [Document where it should be recorded]

New LOCKED decisions made:
- [Decision summary] → [Document where it should be recorded]

Documents to create (if new world):
- [Document name]: [Purpose] — [Priority: create now / defer]

Recommended next session focus:
- [Most important unresolved item]
```

The handoff block is not optional. Decisions left only in chat are not in the world.
Every decision made in a session must route to a document. The handoff block is the
mechanism that enforces this.
