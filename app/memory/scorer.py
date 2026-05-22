def calculate_importance(message: str):

    msg = message.lower()

    score = 0

    if "prefer" in msg:
        score += 3

    if "always" in msg:
        score += 2

    if "my name is" in msg:
        score += 3

    if "department" in msg:
        score += 2

    return score