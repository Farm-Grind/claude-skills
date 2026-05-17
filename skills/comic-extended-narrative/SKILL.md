---
name: comic-extended-narrative
description: >
  Structures narrative for webtoons and manhwa — from concept through season arc,
  episode beat sheets, character arc mapping, and worldbuilding. Adapts Save the
  Cat methodology for episodic webtoon format. Genre-specific frameworks for
  Romance/Drama, Action/Fantasy, and Slice of Life/Comedy. Arc-level guidance is
  flexible; episode level is a strict beat template.
  Use automatically — do not wait to be asked. Trigger on ANY of these signals:
  user says "plot my comic", "structure a webtoon idea", "comic concept",
  "plan out my arc", "episode structure", "worldbuilding for my comic",
  "character arc", "season outline", "story beats", "Save the Cat"; user is
  brainstorming or developing a new comic series; user asks how to hook readers,
  plan cliffhangers, or develop a protagonist's arc. Load once per session.
  Do NOT trigger for: AI image generation, canvas specs, platform publishing,
  or production topics covered by comic-core-creator.
---
gates_passed: 2026-05-17
SKILL_VERSION: v1.0

# Comic Narrative Designer

Single-domain narrative design skill for webtoons and manhwa. Covers concept
development, arc design, episode beat sheets, pacing, worldbuilding, and
genre conventions.

Type: dispatcher

Canonical dispatcher reference: `persona-developer` — read before modifying
dispatcher body structure.

---

## GOTCHAS

1. **Starting at arc design before concept pressure test** — if want and need
   are the same, no internal arc exists and the series will feel flat. Always
   confirm the want/need gap before building structure.
2. **Treating episode beat sheet as optional** — at arc level the frameworks are
   flexible; at episode level the beat sheet is strict. Every episode requires
   every beat. Skipping the midpoint turn produces flat episodes.
3. **Late catalyst** — the Catalyst must land by episode 3 in webtoon format.
   Manhwa readers drop series that don't hook in episode 1 and haven't committed
   by episode 3. Any concept with setup past episode 3 needs restructuring.
4. **Macro and micro pacing conflated** — these are independent problems. A
   well-paced episode in a badly-paced season still fails. Always audit both
   separately when a pacing complaint is raised.
5. **Genre conventions as optional** — each genre has structural expectations
   that readers hold implicitly. Violating them must be intentional. Check Phase 5
   before finalizing any arc for Romance, Action, or SoL.

---

## PART 0 — CLASSIFY

Single-domain narrative skill. All triggers route to references/narrative.md.
Entry point selection determines the Phase — confirm which Phase the user needs
before loading and executing from the reference.

| Starting state | Entry Phase |
|---|---|
| Vague concept, no structure yet | Phase 1 — Concept Pressure Test |
| Concept confirmed, need arc | Phase 2 — Arc Design |
| Arc planned, need episode | Phase 3 — Episode Beat Sheet |
| Pacing problem identified | Phase 3.5 — Pacing Architecture |
| World needs developing | Phase 4 — Worldbuilding |
| Genre expectations unclear | Phase 5 — Genre Conventions |
| Series arc feels broken | Phase 6 — Anti-Patterns |

---

## PART 1 — REFERENCE LOAD

Reference files do not persist across turns — re-view each turn that uses them.

    view /mnt/skills/user/comic-extended-narrative/references/narrative.md

HARD FAIL: Proceed to PART 2 only after narrative.md is loaded and visible
in the current turn's output.

---

## PART 2 — INTAKE

Confirm entry point before generating any output:
- What does the user have already: concept, arc, episode, or nothing?
- Which Phase (1-6) addresses the immediate need?
- Genre (Romance/Drama, Action/Fantasy, Slice of Life) — affects Phase 5 conventions

One question at a time. Most requests imply the Phase directly.

---

## PART 3 — EXECUTE

Route to the appropriate Phase in the loaded reference. Apply the Phase strictly
(especially Phase 3 — episode beat sheet is a required template, not a guide).

HARD FAIL: Never skip the concept pressure test (Phase 1) when want and need
are unstated or unclear. Arc design built on a flat concept amplifies the
flatness — it does not fix it.

HARD FAIL: Always include the catalyst-timing check (Phase 2 critical rule)
when advising on season structure. Catalyst after episode 3 must be explicitly
flagged as requiring restructure.

---

## PART 4 — QUALITY CHECK

Before delivering any output:
- Want/need gap confirmed (Phase 1) before arc framework applied
- STC beat map adapted to actual episode count, not generic percentages
- Episode beat sheet complete with midpoint turn and hook defined
- Genre-specific conventions checked (Phase 5) for the relevant genre
- Anti-patterns (Phase 6) audited for any arc plan delivered

---

## OUT OF SCOPE

- AI image generation, canvas specs, export formats — comic-core-creator
- Platform publishing, upload requirements — comic-core-creator
- Prose fiction (non-comic) — frameworks apply but weren't designed for it
- Manga / print comic format — different pacing and structure conventions

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| comic-core-creator | Production pipeline, canvas specs, AI tools, platform publishing |
| Save the Cat! Writes a Novel — Jessica Brody | Best STC adaptation for non-screenplay media |
| Brandon Sanderson's worldbuilding lectures | Free on YouTube; magic system design |
