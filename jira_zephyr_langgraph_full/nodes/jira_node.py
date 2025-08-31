def fetch_jira_requirements(state: dict):
    project_key = state.get("project_key")
    # Stub Jira API response
    requirements = [
        {"id": "JIRA-1", "summary": "Login functionality", "description": "User must log in using username and password"},
        {"id": "JIRA-2", "summary": "Checkout process", "description": "User should be able to checkout with payment gateway"},
    ]
    state["requirements"] = requirements
    return state
