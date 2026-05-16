---
name: life-core-eve-online
description: >
  Advises on EVE Online activity selection, session routing, ISK strategies,
  and training priorities for pilot Semibarbaric — an Alpha clone (permanent, no Omega sub),
  4.93M SP, Gallente drone specialist, early-game ISK-building phase. Routes every
  recommendation through a time-budget filter and ISK availability gate before
  surfacing activities. Use automatically — do not wait to be asked. Trigger on
  ANY of these signals: "what should I do in EVE", "EVE session", "EVE Online",
  "what should I fly", "ISK per hour", "EVE time budget", "what activity fits
  my time", "what should I train", or any question about EVE Online activities,
  income methods, PvP content, training priorities, or session planning. Do NOT
  trigger for: CCP news, EVE subscription decisions, game installation, or
  general gaming questions unrelated to in-game session strategy.
  Load once per session.
---
SKILL_VERSION: 1.8

# EVE Online Activity Advisor — Semibarbaric

Scope: Alpha clone (permanent — no Omega sub), 4.93M SP, Gallente drone specialist, early-game ISK-building phase. All recommendations must be Alpha-viable. Never recommend Omega-gated content. Always confirm session length and check ISK ladder before recommending any activity.

---

## PLAYER PROFILE

| Dimension | Confirmed value |
|---|---|
| Clone state | **Alpha — permanent, intentional. No Omega sub. All recommendations must be Alpha-viable.** |
| SP | 4,932,912 (58,509 unallocated — inject into Alpha-eligible skills only; ~67k SP before hitting 5M Alpha cap) |
| ISK | ~4.3M — critical constraint |
| Corporation | CAS (NPC starter corp — no SRP, no fleet infrastructure) |
| Combat system | Drones — Light Drone Op L5, Medium Drone Op L4, Drone Interfacing L3, Drone Avionics L4, Drone Durability L4, Drone Navigation L4, Drone Sharpshooting L4; Heavy Drone Op L2; Repair Drone Op L2 |
| Ships available | Gallente Frigate L4, Gallente Destroyer L4, Gallente Cruiser L4, Mining Frigate L3, Gallente Hauler L1, Caldari Frigate L1, Caldari Destroyer L1, Caldari Hauler L1 |
| Specific hulls | Imicus (exploration), Tristan (PvP frigate), Algos (drone destroyer), Vexor (drone cruiser), Venture (mining), Iteron Mk V (hauler) |
| Tank options | Both — Armor core L5 (Hull Upgrades, Mechanics, Repair Systems); Shield core L4 (Shield Management, Shield Operation, Shield Upgrades, Shield Compensation, Tactical Shield Manipulation all L4) |
| Exploration | Fully functional — Hacking L4, Archaeology L4, Astrometrics L3, Survey L3, Astrometric Acquisition L2, Astrometric Rangefinding L2 |
| Targeting | Target Management L4 (up to 8 locks), Signature Analysis L4 (fast lock), Long Range Targeting L3 |
| Fitting | Power Grid Management L5, Weapon Upgrades L5, CPU Management L4, Energy Grid Upgrades L3, Electronics Upgrades L2 |
| Navigation | Navigation L4, Afterburner L4, Acceleration Control L3, High Speed Maneuvering L3, Warp Drive Operation L3, **Evasive Maneuvering L3** |
| Engineering | Capacitor Management L3, Capacitor Systems Operation L3, Capacitor Emission Systems L1 |
| Weapon gap | Small Hybrid Turret L2 only — turrets are backup; Missile Launcher Op L1 — effectively zero |
| Drone Interfacing | **L3** — confirmed. L3→L4 costs 186,275 SP; post-cap injection priority |
| SoE Epic Arc | Unknown — verify completion status; repeatable every 90 days |
| Space access | NPC corp — highsec and lowsec accessible; null requires corp invite |
| Platform | Steam Deck OLED — trackpad + touchscreen only, no physical keyboard |
| Gas Cloud Harvesting | L0 — skillbook not purchased; gas huffing blocked until bought and trained |

**Character identity:** Deliberate Gallente drone specialist with a functional exploration secondary. Skills are not the bottleneck — asset state and input precision are.

**Progression ceiling (NPC corp):** CAS membership blocks: null ratting (sov access required), organized SRP, serious WH operations with corp backup, and null exploration staging. The ceiling becomes material at Rung 2+. When wallet reaches Rung 2 stability, evaluate joining a player corp with WH or null infrastructure — this unlocks the next income tier without requiring additional SP investment.

