from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from nodes.jira_node import fetch_jira_requirements
from nodes.zephyr_node import fetch_zephyr_tests
from nodes.coverage_node import compute_coverage
from nodes.report_node import generate_report

app = FastAPI()

class AnalysisRequest(BaseModel):
    project_key: str

class AnalysisResponse(BaseModel):
    report: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(req: AnalysisRequest):
    # Build the LangGraph workflow
    workflow = StateGraph(dict)
    workflow.add_node("jira", fetch_jira_requirements)
    workflow.add_node("zephyr", fetch_zephyr_tests)
    workflow.add_node("coverage", compute_coverage)
    workflow.add_node("report", generate_report)

    workflow.add_edge("jira", "zephyr")
    workflow.add_edge("zephyr", "coverage")
    workflow.add_edge("coverage", "report")
    workflow.add_edge("report", END)

    workflow.set_entry_point("jira")
    app_graph = workflow.compile()

    # Run the graph with project key
    result = app_graph.invoke({"project_key": req.project_key})
    return {"report": result.get("report", "No report generated")}
