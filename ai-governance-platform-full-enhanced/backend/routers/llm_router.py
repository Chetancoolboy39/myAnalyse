from fastapi import APIRouter
from models.schemas import RephraseRequest, RephraseResponse
from services.llm_service import rephrase_title_description
router = APIRouter(prefix="/llm", tags=["llm"])
@router.post("/rephrase", response_model=RephraseResponse)
def rephrase(req: RephraseRequest):
    new_title, new_desc, prompt = rephrase_title_description(req.title, req.description)
    return {"title": new_title, "description": new_desc, "prompt": prompt}