---

## STEAM DECK PLATFORM

EVE runs on Steam Deck via Proton with a community Steam Input layout (trackpad as mouse). This is the primary hardware constraint on activity selection — precision and reaction time are meaningfully reduced vs keyboard/mouse.

**Setup prerequisites (one-time):**
- Install community Steam Input layout: search "EVE online config" by Dman990099 in Steam Input browser
- Set EVE UI scale to 125–150% (Escape → Display & Graphics → UI Scale) — default UI is unreadably small at 1280×800
- Run in **Windowed mode, not fullscreen** — required to enable touchscreen input
- Battery life running EVE: approximately 2–4 hours — plan sessions near power for anything over 90 minutes

**Touchscreen use:**
EVE's Photon UI supports direct finger taps in windowed mode. Touchscreen is faster than trackpad for static UI interactions: market windows, mission accept/complete, docking prompts, warp target selection from overview, drone menu. Reserve the trackpad for in-space positional clicking only.

**Back button bindings (L4/L5/R4/R5):**
The four Steam Deck back buttons should be bound to high-frequency EVE actions to free the trackpad for in-space use. Useful bindings: lock nearest target (Ctrl+LMB equivalent), drone engage/return, toggle module group. Verify defaults in the Dman990099 layout before rebinding — the layout updates and current binds should be confirmed in-client.

**Window layout for Deck resolution:**
At 1280×800 the default PC window layout is unworkable. Compact setup: collapse all non-essential panels; run overview + local chat as narrow stacked columns pinned to the right edge; detach probe scanner and minimize when not scanning; keep capacitor/module bar centered. This is one-time configuration — worth doing before any active session.

**Activity trackpad viability ratings (1 = hardest, 5 = easiest):**

| Activity | SD Rating | Key constraint |
|---|---|---|
| Mining / Venture | 5 | Set and forget — minimal clicks once running |
| Market orders | 5 | Pure UI navigation — trackpad fine |
| L1–L3 Missions | 4 | Slow NPC AI, forgiving timing |
| Highsec anomaly ratting | 4 | Lock, deploy drones, orbit — low precision needed |
| Exploration hacking minigame | 3 | Small node targets require careful trackpad sensitivity tuning |
| Homefront Operations | 3 | NPC combat + fleet coordination — manageable |
| Abyssals (Algos/Vexor) | 2 | Fixed 20-min timer, real-time drone management, precision maneuvering |
| FW plexing (active PvP) | 1 | PvP reaction time is the bottleneck — trackpad disadvantage is material; budget for higher ship loss rate |

**Rules for Steam Deck recommendations:**
- Always include the SD Rating for the recommended activity.
- For any activity rated SD 1–2: warn that input precision is a material disadvantage and budget ship losses accordingly.
- For Abyssals specifically: recommend starting in docked safety by running the fitting simulator before the first live run to confirm the Vexor controls are mapped intuitively.
- Never recommend an activity rated SD 1 as a first-session activity in a new content type.

---

## SESSION STATE

Update this when: wallet crosses a rung threshold, a ship is lost or fitted, filaments are consumed, or a major sale occurs. Stale by more than one session — ask before routing.

| Field | Current value |
|---|---|
| Wallet ISK | ~4.3M |
| Total assets (Janice est.) | ~26.3M |
| Effective rung | 2 — Vexor owned (activity access gates on ship ownership, not ISK threshold; total assets ~26.3M falls between Rung 1 and 2 by value, but Vexor possession unlocks the T1 Abyss activity path); needs Medium Shield Booster I (~100k) to complete fit |
| Ships fitted and ready | Imicus x2 (exploration), Tristan (FW), Venture (mining), Iteron Mk V (hauler) |
| Ships unfitted | Vexor — one module from Abyss-ready |
| Filaments held | Tranquil Electrical x1 (T0 Tranquil — entry-tier Vexor run; verify in-game item name before running. Calm = T1, Tranquil = T0 — different tiers) |
| Key pending action | Buy Medium Shield Booster I → fit Vexor → run Tranquil Electrical filament |
| Notable asset | Shadow Serpentis Small Armor Repairer — check Janice, likely 15–50M+ |
| Last updated | 2026-05-06 |

---

## ISK LADDER

Check this before every recommendation. Never recommend above the current rung.

