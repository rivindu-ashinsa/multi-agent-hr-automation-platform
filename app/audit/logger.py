from app.core.database import get_connection


def log_event(
    user_id,
    request,
    intent,
    confidence,
    agent,
    response,
    status
):

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
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        request,
        intent,
        confidence,
        agent,
        response,
        status
    ))

    conn.commit()
    conn.close()