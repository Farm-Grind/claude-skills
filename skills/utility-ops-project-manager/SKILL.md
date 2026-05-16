---
name: utility-ops-project-manager
description: >
  Manages solo creative projects from concept to production — games, comics, novels, or
  any multi-phase creative work. Handles phase planning, WBS decomposition, milestone
  definition, sprint scoping, task queue management, MoSCoW scope control, and
  velocity-based scheduling. Eliminates "what do I work on next?" by maintaining a
  pre-decided, dependency-ordered task queue. Use automatically — do not wait to be
  asked. Trigger on ANY of these signals: "start a new project", "plan this out", "stuck
  on what to do next", "scope this", "break this down", "what's my next task", "I need
  milestones", "not making progress", "help me plan my game / novel / comic", "how long
  will this take", "losing focus", "scope creep", "what phase am I in", "set up a
  sprint", "what should I work on today". Do NOT trigger for: in-session design or
  writing work, lore creation, coding, or research. Load once per session.
---
SKILL_VERSION: v1.0

# Managing Creative Projects

Structures solo creative projects from first idea to shipped product. Eliminates
the two failure modes that kill solo work: not knowing what to do next, and
accumulating scope that never closes.

The universal phase model below applies to any creative domain. Domain-specific
equivalents are in `references/domain-phases.md`.

---

## PART 1 — SESSION ENTRY PROTOCOL

When triggered, run this diagnostic before doing anything else.

**Ask (batch into one message, never sequence):**
1. Is this a new project or an in-progress one?
2. What is the output type? (game / novel / comic / other — describe)
3. What is the approximate scale? (jam-scale weekend / short-form 1–3 months / mid-scale 3–12 months / long-form 1+ year)
4. Is there a fixed external deadline? If yes, what is it?

If the project is already in progress, also ask:
- What phase are you currently in?
- What was the last completed milestone?
- What is the current task queue state? (full / partial / empty / nonexistent)

**Do not proceed to Phase Selection until these are answered.**

---

## PART 2 — THE UNIVERSAL PHASE MODEL

Every creative project moves through these phases in order. Phases cannot be skipped;
they can be compressed for small-scale work. Each phase has a defined entry condition
and an exit gate.

```
PHASE 0: CONCEPT
  Entry: An idea exists.
  Work:  Ideation, initial scope statement, "why this project" statement.
  Exit gate: Core concept locked in one paragraph. Audience defined. Purpose defined.

PHASE 1: PROTOTYPE / PROOF-OF-CONCEPT
  Entry: Concept locked.
  Work:  Answer "should I make this?" — fast, disposable, not reusable.
         Test assumptions. Validate the core mechanic/premise/visual language.
         Domain equivalents: see references/domain-phases.md
  Exit gate: Core assumptions validated or invalidated.
             If invalidated → return to Phase 0 with new data.
             If validated → proceed.

PHASE 2: VERTICAL SLICE / PILOT
  Entry: Prototype validated.
  Work:  Answer "can I make this?" — one small segment brought to near-final quality.
         Calibrates pipeline speed. Sets the quality ceiling. Surfaces unknown unknowns.
         This is the production prototype, not a design prototype.
         Domain equivalents: see references/domain-phases.md
  Exit gate: One complete segment exists at target quality.
             Time-per-unit estimate established (e.g., hours per chapter / per page / per level).
             Full project timeline can now be calculated from this rate.

PHASE 3: PRE-PRODUCTION
  Entry: Vertical Slice complete.
  Work:  Full WBS (see Part 3). MoSCoW triage. Calendar built from velocity data.
         Feature/content lock date established. All Must-Haves defined.
  Exit gate: WBS complete. Sprint 1 queue filled. Feature lock date set.
             No production work begins until this gate clears.

PHASE 4: PRODUCTION (FEATURES FIRST)
  Entry: Pre-Production complete.
  Work:  Build all Must-Have structural features/systems/mechanics before filling content.
         Rule: features before content. Structure before population.
         Sprint-based with defined queue at all times.
  Exit gate: Feature Complete — all structural elements exist and function.
             Nothing new can be added. What is here is what ships.

PHASE 5: PRODUCTION (CONTENT FILL)
  Entry: Feature Complete.
  Work:  Fill all content units. All content items are plannable and safe to estimate.
  Exit gate: Content Complete — everything present from start to finish.
             External review / playtesting / beta read begins here.

PHASE 6: POLISH & WRAP
  Entry: Content Complete.
  Work:  Feedback integration, bug fixes, polish passes. No new features or content.
         Feature lock is absolute from Phase 4 forward.
  Exit gate: Release Candidate — stable, complete, shippable build.

PHASE 7: RELEASE & CLOSE
  Entry: Release Candidate approved.
  Work:  Ship. Post-mortem (required). Archive project state.
  Exit gate: Post-mortem complete. Learnings documented for next project.
```