| Rung | ISK threshold | Ship unlocked | Primary activity |
|---|---|---|---|
| 0 — Now | 4.3M current | Fitted Imicus (~2–3M) | Highsec relic/data exploration |
| 1 — Near | 8–12M | Fitted Algos (~5–10M) | FW medium plexes, lowsec exploration, ghost sites (Algos) |
| 2 — Mid | 40–60M | Fitted Vexor (~25–40M) | T1–T2 Abyss (cruiser filaments), sustained income loop |
| 3 — Stable | 100M+ | Vexor Navy Issue (verify Alpha eligibility — Navy ships below BS size are listed as Alpha-accessible per E-UNI; confirm in-client before routing) | T2 Abyss, serious FW engagement |

Rung is determined by **total asset value**, not wallet ISK alone — fitted ships, filaments, and sellable modules all count. Always check SESSION STATE before routing. Wallet ISK alone understates the true position.

When ISK is insufficient for the best option, name the shortfall and route to the fastest activity to close it.

---

## PROPERTIES

**PRE — Run before every recommendation**
1. Confirm session length — ask if absent.
2. Confirm goal: ISK focus, PvP, low-attention, or open.
3. Check SESSION STATE — if last updated more than one session ago, or if user mentions a recent sale, loss, or purchase, ask for current wallet ISK and ship status before routing.
4. Determine ISK Ladder rung from total assets (SESSION STATE), not wallet ISK alone.
5. Confirm location if routing to lowsec/null content.
6. **NEVER state an ISK/hr figure without running a web search confirming it in the current session.** Figures in this skill are estimates for routing only — market conditions shift. If no web search has been run this session, run it before stating any number. Citing stored estimates without searching is a hard fail.

**MFT — Mandatory output format**

```
RECOMMENDATION: [Activity — specific hull name]
SESSION FIT:    [Fits / Tight / Does not fit — with reason]
ISK TIER:       [Low / Medium / High — range, web-verified]
RISK:           [Low / Medium / High — specific exposure]
SOLO:           [Yes / No / Optional]
ISK GATE:       [Rung N — cost and current wallet]
SD RATING:      [1–5 — trackpad viability; warn if 1–2]
TRAIN NEXT:     [One skill that improves this activity — only if relevant]
REFERENCE:      [E-UNI wiki URL]
```

**INV — Never violate**

| Rule | Reason |
|---|---|
| Never recommend a ship the current ISK cannot cover | 4.3M wallet — ship loss ends the run |
| Never recommend turret-primary fits | Small Hybrid Turret L2 is backup only |
| Never recommend missile ships | Missile Launcher Operation L1 — not viable |
| Never recommend capitals or T3 hulls | T3 strategic cruisers require Omega — not accessible on Alpha |
| Never state ISK/hr without web-verifying first | Values shift with patches and market |
| Always name the specific Gallente hull | Generic advice is useless at this character state |

**DIR — Behavioral defaults**

- Lead every recommendation with the specific hull name (Imicus, Algos, Vexor).
- When ISK gate blocks the best option, name the gap and route to the fastest path to close it.
- FW recommendations must specify plex size — Algos cannot enter small plexes (medium and above only).
- When training would meaningfully improve a recommended activity, name the skill and the gain.

---

## TIME BUDGET ROUTER

| Session length | Viable now | Avoid |
|---|---|---|
| 15–30 min | FW medium plex (1 plex, 10–20 min), FW defensive plex, market orders, Vexor Abyssal T1 (1 run — cruiser filament only, not destroyer) | Exploration (travel overhead), null (transit), Algos Abyss (destroyer filaments require 2-filament fleet design — not reliable solo) |
| 45–90 min | Highsec exploration chain (4–6 relic sites), FW plexing session, Vexor Abyssal chain (2–3 runs) | WH exploration (nav overhead), NPSI fleets (too short) |
| 2hr+ | All viable activities — rank by efficiency for goal; SoE Epic Arc fits here | N/A |

---

## DECISION ENGINE

1. Confirm session length. Ask if absent — do not skip.
2. Confirm goal: ISK, PvP, low-attention, or open.
3. Check SESSION STATE for current rung. If stale or user mentions a recent change, ask for updated wallet and ship status before proceeding. Rung is set by total asset value, not wallet alone.
4. Apply Time Budget Router — eliminate time-incompatible activities.
5. Consult the ACTIVITY MATRIX section below — select top match.
6. Apply MFT format: hull name, ISK gate, one training note if relevant.
7. Web-search ISK/hr before presenting any figures.

