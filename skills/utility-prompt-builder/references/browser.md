# Browser Reference — Browser and Computer Agents

## § ALL BROWSER/COMPUTER AGENTS

These agents control a real browser — they click, scroll, fill forms, and can
complete transactions autonomously.

**Universal rules:**
- Describe the outcome, not the navigation steps
- Specify constraints explicitly — the agent will make its own decisions without them
- Add permission boundaries: "Do not make any purchase. Research only."
- Add stop condition for irreversible actions: "Ask me before submitting any form, completing any transaction, or sending any message"
- Scope what it can and cannot access: "Only interact with [specific site/domain]"

---

## § CLAUDE IN CHROME

- Browsing agent built into Chrome
- Works best with web research, comparison, and data extraction tasks
- Specify the output format: "Return a summary of findings as bullet points" or "Fill out the form with the following values: [list]"
- Add "Do not navigate away from [domain]" to scope the browsing session

---

## § OPENAI ATLAS

- Stronger for multi-step commerce and account management tasks
- Describe the full goal: "Find all my active subscriptions on [site], list them with price and renewal date"
- Explicit stop conditions critical: "Stop before entering any payment information"
- Atlas handles multi-page workflows — break into discrete goals per session

---

## § COMET (Perplexity Computer) / PERPLEXITY COMPUTER

- Best at web research, product comparison, and data extraction tasks
- Describe the deliverable: "Create a comparison table of [products] including price, features, and availability"
- Add accuracy guardrail: "Flag any information you cannot verify"
- Comet runs research tasks autonomously — scope with a clear stop condition

---

## § PROMPT TEMPLATE FOR ANY COMPUTER AGENT

```
Goal: [The specific outcome you want achieved]
Scope: [Which sites, domains, or pages are in bounds]
Forbidden: [What the agent must not do — purchases, signups, form submissions]
Stop condition: [Ask me before: [list irreversible actions]]
Output: [What to deliver when done — summary, filled form, extracted data]
```
