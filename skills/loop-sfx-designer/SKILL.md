---
name: loop-sfx-designer
description: >
  Designs the SFX inventory for The Loop: UI feedback sounds, elemental event
  sounds, ambient layers, reward stingers, notification tones, and minigame
  audio cues. Produces category-by-category SFX briefs with trigger conditions,
  tonal register, duration targets, and variation requirements. Distinct from
  suno-prompter (music tracks) and loop-audio-analyzer (spectrogram QA).
  Covers non-music audio — what sounds exist, when they fire, what they
  communicate. Use automatically — do not wait to be asked.
  Trigger on ANY of these signals: SFX inventory is being built or audited;
  a UI sound, reward sound, elemental sound, or ambient layer is being
  designed; "SFX", "sound effect", "UI feedback sound", "upgrade sound",
  "notification tone", "elemental audio cue"; MAN-23 SFX section is active;
  a screen or mechanic is being designed and audio feedback is discussed.
  Do NOT trigger for: music track generation (suno-prompter); spectrogram
  analysis (loop-audio-analyzer); VO or dialogue pipeline.
  Load once per session.
---
SKILL_VERSION: v1.2

# The Loop — SFX Designer

Produces the complete SFX inventory for The Loop and writes briefs for each
sound category. Output is implementation-ready for the Sound Design document.

---

## PART 1 — SFX DESIGN PRINCIPLES

**HARD FAIL:** MUST NOT design or approve any SFX without applying all principles in this section. Sound design is blocked until Part 1 is reviewed.

**Sound is always secondary feedback.** The player may be playing with volume
off, especially on mobile. Every SFX must have a visual or haptic counterpart.
Design audio as reinforcement, not as the primary signal.

**No sharp attack sounds.** Sounds that start at full energy (zero attack
envelope) cause startlement and negative UX. Apply a minimum 10ms fade-in on
all UI sounds. Exception: intentional alarm/alert states.

**Variation is required for repeating sounds.** Any sound that can fire more
than 3 times per session needs at least 2–3 variants (pitch shift, layering
difference, or alternative recording). Hearing identical sounds repeatedly
causes players to mute.

**Hierarchy controls attention.** SFX should not compete with music. Reward
stingers and milestone sounds are high priority — they duck the music briefly.
UI clicks are low priority — they sit under the music, never over it.

**Contextual register matches game state.** A sound in the Dreaming (cozy,
warm register) should not use the same tonal family as a sound in the Rift
(cold, constructed). Design SFX families per location, not globally.

---

## PART 2 — SFX CATEGORIES AND INVENTORY

### Category 1 — UI / Navigation

| Sound | Trigger | Register | Duration | Priority |
|---|---|---|---|---|
| Tab select | Player taps a main nav tab | Neutral, clean | 80–120ms | Low |
| Modal open | Any modal slides up | Neutral, soft | 150–200ms | Low |
| Modal close | Modal dismisses | Neutral, soft | 100–150ms | Low |
| Button confirm | Primary action confirmed | Warm, positive | 100–150ms | Medium |
| Button cancel | Cancellation / back | Neutral | 80–100ms | Low |
| Error / blocked | Invalid action | Dissonant, brief | 150–200ms | Medium |

All UI sounds: clean, non-diegetic. No fantasy instrumentation. Soft plucks,
chimes, or filtered tones. WAV format for instant playback.

### Category 2 — Elemental Events

Each classical element needs its own SFX family. Sounds should be sonically
distinct and reinforce the elemental's personality register.

| Event | Fire | Air | Water | Earth |
|---|---|---|---|---|
| Summon | Ignition burst, crackle | Rushing whoosh, bell-tone | Resonant splash, trickle | Low thud, resonant hum |
| Passive generation tick | Soft crackle loop | Faint flutter | Drip / flow undertone | Slow pulse |
| Upgrade tier | Building fire swell | Accelerating wind | Water deepens, resonates | Earth settles, low boom |
| Mature | Full ignition bloom | Open air swell | Deep liquid resonance | Ground settling |
| Ascend (max tier) | Held flame chord | Held wind chord | Held water chord | Held earth chord |

Duration: Summon 1–2s. Tick loops 2–4s seamless. Upgrade 0.5–1s. Ascend 2–3s.

Mana/Aether: neutral, crystalline, slightly reverberant. Liminal — no
strong elemental character.

Elements 5–11 (Shadow, Light, Void, Nature, 11th): OPEN pending MAN-31.
Reserve "designed" status until identities are confirmed.

### Category 3 — Reward and Progress Stingers

| Event | Tonal register | Duration | Music behavior |
|---|---|---|---|
| Upgrade purchased | Warm chime resolution | 400–600ms | Duck music briefly |
| Achievement unlocked | Triumphant 3-note resolve | 800ms–1s | Duck music |
| Cycle complete | Full resolution stinger | 1–1.5s | Duck music |
| Pay Gate unlocked (cycle 100) | Distinct unlock fanfare | 2–3s | Music pauses then resumes |
| Familiar milestone | Warm, intimate 2-note chime | 500ms | Subtle duck |
| Cards of Fate draw | Card-reveal swish + tone | 300–500ms | No duck |

