from app.agents.classifier import classify_intent
from app.agents.router import get_agent

from app.memory.stm import store_stm
from app.memory.ltm import store_ltm
from app.memory.scorer import calculate_importance

from app.audit.logger import log_event


def run_orchestrator(
    user_id,
    message
):

    # classify
    intent, confidence = classify_intent(message)

    # select agent
    agent = get_agent(intent)

    # run agent
    response = agent(message)

    # store STM
    store_stm(
        user_id,
        message,
        response
    )

    # score importance
    importance = calculate_importance(message)

    # promote to LTM
    if importance >= 3:

        store_ltm(
            user_id,
            message,
            importance
        )

    # audit log
    log_event(
        user_id,
        message,
        intent,
        confidence,
        agent.__name__,
        response,
        "success"
    )

    return {
        "intent": intent,
        "confidence": confidence,
        "response": response
    }