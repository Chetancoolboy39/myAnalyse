import os, requests
from dotenv import load_dotenv
load_dotenv()
ZEPHYR_BASE_URL = os.getenv("ZEPHYR_BASE_URL")
def create_testcase(project_key, name, description):
    url = f"{ZEPHYR_BASE_URL}/public/rest/api/1.0/testcase"
    payload = {"projectKey": project_key, "name": name, "description": description}
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
def add_step_to_testcase(testcase_id, step_order, step, expected):
    url = f"{ZEPHYR_BASE_URL}/public/rest/api/1.0/testcase/{testcase_id}/step"
    payload = {"order": step_order, "step": step, "expected": expected}
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
def list_attachments_for_testcase(testcase_id):
    url = f"{ZEPHYR_BASE_URL}/public/rest/api/1.0/testcase/{testcase_id}/attachments"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()
