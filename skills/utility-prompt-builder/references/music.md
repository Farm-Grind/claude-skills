# Music Reference — AI Music Generation (Generic)

## Contents
- § PLATFORM SELECTION TABLE
- § SUNO v5.5 — OVERVIEW AND INTENT EXTRACTION
- § SUNO HARD RULES
- § SUNO STYLE FIELD TEMPLATE (GENERIC)
- § SUNO LYRICS FIELD TEMPLATE
- § SUNO OUTPUT FORMAT
- § SUNO FAILURE MODE TABLE
- § UDIO v1.5
- § GENERATION WORKFLOW
- § LOOP PROJECT
- § EXAMPLES

---

## § PLATFORM SELECTION TABLE

| Goal | Platform |
|---|---|
| Vocals, full songs, pop/rock/R&B, quick results | Suno v5.5 |
| Instrumental quality, cinematic, ambient, game audio, extended compositions | Udio v1.5 |
| Voice cloning (upload your own voice) | Suno v5.5 Pro+ tier |
| Long-form continuous ambient (up to 15 min) | Udio v1.5 |
| Full standard 3-5 min songs with consistent structure | Suno v5.5 |
| Instrumental separation, stem editing, inpainting | Udio v1.5 |
| Speed (under 60 seconds to track) | Suno v5.5 |

**2026 context:** Suno v5.5 (March 2026) — current flagship with voice cloning, Suno Studio DAW, custom model fine-tuning. Udio v1.5 (mid-2025) — 48kHz output, inpainting, audio-to-audio remixing. Both require paid tiers for commercial rights.

---

## § SUNO v5.5 — OVERVIEW AND INTENT EXTRACTION

**Modes:**
- Simple Mode: single prompt field, AI controls all parameters. 500-char limit. Quick exploration only.
- Custom Mode: separate style field + lyrics field. ALWAYS use for production work.

**Prompting philosophy:** Suno rewards structure and emotional specificity. Front-load genre and feeling — they steer composition and chord structure. Instrumentation and energy come after and refine the production layer.

**Intent extraction — run before any prompt:**

| Dimension | What to extract |
|---|---|
| Function | What does this track do — location, scene, game state, mood context |
| Time signature + BPM | Waltz (3/4), standard (4/4), tango (4/4). BPM sets cognitive register |
| Mode / key | Minor, minor pentatonic, Dorian, drone (no key), or other |
| Lead instrument register | High register, mid register, warm/melodic, minimal/none |
| Reverb character | Bright, cold, dark, warm, deep |
| Special negatives | Track-specific instruments or styles to block beyond the base set |

Missing dimensions require clarifying questions (maximum 2 before generating a best-effort prompt).

---

## § SUNO HARD RULES

- NEVER include artist names in any prompt field. Translate all composer/artist references into sonic descriptors.
- NEVER use `[Continuous]` in the lyrics field — flattens arrangement, removes build arc.
- NEVER output only a style field. Always produce both fields in Custom Mode.
- NEVER front-load the lyrics field with anything other than negatives. Negatives lead.
- NEVER exceed 10-12 style tags. More dilutes rather than reinforces.
- NEVER use mood words that trigger string bleed: "ritual", "mysterious", "ancient wonder", "building energy", "Lydian"
- NEVER use texture adjectives that trigger string substitution: "fluid", "flowing", "lush", "analog synth pad"
- NEVER add a negative without a corresponding positive in the style field.
- ALWAYS use Custom Mode for production work.
- ALWAYS front-load the style field. Suno weights first 200 characters most heavily.
- ALWAYS keep the style field under 800 characters (hard limit 1,000, silently truncated without warning).

---

## § SUNO STYLE FIELD TEMPLATE (GENERIC)

Fill in bracketed variables. Remove unused optional lines.

