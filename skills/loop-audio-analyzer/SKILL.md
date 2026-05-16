---
name: loop-audio-analyzer
description: >
  Analyzes Suno-generated MP3 files for The Loop via spectrogram generation and
  visual frequency analysis. Enforces a strict context-budget protocol to prevent
  context window exhaustion: triage all files first with ffprobe (no images),
  then process in pairs with analysis between — never generate or view more than
  2 spectrograms before producing analysis text. Scores each track pass/fail
  against the track family's text profile in references/track-profiles.md — no
  reference images are ever loaded. Use automatically — do not wait to be asked.
  Trigger on ANY of these signals: one or more MP3 files are uploaded; user says
  "analyze this track", "run the spectrogram", "check the audio", "what does
  this sound like spectrally", "upload for analysis"; an audio file appears in
  the uploads directory; a Suno generation result needs triage against the brief.
  Do NOT trigger for: non-audio files, prompt writing (suno-prompter), or sound
  design document updates. Load once per session.
---
SKILL_VERSION: v1.0

# The Loop — Audio Analyzer Skill

Generates spectrograms and scores Suno MP3 outputs pass/fail against defined
track family profiles. Text profiles only — no reference images ever.

---

## CRITICAL: Context Budget Protocol

**Non-negotiable. Violating this causes response truncation.**

Token cost per spectrogram at 1568×784: ~1,639 tokens.
Hard limit: 2 spectrograms maximum before producing analysis text.
Failure mode: generating and viewing 4+ spectrograms before writing analysis
exhausts the context window mid-response.

### Mandatory sequence for any upload:

```
STEP 1 — TRIAGE (ffprobe only, no images, all files in one bash call)
STEP 2 — RANK by priority (user-flagged first, then by duration outliers)
STEP 3 — PAIR 1: generate 2 spectrograms → view both → write analysis
STEP 4 — PAIR 2 if needed: generate 2 more → view both → write analysis
STEP 5 — BATCH SUMMARY across all analyzed files
```

Never skip triage. Never queue all spectrograms before writing.
Never view more than 2 spectrogram images before producing analysis text.

---

## Step 1 — Triage Command

Run on all files before any spectrogram generation:

```bash
for f in /mnt/user-data/uploads/*.mp3; do
  echo "=== $(basename $f) ==="
  ffprobe -v quiet -show_entries format=duration,size,bit_rate \
    -of default=noprint_wrappers=1 "$f" 2>/dev/null
done
```

Rank output: user-flagged files first, duration outliers second,
previously dismissed files last. Process highest-priority pair first.

---

## Step 2 — Spectrogram Generation

**1568×784 only. Never larger — API silently downsizes anything above
1568px on the long edge anyway, so larger sizes waste tokens with no
quality gain.**

```bash
mkdir -p /home/claude/spectrograms
ffmpeg -y -i "/mnt/user-data/uploads/[FILENAME].mp3" \
  -lavfi "showspectrumpic=s=1568x784:mode=combined:color=intensity:scale=log:fscale=log:legend=1" \
  "/home/claude/spectrograms/[FILENAME]_spec.png" 2>&1 | tail -1
```

Generate 1–2 files per bash call maximum. View immediately after
generating. Never defer viewing.

### 15-second segment (anomaly isolation only):

```bash
ffmpeg -y -i "/mnt/user-data/uploads/[FILE].mp3" \
  -ss [START_SECONDS] -t 15 \
  -lavfi "showspectrumpic=s=1568x784:mode=combined:color=intensity:scale=log:fscale=log:legend=1" \
  "/home/claude/spectrograms/[FILE]_seg[START]s.png" 2>&1 | tail -1
```

Use only when a specific anomaly needs isolation. Not part of standard flow.

---

## Step 3 — Spectrogram Reading

Read these zones in order after viewing each image:

| Zone | Frequency | Target signal |
|---|---|---|
| Sub-bass | 20–80 Hz | Density — warm orange/yellow for Crucible/Waltz |
| Bass | 80–250 Hz | Consistency — gaps = thin, overload = mud |
| Low-mid | 250–640 Hz | Anomaly watch zone — unexpected bright clusters |
| Mid | 640–1200 Hz | CS-80 zone — horizontal banding = phrase loops working |
| Upper-mid | 1200–4000 Hz | Structure vs smear |
| High | 4000–8000 Hz | Groove (periodic lines) vs smear (continuous wall) |
| Air | 8000+ Hz | Should thin on tape saturation tracks |

**Structural markers:**
- Phrase periodicity: repeating vertical columns at regular intervals
- Horizontal banding: same frequency clusters appearing rhythmically
- Density variation: color changes over time = arrangement arc working
- Flat energy: uniform color wall = no structure

---

## Step 4 — Anomalous Layer Detection

Documented on Crucible tracks. Detection zone: 600–900 Hz.

