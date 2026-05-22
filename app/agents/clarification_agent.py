from app.services.llm_service import (
    generate_response
)


def handle(state):

    user_input = state["user_input"]

    prompt = f"""
        You are a clarification assistant.

        The user's intent is unclear.

        User request:
        {user_input}

        Politely ask for clarification.
        """

    response = generate_response(
        prompt
    )

    state["response"] = response

    return state