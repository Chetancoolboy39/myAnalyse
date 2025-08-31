def fetch_zephyr_tests(state: dict):
    # Stub Zephyr API response with execution status
    tests = [
        {"id": "TEST-1", "description": "Verify login with valid credentials", "status": "PASS"},
        {"id": "TEST-2", "description": "Verify checkout with credit card", "status": "FAIL"},
    ]
    state["tests"] = tests
    return state
