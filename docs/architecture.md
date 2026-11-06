ST Insurance Pool — Prototype Architecture
Document status: Prototype architecture
Version: 0.1
Purpose: Demonstration and evaluator presentation
Scope: Local, model-assisted claim evaluation workflow
Not production-ready: This prototype does not provide real insurance underwriting, provider refunds, cash settlement, or production-grade financial controls.
1. Architecture objectives
The prototype should demonstrate that ST can:
1. Accept a claim containing a requirement, model response, and execution evidence.
2. Ask a local LLM to analyze the claim against a defined evaluation framework.
3. Produce a structured evaluation report with findings, evidence references, severity, and a recommendation.
4. Validate the model output independently in backend code.
5. Apply deterministic eligibility and compensation calculations only to approved/simulated cases.
6. Persist claim records and expose them through a dashboard and claim-detail view.
7. Make model output, deterministic decisions, and simulated settlement visibly distinguishable.
The LLM is an evaluator assistant—not an authority for financial posting.
2. System context
Claimant / Presenter
        |
        v
React UI (Dashboard, Claim Submission, Claims, Claim Detail, Investigation)
        |
        v
FastAPI API Layer
        |
        +--> Claim Service ----------> SQLite Repository
        |
        +--> Evaluation Service
        |       |
        |       +--> Rule/Taxonomy/Schema Loader
        |       +--> Ollama Client --> Local Qwen2.5 0.5B model
        |       +--> Output Schema Validator
        |       +--> Policy Validator
        |
        +--> Investigation Service
        |
        +--> Settlement Service
                |
                +--> Compensation Engine
                +--> Reserve/Limit Engine
                +--> Simulated Ledger (prototype)
3. Component responsibilities
3.1 Frontend — frontend/
- src/App.jsx: application shell and route/page composition.
- src/pages/: dashboard, claim submission, claims list, claim detail, investigation, pool/ledger views.
- src/components/: reusable cards, tables, status labels, evaluation report sections.
- src/services/: HTTP calls to FastAPI.
- src/hooks/: reusable UI state and API hooks.
- src/styles/: shared visual styles.
The UI must label model-generated analysis and simulated financial effects. It must not imply that a real provider refund or real-world payout occurred.
3.2 API layer — backend/app/api/
Module	Responsibility
dashboard.py	Dashboard summaries and aggregate metrics
claims.py	Claim creation, listing, retrieval, and evaluation trigger
investigations.py	Investigation queue and review actions
settlements.py	Simulated settlement request and result
pool.py	Pool metadata and simulated balance/ledger views


API handlers should validate request shape, invoke services, and return response schemas. Business logic must not be embedded in route handlers.
3.3 Services — backend/app/services/
Module	Responsibility
claim_service.py	Claim lifecycle orchestration and persistence
evaluation_service.py	Load evaluation inputs, call model, validate output, create evaluation record
investigation_service.py	Manual-review workflow and investigator decisions
settlement_service.py	Settlement preconditions, orchestration, and simulated posting


Services coordinate components. They should not duplicate arithmetic or policy rules.
3.4 Evaluation engine — backend/app/engine/
Module	Responsibility
policy_validator.py	Enforce deterministic eligibility gates, mandatory-review conditions, and allowed decisions
compensation.py	Calculate requested/final token credits from verified usage and approved parameters
reserve.py	Apply configured prototype pool limits and reserve checks


The backend must reject malformed or unsupported model recommendations. A model response alone cannot approve a claim or create a credit.
3.5 Model integration — backend/app/integrations/llm/ollama_client.py
- Communicates with the local Ollama HTTP API.
- Uses OLLAMA_BASE_URL, OLLAMA_MODEL, and OLLAMA_TIMEOUT.
- Sends a compact, versioned evaluation prompt and relevant claim evidence.
- Requests structured JSON output where supported.
- Handles connection errors, timeout, malformed responses, and model unavailability.
- Does not silently convert an unavailable model into a successful evaluation.
3.6 Rules and evaluation assets — backend/rules/
- rules.md: evaluator instructions and rule definitions.
- taxonomy.md: failure categories, severity definitions, and review routing.
- evaluation_schema.json: machine-readable contract for model output.
- examples/positive/: examples where evidence supports satisfaction/no compensable failure.
- examples/negative/: examples with demonstrable requirement failures.
- examples/ambiguous/: insufficient or unclear evidence.
- examples/contradictory/: conflicting requirement, response, or evidence.
3.7 Persistence — backend/app/repositories/ and backend/app/models/
The prototype uses SQLite. Keep persistence access behind repository functions and data models.

