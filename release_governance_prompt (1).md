# Release Governance AI Platform — Master Prompt (For GPT‑5 / GitHub Copilot)

Use this **README.md** file as a **master specification + prompt** for generating the *complete application codebase* using ChatGPT‑5, GitHub Copilot, or any LLM.  
You can paste this entire file into GPT‑5 to generate the full backend + frontend application.

You can also edit the sections where indicated and provide your own:
- **Jira API credentials / URL**
- **Zephyr API credentials / URL**
- **Local LLM endpoint details**

This system *is* an **AI Agent** (multi‑module, multi‑tool agent system) that automates:
- Jira Standardization
- Zephyr Test Case Generation
- Zephyr Step Relevance Scoring
- Zephyr Attachment Verification using OCR
---

# 📌 **MASTER REQUIREMENT SPECIFICATION**

## 🟦 **1. Application Overview**
Build a complete **AI‑driven Release Governance Platform** using:

### **Frontend**
- Streamlit (Python)

### **Backend**
- FastAPI
- JSON/YAML config engine
- OCR Engine (PaddleOCR or Tesseract)
- Local or Cloud LLM
- Jira API
- Zephyr API

### **Architecture**
This will be a **modular agent-based system** with the following agents:

| Agent | Responsibility |
|-------|----------------|
| **Jira Standardization Agent** | Validate fields, LLM rephrase, create Jira issue |
| **Zephyr Generation Agent** | Generate test cases and steps from Jira content |
| **Relevance Scoring Agent** | Score each Zephyr step against Jira requirement |
| **OCR Attachment Verification Agent** | Validate QA attachments vs Zephyr steps |
| **Governance Scoring Agent** | Calculate overall release governance score |

---

# 🟦 **2. Jira Standardization Agent**

## ✔ Mandatory Fields
- Title
- Description

## ✔ Optional Fields (Configurable)
- Priority
- Labels
- Environment
- Assignee

A JSON or YAML file controls which fields are mandatory.

### Example: `config/jira_fields.json`
```json
{
  "mandatory": ["title", "description"],
  "optional": ["priority", "labels", "environment", "assignee"],
  "dynamic_rules": {
    "priority": "optional",
    "labels": "optional",
    "environment": "optional",
    "assignee": "optional"
  }
}
```
---

# 🟦 **3. LLM Rephrase Engine**
User provides Title + Description.  
LLM rewrites into:
- Clear summary
- Problem → Current Behavior → Expected → Impact
- Jira‑standard format

### Insert your local LLM API details:
```
LOCAL_LLM_URL=http://localhost:8000/v1/chat/completions
LOCAL_LLM_MODEL=your-model-name
```

---

# 🟦 **4. Jira Integration**

### Insert your Jira API details below:
```
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email
JIRA_API_TOKEN=your-token
```

The following must be implemented:
- `GET /jira/projects` → list projects
- `POST /jira/create` → create issue

---

# 🟦 **5. Zephyr Test Case Generation Agent**
The agent must:
1. Read Jira title + description
2. Generate:
   - Test Case Name
   - Test Steps
   - Expected Results
3. Calculate **step relevance %** between Jira text & step text
4. Display editable table in UI
5. On confirmation → create Zephyr Test Case using API

### Insert your Zephyr API details below:
```
ZEPHYR_BASE_URL=https://your-zephyr-url
ZEPHYR_API_KEY=your-key
ZEPHYR_SECRET_KEY=your-secret
```

---

# 🟦 **6. Zephyr Attachment Verification Agent (OCR)**
After QA testing:
1. Read attachments from Zephyr
2. Identify image/PDF
3. Run OCR
4. Compare extracted text to expected content for each step
5. Generate:
   - Match %
   - Pass/Fail
   - Missing content
   - Irrelevant attachment detection

---

# 🟦 **7. Governance Dashboard**
Agent must compute:
- Jira Standardization Status
- Zephyr Step Relevance Score
- Zephyr Attachment Validation Score
- Final Governance Score (0–100%)

Display results in Streamlit dashboard.

---

# 🟦 **8. Backend Requirements (FastAPI)**
Backend must include the following endpoints:

### **Config Endpoints**
- `GET /config/fields`

### **LLM Endpoints**
- `POST /llm/rephrase`
- `POST /llm/step-score`

### **Jira Endpoints**
- `GET /jira/projects`
- `POST /jira/create`

### **Zephyr Endpoints**
- `POST /zephyr/generate`
- `POST /zephyr/create`
- `GET /zephyr/attachments/{testCaseId}`
- `POST /zephyr/attachments/verify`

### **Governance**
- `GET /governance/score/{jiraId}`

---

# 🟦 **9. Frontend Requirements (Streamlit)**

### Screens / Pages
1. Jira Standardization Form
2. LLM Rephrase Preview
3. Zephyr Test Case Generator
4. Step Relevance Visualization
5. Attachment Verification Dashboard
6. Final Governance Score

### UI Features
- Editable steps table
- Relevance % indicators
- Attachment Pass/Fail view
- Project dropdown from Jira
- Multi-step workflow navigation

---

# 🟦 **10. Folder Structure**

```
/ai-governance-platform/
  ├── backend/
  │     ├── main.py
  │     ├── routers/
  │     ├── services/
  │     ├── utils/
  │     ├── models/
  │     ├── config/
  │     └── requirements.txt
  ├── frontend/
  │     ├── app.py
  │     ├── components/
  │     ├── services/
  │     ├── assets/
  │     └── requirements.txt
  ├── README.md
  └── .env.template
```

---

# 🟦 **11. .env Template (Fill Yourself)**
```
# Jira
JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=

# Zephyr
ZEPHYR_BASE_URL=
ZEPHYR_API_KEY=
ZEPHYR_SECRET_KEY=

# Local LLM
LLM_API_URL=
LLM_MODEL=

# OCR
OCR_ENGINE=tesseract
```

---

# 🟦 **12. Deliverables (What GPT‑5 or Copilot Must Generate)**

GPT‑5 must produce:

✔ Full backend FastAPI application  
✔ Full frontend Streamlit application  
✔ All routers, services, utils, models  
✔ Complete Jira + Zephyr API callers  
✔ OCR pipeline  
✔ LLM scoring engine  
✔ Editable JSON/YAML configs  
✔ Dockerfiles (optional)  
✔ README + setup instructions  
✔ Fully runnable local code

---

# 🟦 **13. Important Instructions to LLM (GPT‑5 / Copilot)**
When generating code:
- **Do NOT produce pseudocode.**  
- **Generate real, complete files.**  
- **Include ALL folders and all modules.**  
- **Include error handling, logging, pydantic models.**  
- **Ensure all endpoints work end‑to‑end.**

---

# 🟦 **14. Is this an Agent?**
Yes.  
This is a **multi‑agent Release Governance Automation System**, where each module is an independent intelligent agent:

- Jira Standardization Agent  
- Zephyr Generation Agent  
- Relevance Scoring Agent  
- OCR Verification Agent  
- Governance Scoring Agent  

All coordinated together using FastAPI + Streamlit.

---

# ✅ **Use This Entire File as Prompt**
Paste this `.md` file into GPT‑5 or Copilot to generate the full working application.

You may now edit the Jira/Zephyr/LLM details above before running.

