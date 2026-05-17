#!/usr/bin/env python3
"""
Platform Constraints Validator — ci/validate_constraints.py

Codifies known platform limits discovered empirically or from documentation.
Closes F-016 (OPEN): platform constraints discovered mid-build rather than
pre-established. Grounds: R-030 (D1 limits discovered through failure),
R-031 (GitHub connector mismatch), R-018 (external enforcement node).

This script serves two purposes:
  1. Reference — run with --list to see all known constraints
  2. Payload check — pass a JSON payload to verify it does not exceed limits

Usage:
    python3 ci/validate_constraints.py --list
    python3 ci/validate_constraints.py --check-sql "INSERT INTO ..."
    python3 ci/validate_constraints.py --check-json '{"key": "value", ...}'
    python3 ci/validate_constraints.py --check-domain "api.example.com"
    python3 ci/validate_constraints.py --check-mcp-param '{"large": "payload"}'

Exit codes:
    0 = PASS or informational (--list)
    1 = FAIL — payload exceeds a known limit
    2 = WARN — payload approaches a limit (>80% of maximum)

Constraint sources:
    [EMPIRICAL]   Discovered through production failure in this project
    [DOCUMENTED]  From official Cloudflare / Anthropic / platform documentation
    [INFERRED]    Derived from observed behavior without explicit documentation
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Callable


# ── Constraint registry ───────────────────────────────────────────────────────

@dataclass
class Constraint:
    id: str
    category: str
    name: str
    limit: int | None          # None = boolean / non-numeric constraint
    unit: str
    warn_pct: float            # warn when payload > this fraction of limit
    source: str                # EMPIRICAL | DOCUMENTED | INFERRED
    notes: str
    reference: str = ""        # Finding ID or URL
    check_fn: Callable | None = field(default=None, repr=False)


CONSTRAINTS: list[Constraint] = [

    # ── D1 ─────────────────────────────────────────────────────────────────

    Constraint(
        id="D1-01",
        category="cloudflare-d1",
        name="D1 row size",
        limit=1_000_000,
        unit="bytes",
        warn_pct=0.80,
        source="DOCUMENTED",
        notes="Maximum size of a single D1 row. Exceeding this causes silent "
              "truncation or insert failure. Large TEXT fields (e.g. research "
              "finding bodies, skill bodies) must be checked before INSERT.",
        reference="https://developers.cloudflare.com/d1/platform/limits/",
    ),

    Constraint(
        id="D1-02",
        category="cloudflare-d1",
        name="D1 SQL statement size",
        limit=500_000,
        unit="bytes",
        warn_pct=0.80,
        source="DOCUMENTED",
        notes="Maximum size of a single SQL statement including all values. "
              "Large INSERT statements with embedded TEXT content approach this "
              "limit quickly when storing skill bodies or research findings.",
        reference="https://developers.cloudflare.com/d1/platform/limits/",
    ),

    Constraint(
        id="D1-03",
        category="cloudflare-d1",
        name="D1 database size",
        limit=2_000_000_000,
        unit="bytes",
        warn_pct=0.70,
        source="DOCUMENTED",
        notes="Maximum total database size (2 GB for paid plan). "
              "Current claude-config usage is trivial relative to this.",
        reference="https://developers.cloudflare.com/d1/platform/limits/",
    ),

    # ── MCP ────────────────────────────────────────────────────────────────

    Constraint(
        id="MCP-01",
        category="mcp-params",
        name="MCP tool parameter payload",
        limit=100_000,
        unit="bytes",
        warn_pct=0.80,
        source="EMPIRICAL",
        notes="No hard limit is officially documented, but payloads above "
              "~100KB have caused failures in production sessions (F-016). "
              "Treat as a soft limit pending official documentation.",
        reference="F-016",
    ),

    Constraint(
        id="MCP-02",
        category="mcp-schema",
        name="MCP server schema token overhead (per server)",
        limit=55_000,
        unit="tokens",
        warn_pct=1.0,  # Always inform — no way to partially load
        source="EMPIRICAL",
        notes="A 93-tool MCP server consumes ~55,000 context tokens before "
              "any work begins (R-016). 3+ connected servers can consume "
              "40,000–80,000 tokens of a 200,000-token window. Plan sessions "
              "with 3+ servers as starting at 40–50% context utilization.",
        reference="R-016",
    ),

    # ── Bash container network ──────────────────────────────────────────────

    Constraint(
        id="NET-01",
        category="bash-network",
        name="Allowed outbound domains",
        limit=None,
        unit="domain",
        warn_pct=1.0,
        source="DOCUMENTED",
        notes="The bash_tool container has a network allowlist. Requests to "
              "domains not on this list fail with a deny header. Always verify "
              "a domain is accessible before building multi-step workflows "
              "that depend on it.",
        reference="system-prompt network_configuration",
    ),

    Constraint(
        id="NET-02",
        category="bash-network",
        name="GitHub connector (Claude.ai OAuth) is read-only",
        limit=None,
        unit="boolean",
        warn_pct=1.0,
        source="EMPIRICAL",
        notes="The GitHub OAuth integration shown in Claude.ai Settings is "
              "NOT an MCP server. It cannot create repos or push files. "
              "Git push requires bash_tool + PAT + github.com in allowlist. "
              "Confirmed: github.com IS in the allowlist (R-031).",
        reference="R-031, F-029",
    ),

    # ── Claude context window ───────────────────────────────────────────────

    Constraint(
        id="CTX-01",
        category="context-window",
        name="Context window size (Claude Sonnet 4.6)",
        limit=200_000,
        unit="tokens",
        warn_pct=0.40,  # Warn at 40%: MCP schema overhead eats first ~40%
        source="DOCUMENTED",
        notes="Total context window. MCP schema overhead (MCP-02) consumes "
              "40,000–80,000 tokens before first message with 3+ servers. "
              "Intelligence degradation observed at 40–50% fill (R-008). "
              "Sessions with large skill files + multiple MCPs risk crossing "
              "this threshold early.",
        reference="R-008, R-016",
    ),

    Constraint(
        id="CTX-02",
        category="context-window",
        name="Tool call degradation threshold",
        limit=5,
        unit="MCP tool calls",
        warn_pct=1.0,
        source="EMPIRICAL",
        notes="Behavioral drift (repeated questions, contradicted decisions, "
              "dropped constraints) correlates with accumulated MCP tool calls, "
              "not just turn count. 5+ MCP calls is the warning threshold. "
              "20+ turns is a secondary threshold (R-017).",
        reference="R-017",
    ),

    # ── Skill corpus ────────────────────────────────────────────────────────

    Constraint(
        id="SKILL-01",
        category="skill-corpus",
        name="Individual skill body line count (hard limit)",
        limit=500,
        unit="lines",
        warn_pct=0.80,
        source="DOCUMENTED",
        notes="Enforced by ci/validate.py. Skills exceeding 500 lines fail CI. "
              "Target is 400 lines (warn at 400). Hard limit is 500.",
        reference="ci/validate.py check_line_count",
    ),

    Constraint(
        id="SKILL-02",
        category="skill-corpus",
        name="Instruction constraint count (compliance collapse)",
        limit=15,
        unit="discrete constraints",
        warn_pct=0.80,
        source="EMPIRICAL",
        notes="Compliance degrades non-linearly above ~15 discrete constraints "
              "(R-041, MOSAIC). Each additional constraint reduces effective "
              "compliance of all others. This is a ceiling, not a target.",
        reference="R-041",
    ),
]


# ── Allowed domain list (from system prompt network_configuration) ────────────

ALLOWED_DOMAINS = {
    "adobe.io", "api.anthropic.com", "api.github.com", "archive.ubuntu.com",
    "crates.io", "files.pythonhosted.org", "github.com", "index.crates.io",
    "npmjs.com", "npmjs.org", "pypi.org", "pythonhosted.org",
    "registry.npmjs.org", "registry.yarnpkg.com", "security.ubuntu.com",
    "static.crates.io", "www.npmjs.com", "www.npmjs.org", "yarnpkg.com",
}

ALLOWED_WILDCARD_PATTERNS = [
    r"^.*\.adobe\.io$",
    r"^.*\.npmjs\.com$",
    r"^.*\.npmjs\.org$",
]


def is_domain_allowed(domain: str) -> bool:
    domain = domain.lower().strip()
    if domain in ALLOWED_DOMAINS:
        return True
    for pattern in ALLOWED_WILDCARD_PATTERNS:
        if re.match(pattern, domain):
            return True
    return False


# ── Payload checkers ──────────────────────────────────────────────────────────

def check_bytes(payload: str | bytes, constraint: Constraint) -> tuple[str, str]:
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    size = len(payload)
    if constraint.limit is None:
        return "PASS", "no numeric limit"
    pct = size / constraint.limit
    if pct > 1.0:
        return "FAIL", (
            f"{size:,} bytes exceeds limit of {constraint.limit:,} bytes "
            f"({pct*100:.1f}%)"
        )
    if pct >= constraint.warn_pct:
        return "WARN", (
            f"{size:,} bytes is {pct*100:.1f}% of limit ({constraint.limit:,} bytes) — "
            "approaching limit"
        )
    return "PASS", f"{size:,} bytes ({pct*100:.1f}% of {constraint.limit:,} byte limit)"


# ── Main modes ────────────────────────────────────────────────────────────────

def list_constraints() -> int:
    print("\nPLATFORM CONSTRAINTS REGISTRY")
    print("=" * 70)
    by_category: dict[str, list[Constraint]] = {}
    for c in CONSTRAINTS:
        by_category.setdefault(c.category, []).append(c)

    for cat, items in sorted(by_category.items()):
        print(f"\n  [{cat.upper()}]")
        for c in items:
            limit_str = f"{c.limit:,} {c.unit}" if c.limit else f"(see notes) {c.unit}"
            print(f"    {c.id:<10} [{c.source}]  {c.name}: {limit_str}")
            print(f"             {c.notes[:110]}")
            if c.reference:
                print(f"             → ref: {c.reference}")
    print()
    return 0


def check_sql(sql: str) -> int:
    print("\nSQL PAYLOAD CHECK")
    print("=" * 60)
    fails = 0
    warnings = 0

    for cid in ["D1-01", "D1-02"]:
        c = next(x for x in CONSTRAINTS if x.id == cid)
        status, msg = check_bytes(sql, c)
        _print(c.id, c.name, status, msg)
        if status == "FAIL":
            fails += 1
        elif status == "WARN":
            warnings += 1

    print()
    if fails:
        print(f"VERDICT: FAIL ({fails} limit(s) exceeded)")
        return 1
    if warnings:
        print(f"VERDICT: WARN ({warnings} limit(s) approached)")
        return 2
    print("VERDICT: PASS")
    return 0


def check_json_payload(raw: str) -> int:
    print("\nMCP PARAM PAYLOAD CHECK")
    print("=" * 60)
    c = next(x for x in CONSTRAINTS if x.id == "MCP-01")
    status, msg = check_bytes(raw, c)
    _print(c.id, c.name, status, msg)
    print()
    if status == "FAIL":
        print("VERDICT: FAIL")
        return 1
    if status == "WARN":
        print("VERDICT: WARN")
        return 2
    print("VERDICT: PASS")
    return 0


def check_domain(domain: str) -> int:
    print("\nDOMAIN ALLOWLIST CHECK")
    print("=" * 60)
    allowed = is_domain_allowed(domain)
    status = "PASS" if allowed else "FAIL"
    msg = f"'{domain}' is in the allowlist" if allowed else (
        f"'{domain}' is NOT in the bash_tool allowlist — "
        "requests to this domain will fail. Check network_configuration in system prompt."
    )
    _print("NET-01", "Allowed outbound domain", status == "PASS", msg)
    print()
    if not allowed:
        print("VERDICT: FAIL")
        print(f"\n  Allowed domains: {', '.join(sorted(ALLOWED_DOMAINS))}")
        return 1
    print("VERDICT: PASS")
    return 0


def _print(gate: str, label: str, ok_or_status, msg: str):
    if isinstance(ok_or_status, bool):
        status = "PASS" if ok_or_status else "FAIL"
    else:
        status = ok_or_status
    icon = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}.get(status, "?")
    print(f"  {gate:<10} {icon}  {label}: {msg}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Platform constraints reference and payload checker (F-016 closure)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true",
                       help="List all known platform constraints")
    group.add_argument("--check-sql", metavar="SQL",
                       help="Check a SQL statement against D1 limits")
    group.add_argument("--check-json", metavar="JSON",
                       help="Check a JSON payload against MCP parameter limits")
    group.add_argument("--check-domain", metavar="DOMAIN",
                       help="Check if a domain is in the bash_tool allowlist")
    group.add_argument("--check-mcp-param", metavar="JSON",
                       help="Alias for --check-json (MCP parameter payload check)")

    args = parser.parse_args()

    if args.list:
        sys.exit(list_constraints())
    elif args.check_sql:
        sys.exit(check_sql(args.check_sql))
    elif args.check_json or args.check_mcp_param:
        payload = args.check_json or args.check_mcp_param
        sys.exit(check_json_payload(payload))
    elif args.check_domain:
        sys.exit(check_domain(args.check_domain))


if __name__ == "__main__":
    main()
