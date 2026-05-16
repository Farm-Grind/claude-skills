# Cross-Domain Map

Adjacent domain pairs and their named interaction points, conflicts, and
precedence rules. Load this file whenever two or more domain codes are active.

---

## IMAGE + WEBTOON

**Interaction:** Midjourney and Leonardo appear in both IMAGE and WEBTOON
domains but with different purposes and output formats.

| Scenario | Active domain | Rules |
|---|---|---|
| Midjourney for standalone art, concept art, general use | IMAGE | Use image.md Midjourney rules; no webtoon-specific format |
| Midjourney for webtoon episode panel or background | WEBTOON | Use webtoon.md Midjourney section; apply webtoon aspect ratios and style vocabulary |
| Leonardo for general image generation | IMAGE | Use image.md Leonardo section |
| Leonardo for character-consistent webtoon panel (named character, serialized) | WEBTOON | Use webtoon.md Leonardo section; Character Reference and Character DNA required |

**Precedence:** When the user explicitly names a webtoon or serialized production context, WEBTOON rules override IMAGE rules for that tool.

---

## MUSIC + PROJECT CONTEXT (The Loop)

**Interaction:** The Loop project has a locked sound-design document with
master templates that override the base music.md rules.

**Precedence:** Loop project active → load sound-design document first. music.md rules
apply for general prompting only (non-Loop Suno and Udio).

---

## CODE + LLM

**Interaction:** Claude Code, Cursor, and other coding agents accept prompts
written for an LLM but need additional agentic structure.

**Precedence:** When the target is a coding agent (Claude Code, Cursor, Devin),
CODE rules take precedence. Add agentic elements even if the model is a standard LLM.
LLM rules apply for the text model's behavior but CODE rules govern the prompt structure.

---

## VIDEO + IMAGE (image-to-video workflows)

**Interaction:** Veo 3.1, Kling, and Dream Machine all accept reference images.
Generating the source image first (with IMAGE domain rules) then feeding into
video is a common workflow.

**Synthesis:** Build the image prompt using IMAGE domain rules (Flux for
photorealism, Imagen 3 for Veo workflows). Then build the video prompt using
VIDEO domain rules. Note that Imagen 3 / Nano Banana Pro is Google's preferred
image model to feed Veo — specify this pairing when relevant.

---

## CODE + MULTIPLE TOOLS (multi-tool session)

**Interaction:** User requests a coding prompt AND a separate prompt for
another tool in the same session (e.g., "Write a Cursor prompt and a
Midjourney prompt for this feature").

**Synthesis:** These are two independent prompts, not a merged output. Run
core-methodology intent extraction once. Produce separate fenced blocks per
tool. Label each clearly. No single merged prompt.

---

## RESEARCH + ANY DOMAIN

**Interaction:** Research AI (Perplexity, Manus) is used to gather information
that then feeds into another domain's prompt (e.g., research a topic then
write a Suno track about it).

**Synthesis:** Build the research prompt using RESEARCH rules. Then build the
creative prompt using the creative domain's rules, incorporating the research
deliverable as context. Sequence: research prompt first, then creative prompt.

---

## VOICE + VIDEO

**Interaction:** ElevenLabs voice output is sometimes combined with AI video
(Veo 3.1 with dialogue, HeyGen avatars, etc.).

**Synthesis:** Write voice prompts (VOICE domain) and video prompts (VIDEO
domain) as separate outputs. Note where the voice output feeds the video workflow.

---

## WEBTOON + MUSIC

**Interaction:** Score composition for webtoon episodes (MUSIC) alongside
visual production (WEBTOON) — primarily for digital webtoon with embedded audio.

**Synthesis:** Run WEBTOON and MUSIC domains independently (no technical
conflict). Note the scene/chapter context from WEBTOON output when building
the MUSIC prompt. The music should reflect the emotional beat from the
WEBTOON emotional translation table.
