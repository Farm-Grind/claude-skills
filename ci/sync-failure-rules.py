#!/usr/bin/env python3
"""
sync-failure-rules.py

Queries D1 claude-config for the current validation_rules and failure_patterns,
writes ci/failure-audit-rules.json in the clone, then stages it for push.

Run this after any D1 update to keep CI in sync with the source of truth.
Usage: python3 ci/sync-failure-rules.py <repo_root>

The actual D1 query is executed via the Cloudflare MCP in the Claude session;
this script documents the query and writes the output to the repo path.

In practice, Claude executes the D1 query via the MCP tool, formats the output
as JSON matching the failure-audit-rules.json schema, writes the file, and pushes.

Manual steps (paste into Claude when updating D1):
1. Query D1:
   SELECT rule_id, applies_to, trigger_condition, check_description, linked_patterns
   FROM validation_rules ORDER BY rule_id
2. Query D1:
   SELECT pattern_code, name, severity FROM failure_patterns
3. Query D1:
   SELECT finding_id, pattern_code, title, artifact_affected, project_scope
   FROM granular_findings WHERE status = 'OPEN'
4. Regenerate failure-audit-rules.json from query results
5. Write to ci/failure-audit-rules.json in clone
6. git add ci/failure-audit-rules.json && git commit -m "sync: failure audit rules from D1" && git push
"""

DATABASE_ID = "afd78e0e-583e-4e78-87fc-dd6bc8150ce9"
REPO_PATH = "ci/failure-audit-rules.json"

STATIC_CHECK_IMPLEMENTATIONS = {
    "VR-01": "validate.py:check_reference_files()",
    "VR-02": "validate.py:check_line_count(hard_limit=500)",
    "VR-04": "validate.py:GREP_CHECKS banned arxiv IDs",
    "VR-05": "validate.py:check_trigger_vocabulary()",
    "VR-11": "validate.py:check_project_scope_contamination()",
    "VR-12": "validate.py:check_self_application_rule()",
}

if __name__ == "__main__":
    print("This script documents the sync process.")
    print("Execute via Claude + Cloudflare MCP in a session.")
    print(f"Target file: {REPO_PATH}")
    print(f"D1 database: {DATABASE_ID}")
