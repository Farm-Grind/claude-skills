# LLM Reference — Text/Chat Models

## Contents
- § MODEL ROUTING TABLE
- § CLAUDE (claude.ai, Claude API, Claude 4.x)
- § CHATGPT / GPT-5.x
- § O3 / O4-MINI — OpenAI Reasoning Models
- § GEMINI 2.x / 3 Pro
- § QWEN 2.5 / QWEN3
- § DEEPSEEK-R1
- § MINIMAX (M2.7 / M2.5)
- § LLAMA / MISTRAL / OPEN-WEIGHT
- § OLLAMA

---

## § MODEL ROUTING TABLE

| Model | Reasoning-native? | CoT? | Optimal prompt length | Key strength |
|---|---|---|---|---|
| Claude 4.x (Sonnet/Opus) | No | Yes | Long, detailed OK | Instruction following, nuance |
| GPT-5.x | No | Yes | Compact-first | Long-context synthesis, tone adherence |
| o3 / o4-mini | YES | NEVER | Short, under 200 words | Complex reasoning from minimal input |
| Gemini 2.x / 3 Pro | No | Yes | Long context OK | Multimodal, large document tasks |
| Qwen 2.5 (instruct) | No | Yes | Short, focused | JSON, structured output |
| Qwen3 thinking mode | YES | NEVER | Short | Reasoning — treat like o3 |
| Qwen3 non-thinking | No | Yes | Explicit format | Treat like Qwen 2.5 |
| DeepSeek-R1 | YES | NEVER | Short | Reasoning — treat like o3 |
| MiniMax M2.7 | Optional (shows think tags) | Conditional | Normal | 1M context, OpenAI-compatible |
| Llama / Mistral | No | Yes | Short, flat | Locally deployable |
| Ollama | Depends on model | Depends | Short | Local deployment — ask model first |

---

## § CLAUDE

**Current versions (May 2026):** Sonnet 4.6 (standard), Opus 4.6 (complex/reasoning), Opus 4.7 (most literal, released April 2026). Use Sonnet 4.6 for everyday tasks; Opus 4.6 for multi-step work; Opus 4.7 for structured extraction and pipelines.

**Claude 4.x literal behavior (VERIFIED — Anthropic primary, 2026):**
Claude 4.x and especially Opus 4.7 interpret prompts literally and will not silently infer what you probably meant. Claude does not fill in gaps or generalize from examples. If you ask for "a dashboard", you get a dashboard container — not charts, filters, and data. This is by design.

**Consequences for prompting:**
- State scope explicitly: "Apply this formatting to every section, not just the first one."
- Specify what you want, not just what the task is: "Write exactly 3 sections. Each section must contain [X]."
- Do not rely on Claude inferring the 'obvious' next step — state it.

**Opus 4.7 vs Opus 4.6 difference:**
- Opus 4.7 is MORE literal than 4.6 — prompts written for 4.6 that relied on inference will break on 4.7.
- Opus 4.7 is better for precise structured extraction; Opus 4.6 has slightly warmer tone and more interpretation.
- For chat/claude.ai work: Sonnet 4.6 is the standard model. Opus 4.7 is for tasks needing maximum precision.

**General prompting rules:**
- Be explicit and specific — Claude follows instructions literally, not by inference
- XML tags help when prompt is multi-section (above ~300 tokens or 3+ distinct instruction types); skip them for short single-task prompts where flat prose is equal or faster
- Use `<context>`, `<task>`, `<constraints>`, `<output_format>` for complex multi-section prompts
- Provide context AND reasoning WHY, not just WHAT — Claude generalizes better from explanations
- Always specify output format and length explicitly — Claude defaults to thorough without constraints
- For long documents: specify which section to focus on

**Opus 4.6 over-engineering guard:**
Add "Only make changes directly requested. Do not add features or refactor beyond what was asked." to any prompt where output scope creep is a risk.

**Context compaction (Claude 4.6+ sessions):**
In long sessions, Claude compresses context automatically. Help it preserve critical decisions with checkpoint phrases: "Checkpoint: [what was completed]. Next up: [next task]." Add to CLAUDE.md: "When compacting, always preserve [list of things to preserve]."

