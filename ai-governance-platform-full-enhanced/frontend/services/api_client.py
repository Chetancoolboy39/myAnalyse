import os
import requests
BASE = os.getenv("BACKEND_URL", "http://localhost:8000")
def get_fields():
    r = requests.get(f"{BASE}/config/fields"); r.raise_for_status(); return r.json()
def rephrase(title, description):
    r = requests.post(f"{BASE}/llm/rephrase", json={"title": title, "description": description}); r.raise_for_status(); return r.json()
def get_projects():
    r = requests.get(f"{BASE}/jira/projects"); r.raise_for_status(); return r.json()
def create_jira(payload):
    r = requests.post(f"{BASE}/jira/create", json=payload); r.raise_for_status(); return r.json()
def generate_zephyr(jira_key, testcase):
    r = requests.post(f"{BASE}/zephyr/generate", params={"jira_key": jira_key}, json=testcase); r.raise_for_status(); return r.json()
def verify_attachment(testcase_id, step_order, file_path):
    with open(file_path, "rb") as f:
        files = {"file": (file_path.split("/")[-1], f)}
        r = requests.post(f"{BASE}/zephyr/attachments/verify", params={"testcase_id": testcase_id, "step_order": step_order}, files=files)
        r.raise_for_status()
        return r.json()
