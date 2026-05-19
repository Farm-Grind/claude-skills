# Python Scripts, Bash Automation, D1 Ops, GitHub, and CI Toolchain

Source: extracted from session history — covers the scripting work done alongside
The Loop development. Load on `PS` code activation.

---

## Container Environment

### File System Layout

| Path | Write? | Purpose |
|---|---|---|
| `/tmp/` | ✓ | Staging for packaging, temp clones, interim files |
| `/home/claude/` | ✓ | Session working directory |
| `/home/claude/cs-work/` | ✓ | CI scripts, working repo |
| `/mnt/user-data/outputs/` | ✓ | Final deliverables only — what the user downloads |
| `/mnt/skills/user/<name>/` | ✗ | READ-ONLY; copy to `/tmp/` before modifying |
| `/mnt/skills/examples/` | ✗ | READ-ONLY packaging toolchain |
| `/mnt/user-data/uploads/` | ✗ | READ-ONLY user uploads |

HARD FAIL: any write attempted to `/mnt/skills/` or `/mnt/user-data/uploads/`.

### Python Runtime
- Runtime: system python3 (Ubuntu 24)
- pip: **always** `pip install <pkg> --break-system-packages` — bare `pip install` fails
- Syntax validation before every delivery: `python3 -m py_compile script.py && echo "Syntax OK"`
- venv: only if project has conflicting deps; not needed for single-script CI work

### Network Allowlist (bash_tool)
Allowed domains include: `api.anthropic.com`, `pypi.org`, `github.com`,
`registry.npmjs.org`, `files.pythonhosted.org`. Full list in `<network_configuration>`.
Cloudflare MCP calls go via the MCP connection — not raw HTTP from bash.

---

## Python Scripting Conventions

### Script Header

```python
#!/usr/bin/env python3
"""
One-line description.
Usage: python3 script.py [positional] [--flags]
"""
import argparse
import json
import sys
from pathlib import Path
```

### Exit Convention (enforced)
- `sys.exit(0)` — success / PASS
- `sys.exit(1)` — failure / HARD FAIL
- Always print before exit: `print("PASS")` / `print(f"FAIL: {reason}")`
- CI scripts consumed by other scripts must follow this convention — callers check exit code

### CLI Arguments

```python
parser = argparse.ArgumentParser(description="Brief description")
parser.add_argument("input_path", help="Path to input file")
parser.add_argument("--commit", action="store_true", help="Stage and commit changes")
parser.add_argument("--push", action="store_true", help="Push after commit")
args = parser.parse_args()
```

### JSON Config Files

```python
from pathlib import Path
import json

# Read
data = json.loads(Path(path).read_text())

# Write (always indent=2 for readability and diff-friendliness)
Path(path).write_text(json.dumps(data, indent=2))
```

### Error Handling
```python
try:
    result = operation()
except (FileNotFoundError, ValueError, KeyError) as e:
    print(f"FAIL: {e}")
    sys.exit(1)
```
No bare `except:` — always name exception types.
No `os.system()` — use `subprocess.run()` for subprocesses.

---

## Bash Scripting Conventions

### Script Header (mandatory)
```bash
#!/usr/bin/env bash
set -euo pipefail
```

### Temp Directory Management
```bash
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT
```

### Error Capture
```bash
output=$(command 2>&1) || { echo "FAIL: $output"; exit 1; }
```

### Command Availability Check
```bash
command -v python3 >/dev/null 2>&1 || { echo "FAIL: python3 not found"; exit 1; }
```

---

## D1 Database Operations (Cloudflare MCP)

### Database IDs

| Name | ID | Contains |
|---|---|---|
| the-loop-storage | `a2af54f4-6385-45dd-92e7-edc45fa5b8bd` | build_phase, npc_name_reference, game data |
| claude-config | `afd78e0e-583e-4e78-87fc-dd6bc8150ce9` | skills, secrets, failure_patterns, granular_findings, validation_rules |

HARD FAIL: never mix the-loop-storage and claude-config in the same query context. State which DB is being targeted before any query.

### Tool
`d1_database_query` with fields `database_id` and `sql`. Load via `tool_search "D1 database query"`.

### Known Tables — claude-config

| Table | Key columns | Purpose |
|---|---|---|
| `skills` | name, version, status, lines, updated_at | Skill registry (max 50 skills, 17,500 total lines) |
| `secrets` | key, value | PAT and sensitive config; query before any GitHub op |
| `failure_patterns` | pattern_code, name, severity | P-01..P-15 failure taxonomy |
| `granular_findings` | finding_id, pattern_code, title, artifact_affected, status | OPEN/CLOSED failure findings |
| `validation_rules` | rule_id, applies_to, description, linked_patterns | VR-XX CI enforcement rules |

### Known Tables — the-loop-storage

