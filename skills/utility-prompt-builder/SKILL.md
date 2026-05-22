---
name: utility-prompt-builder
description: >
  Generates optimized prompts for any AI tool. Dispatcher across 11 domains:
  LLM text/chat models, coding agents, image generation, music, video, 3D AI,
  voice synthesis, workflow automation, research AI, browser agents, and webtoon
  stack. Use automatically — do not wait to be asked. Trigger on ANY of these
  signals: user says "write a prompt", "prompt for", "generate in [tool]",
  "optimize this prompt", "fix this prompt", "prompt for [Midjourney / Suno /
  Udio / Claude / Cursor / ElevenLabs / Veo / Flux / Runway / Kling / Dashtoon
  / Leonardo / any AI tool]"; user provides a rough idea and names a target
  tool; user pastes a bad prompt to fix; user asks how to prompt any AI tool.
  Do NOT trigger for: coding tasks with no prompt output, lore or GDD content
  with no prompt output, purchase decisions (use life-core-shopping), or
  research synthesis with no prompt output (use utility-data-analyst). Load
  once per session.
---
gates_passed: 2026-05-22
SKILL_VERSION: v1.3

# Utility Prompt Builder — Dispatcher

Generates production-ready prompts for any AI tool. Routes by domain code,
loads the matching reference file, and synthesizes tool-specific output.

Type: dispatcher

---

## GOTCHAS

1. **Stale domain knowledge without reference load** — body contains zero
   domain expertise. Every domain rule lives in a reference file. Generating
   from memory without loading the reference = silent degradation, no error.
   HARD FAIL: no domain expertise output without a visible view call first.
2. **Routing to wrong domain from tool name alone** — some tools span domains
   (Leonardo is IMAGE in general but WEBTOON in the component stack workflow).
   Intake classification uses BOTH tool name AND stated context.
3. **Dispatcher without synthesis** — multi-domain prompts (e.g., a Suno track
   for a game scene) require cross-domain integration, not concatenated
   per-domain sections. Synthesis protocol is mandatory before output.
4. **Treating Flux like Stable Diffusion** — completely different prompt
   syntax. Flux uses natural language prose; SD uses weighted tag lists. Wrong
   syntax = wrong output. IMAGE reference file covers the distinction.
5. **Suno version mismatch** — suno-prompter was written for v5. Current
   platform is v5.5. Music reference file contains current rules.
6. **Video model currency** — video AI landscape changed significantly in 2026.
   Veo 3.1 is now leading. Sora web is discontinued (API continues). Runway
   is Gen-4 not Gen-3. Always load VIDEO reference before building video
   prompts — never from memory.
7. **Brain dump routed to domain without extraction** — a multi-goal brain dump
   contains several tasks that need sequencing. Routing it directly to a domain
   file skips intent extraction and produces a prompt for only the first goal.
   Brain Dump Mode in core-methodology.md runs first; domain reference loads
   after.
8. **Claude 4.x literal behavior ignored** — Claude 4.x does not infer scope or
   fill gaps. Prompts that rely on Claude to "figure out the obvious next step"
   produce partial output. LLM reference file carries this warning; it only
   applies if the reference file is loaded.

---

## INTAKE CLASSIFICATION

Classify the request before loading any reference file. One or more domain
codes may activate for a single request.

| Signal | Domain Code(s) |
|---|---|
| Target is a text/chat model (Claude, ChatGPT, GPT-5, o3, Gemini, Qwen, DeepSeek, Llama, Mistral, MiniMax, Ollama) | LLM |
| Target is a coding agent or IDE (Claude Code, Cursor, Windsurf, Copilot, Bolt, v0, Lovable, Figma Make, Google Stitch, Devin, Antigravity, SWE-agent) | CODE |
| Target is an image generator (Midjourney, DALL-E 3, Stable Diffusion, Flux, ComfyUI, Leonardo, Ideogram, Imagen, SeeDream, or any image AI) NOT in webtoon context | IMAGE |
| Target is a music generator (Suno, Udio, AIVA, Mubert) | MUSIC |
| Target is Suno AND working on The Loop project (explicit project context or Loop track family named) | MUSIC + LOOP — load both music.md AND music-loop.md |
| Target is a video generator (Veo, Runway, Kling, Sora, LTX Video, Dream Machine, Luma, Seedance, Pika, Hailuo) | VIDEO |
| Target is a 3D AI tool (Meshy, Tripo, Rodin, Unity AI, Blender AI add-ons) | 3D |
| Target is a voice synthesis tool (ElevenLabs) | VOICE |
| Target is a workflow/automation tool (Zapier, Make, n8n) | WORKFLOW |
| Target is a research or orchestration AI (Perplexity, Manus, Deep Research) | RESEARCH |
| Target is a browser or computer agent (Claude in Chrome, OpenAI Atlas, Comet, OpenClaw, Perplexity Computer) | BROWSER |
| Target is Dashtoon, OR user is building character-consistent webtoon panel art with Leonardo OR Midjourney in a serialized production context | WEBTOON |
| Request involves an existing prompt the user wants fixed, adapted, or decompiled | Load core-methodology.md Prompt Decompiler section |
| User says "brain dump", "here's what I want to do", voice-input with multiple goals, or asks to translate an idea into a Claude prompt | Load core-methodology.md Brain Dump Mode — run BEFORE loading any domain reference |
| Request involves a tool not listed above | LLM as closest fallback; confirm tool before generating |

