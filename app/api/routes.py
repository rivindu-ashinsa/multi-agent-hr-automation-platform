from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.database import (
    get_connection
)

from app.agents.orchestrator import (
    graph
)

router = APIRouter()


class UserRequest(BaseModel):
    user_id: str
    message: str


class APIEndpoint(BaseModel):
    method: str
    path: str
    description: str
    parameters: List[str]

    
class RootResponse(BaseModel):
    service: str
    status: str
    version: str
    endpoints: List[APIEndpoint]


@router.get("/", response_model=RootResponse)
def root() -> RootResponse:
    """Return the service metadata and available API endpoints."""

    return {
        "service": "HR Multi-Agent System",
        "status": "running",
        "version": "1.0.0",

        "endpoints": [

            {
                "method": "POST",
                "path": "/request",
                "description": (
                    "Submit a user request to the "
                    "HR orchestration system"
                ),
                "parameters": [
                    "user_id: Unique user identifier",
                    "message: User HR request"
                ]
            },

            {
                "method": "GET",
                "path": "/audit",
                "description": (
                    "Retrieve all audit logs ordered "
                    "by created_at descending"
                ),
                "parameters": []
            },

            {
                "method": "GET",
                "path": "/memory/{user_id}",
                "description": (
                    "Retrieve user short-term and "
                    "long-term memory"
                ),
                "parameters": [
                    "user_id: User identifier"
                ]
            },

            {
                "method": "GET",
                "path": "/health",
                "description": (
                    "System health monitoring endpoint"
                ),
                "parameters": []
            }
        ]
    }


@router.post("/request")
def handle_request(data: UserRequest) -> Dict[str, Any]:
    """Submit a user request to the LangGraph orchestration pipeline."""

    initial_state = {
        "user_id": data.user_id,
        "user_input": data.message 
    }

    result = graph.invoke(initial_state)
    return result


@router.get("/audit")
def get_audit_logs() -> List[Dict[str, Any]]:
    """Return audit log entries ordered from newest to oldest."""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY created_at DESC, id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


@router.get("/memory/{user_id}")
def get_memory(user_id: str) -> Dict[str, Any]:
    """Return the stored short-term and long-term memory for a user."""

    conn = get_connection()

    cursor = conn.cursor()

    # STM
    cursor.execute("""
        SELECT *
        FROM short_term_memory
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,))

    stm = [
        dict(row)
        for row in cursor.fetchall()
    ]

    # LTM
    cursor.execute("""
        SELECT *
        FROM long_term_memory
        WHERE user_id = ?
        ORDER BY importance_score DESC
    """, (user_id,))

    ltm = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return {
        "user_id": user_id,
        "short_term_memory": stm,
        "long_term_memory": ltm
    }


@router.get("/health")
def health_check() -> Dict[str, str]:
    """Return a lightweight health status for the service."""

    return {
        "status": "healthy",
        "service": "hr_multi_agent_system"
    }