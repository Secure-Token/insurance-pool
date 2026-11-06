import uuid
from app.repositories import db
from app.services.claim_service import now
def create(cid,notes):
 with db() as c:
  if not c.execute("SELECT id FROM claims WHERE id=?",(cid,)).fetchone(): raise LookupError("Claim not found")
  iid="INV-"+uuid.uuid4().hex[:10].upper();c.execute("INSERT INTO investigations VALUES(?,?,?,?,?)",(iid,cid,notes,"OPEN",now()))
  c.execute("UPDATE claims SET status='UNDER_INVESTIGATION',updated_at=? WHERE id=?",(now(),cid))
  return dict(c.execute("SELECT * FROM investigations WHERE id=?",(iid,)).fetchone())
def listing():
 with db() as c:return [dict(r) for r in c.execute("SELECT * FROM investigations ORDER BY created_at DESC")]
