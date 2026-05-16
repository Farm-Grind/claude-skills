# Failure Detection Heuristics

Use during Pass 1 to flag candidates. These are probabilistic signals, not definitive proof.

| Heuristic | What to look for | Category |
|---|---|---|
| Skill invocation missing | Relevant skill ran without its characteristic output | SK |
| Decision locked without "yes / confirmed" | LOCKED marked but no explicit user sign-off | DR / A7 |
| Widget used for text | show_widget fired but output is structured text or reference block | FMT |
| Missing fenced code block | Copy-paste content delivered inline | FMT |
| Position reversed after pushback | Stated X, pushed back with no new evidence, said "you're right" | SY |
| Partial delivery | Task marked done but a mandatory gate was not run | IH |
| Conditional action fired | "if", "assuming", "once verified" in message; Claude executed anyway | A7 |
| Repeated correction | Correction that also occurred in a prior session | DUP |
| MCP write with no re-fetch | Tool write made but no verification SELECT followed | MCP-W |
| Rule followed early, violated late | Respected in turns 1–10, ignored in turns 20+ | CTX |
| Skill lost after long session | Active early; stopped firing in later turns | CTX |
| Fix proposal at wrong layer | Fix targets skill; source is system prompt or preferences | WL |
| Transcription artifact acted on | Input contains filler words, mid-sentence restarts, or phonetically similar misreads; Claude acted on literal transcription rather than stated intent | VOI |
| Scope grew after correction | User corrected or rejected output; next output added new dimensions not requested rather than narrowing to what was asked | CI |