**Brain dump → Claude prompt:**
When translating a brain dump to a Claude prompt, apply the Brain Dump Mode template from core-methodology.md first to extract and sequence goals, then build the prompt using the rules above. Claude 4.x will execute exactly what the prompt says — so the brain dump translation step is where all the judgment lives.

---

## § CHATGPT / GPT-5.x

- Start with the smallest prompt that achieves the goal — add structure only when needed
- Be explicit about the output contract: format, length, what "done" looks like
- State tool-use expectations explicitly if the model has access to tools
- Use compact structured outputs — GPT-5.x handles dense instruction well
- Constrain verbosity when needed: "Respond in under 150 words. No preamble. No caveats."
- GPT-5.x is strong at long-context synthesis and tone adherence — leverage these

---

## § O3 / O4-MINI

- SHORT clean instructions ONLY — these models reason across thousands of internal tokens
- NEVER add CoT, "think step by step", or reasoning scaffolding — it degrades output
- Prefer zero-shot first — add few-shot only if strictly needed
- State what you want and what done looks like. Nothing more.
- Keep system prompts under 200 words — longer prompts hurt reasoning model performance
- o3 is stronger at complex multi-step reasoning; o4-mini is faster for simpler tasks

---

## § GEMINI 2.x / 3 PRO

- Strong at long-context and multimodal — leverage its large context window for document-heavy prompts
- Prone to hallucinated citations — always add "Cite only sources you are certain of. If uncertain, say [uncertain]."
- Can drift from strict output formats — use explicit format locks with a labelled example
- For grounded tasks: "Base your response only on the provided context. Do not extrapolate."
- Gemini 2.5 Flash handles most everyday tasks; Gemini 3 Pro for complex reasoning and longer outputs

---

## § QWEN 2.5 / QWEN3

**Qwen 2.5 (instruct variants):**
- Excellent instruction following, JSON output, structured data — leverage these
- Provide a clear system prompt defining the role — Qwen 2.5 responds well to role context
- Works well with explicit output format specs including JSON schemas
- Shorter focused prompts outperform long complex ones

**Qwen3 — two modes:**
- Thinking mode (/think or enable_thinking=True): treat exactly like o3 — short clean instructions, no CoT, no scaffolding
- Non-thinking mode: treat like Qwen 2.5 instruct — full structure, explicit format, role assignment

---

## § DEEPSEEK-R1

- Reasoning-native like o3 — do NOT add CoT instructions
- Short clean instructions only — state the goal and desired output format
- Outputs reasoning in `<think>` tags by default — add "Output only the final answer, no reasoning." if clean output needed
- R1 performs comparably to o3 on many reasoning tasks at lower cost

---

## § MINIMAX (M2.7 / M2.5)

- OpenAI-compatible API — prompts that work with GPT models transfer directly
- Strong at instruction following, structured output, and long-context synthesis — 1M context window on M2.7
- M2.5-highspeed: 204K context, optimized for latency-sensitive tasks
- Temperature must be between 0 and 1 (inclusive) — values above 1 fail
- May output reasoning in `<think>` tags — add "Output only the final answer, no reasoning tags." if unwanted
- Good at code generation, JSON output, and multi-step analysis
- For function calling: supports OpenAI-style tool definitions — include tool schemas directly

---

## § LLAMA / MISTRAL / OPEN-WEIGHT

- Shorter prompts work better — lose coherence with deeply nested instructions
- Simple flat structure — avoid heavy nesting or multi-level hierarchies
- Be more explicit than you would with Claude or GPT — instruction following is weaker
- Always include a role in the system prompt
- Mistral is stronger at instruction following than base Llama; Llama 3.x improved significantly over earlier versions

---

## § OLLAMA

- ALWAYS ask which model is running before writing — Llama3, Mistral, Qwen2.5, CodeLlama all behave differently
- System prompt is the most impactful lever — include it so user can set it in their Modelfile
- Shorter simpler prompts outperform complex ones — local models lose coherence with deep nesting
- Temperature 0.1 for coding/deterministic tasks, 0.7-0.8 for creative tasks
- For coding: CodeLlama or Qwen2.5-Coder, not general Llama
