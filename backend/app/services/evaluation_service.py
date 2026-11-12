import logging
import uuid
import re

from app.services.claim_service import get, save
from app.integrations.llm.ollama_client import assess_claim
from app.engine.policy_validator import validate, status
from app.engine.compensation import calculate
from app.services.settlement_service import settle

logger = logging.getLogger(__name__)
SCHEMA_VERSION = "1.0.0"


def _evaluation_prompt(claim):
    return f"""
You are evaluating a submitted AI-task failure claim for a prototype credit pool.
Assess ANY task type (coding, math, writing, research, reasoning, formatting,
tool use, or other). Compare only the stated requirement, response, and evidence.

Return exactly one JSON object matching the provided evaluation schema fields.
Use:
- evaluation_status: COMPLETED, PARTIAL, INSUFFICIENT_EVIDENCE, EVALUATOR_ERROR
- criterion status: PASS, FAIL, PARTIAL, NOT_ASSESSED, CONFLICTING
- recommendation: RECOMMEND_APPROVAL when task failed and compensation is warranted;
  RECOMMEND_PARTIAL_APPROVAL for partial failure; RECOMMEND_REJECTION when task
  was fulfilled/no compensable failure; RECOMMEND_MANUAL_REVIEW only if evidence
  truly prevents a decision; RECOMMEND_WITHHOLD for unresolved conflict.
- A truthful limitation can still mean the requested task was not completed.
  For this prototype, classify unfulfilled requirements as compensable unless
  the user explicitly asked only for a limitation/feasibility assessment.
- manual_review_required=false for a usable decision.
- severity LOW/MEDIUM/HIGH/CRITICAL; confidence 0..1 or null.
- Do not invent evidence, criteria, call IDs, or token usage.
- findings must use the schema's allowed codes/fields.
- usage_attribution token counts may copy the claim values; status UNVERIFIED.
- Include all required top-level schema fields.
This is a prototype assessment, not real insurance advice or settlement.

CLAIM:
requirement: {str(claim.get('requirement',''))[:12000]}
response: {str(claim.get('response_text',''))[:16000]}
reason: {str(claim.get('reason',''))[:3000]}
evidence: {str(claim.get('evidence') or 'none')[:8000]}
claim_id: {claim.get('id')}
interaction_id: {claim.get('interaction_id')}
input_tokens: {claim.get('input_tokens')}
output_tokens: {claim.get('output_tokens')}
"""


def _fallback(claim, message):
    return {
        "schema_version": SCHEMA_VERSION,
        "evaluation_id": str(uuid.uuid4()),
        "claim_id": claim.get("id"),
        "interaction_id": claim.get("interaction_id"),
        "evaluation_status": "EVALUATOR_ERROR",
        "requirement_assessment": {
            "requirement_available": bool(claim.get("requirement")),
            "summary": message,
            "criteria": [],
        },
        "dimensions": [],
        "findings": [],
        "severity": "UNASSESSED",
        "confidence": 0.0,
        "evidence_summary": message,
        "missing_evidence": [],
        "contradictions": [],
        "recommendation": "RECOMMEND_MANUAL_REVIEW",
        "manual_review_required": True,
        "review_reasons": [message],
        "usage_attribution": {
            "status": "UNVERIFIED", "affected_call_ids": [],
            "input_tokens": claim.get("input_tokens"),
            "output_tokens": claim.get("output_tokens"),
            "source_refs": [], "notes": "Copied from claim record; not verified.",
        },
        "policy_refs": {
            "rules_version": "v1", "taxonomy_version": "v1",
            "evaluation_policy_version": "v1",
        },
        "limitations": ["Prototype evaluator; not a real-world settlement decision."],
    }


def _normalize(raw, claim):
    if not isinstance(raw, dict):
        raise ValueError("Evaluator response must be a JSON object")
    # Fill optional omissions without masking invalid decision values.
    raw.setdefault("schema_version", SCHEMA_VERSION)
    raw.setdefault("evaluation_id", str(uuid.uuid4()))
    raw["claim_id"] = claim.get("id")
    raw["interaction_id"] = claim.get("interaction_id")
    raw.setdefault("requirement_assessment", {
        "requirement_available": bool(claim.get("requirement")),
        "summary": raw.get("evidence_summary", ""),
        "criteria": [],
    })
    raw.setdefault("dimensions", [])
    raw.setdefault("findings", [])
    raw.setdefault("severity", "UNASSESSED")
    raw.setdefault("confidence", None)
    raw.setdefault("evidence_summary", "")
    raw.setdefault("missing_evidence", [])
    raw.setdefault("contradictions", [])
    raw.setdefault("manual_review_required", False)
    raw.setdefault("review_reasons", [])
    raw.setdefault("usage_attribution", {
        "status": "UNVERIFIED", "affected_call_ids": [],
        "input_tokens": claim.get("input_tokens"),
        "output_tokens": claim.get("output_tokens"),
        "source_refs": [], "notes": "Copied from claim record; not verified.",
    })
    raw.setdefault("policy_refs", {
        "rules_version": "v1", "taxonomy_version": "v1",
        "evaluation_policy_version": "v1",
    })
    raw.setdefault("limitations", ["Prototype evaluation only."])
    return raw


