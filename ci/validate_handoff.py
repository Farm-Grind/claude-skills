#!/usr/bin/env python3
"""
Handoff Block Validator — ci/validate_handoff.py

Validates a handoff block (written to a file) against the structural rules
defined in user preferences before delivery. Closes the enforcement gap on
P-09 (Partial Paste / Incomplete Deliverable), recurrence 12.

Grounds: R-012 (omission decay at turn 16), R-022 (binary checks more
durable), R-069 (commission framing most durable), R-018 (external node).

Usage:
    python3 ci/validate_handoff.py <path-to-handoff.md>
    python3 ci/validate_handoff.py --stdin   (reads from stdin)

Workflow:
    1. Claude writes the handoff block to /tmp/handoff.md
    2. Claude runs: python3 ci/validate_handoff.py /tmp/handoff.md
    3. If exit 0 (pass, block is structurally valid) — paste the block into chat
    4. If exit 1 (fail, one or more gates failed) — fix the reported failures,
       re-validate, then paste

Exit codes:
    0 = PASS — block is structurally valid, safe to deliver
    1 = FAIL — one or more gates failed, block must not be delivered

Gates (FAIL unless noted):
    HV-01  Block is wrapped in a fenced code block (``` delimiters)
    HV-02  Opening and closing delimiters are present and balanced
    HV-03  No prose appears after the closing delimiter
    HV-04  Required fields are all present: SUMMARY, NEXT, CONTEXT,
           RECOMMENDATION, ACTION REQUIRED
    HV-05  No nested fenced code blocks inside the handoff block
    HV-06  NEXT field is non-empty (not just a label)
    HV-07  CONTEXT field is non-empty
    HV-08  RECOMMENDATION field is non-empty and contains a stated position
    HV-09  ACTION REQUIRED section contains at least one bullet (•)
    HV-10  Block is the last non-whitespace content in the file
           (no trailing prose after closing ```)
    HV-11  SUMMARY field is non-empty (≥15 chars) and is not composed
           solely of bare F-XX / P-XX ticket codes without inline descriptions
    HV-12  [WARN only — does not cause FAIL] CONTEXT, RECOMMENDATION, and
           ACTION REQUIRED fields are scanned for bare F-XX / P-XX ticket
           codes not immediately followed by a parenthetical description.
           Each match emits a WARN line. Gradual rollout: fix before next
           audit cycle.
"""

import re
import sys
import argparse
from pathlib import Path


# ── Required fields ───────────────────────────────────────────────────────────

REQUIRED_FIELDS = [
    "SUMMARY",
    "NEXT",
    "CONTEXT",
    "RECOMMENDATION",
    "ACTION REQUIRED",
]

# ── Regex for bare F-XX / P-XX codes ─────────────────────────────────────────
# Matches F-NNN or P-NN not immediately followed by whitespace + '(' ...
# i.e. the code appears alone with no inline parenthetical description.
_BARE_CODE_RE = re.compile(
    r'\b([FP]-\d{2,3})\b(?!\s*\()',
)

# ── Gate implementations ──────────────────────────────────────────────────────

def extract_block(text: str) -> tuple[str | None, str]:
    """
    Find the outermost fenced code block in the file.
    Returns (block_content, remainder_after_block) or (None, '') if not found.
    The block_content includes the fence lines.
    """
    lines = text.splitlines(keepends=True)
    open_idx = None
    fence_marker = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if open_idx is None:
            # Look for opening fence
            m = re.match(r'^(`{3,}|~{3,})', stripped)
            if m:
                open_idx = i
                fence_marker = m.group(1)[0] * len(m.group(1))
        else:
            # Look for matching closing fence
            if stripped == fence_marker:
                block_lines = lines[open_idx:i + 1]
                after_lines = lines[i + 1:]
                return "".join(block_lines), "".join(after_lines)

    return None, ""


def hv_01_02_fenced_block(text: str) -> tuple[bool, str, str | None, str]:
    """HV-01 + HV-02: block exists and delimiters are balanced."""
    block, after = extract_block(text)
    if block is None:
        return False, "no fenced code block found — handoff must be wrapped in ``` delimiters", None, ""
    # Count opening lines
    open_count = sum(1 for l in block.splitlines() if re.match(r'^`{3,}|^~{3,}', l.strip()))
    if open_count < 2:
        return False, "fenced block has no closing delimiter — delimiters unbalanced", None, ""
    return True, f"fenced block found ({len(block.splitlines())} lines)", block, after


def hv_03_10_no_prose_after(after: str) -> tuple[bool, str]:
    """HV-03 + HV-10: nothing but whitespace after closing delimiter."""
    stripped = after.strip()
    if stripped:
        preview = stripped[:80].replace("\n", " ")
        return False, f"prose found after closing delimiter: \"{preview}...\""
    return True, "no trailing prose after closing delimiter"


