import os
from fastapi import FastAPI
from routers.config_router import router as config_router
from routers.llm_router import router as llm_router
from routers.jira_router import router as jira_router
from routers.zephyr_router import router as zephyr_router
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
load_dotenv()
app = FastAPI(title="Release Governance Platform", version="0.2-enhanced")
app.include_router(config_router)
app.include_router(llm_router)
app.include_router(jira_router)
app.include_router(zephyr_router)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./governance.db")
engine = create_engine(DATABASE_URL, echo=False)
SQLModel.metadata.create_all(engine)
@app.get("/")
def root():
    return {"msg": "Release Governance Platform Backend Running (enhanced)"}
