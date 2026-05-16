# Configuration Format — utility-session-manager

All project-specific config in D1 `session_config` table.

## Config Entry Types

### 1. Briefing Format
```
config_type = "session_manager_briefing_format_[PROJECT_ID]"
content = """
[BRIEFING_FIELDS]
field_1 = [NAME] | source = [TABLE] | filter = [WHERE] | format = "[TEMPLATE]"
field_2 = ...

[CONDITIONAL_ALERTS]
condition_1 = [EXPR]
alert_1 = "[MESSAGE]"
"""
```

### 2. Sequencer Mode
```
config_type = "session_manager_sequencer_mode_[PROJECT_ID]"
content = """
mode = dependency_order
dependency_table = [TABLE]
task_status_table = [TABLE]
status_join_key = [JOIN_EXPR]

[EXIT_GATES_ENABLED]
gate_task_specificity = true
gate_alternatives_considered = true
gate_uncertainty_surfaced = true
"""
```

### 3. Handoff Schema
```
config_type = "session_manager_handoff_schema_[PROJECT_ID]"
content = """
[HANDOFF_FIELDS]
field = [NAME] | type = TEXT|AUDIT | required = yes|no | constraint = [TYPE] | source = [SOURCE]

[OPTIONAL_FIELDS]
field = [NAME] | required_if = [COND]
"""
```

### 4. RENAME_BLOCK Gate
```
config_type = "session_manager_gates_rename_block_gate_[PROJECT_ID]"
content = """
[GATE_NAME] RENAME_BLOCK_GATE
[WHEN] before_output

[FIELD_BINDING]
WORKSTREAM ← session_handoff.workstream
N ← extract_session_number(session_handoff.stopped_at)
TASK_ID ← extract_task_id(session_handoff.next_action)

[VALIDATION]
format = "[WORKSTREAM] · S[N] · [TASK_ID]"
backtick_count = exactly_4
field_sources = D1_data_only

[FAILURE] HALT_before_sending
"""
```

### 5. HANDOFF_CONTENT Gate
```
config_type = "session_manager_gates_handoff_content_gate_[PROJECT_ID]"
content = """
[GATE_NAME] HANDOFF_CONTENT_GATE
[WHEN] before_write_to_d1

[REQUIRED_FIELDS_CHECK]
For each field in schema where required=true:
  If empty: prompt to fill OR error if context exhausted

[NO_SILENT_THINNING]
NEVER truncate without confirmation

[VERIFICATION_AFTER_WRITE]
After D1 INSERT: re-fetch and compare all fields
"""
```

## design_dependencies Table

Separate D1 table (not session_config).

**Schema:**
```
id | project_id | level | name | subsystems | blocks | requires | status | created_at | updated_at
```

**Used by:** @sequencer for dependency ordering.

## Storage & Versioning

- Config stored in D1 with updated_at
- Lock config entries in decisions table when stable
- Changes to config = STRUCTURAL (dispatcher routing only, never behavioral additions)
