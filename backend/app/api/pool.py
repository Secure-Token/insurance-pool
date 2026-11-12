from fastapi import APIRouter
from app.repositories import db
router=APIRouter(tags=["pool"])
@router.get("/pool")
def pool():
 with db() as c:
  a=c.execute("SELECT funded,reserved,paid FROM pool_account WHERE id=1").fetchone()
  pending=c.execute("SELECT COALESCE(SUM(rec_input+rec_output),0) FROM claims WHERE status IN ('SUBMITTED','ELIGIBILITY_REVIEW','INVESTIGATING')").fetchone()[0]
  funded,paid,reserved=int(a["funded"]),int(a["paid"]),int(a["reserved"])
  available=max(0,funded-paid-reserved)
  return {"total_funded":funded,"committed":paid,"pending":pending,"reserved":reserved,"available":available,"utilization":round((paid+reserved)/funded,4) if funded else 0,"mode":"simulated internal units"}
@router.get("/wallet/{claimant_id}")
def wallet(claimant_id:str):
 with db() as c:
  w=c.execute("SELECT * FROM wallets WHERE claimant_id=?",(claimant_id,)).fetchone()
  entries=[dict(r) for r in c.execute("SELECT * FROM wallet_ledger WHERE claimant_id=? ORDER BY created_at DESC",(claimant_id,))]
  return {"claimant_id":claimant_id,"balance":int(w["balance"]) if w else 0,"ledger":entries}