**Multi-domain flag:** Activate multiple codes when: (a) the target tool appears
in multiple domains (Leonardo in IMAGE and WEBTOON), (b) the prompt must bridge
domains (music prompt for a game scene — MUSIC + project context), (c) user
asks to compare or adapt across tools.

**Ask if genuinely ambiguous:** "Which tool is this for?" — one question,
before generating. Count toward the 3-question limit in core-methodology.md.

---

## DOMAIN DECLARATION

After classification and before loading reference files, output this block
(visible, not internal):

```
DOMAINS ACTIVATED: [code list, e.g., IMAGE | WEBTOON]
Reference files loading: [filenames]
```

---

## REFERENCE FILE LOAD INSTRUCTIONS

HARD FAIL: Do not generate any domain-specific content before the
corresponding reference file has been loaded via a view tool call.

| Domain Code | Reference File | Load when |
|---|---|---|
| LLM | references/llm.md | LLM activated |
| CODE | references/code.md | CODE activated |
| IMAGE | references/image.md | IMAGE activated |
| MUSIC | references/music.md | MUSIC activated |
| MUSIC + The Loop | references/music.md AND references/music-loop.md | MUSIC activated AND Loop project context present |
| VIDEO | references/video.md | VIDEO activated |
| 3D | references/3d.md | 3D activated |
| VOICE | references/voice.md | VOICE activated |
| WORKFLOW | references/workflow.md | WORKFLOW activated |
| RESEARCH | references/research.md | RESEARCH activated |
| BROWSER | references/browser.md | BROWSER activated |
| WEBTOON | references/webtoon.md | WEBTOON activated |
| Always | references/core-methodology.md | Every request — load first |

Load `references/core-methodology.md` on every request before domain files.
For multi-domain requests, load all activated domain files before generating.

---

## SYNTHESIS PROTOCOL

Applies when two or more domain codes are active.

1. Load `references/cross-domain-map.md` and identify any named conflicts or
   interaction points between the activated domains.
2. Run core-methodology intent extraction (from core-methodology.md) once
   across all activated domains — do not run it per-domain.
3. Apply each domain's rules to the relevant part of the output. Where rules
   conflict, the cross-domain map defines precedence.
4. Produce a single integrated prompt output — not separate per-domain
   sections. Domain headers (MUSIC FINDINGS: ...) are a HARD FAIL.
5. If domain rules genuinely cannot be reconciled, present the tradeoff and
   ask which takes precedence. One question.

---

## META-ADVERSARIAL REVIEW

Run before delivering any prompt output.

1. **Tool currency check** — is the target tool or model version current?
   Fast-moving domains (VIDEO, IMAGE, MUSIC) are highest risk. If generating
   from a reference file with a version note older than 6 months, flag it.
2. **Syntax match check** — does the generated prompt use the syntax the
   target model actually accepts? (prose vs. tags vs. parameters vs. dual-field)
3. **Critical-first check** — are the most important constraints in the first
   30% of the generated prompt? Attention decay applies across all models.
4. **Fabrication technique check** — no techniques that cannot execute in a
   single prompt pass. See core-methodology.md hard rules list.
5. **Cross-domain coherence** (multi-domain only) — does the output read as
   integrated direction, or as concatenated per-domain sections? Any domain
   header is a failure.

---

## OUTPUT FORMAT

Defined in core-methodology.md. Short form:
1. Copyable prompt block, fenced, ready to paste
2. `🎯 Target: [tool] — [one sentence: what was optimized and why]`
3. Setup note if needed (1-2 lines, only when genuinely required)