---

## TRAINING PRIORITY

Surface when asked "what should I train?" Proactively surface the top relevant skill when making an activity recommendation.

| Priority | Skill | Current | Alpha Max | SP Cost | Notes |
|---|---|---|---|---|---|
| 1 | Drone Interfacing | L3 | L4 | 186,275 SP | Post-cap injection — highest DPS gain available on Alpha |
| 2 | Medium Drone Operation | L4 | L5 | 421,490 SP | Post-cap injection — unlocks full damage ceiling |
| 3 | Capacitor Management | L3 | L4 | 111,765 SP | Post-cap injection — improves all combat |
| 4 | Propulsion Jamming | L2 | L4 | 19,755 SP to L3 | Only skill in this list that fits in remaining ~67k free training |

**Skills at Alpha cap — do not queue, Omega required for further training:**
- Evasive Maneuvering L3 (Alpha max L3) — shown as Omega-locked in client
- Astrometrics L3 (Alpha max L3)
- Astrometric Acquisition L2 (Alpha max L2)
- Astrometric Rangefinding L2 (Alpha max L2)
- Warp Drive Operation L3 (Alpha max L3)
- Afterburner L3 Alpha max, trained to L4 as Omega — L4 now INACTIVE
- Gallente Cruiser L4 (Alpha max L4) — already at cap, L5 requires Omega

**Skills trained above Alpha cap (Omega-era, now inactive):**
Hacking L4 (max L3), Archaeology L4 (max L3), Afterburner L4 (max L3), Signature Analysis L4 (max L3), Remote Armor Repair Systems L4 (max L3), Remote Hull Repair Systems L4 (max L2), Astronautics Rigging L4 (max L3) — these skills function at their Alpha cap level only.

Never recommend training missiles or turrets — the drone path is invested and the correct specialization for this character.

---

## EXAMPLES

**Example 1 — 30 min, ISK, Rung 0 (4.3M ISK)**

User: "30 minutes, want ISK."

```
RECOMMENDATION: Highsec relic exploration — Imicus
SESSION FIT:    Fits — interruptible between sites, no timer pressure
ISK TIER:       Low-Medium — 10–30M/hr highsec; web-verify loot prices
RISK:           Very Low — highsec, minimal PvP exposure
SOLO:           Yes
ISK GATE:       Rung 0 — fitted Imicus ~2–3M, within current 4.3M wallet
SD RATING:      3 — hacking minigame requires trackpad precision; tune sensitivity before first run
TRAIN NEXT:     Astrometrics L4 — faster scanning = more sites per session
REFERENCE:      https://wiki.eveuniversity.org/Exploration
```

**Example 2 — 2 hrs, PvP + ISK, Rung 1 (12M ISK)**

User: "2 hours, want to fight and make money."

```
RECOMMENDATION: Faction Warfare medium plexing — Algos
SESSION FIT:    Fits — each plex 10–20 min, dock freely between
ISK TIER:       Medium — LP conversion dependent; web-verify LP store prices
RISK:           High — PvP exposure constant; budget fit essential, expect losses
SOLO:           Yes
ISK GATE:       Rung 1 — fitted Algos ~5–10M; confirm wallet clears this
SD RATING:      1 — active PvP on trackpad is hardest content; budget for higher loss rate
TRAIN NEXT:     Propulsion Jamming L3 — improves tackle range; fits in remaining ~67k free SP
REFERENCE:      https://wiki.eveuniversity.org/Faction_warfare
```
FW NPC meta change (Nov 2025): drone ships hold position well under new NPC behavior. Use medium plexes only — Algos cannot enter small plexes.

**Example 3 — 15 min, ISK, Rung 0, not enrolled in FW**

User: "15 minutes, want ISK, not in FW."

```
RECOMMENDATION: Highsec relic exploration — Imicus
SESSION FIT:    Fits — one or two sites possible in 15 min; interruptible at any point
ISK TIER:       Low-Medium — 10–30M/hr highsec; web-verify loot prices
RISK:           Very Low — highsec, minimal PvP exposure
SOLO:           Yes
ISK GATE:       Rung 0 — fitted Imicus ~2–3M, within current wallet
SD RATING:      3 — hacking minigame requires trackpad precision
TRAIN NEXT:     Astrometrics L4 — faster scanning = more sites per session
REFERENCE:      https://wiki.eveuniversity.org/Exploration
```
Note: FW plexing requires militia enrollment and travel to FW space — not viable for a 15-min session from a non-FW staging location.

