import os
import sys
import requests
import openai
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_AUTH = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
ZEPHYR_BASE_URL = os.getenv("ZEPHYR_BASE_URL")
ZEPHYR_TOKEN = os.getenv("ZEPHYR_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# --- Step 1: Fetch Jira Issue Description ---
def fetch_jira_description(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}"
    response = requests.get(url, auth=JIRA_AUTH)
    response.raise_for_status()
    return response.json()["fields"]["description"]

# --- Step 2: Fetch Linked Zephyr Test Cases & Steps ---
def fetch_zephyr_testcases(issue_key):
    url = f"{ZEPHYR_BASE_URL}/public/rest/api/1.0/requirement/{issue_key}/testcases"
    headers = {"Authorization": f"Bearer {ZEPHYR_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_test_steps(testcase_id):
    url = f"{ZEPHYR_BASE_URL}/public/rest/api/1.0/testcase/{testcase_id}"
    headers = {"Authorization": f"Bearer {ZEPHYR_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    steps = response.json().get("testSteps", [])
    return [s.get("step") for s in steps]

# --- Step 3: LLM Coverage Analysis ---
def analyze_coverage(requirement_desc, test_steps):
    prompt = f"""
You are an expert QA reviewer.
Requirement Description:
{requirement_desc}

Test Steps:
{test_steps}

Task:
1. Verify whether every aspect of the requirement description is covered by at least one test step.
2. Highlight any part of the requirement that is not addressed by any test step.
3. If coverage is complete, respond with "100% Covered."
4. If coverage is incomplete, respond with "Gaps Found" and list the gaps clearly.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message["content"]

# --- Main Flow ---
def check_requirement_coverage(issue_key):
    requirement_desc = fetch_jira_description(issue_key)
    testcases = fetch_zephyr_testcases(issue_key)

    all_test_steps = []
    for tc in testcases:
        testcase_id = tc["id"]
        steps = fetch_test_steps(testcase_id)
        all_test_steps.extend(steps)

    result = analyze_coverage(requirement_desc, all_test_steps)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <JIRA_ISSUE_KEY>")
        sys.exit(1)
    issue_key = sys.argv[1]
    coverage_result = check_requirement_coverage(issue_key)
    print("Coverage Analysis Result:\n", coverage_result)
