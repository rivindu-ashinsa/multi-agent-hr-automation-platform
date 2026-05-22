def handle(state):

    memories = state["ltm_memory"]

    response = (
        "Leave  request processed."
    )

    if memories:
        response += (
            f" Context found: {memories}"
        )

    state["response"] = response

    return state