# ST Insurance Pool — Evaluation Rules (Prototype)

**Document status:** Prototype evaluator policy; not a finalized insurance policy.  
**Purpose:** Define a repeatable, evidence-grounded assessment of an AI interaction after a user reports that the response did not satisfy the recorded requirement.

## 1. Authority and scope

1. The finalized ST FRD and Database Schema Handoff remain authoritative for product requirements and persisted structures.
2. This file specifies evaluator behavior only. It must not silently amend claim eligibility, lifecycle, compensation, settlement, or schema rules.
3. If a rule here conflicts with the FRD, schema handoff, or an approved policy version, stop automated processing and flag `POLICY_CONFLICT`.
4. The model produces an assessment/recommendation. It does **not** approve claims, calculate authoritative compensation, post wallet credits, or execute settlement.
5. A demo must display `SIMULATED / NON-FINANCIAL` and must not imply a real provider refund or cash payment.

## 2. Evaluation inputs

The evaluator may receive:
- `requirement`: the user's recorded requirement/baseline, preferably immutable and timestamped.
- `response`: the model's response or output artifact.
- `execution_context`: relevant, bounded context such as tool outputs, files changed, test results, and execution events.
- `usage_records`: provider- or middleware-reported token usage, including provenance and attribution.
- `claim_context`: claim ID, interaction ID, coverage/policy identifiers and submitted reason, where available.
- `evidence`: user-provided evidence and system-collected evidence with source identifiers.
- `evaluation_policy`: versioned rules, threshold settings and permitted evaluator dimensions.

Missing input is not permission to infer it. Record missing evidence explicitly.

## 3. Evidence and provenance rules

- Distinguish **observed fact**, **user assertion**, **tool/test result**, **model inference**, and **unknown**.
- Every material finding must cite one or more evidence IDs or explicitly state `evidence_missing`.
- Never fabricate logs, test results, file changes, token counts, provider charges, timestamps, or requirement text.
- A model-generated explanation is not independent proof of its own correctness.
- Prefer reproducible executable evidence (tests/build/static checks) for claims about code behavior; do not treat a passing test suite as proof of full requirement satisfaction.
- Preserve contradictory evidence; do not silently choose the convenient side.
- Do not treat user dissatisfaction alone as objective technical failure.
- Do not infer causality merely because an error occurred after an AI response.

## 4. Evaluation dimensions

Assess only dimensions supported by available evidence. Each dimension uses `PASS`, `FAIL`, `PARTIAL`, `NOT_ASSESSED`, or `CONFLICTING`.

### 4.1 Requirement alignment
Compare output against explicit, recorded acceptance criteria. Identify:
- satisfied criteria;
- unmet criteria;
- partially satisfied criteria;
- criteria that are ambiguous, missing, or mutually inconsistent.

### 4.2 Factual / semantic correctness
Check claims against supplied authoritative context or verifiable evidence. Mark unsupported claims as `UNVERIFIED`, not automatically false.

### 4.3 Functional correctness
Use actual test/build/runtime evidence where available. Report test command, environment, result, and evidence reference. Do not claim execution if no execution evidence exists.

### 4.4 Completeness
Identify omitted requested deliverables, steps, constraints, or output sections.

### 4.5 Constraint compliance
Check explicit constraints (format, language, tools, architecture, scope, safety boundaries) individually.

### 4.6 Execution/tool integrity
Report tool failures, partial execution, missing artifacts, timeouts, or environment problems separately from model reasoning errors.

### 4.7 User preference / subjective quality
Capture preference mismatch separately. Subjective dissatisfaction alone cannot establish objectively compensable failure.

## 5. Failure taxonomy (prototype labels)

The labels below are evaluator taxonomy identifiers, not final claim rejection codes. The taxonomy is deliberately conservative and can be revised only through version control.

| Code | Meaning | Typical evidence |
|---|---|---|
| `REQ_MISUNDERSTOOD` | Response materially misinterprets explicit requirement | Requirement text vs response |
| `REQ_OMITTED` | Explicit acceptance criterion not addressed | Criterion checklist |
| `FACT_UNSUPPORTED` | Material assertion lacks supplied/verifiable support | Citation/source audit |
| `FACT_INCORRECT` | Material assertion contradicted by reliable evidence | Contradictory source |
| `OUTPUT_INCOMPLETE` | Required deliverable is missing or unfinished | Expected vs delivered artifacts |
| `FUNCTIONAL_FAILURE` | Output fails a relevant reproducible test or execution | Test/build/runtime record |
| `CONSTRAINT_VIOLATION` | Explicit constraint breached | Constraint-to-output comparison |
| `TOOL_FAILURE` | Tool/API/environment prevented or corrupted execution | Tool trace/error |
| `CONTEXT_FAILURE` | Relevant context was missing, ignored, or misapplied | Context record and response |
| `AMBIGUOUS_REQUIREMENT` | Requirement cannot be assessed uniquely | Requirement analysis |
| `CONTRADICTORY_EVIDENCE` | Evidence supports incompatible conclusions | Evidence set |
| `SUBJECTIVE_MISMATCH` | User dislikes quality/style despite no demonstrated objective violation | User feedback |
| `UNKNOWN_FAILURE` | Failure cannot be responsibly classified | Insufficient evidence |

