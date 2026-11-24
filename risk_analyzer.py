
def calculate_risk(pattern, evidence_count=1):

    base_scores = {
        "Nagging": 30,
        "Obstruction": 65,
        "Sneaking": 80,
        "Interface Interference": 50,
        "Forced Action": 70
    }

    if pattern not in base_scores:
        return {"score": 0, "level": "Unknown"}

    # Base risk + additional evidence
    score = base_scores[pattern] + (evidence_count - 1) * 5

    # Keep score within 0–100
    score = min(score, 100)

    if score < 35:
        level = "Low"
    elif score < 65:
        level = "Medium"
    else:
        level = "High"

    return {
        "score": score,
        "level": level
    }
