from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class FieldConfig(BaseModel):
    mandatory: List[str]
    optional: List[str]
    dynamic_rules: Dict[str, str]

class RephraseRequest(BaseModel):
    title: str
    description: str

class RephraseResponse(BaseModel):
    title: str
    description: str
    prompt: Optional[str] = None

class JiraCreateRequest(BaseModel):
    project_key: str
    title: str
    description: str
    issuetype: str = "Task"
    optional_fields: Optional[Dict[str, Any]] = {}

class JiraCreateResponse(BaseModel):
    key: str
    url: Optional[str]

class ZephyrStep(BaseModel):
    order: int
    step: str
    expected: Optional[str] = None
    relevance: Optional[float] = None

class ZephyrTestCase(BaseModel):
    name: str
    description: Optional[str]
    steps: List[ZephyrStep]

class AttachmentVerifyResult(BaseModel):
    step_order: int
    ocr_text: str
    match_percent: float
    status: str
    comments: Optional[str] = None

# Simple persistence model
class Mapping(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jira_key: str
    zephyr_testcase_id: Optional[str] = None
    meta: Optional[str] = None