Multiple findings are allowed. Each finding must state whether it is primary or contributing; do not force mutually exclusive categories.

## 6. Severity (assessment only)

Severity describes impact, not eligibility or compensation by itself.

- `LOW`: minor, localized deviation; core objective remains usable.
- `MEDIUM`: material deficiency; meaningful correction/rework required.
- `HIGH`: major failure affecting a core acceptance criterion or making output unusable for intended task.
- `CRITICAL`: severe failure with broad impact, destructive/unsafe behavior, or loss of essential work. Use only with explicit evidence and human review.

Severity is `UNASSESSED` when impact cannot be established. Do not map severity to a compensation percentage unless an approved policy explicitly defines that mapping.

## 7. Confidence and routing

Confidence is a calibrated evaluator estimate of the **assessment**, not a probability of claim approval or payment.

- Return a numeric confidence in `[0,1]` only when the evaluator can support it.
- Confidence must not override missing evidence, contradictory evidence, policy conflicts, mandatory review, or suspected manipulation.
- Low confidence, ambiguous requirements, missing provenance, conflicting evidence, unknown failures, or unsupported usage attribution should route to `MANUAL_REVIEW`.
- A high-confidence model recommendation is still advisory and must pass backend validation and configured policy gates.
- The initial prototype threshold (if configured as `0.70`) is a routing experiment only; it is not a finalized business policy. Equality behavior must be defined in code/config and tested.

## 8. Token usage and compensation boundary

The evaluator must not invent or estimate billable usage.

- `I_a`: actual billed input tokens attributable to the affected task/call.
- `O_a`: actual billed output tokens attributable to the failed task/call.
- `I_u`: original user prompt tokens.
- `I_s`: billed input-token contribution attributable to ST-added requirement expansion.
- `I_e = min(I_s, I_a)` only when attribution is defensible; otherwise usage attribution is unresolved.
- `O_e`: actual billed output usage attributable to the failed task; exclude unrelated calls and internal ST-generated output.
- Category C / subjective-only findings have zero compensation under the discussed prototype treatment.
- Category B / unresolved attribution or ambiguous failure requires manual adjudication.
- Deterministic backend calculation—not the LLM—applies approved factors, caps, pricing, rounding, and allocation rules.
- Missing optional limits must not be interpreted as zero. Missing required financial parameters must block calculation.
- Credits are internal ST units unless a separately approved policy defines otherwise; do not describe them as provider refunds or cash.

## 9. Decision recommendation vocabulary

The model may recommend one of:
- `RECOMMEND_APPROVAL`
- `RECOMMEND_PARTIAL_APPROVAL`
- `RECOMMEND_REJECTION`
- `RECOMMEND_MANUAL_REVIEW`
- `RECOMMEND_WITHHOLD`

These are recommendations, not state transitions. Backend services must enforce allowed lifecycle transitions, authorization, evidence requirements, and policy version.

## 10. Mandatory manual review triggers

Always recommend manual review when any applies:
- requirement is missing, ambiguous, impossible, or changed after execution;
- evidence is contradictory or materially incomplete;
- usage is absent, inconsistent, or not attributable;
- evaluator/tool execution failed;
- potential abuse, prompt injection, evidence manipulation, replay, or claim duplication is indicated;
- policy/FRD/schema conflict exists;
- proposed result would require an override;
- confidence is below configured routing threshold;
- impact is CRITICAL;
- model output is invalid or fails schema validation.

## 11. Output and validation

- Output must conform exactly to `evaluation_schema.json`.
- No extra keys unless schema is deliberately versioned.
- `null`/`NOT_ASSESSED` must be used for unknown values; never fill gaps with guesses.
- Backend validates IDs, evidence references, enums, numeric bounds, policy version, and recommendation permissions.
- Invalid output is rejected, logged, and retried only under bounded retry policy; persistent failure becomes manual review.
- Keep raw model output, normalized result, evaluator/model version, prompt/rules version, timestamp, and validation errors for reproducibility—subject to data minimization and retention policy.

## 12. Versioning

Version this file and `evaluation_schema.json` together. Every evaluation record should identify:
- rules version;
- schema version;
- model/provider and model version;
- prompt/template version;
- evaluator configuration;
- timestamp;
- input/evidence snapshot or immutable references.

Do not retroactively apply a new evaluator policy to historical claims without an approved recalculation process.
