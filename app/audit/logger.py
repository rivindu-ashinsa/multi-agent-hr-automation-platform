from app.core.database import get_connection


def audit_node(state):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs
        (
            user_id,
            request,
            intent,
            confidence,
            agent,
            response,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        state["user_id"],
        state["user_input"],
        state["intent"],
        state["confidence"],
        state["selected_agent"],
        state["response"],
        "success"
    ))

    conn.commit()
    conn.close()

    state["audit_logged"] = True

    return state