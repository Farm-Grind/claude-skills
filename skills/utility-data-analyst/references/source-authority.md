# Source Authority Scoring

Reference for `utility-data-analyst`. Apply at retrieval time. Confidence labels ([VERIFIED] / [PARTIAL] / [UNVERIFIED]) must appear in the SOURCES section of every synthesis output, not only on findings.

## Contents

- § Authority signals
- § Source labels (used in output)
- § Red flags
- § Confidence label rules

---

## § Authority signals

Score each source against these signals at the point of retrieval.

| Signal | What to look for | Weight |
|---|---|---|
| Primary vs. secondary | Original research, data, or direct experience vs. summarizing others | Highest |
| Author expertise | Recognized practitioner, researcher, or domain expert with publication history | High |
| Institutional backing | Affiliated with respected institution, peer-reviewed journal, or official industry body | High |
| Evidence quality | Claims backed by data, studies, or demonstrated outcomes vs. assertions | High |
| Community validation | Cited, referenced, or built on by others in the domain | Medium |
| Recency vs. foundational | Fast-moving domain: recent > older. Stable domain: foundational works retain weight. | Context-dependent |
| Conflict of interest | Commercial stake in conclusions — disclosed = reduced risk, undisclosed = red flag | Penalizing |
| Specificity | Addresses the actual question vs. adjacent territory | Medium |

---

## § Source labels

Use these inline in SOURCES section.

| Label | When to use |
|---|---|
| [Primary] | Original research, original data, direct practitioner account |
| [Industry] | Respected publication, conference, professional body |
| [Practitioner] | Expert practitioner with demonstrated domain experience |
| [Academic] | Peer-reviewed or institutional research |
| [Secondary] | Summarizes others; use only when primaries unavailable |
| [Contested] | Flag when source has conflicting positions in the field |

---

## § Red flags

Flag but do not automatically exclude:

- Vendor or agency promoting its own tools
- Undated source, or more than 5 years old in a fast-moving domain
- Sweeping claims without evidence
- Widely cited but original claim unverified
- Single source for a finding labeled [VERIFIED]

---

## § Confidence label rules (per finding and per source)

| Label | Evidential standard |
|---|---|
| [VERIFIED] | N≥2 independent high-authority sources, or 1 controlled study/meta-analysis. For Triple Pass: Pass 2 found new corroborating sources. |
| [PARTIAL] | Evidence exists with named limitation — single source, contested origin, fast-moving domain with stale sources, or partial analogue from cross-industry |
| [UNVERIFIED] | Practitioner consensus or training knowledge without external corroboration |
| [TRAINING KNOWLEDGE — not externally verified] | Required label for any finding in Creative Synthesis mode. Cannot be upgraded to [VERIFIED]. |
| [SPECULATIVE] | Reasoning from premises with limited evidence — flag explicitly |

A finding's label cannot exceed the strongest single source supporting it unless N≥2 independent sources converge.
