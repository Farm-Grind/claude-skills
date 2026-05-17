#!/usr/bin/env python3
"""
Research Quality Gate — ci/validate_research.py

Validates a proposed research_finding against mechanical quality gates
before D1 insertion. Part of the research database integrity pipeline.

Called by:
  - utility-data-analyst PART 13 (via bash_tool before any INSERT)
  - GitHub CI (on PRs that include research_findings SQL changes)

Usage:
    python3 ci/validate_research.py finding.json
    python3 ci/validate_research.py --json '{"research_id": "R-071", ...}'
    python3 ci/validate_research.py --sql "INSERT INTO research_findings ..."

Exit codes:
    0 = PASS (ready for INSERT)
    1 = HARD FAIL (one or more gates failed — block INSERT)
    2 = WARN (passes structurally but requires manual review before INSERT)

Gates:
    RQG-01  Required fields present and non-empty
    RQG-02  confidence ∈ {VERIFIED, PARTIAL, OPEN}
    RQG-03  source_type ∈ {academic, practitioner, empirical,
                            primary-anthropic, conversation-audit}
    RQG-04  research_id matches R-[0-9]{3,4}
    RQG-05  finding length ≥ 80 chars
    RQG-06  application_guidance length ≥ 60 chars
    RQG-07  application_guidance contains at least one action verb
    RQG-08  No banned arxiv IDs in primary_source
    RQG-09  WARN if source_type=conversation-audit with confidence=VERIFIED
    RQG-10  misapplication_warning is not empty string
    RQG-11  WARN if application_guidance contains additive-complexity language
             without a populated misapplication_warning
    RQG-12  category is lowercase-hyphenated (a-z and hyphens only)
"""

import argparse
import json
import re
import sys

# ── Constants ─────────────────────────────────────────────────────────────────

REQUIRED_FIELDS = [
    "research_id", "category", "finding", "confidence",
    "primary_source", "source_type", "application_guidance",
    "misapplication_warning",
]

VALID_CONFIDENCE = {"VERIFIED", "PARTIAL", "OPEN"}

VALID_SOURCE_TYPES = {
    "academic", "practitioner", "empirical",
    "primary-anthropic", "conversation-audit",
}

BANNED_ARXIV_IDS = {"2605.06445", "2601.22025"}

ACTION_VERBS = {
    "use", "apply", "check", "verify", "test", "run", "confirm", "query",
    "load", "require", "avoid", "never", "always", "before", "after", "when",
    "must", "should", "route", "assign", "monitor", "flag", "set", "keep",
    "remove", "add", "update", "write", "read", "ensure", "do not", "do",
    "place", "deploy", "call", "invoke", "validate", "enforce", "default",
    "for", "filter", "scope", "restrict", "prefer", "choose", "select",
}

# Language patterns that suggest adding complexity without budget check.
# Present in application_guidance AND misapplication_warning is 'None.'
# → WARN (likely should be flagged as misapplication risk).
ADDITIVE_RISK_PATTERNS = [
    r"add\s+a\s+(gate|rule|check|constraint|validation)",
    r"add\s+more\s+(gates|rules|checks|constraints)",
    r"create\s+additional\s+(gates?|rules?|checks?)",
    r"extend\s+the\s+(gate|rule|check)",
    r"include\s+a\s+new\s+(gate|rule|constraint)",
]

RESEARCH_ID_RE = re.compile(r"^R-\d{3,4}$")
CATEGORY_RE = re.compile(r"^[a-z][a-z0-9-]*$")

# ── Gate functions ─────────────────────────────────────────────────────────────

def rgq_01_required_fields(f: dict) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in f:
            errors.append(f"missing field '{field}'")
        elif not isinstance(f[field], str) or not f[field].strip():
            errors.append(f"field '{field}' is empty or not a string")
    return errors


def rgq_02_confidence(f: dict) -> list[str]:
    v = f.get("confidence", "")
    if v not in VALID_CONFIDENCE:
        return [f"confidence '{v}' not in {sorted(VALID_CONFIDENCE)}"]
    return []