User: "Can I run L4 missions?"

Response: Alpha clones cannot accept L4 or L5 missions — this is a hard game restriction, not a standing issue. L3 missions are the highest accessible level. L3 access requires standing 5 with a specific agent corp, which takes weeks of L1–L2 grinding from zero. At current character state, Abyssal T1 or exploration provides better ISK with no standing gate. L3 missions become a secondary income path once the Vexor is fitted and standings are developed alongside it.

---

## SKILL INVENTORY

Complete individual skill list confirmed from in-game screenshots (April 2026). Alpha max levels confirmed from official Alpha clone skill list. Skills marked ⚠ are trained above Alpha cap and are INACTIVE until Omega resub.

**ARMOR**
Hull Upgrades L5 (max L5), Mechanics L5 (max L5), Repair Systems L5 (max L5), Remote Armor Repair Systems L4 ⚠ (max L3 — inactive), Remote Hull Repair Systems L4 ⚠ (max L2 — inactive), EM/Explosive/Kinetic/Thermal Armor Compensation L2 (max L2 — at cap)

**DRONES**
Drones L5 (max L5), Light Drone Operation L5 (max L5), Medium Drone Operation L4 (max L5 — **can train**), Drone Avionics L4 (max L4), Drone Durability L4 (max L4), Drone Navigation L4 (max L4), Drone Sharpshooting L4 (max L4), **Drone Interfacing L3 (max L4 — can train, 186k SP)**, Heavy Drone Operation L2 (max L4 — can train), Repair Drone Operation L2 (max L2 — at cap)

**ELECTRONIC SYSTEMS**
Propulsion Jamming L2 (max L4 — **can train**), Electronic Warfare L1 (max L4 — **can train**)

**ENGINEERING**
Power Grid Management L5 (max L5), Weapon Upgrades L5 (max L5), CPU Management L4 (max L5 — can train), Capacitor Management L3 (max L4 — **can train, 112k SP**), Capacitor Systems Operation L3 (max L3 — at cap), Energy Grid Upgrades L3 (max L5 — can train), Electronics Upgrades L2 (max L5 — **can train**)

**FLEET SUPPORT**
Leadership L1 (max L3 — can train)

**GUNNERY**
Gunnery L4 (max L5), Motion Prediction L2 (max L4), Rapid Firing L2 (max L4), Controlled Bursts L2 (max L4), Sharpshooter L2 (max L4), Small Hybrid Turret L2 (max L5), Surgical Strike L1 (max L4), Trajectory Analysis L1 (max L4)

**MISSILES**
Missile Launcher Operation L1 (max L5)

**NAVIGATION**
Navigation L4 (max L4 — at cap), Afterburner L4 ⚠ (max L3 — inactive), Acceleration Control L3 (max L3 — at cap), High Speed Maneuvering L3 (max L3 — at cap), Warp Drive Operation L3 (max L3 — at cap), **Evasive Maneuvering L3 (max L3 — at cap, Omega to advance)**

**NEURAL ENHANCEMENT**
Biology L3 (max L3 — at cap), Cybernetics L3 (max L3 — at cap), Infomorph Psychology L1 (max L1 — at cap)

**PRODUCTION**
Industry L4 (max L5 — can train), Mass Production L2 (max L3 — can train), Advanced Industry L1 (not on Alpha list)

**RESOURCE PROCESSING**
Mining L4 (max L4 — at cap), Mining Upgrades L3 (max L4 — can train), Reprocessing L3 (max L3 — at cap), Salvaging L3 (max L3 — at cap)

**RIGGING**
Astronautics Rigging L4 ⚠ (max L3 — inactive), Armor Rigging L3 (max L3 — at cap), Drones Rigging L3 (max L3 — at cap), Energy Weapon Rigging L3 (max L3 — at cap), Hybrid Weapon Rigging L3 (max L3 — at cap), Jury Rigging L3 (max L3 — at cap), Shield Rigging L3 (max L3 — at cap), Electronic Superiority Rigging L3 (max L3 — at cap)

**SCANNING**
Archaeology L4 ⚠ (max L3 — inactive), Hacking L4 ⚠ (max L3 — inactive), Astrometrics L3 (max L3 — at cap), Survey L3 (max L3 — at cap), Astrometric Acquisition L2 (max L2 — at cap), Astrometric Rangefinding L2 (max L2 — at cap)

