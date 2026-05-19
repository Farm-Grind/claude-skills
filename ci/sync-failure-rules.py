#!/usr/bin/env python3
"""
sync-failure-rules.py  —  Layer 4 sync gate

Executable sync: updates ci/failure-audit-rules.json from D1 query results,
optionally commits to a sync/* branch and pushes.

== SYNC TRIGGERS ==
Run after ANY of these D1 writes:
  - INSERT into granular_findings (new finding)
  - UPDATE granular_findings SET status = 'RESOLVED' (finding closed)
  - UPDATE failure_patterns SET recurrence_count = N (pattern bumped)
  - INSERT into failure_patterns (new pattern)
  - UPDATE granular_findings SET status = 'OPEN' (finding reopened)

Never push to main directly — main is protected.
Always push to sync/failure-audit-YYYY-MM-DD; open PR to merge.

== WORKFLOW ==
Step 1 — Query D1 via Cloudflare MCP and save results to temp files:

  # Patterns query:
  SELECT pattern_code, name, severity, recurrence_count
  FROM failure_patterns ORDER BY pattern_code
  → save to /tmp/patterns.json (D1 results array)

  # Open findings query:
  SELECT finding_id, pattern_code, title, artifact_affected, project_scope
  FROM granular_findings WHERE status = 'OPEN' ORDER BY pattern_code, finding_id
  → save to /tmp/open_findings.json (D1 results array)

  # Total findings count:
  SELECT COUNT(*) as total FROM granular_findings
  → note the number

Step 2 — Run this script:

  python3 ci/sync-failure-rules.py \\
    --patterns /tmp/patterns.json \\
    --open-findings /tmp/open_findings.json \\
    --total-findings 44 \\
    [--last-synced 2026-05-19] \\
    [--repo-root /home/claude/cs-work] \\
    [--commit] \\
    [--push]

== EXIT CODES ==
  0 = success (file written; committed/pushed if flags set)
  1 = input error (bad JSON, missing file)
  2 = git error (commit or push failed)

D1 database: afd78e0e-583e-4e78-87fc-dd6bc8150ce9
"""

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


