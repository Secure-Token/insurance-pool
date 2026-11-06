def validate(a):
 required={"classification","confidence","findings","recommendation","rationale"}
 if not required<=a.keys(): raise ValueError(f"Missing assessment fields: {required-a.keys()}")
 if a["classification"] not in {"objective_failure","subjective","unclear"}: raise ValueError("Invalid classification")
 if not 0<=float(a["confidence"])<=1: raise ValueError("Confidence must be 0..1")
 if not isinstance(a["findings"],list): raise ValueError("findings must be an array")
 return a
def status(a):
 if a["classification"]=="subjective": return "REJECTED"
 if a["classification"]=="unclear" or float(a["confidence"])<.70: return "UNDER_INVESTIGATION"
 return "ELIGIBILITY_REVIEW"
