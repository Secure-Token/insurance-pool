# ST Insurance Pool — Failure Taxonomy (Prototype)

**Status:** Prototype classification vocabulary; not final claim codes or finalized policy. See `rules.md`.

## Classification principles
1. Classify the observed defect, not the claimant's emotion or the evaluator's confidence.
2. One execution may contain multiple findings; identify one primary finding only when evidence supports it.
3. Separate AI reasoning/output defects from external tool/provider/environment failures.
4. Distinguish `FAIL`, `PARTIAL`, `NOT_ASSESSED`, and `CONFLICTING`; absence of evidence is not evidence of failure.
5. Findings are assessment data. Claim eligibility, compensation, and lifecycle decisions remain governed by approved policy and backend controls.

## Codes

| Code | Class | Definition | Evidence examples | Common false-positive risk |
|---|---|---|---|---|
| `REQ_MISUNDERSTOOD` | Requirement | Materially interpreted explicit requirement incorrectly | Baseline, response, criterion mapping | Ambiguous prompt |
| `REQ_OMITTED` | Requirement | Explicit criterion not addressed | Acceptance checklist | Criterion implied but not explicit |
| `REQ_CONFLICT` | Requirement | Requirements conflict and cannot all be met | Requirement clauses | Evaluator overlooking precedence |
| `REQ_AMBIGUOUS` | Requirement | Requirement has multiple plausible interpretations | Baseline text/context | Evaluator treating one interpretation as obvious |
| `FACT_UNSUPPORTED` | Factual | Material assertion has no adequate evidence | Sources/citations | Missing citation where claim is nevertheless true |
| `FACT_INCORRECT` | Factual | Assertion contradicted by reliable evidence | Authoritative source | Source stale or inapplicable |
| `HALLUCINATED_ARTIFACT` | Factual/artifact | Claims file/code/action exists without evidence | Workspace inventory, logs | Artifact exists outside inspected scope |
| `OUTPUT_INCOMPLETE` | Output | Required output/artifact absent or unfinished | Deliverable list vs output | Requirement did not require completion |
| `FUNCTIONAL_FAILURE` | Functional | Output fails reproducible relevant behavior/test | Test/build/runtime evidence | Test invalid or environment-dependent |
| `REGRESSION` | Functional | Change breaks previously working behavior | Before/after tests or diff | Baseline not comparable |
| `CONSTRAINT_VIOLATION` | Constraint | Explicit constraint breached | Constraint list, output | Constraint was superseded |
| `FORMAT_VIOLATION` | Constraint | Required structure/format not followed | Requested vs delivered format | Cosmetic variation accepted |
| `TOOL_FAILURE` | Execution | Tool/API/environment error interrupts task | Trace, error, status | Model caused invalid tool call |
| `EXECUTION_PARTIAL` | Execution | Task only partly executed | Execution events/artifacts | Partial output was intended |
| `CONTEXT_OMISSION` | Context | Relevant supplied context not used | Context snapshot vs output | Context irrelevant |
| `CONTEXT_CORRUPTION` | Context | Context inaccurate, truncated, or mismatched | Context provenance | Source itself erroneous |
| `SUBJECTIVE_MISMATCH` | Preference | Preference/style dissatisfaction without objective defect | User feedback | Hidden explicit preference ignored |
| `EXTERNAL_FAILURE` | External | Failure attributable to provider/service outside model output | Provider/tool status | Attribution not established |
| `UNKNOWN_FAILURE` | Unknown | Available evidence cannot classify failure | Evidence inventory | Prematurely used instead of collecting evidence |

## Finding attributes

Each finding should include:
- `code`: one taxonomy code;
- `level`: `REQUIREMENT`, `INTERACTION`, `EXECUTION`, `MODEL_CALL`, or `ARTIFACT`;
- `role`: `PRIMARY`, `CONTRIBUTING`, or `SECONDARY`;
- `impact`: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`, or `UNASSESSED`;
- `description`: concise, evidence-based explanation;
- `evidence_refs`: zero or more evidence IDs; empty list requires `evidence_missing_reason`;
- `affected_criteria`: criterion IDs, if applicable;
- `confidence`: `[0,1]` or null;
- `compensability_signal`: `POTENTIALLY_ELIGIBLE`, `NOT_ELIGIBLE_UNDER_PROTOTYPE`, `UNRESOLVED`, or `NOT_EVALUATED`.

`compensability_signal` is not an approval. It must not directly create wallet credits or settlements.

## Prototype category mapping (non-authoritative)

For demonstration only:
- **A — Potentially objective failure:** `REQ_MISUNDERSTOOD`, `REQ_OMITTED`, `FACT_INCORRECT`, `OUTPUT_INCOMPLETE`, `FUNCTIONAL_FAILURE`, `CONSTRAINT_VIOLATION`, subject to coverage/evidence/attribution checks.
- **B — Ambiguous / requires adjudication:** `REQ_AMBIGUOUS`, `REQ_CONFLICT`, `TOOL_FAILURE`, `EXECUTION_PARTIAL`, `CONTEXT_OMISSION`, `EXTERNAL_FAILURE`, `UNKNOWN_FAILURE`, contradictory evidence, or uncertain causality.
- **C — Subjective-only / no objective failure demonstrated:** `SUBJECTIVE_MISMATCH` alone.

This mapping is provisional and must not be represented as finalized policy or as an automatic claim outcome.