```
[TIME SIG], [BPM] BPM,
[PRIMARY GENRE], [SUB-GENRE OR AESTHETIC],
[SONIC DESCRIPTOR — atmosphere, no artist names],
[KEY/MODE], [half-time feel — ambient/menu tracks only],
[PRODUCTION CONTEXT — e.g. video game soundtrack, film score], instrumental,
no vocals, no strings, no violin, no fiddle,
no guitar, no bass guitar, no orchestra, no choir, no saxophone,
[LEAD INSTRUMENT/SYNTH — register and character],
[BASS CHARACTER — e.g. driving analog synthesizer bass],
[DRUM PATTERN — e.g. standard pattern, slow driving 16th hi-hats],
[TEXTURE/SATURATION — e.g. tape saturation, lo-fi recording, clean mix],
[REVERB CHARACTER] reverb,
[loop-friendly — ambient tracks only],
[TRACK FUNCTION — e.g. menu track, combat cue, ambient tension],
[SPECIAL NEGATIVES — append only if needed]
```

**Notes:**
- Half-time feel: menu, ambient, neutral, panel tracks only. Omit for waltz and tango.
- Loop-friendly: ambient tracks only.
- Keep under 800 characters. Count before submitting.

---

## § SUNO LYRICS FIELD TEMPLATE

```
[No Vocals]
[No Choir]
[No Strings]
[No Violin]
[No Fiddle]
[No Guitar]
[No Bass Guitar]
[No Orchestra]
[No Saxophone]
[No Chanting]
[SPECIAL NEGATIVES — e.g. No Electroswing, No Concertina, No Accordion]
[Instrumental]
[Repeating Hook]
[Minimal Opening]
[Gradual Arrangement Build]
[Full Texture Midpoint]
[Sparse Ending]
[TEXTURE TAG — e.g. Analog Tape Saturation, Clean Digital Mix]
[BASS TAG — e.g. Driving Synth Bass Throughout]
[DRUM PATTERN TAG]
[RHYTHM TAG — e.g. Slow Driving 16th Hi-Hats]
[LEAD REGISTER TAG — e.g. High Register Lead, Warm Mid Lead]
[KEY/MOOD HARMONY TAG — e.g. Minor Key Harmony, Dorian Mode Harmony]
[SYNTH PAD LAYER — cold / warm / bright]
[RHYTHM CHARACTER TAG — omit on ambient and drone tracks]
[SINGLE EFFECT TAG — e.g. Single Filter Sweep, Single Ascending Synth Glide]
[No Hard Transitions]
```

**Short track (under 90 sec):** Compress to `[Minimal Opening]` `[Full Texture]` `[Sparse Ending]`. Drop `[Gradual Arrangement Build]`.

**v5.5 build arc note:** Generate first without build arc tags. Add only if output lacks natural build — v5.5 may handle loopable structure natively.

---

## § SUNO OUTPUT FORMAT

Always produce this exact structure:

```
STYLE FIELD
———————————
[style field content — under 800 characters]

LYRICS FIELD
———————————
[lyrics field content — bracket tags only, no prose]
```

After the blocks:
`🎯 Suno v5.5 Custom Mode — [one sentence: what was optimized and why]`

If the character count is near the limit, add:
`⚠ Style field: ~[N] characters. Monitor for truncation.`

---

## § SUNO FAILURE MODE TABLE

| Failure | Cause | Fix |
|---|---|---|
| Violin / strings bleed | Lydian mode, ritual, mysterious, ancient wonder, building energy, minor key + slow BPM + sparse arrangement | Remove mood words. Switch to minor pentatonic if bleed persists. Add `[No Violin][No Fiddle]` to both fields. |
| Guitar bleed | Dark fantasy without synth-dominance lock | Add `no guitar, no bass guitar` to both fields. Add explicit bass instrument tag. |
| Concertina / accordion bleed | Waltz time sig without sufficient synth specificity | Add `no concertina, no accordion, no electroswing` to style field. Add `[No Electroswing]` to lyrics field top. |
| Full orchestral bleed | Game title name references + mood words | Describe the sound, never name the game. Add `no orchestra` explicitly. |
| Vocals / chanting | ritual, shamanic, tribal, atmospheric without negatives | Never use these words. Block with `[No Vocals][No Choir][No Chanting]` at lyrics field top. |
| Choppy transitions | `[Intro][Bridge][Outro]` tags, `[Building Energy]`, or `[Continuous]` | Use build arc tags only. Never use section structure tags. `[Continuous]` is banned. |
| Modern EDM drift | Generic electronic / synth / dance without period anchors | Pair with a production era descriptor (e.g. `demoscene electronic`, `80s synthwave`). |
| Uptempo read at correct BPM | hook-driven + punchy mix + driving hi-hats together | Add `half-time feel`. Use `slow driving 16th hi-hats`. |
| Artist name flagged or ignored | Named artist in any prompt field | No artist names. Sonic abstractions only. |
| String substitution from texture words | fluid, flowing, lush, analog synth pad | Replace with specific instrument tags (e.g. `CS-80 pad`, `synth pad layer`). |