DATABASE_ID = "afd78e0e-583e-4e78-87fc-dd6bc8150ce9"
TARGET_FILE = "ci/failure-audit-rules.json"


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_json(path_or_str, label):
    """Load JSON from a file path. Unwrap D1 {results:[...]} envelope if present."""
    try:
        p = Path(path_or_str)
        data = json.loads(p.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: could not load {label} from {path_or_str}: {e}", file=sys.stderr)
        sys.exit(1)
    if isinstance(data, dict) and "results" in data:
        return data["results"]
    if isinstance(data, list):
        return data
    print(f"ERROR: {label} must be a JSON array or D1 results envelope", file=sys.stderr)
    sys.exit(1)


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


# ── sync logic ────────────────────────────────────────────────────────────────

def build_pattern_recurrence(patterns):
    """Build pattern_recurrence dict from D1 failure_patterns rows."""
    return {row["pattern_code"]: row["recurrence_count"] for row in patterns}


def build_patterns_section(patterns):
    """Build patterns list with full metadata for check_fix_type.py consumption."""
    return [
        {
            "pattern_code": row["pattern_code"],
            "name": row["name"],
            "severity": row["severity"],
            "recurrence_count": row["recurrence_count"],
        }
        for row in patterns
    ]


def build_open_findings(open_findings):
    """Format open findings for the JSON schema."""
    out = []
    for row in open_findings:
        entry = {
            "finding_id": row["finding_id"],
            "pattern_code": row["pattern_code"],
            "title": row["title"],
        }
        if row.get("artifact_affected"):
            entry["artifact_affected"] = row["artifact_affected"]
        if row.get("project_scope"):
            entry["project_scope"] = row["project_scope"]
        out.append(entry)
    return out


def sync_data(repo_root, patterns, open_findings, total_findings, last_synced):
    """
    Load existing failure-audit-rules.json, update dynamic fields, return updated dict.

    Updated fields:
      _meta.last_synced         <- last_synced arg
      _meta.total_patterns      <- len(patterns)
      _meta.total_findings      <- total_findings arg
      pattern_recurrence        <- built from patterns rows (schema extension item 3)
      open_findings             <- built from open_findings rows

    Preserved fields (structural — do not regenerate from D1):
      static_checks, behavioral_rules
    """
    target = repo_root / TARGET_FILE
    if not target.exists():
        print(f"ERROR: {target} not found — is the repo cloned?", file=sys.stderr)
        sys.exit(1)

    data = json.loads(target.read_text())

    # Update _meta
    data["_meta"]["last_synced"] = last_synced
    data["_meta"]["total_patterns"] = len(patterns)
    data["_meta"]["total_findings"] = total_findings

    # Update patterns list (full metadata: name, severity, recurrence_count)
    data["patterns"] = build_patterns_section(patterns)

    # Update pattern_recurrence (check_fix_type.py reads this for recurrence counts)
    data["pattern_recurrence"] = build_pattern_recurrence(patterns)

    # Update open_findings
    data["open_findings"] = build_open_findings(open_findings)

    return data


def write_and_report(repo_root, data):
    target = repo_root / TARGET_FILE
    target.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Written: {target}")
    print(f"  _meta.last_synced     = {data['_meta']['last_synced']}")
    print(f"  _meta.total_patterns  = {data['_meta']['total_patterns']}")
    print(f"  _meta.total_findings  = {data['_meta']['total_findings']}")
    print(f"  pattern_recurrence    = {len(data['pattern_recurrence'])} entries")
    print(f"  open_findings         = {len(data['open_findings'])} entries")


# ── git operations ────────────────────────────────────────────────────────────

def git_commit(repo_root, last_synced, open_finding_ids):
    branch = f"sync/failure-audit-{last_synced}"

    # Create or switch to sync branch
    check = _run(["git", "branch", "--list", branch], repo_root)
    if branch in check.stdout:
        r = _run(["git", "checkout", branch], repo_root)
    else:
        r = _run(["git", "checkout", "-b", branch], repo_root)
    if r.returncode != 0:
        print(f"ERROR: git checkout failed: {r.stderr}", file=sys.stderr)
        sys.exit(2)

    r = _run(["git", "add", TARGET_FILE], repo_root)
    if r.returncode != 0:
        print(f"ERROR: git add failed: {r.stderr}", file=sys.stderr)
        sys.exit(2)

    ids_str = ", ".join(open_finding_ids[:5])
    if len(open_finding_ids) > 5:
        ids_str += f" +{len(open_finding_ids) - 5} more"
    msg = f"sync: failure audit rules from D1 ({last_synced})"
    if ids_str:
        msg += f"\n\nOpen findings: {ids_str}"

    r = _run(["git", "commit", "-m", msg], repo_root)
    if r.returncode != 0:
        if "nothing to commit" in r.stdout:
            print("Nothing to commit — failure-audit-rules.json unchanged.")
        else:
            print(f"ERROR: git commit failed: {r.stderr}", file=sys.stderr)
            sys.exit(2)
    else:
        print(f"Committed on branch: {branch}")


def git_push(repo_root, last_synced, force: bool = False):
    branch = f"sync/failure-audit-{last_synced}"
    cmd = ["git", "push", "origin", branch]
    if force:
        cmd.insert(3, "--force-with-lease")
    r = _run(cmd, repo_root)
    if r.returncode != 0:
        print(f"ERROR: git push failed: {r.stderr}", file=sys.stderr)
        print("HARD FAIL: emit open_findings JSON as fenced block for next session.")
        sys.exit(2)
    push_type = "Force-pushed" if force else "Pushed"
    print(f"{push_type}: origin/{branch}")
    print(f"Next step: open PR from {branch} -> main")


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Sync failure-audit-rules.json from D1 query results (Layer 4 sync gate)."
    )
    parser.add_argument(
        "--patterns", required=True, metavar="FILE",
        help="JSON file: SELECT pattern_code, name, severity, recurrence_count "
             "FROM failure_patterns ORDER BY pattern_code"
    )
    parser.add_argument(
        "--open-findings", required=True, metavar="FILE",
        help="JSON file: SELECT finding_id, pattern_code, title, artifact_affected, "
             "project_scope FROM granular_findings WHERE status='OPEN' "
             "ORDER BY pattern_code, finding_id"
    )
    parser.add_argument(
        "--total-findings", required=True, type=int, metavar="N",
        help="Total findings count: SELECT COUNT(*) FROM granular_findings"
    )
    parser.add_argument(
        "--last-synced", default=str(date.today()), metavar="YYYY-MM-DD",
        help="Sync date (default: today)"
    )
    parser.add_argument(
        "--repo-root", default="/home/claude/cs-work", metavar="DIR",
        help="Repo root (default: /home/claude/cs-work)"
    )
    parser.add_argument(
        "--commit", action="store_true",
        help="Stage and commit the updated JSON to sync/* branch"
    )
    parser.add_argument(
        "--push", action="store_true",
        help="Push the sync/* branch to origin (implies --commit)"
    )
    parser.add_argument(
        "--force-push", action="store_true",
        help="Force-push (--force-with-lease) the sync/* branch — use when branch "
             "already exists on remote after a squash-merge divergence (PROC-05 workaround)"
    )

    args = parser.parse_args()
    if args.force_push:
        args.push = True
    if args.push:
        args.commit = True

    repo_root = Path(args.repo_root)
    patterns = _load_json(args.patterns, "patterns")
    open_findings = _load_json(args.open_findings, "open_findings")

    if not patterns:
        print("ERROR: patterns input is empty", file=sys.stderr)
        sys.exit(1)

    data = sync_data(
        repo_root=repo_root,
        patterns=patterns,
        open_findings=open_findings,
        total_findings=args.total_findings,
        last_synced=args.last_synced,
    )
    write_and_report(repo_root, data)

    if args.commit:
        open_ids = [f["finding_id"] for f in data["open_findings"]]
        git_commit(repo_root, args.last_synced, open_ids)

    if args.push:
        git_push(repo_root, args.last_synced, force=args.force_push)


if __name__ == "__main__":
    main()
