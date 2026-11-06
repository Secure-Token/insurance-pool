from math import floor
def calculate(claim,a):
 # Conservative demo: only high-confidence objective classification yields recommendation.
 factor=1 if a["classification"]=="objective_failure" and float(a["confidence"])>=.70 else 0
 i=floor(claim["input_tokens"]*factor); o=floor(claim["output_tokens"]*factor)
 value=(i*claim["input_rate"]+o*claim["output_rate"])/1_000_000
 return {"factor":factor,"recommended_input_credits":i,"recommended_output_credits":o,"estimated_value":round(value,8),"unit":"internal demo credits"}
