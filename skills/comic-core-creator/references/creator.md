# Webtoon / Manhwa Creator Reference

All methodology, phases, scripts, platform specs, AI tool guidance, and
examples for comic-core-creator. Loaded on demand — zero token cost until triggered.

---

## TOC

1. Terminology
2. Phase 1 — Pre-Production Documents
3. Phase 2 — Script Format
4. Phase 3 — Scroll Design Principles
5. Phase 4 — Canvas Technical Specs
6. Phase 5 — AI Production Tools
7. Phase 6 — Platform Publishing
8. Phase 7 — Project Plan Template
9. Manhwa Storytelling Conventions
10. Output Formats
11. Examples

---

# Webtoon / Manhwa Creator

## TERMINOLOGY

**Manhwa** — Korean comics (origin label). Covers print and digital.
**Webtoon** — Digital vertical-scroll format optimized for mobile. Originated in Korea but format is international. Most modern manhwa IS webtoon format.
**WEBTOON** — The platform (by Naver/LINE). Common point of confusion: the platform shares a name with the format.
**Practical implication:** When users say "manhwa" or "webtoon," assume they mean the same vertical-scroll digital format unless explicitly stated otherwise. Treat as identical for production purposes.

---

## PHASE 1 — PRE-PRODUCTION DOCUMENTS

Build these before drawing a single panel. A missing document will cost more time later than it takes to write now.

### 1.1 Series Bible
Single source of truth for the entire series. Sections:
- **Logline** — one sentence. Genre + protagonist + core conflict + stakes.
- **Premise** — 1–2 paragraphs. What the series IS, what makes it distinct.
- **Tone & Genre** — list primary and secondary genre. Describe emotional register.
- **World** — setting rules, any relevant lore, power systems, geography. Only what affects story.
- **Themes** — 2–3 recurring themes the series returns to.
- **Arc overview** — season or act structure, major turning points. Not episode-by-episode yet.
- **Target audience** — platform, age range, comparable titles.

### 1.2 Character Sheets
One sheet per major character. Two components:

**Visual spec** (for AI generation or artist):
- Physical description: height, build, skin/hair/eye color
- Costume: primary outfit with every element described precisely (specificity matters for any AI consistency method)
- Alternate outfits if recurring
- Expression range: neutral, happy, angry, sad, determined
- Silhouette note: character should be recognizable in pure silhouette

**Character profile:**
- Backstory summary (relevant to story, not exhaustive biography)
- Core motivation + core fear
- Voice/speech patterns (do they use slang? formal? clipped sentences?)
- Relationship map to other characters

### 1.3 Style Guide
Governs visual consistency across all episodes:
- Color palette: 5–8 hex values for recurring use (skin tones, environment, accent colors)
- Font stack: dialogue bubble font, caption font, SFX font
- Panel border style: rounded, sharp, borderless
- Gutter color(s)
- Recurring design motifs (e.g., flowers for emotion beats, rain for grief scenes)
- Episode title card template

### 1.4 Episode Outline
Before scripting, outline entire season/arc at episode level:
- Episode number + working title
- One-paragraph summary of events
- Emotional beat of episode (what does the reader feel by the end?)
- Cliffhanger or hook for next episode
- Character development moment (what changes or is revealed?)

### 1.5 Continuity Tracker
Start this document at episode 1 and update every episode. Continuity debt compounds — retroactive fixes are far harder than prevention.

Track:
- **Established facts:** anything stated about a character, place, or rule (names, ages, powers, relationships, injuries)
- **Open questions:** mysteries or unresolved threads planted for later
- **Visual continuity:** appearance details that must match across episodes
- **Timeline:** when events occur relative to each other

Format: living spreadsheet or flat document, one row per fact, flagging contradictions immediately.

---

## PHASE 2 — SCRIPT FORMAT

Webtoon scripts are panel-by-panel. Use this structure:

```
EPISODE [N]: [TITLE]

PANEL 1
[Scene/mood description. Camera angle. Who is present.]
DIALOGUE: Character Name: "Dialogue text."
CAPTION: [Narration if any.]
SFX: [Sound effect text.]

PANEL 2
...
```

**Script conventions:**
- Note full-width panels explicitly: `[FULL WIDTH — impact panel]`
- Note gutter size when pacing requires it: `[WIDE GUTTER — pause before reveal]`
- Max 3 speech bubbles per panel (WEBTOON guideline)
- Plan bubble placement in script — never fill panels retroactively
- Episodes: 30–80 panels is typical range. 40–55 is common for weekly release.
- Script word count: 1,500–2,500 words for a standard episode.