**Critical rule — Features Before Content:**
In Phase 4, lock all structural elements before populating them with content.
For a novel: lock plot structure before writing all scenes.
For a comic: lock panel layouts and visual language before all pages.
For a game: lock all mechanics before building all levels.
Breaking this produces rework.

---

## PART 3 — WORK BREAKDOWN STRUCTURE (WBS)

Runs during Pre-Production (Phase 3). Must be complete before any Production work.

### Step 1 — Define the top-level deliverable

State the project in one sentence: "A complete [type] that [does/achieves X] for [audience]."
This is the root node of the WBS.

### Step 2 — Decompose to phases (Level 1)

List all Phases from the Universal Phase Model that apply to this project.
For compressed projects (jam-scale), phases may merge.

### Step 3 — Decompose to deliverables (Level 2)

For each Phase, list all distinct deliverables — outputs that will exist when the phase
is done. Deliverables are nouns (things), not actions (verbs).

100% Rule: The sum of Level 2 deliverables must account for 100% of the project scope.
Nothing extra, nothing missing.

### Step 4 — Decompose to work packages (Level 3)

Break each deliverable into work packages — the smallest trackable units.

**8/80 Rule:** Each work package should take 8–80 hours. If under 8 hours, it's too
granular to track; merge it. If over 80 hours, it's underdefined; break it further.
For solo creative work: tasks under 1 session are usually too small. Tasks with no
clear end in 2 weeks are too large and will become invisible.

Each work package must have:
- A clear deliverable (not an activity — "Chapter 3 first draft complete", not "work on chapter 3")
- An estimated size (hours or sessions)
- A dependency (what must be done before this can start)

### Step 5 — Identify dependencies and critical path

Order work packages by dependency. The critical path is the longest chain of dependent
tasks — this sets the minimum project duration regardless of effort.

---

## PART 4 — MOSCOW TRIAGE

MoSCoW is applied at each phase boundary, not once at project start. Priorities shift.

**Categories:**
- **Must** — Without this, the project fails or cannot be released. Non-negotiable.
- **Should** — High value. Project is significantly weaker without it. Include if possible.
- **Could** — Nice to have. Only included if Must and Should are complete with time left.
- **Won't (this time)** — Explicitly excluded from current scope. Logged for a future project.

**Resource allocation rule (enforce this):**
Assign approximate % of total effort to each category before work begins.
Recommended starting split for solo work: Must ≈ 60%, Should ≈ 25%, Could ≈ 15%.
If Must exceeds 70% of capacity: scope is too large. Cut Shoulds to Could or Won't.

**Scope creep defense:**
When a new idea arrives mid-project: assign it a MoSCoW category immediately.
If it's a Must → something else must become a Won't to preserve capacity.
If it's a Could → log it in the Won't bucket and move on.
New ideas do not enter the active sprint without a trade-off.

**Feature lock date:**
Set this at the end of Phase 3. After this date:
- No new Must or Should items can be added.
- Could and Won't items are frozen.
- Ideas go into a "next project" file, not the current backlog.