**SCIENCE**
Science L4 (max L4 — at cap)

**SHIELDS**
Shield Compensation L4 (max L4), Shield Management L4 (max L4), Shield Operation L4 (max L4), Shield Upgrades L4 (max L4), Tactical Shield Manipulation L4 (max L4), Shield Emission Systems L3 (max L3 — at cap), EM/Explosive/Kinetic/Thermal Shield Compensation L2 (max L2 — at cap)

**SOCIAL**
Diplomacy L3 (max L3 — at cap), Social L3 (max L3 — at cap), Connections L2 (max L2 — at cap), Criminal Connections L2 (max L2 — at cap), Negotiation L2 (max L2 — at cap)

**SPACESHIP COMMAND**
Spaceship Command L4 (max L4 — at cap), Gallente Frigate L4 (max L4 — at cap), Gallente Destroyer L4 (max L4 — at cap), Gallente Cruiser L4 (max L4 — **at cap, L5 requires Omega**), Mining Frigate L3 (max L4 — can train), Gallente Hauler L1 (max L1 — at cap), Caldari Frigate L1 (max L4 — can train), Caldari Destroyer L1 (max L4 — can train), Caldari Hauler L1 (max L1 — at cap)

**TARGETING**
Target Management L4 (max L4 — at cap), Signature Analysis L4 ⚠ (max L3 — inactive), Long Range Targeting L3 (max L3 — at cap)

**TRADE**
Trade L3 (max L3 — at cap), Broker Relations L2 (max L2 — at cap), Marketing L2 (max L2 — at cap)

---

## CURRENT EVENTS

**Capsuleer Day XXIII — Warpath (active April 30–June 2, 2026)**
Alpha login track: up to **140,000 SP** total (Omega track adds 525,000 more but is not accessible). Seasonal challenge track adds up to 75,000 SP. Log in daily — check the current daily reward on the Capsuleer Day XXIII login calendar in-client. Warpath combat sites appear in highsec at frigate/destroyer scale and are directly playable by this character.
Reference: https://wiki.eveuniversity.org/Capsuleer_Day_XXIII

Always check for active events before a session — CCP runs major events every 4–6 weeks, most give 100k–200k free SP on login tracks.

---

## SP PROGRESSION

**Alpha clone — permanent state. No Omega sub. Do not recommend Omega as a path.**

Free training runs until the 5M SP cap. Character is at 4,932,912 SP — approximately 67k SP of free training remaining (58,509 already unallocated).

**Correct queue to hit 5M cap (all Alpha-verified):**
1. Propulsion Jamming L3 — 19,755 SP — completes (Alpha max L4)
2. Electronics Upgrades L3 — 13,170 SP — completes (Alpha max L5)
3. Electronic Warfare L3 — 15,500 SP total (L1→L3) — completes (Alpha max L4)
4. Capacitor Management L4 — 111,765 SP needed, only ~18,575 SP remaining — partially trains, hits 5M cap

After hitting 5M cap:
- Unallocated SP (from AIR rewards, login tracks, etc.) can still be injected into Alpha-eligible skills — up to 20M total (AIR Daily Goals can push beyond)
- **Do NOT inject unallocated SP before hitting the 5M cap** — it counts against free training headroom. Train to cap first, then inject.
- Daily Alpha Injectors (DAI) add 50,000 SP/day, purchasable on market for ISK. Web-verify current DAI price before recommending.
- All training must stay within the Alpha skill set. Omega-locked skills cannot be trained or used.

**CRITICAL Alpha cap rules — verify before EVERY training recommendation:**
- Never recommend training a skill that is already at its Alpha max level
- Never recommend training a skill level that requires Omega (these appear with Ω lock icon in client)
- Check SKILL INVENTORY alpha max column before recommending any skill
- Skills confirmed at Alpha cap (Omega required to advance): Evasive Maneuvering, Astrometrics, Astrometric Acquisition, Astrometric Rangefinding, Warp Drive Operation, Acceleration Control, High Speed Maneuvering, Navigation, Gallente Cruiser, and all skills marked "at cap" in SKILL INVENTORY
- L4 missions: **Alpha clones cannot accept L4 or L5 missions.** Do not route to L4 missions under any circumstances.

---

## ACTIVITY MATRIX

Full activity details: See [references/activity-matrix.md](references/activity-matrix.md)

Quick reference (hull, rung, SD rating):

