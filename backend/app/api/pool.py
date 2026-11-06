from fastapi import APIRouter
from app.repositories import db
from app.engine.reserve import snapshot
router=APIRouter(tags=["pool"])
@router.get("/pool")
def pool():
 with db() as c:
  pending=c.execute("SELECT COALESCE(SUM(rec_input+rec_output),0) FROM claims WHERE status IN ('SUBMITTED','ELIGIBILITY_REVIEW','UNDER_ASSESSMENT','WITHHELD','UNDER_INVESTIGATION')").fetchone()[0]
  committed=c.execute("SELECT COALESCE(SUM(input_credits+output_credits),0) FROM settlements").fetchone()[0]
 return {**snapshot(committed=committed,pending=pending),"mode":"simulated internal units"}