Webtoon pre-production artifacts: defined in webtoon.md. Full artifact set
before runtime panel prompts.

---

## Examples

- "Okay so basically I want to create a new skill using skill-publisher, and I
  need to first run data-analyst to validate it, and also review the last 60
  days of conversations, oh and I need confirmation before building" → DOMAINS
  ACTIVATED: LLM. Load core-methodology.md Brain Dump Mode FIRST. Extract 3
  tasks: (1) conversation review, (2) data-analyst validation, (3) skill
  creation with confirmation gate. Sequence by dependency. Then build structured
  Claude prompt with explicit task order and confirmation checkpoint.

- "Write a Claude Code prompt to refactor my auth module" → DOMAINS ACTIVATED:
  CODE. Load core-methodology.md, references/code.md. Apply Claude Code rules
  from code.md. Output fenced prompt block.

- "Generate a Suno prompt for the ritual waltz" → DOMAINS ACTIVATED: MUSIC.
  Load core-methodology.md, references/music.md. Check Loop project flag in
  music.md. Apply Suno dual-block rules. Output STYLE FIELD + LYRICS FIELD.

- "Prompt for my webtoon protagonist's confrontation panel in Dashtoon" →
  DOMAINS ACTIVATED: WEBTOON. Load core-methodology.md, references/webtoon.md.
  Check Character DNA exists before panel prompt. Output panel prompt with
  settings block.

- "Fix this Midjourney prompt — it keeps making the background wrong" →
  DOMAINS ACTIVATED: IMAGE. Load core-methodology.md, references/image.md.
  Run Prompt Decompiler from core-methodology.md. Apply MJ failure mode table
  from image.md.

- "I need a Veo 3 prompt for the intro sequence of my game" → DOMAINS
  ACTIVATED: VIDEO. Check tool version — Veo 3.1 current. Load
  core-methodology.md, references/video.md. Apply Veo 3.1 formula (shot
  composition + subject + action + setting + aesthetics/mood + audio).

- "Write me a Cursor prompt and a Midjourney prompt for this feature" → DOMAINS
  ACTIVATED: CODE | IMAGE. Load core-methodology.md, references/code.md,
  references/image.md, references/cross-domain-map.md. Run core intent
  extraction once. Build separate fenced blocks per tool — these are two
  independent prompts, not a merged output. Cross-domain map confirms no
  synthesis conflict.

---

## Out of Scope

This skill does NOT:
- Generate GDD sections, design docs, or lore — use the project's design skills
- Conduct research synthesis — use utility-data-analyst
- Recommend products for purchase — use life-core-shopping
- Manage The Loop sound-design document — use loop-core-tracker
- Log Suno prompt results for The Loop — use suno-prompter (until retired)

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| references/core-methodology.md | Intent extraction, diagnostic checklist, safe techniques, memory block, decompiler |
| references/llm.md | Claude, ChatGPT, GPT-5, o3, Gemini, Qwen, DeepSeek, Llama, Mistral, MiniMax |
| references/code.md | Claude Code, Cursor/Windsurf, Copilot, Bolt/v0/Lovable, Devin, Antigravity |
| references/image.md | Midjourney V7, DALL-E 3, Flux 2, Stable Diffusion, ComfyUI, Ideogram 2, Imagen 3 |
| references/music.md | Suno v5.5, Udio v1.5 — generic rules, intent extraction, failure modes |
| references/music-loop.md | Suno for The Loop — base template, ritual waltz example, prompt-result log |
| references/video.md | Veo 3.1, Runway Gen-4, Kling 3.0, Sora 2, LTX Video, Dream Machine |
| references/3d.md | Meshy, Tripo, Rodin, Unity AI, Blender AI |
| references/voice.md | ElevenLabs |
| references/workflow.md | Zapier, Make, n8n |
| references/research.md | Perplexity, Manus, Deep Research |
| references/browser.md | Claude in Chrome, OpenAI Atlas, Comet, Perplexity Computer |
| references/webtoon.md | Dashtoon, Leonardo (webtoon panels), Midjourney (webtoon backgrounds) |
| references/cross-domain-map.md | Multi-domain conflict map |

Reference files do not persist across turns — re-view each turn that uses them.
| utility-skill-builder | Quality gate for this skill's creation and updates |
| utility-data-analyst | Research and synthesis (feeds this skill's reference files) |
