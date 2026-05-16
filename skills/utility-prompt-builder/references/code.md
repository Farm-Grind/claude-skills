# Code Reference — Coding Agents and IDEs

## Contents
- § CLAUDE CODE
- § CURSOR / WINDSURF
- § GITHUB COPILOT
- § BOLT / V0 / LOVABLE / FIGMA MAKE / GOOGLE STITCH
- § DEVIN / SWE-AGENT
- § ANTIGRAVITY

---

## § CLAUDE CODE

- Agentic — runs tools, edits files, executes commands autonomously
- Required elements: starting state + target state + allowed actions + forbidden actions + stop conditions + checkpoints
- Stop conditions are MANDATORY — runaway loops are the biggest credit/compute killer
- Claude Opus 4.x over-engineers — add "Only make changes directly requested. Do not add extra files, abstractions, or features."
- Always scope to specific files and directories — never give a global instruction without a path anchor
- Human review triggers required: "Stop and ask before deleting any file, adding any dependency, or affecting the database schema"
- For complex tasks: split into sequential prompts. Output Prompt 1 and add "➡️ Run this first, then ask for Prompt 2." If user wants the full prompt, deliver all parts with clear section breaks.

**Template structure:**
```
Task: [specific deliverable]
Files in scope: [list — no other files should be touched]
Starting state: [current behavior or structure]
Target state: [desired outcome — binary pass/fail where possible]
Allowed actions: [list]
Forbidden actions: [list]
Stop conditions: [when to pause and ask]
Done when: [binary completion criteria]
```

---

## § CURSOR / WINDSURF

- Required: file path + function name + current behavior + desired change + do-not-touch list + language and version
- Never give a global instruction without a file anchor
- "Done when:" is required — defines when the agent stops editing
- For complex tasks: split into sequential prompts rather than one large prompt
- Windsurf's Cascade mode is more autonomous — add explicit stop conditions same as Claude Code

---

## § GITHUB COPILOT

- Write the exact function signature, docstring, or comment immediately before invoking
- Describe input types, return type, edge cases, and what the function must NOT do
- Copilot completes what it predicts, not what you intend — leave no ambiguity in the comment
- For test generation: specify the test framework, coverage level, and edge cases to include
- Tab completion responds to very local context — the lines immediately above the cursor matter most

---

## § BOLT / V0 / LOVABLE / FIGMA MAKE / GOOGLE STITCH

- Full-stack generators default to bloated boilerplate — scope it down explicitly
- Always specify: stack, version, what NOT to scaffold, clear component boundaries
- Lovable responds well to design-forward descriptions — include visual/UX intent
- v0 is Vercel-native — specify if you need non-Next.js output
- Bolt handles full-stack — be explicit about which parts are frontend vs backend vs database
- Figma Make is design-to-code native — reference your Figma component names directly
- Google Stitch is prompt-to-UI focused — describe the interface goal not the implementation. Add "match Material Design 3 guidelines" for Google-native styling
- Add "Do not add authentication, dark mode, or features not explicitly listed" to prevent feature bloat

---

## § DEVIN / SWE-AGENT

- Fully autonomous — can browse web, run terminal, write and test code
- Very explicit starting state + target state required
- Forbidden actions list is critical — Devin will make decisions you did not intend without explicit constraints
- Scope the filesystem: "Only work within /src. Do not touch infrastructure, config, or CI files."
- For SWE-agent: specify the repo structure and entry points explicitly

---

## § ANTIGRAVITY

Google's agent-first IDE, powered by Gemini 3 Pro.

- Task-based prompting — describe outcomes, not steps
- Prompt for an Artifact (task list, implementation plan) before execution so you can review it first
- Browser automation is built-in — include verification steps: "After building, verify UI at 375px and 1440px using the browser agent"
- Specify autonomy level: "Ask before running destructive terminal commands"
- Do NOT mix unrelated tasks — scope to one deliverable per session
- Antigravity handles multimodal context well — attach screenshots or designs directly