---

## PART 5 — VELOCITY-BASED SCHEDULING

Produces a calendar grounded in observed personal throughput, not wishful capacity.

### Step 1 — Establish velocity from Vertical Slice

After Phase 2, you know:
- Hours to produce one unit (page / chapter / level / scene / mechanic)
- Your actual session length and frequency

Velocity = units per session × sessions per week = units per week

### Step 2 — Project total units

From the WBS, count total units remaining in the project.

### Step 3 — Calculate raw timeline

Raw weeks = Total units ÷ Velocity

### Step 4 — Apply buffer

Add 20–30% to raw timeline for unknowns, life interruption, and rework.
Do not skip this. Projects without buffer always run late.

### Step 5 — Build the calendar

Work backward from the target completion date (or forward from now, whichever is binding).
Assign units to weeks. Mark phase boundary dates.
These become your milestones.

### Step 6 — Track and recalibrate

At the end of each sprint: compare actual output to planned output.
If actual < planned for 2 consecutive sprints: the velocity estimate is wrong.
Recalibrate. Do not assume the next sprint will be different without a structural change.

---

## PART 6 — SPRINT PLANNING & TASK QUEUE

The sprint solves "what do I work on next?" The answer must always be pre-decided before
the session starts, not figured out during it.

### Sprint structure (recommended defaults)

- Sprint length: 1–2 weeks (shorter for jam-scale, longer for long-form)
- Sprint capacity: 70% of available hours (reserve 30% for life)
- Sprint queue: ordered list of work packages for this sprint, dependency-sorted

### Sprint planning protocol (runs at start of each sprint)

1. Review previous sprint: what completed, what didn't, why.
2. Update WBS: mark completed items, re-estimate any that ran long.
3. Recalibrate velocity if needed.
4. Pull next work packages from WBS into sprint queue (Must-Haves first, dependency order).
5. Verify each item has a clear deliverable and is ≤ 80 hours.
6. Set sprint goal: one sentence describing what will exist at the end of this sprint.

### Daily session entry

The task for today is already decided. Open the sprint queue. Work the top item.
If blocked: move to the next item and log the blocker. Never spend session time
deciding what to work on.

### Backlog management

Three buckets only:
- **Sprint queue** — in-scope for this sprint, ordered
- **Project backlog** — all remaining work packages, ordered by phase and dependency
- **Parking lot** — ideas, Could/Won't items, future-project candidates

Nothing moves from Parking Lot to Sprint Queue without a sprint planning review.

---

## PART 7 — PHASE BOUNDARY REVIEWS

At the exit gate of every phase, run this before starting the next phase.

**Phase Boundary Review checklist:**
- Exit gate conditions — are all of them met? (Be honest. Partial credit is not passing.)
- WBS — update all completed items. Re-estimate anything that changed.
- MoSCoW — re-triage remaining backlog. Priorities shift at phase boundaries.
- Velocity — recalibrate from actual output vs. planned output in this phase.
- Calendar — update remaining milestone dates from new velocity data.
- Feature lock — is the lock date still valid? If the project is running late, lock earlier, not later.
- Scope — did any items enter the project without a trade-off? Remove them now.

If any exit gate condition is not met: the phase is not complete. Do not proceed.

---

## PART 8 — END-OF-PROJECT POSTMORTEM

Required. Run before archiving any project.

1. What was the original scope vs. what shipped? What changed and why?
2. What phase took the longest? Was that expected?
3. Where did velocity estimates break down? What caused it?
4. What did you do well that should be repeated?
5. What would you change about the process for the next project?
6. What's in the "next project" Parking Lot from this project?

Save the postmortem. Reference it when starting the next project of the same type.

---

## PART 9 — COLLABORATION MODE (OPTIONAL)

For projects with one additional collaborator:

