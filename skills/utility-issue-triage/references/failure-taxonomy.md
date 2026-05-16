# Failure Taxonomy Reference

## Failure Categories

| ID | Category | What it covers |
|---|---|---|
| SK | Skill non-invocation | Mandatory skill not loaded when it should have been |
| LC | Lore/canon violation | In-world content contradicted confirmed lore or GDD |
| DR | Instruction drift | Rule from system prompt or preferences silently dropped. Omission rules ("never X") decay under context depth; commission rules ("always Y") are more resistant [arxiv 2604.20911]. Fix must rewrite omission as commission — adding another omission rule is prohibited. |
| HL | Hallucination | Invented facts, fabricated citations, invented decisions |
| FMT | Formatting failure | Format rules violated (widget for text, missing fenced block) |
| IH | Incomplete/unhelpful | Task partially completed, question deflected, answer too thin |
| A7 | Conditional execution | Action taken without confirming the gating condition |
| SY | Sycophantic concession | Position reversed under pressure with no new evidence |
| DUP | Repeated failure | Same error type in a prior session and not fixed |
| MCP-W | MCP write unverified | Tool write reported complete but no re-fetch verification appeared |
| CTX | Context compression loss | Rule or correction followed early; violated after compaction |
| VOI | Voice input misclassification | Transcription artifact caused intent to be misread |
| WL | Wrong-layer fix | Proposed fix targets wrong architectural layer |
| HB | Half-baked fix | Prior fix tried and still failed — auto-escalate CRITICAL |
| CI | Complexity inflation | Under iterative pressure, output adds dimensions not requested [arxiv 2604.28031 — VERIFIED: DriftBench, 2,146 runs, 7 models, 5 providers; Claude Sonnet 4.6 99% KBV; structured checkpointing does not close dissociation] |

## Severity Levels

| Level | Criteria |
|---|---|
| CRITICAL | Wrong output delivered, decision incorrectly locked, or tool action fired incorrectly |
| HIGH | Meaningfully degraded output, missed mandatory check, required significant correction |
| MEDIUM | Suboptimal output, format rule violated, step skipped with recoverable consequence |
| LOW | Minor drift, preference ignored once, cosmetic issue |

## Fix Category Taxonomy

| Category | Definition |
|---|---|
| STRUCTURAL | Executes through external tool, format constraint, or process producing mandatory visible output independent of model judgment |
| TEMPORAL | Separates generation and evaluation into different turns or contexts |
| BEHAVIORAL | Adds/rewrites language for same-context self-check — model judges own output in same generation context |

**HB findings — fix_category_floor = TEMPORAL.** BEHAVIORAL for HB = hard fail [arxiv 2603.04582].
