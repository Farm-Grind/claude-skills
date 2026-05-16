# Image Reference — Image Generation AI

## Contents
- § MODEL SELECTION TABLE
- § MIDJOURNEY V7
- § FLUX 2 / FLUX.1 (Black Forest Labs)
- § DALL-E 3
- § STABLE DIFFUSION (SD 3.5 / SDXL)
- § COMFYUI
- § IDEOGRAM 2
- § IMAGEN 3 (Google)
- § SEEDREAM / SEEDREAM 3
- § IMAGE EDITING / REFERENCE EDITING
- § COMMON FAILURE PATTERNS

---

## § MODEL SELECTION TABLE

| Goal | Best model | Notes |
|---|---|---|
| Photorealism, cinematic, natural language prompting | Flux 2 Pro / Flux 1.1 Pro | Leading 2026 photorealism tool |
| Artistic styles, creative interpretation, parameters control | Midjourney V7 | Best for webtoon, concept art, stylized work |
| Accurate text in image, precise prompt adherence | Ideogram 2 | Best text rendering of any image AI |
| Fast local/API generation with natural language | Flux.1 Dev or Schnell | Open-weight; Dev = quality, Schnell = speed |
| Commercial pipelines needing licensing clarity | Flux.1 Pro or DALL-E 3 | Both have clear commercial terms |
| Anime / manga character art | Midjourney Niji 7 or Leonardo Anime XL | See webtoon.md for panel workflow |
| Google ecosystem / Gemini integration | Imagen 3 / Nano Banana Pro | Pairs with Veo for image-to-video |
| Full workflow control, custom nodes, LoRA | ComfyUI | Node-based; not single-prompt |
| Consistent text in designed outputs | Ideogram 2 | Far ahead of other models on legible text |

---

## § MIDJOURNEY V7

**Current default: V7** (became default June 2025)

| Version | When |
|---|---|
| V7 (default) | All production work. Best quality, Omni Reference support. |
| V6 (`--v 6.0`) | When you need `--cref` (Character Reference) — V7 uses `--oref` only |
| Niji 7 (`--niji 7`) | Anime and manga aesthetic. Best for webtoon. |
| Draft mode (`--draft`) | Fast/cheap test runs. |

**Prompt structure:** Comma-separated descriptors, not prose sentences. Subject first, then style, mood, lighting, composition.

```
[subject], [action], [setting], [style], [mood], [lighting], [composition] --ar [ratio] --v 7
```

**Key parameters:**
- `--ar` — aspect ratio (9:16 vertical, 16:9 landscape, 1:1 square, 2:3 portrait)
- `--niji 7` — anime/manga aesthetic
- `--s [0-1000]` — stylize (250 = default; 750+ = very stylized)
- `--c [0-100]` — chaos/variation
- `--q 2` — higher quality (slower)
- `--no [terms]` — negative prompts

**Omni Reference V7 (`--oref`):** Replaces `--cref` in V7. Lock character appearance.
- `--ow 0-30`: light influence, mostly follows prompt
- `--ow 50-70`: balanced (face + general appearance) — good default
- `--ow 80-100`: strong adherence — may bleed reference's lighting/background

**Style Reference (`--sref`):**
- `--sw 100-200`: subtle influence
- `--sw 500`: moderate transfer
- `--sw 750-1000`: strong — image strongly resembles reference aesthetic
- `--sref random` to explore Midjourney's internal style library

**Common failures:**

| Problem | Fix |
|---|---|
| `--cref` not working | Switch to `--oref` in V7, or use `--v 6.0` for `--cref` |
| Style too close to reference | Lower `--sw` to 200-300 |
| Character ignoring prompt | Lower `--ow` to 40-60 |
| Text appears in image | Add `--no text`; rephrase prompt away from text-adjacent concepts |
| Establishing shot has unwanted characters | Add `--no people, characters, figures` |
| Anime style not triggering | Explicitly add `--niji 7` |

---

## § FLUX 2 / FLUX.1 (Black Forest Labs)

**Architecture:** Diffusion Transformer (DiT) with T5-XXL or VLM text encoder.
Understands natural language contextually — not keyword matching. Write clear,
descriptive prose for best results.

**Version guide:**

| Version | Use for |
|---|---|
| Flux 2 Pro | Best quality; natural language; 10 reference image support; up to 4MP |
| Flux.1 Pro | Commercial production; top quality |
| Flux.1 Dev | Open-weight; comparable quality to Pro; local deployment |
| Flux.1 Schnell | Speed (4 inference steps); local/API; slightly softer details |
| Flux.1 Kontext Pro | In-context image editing — modify specific elements while preserving the rest |

**Prompt syntax:**
- Write in natural language prose — NOT comma-separated tag lists
- Front-load the subject: Flux weights earlier tokens more heavily
- Structure: Subject → Action/Pose → Environment → Lighting → Camera/Style
- Target 30-80 words for standard prompts; up to 150 for complex scenes
- Do NOT use `(word:weight)` syntax from SD — not supported in Flux Dev/Schnell
- Do NOT use negative prompts for Flux via simple mode — use positive descriptions instead; Flux.1 Kontext and API support negative prompts

**Prompt structure example:**
```
[Subject with specific physical details], [action or pose], [environment and
setting details], [lighting description], [camera/lens specification],
[style or mood]
```