| Table | Key columns | Purpose |
|---|---|---|
| `build_phase` | key, content | `SELECT content FROM build_phase WHERE key = 'current'` |
| `npc_name_reference` | id, name, category | 423-record NPC naming database |

### Common Patterns
```sql
-- Upsert
INSERT OR REPLACE INTO skills (name, version, status, lines, updated_at)
VALUES ('skill-name', 'v1.0', 'INSTALLED', 120, '2026-05-18')

-- Fetch PAT
SELECT value FROM secrets WHERE key = 'github_pat'

-- Skill ceiling check
SELECT COUNT(*) cnt, COALESCE(SUM(lines),0) ttl FROM skills WHERE status='INSTALLED'
```

Batch limit: D1 handles ~1000 rows per query reliably. Batch large inserts; test with small batches first.

---

## GitHub Operations

### PAT Handling
1. `SELECT value FROM secrets WHERE key = 'github_pat'` on claude-config
2. Use value in-memory only — never hardcode in scripts, bash strings, or comments
3. After push: `rm -rf /tmp/<clone-dir>` immediately to wipe PAT from disk
4. Signal string to scan for: `github_pat_` — if found in generated code outside a comment, FAIL

### Clone Pattern
```bash
git clone --depth=1 https://<PAT>@github.com/Farm-Grind/claude-skills.git /tmp/claude-skills
```

### Commit Pattern
```bash
cd /tmp/claude-skills
git config user.email "sync@claude-skills"
git config user.name "Claude Sync"
git add <files>
git commit -m "<type>(<scope>): <summary>"
git remote set-url origin "https://<PAT>@github.com/Farm-Grind/claude-skills.git"
git push origin main    # or sync/<description>-YYYY-MM-DD
rm -rf /tmp/claude-skills   # PAT wipe
```

### Branch Naming
| Type | Branch |
|---|---|
| Direct production commit | `main` |
| Automated sync script | `sync/<description>-YYYY-MM-DD` (open PR to merge) |

### Repo Layout
```
Farm-Grind/claude-skills (public read / PAT-auth write)
├── skills/<skill-name>/SKILL.md
├── skills/<skill-name>/references/
├── ci/
│   ├── validate.py
│   ├── sync-skills.sh
│   ├── sync-failure-rules.py
│   └── failure-audit-rules.json
```

---

## CI Toolchain

### Script Inventory

| Script | Location | Call pattern |
|---|---|---|
| `validate_handoff.py` | `/home/claude/cs-work/ci/validate_handoff.py` | `python3 validate_handoff.py /tmp/handoff.md` → exit 0 = PASS |
| `validate.py` | `/home/claude/cs-work/ci/validate.py` | `python3 validate.py skills/<name>/SKILL.md` → `OVERALL: PASS` in output |
| `sync-failure-rules.py` | `/home/claude/cs-work/ci/sync-failure-rules.py` | Syncs D1 failure_patterns → `ci/failure-audit-rules.json` |
| `sync-skills.sh` | `/home/claude/sync-skills.sh` | Syncs GitHub repo → `/mnt/skills/user/`; run at session start |
| `pre_package_check.py` | `/mnt/skills/user/skill-tools/pre_package_check.py` | Pre-packaging body validation |
| `pack_skill.sh` | `/mnt/skills/user/skill-tools/pack_skill.sh` | Entry point: checks then packages |

If a CI script path doesn't resolve (`find /home/claude -name script.py`), check if cs-work repo needs cloning before referencing it.

### Skill Packaging Command
```bash
cd /mnt/skills/examples/skill-creator
python3 -m scripts.package_skill /tmp/<skill-name>/ /tmp/pkg-output/
```
Output must contain `Skill is valid!` — HARD FAIL otherwise. Copy result to `/mnt/user-data/outputs/`.

---

## Pre-Generation Checklist (PS code active)

Before writing any Python or bash script:
1. **Target directory** — output goes to `/home/claude/` or `/tmp/`; never directly to `/mnt/skills/`
2. **D1 target** — state which database (the-loop-storage or claude-config) before any query
3. **PAT handling** — confirm PAT is fetched from D1 at runtime; not embedded in code
4. **pip flag** — confirm `--break-system-packages` on all pip installs in scope
5. **CI script paths** — if referencing CI scripts, confirm paths exist: `find /home/claude/cs-work -name <script>`

---

## Post-Generation Audit (PS code active)

After generating any script, check all before presenting:
- No `github_pat_` string in code outside a comment
- No hardcoded D1 database ID without an identifying comment naming the database
- Every `pip install` includes `--break-system-packages`
- No writes attempted to `/mnt/skills/` or `/mnt/user-data/uploads/`
- No bare `except:` in Python
- No `os.system()` — `subprocess.run()` or bash equivalent
- Exit conventions: `sys.exit(0)` pass, `sys.exit(1)` fail
- Syntax check block visible: `python3 -m py_compile script.py && echo "Syntax OK"`
