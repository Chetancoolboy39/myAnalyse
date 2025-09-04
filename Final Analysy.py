from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import json

client = OpenAI()

# -------------------------------
# Sample Jira + Zephyr Data
# -------------------------------
jira_data = [
    {
        "id": "JIRA-101",
        "requirement": "System should allow login using email and password, and lock the user after 5 failed attempts.",
        "zephyr_steps": [
            "Navigate to login page",
            "Enter email and password",
            "Click login button",
            "Verify user is redirected to dashboard"
        ]
    },
    {
        "id": "JIRA-102",
        "requirement": "System should allow users to reset password via email verification.",
        "zephyr_steps": [
            "Trigger password reset request",
            "Receive password reset email",
            "Set new password using reset link"
        ]
    },
    {
        "id": "JIRA-103",
        "requirement": "System should log all user activities including login, logout, and password changes.",
        "zephyr_steps": [
            "Log user activity after login",
            "Log user activity after logout"
        ]
    }
]

# -------------------------------
# Step 1: Extract functionalities per Jira using LLM
# -------------------------------
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a QA analyst. Break each Jira requirement into atomic testable functionalities."},
        {"role": "user", "content": f"""Here are multiple Jira requirements:
{json.dumps([{j['id']: j['requirement']} for j in jira_data], indent=2)}

Return only JSON in this format:
{{
  "JIRA-101": ["func1", "func2"],
  "JIRA-102": ["func1", "func2"]
}}"""}
    ],
    temperature=0
)

functionalities_map = json.loads(resp.choices[0].message.content)

# -------------------------------
# Step 2: Embedding Coverage Calculation
# -------------------------------
def get_embedding(text, model="text-embedding-3-small"):
    return client.embeddings.create(model=model, input=text).data[0].embedding

threshold = 0.70
coverage_results = {}

for jira in jira_data:
    jira_id = jira["id"]
    funcs = functionalities_map.get(jira_id, [])
    zephyr_steps = jira["zephyr_steps"]

    zephyr_emb = [get_embedding(step) for step in zephyr_steps]
    func_results = {}
    covered_count = 0

    for func in funcs:
        func_emb = get_embedding(func)
        scores = [cosine_similarity([func_emb], [step_emb])[0][0] for step_emb in zephyr_emb]

        max_score = max(scores)
        best_step = zephyr_steps[scores.index(max_score)]

        is_covered = max_score >= threshold
        if is_covered:
            covered_count += 1

        func_results[func] = {
            "covered": is_covered,
            "best_step": best_step,
            "score": round(max_score, 2)
        }

    coverage_percent = (covered_count / len(funcs)) * 100 if funcs else 0
    coverage_results[jira_id] = {
        "functionalities": func_results,
        "coverage_percent": round(coverage_percent, 1)
    }

# -------------------------------
# Step 3: Gap Analysis (all Jira in one call)
# -------------------------------
jira_for_llm = []
for item in jira_data:
    jira_for_llm.append({
        "id": item["id"],
        "requirement": item["requirement"],
        "zephyr_steps": item["zephyr_steps"]
    })

resp_gap = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a QA reviewer. Compare requirements with test steps and return uncovered functionalities."},
        {"role": "user", "content": f"""Perform gap analysis for these Jira requirements and their Zephyr steps. 
Return JSON in this format:
{{
  "JIRA-101": {{
    "missing": ["func1", "func2"],
    "covered": ["func3", "func4"]
  }}
}}

Here is the data:
{json.dumps(jira_for_llm, indent=2)}
"""}
    ],
    temperature=0
)

gap_analysis = json.loads(resp_gap.choices[0].message.content)

# -------------------------------
# Step 4: Merge All Results
# -------------------------------
final_results = {}
for jira in jira_data:
    jira_id = jira["id"]
    final_results[jira_id] = {
        "requirement": jira["requirement"],
        "zephyr_steps": jira["zephyr_steps"],
        "functionalities": functionalities_map.get(jira_id, []),
        "embedding_coverage": coverage_results.get(jira_id, {}),
        "gap_analysis": gap_analysis.get(jira_id, {})
    }

print("\n🔹 Final Unified Results:")
print(json.dumps(final_results, indent=2))
