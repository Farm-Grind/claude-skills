---
name: utility-skill-publisher
description: >
  Governs creation and update of Claude skills. Use automatically — do not
  wait to be asked. Trigger on ANY of these signals: a new skill is being
  written; an existing skill is being updated, edited, or reformatted; a
  skill is being audited; the words "skill", "SKILL.md", or "package" appear
  in a skill-authoring context; user says "create a skill", "update this
  skill", "audit this skill", "fix this skill", "change the trigger", "add
  an example to", "update the description on". For any change to an existing
  skill, surfaces one keep/remove decision to the user with its carrying cost
  before applying. Do NOT trigger for: non-skill documents (GDD, README,
  changelog, Notion pages), code generation, or content creation tasks
  unrelated to skill authoring (game ability design, lore writing, marketing
  copy). Load once per session.
---

# Skill Publisher

Source of truth: `Farm-Grind/claude-skills` repo, `main` branch.
"Done" means pushed to `main` AND CI green — nothing else counts.

---

## Skill change protocol

**1. Keep/remove decision (updates only — skip for new skills)**

Before any edits, surface one decision to the user: state what the existing
content does, why it exists, and its carrying cost (line delta, always-on
context load). Wait for confirmation before proceeding.

**2. Write or edit the SKILL.md**

- Hard limit: 500 lines. Target: 400 or fewer.
- Frontmatter: `name` (kebab-case, ≤ 64 chars) + `description` (≤ 1024 chars).
- Description must be third-person and include: "Use automatically — do not
  wait to be asked.", "Trigger on ANY of these signals:", at least one
  NOT-trigger clause, and "Load once per session." for skills over 100 lines.
- Body: imperative voice. No hedged language. No blockquotes.
- Any `references/*.md` path cited in the body must exist on disk.

**3. Validate before push**

Run against the target skill — must exit 0 before pushing:

```
python3 ci/validate.py skills/<skill-name>/SKILL.md
```

Fix every FAIL. WARN on line count is advisory.

**4. Deploy and push**

Work inside a clone of the repo so the working copy IS the repo copy:

```bash
git clone --depth=1 https://github.com/Farm-Grind/claude-skills.git /tmp/cs-$$
```

After writing and validating, deploy to the live load path and push:

```bash
# Load credentials (stored once, never expires, never enters repo)
source /mnt/skills/user/.github-credentials

# Deploy immediately — skills load from here at session start
cp -r /tmp/cs-$$/skills/<skill-name> /mnt/skills/user/<skill-name>

# Push — triggers CI validation on GitHub
cd /tmp/cs-$$
git add skills/<skill-name>/
git commit -m "<message>"
git remote set-url origin "https://${GITHUB_PAT}@github.com/Farm-Grind/claude-skills.git"
git push origin main
rm -rf /tmp/cs-$$
```

No manual PAT paste. If `/mnt/skills/user/.github-credentials` is missing,
stop and tell the user — do not ask them to paste a PAT inline.

**5. Confirm CI green**

Green CI on `main` = skill is live. This is the only done state.

---

## Dispatcher skills

All skills are dispatchers. Before writing or auditing any skill, read:

```
references/dispatcher-skeleton.md
```

It contains: the canonical 5-part body structure, classification table
template, domain code conventions, resource placement rules (body vs
references/ vs scripts/ vs assets/), cross-domain-map template, and a
worked example. Do not build a dispatcher from memory.

Resource placement summary (full criteria in dispatcher-skeleton.md §7–8):

- **Body** — routing logic, imperative instructions, fenced examples ≤ 20 lines
- **references/** — content Claude reads before executing: domain knowledge,
  formulas, frameworks, patterns. Anything > 20 lines or > 5-row table.
- **scripts/** — deterministic executable code Claude runs and checks output
  of. Use when the same procedure repeats across runs with no judgment step.
- **assets/** — fillable templates Claude copies and populates. Use when
  output is a document/boilerplate with fixed structure.

For skills with 2+ active domains: also populate `references/cross-domain-map.md`
using the template in dispatcher-skeleton.md §5.

---

## Out of Scope

- `ci/corpus-ceiling.txt` — user-owned; never edit this file.
- `.github/workflows/` — infrastructure, not skill authoring.
- CI failures caused by content bloat — fix is trimming, not a skip.

---

## SEE ALSO

| Skill / Resource | Domain |
|---|---|
| `ci/validate.py` | Single mechanical validator — all deterministic checks |
| `ci/corpus-ceiling.txt` | User-owned corpus ceiling |
| `references/dispatcher-skeleton.md` | Canonical dispatcher pattern, resource placement rules |
| `Farm-Grind/claude-skills` | Authoritative source of truth for all skills |
