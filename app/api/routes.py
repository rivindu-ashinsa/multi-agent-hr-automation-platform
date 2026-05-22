from fastapi import APIRouter

from app.agents.orchestrator import (
    run_orchestrator
)

router = APIRouter()




@router.get("/")
def root():
    return {"message": "Application is running!"}

@router.post("/request")
def handle_request(data: dict):

    user_id = data["user_id"]
    message = data["message"]

    return run_orchestrator(
        user_id,
        message
    )