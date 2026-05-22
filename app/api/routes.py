from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.orchestrator import (
    graph
)

router = APIRouter()


class UserRequest(BaseModel):
    user_id: str
    message: str

@router.post("/request")
def handle_request(data: UserRequest):
    # 2. Map request data to match your AgentState keys
    initial_state = {
        "user_id": data.user_id,
        "user_input": data.message 
    }
    
    # 3. Pass the dictionary directly to the graph
    result = graph.invoke(initial_state)
    return result