# Music Reference — The Loop Project (Suno)

Extends `references/music.md`. Load both files for any Loop Suno session.
All generic Suno rules from music.md apply unless explicitly overridden here.

## Contents
- § LOOP PREREQUISITE
- § THE LOOP BASE TEMPLATE — STYLE FIELD
- § THE LOOP BASE TEMPLATE — LYRICS FIELD
- § LOOP INTENT EXTRACTION DEFAULTS
- § LOOP GENERATION WORKFLOW
- § PROMPT-RESULT LOG
- § WORKED EXAMPLE — RITUAL WALTZ

---

## § LOOP PREREQUISITE

Load the current sound-design document BEFORE generating any prompt. It contains:
- Master prompt template (LOCKED)
- Per-track variable table (time sig, BPM, mode, CS-80 register, reverb, special negatives per track family)
- Location briefs and named genres
- Waltz speed variants and Crucible tango speed tiers
- Asset inventory and track status

Do not generate a Loop prompt without consulting that document. Per-track variables live there, not here. This file contains the base template and operational protocol only.

---

## § THE LOOP BASE TEMPLATE — STYLE FIELD

The Loop's locked aesthetic: dark synthwave / demoscene electronic, CS-80 lead, TR-808 rhythm, analog bass, tape saturation. Fill in bracketed variables from the sound-design document per-track table.

```
[TIME SIG], [BPM] BPM,
[NAMED GENRE], dark synthwave,
[PROMPT ABSTRACTION — sonic descriptor, no artist names],
[KEY/MODE], [half-time feel — ambient/menu only],
video game soundtrack, instrumental,
no vocals, no strings, no violin, no fiddle,
no guitar, no bass guitar, no orchestra, no choir, no saxophone,
[CS-80 REGISTER] CS-80 [lead melody / lead synth riff / minimal],
driving analog synthesizer bass, bass-dominant mix,
TR-808 [PATTERN], [slow / standard] driving 16th hi-hats,
tape saturation, lo-fi recording,
[REVERB CHARACTER] reverb, demoscene electronic,
[loop-friendly — ambient tracks only],
[TRACK FUNCTION],
[SPECIAL NEGATIVES — append only if needed]
```

**Half-time feel:** Apply to menu, ambient, neutral, and panel tracks. Omit for waltz and tango tracks.
**Loop-friendly:** Ambient tracks only.
**Character limit:** Under 800 characters. Count before submitting.

---

