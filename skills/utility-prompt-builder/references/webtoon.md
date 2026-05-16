# Webtoon Reference — Webtoon Production Stack

## Contents
- § TOOL ROLES IN THE WEBTOON STACK
- § PRE-PRODUCTION ARTIFACTS (Dashtoon)
- § DASHTOON GENERATION MODES
- § DASHTOON PANEL SEQUENCING
- § LEONARDO AI — CHARACTER PANELS
- § MIDJOURNEY — ENVIRONMENTS AND BACKGROUNDS
- § NEGATIVE PROMPTS
- § EMOTIONAL BEAT → VISUAL TRANSLATION
- § OUTPUT FORMATS
- § COMMON FAILURES

---

## § TOOL ROLES IN THE WEBTOON STACK

| Use for | Tool |
|---|---|
| Full episode generation, Story-to-Comic workflow | Dashtoon Studio |
| Character-consistent panels (dialogue, emotion) | Leonardo AI (Anime XL or Lucid Origin) |
| Establishing shots, environments, concept art, cover art | Midjourney V7 / Niji 7 |
| Pre-production artifacts (Character DNA, training briefs) | Dashtoon + Claude (this skill) |
| Inpainting panel fixes | Dashtoon Editor / Leonardo Canvas |
| Key art, hero panels, covers with highest quality | Midjourney V7 + Omni Reference |

---

## § PRE-PRODUCTION ARTIFACTS (Dashtoon)

Five artifacts required before generating any panel. Establish all before
opening Dashtoon Studio.

### Artifact 1 — Character DNA Document [Claude produces]

Canonical verbatim prompt text. Copy-paste into every panel prompt — never paraphrase.

```
CHARACTER DNA — [SERIES TITLE]
Generated: [episode / version]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[CHARACTER NAME]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERBATIM PROMPT BLOCK:
[age/gender], [build], [hair: color + length + style], [eyes: color + shape],
[skin], [signature outfit: every piece + colors]

DISTINGUISHING MARKS: [scars, tattoos, accessories]

DO NOT SUBSTITUTE: [exact terms that must appear verbatim — e.g. "blunt bangs" → never "fringe"]

OUTFIT VARIANTS:
  Variant A — [name]: [complete outfit description]
  Variant B — [name]: [complete outfit description]
```

Produce one block per named character. Never edit mid-episode.

### Artifact 2 — Character Model Training Brief [Claude produces → you execute]

```
CHARACTER MODEL TRAINING BRIEF — [CHARACTER NAME]

TRAINING IMAGE REQUIREMENTS:
- Count: 10–15 images minimum
- Poses required: front-facing, 3/4 view, profile, full body, close-up face
- Expression range: neutral, happy, angry, sad, determined
- Single character per image; consistent art style; soft diffuse lighting
- IMAGE LABEL format: [name], [build], [hair], [eyes], [skin], [outfit]

TRAINING STEPS IN DASHTOON STUDIO:
1. Generate or source reference images
2. Open dashtoon.com/studio → create or open project
3. Generate one image, right-click → "Create Character"
4. Input: Name, personality summary, physical description
5. Upload reference image set
6. Click "Train Character" (minutes to hours)
7. Free plan: 1 character/day; premium: up to 5/day

OUTFIT VARIANTS: Train on primary outfit only. Use DashTailor for alternates.
QUALITY CHECK: Generate test with verbatim DNA prompt. Verify face, hair, outfit. If unstable: add 5 more focused reference images and retrain.
```

### Artifact 3 — Outfit/Prop Reference Brief [Claude produces → you execute]
Required when character wears non-primary costume or uses a signature prop.
DashTailor is in the Editor section of any Dashtoon Studio project.
Reference image must match the target panel's art style.
Run a final inpaint pass at 0.15 denoise after DashTailor transfer.

### Artifact 4 — Style Anchor Record [Claude produces → you execute]
Produced after episode 1. The first episode's best panel is used as Style Reference for all future sessions.
Update only at season breaks. Version the file before replacing.

### Artifact 5 — Story-Mode Script [Claude produces]
Prose-formatted episode input for Dashtoon Story-to-Comic mode.
Character names must exactly match trained model names — Dashtoon maps by name.
One blank line between scenes signals a scene change.

---

## § DASHTOON GENERATION MODES

### Mode A: Text-to-Image

Standard mode. Use for most panel generation.

```
PANEL [N] PROMPT:
[CHARACTER DNA verbatim] [action/pose] [shot type] [setting] [lighting] [mood] [art style]
CAPTION PLACEMENT: [position, or NONE]
SPEECH BUBBLE: [position, direction, text, or NONE]
```

### Mode B: Story-to-Comic

Prose input. Dashtoon auto-generates panel screenplay.

```
[CHARACTER NAME] [action, setting, tone]
TONE: [tense / romantic / comedic]
```

Verify character name mapping before generating — AI matches names to models.

### Mode C: Storyboard2Comic

Draw rough stick-figure layouts first, then annotate:

```
Panel [N] storyboard notes:
- Layout: [panel shape and composition]
- Characters: [who, where, rough pose]
- Camera: [shot type]
- Key visual: [what the panel must communicate]
- Inpaint prompt (if needed): [what to refine after generation]
```

### Mode D: Inpainting

Fix specific elements without regenerating the whole panel.

- Describe ONLY the masked region, not the whole panel
- Include character DNA for any character in the masked area
- Denoise 0.15-0.2 for minor fixes; 0.4-0.6 for significant changes
- Final inpaint pass at 0.15 to eliminate artifacts and enforce style

---

