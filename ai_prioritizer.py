import re

# Explainable, offline AI-style prioritizer.
# It uses weighted urgency signals so the project works without an API key.
CRITICAL_TERMS = {
    "fire": 35, "smoke": 30, "gas leak": 40, "electrical shock": 40,
    "electrocution": 40, "violent": 35, "assault": 35, "emergency": 35,
    "life threatening": 45, "life-threatening": 45
}

HIGH_TERMS = {
    "no water": 25, "water supply": 18, "power outage": 22,
    "electricity": 16, "unsafe": 20, "harassment": 22,
    "bullying": 18, "security": 18, "broken toilet": 15,
    "food poisoning": 30, "poisoning": 30, "injury": 28,
    "medical": 22, "urgent": 20, "exam": 16
}

MEDIUM_TERMS = {
    "wifi": 10, "internet": 10, "projector": 8, "classroom": 7,
    "library": 6, "canteen": 7, "hostel": 6, "transport": 7,
    "maintenance": 6, "leak": 8
}

CATEGORY_BONUS = {
    "Safety": 12,
    "Medical": 15,
    "Hostel": 5,
    "Academic": 4,
    "Infrastructure": 4,
    "IT / Wi-Fi": 2,
    "Transport": 3,
    "Food / Canteen": 8,
    "Other": 0
}

def _clean(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def prioritize_complaint(title, description, category):
    text = _clean(f"{title} {description}")
    score = CATEGORY_BONUS.get(category, 0)
    reasons = []

    for term, weight in CRITICAL_TERMS.items():
        if term in text:
            score += weight
            reasons.append(f"critical signal: '{term}'")

    for term, weight in HIGH_TERMS.items():
        if term in text:
            score += weight
            reasons.append(f"urgent signal: '{term}'")

    for term, weight in MEDIUM_TERMS.items():
        if term in text:
            score += weight
            reasons.append(f"service signal: '{term}'")

    if any(x in text for x in ["many students", "entire hostel", "whole campus", "everyone"]):
        score += 15
        reasons.append("wide student impact")

    if any(x in text for x in ["2 days", "three days", "3 days", "week", "weeks"]):
        score += 8
        reasons.append("extended duration")

    if score >= 50:
        priority = "Critical"
    elif score >= 30:
        priority = "High"
    elif score >= 15:
        priority = "Medium"
    else:
        priority = "Low"

    if not reasons:
        reasons.append("no strong urgency indicators detected")

    return {
        "priority": priority,
        "score": min(score, 100),
        "reason": "; ".join(reasons[:4])
    }
