from fastapi import APIRouter
from models.schemas import FieldConfig
from utils.field_validator import load_field_config
router = APIRouter(prefix="/config", tags=["config"])
@router.get("/fields", response_model=FieldConfig)
def get_fields():
    return load_field_config()
