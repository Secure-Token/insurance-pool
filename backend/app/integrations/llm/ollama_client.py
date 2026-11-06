import httpx,json
from app.config import settings
async def assess_claim(claim):
 prompt=f"""Assess this claim. JSON keys: classification (objective_failure|subjective|unclear), confidence (0..1), findings (array), recommendation (manual_review|likely_valid|likely_invalid), rationale. Advisory only; do not approve or calculate credits.
Requirement: {claim['requirement'][:6000]}
Response: {claim['response_text'][:8000]}
Reason: {claim['reason']}
Evidence: {claim.get('evidence') or 'none'}"""
 async with httpx.AsyncClient(timeout=settings.ollama_timeout) as client:
  r=await client.post(settings.ollama_base_url.rstrip("/")+"/api/generate",json={"model":settings.ollama_model,"prompt":prompt,"stream":False,"format":"json","options":{"temperature":0}})
  r.raise_for_status(); raw=r.json().get("response","{}")
 try: return json.loads(raw)
 except json.JSONDecodeError: raise ValueError("Ollama returned invalid JSON")
