
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB_PATH = Path("./st_pool.db")
NOW = datetime.now(timezone.utc)

def timestamp(days_ago=0, hours_ago=0):
    return (NOW - timedelta(days=days_ago, hours=hours_ago)).isoformat()

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

# Ensure tables exist
conn.executescript("""
CREATE TABLE IF NOT EXISTS claims (
    id TEXT PRIMARY KEY,
    claimant_id TEXT,
    task_id TEXT,
    requirement TEXT,
    response_text TEXT,
    reason TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    input_rate REAL,
    output_rate REAL,
    evidence TEXT,
    status TEXT,
    evaluation TEXT,
    rec_input INTEGER DEFAULT 0,
    rec_output INTEGER DEFAULT 0,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS investigations (
    id TEXT PRIMARY KEY,
    claim_id TEXT,
    notes TEXT,
    status TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS settlements (
    id TEXT PRIMARY KEY,
    claim_id TEXT,
    input_credits INTEGER,
    output_credits INTEGER,
    total_credits INTEGER,
    status TEXT,
    created_at TEXT
);
""")

claims = [
    ("CLM-DEMO-001", "USER-001", "TASK-101", "Generate a Python function with unit tests.", "Function generated without unit tests.", "REQUIREMENT_MISSED", "UNDER_INVESTIGATION"),
    ("CLM-DEMO-002", "USER-002", "TASK-102", "Return valid JSON with three fields.", "Returned malformed JSON.", "INCORRECT_OUTPUT", "APPROVED"),
    ("CLM-DEMO-003", "USER-003", "TASK-103", "Explain database indexing with examples.", "Explanation omitted examples.", "INCOMPLETE_OUTPUT", "SETTLED"),
    ("CLM-DEMO-004", "USER-004", "TASK-104", "Refactor code without changing behavior.", "Refactoring introduced a regression.", "REGRESSION", "SUBMITTED"),
    ("CLM-DEMO-005", "USER-005", "TASK-105", "Create SQL query with aggregation.", "Query omitted GROUP BY.", "INCORRECT_OUTPUT", "UNDER_ASSESSMENT"),
    ("CLM-DEMO-006", "USER-006", "TASK-106", "Provide a complete API implementation.", "Only partial implementation returned.", "INCOMPLETE_OUTPUT", "APPROVED"),
    ("CLM-DEMO-007", "USER-007", "TASK-107", "Generate optimized Python code.", "Output failed performance requirement.", "REQUIREMENT_MISSED", "SETTLED"),
    ("CLM-DEMO-008", "USER-008", "TASK-108", "Produce a valid CSV dataset.", "CSV columns were inconsistent.", "INCORRECT_OUTPUT", "REJECTED"),
    ("CLM-DEMO-009", "USER-009", "TASK-109", "Implement error handling.", "Exception handling was incomplete.", "INCOMPLETE_OUTPUT", "SUBMITTED"),
    ("CLM-DEMO-010", "USER-010", "TASK-110", "Preserve existing function signatures.", "Function signature was changed.", "REGRESSION", "UNDER_INVESTIGATION"),
    ("CLM-DEMO-011", "USER-011", "TASK-111", "Create documentation with examples.", "Examples were missing.", "REQUIREMENT_MISSED", "SUBMITTED"),
    ("CLM-DEMO-012", "USER-012", "TASK-112", "Return output in requested format.", "Output format was incorrect.", "OTHER", "UNDER_ASSESSMENT"),
]

for i, item in enumerate(claims):
    cid, claimant, task, req, response, reason, status = item

    # Do not overwrite records already present
    exists = conn.execute(
        "SELECT 1 FROM claims WHERE id=?", (cid,)
    ).fetchone()

    if exists:
        continue

    input_tokens = 400 + i * 75
    output_tokens = 150 + i * 35
    input_rate = 2.0
    output_rate = 8.0

    rec_input = round(input_tokens * input_rate / 1_000_000, 6)
    rec_output = round(output_tokens * output_rate / 1_000_000, 6)

    evaluation = {
        "demo": True,
        "score": 0.35 + (i % 5) * 0.1,
        "summary": "Demo evaluation result for presentation.",
        "findings": [
            "Requirement compliance issue identified.",
            "Evidence reviewed against submitted output."
        ],
        "calculation": {
            "recommended_input_credits": rec_input,
            "recommended_output_credits": rec_output,
            "total_recommended_credits": rec_input + rec_output
        }
    }

    conn.execute("""
        INSERT INTO claims (
            id, claimant_id, task_id, requirement, response_text,
            reason, input_tokens, output_tokens, input_rate, output_rate,
            evidence, status, evaluation, rec_input, rec_output,
            created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cid, claimant, task, req, response, reason,
        input_tokens, output_tokens, input_rate, output_rate,
        "DEMO: Requirement mismatch documented for evaluator.",
        status, json.dumps(evaluation),
        rec_input, rec_output,
        timestamp(days_ago=i), timestamp(days_ago=i)
    ))

# Investigations
investigations = [
    ("INV-DEMO-001", "CLM-DEMO-001", "Review requirement compliance and output evidence."),
    ("INV-DEMO-002", "CLM-DEMO-010", "Investigate regression introduced by generated code."),
    ("INV-DEMO-003", "CLM-DEMO-005", "Verify SQL correctness against original requirement."),
    ("INV-DEMO-004", "CLM-DEMO-006", "Validate completeness of API implementation."),
]

for iid, cid, notes in investigations:
    conn.execute("""
        INSERT OR IGNORE INTO investigations
        VALUES (?, ?, ?, ?, ?)
    """, (iid, cid, notes, "OPEN", timestamp(days_ago=1)))

# Settlements - simulated only
settlements = [
    ("SET-DEMO-001", "CLM-DEMO-003", 10, 15, 25),
    ("SET-DEMO-002", "CLM-DEMO-007", 12, 18, 30),
]

for sid, cid, input_credits, output_credits, total in settlements:
    conn.execute("""
        INSERT OR IGNORE INTO settlements
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        sid, cid, input_credits, output_credits,
        total, "SIMULATED", timestamp(days_ago=2)
    ))

conn.commit()
conn.close()

print("Demo data seeded successfully.")
print("Claims: 12 | Investigations: 4 | Settlements: 2")
print("All settlement records are simulated.")
