import json
from pathlib import Path
from typing import Dict, Any
from models.schemas import FieldConfig
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "jira_fields.json"
def load_field_config() -> FieldConfig:
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return FieldConfig(**data)
def validate_payload(payload: Dict[str, Any]) -> (bool, str):
    cfg = load_field_config()
    for m in cfg.mandatory:
        if m not in payload or not payload[m]:
            return False, f"Mandatory field {m} missing or empty"
    return True, "ok"
