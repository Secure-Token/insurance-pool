import uuid
from app.repositories import db
from app.services.claim_service import now
def ledger():
 with db() as c:return [dict(r) for r in c.execute("SELECT * FROM settlements ORDER BY created_at DESC")]
def settle(cid):
 with db() as c:
  r=c.execute("SELECT * FROM claims WHERE id=?",(cid,)).fetchone()
  if not r:raise LookupError("Claim not found")
  if r["status"] not in ("APPROVED","PARTIALLY_APPROVED","READY_FOR_SETTLEMENT"):raise ValueError("Claim must be explicitly approved before settlement")
  sid="SET-"+uuid.uuid4().hex[:10].upper();i,o=r["rec_input"],r["rec_output"];t=now()
  c.execute("INSERT INTO settlements VALUES(?,?,?,?,?,?,?)",(sid,cid,i,o,i+o,"SIMULATED",t))
  c.execute("UPDATE claims SET status='SETTLED',updated_at=? WHERE id=?",(t,cid))
  return dict(c.execute("SELECT * FROM settlements WHERE id=?",(sid,)).fetchone())
