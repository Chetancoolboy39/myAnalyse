import streamlit as st
from services.api_client import get_fields, rephrase, get_projects, create_jira, generate_zephyr, verify_attachment
import json, tempfile
st.set_page_config(page_title="Release Governance UI", layout="wide")
st.title("Release Governance Assistant — Enhanced")
st.sidebar.header("Workflow")
step = st.sidebar.radio("Choose step", ["Jira", "Zephyr", "Attachments", "Dashboard"])
if step == "Jira":
    st.header("Jira Standardization")
    try:
        cfg = get_fields(); st.write("Mandatory fields:", cfg["mandatory"])
    except Exception as e:
        st.error(f"Failed to load config: {e}"); cfg=None
    title = st.text_input("Title", "")
    description = st.text_area("Description", "", height=200)
    if st.button("Improve using AI"):
        try:
            r = rephrase(title, description)
            st.subheader("AI Suggestions")
            st.text_input("AI Title", r.get("title", ""))
            st.text_area("AI Description", r.get("description", ""), height=200)
            st.session_state["ai_title"] = r.get("title", "")
            st.session_state["ai_description"] = r.get("description", "")
        except Exception as e:
            st.error(f"LLM call failed: {e}")
    st.write("---")
    try:
        projects = get_projects(); project_opts = [f'{p["key"]} - {p["name"]}' for p in projects]; selected = st.selectbox("Select Project", project_opts)
    except Exception as e:
        st.error(f"Failed to load projects: {e}"); selected=None
    project_key = selected.split(" - ")[0] if selected else None
    if st.button("Create Jira"):
        payload = {"project_key": project_key, "title": st.session_state.get("ai_title", title), "description": st.session_state.get("ai_description", description), "issuetype": "Task", "optional_fields": {}}
        try:
            res = create_jira(payload); st.success(f"Created Jira: {res.get('key')}"); st.session_state["last_jira"] = res.get("key")
        except Exception as e:
            st.error(f"Failed to create Jira: {e}")
elif step == "Zephyr":
    st.header("Zephyr Test Case Generator")
    jira_id = st.text_input("Jira Key (e.g. PROJ-123)", value=st.session_state.get("last_jira", ""))
    name = st.text_input("Test Case Name", ""); desc = st.text_area("Test Case Description", ""); steps_raw = st.text_area("Steps (one per line, format: step || expected)", height=200)
    if st.button("Generate Testcase"):
        steps_lines = [s for s in steps_raw.splitlines() if s.strip()]; steps=[]
        for idx, line in enumerate(steps_lines, start=1):
            parts = line.split("||"); step_text = parts[0].strip(); expected = parts[1].strip() if len(parts)>1 else ""
            steps.append({"order": idx, "step": step_text, "expected": expected})
        testcase = {"name": name, "description": desc, "steps": steps}
        try:
            res = generate_zephyr(jira_id, testcase); st.success(f"Created Zephyr Testcase: {res.get('testcase_id')}"); st.session_state["last_tc"] = res.get("testcase_id")
        except Exception as e:
            st.error(f"Failed to create zephyr testcase: {e}")
elif step == "Attachments":
    st.header("Attachment Verification (Embeddings + LLM)")
    tc_id = st.text_input("Test Case ID", value=st.session_state.get("last_tc", ""))
    step_order = st.number_input("Step Order", min_value=1, value=1)
    uploaded = st.file_uploader("Upload attachment (image/pdf)", type=["png","jpg","jpeg","pdf"])
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix="."+uploaded.name.split(".")[-1]) as tmp:
            tmp.write(uploaded.getbuffer()); tmp_path = tmp.name
        if st.button("Verify Attachment"):
            try:
                res = verify_attachment(tc_id, step_order, tmp_path)
                st.subheader("Verification Result")
                st.write(f"Final Match %: {res.get('final_percent')}")
                st.write(f"Pass/Fail: {res.get('pass_fail')}")
                st.write(f"Embedding score: {res.get('embedding_score')}")
                st.write(f"LLM match %: {res.get('llm_match_percent')}")
                st.write("Reasoning:"); st.write(res.get('comments') or res.get('reasoning') or '')
            except Exception as e:
                st.error(f"Attachment verification failed: {e}")
elif step == "Dashboard":
    st.header("Governance Dashboard")
    st.write("Coming soon: aggregated scores and visualization.")
