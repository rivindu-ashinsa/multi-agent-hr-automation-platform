from app.services.llm_service import (
    generate_response
)


def handle(state):

    user_input = state["user_input"]

    stm = state["stm_memory"]

    ltm = state["ltm_memory"]

    prompt = f"""
        You are an HR leave management assistant.

        Recent conversation history:
        {stm}

        Long-term user information:
        {ltm}

        Current request:
        {user_input}

        Provide a helpful leave-management response.
        """

    response = generate_response(
        prompt
    )

    state["response"] = response

    return state