import sqlite3, os, json
from contextlib import contextmanager
from app.config import settings
def path():
 u=settings.database_url
 if not u.startswith("sqlite:///"): raise RuntimeError("Demo currently supports SQLite only")
 return u[10:]
@contextmanager
def db():
 p=path(); os.makedirs(os.path.dirname(os.path.abspath(p)),exist_ok=True)
 c=sqlite3.connect(p,timeout=30); c.row_factory=sqlite3.Row
 c.execute("PRAGMA foreign_keys=ON"); c.execute("PRAGMA busy_timeout=30000")
 try: yield c; c.commit()
 except Exception: c.rollback(); raise
 finally: c.close()
def init_db():
 with db() as c:
  c.executescript("""
  CREATE TABLE IF NOT EXISTS claims(id TEXT PRIMARY KEY,claimant_id TEXT,task_id TEXT,requirement TEXT,response_text TEXT,reason TEXT,input_tokens INTEGER,output_tokens INTEGER,input_rate REAL,output_rate REAL,evidence TEXT,status TEXT,evaluation TEXT,rec_input INTEGER DEFAULT 0,rec_output INTEGER DEFAULT 0,created_at TEXT,updated_at TEXT);
  CREATE TABLE IF NOT EXISTS investigations(id TEXT PRIMARY KEY,claim_id TEXT,notes TEXT,status TEXT,created_at TEXT);
  CREATE TABLE IF NOT EXISTS settlements(id TEXT PRIMARY KEY,claim_id TEXT UNIQUE,input_credits INTEGER,output_credits INTEGER,total_credits INTEGER,status TEXT,created_at TEXT);
  CREATE TABLE IF NOT EXISTS wallets(claimant_id TEXT PRIMARY KEY,balance INTEGER NOT NULL DEFAULT 0,updated_at TEXT);
  CREATE TABLE IF NOT EXISTS wallet_ledger(id TEXT PRIMARY KEY,claimant_id TEXT NOT NULL,claim_id TEXT NOT NULL,settlement_id TEXT NOT NULL UNIQUE,direction TEXT NOT NULL,amount INTEGER NOT NULL,balance_after INTEGER NOT NULL,created_at TEXT);
  CREATE TABLE IF NOT EXISTS pool_account(id INTEGER PRIMARY KEY CHECK(id=1),funded INTEGER NOT NULL DEFAULT 100000,reserved INTEGER NOT NULL DEFAULT 0,paid INTEGER NOT NULL DEFAULT 0,updated_at TEXT);
  CREATE TABLE IF NOT EXISTS pool_ledger(id TEXT PRIMARY KEY,claim_id TEXT NOT NULL,settlement_id TEXT NOT NULL UNIQUE,entry_type TEXT NOT NULL,amount INTEGER NOT NULL,created_at TEXT);
  INSERT OR IGNORE INTO pool_account(id,funded,reserved,paid) VALUES(1,100000,0,0);
  CREATE INDEX IF NOT EXISTS idx_claims_status_created ON claims(status,created_at);
  """)
def claim_dict(r):
 d=dict(r); d["evaluation"]=json.loads(d["evaluation"]) if d.get("evaluation") else None
 return d
