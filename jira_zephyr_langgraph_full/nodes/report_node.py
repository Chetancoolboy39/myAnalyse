def generate_report(state: dict):
    results = state.get("coverage_results", [])
    report_lines = []

    for result in results:
        req = result["requirement"]
        test = result["matched_test"]
        similarity = result["similarity"]
        if test:
            report_lines.append(
                f"Requirement {req['id']} ({req['summary']}): "
                f"covered by Test {test['id']} (status={test['status']}, sim={similarity:.2f})"
            )
        else:
            report_lines.append(f"Requirement {req['id']} ({req['summary']}): NO TEST FOUND")

    state["report"] = "\n".join(report_lines)
    return state