def rgq_03_source_type(f: dict) -> list[str]:
    v = f.get("source_type", "")
    if v not in VALID_SOURCE_TYPES:
        return [f"source_type '{v}' not in {sorted(VALID_SOURCE_TYPES)}"]
    return []


def rgq_04_research_id(f: dict) -> list[str]:
    rid = f.get("research_id", "")
    if not RESEARCH_ID_RE.match(rid):
        return [f"research_id '{rid}' must match R-NNN or R-NNNN"]
    return []


def rgq_05_finding_length(f: dict) -> list[str]:
    finding = f.get("finding", "")
    if len(finding) < 80:
        return [f"finding too short ({len(finding)} chars, minimum 80)"]
    return []


def rgq_06_guidance_length(f: dict) -> list[str]:
    g = f.get("application_guidance", "")
    if len(g) < 60:
        return [f"application_guidance too short ({len(g)} chars, minimum 60)"]
    return []


def rgq_07_guidance_verb(f: dict) -> list[str]:
    g = f.get("application_guidance", "").lower()
    for verb in ACTION_VERBS:
        if verb in g:
            return []
    return ["application_guidance contains no recognisable action verb — "
            "guidance must be specific and actionable"]


def rgq_08_banned_arxiv(f: dict) -> list[str]:
    src = f.get("primary_source", "")
    errors = []
    for arxiv_id in BANNED_ARXIV_IDS:
        if arxiv_id in src:
            errors.append(f"banned arxiv ID {arxiv_id} in primary_source")
    return errors


def rgq_09_warn_conversation_verified(f: dict) -> list[str]:
    """WARN only — does not cause HARD FAIL."""
    if (f.get("source_type") == "conversation-audit"
            and f.get("confidence") == "VERIFIED"):
        return ["source_type=conversation-audit with confidence=VERIFIED — "
                "confirm at least one external source corroborates before INSERT"]
    return []


def rgq_10_misapplication_warning(f: dict) -> list[str]:
    maw = f.get("misapplication_warning", "")
    if not maw.strip():
        return ["misapplication_warning must be 'None.' or a substantive warning "
                "— empty string is not valid"]
    return []


def rgq_11_warn_additive_without_flag(f: dict) -> list[str]:
    """WARN only — does not cause HARD FAIL.

    Catches the most obvious additive-language patterns locally. The full
    check (JOIN against research_findings.misapplied_pattern_code to find
    prior misapplications in the same category) runs in d1-validation.md
    Step 2a and requires D1 access.
    """
    guidance = f.get("application_guidance", "").lower()
    maw = f.get("misapplication_warning", "")
    if maw.strip() != "None.":
        return []  # already flagged
    warnings = []
    for pattern in ADDITIVE_RISK_PATTERNS:
        if re.search(pattern, guidance):
            warnings.append(
                f"application_guidance contains additive-complexity language "
                f"matching '{pattern}' — misapplication_warning is 'None.' "
                f"Run d1-validation.md Step 2a (misapplied_pattern_code JOIN) "
                f"before INSERT to confirm no P-02 risk"
            )
    return warnings


def rgq_12_category_format(f: dict) -> list[str]:
    cat = f.get("category", "")
    if not CATEGORY_RE.match(cat):
        return [f"category '{cat}' must be lowercase-hyphenated (a-z, 0-9, hyphens only, "
                "must start with a letter)"]
    return []


# ── Runner ────────────────────────────────────────────────────────────────────

HARD_FAIL_GATES = [
    ("RQG-01", "Required fields",           rgq_01_required_fields),
    ("RQG-02", "Confidence enum",           rgq_02_confidence),
    ("RQG-03", "Source type enum",          rgq_03_source_type),
    ("RQG-04", "research_id format",        rgq_04_research_id),
    ("RQG-05", "Finding length",            rgq_05_finding_length),
    ("RQG-06", "Guidance length",           rgq_06_guidance_length),
    ("RQG-07", "Guidance action verb",      rgq_07_guidance_verb),
    ("RQG-08", "Banned arxiv IDs",          rgq_08_banned_arxiv),
    ("RQG-10", "Misapplication warning",    rgq_10_misapplication_warning),
    ("RQG-12", "Category format",           rgq_12_category_format),
]

