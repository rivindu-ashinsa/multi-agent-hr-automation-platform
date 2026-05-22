import re


def calculate_importance(message: str):
    """Estimate how valuable a message is for long-term memory."""

    if not message:
        return 0

    msg = message.strip().lower()
    score = 0

    # Identity / profile facts
    identity_patterns = (
        r"\bmy name is\b",
        r"\bi am\b",
        r"\bi'm\b",
        r"\bcall me\b",
        r"\bmy title is\b",
        r"\bmy role is\b",
    )
    for pattern in identity_patterns:
        if re.search(pattern, msg):
            score += 4

    # Preferences and recurring behavior
    preference_patterns = (
        r"\bi prefer\b",
        r"\bi like\b",
        r"\bi love\b",
        r"\bi always\b",
        r"\bi never\b",
        r"\bplease remember\b",
        r"\bremember that\b",
        r"\bmy preference\b",
    )
    for pattern in preference_patterns:
        if re.search(pattern, msg):
            score += 3

    # Work and organizational context
    work_patterns = (
        r"\bdepartment\b",
        r"\bteam\b",
        r"\bmanager\b",
        r"\bproject\b",
        r"\bdeadline\b",
        r"\bschedule\b",
        r"\blocation\b",
        r"\btimezone\b",
    )
    for pattern in work_patterns:
        if re.search(pattern, msg):
            score += 2

    # Explicit durable-memory signals
    durable_patterns = (
        r"\balways\b",
        r"\bnever\b",
        r"\btypically\b",
        r"\busually\b",
        r"\bimportant to me\b",
        r"\bkeep in mind\b",
        r"\bfor future reference\b",
    )
    for pattern in durable_patterns:
        if re.search(pattern, msg):
            score += 2

    # Relationship / personalization hints
    if any(term in msg for term in ("partner", "spouse", "child", "family", "friend")):
        score += 1

    # Longer statements often contain richer memory candidates
    word_count = len(re.findall(r"\b\w+\b", msg))
    if word_count >= 25:
        score += 1
    if word_count >= 50:
        score += 1

    # Strong self-disclosure and structured preference statements
    if re.search(r"\b(my|our) (name|role|department|team|timezone|preference|favorite)\b", msg):
        score += 2

    return min(score, 10)