## § THE LOOP BASE TEMPLATE — LYRICS FIELD

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
[Analog Tape Saturation]
[Driving Synth Bass Throughout]
[TR-808 PATTERN TAG]
[Slow / Standard Driving 16th Hi-Hats]
[CS-80 REGISTER — e.g. High Register CS-80 Lead]
[KEY/MOOD HARMONY TAG — e.g. Minor Key Harmony / Dorian Mode Harmony]
[SYNTH PAD LAYER — cold / warm / bright]
[RHYTHM CHARACTER TAG — omit on ambient and drone tracks]
[SINGLE EFFECT TAG — e.g. Single Filter Sweep / Single Ascending Synth Glide]
[No Hard Transitions]
```

**Short track (under 90 sec):** Compress to `[Minimal Opening]` `[Full Texture]` `[Sparse Ending]`. Drop `[Gradual Arrangement Build]`.
**v5.5 build arc:** Generate first without build arc tags. Add only if output lacks natural build.

---

## § LOOP INTENT EXTRACTION DEFAULTS

The Loop's six intent dimensions with typical values per track type. Pull exact values from the sound-design document per-track table.

| Dimension | Loop Typical Values |
|---|---|
| Function | ritual waltz / dreaming ambient / rift action / menu / panel / combat |
| Time sig + BPM | 3/4 waltz (70-110 BPM) / 4/4 standard / 4/4 tango (see speed tiers) |
| Mode / key | Minor / minor pentatonic / Dorian / drone (see track family) |
| CS-80 register | High (lead melody) / mid riff / warm melodic / minimal |
| Reverb character | Bright / cold / dark / warm / deep (see track family) |
| Special negatives | Waltz: `no concertina, no accordion, no electroswing` / tango: `no bandoneon` |

---

## § LOOP GENERATION WORKFLOW

1. Load sound-design document — verify per-track variables match what you're building.
2. Generate 2-3 tracks per prompt in Custom Mode.
3. Evaluate — identify what drifted vs what held.
4. If close but rough: use Suno Studio section editing and fade tools. Do not re-prompt for isolated problems.
5. Re-prompt only if the fundamental register is wrong.
6. Save the exact style prompt for every keeper.
7. Log the result in the Prompt-Result Log (see below) if the track was evaluated.
8. Export stems for any track going into final production.

---

## § PROMPT-RESULT LOG

Tracks which prompts produced which outcomes for Loop tracks. Accumulates iteration knowledge across sessions.

**Storage:** Cloudflare D1 — `suno_log` table
**DATABASE_ID:** `a2af54f4-6385-45dd-92e7-edc45fa5b8bd` (from protocol doc — never from memory)
**MCP tool:** `d1_database_query` — always use parameterized queries per the protocol
**Authoritative protocol:** `D1:SUNO_LOG_PROTOCOL` — fetch from `documents` table if this reference and the D1 doc diverge; D1 doc wins.

**D1 schema:**
```sql
CREATE TABLE IF NOT EXISTS suno_log (
  id         TEXT PRIMARY KEY,
  track_name TEXT,
  prompt     TEXT,
  result     TEXT,
  created_at TEXT
)
```

**ID assignment — run before every INSERT:**
```sql
SELECT MAX(id) FROM suno_log
```
IDs are zero-padded three digits: SL-001, SL-042. On INSERT failure (UNIQUE constraint): re-run SELECT MAX and reassign.

**Write (log a result):**
```sql
-- params: ['SL-001', 'ritual-waltz', 'full style + lyrics field text', 'PASS | strings held, BPM correct']
INSERT INTO suno_log VALUES (?, ?, ?, ?, datetime('now'))
```

`result` format: `OUTCOME | notes` — e.g., `PARTIAL | strings bled, switched to minor pentatonic. Try half-time feel next.`

**Read (view log):**
```sql
SELECT id, track_name, result, created_at FROM suno_log ORDER BY created_at DESC
```

**Read by track family:**
```sql
-- params: ['ritual-waltz']
SELECT id, prompt, result, created_at FROM suno_log WHERE track_name = ? ORDER BY created_at DESC
```

**When to log:** After every generation session where a prompt was evaluated. Minimum useful entry: track_name + OUTCOME in result field + one-sentence notes. Do not log if no evaluation happened.

**Trigger signals:** user says "log that result", "note what happened", "track this", or a session ends where prompts were generated and evaluated.

**Confirm format:**
`✓ SL-007 logged — ritual-waltz PARTIAL: strings held, BPM read as uptempo. Try half-time feel next.`

---

## § WORKED EXAMPLE — RITUAL WALTZ

**Input:** "Write a Suno prompt for the ritual waltz at adagio tempo (80 BPM), fire element."

**Output:**
```
STYLE FIELD
———————————
3/4 waltz time, 80 BPM,
pulp action demoscene synthwave, dark synthwave,
electric ritual synth, primal demoscene waltz,
minor key, video game soundtrack, instrumental,
no vocals, no strings, no violin, no fiddle,
no guitar, no bass guitar, no orchestra, no choir, no saxophone,
no electroswing, no concertina, no accordion,
high register CS-80 lead, driving analog synthesizer bass, bass-dominant mix,
TR-808 waltz pattern, slow driving 16th hi-hats,
tape saturation, lo-fi recording, bright reverb,
demoscene electronic, ritual minigame waltz

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
[No Electroswing]
[No Concertina]
[Instrumental]
[Repeating Hook]
[Minimal Opening]
[Gradual Arrangement Build]
[Full Texture Midpoint]
[Sparse Ending]
[Analog Tape Saturation]
[Driving Synth Bass Throughout]
[TR-808 Waltz Pattern]
[Slow Driving 16th Hi-Hats]
[High Register CS-80 Lead]
[Minor Key Harmony]
[Bright Synth Pad Layer]
[Waltz Pulse Throughout]
[Single Ascending Synth Glide]
[No Hard Transitions]
```
`🎯 Suno v5.5 Custom Mode — ritual waltz brief filled, special negatives added for waltz bleed, build arc included.`