---

## § UDIO v1.5

**Prompting philosophy:** Udio rewards modularity and clarity. Each clause influences a discrete musical parameter. Clarity beats poetry.

**Best practices:**
- Break ideas into short sentences or fragments
- Use semicolons (;) instead of commas to separate concepts
- List genres, moods, and instruments as modular tags
- End with explicit style references or descriptors
- Iterate by swapping a single tag (e.g. "acoustic" → "electronic")

**Udio-specific features:**
- Advanced Controls: fine-tune BPM, key, and instrumentation independently
- Audio-to-audio remixing: upload a track as style reference
- Inpainting editor: fix specific sections without full regeneration
- Stem separation: available for post-production
- 48kHz output: professional video/film standard

**Udio output format:**
```
UDIO PROMPT
————————————
[prompt content using modular tag structure]
```
`🎯 Udio v1.5 — [one sentence: what was optimized]`

---

## § GENERATION WORKFLOW

1. Generate 2-3 tracks per prompt in Suno Custom Mode (or Udio with variation).
2. Evaluate — identify what drifted vs what held.
3. If a track is close but has a rough loop point or isolated problem section:
   - Suno: use Studio section editing and fade tools
   - Udio: use inpainting editor on the problem section
4. Re-prompt only if the fundamental register is wrong.
5. Save the exact style prompt for every keeper — reuse as base for variant tracks.
6. Export stems for any track going into final production.

---

## § LOOP PROJECT

When working on The Loop, load `references/music-loop.md` in addition to this file before generating any Suno prompt. It contains the Loop-specific aesthetic base template, intent extraction defaults per track family, the ritual waltz worked example, and the prompt-result log protocol.

Do not generate a Loop Suno prompt from this generic reference alone.

---

## § EXAMPLES

### Example — Fixing a broken prompt

**Input:** User pastes "Vangelis-inspired atmospheric strings, flowing and lush, mystical ritual energy."

**Violations found:**
- Artist name "Vangelis" → translate to sonic descriptors
- "flowing" and "lush" → string-substitution texture words → replace with instrument tags
- "atmospheric strings" → direct string summon → remove, add `no strings` negative
- "mystical ritual" → vocal/chanting bleed trigger → remove, replace with track function

**Output:**
```
STYLE FIELD
———————————
4/4 time, 90 BPM,
dark ambient, cinematic electronic,
cinematic analog synthesizer, tense minimal texture,
minor key, instrumental,
no vocals, no strings, no violin, no fiddle,
no guitar, no bass guitar, no orchestra, no choir, no saxophone,
warm register lead synth, driving synthesizer bass, bass-dominant mix,
standard drum pattern, slow driving 16th hi-hats,
tape saturation, cold reverb,
ambient tension cue

LYRICS FIELD
———————————
[No Vocals]
[No Choir]
[No Strings]
[No Violin]
[No Fiddle]
[No Guitar]
[No Bass Guitar]
[No Orchestra]
[No Saxophone]
[No Chanting]
[Instrumental]
[Minimal Opening]
[Gradual Arrangement Build]
[Full Texture Midpoint]
[Sparse Ending]
[Analog Tape Saturation]
[Driving Synth Bass Throughout]
[Standard Drum Pattern]
[Slow Driving 16th Hi-Hats]
[Warm Register Lead]
[Minor Key Harmony]
[Cold Synth Pad Layer]
[No Hard Transitions]
```
`🎯 Suno v5.5 Custom Mode — removed artist reference, replaced string-summoning texture words, added full negative set, translated "mystical ritual" to track function descriptor.`
