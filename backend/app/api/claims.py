from fastapi import APIRouter,HTTPException
from app.models import ClaimCreate
from app.services.claim_service import create,get,listing
from app.services.evaluation_service import evaluate
router=APIRouter(tags=["claims"])
@router.post("/claims",status_code=201)
def submit(p:ClaimCreate):return create(p)
@router.get("/claims")
def all_claims(status:str|None=None):return listing(status)
@router.get("/claims/{cid}")
def detail(cid):
 x=get(cid)
 if not x:raise HTTPException(404,"Claim not found")
 return x
@router.post("/claims/{cid}/evaluate")
async def run(cid):
 try:return await evaluate(cid)
 except LookupError as e:raise HTTPException(404,str(e))
 except Exception as e:raise HTTPException(502,f"Evaluation failed: {e}")
