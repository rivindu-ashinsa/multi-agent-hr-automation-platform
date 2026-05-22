from app.agents import clarification_agent, compliance_agent, leave_agent, scheduling_agent

def get_agent(intent: str):

    if intent == "scheduling":
        return scheduling_agent.handle

    if intent == "leave":
        return leave_agent.handle

    if intent == "compliance":
        return compliance_agent.handle

    return clarification_agent.handle
