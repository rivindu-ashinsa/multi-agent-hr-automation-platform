from app.core.database import get_connection


def store_stm(
    user_id,
    message,
    response
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO short_term_memory
        (user_id, message, response)
        VALUES (?, ?, ?)
    """, (user_id, message, response))

    conn.commit()
    conn.close()