def hv_04_required_fields(block: str) -> tuple[bool, list[str]]:
    """HV-04: all required fields present in block."""
    missing = []
    for field in REQUIRED_FIELDS:
        # Field must appear as a bold label or plain header
        pattern = rf'\*\*{re.escape(field)}[:\*]|\b{re.escape(field)}:'
        if not re.search(pattern, block, re.IGNORECASE):
            missing.append(field)
    return (len(missing) == 0), missing


def hv_05_no_nested_fences(block: str) -> tuple[bool, str]:
    """HV-05: no nested fenced code blocks inside the handoff block."""
    inner_lines = block.splitlines()[1:-1]  # Strip outer fence lines
    fence_count = sum(1 for l in inner_lines if re.match(r'^\s*(`{3,}|~{3,})', l))
    if fence_count > 0:
        return False, (
            f"{fence_count} nested fence delimiter(s) found inside block — "
            "use 4-space indentation for inner code samples, not fences"
        )
    return True, "no nested fenced blocks"


def hv_06_next_nonempty(block: str) -> tuple[bool, str]:
    """HV-06: NEXT field has content beyond the label."""
    m = re.search(r'\*\*NEXT[:\*][^\n]*\n([^\n]*)', block, re.IGNORECASE)
    if not m:
        m = re.search(r'NEXT:[^\n]*\n([^\n]*)', block, re.IGNORECASE)
    if not m:
        return False, "NEXT field not found or has no following content"
    # Content may be on same line or next line
    same_line = re.search(r'\*\*NEXT[:\*]\*?\*?\s+(.+)', block, re.IGNORECASE)
    if same_line and same_line.group(1).strip():
        return True, f"NEXT: \"{same_line.group(1).strip()[:60]}\""
    next_line = m.group(1).strip()
    if next_line:
        return True, f"NEXT: \"{next_line[:60]}\""
    return False, "NEXT field label present but content is empty"


def _field_content(block: str, field: str) -> str:
    """
    Extract text content for a field label, handling two formats:
      **FIELD:** content on same line
      **FIELD:**
      content on next line(s) until next **CAPS field
    Returns the combined content stripped.
    """
    # Same-line content
    same = re.search(
        rf'\*\*{re.escape(field)}[:\*]\**\s+([^\n]+)',
        block, re.IGNORECASE
    )
    # Multi-line content (may be empty same-line)
    multi = re.search(
        rf'\*\*{re.escape(field)}[:\*][^\n]*\n(.*?)(?=\*\*[A-Z\[]|\Z)',
        block, re.IGNORECASE | re.DOTALL
    )
    parts = []
    if same:
        parts.append(same.group(1).strip())
    if multi:
        parts.append(multi.group(1).strip())
    return " ".join(p for p in parts if p)


def hv_07_context_nonempty(block: str) -> tuple[bool, str]:
    """HV-07: CONTEXT field has substantive content."""
    content = _field_content(block, "CONTEXT")
    if not content:
        return False, "CONTEXT field not found or unparseable"
    if len(content) < 20:
        return False, f"CONTEXT content too short ({len(content)} chars) — must be substantive"
    return True, f"CONTEXT: {len(content)} chars"


def hv_08_recommendation_position(block: str) -> tuple[bool, str]:
    """HV-08: RECOMMENDATION has a stated position (not just a label)."""
    content = _field_content(block, "RECOMMENDATION")
    if not content:
        return False, "RECOMMENDATION field not found or has no stated position"
    if len(content) < 15:
        return False, f"RECOMMENDATION too short ({len(content)} chars) — must state a position"
    return True, f"RECOMMENDATION: {len(content)} chars"


def hv_09_action_bullets(block: str) -> tuple[bool, str]:
    """HV-09: ACTION REQUIRED section has at least one bullet (•)."""
    m = re.search(
        r'\*\*ACTION REQUIRED[:\*][^\n]*\n(.*?)(?=\*\*BLOCKS|\*\*NEXT|\Z)',
        block, re.IGNORECASE | re.DOTALL
    )
    if not m:
        return False, "ACTION REQUIRED section not found or unparseable"
    section = m.group(1)
    bullets = re.findall(r'^\s*[•\-\*]\s+', section, re.MULTILINE)
    if not bullets:
        return False, "ACTION REQUIRED has no bullet points (•) — each action must be a bullet"
    return True, f"{len(bullets)} action bullet(s) found"


