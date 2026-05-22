def choose_agent(state):

    intent = state["intent"]

    if intent == "scheduling":
        state["selected_agent"] = (
            "scheduling"
        )

    elif intent == "leave":
        state["selected_agent"] = (
            "leave"
        )

    elif intent == "compliance":
        state["selected_agent"] = (
            "compliance"
        )

    else:
        state["selected_agent"] = (
            "clarification"
        )

    return state