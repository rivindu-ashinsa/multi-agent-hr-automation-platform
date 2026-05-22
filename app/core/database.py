import sqlite3

DB_PATH = "app.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS short_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            response TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            memory TEXT,
            importance_score INTEGER
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            request TEXT,
            intent TEXT,
            confidence REAL,
            agent TEXT,
            response TEXT,
            status TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TRIGGER IF NOT EXISTS audit_logs_prevent_update
        BEFORE UPDATE ON audit_logs
        BEGIN
            SELECT RAISE(ABORT, 'audit_logs is append-only');
        END;
        """
    )

    cursor.execute(
        """
        CREATE TRIGGER IF NOT EXISTS audit_logs_prevent_delete
        BEFORE DELETE ON audit_logs
        BEGIN
            SELECT RAISE(ABORT, 'audit_logs is append-only');
        END;
        """
    )

    cursor.execute("PRAGMA table_info(audit_logs)")
    audit_columns = {row[1] for row in cursor.fetchall()}

    if "created_at" not in audit_columns:
        cursor.execute("ALTER TABLE audit_logs ADD COLUMN created_at TEXT")
        cursor.execute(
            """
            UPDATE audit_logs
            SET created_at = CURRENT_TIMESTAMP
            WHERE created_at IS NULL
            """
        )

    conn.commit()
    conn.close()
