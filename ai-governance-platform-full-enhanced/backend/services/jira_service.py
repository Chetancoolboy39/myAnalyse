import os, requests
from dotenv import load_dotenv
load_dotenv()
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
def _auth():
    return (JIRA_EMAIL, JIRA_API_TOKEN)
def list_projects():
    url = f"{JIRA_BASE_URL}/rest/api/3/project/search"
    r = requests.get(url, auth=_auth(), timeout=20)
    r.raise_for_status()
    data = r.json()
    projects = data.get("values", []) if isinstance(data, dict) else data
    return [{"key": p.get("key"), "name": p.get("name")} for p in projects]
def create_issue(project_key, summary, description, issuetype="Task", optional_fields=None):
    payload = {"fields":{"project":{"key":project_key},"summary":summary,"description":description,"issuetype":{"name":issuetype}}}
    if optional_fields:
        payload["fields"].update(optional_fields)
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    r = requests.post(url, json=payload, auth=_auth(), timeout=30)
    r.raise_for_status()
    return r.json()
