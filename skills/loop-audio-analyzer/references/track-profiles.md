# Track Family Profiles — Spectrogram Targets

Text-only targets. No reference images. Each profile defines the expected
spectrogram state for a confirmed brief-compliant track. Analysis scores
pass/fail against these. Update when a track is confirmed as a keeper.

---

## How to Read These Profiles

Each frequency zone is rated:
- HOT: dense orange/yellow/white — high energy, continuous
- WARM: moderate orange — present but not dominant
- COLD: dark blue/purple — minimal energy, intentional absence
- STRUCTURED: visible repeating pattern (banding or periodic columns)
- FLAT: uniform color with no temporal variation — absence of arrangement

---

## CRUCIBLE TANGO (all elements, all speed tiers)

Named genre: Mechanical precision industrial tango

| Zone | Frequency | Target state | Notes |
|---|---|---|---|
| Sub-bass | 20–80 Hz | HOT | Dense, continuous, no gaps |
| Bass | 80–250 Hz | HOT | Warmest zone — bass-dominant mix |
| Low-mid | 250–640 Hz | COLD | No bright clusters — anomaly watch zone |
| Mid | 640–1200 Hz | STRUCTURED | Horizontal banding at regular intervals; CS-80 phrase loops visible as repeating columns |
| Upper-mid | 1.2–4 kHz | WARM + STRUCTURED | Melodic content visible and periodic, not smeared |
| High | 4–8 kHz | STRUCTURED | Periodic vertical lines (hi-hat groove), NOT a continuous wall |
| Air | 8 kHz+ | COLD→WARM | Tape saturation rolloff — thins toward top |

Structural requirements:
- Phrase periodicity: visible repeating event columns at ~8-bar intervals
- Density variation: sparse open → full texture midpoint → sparse ending
- No flat-energy sections longer than 8 bars

Speed tier differences (same profile, density scales):
- Andante (96 BPM): longer phrase columns, more space between events
- Moderato (108 BPM): baseline density
- Allegretto (120 BPM): tighter columns, same spacing ratio
- Allegro (132 BPM): dense but still structured — columns must remain visible
- Presto (152 BPM): maximum density — high-end control most critical here

Anomalous layer ruling: periodic anomaly at 640–877 Hz is acceptable IF
timbre is CS-80 consistent. Random anomaly at same zone = add to negative set.

---

## RITUAL WALTZ (all elements, all speed tiers)

Named genre: Electric ritual demoscene waltz
Status: [OPEN — no confirmed keeper track yet. Profile to be built in v5 test session.]

Speed tiers: Adagio (80 BPM) / Moderato (96 BPM) / Allegro (112 BPM)

---

## MAIN MENU

Named genre: Pulp action demoscene synthwave
Status: [OPEN — v4.5 reference track Main_Menu_01 (72 BPM, 4/4, Dorian) is
a strong candidate but not confirmed on v5. Profile to be built after v5 test.]

Candidate profile notes from v4.5 analysis:
- Clean spectral separation (high-end not smeared)
- Three visible structural sections with density breathing
- Repeating horizontal banding in mid zone
- Occasional vertical transients as rhythmic arrival points
- Warm but not bass-dominant (lower priority than Crucible)

---

## RIFT NEUTRAL

Named genre: Cold constructed demoscene synthwave
BPM: 72 | Time sig: 4/4 | Mode: Minor pentatonic
Status: [OPEN — prompt not yet drafted. Profile to be built after first v5 test.]

Expected profile direction:
- COLD dominant across all zones — this is a waiting/holding-breath track
- Sub-bass: WARM (present but restrained)
- Mid: COLD with occasional STRUCTURED events (sparse phrase arrivals)
- High: COLD — minimal hi-hat content
- Structural: flat energy is acceptable here — this is an ambient/tension track,
  not a driving groove

---

## DREAMING

Named genre: Warm cozy analog synthwave
BPM: 70 | Time sig: 4/4 | Mode: Dorian
Status: [OPEN — no v5 test yet. Profile to be built after first v5 test.]

Expected profile direction (inverse of Crucible):
- Bass: WARM not HOT — not bass-dominant
- Mid: WARM + STRUCTURED — call-and-response melody visible as alternating bands
- High: WARM — no tape saturation harshness
- Air: present — unlike Crucible, this track has air
- Structural: gentle variation, no hard density drops

---

## TOWER AMBIENT

Named genre: Industrial action demoscene synthwave
BPM: 72 | Time sig: 3/4 | Mode: Minor
Status: [OPEN — prompt needs v5 test. Profile to be built after first v5 test.]

---

## MAINTENANCE PANEL (Refueling / Coolant / Waste)

Named genre: Industrial mechanical ambient
Status: [OPEN — all three tracks deferred to v5 session.]

Expected profile direction by track:
- Refueling: HOT bass, WARM mid, STRUCTURED rhythm — most hospitable
- Coolant: COLD with STRUCTURED high-frequency texture — precision not dread
- Waste: COLD dominant, LOW register only, SPARSE — ugliest track in game

---

## VOID

Named genre: Dark ambient drone synthwave
BPM: 62 | Mode: None (drone only)
Status: [OPEN — Suno vs Mubert decision pending.]

Expected profile direction:
- Sub-bass: HOT (sub-bass pulse is the primary content)
- All other zones: COLD to near-black
- Structural: FLAT is correct — no phrase periodicity, no arrangement arc
- Air: absent

---

## FORAGING MINIGAME

Status: [OPEN — dance style TBD, mechanic unconfirmed. Cannot profile until
dance style and BPM are locked.]

