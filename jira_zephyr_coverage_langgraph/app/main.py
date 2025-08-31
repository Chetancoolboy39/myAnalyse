from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import httpx
from embeddings.matcher import EmbeddingMatcher

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_USER = os.getenv("JIRA_USER")
ZEPHYR_BASE_URL = os.getenv("ZEPHYR_BASE_URL")

app = FastAPI()
matcher = EmbeddingMatcher()

class AnalyzeRequest(BaseModel):
    project_key: str
    requirement_ids: List[str]

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        requirements = []
        for rid in req.requirement_ids:
            url = f"{JIRA_BASE_URL}/rest/api/2/issue/{rid}"
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, auth=(JIRA_USER, JIRA_API_TOKEN))
                data = resp.json()
                requirements.append({"id": rid, "summary": data['fields']['summary']})

        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{ZEPHYR_BASE_URL}/tests")
            zephyr_tests = resp.json()

        coverage_results = matcher.check_coverage(requirements, zephyr_tests)

        return {"coverage": coverage_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
