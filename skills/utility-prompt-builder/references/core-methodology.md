# Core Methodology Reference

## Contents
- § HARD RULES — never violate
- § INTENT EXTRACTION — 9-dimension extraction
- § DIAGNOSTIC CHECKLIST — failure patterns to fix
- § SAFE TECHNIQUES — apply only when needed
- § MEMORY BLOCK — for prompts referencing prior work
- § PROMPT DECOMPILER — for fixing or adapting existing prompts
- § OUTPUT FORMAT — final delivery structure

---

## § HARD RULES — NEVER VIOLATE

- NEVER output a prompt without confirming the target tool — ask if ambiguous
- NEVER embed techniques that cause fabrication in single-prompt execution:
  - Mixture of Experts — model role-plays personas from one forward pass, no real routing
  - Tree of Thought — model generates linear text and simulates branching, no real parallelism
  - Graph of Thought — requires an external graph engine, single-prompt = fabrication
  - Universal Self-Consistency — requires independent sampling, later paths contaminate earlier ones
  - Prompt chaining as a layered technique — pushes models into fabrication on longer chains
- NEVER add Chain of Thought to reasoning-native models (o3, o4-mini, DeepSeek-R1, Qwen3 thinking mode)
- NEVER ask more than 3 clarifying questions before producing a prompt
- NEVER pad output with explanations the user did not request

---

## § INTENT EXTRACTION

Before writing any prompt, silently extract these 9 dimensions. Missing
critical dimensions trigger clarifying questions (max 3 total).

| Dimension | What to extract | Critical? |
|---|---|---|
| Task | Specific action — convert vague verbs to precise operations | Always |
| Target tool | Which AI system receives this prompt | Always |
| Output format | Shape, length, structure, filetype of the result | Always |
| Constraints | What MUST and MUST NOT happen, scope boundaries | If complex |
| Input | What the user is providing alongside the prompt | If applicable |
| Context | Domain, project state, prior decisions from this session | If session has history |
| Audience | Who reads the output, their technical level | If user-facing |
| Success criteria | How to know the prompt worked — binary where possible | If task is complex |
| Examples | Desired input/output pairs for pattern lock | If format-critical |

---

## § DIAGNOSTIC CHECKLIST

Scan every user-provided prompt or rough idea for these failure patterns.
Fix silently — flag only if the fix changes the user's intent.

**Task failures**
- Vague task verb → replace with a precise operation
- Two tasks in one prompt → split, deliver as Prompt 1 and Prompt 2
- No success criteria → derive a binary pass/fail from the stated goal
- Emotional description ("it's broken") → extract the specific technical fault
- Scope is "the whole thing" → decompose into sequential prompts

**Context failures**
- Assumes prior knowledge → prepend memory block with all prior decisions
- Invites hallucination → add grounding constraint: "State only what you can verify. If uncertain, say so."
- No mention of prior failures → ask what they already tried (counts toward 3-question limit)

**Format failures**
- No output format specified → derive from task type and add explicit format lock
- Implicit length ("write a summary") → add word or sentence count
- No role assignment for complex tasks → add domain-specific expert identity
- Vague aesthetic ("make it professional") → translate to concrete measurable specs

**Scope failures**
- No file or function boundaries for IDE AI → add explicit scope lock
- No stop conditions for agents → add checkpoint and human review triggers
- Entire codebase pasted as context → scope to the relevant file and function only

**Reasoning failures**
- Logic or analysis task with no step-by-step → add "Think through this carefully before answering"
- CoT added to o3/o4-mini/R1/Qwen3-thinking → REMOVE IT
- New prompt contradicts prior session decisions → flag, resolve, include memory block

**Agentic failures**
- No starting state → add current project state description
- No target state → add specific deliverable description
- Silent agent → add "After each step output: ✅ [what was completed]"
- Unrestricted filesystem → add scope lock on which files and directories are touchable
- No human review trigger → add "Stop and ask before: [list destructive actions]"

---

## § SAFE TECHNIQUES

Apply only when genuinely needed.

**Role assignment** — for complex or specialized tasks.
- Weak: "You are a helpful assistant"
- Strong: "You are a senior backend engineer specializing in distributed systems who prioritizes correctness over cleverness"

**Few-shot examples** — when format is easier to show than describe. Apply when user has re-prompted for the same formatting issue more than once. 2-5 examples.

**Grounding anchors** — for any factual or citation task:
"Use only information you are highly confident is accurate. If uncertain, write [uncertain] next to the claim. Do not fabricate citations or statistics."

**Chain of Thought** — for logic, math, and debugging on standard reasoning models ONLY (Claude, GPT-5.x, Gemini, Qwen2.5, Llama). NEVER on o3/o4-mini/R1/Qwen3-thinking.
"Think through this step by step before answering."

---

## § MEMORY BLOCK

When the user's request references prior work, decisions, or session history — prepend this block to the generated prompt. Place in the first 30% of the prompt.

