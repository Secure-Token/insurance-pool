import uuid
from app.repositories import db
from app.services.claim_service import now
def ledger():
 with db() as c:return [dict(r) for r in c.execute("SELECT * FROM settlements ORDER BY created_at DESC")]
def settle(cid):
 with db() as c:
  r=c.execute("SELECT * FROM claims WHERE id=?",(cid,)).fetchone()
  if not r: raise LookupError("Claim not found")
  if r["status"] not in ("APPROVED","PARTIALLY_APPROVED"): raise ValueError("Claim must be APPROVED or PARTIALLY_APPROVED before settlement")
  existing=c.execute("SELECT * FROM settlements WHERE claim_id=?",(cid,)).fetchone()
  if existing:return dict(existing)
  i,o=max(0,int(r["rec_input"] or 0)),max(0,int(r["rec_output"] or 0)); total=i+o
  a=c.execute("SELECT funded,reserved,paid FROM pool_account WHERE id=1").fetchone()
  available=max(0,int(a["funded"])-int(a["reserved"])-int(a["paid"]))
  if total>available:raise ValueError(f"Insufficient pool balance: requested {total}, available {available}")
  sid="SET-"+uuid.uuid4().hex[:10].upper();t=now()
  c.execute("INSERT INTO settlements VALUES(?,?,?,?,?,?,?)",(sid,cid,i,o,total,"SIMULATED",t))
  c.execute("UPDATE claims SET status='SETTLED',updated_at=? WHERE id=?",(t,cid))
  c.execute("INSERT OR IGNORE INTO wallets(claimant_id,balance,updated_at) VALUES(?,0,?)",(r["claimant_id"],t))
  c.execute("UPDATE wallets SET balance=balance+?,updated_at=? WHERE claimant_id=?",(total,t,r["claimant_id"]))
  balance=c.execute("SELECT balance FROM wallets WHERE claimant_id=?",(r["claimant_id"],)).fetchone()[0]
  c.execute("INSERT INTO wallet_ledger VALUES(?,?,?,?,?,?,?,?)",("WLT-"+uuid.uuid4().hex[:10].upper(),r["claimant_id"],cid,sid,"CREDIT",total,balance,t))
  c.execute("UPDATE pool_account SET paid=paid+?,updated_at=? WHERE id=1",(total,t))
  c.execute("INSERT INTO pool_ledger VALUES(?,?,?,?,?,?)",("PL-"+uuid.uuid4().hex[:10].upper(),cid,sid,"CLAIM_PAYOUT",-total,t))
  return dict(c.execute("SELECT * FROM settlements WHERE id=?",(sid,)).fetchone())
