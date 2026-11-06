from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.repositories import init_db
from app.api import claims,dashboard,investigations,pool,settlements
app=FastAPI(title=settings.app_name,version="0.1.0",description="Simulation API; no provider refunds or cash settlement.")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.on_event("startup")
def startup(): init_db()
@app.get("/health")
def health(): return {"status":"ok","environment":settings.app_env,"mode":"simulation"}
for r in [dashboard.router,claims.router,investigations.router,pool.router,settlements.router]: app.include_router(r,prefix="/api")
