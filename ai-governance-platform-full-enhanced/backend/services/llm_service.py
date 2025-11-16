import os, requests
from dotenv import load_dotenv
load_dotenv()
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL","")
def rephrase_title_description(title: str, description: str):
    prompt = f"Rephrase title: {title}\n\nDescription: {description}"
    if not LLM_API_URL:
        return title, description, prompt
    payload = {"model": LLM_MODEL, "messages":[{"role":"user","content":prompt}], "max_tokens":400}
    r = requests.post(LLM_API_URL, json=payload, timeout=30)
    try:
        r.raise_for_status()
        data = r.json()
        content = ""
        if "choices" in data and len(data["choices"])>0:
            content = data["choices"][0].get("message",{}).get("content","")
        import json
        try:
            parsed = json.loads(content)
            return parsed.get("title", title), parsed.get("description", description), prompt
        except Exception:
            return title, description, prompt
    except Exception:
        return title, description, prompt