**Flux 2 multi-reference:** Use up to 10 reference images with @ notation or
ordinal indexing. Enables character consistency without ControlNet.

**Flux.1 Kontext (image editing):**
- Provide source image + edit instruction
- Describe ONLY what to change — model preserves context automatically
- Text editing: use quotes around text to change: `Replace "Open" with "Closed"`
- For dramatic changes: do in multiple steps rather than one large edit

**Key differences from Stable Diffusion:**
- No prompt weights `(word:weight)` — use emphasis phrases instead: "with emphasis on"
- No negative prompt list in basic mode — describe what you want, not what to avoid
- White background prompt can cause blurry output in Dev variant — avoid on Dev
- Prose beats tag lists — "a red barn at sunset" > "red, barn, sunset, golden hour"

---

## § DALL-E 3

- Prose description works well — DALL-E responds to natural language
- Add "do not include text in the image unless specified" — prevents unwanted text
- Describe foreground, midground, background separately for complex compositions
- Strong text rendering — good choice when legible text in image is needed (but Ideogram 2 is better)
- OpenAI's safety filters are conservative — rephrase rather than push limits
- For consistent character across generations: describe the character in detail every time (no reference system)

---

## § STABLE DIFFUSION (SD 3.5 / SDXL)

- Uses tag-list syntax with optional weights: `(keyword:weight)` where 1.0 is neutral
- Negative prompt is MANDATORY — specify what to exclude
- CFG scale 7-12 (lower = more creative, higher = more literal)
- Steps: 20-30 for drafts, 40-50 for finals
- SDXL works better with structured tag prompts than SD 1.5
- SD 3.5 supports more natural language than older versions but still benefits from tags
- Standard negative prompt: "blurry, low quality, watermark, bad anatomy, extra limbs, deformed, ugly, disfigured"
- LoRA and ControlNet require knowing which checkpoints/models are loaded

---

## § COMFYUI

Node-based workflow — not a single prompt box. Ask which checkpoint model
is loaded before writing. Always output two separate blocks: Positive Prompt
and Negative Prompt. Never merge them.

**Positive Prompt:**
Detailed description using the syntax of the loaded model (SD 1.5 style tags
vs SDXL natural language vs Flux natural language — depends on checkpoint)

**Negative Prompt:**
Always explicit. Standard: "blurry, bad anatomy, watermark, text, ugly, 
deformed, low resolution, artifacts"

**Key clarifying questions to ask user:**
1. Which checkpoint model?
2. Which sampling method (DPM++, Euler, DDIM)?
3. Is ControlNet or LoRA active, and which adapter/model?
4. Target resolution and aspect ratio?

---

## § IDEOGRAM 2

- Best-in-class for text rendering in images — use when legible text is required
- Accuracy on complex text layouts: ~92% — far ahead of other models
- Natural language prompt — describe scene, text to include in quotes: "a sign reading 'Open 24 Hours'"
- Supports style presets (design, illustration, realistic, anime, 3D render) — specify one
- Strong at logo, poster, and graphic design work
- Less strong than Flux/Midjourney for purely photorealistic or cinematic work without text

---

## § IMAGEN 3 (Google)

- Google's flagship image model; available via Gemini and Vertex AI (as "Nano Banana Pro" in Google Flow)
- Strong photorealism; pairs naturally with Veo 3.1 for image-to-video workflows
- Natural language prompting — no special syntax
- Best paired with Google ecosystem tools when output feeds into Veo
- "Nano Banana Pro" is the branding in Google's creative apps (Flow, Gemini)

---

## § SEEDREAM / SEEDREAM 3

- Strong at artistic and stylized generation
- Specify art style explicitly (anime, cinematic, painterly) before scene content
- Mood and atmosphere descriptors work well
- Negative prompt recommended
- Available via several third-party platforms and Artlist

---

## § IMAGE EDITING / REFERENCE EDITING

Activate when: user mentions "change", "edit", "modify", "adjust" anything in an
existing image, or uploads a reference image.

**Always instruct user:** attach the reference image to the tool first.
Build the prompt around the delta ONLY — what changes, what stays the same.

**Flux.1 Kontext** is currently the best option for reference editing:
- Single reference image: describe only the change
- Style transfer: "Using this style, [new scene description]"
- Character consistency editing: establish reference once, then make targeted edits step by step

**Other tools:**
- DALL-E 3: inpainting via ChatGPT — describe the masked region precisely
- Midjourney: image variation with `--v 7` and optional `--oref`; no direct edit mode
- ComfyUI with img2img: set denoise strength (0.1-0.3 for subtle changes, 0.5-0.7 for major)

---

## § COMMON FAILURE PATTERNS

| Problem | Cause | Fix |
|---|---|---|
| Wrong syntax for tool | Flux tag-list prompts, MJ prose sentences | Match prompt syntax to model architecture |
| Negative prompt list in Flux Dev | Unsupported | Use positive descriptions; switch to Kontext for editing |
| `--cref` error in MJ V7 | V7 uses `--oref` | Switch to `--oref` or specify `--v 6.0` |
| Generic/flat output | Too short or too vague | For Flux: 40-80 words; for MJ: add style and mood descriptors |
| Text in Midjourney image | Default behavior | Add `--no text` to every MJ prompt |
| Hand deformities | Common in all models | Inpaint hands separately; Flux handles better than older models |
| Characters in background shots | MJ adds figures by default | `--no people, characters, figures` |
