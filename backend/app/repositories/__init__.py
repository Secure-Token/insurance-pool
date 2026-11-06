import sqlite3,os,json
from contextlib import contextmanager
from app.config import settings
def path():
 u=settings.database_url
 if not u.startswith("sqlite:///"): raise RuntimeError("Demo currently supports SQLite only")
 return u[10:]
@contextmanager
def db():
 p=path(); os.makedirs(os.path.dirname(os.path.abspath(p)),exist_ok=True)
 c=sqlite3.connect(p,timeout=20); c.row_factory=sqlite3.Row
 try: yield c; c.commit()
 except: c.rollback(); raise
 finally: c.close()
def init_db():
 with db() as c:
  c.executescript("""CREATE TABLE IF NOT EXISTS claims(id TEXT PRIMARY KEY,claimant_id TEXT,task_id TEXT,requirement TEXT,response_text TEXT,reason TEXT,input_tokens INTEGER,output_tokens INTEGER,input_rate REAL,output_rate REAL,evidence TEXT,status TEXT,evaluation TEXT,rec_input INTEGER DEFAULT 0,rec_output INTEGER DEFAULT 0,created_at TEXT,updated_at TEXT);
  CREATE TABLE IF NOT EXISTS investigations(id TEXT PRIMARY KEY,claim_id TEXT,notes TEXT,status TEXT,created_at TEXT);
  CREATE TABLE IF NOT EXISTS settlements(id TEXT PRIMARY KEY,claim_id TEXT,input_credits INTEGER,output_credits INTEGER,total_credits INTEGER,status TEXT,created_at TEXT);""")
def claim_dict(r):
 d=dict(r); d["evaluation"]=json.loads(d["evaluation"]) if d["evaluation"] else None; return d