## § DASHTOON PANEL SEQUENCING

1. Establishing panel first — locks environment and lighting
2. Use establishing shot as Style Reference for all subsequent panels in same scene
3. Character panels — use locked DNA verbatim
4. Reaction panels — DNA + emotion + lighting. Omit outfit if not in frame.
5. Anti-drift: every 5 panels in same scene, regenerate once with establishing shot as reference

---

## § LEONARDO AI — CHARACTER PANELS

**Model selection:**

| Goal | Model |
|---|---|
| Anime / manhwa | Leonardo Anime XL |
| Versatile manhwa + natural language | Lucid Origin |
| High fidelity, text adherence | Phoenix (FLUX-based) |
| Photorealistic | Leonardo Vision XL + PhotoReal v2 |
| Fast drafts | Lightning XL |

**Prompt structure:**
```
[STYLE TAG] [CHARACTER DNA] [ACTION/POSE] [SHOT TYPE] [SETTING] [LIGHTING] [MOOD] [QUALITY BOOSTERS]
```

Quality boosters: "highly detailed, sharp focus, professional illustration, high resolution"

**Character Reference settings:**
- Low: face only — action panels
- Medium: face + hair — dialogue and emotion panels (default)
- High: face + hair + clothing — when in standard outfit and full consistency needed

**Settings:**
- Guidance Scale: 7-9 (7 = creative; 9 = strict adherence)
- Steps: 20 for drafts, 40 for finals
- Aspect Ratio: 9:16 (vertical) or 2:3
- Alchemy: ON for finals

**Draft → final workflow:**
1. 4 images at guidance 7, no Alchemy, Anime XL or Lightning XL
2. Select best candidate
3. Lock seed, switch to Anime XL or Phoenix, enable Alchemy, guidance 8-9
4. Generate 2 finals

**Output format:**
```
PANEL [N] — LEONARDO AI

POSITIVE PROMPT:
[full prompt]

NEGATIVE PROMPT:
[negative block]

SETTINGS:
Model: [specified]
Guidance Scale: [7-9]
Aspect Ratio: [specified]
Character Reference: [image + strength, or NONE]
Style Reference: [source + strength, or NONE]
Seed: [locked / generate new]
Alchemy: [ON/OFF]
```

---

## § MIDJOURNEY — ENVIRONMENTS AND BACKGROUNDS

For establishing shots and environments. See image.md for full Midjourney rules.

**Webtoon-specific aspect ratios:**
- `--ar 9:16` → vertical scroll panel
- `--ar 16:9` → wide establishing shot
- `--ar 2:3` → portrait panels

**Style vocabulary for webtoon environments:**
- `manhwa style, clean line art, full color, vertical composition`
- `webtoon background, detailed environment, warm atmospheric lighting`
- `anime background, painterly style, Studio Ghibli-inspired`

**Establishing shot template:**
```
[location type], [time of day], [weather/atmosphere], [architectural details],
[mood descriptors], [art style], [color palette] --ar 16:9 --niji 7 --s 300
```

**Always add:** `--no people, characters, figures` for environment-only shots.

**Output format:**
```
PANEL [N] / [USE CASE] — MIDJOURNEY

PROMPT:
/imagine [full prompt] [--parameters]

NEGATIVE:
--no [terms]

VERSION: [V7 / V6 / Niji 7]
REFERENCE: --oref [URL] --ow [value] (if applicable)
STYLE REF: --sref [URL or code] --sw [value] (if applicable)
NOTES: [series continuity or follow-up actions]
```

---

## § NEGATIVE PROMPTS

**Dashtoon standard:**
```
blurry, low quality, watermark, text in image, extra fingers, deformed hands,
bad anatomy, distorted face, duplicate character, mismatched eye color, wrong
hair color, inconsistent art style, realistic photo, 3D render, extra limbs
```

**Leonardo standard:**
```
blurry, low quality, watermark, text in image, extra fingers, bad hands,
deformed anatomy, distorted face, extra limbs, duplicate, monochrome,
grayscale, realistic photo, 3D render, inconsistent style
```

**Midjourney standard:** `--no text, watermark, speech bubbles, bad anatomy, extra limbs, blurry`

---

## § EMOTIONAL BEAT → VISUAL TRANSLATION

| Beat | Shot + Composition + Lighting |
|---|---|
| Tension / confrontation | Medium shot, harsh side light, low angle |
| Vulnerability / confession | Close-up, soft front light, slight high angle |
| Revelation / shock | Extreme close-up (eyes) OR wide pull-back |
| Joy / relief | Medium-wide, warm golden light, open composition |
| Grief / loss | Close-up, dim cool light, character small in frame |
| Determination | Low angle, rim light, strong vertical composition |
| Quiet intimacy | Medium two-shot, soft warm light |
| Rage | Close-up, harsh under-lighting, tilted frame |
| Wonder | Wide establishing, golden hour or cool blue, figure small |

---

## § COMMON FAILURES

| Problem | Cause | Fix |
|---|---|---|
| Character looks different every panel | No DNA lock | Use verbatim Character DNA in every panel prompt |
| Wrong model activates | Name mismatch in Dashtoon | Verify trained model name exactly matches name in script |
| Style drifts mid-episode | No Style Anchor Reference | Lock Style Anchor after episode 1; re-anchor every 5 panels |
| Bad hands in close-up | Common AI issue | Inpaint hands separately; add "correct anatomy, 5 fingers" to mask description |
| Character ignores prompt in MJ V7 | `--cref` doesn't work in V7 | Use `--oref`; or switch to `--v 6.0` |
