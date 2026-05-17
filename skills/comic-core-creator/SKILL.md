---
name: comic-core-creator
description: >
  Guides creation of vertical-scroll webtoons and manhwa-style webcomics — from
  concept through AI-assisted production to platform publishing. Covers series
  bible, character sheets, episode scripts, scroll pacing, AI tool selection for
  character consistency, canvas specs, and platform submission requirements.
  Use automatically — do not wait to be asked. Trigger on ANY of these signals:
  user says "webtoon", "manhwa", "webcomic", "vertical scroll comic"; user asks
  to "create a comic series", "write a comic script", "design a character sheet
  for a comic", "publish on WEBTOON", "publish on Tapas", "panel layout"; user
  mentions episode-based comics, "character consistency" for AI-generated comics,
  canvas size, or episode formatting. Load once per session.
  Do NOT trigger for: manga (Japanese print format), traditional print comics,
  graphic novels with page-turn format, or general AI image generation unrelated
  to comics.
---
gates_passed: 2026-05-17
SKILL_VERSION: v1.0

# Webtoon / Manhwa Creator

Single-domain skill covering the full vertical-scroll webtoon production
pipeline: pre-production, scripting, scroll design, canvas specs, AI tools,
and platform publishing.

Type: dispatcher

Canonical dispatcher reference: `persona-developer` — read before modifying
dispatcher body structure.

---

## GOTCHAS

1. **Jumping to AI tools before pre-production** — skipping the series bible
   and character sheets produces inconsistent characters with no fix path. Phase 1
   documents must exist before Phase 5 tools are recommended.
2. **Recommending an AI tool before asking overhead and distribution questions**
   — the three paths (Integrated / Component Stack / Full Control) have completely
   different ramp-up costs. Always run Phase 5 Step 1 questions before naming a tool.
3. **Dashtoon exclusive contract warning** — always state the self-publish vs.
   exclusive contract distinction before any Dashtoon recommendation. Never
   present the integrated platform without the IP warning.
4. **Drawing at export resolution** — 800px working canvas degrades art. Always
   prescribe 1,600px working canvas and 800px export. Stale memory from non-webtoon
   workflows will produce the wrong advice here.
5. **Treating manhwa/webtoon as interchangeable with manga** — left-to-right
   reading, full color, and K-drama pacing conventions are manhwa-specific. Manga
   conventions (right-to-left, grayscale, panel layout norms) do not apply here.

---

## PART 0 — CLASSIFY

Single-domain webtoon production skill. All triggers route to
references/creator.md. Phase selection determines the relevant section —
always load the reference before recommending any specific phase output.

---

## PART 1 — REFERENCE LOAD

Reference files do not persist across turns — re-view each turn that uses them.

    view /mnt/skills/user/comic-core-creator/references/creator.md

HARD FAIL: Proceed to PART 2 only after creator.md is loaded and visible
in the current turn's output.

---

## PART 2 — INTAKE

Establish the current production stage before generating any output:
- New series from scratch, or continuing series already in production?
- Which Phase (1-7) is the immediate need?
- If AI tool selection (Phase 5): technical overhead tolerance and distribution intent

One question at a time if genuinely blocked. Most requests imply the phase directly.

---

## PART 3 — EXECUTE

Route to the appropriate Phase in the loaded reference:

| Signal | Reference section |
|---|---|
| New series, no documents yet | Phase 1 — pre-production documents |
| Writing or reviewing episode script | Phase 2 — script format |
| Scroll layout, panel composition, pacing | Phase 3 — scroll design |
| Canvas size, DPI, export workflow | Phase 4 — canvas specs |
| AI tool selection or character consistency | Phase 5 — AI tools |
| Platform upload, rights, publishing strategy | Phase 6 — platform publishing |
| Pre-launch checklist or buffer plan | Phase 7 — project plan |
| Storytelling conventions or genre tropes | Manhwa conventions section |
| Producing a series bible / character sheet / etc. | Output Formats section |

HARD FAIL: Never recommend an AI tool (Phase 5) without first running the
two Step 1 questions (overhead tolerance + distribution intent) from the
loaded reference.

---

## PART 4 — QUALITY CHECK

Before delivering any output:
- Phase 1 documents confirmed before any Phase 5 AI tool recommendation
- Dashtoon self-publish vs. exclusive contract warning included if Dashtoon mentioned
- Canvas width prescribed as 1,600px working / 800px export — never 800px working
- Rights caution included in any platform publishing discussion
- Manhwa conventions (L-to-R, full color, cliffhanger requirement) applied
  for any genre/storytelling guidance

---

## OUT OF SCOPE

- Manga (Japanese, right-to-left, print format) — different conventions
- Traditional print comics and graphic novels — different format requirements
- General AI image generation with no comic application
- Video and motion comics
- Narrative structure and arc planning — comic-extended-narrative

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| comic-extended-narrative | Narrative design — series structure, episode beats, worldbuilding |
| frontend-design | Web reader or series landing page |
| docx | Pre-production documents as Word files |
| WEBTOON Creator Guide | https://www.webtoons.com/en/creator-guide |
| Clip Studio Paint webtoon guides | https://tips.clip-studio.com |