Stingers must feel earned. Do not reuse the same stinger for different
significance levels — the Pay Gate unlock should sound materially distinct
from a routine upgrade.

### Category 4 — Minigame Audio Cues

**Ritual minigame:**
- Correct code element input: ascending note hit, harmonious
- Incorrect element input: dissonant, brief — not alarming, just wrong
- Pure code completion: resolution chord, brighter than Basic
- Basic code completion: resolution chord, muted

**Foraging minigame:**
- Dial turning: mechanical rotation sound, looped to dial speed
- Find: short resonant note matched to resource type
  (Decay: earthy, low; Treasure: bright chime; Fossil: stone tap;
  Artifact: crystalline; Aether: high, pure tone)
- Time pressure: ambient increases slightly — never a harsh alarm

**The Relay (DESIGN IN PROGRESS — treat as provisional):**
The Relay's stage design is not yet finalized. Stage 1 (Switchboard address
config mechanic) is still being resolved. Stages 2 and 3 are downstream.
SFX briefs below reflect the current working model but must be revisited
once The Relay design is locked.
- Switchboard plug connect: satisfying click + brief resonance
- Wrong plug: wrong-tone buzz, brief
- Frequency Tuning: tone sweeping with dial movement
- Lock in: decisive click-thunk
- Rotary Dial: mechanical ratchet per step

### Category 5 — Notification Tones

Notifications must be short, non-intrusive, and recognizable out of context
(player's device, volume low, phone in pocket).

| Notification type | Character | Duration |
|---|---|---|
| True Time event ready | Soft bell, single note | 300–500ms |
| Exchange NPC request | Warm tap + undertone | 200–300ms |
| Familiar message | Intimate two-tone | 300–400ms |
| Cycle available | Gentle alert, neutral | 200–300ms |

Never use stock OS notification sounds. All tones must be original and
recognizable as The Loop's audio identity.

---

## PART 3 — BRIEF FORMAT

When writing a SFX brief for the Sound Design document:

```
SFX BRIEF — [Sound name / ID]
Category: [UI / Elemental / Reward / Minigame / Notification]
Trigger: [exactly when this sound fires]
Location register: [Dreaming / Rift / Tower / Global]
Tonal character: [describe in sonic terms, not emotional metaphors]
Duration target: [range in ms]
Variation count: [minimum N variants required]
Priority in mix: [High = ducks music / Medium = sits with music / Low = under music]
Haptic pair: [yes / no — if yes, describe trigger]
```

---

## PART 4 — IMPLEMENTATION NOTES (React Native)

- Short UI sounds (<300ms): use uncompressed WAV for zero-latency playback.
- Looping elemental tones: OGG Vorbis for file size efficiency.
- Stingers and reward sounds: MP3 at 192kbps minimum.
- Audio ducking: implement globally when high-priority sounds fire.
- Separate volume sliders in Settings: Music (separate), SFX, Notifications.
- Test all sounds through device speaker at 50% volume — not headphones only.

---

## Out of Scope

This skill does NOT:
- Generate music tracks or Suno prompts (use suno-prompter)
- Analyze generated audio files via spectrogram (use loop-audio-analyzer)
- Design or script VO or dialogue audio pipelines
- Output code for audio playback implementation — see Part 4 for React Native notes only
- Make decisions about unconfirmed mechanics (Cards of Fate, unreleased elementals) — flag these as OPEN

---

## Examples

**Example 1 — Single SFX brief**

User: "Write the SFX brief for the Familiar milestone sound."

Skill fires. Part 1 principles reviewed first. Output:

```
SFX BRIEF — Familiar Milestone
Category: Reward
Trigger: Player reaches first relationship milestone with Familiar (depth meter Stage 1 → Stage 2)
Location register: Global (fires in any screen)
Tonal character: Warm, intimate — two-note resolution, soft attack, no sharp transient.
  Lower note first, higher note second. Not triumphant; quiet acknowledgment.
Duration target: 500ms
Variation count: 2 minimum (pitch-shift subtle variant)
Priority in mix: Medium — subtle duck at the moment of milestone, under stinger
Haptic pair: Yes — gentle single pulse at peak of upper note
```

**Example 2 — Category audit for elemental events**

User: "Have we covered all the elemental event sounds for the 5 classical elements?"

Skill fires. Part 2 Category 2 reviewed.

Confirmed coverage: Fire ✓, Air ✓, Water ✓, Earth ✓, Mana/Aether ✓ (neutral, crystalline)
OPEN: Elements 5–11 (Shadow, Light, Void, Nature, 11th) — pending MAN-31. Do not design SFX for these yet.

Output: gap summary noting which elements are pending and citing the OPEN blocker.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| suno-prompter | Music track generation for all Loop track families |
| loop-audio-analyzer | Spectrogram QA on generated Suno MP3s |
| utility-game-accessibility | Haptic feedback requirements and audio-as-sole-signal rule |