- Assign work packages to individuals at WBS Level 3.
- Each person maintains their own sprint queue.
- Sync at phase boundaries only — not mid-sprint.
- Scope decisions (MoSCoW changes, feature lock) require both parties to agree.
- Log all decisions in writing — verbal agreements evaporate.

---

## PART 10 — LINEAR INTEGRATION

All task state lives in Linear. Claude reads and writes Linear directly via MCP.
Workspace: Managed Projects. Team: Creative Work. One project per creative project.

**Vocabulary mapping:** See `references/linear-vocab.md` for Linear ↔ skill term mapping.

### Session start — "what's next?" protocol

When the user asks what to work on, or starts a session on a project:
1. If the user names a project: query that project in Linear directly.
2. If no project is named and multiple active projects exist: ask which project before querying. Never guess.
3. Query Linear for the project's current In Progress issues (these are today's tasks).
4. If none in progress: query Todo issues sorted by priority, return the top item.
5. If the backlog is empty (no issues exist yet): do not return an empty result. Trigger the WBS decomposition protocol (Part 3) to build the initial backlog.
6. Report using the Project Status Report format below.
7. Never ask the user to consult Linear themselves — pull it and present it.

### Logging new tasks

When a new task, idea, or scope item comes up mid-session:
- Ask: is this Must / Should / Could / Parking lot?
- Create the issue in Linear with the correct priority and label.
- If it's a Must that would push scope: flag the trade-off before creating it.
- Confirm creation to the user with the issue identifier (e.g., CW-12).

### Pushing work

When the user says they can't get to something this sprint:
- Update the issue status to Backlog in Linear.
- Remove it from the current cycle if one is active.
- Confirm: "Pushed CW-[N] to backlog."
- Do not ask for a reason unless the user volunteers one.

### End-of-day quick-wins protocol

Run when the user asks for quick options, end-of-day tasks, or a choose-your-own menu.
1. Query Linear for all issues labeled quick-decision, quick-win, or quick-task
   that are in Backlog or Todo status, across all active projects.
2. Sort by: proximity to being needed by priority work first, then by size ascending.
3. Present as a tiered menu — do not flatten into one list:

```
END OF DAY — [date]
Pick something from any tier. Go longer if you want.

⚡ QUICK DECISIONS (≤5 min)
  [ ] CW-[N] [task name] — [project] — [why it matters now, one clause]
  [ ] CW-[N] [task name] — [project]

🎯 QUICK WINS (≤15 min)
  [ ] CW-[N] [task name] — [project] — [why it matters now, one clause]
  [ ] CW-[N] [task name] — [project]

🔧 QUICK TASKS (≤30 min)
  [ ] CW-[N] [task name] — [project] — [why it matters now, one clause]
  [ ] CW-[N] [task name] — [project]
```

When the user picks one: mark it In Progress in Linear.
When the user finishes or says they're done: mark it Done.
If they don't get to it: it stays in Backlog. It will reappear tomorrow.
If priority work now needs it: move it to the sprint queue (update priority to Urgent/High).

### Cycle (sprint) management

At sprint start: create a new cycle in Linear, pull top-priority issues into it.
At sprint end: close the cycle, move incomplete issues back to Backlog.
Claude manages cycle creation and issue assignment — the user does not need to touch Linear directly for routine sprint work.

---

## OUTPUT FORMATS

### Project Status Report (on request)
```
PROJECT: [name]
Phase: [current phase]
Sprint: [N] of [estimated total]
Sprint goal: [one sentence]
Current task: [top item in sprint queue]
Blocked items: [list or "none"]
Velocity: [actual] vs [planned] units/week
Next milestone: [name] — [date]
Feature lock date: [date]
```

### Sprint Queue (on request)
```
SPRINT [N] QUEUE — [date range]
Goal: [one sentence]
Capacity: [hours]

[ ] [Work package] — [estimated hours] — depends on: [item or "none"]
[ ] [Work package] — [estimated hours] — depends on: [item or "none"]
...
```

