# Jira-Zephyr Coverage Analyzer (LangGraph + FastAPI)

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker
```bash
docker build -t jira-zephyr-analyzer .
docker run -p 8000:8000 --env-file .env jira-zephyr-analyzer
```

## API
POST /analyze
```json
{
  "project_key": "MYPROJ",
  "requirement_ids": ["REQ-1", "REQ-2"]
}
```
