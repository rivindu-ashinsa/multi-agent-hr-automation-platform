from app.core.database import get_connection


def store_ltm(
    user_id,
    memory,
    score
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO long_term_memory
        (user_id, memory, importance_score)
        VALUES (?, ?, ?)
    """, (user_id, memory, score))

    conn.commit()
    conn.close()