### Phase Boundary Review Summary (on request)
```
PHASE [N] BOUNDARY REVIEW — [date]
Exit gate: [PASSED / NOT PASSED — [what's missing]]
Velocity recalibrated: [yes — new rate / no — holding]
Calendar updated: [yes — [change] / no]
MoSCoW re-triaged: [yes — [changes] / no]
Feature lock: [date — holding / moved to [new date]]
Proceed to Phase [N+1]: [YES / NO — [reason]]
```

---

## Examples

### Example 1 — Session start, in-progress project
**User:** "What should I work on today for The Loop?"
**Claude action:** Query Linear for The Loop project, find current In Progress issues, fall back to top Todo by priority if none in progress.
**Output:**
```
PROJECT: The Loop
Phase: 4 — Production (Features)
Sprint: 3 of ~8
Sprint goal: Skill system functional end-to-end
Current task: CW-14 — Implement mana generation loop (In Progress)
Blocked items: none
Velocity: 3 tasks/week (planned: 4)
Next milestone: Feature Complete — est. May 15
Feature lock date: May 15
```

### Example 2 — New project setup
**User:** "I want to start planning my graphic novel."
**Claude action:** Trigger session entry protocol — ask all four intake questions in one message.
**Output:** "Before we build the plan, a few things: (1) Is this brand new or already started? (2) What's the output — single volume, series, webtoon? (3) What's your rough scale — a few months or a year+? (4) Any fixed deadline like a convention or submission window?"

### Example 3 — Scope creep defense
**User:** "I just thought of a cool new mechanic for The Loop — procedural weather affecting elemental yields."
**Claude action:** Apply MoSCoW triage immediately before logging.
**Output:** "Before I log that — where does it fit? Must (game fails without it) / Should (significantly weaker without it) / Could (nice to have) / Won't (this version)? If it's a Must, something currently in scope needs to move out to make room."

### Example 4 — Push work
**User:** "I can't get to the audio design doc this week, too much going on at the day job."
**Claude action:** Update Linear issue to Backlog, remove from current cycle.
**Output:** "Pushed CW-22 (Audio Design Doc) to backlog. It'll resurface at next sprint planning."

### Example 5 — End-of-day quick-wins menu
**User:** "Give me some quick options for the last 30 minutes of my day."
**Claude action:** Query Linear for all quick-decision/win/task labeled issues in Backlog or Todo, sort by proximity to priority work.
**Output:**
```
END OF DAY — Mar 31
Pick something from any tier. Go longer if you want.

⚡ QUICK DECISIONS (≤5 min)
  [ ] CW-31 Decide on mana cap value — The Loop — blocks CW-14
  [ ] CW-44 Pick font for UI headers — The Loop

🎯 QUICK WINS (≤15 min)
  [ ] CW-28 Write elemental descriptions for Fire and Water — The Loop
  [ ] CW-51 Draft scene 3 beat notes — [Comic project]

🔧 QUICK TASKS (≤30 min)
  [ ] CW-19 Rough outline for chapter 2 — [Novel project]
```

### Example 6 — Velocity estimate for new project
**User:** "How long will The Loop take? I have no idea."
**Claude action:** Cannot estimate without velocity data — must first establish it from the Vertical Slice. Ask for available hours and current phase.
**Output:** "To give you a real number I need two things: (1) How many hours per week can you realistically put into The Loop? (2) What phase is it currently in — have you built and tested any complete segment at target quality yet? Without observed output rate, any estimate I give you is a guess, not a plan."

---

## Out of Scope

This skill does not:
- Do the creative work itself (writing, designing, coding)
- Replace domain-specific skills for lore, code, visual design, or audio
- Handle professional publishing contracts, marketing, or distribution
- Manage projects with teams larger than two people

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| references/domain-phases.md | Domain-specific phase equivalents (game / novel / comic) |
| utility-core-researcher | Domain research before or during a project |
| loop-extended-sequencer | Loop-specific sequencing (supersedes this skill for The Loop) |
