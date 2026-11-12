import uuid
from app.repositories import db
from app.services.claim_service import now
def create(cid,notes):
 with db() as c:
  claim=c.execute("SELECT id,status FROM claims WHERE id=?",(cid,)).fetchone()
  if not claim: raise LookupError("Claim not found")
  if claim["status"] in ("SETTLED","REJECTED","WITHDRAWN"): raise ValueError("Investigation cannot be opened for terminal claim")
  iid="INV-"+uuid.uuid4().hex[:10].upper(); t=now()
  c.execute("INSERT INTO investigations VALUES(?,?,?,?,?)",(iid,cid,notes,"OPEN",t))
  c.execute("UPDATE claims SET status='INVESTIGATING',updated_at=? WHERE id=?",(t,cid))
  return dict(c.execute("SELECT * FROM investigations WHERE id=?",(iid,)).fetchone())
def listing():
 with db() as c:return [dict(r) for r in c.execute("SELECT * FROM investigations ORDER BY created_at DESC")]
