# Workflow Reference — Automation and Workflow AI

## § ZAPIER / MAKE / N8N

**Shared prompting structure:**
```
Trigger app + trigger event → action app + action + field mapping
```

Step by step. Auth requirements noted explicitly: "assumes [app] is already connected."

For multi-step workflows:
- Number each step explicitly
- Specify what data passes between steps
- Name the fields that map from one step's output to the next step's input

**Zapier-specific:**
- Natural language workflow builder: describe the trigger and action in plain English
- Be explicit about filters (only trigger when [field] equals [value])
- Formatter step: specify date format, text transforms, or number operations explicitly

**Make (Integromat)-specific:**
- Module-based — describe each module's role and the data transformation between modules
- Specify error handling routes: "if the [step] fails, route to [fallback action]"
- Iterator and aggregator patterns: name them explicitly when splitting/joining arrays

**n8n-specific:**
- Node-based — open source with self-hosting option
- Supports code nodes (JavaScript/Python) — specify which language and the transformation needed
- HTTP Request nodes: provide full URL, method, headers, and body format
- When using AI/LLM nodes in n8n: specify the model and provide a complete system prompt

**Universal checklist for automation prompts:**
1. Trigger: what event starts the workflow?
2. Condition: any filters or conditions before proceeding?
3. Action: what does the workflow do?
4. Field mapping: exactly which fields from step A feed step B?
5. Error handling: what happens if a step fails?
6. Auth: which apps need to be connected before this runs?
