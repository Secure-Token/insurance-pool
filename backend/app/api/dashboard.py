from fastapi import APIRouter
from app.repositories import db
router=APIRouter(tags=["dashboard"])
@router.get("/dashboard")
def dashboard():
 with db() as c:
  n=lambda q:c.execute(q).fetchone()[0]
  return {"total_claims":n("SELECT COUNT(*) FROM claims"),"open_claims":n("SELECT COUNT(*) FROM claims WHERE status NOT IN ('SETTLED','REJECTED','WITHDRAWN')"),"settled_claims":n("SELECT COUNT(*) FROM claims WHERE status='SETTLED'"),"open_investigations":n("SELECT COUNT(*) FROM investigations WHERE status='OPEN'"),"recent_claims":[dict(r) for r in c.execute("SELECT id,task_id,status,reason,created_at FROM claims ORDER BY created_at DESC LIMIT 8")],"mode":"simulation"}
