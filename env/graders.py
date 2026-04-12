def grade(task, result):
    task_id = task.get("id") or task.get("name")
    score = 0.0

    if task_id == "route_correct_department":
        if result.get("correct_department") == result.get("action"):
            score = 1.0

    elif task_id == "handle_high_urgency":
        if result.get("urgency", 0) > 70 and not result.get("redirected"):
            score = 1.0

    elif task_id == "use_resources_efficiently":
        if not result.get("redirected"):
            score = 1.0

    return score