Classify if found:
- **Periodic** (repeats on phrase rhythm): melodic instrument on a loop —
  redirectable via prompt, may be desirable if timbre fits brief
- **Random** (irregular bursts): instrument bleed — add to negative set
- **Merged** (indistinguishable from main texture): density problem

---

## Step 5 — Scored Analysis Output

Load track family profile from `references/track-profiles.md` before scoring.
Score each criterion PASS / FAIL / PARTIAL. No essays — one line per criterion.

```
ANALYSIS — [filename]
Duration: [X:XX]  |  Settings: [weirdness/style-influence if known]
Track family: [Crucible / Waltz / Menu / Rift / etc.]

SCORE
  Bass dominance:        [PASS/FAIL/PARTIAL]
  Phrase periodicity:    [PASS/FAIL/PARTIAL]
  Density variation:     [PASS/FAIL/PARTIAL]
  High-end control:      [PASS/FAIL/PARTIAL]
  Anomaly status:        [ABSENT/PERIODIC/RANDOM/MERGED]

ISSUES  [bullet per failure/partial — one line each]
FIX     [one prompt or settings change per issue — one line each]
VERDICT [KEEP / DISCARD / CANDIDATE — one sentence max]
```

---

## Step 6 — Batch Summary

After all files in a batch are analyzed:

```
BATCH — [N] files analyzed

Best structural candidate:  [filename]
Best tonal candidate:       [filename]
Recommended action:         [keep X / re-prompt / adjust settings]
Settings finding:           [what the A/B comparison revealed]
Next prompt change:         [single most impactful change, or "none"]
```

---

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Response truncated | Too many spectrograms before writing text | Never exceed 2 before analysis output |
| Spectrogram generation fails | Path wrong or ffmpeg missing | `which ffmpeg` + `ls /mnt/user-data/uploads/*.mp3` |
| Image too dark to read | Wrong scale | Always use `scale=log:fscale=log` |
| All files look identical | Style Influence too high | Note in batch summary |
| Anomaly not isolatable | Track too dense | Generate 15s segment spectrogram |

---

## Settings Reference

| Setting | Confirmed behavior |
|---|---|
| Weirdness 10% | More rhythmic regularity, cleaner high-end |
| Weirdness 50% | More variation, episodic bursts, less structural discipline |
| Style Influence 70% | Strong style adherence, descriptor words taken literally |
| Style Influence 90% | Verbatim style field readout artifacts |
| Inspo track | Anchors rhythmic structure to reference MP3 |
| Lyrics Mode | Always Manual |

---

## Examples

**Example 1 — Single file triage and analysis**

User uploads one MP3: `crucible_v3.mp3`. Skill fires on file in uploads directory.

Correct sequence:
1. STEP 1 — ffprobe triage on `crucible_v3.mp3` (no images)
2. STEP 3 — generate spectrogram → view → write ANALYSIS block immediately
3. STEP 6 — batch summary (N=1)

Skill catches:
- Generating spectrogram without running ffprobe first → CRITICAL: triage always precedes spectrogram
- Generating spectrogram and deferring view until after a second → CRITICAL: view immediately, 2-image max before text

**Example 2 — Multi-file batch with context budget enforcement**

User uploads 5 MP3 files for A/B comparison. Skill fires on multiple uploads.

Correct sequence:
1. STEP 1 — single ffprobe bash call across all 5 files, rank by priority
2. STEP 3 — generate files 1+2 → view both → write full ANALYSIS blocks for each
3. STEP 4 — generate files 3+4 → view both → write full ANALYSIS blocks for each
4. Single file 5 → view → write ANALYSIS block
5. STEP 6 — batch summary across all 5

Context budget: never exceed 2 spectrograms before producing analysis text. With 5 files: pair (2) → text → pair (2) → text → single (1) → text → batch summary.

**Example 3 — Anomaly isolation with segment spectrogram**

Standard Crucible analysis shows suspicious energy cluster in 600–900 Hz zone on `crucible_v7.mp3`. Step 4 anomaly detection fires.

Correct sequence:
- Classify anomaly as PERIODIC / RANDOM / MERGED from the full spectrogram first
- If MERGED or ambiguous: generate 15-second segment at the anomalous timestamp
- Classify again from segment — does it repeat on phrase rhythm?
- Report in SCORE block under "Anomaly status" and provide targeted FIX prompt change

Segment spectrogram is anomaly isolation only — never substitute for the full spectrogram.

---

## Out of Scope

- Writing or revising Suno prompts → suno-prompter
- Updating the sound design document → human action after analysis
- Loading or comparing reference spectrogram images → retired, text profiles only
- Subjective feel or emotional response → structural and spectral only

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| suno-prompter | Writing and revising Suno prompts based on analysis findings |
| references/track-profiles.md | Target profiles for all Loop track families |
| the-loop sound-design document | Brief, named genres, per-track variables |
