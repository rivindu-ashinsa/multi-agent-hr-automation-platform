def handle(state):

    memories = state.get("ltm_memory", [])

    response = (
        "Clarification requested. Please provide more details about your HR request."
    )

    if memories:
        response += (
            f" Context found: {memories}"
        )

    state["response"] = response

    return state