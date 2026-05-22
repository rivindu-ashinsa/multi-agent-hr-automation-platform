from typing import TypedDict
from typing import List


class AgentState(TypedDict):

    user_id: str

    user_input: str

    intent: str

    confidence: float

    selected_agent: str

    stm_memory: List[str]

    ltm_memory: List[str]

    response: str

    importance_score: float

    audit_logged: bool