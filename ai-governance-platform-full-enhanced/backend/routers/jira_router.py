from fastapi import APIRouter, HTTPException
from models.schemas import JiraCreateRequest, JiraCreateResponse
from services.jira_service import list_projects, create_issue
from utils.field_validator import validate_payload
router = APIRouter(prefix="/jira", tags=["jira"])
@router.get("/projects")
def get_projects():
    return list_projects()
@router.post("/create", response_model=JiraCreateResponse)
def create_jira(req: JiraCreateRequest):
    ok, msg = validate_payload({"title": req.title, "description": req.description})
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    try:
        res = create_issue(req.project_key, req.title, req.description, req.issuetype, req.optional_fields)
        key = res.get("key")
        url = None
        if key:
            url = f"{os.getenv('JIRA_BASE_URL')}/browse/{key}"
        return {"key": key, "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