Persist at least:
- Claim input and claim status.
- Evaluation input snapshot and model output.
- Evaluation/rules/schema/model version identifiers.
- Evidence references and findings.
- Deterministic validation result.
- Investigation decisions.
- Compensation calculation inputs and output.
- Simulated settlement/ledger entries.
- Timestamps and error states.
A model retry should not overwrite a previous evaluation silently; retain a new evaluation attempt or version.
4. Claim evaluation sequence
Claim submitted
    |
    v
Validate required claim fields and evidence references
    |
    v
Persist claim + immutable evaluation input snapshot
    |
    v
Load rules, taxonomy, schema, and versions
    |
    v
Call Ollama evaluator
    |
    +--> timeout/unavailable/invalid JSON --> evaluation error or manual review
    |
    v
Validate JSON against evaluation_schema.json
    |
    v
Run deterministic policy validation
    |
    +--> mandatory review / evidence gap / contradiction --> investigation
    |
    +--> ineligible or excluded case ------------------> rejection/zero compensation path
    |
    v
Create evaluation report and recommendation
    |
    v
Human review or prototype decision gate
    |
    v
Approved simulated case
    |
    v
Compensation + reserve/limit calculation
    |
    v
Simulated settlement / ledger entry
    |
    v
Dashboard and claim detail updated
5. Trust boundaries and safety controls
- User input is untrusted: requirement text, model response, attachments, and user-provided evidence may contain prompt injection or misleading claims.
- LLM output is untrusted: validate syntax, schema, enum values, evidence references, and decision consistency.
- Evidence is authoritative only according to its source: distinguish provider usage records, test outputs, logs, user statements, and model-generated explanations.
- No model-generated token counts or prices: token usage and pricing must come from verified records/configuration.
- No direct model-to-ledger path: settlement service accepts only validated, approved calculation objects.
- No arbitrary code execution: claim evaluation must not execute claimant-supplied code in this prototype.
- No real financial action: ledger and settlement are simulated and labeled accordingly.
- Prompt injection defense: treat claim text and model output as data, not instructions that can override evaluator rules.
- Failure handling: model/API errors must be recorded and surfaced; do not default to approval.
6. Model and policy separation
Decision/input	Responsible component
Identify candidate failure and explain evidence	LLM evaluator
Return structured findings and recommendation	LLM evaluator
Validate output structure and allowed values	Schema validator
Verify evidence references exist	Backend
Enforce eligibility/exclusions and review gates	Deterministic policy validator
Determine eligible token usage	Verified usage records + backend rules
Calculate credits and caps	Compensation/reserve engines
Approve real financial action	Not implemented
Record simulated settlement	Prototype settlement service


7. Runtime configuration
Read configuration from backend/.env (never commit this file). .env.example is the template.

Relevant settings:
- OLLAMA_BASE_URL: local Ollama API endpoint.
- OLLAMA_MODEL: model tag, initially qwen2.5:0.5b.
- OLLAMA_TIMEOUT: model request timeout in seconds.
- MODEL_CONFIDENCE_THRESHOLD: prototype routing threshold only; not a calibrated probability.
- MODEL_TEMPERATURE: generation temperature.
- MODEL_MAX_TOKENS: response limit.
- EVALUATION_MODE: prototype evaluation mode.
- DATABASE_URL: persistence connection.
8. Observability and error states
Record:
- Claim ID and evaluation attempt ID.
- Model tag and prompt/rules/schema versions.
- Start/end timestamps and latency.
- Model request status and error type.
- Schema validation result.
- Deterministic policy result.
- Manual-review reason.
- Compensation calculation result.
- Simulated settlement result.
Do not log secrets. Avoid storing unnecessary sensitive user content in logs.
9. Prototype limitations
This architecture is intentionally limited:
- A 0.5B local model is a demonstration model and is not expected to reliably adjudicate complex claims.
- The evaluation framework and examples are not a calibrated production evaluator.
- No provider billing reconciliation or universal token attribution is implemented unless explicitly wired to verified data.
- No production fraud detection, legal insurance structure, solvency analysis, or real money movement is implemented.
- UI status labels and transitions must be checked against the finalized FRD before being represented as authoritative.
- Human review is required for ambiguous, contradictory, unsupported, or high-impact cases.
10. Implementation order
1. Configuration and application startup.
2. Pydantic request/response models and database entities.
3. Repository functions and claim creation/list/detail.
4. Ollama client with timeout/error handling.
5. Rules/taxonomy/schema loader.
6. Evaluation service and schema validation.
7. Deterministic policy validator.
8. Compensation and reserve engines with unit tests.
9. Investigation and simulated settlement services.
10. API routes and frontend integration.
11. Evaluation test suite and presentation scenario.