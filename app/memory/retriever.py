from app.core.database import get_connection


def retrieve_memory(state):

    user_id = state["user_id"]

    conn = get_connection()

    cursor = conn.cursor()

    # STM retrieval
    cursor.execute("""
        SELECT message
        FROM short_term_memory
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,))

    stm_rows = cursor.fetchall()

    # LTM retrieval
    cursor.execute("""
        SELECT memory
        FROM long_term_memory
        WHERE user_id = ?
        ORDER BY importance_score DESC
        LIMIT 3
    """, (user_id,))

    ltm_rows = cursor.fetchall()

    conn.close()

    state["stm_memory"] = [
        row["message"]
        for row in stm_rows
    ]

    state["ltm_memory"] = [
        row["memory"]
        for row in ltm_rows
    ]

    return state