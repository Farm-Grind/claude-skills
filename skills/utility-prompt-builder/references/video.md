# Video Reference — AI Video Generation

## Contents
- § MODEL SELECTION TABLE
- § VEO 3.1 (Google)
- § RUNWAY GEN-4
- § KLING 3.0
- § SORA 2 (OpenAI)
- § LTX VIDEO
- § DREAM MACHINE (Luma)
- § SEEDANCE 2.0
- § GENERAL VIDEO PROMPTING PRINCIPLES
- § COMMON FAILURES

---

## § MODEL SELECTION TABLE (2026)

| Goal | Best model |
|---|---|
| Best overall quality, cinematic, synchronized audio | Veo 3.1 (Google) |
| Realistic human motion, start-and-end-frame control | Kling 3.0 |
| Artistic / experimental, short social clips | Runway Gen-4 |
| Human emotion, breakdancing, unusual motion | Sora 2 |
| Fast generation for iteration | Seedance 2.0 |
| B-roll, cinematic, keyframe transitions | Dream Machine (Luma) |
| Prompt-sensitive, fast social content | LTX Video |
| Multi-shot narrative sequences | Kling O3 (multishot mode) |

**2026 context:** Veo 3.1 is the current leading all-arounder. Sora web/app discontinued
April 2026 (API continues as Sora 2). Runway is Gen-4. Kling is at 3.0 with Kling O3
introducing multishot. Seedance 2.0 (ByteDance, Feb 2026) is fastest. Pika 3.0 is
available for social creators.

---

## § VEO 3.1 (Google)

**Access:** Google Flow app, Gemini (Veo 3 Lite), Vertex AI API

**Prompt formula (5-part):**
```
[Shot Composition] + [Subject Details] + [Action] + [Setting/Environment] + [Aesthetics/Mood + Audio]
```

Optimal prompt length: 3-6 sentences, 100-150 words. Too short = generic; too long = confused.

**Subject definition (lock early):**
Front-load subject identity. Include: clear identity anchor + material cues for lighting stability.
Example: "A startup founder in his late 30s with short black hair and light stubble,
wearing a charcoal cotton hoodie" — material cues give Veo a light-reflection profile.

**Motion description:**
Name a force or resistance: "falls with sudden weight", not just "falls". Vague motion = floaty output.
Use motion verbs: spins, lurches, sways, snaps, drifts.

**Camera language:**
- Shot types: extreme close-up, close-up, medium shot, wide shot, establishing shot
- Movements: static, slow dolly-in, tracking, pan, crane shot, handheld
- Speed: real-time, slow motion, time-lapse
- Lens cues: "35mm lens", "wide angle", "telephoto"

**Lighting:**
Always name a light source and how it behaves: "neon sign casting blue spill on wet pavement".
Do NOT describe brightness — describe source and behavior.

**Audio (Veo 3.1 unique feature):**
Use separate sentences for audio. Elements:
- Sound effects: "the sound of rain on a tin roof, distant thunder"
- Ambient noise: "city traffic and distant sirens"
- Dialogue: `"The woman in the blue coat says: 'I always knew you'd come back.'"` — dialogue in quotes
- Music: "gentle piano underscore"

**Aspect ratios supported:** 16:9, 9:16, 1:1, 4:3
**Resolution:** 720p or 1080p
**Clip length:** Up to 8 seconds standard; extend via Veo Extend

**Advanced features (Vertex AI):**
- Ingredients to video: provide reference images of characters/objects for consistency
- First and last frame: generate transition between provided start and end images
- Image to video: animate a source image with audio

**Prompting pattern for Veo 3.1:**
```
[Camera move] of [subject with material/appearance details]. [Subject action with
force/motion description]. [Setting with time and atmosphere]. [Lighting source and
behavior]. [Mood]. [Optional: audio in separate sentence]
```

---

## § RUNWAY GEN-4

- Strong at artistic, experimental, and surreal visuals
- Responds to cinematic language — reference film styles for consistent aesthetic
- Good for short-form social and music video style content
- Supports image-to-video and video-to-video modes
- Motion Brush: apply targeted motion to specific regions (available on Gen-4)
- Reference mode: maintain character/object appearance across clips

---

## § KLING 3.0

- Leading model for realistic human motion
- Best-in-class for start-and-end-frame control (keyframe interpolation)
- Kling O3 adds multishot — multiple camera perspectives in one generation (unique feature)
- Motion Control feature: specify exact trajectory of subjects
- Kling Lab: team collaboration tools
- Strong on body movement, physics-accurate motion
- Describe body movement explicitly: "right arm extends fully, elbow locking at full extension"
- Camera angle and shot type matter more on Kling than other models — specify explicitly

---

## § SORA 2 (OpenAI)

**Note: Sora web and app discontinued April 26, 2026. Sora 2 API continues.**

- Best at depicting human emotion and unusual/complex motion (breakdancing, acrobatics)
- Produces strong sense of depth and world immersion
- Camera movements and depth of field are auto-added — specify if you want static
- Adds audio and speech by default — add "no dialogue, no music, ambient only" if needed
- Strong prompt adherence; describe cinematically
- Watch for compression artifacts in complex scenes — iterate with refined prompts

---

## § LTX VIDEO

- Fast generation, prompt-sensitive
- Keep descriptions concise and visual — LTX responds to specific visual cues
- Specify resolution and motion intensity explicitly
- Good for rapid iteration and prototype clips

---

## § DREAM MACHINE (Luma)

- Cinematic quality with good lighting
- Keyframe feature: provide start image and end image → smooth interpolation
- Good for B-roll and visual social content
- Less reliable for people, dialogue, or structured narrative
- Reference lighting setups, lens types, and color grading styles in prompts

---

## § SEEDANCE 2.0 (ByteDance)

- Fastest generation time — ~30 seconds for 10-second clip
- ~85% usable output rate (higher than most competitors at ~65%)
- Multimodal input: combine images, videos, and audio tracks
- Good for rapid prompt variation testing — test 10 variations in time Kling generates 3
- Available via Artlist and as standalone platform

---

## § GENERAL VIDEO PROMPTING PRINCIPLES

1. **Describe outcomes, not steps.** "A woman finds a letter and her expression shifts from confusion to grief" not "first show the woman, then show the letter, then change her face."

2. **One main action per clip.** Complex multi-event clips degrade quality. Plan your shoot around single shots.

3. **Specify camera intent before subject action.** The camera framing sets up how the action reads.

4. **Material/texture descriptors stabilize subjects.** "Charcoal wool coat" gives the model a physical texture to track across frames.

5. **Audio is now first-class on Veo 3.1.** Write audio as a separate sentence at the end of the prompt. Other models: note their audio support level before prompting for sound.

6. **Aspect ratio defines the experience.** 9:16 for social; 16:9 for YouTube/cinematic; 1:1 for square social; 2.39:1 for anamorphic.

---

## § COMMON FAILURES

| Problem | Cause | Fix |
|---|---|---|
| Floaty, weightless motion | No force/resistance in motion description | Name a physical force: "slams", "pulls", "lurches" |
| Generic AI-plastic look | No surface texture on subject | Add material cues: "worn leather", "rough concrete", "silk catching light" |
| Subject drifts across clip | No identity anchor | Front-load detailed physical description before any action |
| Audio doesn't match video | Vague or absent audio description | Write audio as dedicated sentence at end of prompt (Veo 3.1 specifically) |
| Camera moves when should be static | Most models add movement by default | Explicitly state "static camera, no movement" |
| Sora web doesn't work | Web app discontinued April 2026 | Use Sora 2 API or switch to Veo 3.1 / Kling 3.0 |
