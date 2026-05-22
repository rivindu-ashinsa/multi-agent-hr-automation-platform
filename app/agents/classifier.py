def classify_intent(message: str):
    msg = message.lower()

    keywords = {
        "scheduling": ["schedule", "meeting", "interview", "appointment", "calendar", "time", "date", "book", "arrange", "set up"],
        "leave": ["leave", "vacation", "holiday", "absent", "time off", "days off", "sick leave", "annual leave", "request", "approval"],
        "compliance": ["policy", "rule", "regulation", "compliance", "guideline", "code of conduct", "ethics", "agreement", "contract", "legal"],
        "clarification": [
            "what",
            "who",
            "how",
            "when",
            "where",
            "clarify",
            "clarification",
            "details",
            "more info",
            "explain",
            "question",
            "policy"
        ],
    }

    # initialize scores for all intents defined in keywords
    scores = {intent: 0 for intent in keywords}

    # count occurrences of each keyword to allow larger keyword sets
    for intent, words in keywords.items():
        for word in words:
            count = msg.count(word)
            if count:
                # weight each occurrence; keep same relative weighting as before
                scores[intent] += 2 * count
    total = sum(scores.values())
    if total == 0:
        return "clarification", 0.0

    normalized = {key: round(value / total, 2) for key, value in scores.items()}
    best_intent = max(normalized, key=normalized.get)

    return best_intent, normalized[best_intent]

