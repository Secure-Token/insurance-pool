from math import floor


def calculate(claim, assessment):
    classification = assessment["classification"]
    # Prototype: full compensation for failed task, half for partial failure.
    factor = 1.0 if classification == "objective_failure" else (
        0.5 if classification == "subjective" else 0.0
    )
    input_tokens = max(0, int(claim.get("input_tokens") or 0))
    output_tokens = max(0, int(claim.get("output_tokens") or 0))
    input_credits = floor(input_tokens * factor)
    output_credits = floor(output_tokens * factor)
    input_rate = float(claim.get("input_rate") or 0)
    output_rate = float(claim.get("output_rate") or 0)
    value = (input_credits * input_rate + output_credits * output_rate) / 1_000_000
    return {
        "factor": factor,
        "recommended_input_credits": input_credits,
        "recommended_output_credits": output_credits,
        "estimated_value": round(value, 8),
        "unit": "internal demo credits",
    }
