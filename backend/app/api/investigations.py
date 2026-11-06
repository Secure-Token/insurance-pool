from fastapi import APIRouter,HTTPException
from app.schemas import InvestigationCreate
from app.services.investigation_service import create,listing
router=APIRouter(tags=["investigations"])
@router.get("/investigations")
def all():return listing()
@router.post("/claims/{cid}/investigations",status_code=201)
def open_one(cid,p:InvestigationCreate):
 try:return create(cid,p.notes)
 except LookupError as e:raise HTTPException(404,str(e))