def hv_11_summary(block: str) -> tuple[bool, str]:
    """HV-11: SUMMARY field non-empty (≥15 chars) and not composed solely of bare codes."""
    content = _field_content(block, "SUMMARY")
    if not content:
        return False, "SUMMARY field not found or has no content"
    if len(content) < 15:
        return False, f"SUMMARY too short ({len(content)} chars) — must be ≥15 chars of plain English"
    # Check if the entire content is nothing but bare codes and whitespace/punctuation
    stripped = _BARE_CODE_RE.sub("", content).strip(" ,;:-|")
    if not stripped:
        return False, "SUMMARY consists solely of bare F-XX/P-XX codes — must include plain-English description"
    return True, f"SUMMARY: {len(content)} chars"


def hv_12w_bare_codes(block: str) -> list[str]:
    """
    HV-12W (WARN — not a FAIL gate): scan CONTEXT, RECOMMENDATION, and
    ACTION REQUIRED for bare F-XX / P-XX codes not followed by a parenthetical.
    Returns list of warning strings (empty if clean).
    """
    warnings = []
    fields_to_scan = ["CONTEXT", "RECOMMENDATION", "ACTION REQUIRED"]
    for field in fields_to_scan:
        content = _field_content(block, field)
        if not content:
            continue
        for m in _BARE_CODE_RE.finditer(content):
            code = m.group(1)
            # Get context around the match for the warning message
            start = max(0, m.start() - 20)
            snippet = content[start:m.start() + len(code) + 30].replace("\n", " ")
            warnings.append(
                f"  HV-12W    WARN  {field}: bare code \"{code}\" has no inline "
                f"description — add (description) after it. Context: \"…{snippet}…\""
            )
    return warnings


# ── Runner ────────────────────────────────────────────────────────────────────

def validate(text: str) -> int:
    print("\nHANDOFF BLOCK VALIDATOR")
    print("=" * 60)

    fails = 0

    # HV-01 + HV-02
    ok, msg, block, after = hv_01_02_fenced_block(text)
    _print("HV-01/02", "Fenced block + balanced delimiters", ok, msg)
    if not ok:
        fails += 1
        # Cannot continue without a block
        print()
        print(f"VERDICT: FAIL ({fails} error(s)) — fix fencing before re-validating")
        return 1

    # HV-03 + HV-10
    ok, msg = hv_03_10_no_prose_after(after)
    _print("HV-03/10", "No prose after closing delimiter", ok, msg)
    if not ok:
        fails += 1

    # HV-04
    ok, missing = hv_04_required_fields(block)
    if ok:
        _print("HV-04", "Required fields", True, "all present")
    else:
        _print("HV-04", "Required fields", False, f"missing: {missing}")
        fails += 1

    # HV-05
    ok, msg = hv_05_no_nested_fences(block)
    _print("HV-05", "No nested fenced blocks", ok, msg)
    if not ok:
        fails += 1

    # HV-06
    ok, msg = hv_06_next_nonempty(block)
    _print("HV-06", "NEXT field non-empty", ok, msg)
    if not ok:
        fails += 1

    # HV-07
    ok, msg = hv_07_context_nonempty(block)
    _print("HV-07", "CONTEXT field substantive", ok, msg)
    if not ok:
        fails += 1

    # HV-08
    ok, msg = hv_08_recommendation_position(block)
    _print("HV-08", "RECOMMENDATION states a position", ok, msg)
    if not ok:
        fails += 1

    # HV-09
    ok, msg = hv_09_action_bullets(block)
    _print("HV-09", "ACTION REQUIRED has bullets", ok, msg)
    if not ok:
        fails += 1

    # HV-11
    ok, msg = hv_11_summary(block)
    _print("HV-11", "SUMMARY non-empty and not code-only", ok, msg)
    if not ok:
        fails += 1

    # HV-12W (warn only — does not increment fails)
    code_warnings = hv_12w_bare_codes(block)
    if code_warnings:
        for w in code_warnings:
            print(w)
    else:
        _print("HV-12W", "No bare F-XX/P-XX codes in scanned fields", True, "clean")

    print()
    if fails:
        print(f"VERDICT: FAIL ({fails} error(s)) — fix before delivering")
        return 1
    print("VERDICT: PASS — block is structurally valid, safe to deliver")
    return 0


def _print(gate: str, label: str, ok: bool, msg: str):
    status = "PASS" if ok else "FAIL"
    print(f"  {gate:<10} {status}  {label}: {msg}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Validate a handoff block before delivery (P-09 enforcement)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="Path to handoff .md file")
    group.add_argument("--stdin", action="store_true", help="Read from stdin")
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    else:
        path = Path(args.file)
        if not path.exists():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text()

    sys.exit(validate(text))


if __name__ == "__main__":
    main()