```
## Context (carry forward)
- Stack and tool decisions established
- Architecture choices locked
- Constraints from prior turns
- What was tried and failed
```

---

## § BRAIN DUMP MODE

Activate when: user says "brain dump", "here's what I'm thinking", "let me just tell you what I want to do"; input has voice-input markers (incomplete clauses, mid-sentence restarts, "and also", "oh and", "actually"); user provides multiple goals without structure or sequencing; user says "translate this into a Claude prompt" or "turn this into an action plan."

**Brain dump is different from a bad prompt.** A bad prompt has clear intent but poor structure. A brain dump has multiple goals that need to be extracted, separated, and sequenced before any prompt can be built.

**Step 1 — Extract:**
Pull every stated goal as a distinct task. One verb, one deliverable per task. Ignore filler words and repetition.

**Step 2 — Sequence:**
Identify dependencies (what must happen before what). Flag any task that requires the output of a prior task.

**Step 3 — Flag ambiguities:**
Note missing context, unclear scope, or goals that could be interpreted multiple ways. One clarifying question maximum if needed — ask it BEFORE producing the prompt.

**Step 4 — Build:**
Produce a structured Claude prompt using the sequenced tasks. Apply Claude-specific rules from llm.md: explicit scope, literal behavior accommodations, XML tags only if multi-section, output format specified.

**Output format:**
```
GOAL EXTRACTION
———————————
Tasks identified: [N]
1. [Task — verb-first, one sentence, binary completion criteria]
2. [Task]
[...]

DEPENDENCIES: [sequencing rules, or "none identified"]
CLARIFYING: [one question if ambiguous, or omit]

STRUCTURED PROMPT FOR CLAUDE
———————————
[Complete prompt, ready to paste. Context block first, then tasks in sequence, then output format.]
```

`🎯 Target: Claude [version] — brain dump translated to [N] structured tasks`

---

## § MULTI-TASK SESSION TEMPLATE

Use when the user has multiple distinct tasks for a single Claude session that must be executed in order. Different from a brain dump — the tasks are already clear, but the user needs help structuring them as a session prompt.

```
<context>
[Project state, prior decisions, what Claude needs to know before starting]
</context>

<tasks>
Task 1: [verb-first, specific, done-when criteria]
Task 2: [must follow Task 1 — describe dependency explicitly]
Task 3: [independent or follows Task 2]
</tasks>

<constraints>
- Complete each task fully before starting the next
- After each task: output [specified format showing completion]
- Stop and confirm before: [any irreversible actions]
</constraints>

<output_format>
[Specify format for each task's output]
</output_format>
```

**Rules:**
- Maximum 3-4 tasks per session prompt. More than 4 = split into two sessions.
- Each task needs a "done when" condition — not just a description of what to do.
- Dependencies must be stated explicitly: "Task 2 uses the output of Task 1."
- Never sequence a research task immediately before an implementation task without a confirmation step between them.

---

## § PROMPT DECOMPILER

Activate when: user pastes an existing prompt and wants to break it down,
adapt it for a different tool, simplify it, or split it.

**Step 1 — Parse:**
- Identify tool the prompt was written for
- Extract: task, role, constraints, format, techniques used, tone

**Step 2 — Diagnose:**
- Apply diagnostic checklist above
- Flag: banned techniques, wrong syntax for target tool, vague task verbs,
  missing constraints, fabrication risks

**Step 3 — Route:**
- If adapting to a new tool: re-run intent extraction for the new tool, apply
  new tool's rules from domain reference file
- If simplifying: remove hedged language, empty constraints, filler
- If splitting: identify where two distinct tasks exist, output as Prompt 1
  and Prompt 2 with a handoff note

**Output format for decompiler:**
```
ORIGINAL: [tool, detected techniques, issues found]
DIAGNOSIS: [list of failure patterns fixed]
RESULT: [rebuilt prompt(s)]
🎯 Target: [tool] — [what was fixed and why]
```

---

## § OUTPUT FORMAT

All prompt output follows this format:

1. A single copyable prompt block in a fenced code block, ready to paste
2. `🎯 Target: [tool name] — [one sentence: what was optimized and why]`
3. Setup note if needed (1-2 lines, only when genuinely required before pasting)

For tools requiring dual-field input (Suno, ComfyUI positive/negative): always
produce both fields, labeled, in separate fenced blocks.

For copywriting and content prompts: include fillable placeholders where relevant:
[TONE], [AUDIENCE], [BRAND VOICE], [PRODUCT NAME]

**Pre-delivery verification:**
1. Is the target tool correctly identified and prompt formatted for its specific syntax?
2. Are the most critical constraints in the first 30% of the prompt?
3. Does every instruction use the strongest signal word? MUST over should. NEVER over avoid.
4. Has every fabrication technique been removed?
5. Token efficiency: every sentence load-bearing, no vague adjectives, format explicit, scope bounded?
6. Would this prompt produce the right output on the first attempt?

**Success metric:** The user pastes the prompt into the target tool. It works
on the first try. Zero re-prompts needed.