**Script style options:**
- Full panel description (for artist handoff)
- Dialogue-only script (for solo creator who will draw)
- Hybrid: scene description + dialogue (most common)

---

## PHASE 3 — SCROLL DESIGN PRINCIPLES

These are unique to webtoon format. Traditional comic instincts will fail here.

### Panel Width
- **Full-width panel:** high-impact moments, reveals, establishing shots
- **Half-width panels side-by-side:** rapid dialogue exchange, reaction shots
- **Narrow panels (stacked):** time passing, text-heavy exposition
- **Asymmetric split:** one large + one small in same row for contrast

### Gutter Space
The gap between panels is active storytelling:
- Tight gutter (8–16px): continuous action, quick pacing
- Standard gutter (30–60px): normal scene progression
- Wide gutter (100px+): dramatic pause, scene transition, breath moment
- Black/color fill gutter: chapter break, major tonal shift

### Thumb Stop Design
Readers scroll continuously. Design "thumb stop" moments to interrupt the scroll:
- Place a visually striking full-width panel at the point where you want readers to pause
- Typically: emotional peak, twist reveal, key character expression
- One to two per episode minimum; three to four for longer episodes

### Vertical Composition
- Lead the eye downward. Elements should flow top-to-bottom.
- Avoid strong horizontal vectors in action scenes (scroll format punishes them).
- Use character sightlines and gesture direction to pull the reader forward.
- Flashbacks: warm/sepia color overlay. Dream sequences: desaturated or inverted palette.

### Episode Hook Architecture
- **Opening panel:** re-establish where we are; do NOT recap — trust the reader.
- **End-of-episode hook:** never resolve cleanly. Either cliff (action/danger) or lure (emotional question left open). The last panel before scroll-end is your subscription hook.

### Visual Tone Coherence
The visual register (color temperature, line weight, SFX style) must match the narrative stakes at every moment. Misalignment breaks reader immersion without them knowing why.

- **Bright colors + comedic SFX during a death scene** → reader disengages
- **Dark, heavy contrast during a lighthearted moment** → tonal whiplash
- Match saturation and warmth to the emotional content: desaturate for grief, heighten contrast for danger, soften palettes for intimacy
- Transition visual tone deliberately when the story's emotional register shifts — don't let it drift

### Show, Don't Tell in Panels
Webtoons are a visual medium. Every emotion that can be shown through body language, environment, or action should not also be stated in dialogue.

- **Tell (weak):** Character says "I'm terrified."
- **Show (strong):** Character's hands grip the door frame, knuckles white. Wide eyes. One panel of silence before they speak.
- Use environment to externalize internal state: cluttered room = overwhelmed character; empty space = isolation
- Dialogue should do double duty — advance plot AND reveal character. Single-function dialogue wastes panel space.
- What characters don't say is often more powerful. A meaningful silence, a deflection, a changed subject — these carry subtext that direct statement cannot.

---

## PHASE 4 — CANVAS TECHNICAL SPECS

These specs apply to **manual production workflows** exporting to WEBTOON Canvas, Tapas, or self-hosted platforms. If using an integrated platform like Dashtoon, it handles export natively — skip this section and follow the platform's own export flow.

### Working Resolution
| Setting | Value |
|---|---|
| Working canvas width | 1,600 px (draw at 2x) |
| Export width | 800 px |
| Working DPI | 300 |
| Export format | JPG (painted/colored) or PNG (line art) |
| Upload slice height (WEBTOON Canvas) | Max 1,280 px per file |
| Export height per file | 1,280 px after downscale |
| Software that handles auto-slice | Clip Studio Paint EX, Croppy tool |

**Never draw at 800px.** Art will be visibly degraded. Draw at 1,600px minimum, export at 800px.

### Canvas Structure
- One continuous vertical canvas per episode (not separate pages)
- Typical episode height: 8,000–20,000 px working size (5,000–12,500px exported)
- Safe margin: 20–40px on left and right edges (mobile crop buffer)
- Keep critical content (faces, key text) away from bottom 80px of each 1,280px slice

### Export Workflow
1. Draw on long canvas at 1,600px wide
2. Export full-resolution file
3. Downscale to 800px wide
4. Auto-slice into 1,280px-height segments (Clip Studio or Croppy)
5. Upload all slices to platform — the platform stitches them seamlessly

---

## PHASE 5 — AI PRODUCTION TOOLS

### Step 1: Choose Your Approach

Answer these two questions before looking at any specific tool:

