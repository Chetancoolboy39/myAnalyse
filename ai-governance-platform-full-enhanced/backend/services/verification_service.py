import os
import requests
from typing import Tuple, Dict, Any
from dotenv import load_dotenv
load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL", "")

def compute_embedding_score(step_text: str, ocr_text: str) -> float:
    try:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('all-MiniLM-L6-v2')
        emb1 = model.encode(step_text, convert_to_tensor=True)
        emb2 = model.encode(ocr_text, convert_to_tensor=True)
        score = util.cos_sim(emb1, emb2).item()
        if score < 0:
            score = 0.0
        if score > 1:
            score = 1.0
        return float(score)
    except Exception as e:
        print('Embedding error:', e)
        return 0.0

def llm_judgement(step_text: str, ocr_text: str) -> Dict[str, Any]:
    prompt = f"""You are an expert QA verifier.
Given a test step (what should be done/verified) and extracted OCR text from an attachment,
determine whether the attachment proves the execution of the step.

Return a JSON object with keys:
- match_percent: integer 0-100
- pass_fail: 'Pass' or 'Fail'
- reasoning: short explanation (1-2 sentences)

Step:
{step_text}

OCR Extracted Text:
{ocr_text}
"""
    if not LLM_API_URL:
        if ocr_text and len(ocr_text.strip())>30:
            return {"match_percent": 80, "pass_fail": "Pass", "reasoning": "Non-empty OCR content"}
        else:
            return {"match_percent": 10, "pass_fail": "Fail", "reasoning": "No useful text found"}

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that judges attachments against test steps."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 400,
        "temperature": 0
    }
    try:
        r = requests.post(LLM_API_URL, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        content = ""
        if "choices" in data and len(data["choices"])>0:
            content = data["choices"][0].get("message", {}).get("content","")
        elif "result" in data:
            content = data["result"]
        else:
            content = r.text

        import json
        try:
            parsed = json.loads(content)
            match_percent = int(parsed.get("match_percent", parsed.get("match", 0)))
            pass_fail = parsed.get("pass_fail", parsed.get("status","Fail"))
            reasoning = parsed.get("reasoning", parsed.get("comments",""))
            return {"match_percent": match_percent, "pass_fail": pass_fail, "reasoning": reasoning}
        except Exception:
            if "pass" in content.lower():
                return {"match_percent": 75, "pass_fail":"Pass", "reasoning": content.strip()[:200]}
            else:
                return {"match_percent": 20, "pass_fail":"Fail", "reasoning": content.strip()[:200]}
    except Exception as e:
        return {"match_percent": 0, "pass_fail":"Fail", "reasoning": str(e)}

def unified_verification(step_text: str, ocr_text: str) -> Dict[str, Any]:
    emb_score = compute_embedding_score(step_text, ocr_text)
    llm_res = llm_judgement(step_text, ocr_text)
    llm_percent = llm_res.get("match_percent",0)/100.0
    final = (emb_score * 0.4) + (llm_percent * 0.6)
    final_percent = int(final * 100)
    pass_fail = "Pass" if final_percent >= 60 else "Fail"
    reasoning = llm_res.get("reasoning","")
    return {
        "embedding_score": round(float(emb_score),4),
        "llm_match_percent": int(llm_res.get("match_percent",0)),
        "final_percent": final_percent,
        "pass_fail": pass_fail,
        "reasoning": reasoning
    }
