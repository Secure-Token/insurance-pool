import uuid,json
from datetime import datetime,timezone
from app.repositories import db,claim_dict
def now(): return datetime.now(timezone.utc).isoformat()
def create(x):
 d=x.model_dump(); cid="CLM-"+uuid.uuid4().hex[:10].upper(); t=now()
 with db() as c:
  c.execute("INSERT INTO claims(id,claimant_id,task_id,requirement,response_text,reason,input_tokens,output_tokens,input_rate,output_rate,evidence,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(cid,d["claimant_id"],d["task_id"],d["requirement"],d["response_text"],d["reason"],d["input_tokens"],d["output_tokens"],d["input_rate_per_million"],d["output_rate_per_million"],d["evidence"],"SUBMITTED",t,t))
  return claim_dict(c.execute("SELECT * FROM claims WHERE id=?",(cid,)).fetchone())
def get(cid):
 with db() as c:
  r=c.execute("SELECT * FROM claims WHERE id=?",(cid,)).fetchone(); return claim_dict(r) if r else None
def listing(status=None):
 with db() as c:
  q="SELECT * FROM claims"; args=[]
  if status:q+=" WHERE status=?";args=[status]
  q+=" ORDER BY created_at DESC";return [claim_dict(r) for r in c.execute(q,args)]
def save(cid,a,calc,s):
 with db() as c:
  c.execute("UPDATE claims SET evaluation=?,rec_input=?,rec_output=?,status=?,updated_at=? WHERE id=?",(json.dumps({**a,"calculation":calc}),calc["recommended_input_credits"],calc["recommended_output_credits"],s,now(),cid))
 return get(cid)