**Q1 — Technical overhead tolerance?**
- Minimal (prefer GUI, no setup, no CLI) → **Integrated Platform** path
- Moderate (comfortable with tutorials and GUI tools) → **Component Stack** path
- High (comfortable with local installs, CLI, model management) → **Full Control** path

**Q2 — Distribution intent?**
- Publish on Dashtoon's own platform → Dashtoon integrated workflow
- Publish on WEBTOON Canvas, Tapas, or own site → Component Stack or export from integrated platform
- Maximum flexibility across platforms → Component Stack

### Integrated Platform Path (minimal overhead)

**Dashtoon Studio** — the strongest current option for creators prioritizing simplicity.
- Purpose-built for vertical scroll webtoon format
- Built-in character library + trainable character models (GUI, no technical setup)
- Storyboard2Comic: sketch rough layouts, AI fills panels — gives composition control without art skill
- Speech bubble and text tools built in
- Native webtoon export
- Free tier: 100 images/day, 1 character training/day
- Publishes directly to Dashtoon's reader platform OR exports for publishing elsewhere

**IP and contract warning for Dashtoon:** Two distinct contract types exist. The self-publish path (you create and upload yourself) uses a non-exclusive license — you retain ownership, can publish elsewhere, can terminate with 60 days notice. The exclusive contract is a long-term rights grant and should not be signed without legal review. Always use the self-publish path unless you have negotiated custom terms. Verify current terms at dashtoon.com before committing.

**LlamaGen.ai** — lighter alternative, generation-focused without Dashtoon's full ecosystem.

### Component Stack Path (moderate overhead)

Best for creators who want output quality control and plan to publish on WEBTOON Canvas, Tapas, or their own platform.

**Generation:** Leonardo.AI — built-in character reference, good anime/manhwa output, usable free tier. Midjourney for backgrounds and establishing shots where character consistency isn't required.

**Compositing and export:** Clip Studio Paint — industry standard for webtoon production. Handles lettering, SFX, motion lines, panel assembly, and auto-slicing for platform upload. One-time license ~$50.

**Workflow:**
1. Generate character concept art (Leonardo.AI or Midjourney)
2. Build locked character reference sheet (multiple poses, expressions)
3. Use Leonardo character reference consistently — same reference image every generation
4. Generate panels; composite in Clip Studio Paint
5. Add dialogue, SFX, effects manually in Clip Studio
6. Export and slice per Phase 4 canvas specs

### Full Control Path (high overhead)

For creators willing to invest setup time for maximum consistency and pipeline control.

**ComfyUI + FLUX + LoRA** — train a character LoRA (15–50 reference images, 1–4 hours, local GPU or RunPod cloud), then generate all panels with locked character appearance. Highest consistency of any method. Steep learning curve.

**Character Consistency Methods (ranked by reliability):**

1. **LoRA Fine-Tuning** — train on reference images; output is a `.safetensors` file applied per generation. Best for series with 20+ episodes.
2. **IP-Adapter / InstantID** — reference image injected per generation via ComfyUI nodes. Good consistency without training.
3. **Character Reference (Midjourney `--cref`)** — fastest iteration, less precise.
4. **Seed Lock + Prompt** — lowest effort, breaks on pose/outfit variation. Not suitable for serialized production.

### AI Limitations Across All Approaches
- **Hands and text in images:** unreliable in all tools — always add text manually
- **Multi-character scenes:** consistency degrades with 3+ characters regardless of tool
- **Dynamic action:** AI generations are static; motion lines must be added manually
- **Style drift:** integrated platforms manage this internally; component stacks require LoRA or strict reference discipline

---

## PHASE 6 — PLATFORM PUBLISHING

### Platform Comparison

| Platform | Access | Audience | Monetization | Content |
|---|---|---|---|---|
| WEBTOON Canvas | Open (self-pub) | Largest global | Ad revenue share | All ages (genre-filtered) |
| Tapas | Open | Mid-size, community-focused | Ink tips, ad revenue, paid eps | All ages |
| Lezhin | Audition/invite | Premium paid readers | Paid episodes | Mature content allowed |
| Manta | Curated | Subscription readers | Subscription share | All ages |
| Naver/Kakao | Korean market | Domestic Korea | High revenue potential | Requires Korean |

### WEBTOON Canvas Launch Strategy
- Upload first 3 episodes on launch day (platform prompts subscribe after ep 3)
- Weekly release cadence is the standard; biweekly is acceptable
- Build a buffer of 4–8 episodes before publishing episode 1
- Thumbnail optimization: close-up character face, high contrast, readable at 200px
- Episode title: descriptive + emotionally evocative

