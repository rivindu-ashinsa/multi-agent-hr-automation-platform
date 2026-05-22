from app.services.llm_service import (
    generate_response
)


def handle(state):

    user_input = state["user_input"]

    stm = state["stm_memory"]

    ltm = state["ltm_memory"]

    prompt = f"""
        You are a scheduling assistant.

        Recent conversation history:
        {stm}

        Long-term user information:
        {ltm}

        Current user request:
        {user_input}

        Provide a helpful HR scheduling response.
        """

    response = generate_response(
        prompt
    )

    state["response"] = response

    return state