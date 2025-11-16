from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import ZephyrTestCase, ZephyrStep, AttachmentVerifyResult
from services.zephyr_service import create_testcase, add_step_to_testcase, list_attachments_for_testcase
from services.ocr_service import extract_text_from_file
from services.verification_service import unified_verification
from typing import List
import tempfile, os
router = APIRouter(prefix="/zephyr", tags=["zephyr"])
@router.post("/generate")
def generate_zephyr(jira_key: str, testcase: ZephyrTestCase):
    try:
        res = create_testcase(jira_key, testcase.name, testcase.description or "")
        tcid = res.get("id") or res.get("testcaseId") or res.get("key")
        for s in testcase.steps:
            add_step_to_testcase(str(tcid), s.order, s.step, s.expected or "")
        return {"testcase_id": tcid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/attachments/{testcase_id}")
def get_attachments(testcase_id: str):
    try:
        return list_attachments_for_testcase(testcase_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/attachments/verify")
def verify_attachments(testcase_id: str, step_order: int, file: UploadFile = File(...)):
    try:
        suffix = "." + file.filename.split(".")[-1] if "." in file.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name
        text = extract_text_from_file(tmp_path)
        step_text = os.getenv("DUMMY_STEP_TEXT", f"Expected step for order {step_order} of testcase {testcase_id}")
        score_obj = unified_verification(step_text, text)
        from models.schemas import AttachmentVerifyResult
        result = AttachmentVerifyResult(
            step_order=step_order,
            ocr_text=text,
            match_percent=score_obj["final_percent"],
            status=score_obj["pass_fail"],
            comments=score_obj["reasoning"]
        )
        try:
            os.remove(tmp_path)
        except:
            pass
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