### Platform Upload Specs (WEBTOON Canvas)
- Width: 800px (720–1,080px acceptable)
- Height per image: flexible, 1,280px per slice recommended
- File type: JPG or PNG
- File size: under 5–10 MB per image (confirm in uploader)
- Series thumbnail: 300×400px
- Episode thumbnail: 800×250px

### Rights Caution
- Read exclusivity terms before signing any contract
- WEBTOON Canvas (self-pub) does not claim exclusivity
- WEBTOON Originals contracts typically include exclusivity and adaptation rights
- Lezhin and Manta exclusivity terms vary — review before accepting
- **AI tool IP:** Integrated platforms (Dashtoon, LlamaGen) have their own terms governing generated image ownership. Dashtoon's self-publish path is non-exclusive and you retain ownership; their exclusive contract is not. Always verify current terms before publishing — these change and the distinction is material.

---

## PHASE 7 — PROJECT PLAN TEMPLATE

Standard pre-launch checklist:

**Pre-Production (weeks 1–4)**
- Series bible complete
- All major character sheets complete with visual references
- Style guide complete
- Season/arc outline complete
- Episode scripts for episodes 1–8 drafted

**Production — Buffer Build (weeks 5–10)**
- AI tool stack validated and character consistency method confirmed
- Character consistency baseline established (LoRA trained, or reference sheet locked, or platform character model trained — per chosen approach)
- Episodes 1–5 fully produced (panels, color, effects, typography, formatted)
- Episode 6–8 in production

**Publishing Setup (week 11)**
- Platform account created
- Series metadata written (logline, synopsis, genre tags)
- Thumbnail and cover art produced
- Social media presence established (minimum: one platform)

**Launch (week 12)**
- Episodes 1–3 published
- Social announcement
- Weekly cadence begins

---

## MANHWA STORYTELLING CONVENTIONS

Distinct from manga and Western comics — reflect K-drama influence:
- **Hook immediately:** First chapter must establish the central conflict or character hook. No slow-burn introductions.
- **Emotional intensity first:** Manhwa readers expect melodrama, dramatic close-ups, heightened stakes early.
- **Common structural tropes:** regression arcs, reincarnation/isekai, villainess redemption, second-chance romance, system/status screens (OP protagonist).
- **Cliffhangers are structural:** every episode ends on an open question or danger. Not optional.
- **Left-to-right reading:** unlike manga. Panels flow L→R, then downward.
- **Full color is expected:** black-and-white webtoons exist but are an exception and audience expectations differ.
- **Bingeable pacing:** structure for readers who will consume multiple episodes in one session. Reward binge-reading with satisfying arc payoffs at regular intervals.

---

## OUTPUT FORMATS

When activated for document creation, Claude produces:

- **Series Bible:** structured document, sections per Phase 1.1
- **Character Sheet:** visual spec block + character profile block
- **Style Guide:** color swatches (hex), font names, visual motif list
- **Episode Outline:** table format — episode number, summary, beat, hook
- **Continuity Tracker:** spreadsheet-style living document, one row per established fact
- **Episode Script:** panel-by-panel format per Phase 2
- **Production Checklist:** Phase 7 template adapted to the specific project

---

## EXAMPLES

**Example triggers:**
- "Help me build a webtoon about a girl who discovers her memories have been erased" → Start with series bible, then offer to build character sheets
- "I need a character sheet for my male lead — he's a brooding swordsman" → Prompt for visual details, then produce visual spec + profile
- "How many panels should my first episode have?" → Answer from Phase 2 conventions + ask about genre/pacing intent
- "Which AI tool should I use to generate consistent characters?" → Phase 5 Step 1 decision questions (overhead tolerance + distribution intent) before recommending
- "Should I use Dashtoon?" → Phase 5 Integrated Platform path + IP/contract warning
- "How do I export for WEBTOON?" → Phase 4 canvas specs (manual workflow) + Phase 6 upload specs

**Out of scope:**
- Manga (Japanese, right-to-left, print format) — different conventions; this skill does not cover it
- Print comic books or graphic novels — different format requirements
- General AI image generation with no comic application
- Video/motion comics — not covered

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| comic-extended-narrative | Narrative design — series structure, episode beats, worldbuilding, character arcs |
| frontend-design | If building a web reader or series landing page |
| docx | If producing any of the pre-pro documents as Word files |
| WEBTOON Creator Help | https://www.webtoons.com/en/creator-guide |
| Clip Studio Paint webtoon guides | https://tips.clip-studio.com |
