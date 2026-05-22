from app.memory.stm import store_stm
from app.memory.ltm import store_ltm
from app.memory.scorer import (
    calculate_importance
)


def memory_node(state):

    user_id = state["user_id"]

    message = state["user_input"]

    response = state["response"]

    # always store STM
    store_stm(
        user_id,
        message,
        response
    )

    # calculate importance
    score = calculate_importance(
        message
    )

    state["importance_score"] = score

    # store LTM if important
    if score >= 3:

        store_ltm(
            user_id,
            message,
            score
        )

    return state