| Activity | Rung | Hull | Session | ISK tier | SD |
|---|---|---|---|---|---|
| Highsec relic exploration | 0 | Imicus | Any | Low-Med | 3 |
| FW wreck scavenging | 0 | Imicus | 30min+ | Variable | 4 |
| Battle salvaging | 0 | Catalyst | 30min+ | Variable | 4 |
| Ore mining | 0 | Venture | 60min+ | Very Low | 5 |
| Gas huffing (K-space Mykoserocin) | 0 | Venture | Any | Low-Med | 5 |
| SoE Epic Arc (if unrun) | 0–1 | Algos | 2–4hr | Low (standing gain primary) | 4 |
| Event sites (Warpath) | 0 | Imicus/Algos | Any | Low (SP value) | 3 |
| FW defensive plexing | 0 | Tristan | Any | Low | 4 |
| FW small plexes (offensive) | 1 | Tristan | Any | Low-Med | 1 |
| FW medium plexes (offensive) | 1 | Algos | Any | Medium | 1 |
| Ghost sites (highsec) | 1 | Algos | 30min+ | Variable | 3 |
| Homefront Operations | 1 | Algos/Vexor | 45min+ | Medium | 3 |
| Lowsec/null exploration | 1 | Imicus | 45min+ | Med-High | 3 |
| Algos Abyss (⚠ fleet-designed) | 1 | Algos ×2 | 15–30 min | Medium | 2 |
| T1-T2 Abyss (cruiser) | 2 | Vexor | 15–30 min | Med-High | 2 |
| Highsec anomaly ratting | 1–2 | Algos/Vexor | 30min+ | Low | 4 |
| L3 missions (with standing) | 2 | Vexor | 30min+ | Low-Med | 4 |
| DED sites | 2 | Vexor | 30–60 min | Med-High | 3 |
| Gas huffing (WH Fullerites) | 0 | Venture | 15–30 min | Med-High | 2 |


| Topic | URL |
|---|---|
| Exploration | https://wiki.eveuniversity.org/Exploration |
| Abyssals | https://wiki.eveuniversity.org/Abyssals |
| Faction Warfare | https://wiki.eveuniversity.org/Faction_warfare |
| Homefront Operations | https://wiki.eveuniversity.org/Homefront_operation |
| Ratting | https://wiki.eveuniversity.org/Ratting |
| Missions | https://wiki.eveuniversity.org/Missions |
| Wormholes | https://wiki.eveuniversity.org/Wormholes |
| Imicus | https://wiki.eveuniversity.org/Imicus |
| Algos | https://wiki.eveuniversity.org/Algos |
| Vexor | https://wiki.eveuniversity.org/Vexor |
| Magic 14 skills | https://wiki.eveuniversity.org/Magic_14 |

| Tool | Use |
|---|---|
| Janice | Loot valuation — https://janice.e-351.com/ |
| Eve Tycoon | Trade tracking — https://evetycoon.com/ |
| zKillboard | PvP records — https://zkillboard.com/ |
| Dotlan | Maps/routes — https://evemaps.dotlan.net/ |

---

## META PATCH PROTOCOL

Always web-search before stating: ISK/hr benchmarks, FW LP store prices, Abyssal filament costs, relic/data loot values.

Stable — no search needed: mechanic descriptions, ship class access, general risk profiles.

FW flag: NPC behavior in plexes changed November 2025. Drone boats hold position well under new NPC spread/disruptor behavior. Verify current meta before recommending specific fits.

FW flag (unverified): EVE Online Version 23.03 releases from 2026-02-25 and 2026-04-16 may have changed FW mechanics (LP values, plex eligibility, or ship restrictions). E-UNI FW wiki flagged for update. Web-search FW patch notes before recommending specific LP store arbitrage or plex ship class eligibility.

---

## Out of Scope

This skill does NOT:
- Provide ship fitting theory — use Pyfa or E-UNI ship pages
- Cover EVE lore, CCP news, or subscription pricing
- Cover Planetary Industry — no PI skills trained (0/5)
- Cover Incursions — require specific fleet comps, not viable from NPC corp
- Cover null ratting — requires player corp sov access

---

## SEE ALSO

| Resource | Domain |
|---|---|
| EVE University Wiki | Mechanics reference — https://wiki.eveuniversity.org |
| life-core-fitness | Personal fitness — not EVE-specific |
| life-core-boxing | Boxing training — not EVE-specific |
