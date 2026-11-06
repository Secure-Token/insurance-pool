from fastapi import APIRouter,HTTPException
from app.services.settlement_service import settle,ledger
router=APIRouter(tags=["settlements"])
@router.get("/settlements/ledger")
def get_ledger():return ledger()
@router.post("/claims/{cid}/settle")
def run(cid):
 try:return settle(cid)
 except LookupError as e:raise HTTPException(404,str(e))
 except ValueError as e:raise HTTPException(409,str(e))
