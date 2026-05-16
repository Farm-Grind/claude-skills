# Research Reference — Research and Orchestration AI

## § PERPLEXITY

**Three modes — specify which:**
- Search mode: web research, current information, citations
- Analyze mode: reason over provided documents or URLs
- Compare mode: side-by-side comparison of sources or topics

**Rules:**
- Add citation requirements: "Cite your sources inline. Include URL and date."
- Reframe hallucination-prone questions as grounded queries: not "What happened at X?" → "What does [source type] say about X?"
- Perplexity Computer: multi-step research to deliverable. Describe the end artifact type (report / spreadsheet / summary). Add "Flag any data point you are not confident about."
- Add verification checkpoints for multi-step tasks: "After each research phase, summarize findings before proceeding."

---

## § MANUS AI

- Multi-agent orchestrator — describe the end deliverable, not the steps. Manus decomposes internally.
- Specify output artifact type: report, spreadsheet, code, action taken
- Add "Flag any data point you are not confident about"
- For long tasks: request progress checkpoints — each chained step compounds hallucination risk
- Manus can browse the web and execute code — scope what it can and cannot do: "Research only. Do not sign up for any accounts or make any transactions."

---

## § DEEP RESEARCH (Claude / ChatGPT / Gemini)

- Describe the research question precisely — not "tell me about X" but "compare X and Y on these dimensions: [list]"
- Specify the output format: executive summary, structured report, comparison table, annotated bibliography
- Add source requirements: "Include only sources from the last 12 months" or "Prioritize peer-reviewed sources"
- Add accuracy guardrail: "Indicate your confidence level for each key claim. Flag anything uncertain."