def _adapt(e):
    rec = e["recommendation"]
    criteria = e.get("requirement_assessment", {}).get("criteria", [])
    statuses = [c.get("status") for c in criteria if isinstance(c, dict)]
    findings = [
        f'{f.get("code", "FINDING")}: {f.get("description", "")}'
        for f in e.get("findings", []) if isinstance(f, dict)
    ]
    if rec == "RECOMMEND_APPROVAL":
        classification = "objective_failure"
    elif rec == "RECOMMEND_PARTIAL_APPROVAL":
        classification = "subjective"
    elif rec == "RECOMMEND_REJECTION":
        classification = "no_failure"
    else:
        classification = "unclear"
    # Preserve schema output and make compensation decision explicit.
    return {
        "classification": classification,
        "confidence": float(e.get("confidence") or 0.0),
        "findings": findings,
        "recommendation": rec,
        "rationale": e.get("evidence_summary") or
                     e.get("requirement_assessment", {}).get("summary", ""),
        "evaluation": e,
        "criteria_statuses": statuses,
        "manual_review_required": bool(e.get("manual_review_required")),
    }


def _deterministic_arithmetic(claim):
    requirement = str(claim.get("requirement") or "").strip().lower()
    response = str(claim.get("response_text") or "").strip()

    match = re.search(
        r"(?:calculate|compute|what is)?\s*(\d+(?:\.\d+)?)\s*(?:multiplied by|\*|×)\s*(\d+(?:\.\d+)?)",
        requirement
    )

    if not match:
        return None

    expected = float(match.group(1)) * float(match.group(2))

    numbers = re.findall(
        r"(?<![\w.])-?\d+(?:\.\d+)?",
        response.replace(",", "")
    )

    if not numbers:
        return None

    actual = float(numbers[-1])
    passed = abs(actual - expected) <= 1e-9

    return {
        "schema_version": SCHEMA_VERSION,
        "evaluation_id": str(uuid.uuid4()),
        "claim_id": claim.get("id"),
        "interaction_id": claim.get("interaction_id"),
        "evaluation_status": "COMPLETED",
        "requirement_assessment": {
            "requirement_available": True,
            "summary": f"Expected {expected:g}, observed {actual:g}.",
            "criteria": [{
                "criterion_id": "ARITHMETIC_RESULT",
                "description": "Arithmetic result matches requirement",
                "status": "PASS" if passed else "FAIL",
                "expected": str(expected),
                "observed": str(actual)
            }]
        },
        "dimensions": [],
        "findings": [] if passed else [{
            "code": "INCORRECT_OUTPUT",
            "description": "Arithmetic result does not match expected value"
        }],
        "severity": "LOW" if passed else "HIGH",
        "confidence": 1.0,
        "evidence_summary": f"Expected {expected:g}; actual {actual:g}.",
        "missing_evidence": [],
        "contradictions": [],
        "recommendation": (
            "RECOMMEND_REJECTION"
            if passed else "RECOMMEND_APPROVAL"
        ),
        "manual_review_required": False,
        "review_reasons": [],
        "usage_attribution": {
            "status": "UNVERIFIED",
            "affected_call_ids": [],
            "input_tokens": claim.get("input_tokens"),
            "output_tokens": claim.get("output_tokens"),
            "source_refs": [],
            "notes": "Token usage copied from claim."
        },
        "policy_refs": {
            "rules_version": "v1",
            "taxonomy_version": "v1",
            "evaluation_policy_version": "v1"
        },
        "limitations": ["Deterministic arithmetic evaluation."]
    }


async def evaluate(cid):
    claim = get(cid)
    if not claim:
        raise LookupError("Claim not found")
    try:
        evaluation = _deterministic_arithmetic(claim)

        if evaluation is None:
            payload = dict(claim)
            payload["evaluation_prompt"] = _evaluation_prompt(claim)
            evaluation = _normalize(
                await assess_claim(payload),
                claim
            )

    except Exception as exc:
        logger.exception("Evaluation failed for claim %s", cid)
        evaluation = _fallback(claim, f"Evaluator error: {type(exc).__name__}")
    assessment = validate(_adapt(evaluation))
    calculation = calculate(claim, assessment)
    claim_status = status(assessment)

    result = save(cid, assessment, calculation, claim_status)

    if claim_status in ("APPROVED", "PARTIALLY_APPROVED"):
        settle(cid)

    return result