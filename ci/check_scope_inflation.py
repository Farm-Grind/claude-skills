#!/usr/bin/env python3
"""
Scope Inflation Gate — ci/check_scope_inflation.py

STRUCTURAL fix for P-15 (Complexity Inflation Under Iterative Pressure).

Closes F-048. Grounds: FC-04 (CRITICAL severity requires STRUCTURAL or TEMPORAL);
A6 in user preferences is BEHAVIORAL and insufficient.

Mechanism
---------
Before starting any task, declare a scope manifest (--init). The manifest
records which files are allowed to change and whether new files are permitted.
After work is done, run --check (or let the pre-commit hook run it). If the
diff touches files outside the manifest, the gate FAILS.

This is STRUCTURAL because the git pre-commit hook refuses to commit when scope
is exceeded — Claude cannot self-override a commit block.

Integration
-----------
  .githooks/pre-commit calls:
      python3 ci/check_scope_inflation.py --check --staged

  If no manifest exists at the time of commit, the gate emits WARN (exit 2)
  and allows the commit to proceed (not all commits require scope tracking).
  This prevents the gate from blocking unrelated infrastructure work.

Usage
-----
  # 1. Declare scope before starting work:
  python3 ci/check_scope_inflation.py --init \\
      --task "Add --force-push flag to git_push()" \\
      --files "ci/sync-failure-rules.py"

  # 2. Optionally allow new files:
  python3 ci/check_scope_inflation.py --init \\
      --task "Add scope inflation gate" \\
      --files "ci/check_scope_inflation.py,ci/scope-active.json" \\
      --new-files-ok

  # 3. Validate staged changes (run before commit):
  python3 ci/check_scope_inflation.py --check --staged

  # 4. Validate HEAD diff (post-commit audit):
  python3 ci/check_scope_inflation.py --check --diff-head

  # 5. Validate a specific diff file:
  python3 ci/check_scope_inflation.py --check --diff-file /tmp/my.diff

  # 6. Clear manifest after task is complete:
  python3 ci/check_scope_inflation.py --clear

  # 7. Show active manifest:
  python3 ci/check_scope_inflation.py --show

Manifest location
-----------------
  ci/scope-active.json  (gitignored — session artifact, not committed)

Exit codes
----------
  0 = PASS  — diff is within declared scope
  1 = FAIL  — diff touches files outside declared scope
  2 = WARN  — manifest absent, stale (>24h), or no diff to check

Gates
-----
  SCI-00  Manifest present and schema-valid
  SCI-01  All modified/deleted files in diff are in files_allowed
  SCI-02  New files in diff are in files_allowed OR new_files_allowed=true
  SCI-03  Manifest not stale (warn if created >24h ago)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_MANIFEST = Path("ci/scope-active.json")
STALE_HOURS = 24


# ── Manifest I/O ──────────────────────────────────────────────────────────────

def write_manifest(task: str, files: list[str], new_files_ok: bool,
                   manifest_path: Path) -> dict:
    manifest = {
        "task": task,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files_allowed": [f.strip() for f in files if f.strip()],
        "new_files_allowed": new_files_ok,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def read_manifest(manifest_path: Path) -> tuple[dict | None, str]:
    """Return (manifest_dict, error_message). error_message is '' on success."""
    if not manifest_path.exists():
        return None, f"no manifest found at {manifest_path}"
    try:
        data = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        return None, f"manifest JSON invalid: {e}"
    for field in ("task", "created_at", "files_allowed", "new_files_allowed"):
        if field not in data:
            return None, f"manifest missing required field: '{field}'"
    if not isinstance(data["files_allowed"], list):
        return None, "'files_allowed' must be a list"
    if not isinstance(data["new_files_allowed"], bool):
        return None, "'new_files_allowed' must be a boolean"
    return data, ""


# ── Git diff parsing ──────────────────────────────────────────────────────────

class DiffEntry:
    def __init__(self, status: str, path: str, old_path: str | None = None):
        self.status = status   # M, A, D, R, C, T, U
        self.path = path       # new path (or only path)
        self.old_path = old_path  # original path for renames

    @property
    def is_new(self) -> bool:
        return self.status in ("A", "C")

    @property
    def is_modified(self) -> bool:
        return self.status in ("M", "T", "U")

    @property
    def is_deleted(self) -> bool:
        return self.status == "D"

    @property
    def is_renamed(self) -> bool:
        return self.status == "R"


def get_diff_entries(mode: str, diff_file: str | None = None) -> tuple[list[DiffEntry], str]:
    """
    Return (entries, error). mode is 'staged', 'head', or 'file'.
    'staged' → git diff --cached --name-status
    'head'   → git diff HEAD --name-status
    'file'   → parse provided diff file (unified diff --name-status format not available;
               parse unified diff for +++ / --- lines instead)
    """
    if mode == "staged":
        cmd = ["git", "diff", "--cached", "--name-status"]
    elif mode == "head":
        cmd = ["git", "diff", "HEAD", "--name-status"]
    elif mode == "file":
        if not diff_file:
            return [], "diff_file path required for mode=file"
        return _parse_unified_diff(Path(diff_file))
    else:
        return [], f"unknown diff mode: {mode}"

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # No commits yet → diff HEAD fails; treat as empty diff
        if "unknown revision" in result.stderr or "fatal" in result.stderr:
            return [], ""
        return [], f"git error: {result.stderr.strip()}"

    return _parse_name_status(result.stdout), ""


def _parse_name_status(output: str) -> list[DiffEntry]:
    entries = []
    for line in output.strip().splitlines():
        if not line:
            continue
        parts = line.split("\t")
        if not parts:
            continue
        status_raw = parts[0].strip()
        status = status_raw[0]  # first char (R100 → R)
        if status == "R" and len(parts) >= 3:
            entries.append(DiffEntry(status, parts[2].strip(), parts[1].strip()))
        elif len(parts) >= 2:
            entries.append(DiffEntry(status, parts[1].strip()))
        # else: malformed line, skip
    return entries


def _parse_unified_diff(path: Path) -> tuple[list[DiffEntry], str]:
    """
    Minimal parser for unified diff files: extract changed file paths from
    '+++ b/<path>' and '--- a/<path>' lines. Not as precise as --name-status
    but works when only a .diff file is available.
    """
    if not path.exists():
        return [], f"diff file not found: {path}"
    entries: list[DiffEntry] = []
    seen: set[str] = set()
    try:
        content = path.read_text(errors="replace")
    except OSError as e:
        return [], str(e)

    new_files: set[str] = set()
    deleted_files: set[str] = set()

    for line in content.splitlines():
        if line.startswith("+++ b/"):
            fp = line[6:].strip()
            if fp not in seen:
                seen.add(fp)
                new_files.add(fp)
        elif line.startswith("--- a/"):
            fp = line[6:].strip()
            if fp not in seen:
                seen.add(fp)
                deleted_files.add(fp)
        elif line.startswith("--- /dev/null"):
            pass  # new file marker handled via +++ b/

    for fp in new_files:
        if fp not in deleted_files:
            entries.append(DiffEntry("A", fp))
        else:
            entries.append(DiffEntry("M", fp))
    for fp in deleted_files - new_files:
        entries.append(DiffEntry("D", fp))

    return entries, ""


# ── Gate implementations ──────────────────────────────────────────────────────

def sci_00_manifest_valid(manifest: dict | None, error: str) -> tuple[str, str]:
    if manifest is None:
        return "FAIL", f"manifest invalid or absent: {error}"
    return "PASS", f"manifest schema valid (task: {manifest['task']!r})"


def sci_01_modified_in_scope(entries: list[DiffEntry],
                              allowed: set[str]) -> tuple[str, list[str]]:
    """Modified and deleted files must be in files_allowed."""
    violations = []
    for e in entries:
        if e.is_new:
            continue  # handled by SCI-02
        # Modified, deleted, renamed — old and new paths must both be declared
        if e.path not in allowed:
            violations.append(f"{e.status}  {e.path}  ← NOT in files_allowed")
        if e.is_renamed and e.old_path and e.old_path not in allowed:
            violations.append(f"R  {e.old_path}  ← renamed-from NOT in files_allowed")
    status = "FAIL" if violations else "PASS"
    return status, violations


def sci_02_new_files_in_scope(entries: list[DiffEntry],
                               allowed: set[str],
                               new_files_ok: bool) -> tuple[str, list[str]]:
    """New files must be in files_allowed OR new_files_allowed=true."""
    violations = []
    for e in entries:
        if not e.is_new:
            continue
        if e.path in allowed:
            continue  # explicitly declared
        if new_files_ok:
            continue  # blanket permission
        violations.append(f"A  {e.path}  ← new file not declared; set new_files_allowed=true or add to files_allowed")
    status = "FAIL" if violations else "PASS"
    return status, violations


def sci_03_manifest_staleness(manifest: dict) -> tuple[str, str]:
    """Warn if manifest was created more than STALE_HOURS hours ago."""
    try:
        created = datetime.fromisoformat(manifest["created_at"])
        age_hours = (datetime.now(timezone.utc) - created).total_seconds() / 3600
    except (KeyError, ValueError):
        return "WARN", "could not parse created_at — manifest may be stale"
    if age_hours > STALE_HOURS:
        return "WARN", (
            f"manifest is {age_hours:.1f}h old (threshold: {STALE_HOURS}h) — "
            "run --clear and --init again if this is a new task"
        )
    return "PASS", f"manifest age {age_hours:.1f}h (within {STALE_HOURS}h threshold)"


# ── Formatters ────────────────────────────────────────────────────────────────

def _icon(status: str) -> str:
    return {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}.get(status, "?")


def _print_gate(gate: str, status: str, summary: str, details: list[str] | None = None):
    print(f"  {gate}  {_icon(status)}  {summary}")
    for d in (details or []):
        print(f"          {d}")


# ── Modes ─────────────────────────────────────────────────────────────────────

def cmd_init(args) -> int:
    manifest_path = Path(args.manifest)
    if not args.task:
        print("ERROR: --task is required with --init", file=sys.stderr)
        return 1
    if not args.files:
        print("ERROR: --files is required with --init", file=sys.stderr)
        return 1

    files = [f.strip() for f in args.files.split(",") if f.strip()]
    manifest = write_manifest(args.task, files, args.new_files_ok, manifest_path)

    print(f"\nSCOPE MANIFEST WRITTEN — {manifest_path}")
    print("=" * 60)
    print(f"  Task              : {manifest['task']}")
    print(f"  Created at        : {manifest['created_at']}")
    print(f"  files_allowed     : {manifest['files_allowed']}")
    print(f"  new_files_allowed : {manifest['new_files_allowed']}")
    print()
    print("Run check before commit:")
    print(f"  python3 ci/check_scope_inflation.py --check --staged")
    return 0


def cmd_clear(args) -> int:
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"No manifest at {manifest_path} — nothing to clear.")
        return 0
    manifest_path.unlink()
    print(f"Cleared: {manifest_path}")
    return 0


def cmd_show(args) -> int:
    manifest_path = Path(args.manifest)
    manifest, error = read_manifest(manifest_path)
    if manifest is None:
        print(f"No active manifest ({error})")
        return 2
    print(f"\nACTIVE SCOPE MANIFEST — {manifest_path}")
    print("=" * 60)
    print(json.dumps(manifest, indent=2))
    return 0


def cmd_check(args) -> int:
    manifest_path = Path(args.manifest)

    # SCI-00 — manifest
    manifest, error = read_manifest(manifest_path)
    print("\nSCOPE INFLATION GATE")
    print("=" * 60)

    if manifest is None:
        _print_gate("SCI-00", "WARN",
                    f"no manifest at {manifest_path} — no scope declared for this commit")
        print()
        print("VERDICT: WARN (no manifest — scope gate skipped)")
        print("  Create a manifest with: python3 ci/check_scope_inflation.py --init \\")
        print("    --task \"<description>\" --files \"<comma-separated paths>\"")
        return 2

    sci00_status, sci00_msg = sci_00_manifest_valid(manifest, error)
    _print_gate("SCI-00", sci00_status, sci00_msg)
    if sci00_status == "FAIL":
        print()
        print("VERDICT: FAIL (manifest invalid — fix or re-run --init)")
        return 1

    # Resolve diff mode
    if args.staged:
        diff_mode = "staged"
        diff_label = "staged (--cached)"
    elif args.diff_head:
        diff_mode = "head"
        diff_label = "HEAD"
    elif args.diff_file:
        diff_mode = "file"
        diff_label = f"file:{args.diff_file}"
    else:
        diff_mode = "staged"
        diff_label = "staged (default)"

    entries, diff_error = get_diff_entries(diff_mode, args.diff_file)
    if diff_error:
        _print_gate("DIFF", "WARN", f"could not read diff ({diff_label}): {diff_error}")
        print()
        print("VERDICT: WARN (diff unavailable — run manually after git add)")
        return 2

    if not entries:
        _print_gate("DIFF", "WARN",
                    f"diff is empty ({diff_label}) — nothing staged/changed")
        print()
        print("VERDICT: WARN (empty diff — stage changes before checking)")
        return 2

    print(f"  Diff source       : {diff_label}")
    print(f"  Files in diff     : {len(entries)}")
    print(f"  files_allowed     : {manifest['files_allowed']}")
    print(f"  new_files_allowed : {manifest['new_files_allowed']}")
    print()

    allowed = set(manifest["files_allowed"])
    new_files_ok = manifest["new_files_allowed"]

    hard_fails: list[str] = []
    warnings: list[str] = []

    # SCI-01
    sci01_status, sci01_violations = sci_01_modified_in_scope(entries, allowed)
    _print_gate("SCI-01", sci01_status,
                "Modified/deleted files within declared scope",
                sci01_violations)
    if sci01_status == "FAIL":
        hard_fails.extend(sci01_violations)

    # SCI-02
    sci02_status, sci02_violations = sci_02_new_files_in_scope(entries, allowed, new_files_ok)
    _print_gate("SCI-02", sci02_status,
                "New files within declared scope",
                sci02_violations)
    if sci02_status == "FAIL":
        hard_fails.extend(sci02_violations)

    # SCI-03
    sci03_status, sci03_msg = sci_03_manifest_staleness(manifest)
    _print_gate("SCI-03", sci03_status, f"Manifest staleness: {sci03_msg}")
    if sci03_status == "WARN":
        warnings.append(sci03_msg)

    print()
    print(f"  Task: {manifest['task']!r}")
    print()

    if hard_fails:
        print(f"VERDICT: FAIL ({len(hard_fails)} scope violation(s))")
        print()
        print("  Scope exceeded — changes outside declared scope detected.")
        print("  Options:")
        print("    1. Revert the out-of-scope changes")
        print(f"    2. Re-declare scope: python3 ci/check_scope_inflation.py --init \\")
        print(f"         --task \"{manifest['task']}\" \\")
        print(f"         --files \"<expanded file list>\"")
        print("  Note: re-declaring scope is an audit trail event — it documents")
        print("  scope expansion, which is the P-15 signal.")
        return 1

    if warnings:
        print(f"VERDICT: WARN ({len(warnings)} warning(s)) — scope OK, review warnings above")
        return 2

    print("VERDICT: PASS — diff is within declared scope")
    return 0


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Scope inflation gate (P-15 STRUCTURAL fix). "
            "Declare task scope before work; validate diff before commit."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Declare scope (run before starting work):
  python3 ci/check_scope_inflation.py --init \\
      --task "Add --force-push flag" \\
      --files "ci/sync-failure-rules.py"

  # Validate staged changes (run after git add, before git commit):
  python3 ci/check_scope_inflation.py --check --staged

  # Clear manifest after task complete:
  python3 ci/check_scope_inflation.py --clear
""",
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--init", action="store_true",
                            help="Write a new scope manifest")
    mode_group.add_argument("--check", action="store_true",
                            help="Validate diff against active manifest")
    mode_group.add_argument("--clear", action="store_true",
                            help="Remove active manifest")
    mode_group.add_argument("--show", action="store_true",
                            help="Print active manifest")

    # --init options
    parser.add_argument("--task", help="Task description (required with --init)")
    parser.add_argument("--files", help="Comma-separated list of allowed files (required with --init)")
    parser.add_argument("--new-files-ok", action="store_true", default=False,
                        help="Allow new files not in --files list (default: false)")

    # --check options
    diff_group = parser.add_mutually_exclusive_group()
    diff_group.add_argument("--staged", action="store_true",
                            help="Check staged diff (git diff --cached) [default]")
    diff_group.add_argument("--diff-head", action="store_true",
                            help="Check HEAD diff (git diff HEAD)")
    diff_group.add_argument("--diff-file", metavar="FILE",
                            help="Check a unified diff file")

    # shared
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                        help=f"Manifest path (default: {DEFAULT_MANIFEST})")

    args = parser.parse_args()

    if args.init:
        return cmd_init(args)
    elif args.check:
        return cmd_check(args)
    elif args.clear:
        return cmd_clear(args)
    elif args.show:
        return cmd_show(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
