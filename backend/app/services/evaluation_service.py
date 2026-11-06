from app.services.claim_service import get,save
from app.integrations.llm.ollama_client import assess_claim
from app.engine.policy_validator import validate,status
from app.engine.compensation import calculate
async def evaluate(cid):
 c=get(cid)
 if not c: raise LookupError("Claim not found")
 a=validate(await assess_claim(c)); calc=calculate(c,a)
 return save(cid,a,calc,status(a))