WARN_GATES = [
    ("RQG-09", "Conversation-audit VERIFIED", rgq_09_warn_conversation_verified),
    ("RQG-11", "Additive language without flag", rgq_11_warn_additive_without_flag),
]


def validate(finding: dict) -> int:
    """Returns exit code: 0=PASS, 1=FAIL, 2=WARN."""
    print(f"\nRESEARCH QUALITY GATE — {finding.get('research_id', '?')}")
    print("=" * 60)

    hard_fails = []
    warnings = []

    for gate_id, gate_name, fn in HARD_FAIL_GATES:
        errors = fn(finding)
        if errors:
            for e in errors:
                print(f"  {gate_id}  FAIL  {gate_name}: {e}")
                hard_fails.append(f"{gate_id}: {e}")
        else:
            print(f"  {gate_id}  PASS  {gate_name}")

    for gate_id, gate_name, fn in WARN_GATES:
        warns = fn(finding)
        if warns:
            for w in warns:
                print(f"  {gate_id}  WARN  {gate_name}: {w}")
                warnings.append(f"{gate_id}: {w}")
        else:
            print(f"  {gate_id}  PASS  {gate_name}")

    print()
    if hard_fails:
        print(f"VERDICT: HARD FAIL ({len(hard_fails)} error(s)) — block INSERT")
        for e in hard_fails:
            print(f"  ✗ {e}")
        return 1
    elif warnings:
        print(f"VERDICT: WARN ({len(warnings)} warning(s)) — manual review required before INSERT")
        for w in warnings:
            print(f"  ⚠ {w}")
        return 2
    else:
        print("VERDICT: PASS — ready for INSERT")
        return 0


# ── SQL extraction ────────────────────────────────────────────────────────────

def extract_from_sql(sql_text: str) -> dict | None:
    """
    Naive extraction of VALUES from a single-row INSERT INTO research_findings.
    Returns None if extraction fails (fall back to error).
    Handles single-quoted SQL strings; does not handle escaped quotes robustly
    — use JSON input mode for complex values.
    """
    # Match INSERT INTO research_findings (...) VALUES (...)
    m = re.search(
        r"INSERT\s+INTO\s+research_findings\s*\([^)]+\)\s*VALUES\s*\((.+)\)\s*$",
        sql_text, re.IGNORECASE | re.DOTALL
    )
    if not m:
        return None

    cols_m = re.search(
        r"INSERT\s+INTO\s+research_findings\s*\(([^)]+)\)",
        sql_text, re.IGNORECASE
    )
    if not cols_m:
        return None

    cols = [c.strip() for c in cols_m.group(1).split(",")]
    vals_str = m.group(1)

    # Tokenize single-quoted strings and bare tokens
    tokens = re.findall(r"'(?:[^'\\]|\\.)*'|[^,]+", vals_str)
    vals = []
    for t in tokens:
        t = t.strip()
        if t.startswith("'") and t.endswith("'"):
            vals.append(t[1:-1])
        else:
            vals.append(t)

    if len(cols) != len(vals):
        return None

    return dict(zip(cols, vals))


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Validate a research_finding before D1 insertion."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="JSON file containing the finding")
    group.add_argument("--json", help="Inline JSON string")
    group.add_argument("--sql", help="INSERT SQL string to parse")
    args = parser.parse_args()

    try:
        if args.json:
            finding = json.loads(args.json)
        elif args.sql:
            finding = extract_from_sql(args.sql)
            if finding is None:
                print("ERROR: could not parse SQL — use --json for complex values", file=sys.stderr)
                sys.exit(1)
        else:
            with open(args.file) as fh:
                finding = json.load(fh)
    except (json.JSONDecodeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(validate(finding))


if __name__ == "__main__":
    main()
