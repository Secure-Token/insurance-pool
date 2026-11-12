def validate(a):
    required = {"classification", "confidence", "findings", "recommendation", "rationale"}
    if not isinstance(a, dict) or not required <= a.keys():
        raise ValueError("Assessment missing required fields")
    if a["classification"] not in {"objective_failure", "subjective", "no_failure", "unclear"}:
        raise ValueError("Invalid classification")
    confidence = float(a["confidence"])
    if not 0 <= confidence <= 1:
        raise ValueError("Confidence must be 0..1")
    if not isinstance(a["findings"], list) or not isinstance(a["rationale"], str):
        raise ValueError("Invalid findings or rationale")
    return a


def status(a):
    # Only return values present in the database claim_status controlled values.
    classification = a["classification"]
    if classification == "objective_failure":
        return "APPROVED"
    if classification == "subjective":
        return "PARTIALLY_APPROVED"
    if classification == "no_failure":
        return "REJECTED"
    return "INVESTIGATING"
