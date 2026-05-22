import os
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


FIXTURE_PATH = Path(__file__).with_name("fixtures") / "mock_data.json"


def load_mock_data() -> dict:
    with FIXTURE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def create_temp_db(db_path: Path, data: dict) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS short_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            response TEXT
        );

        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            memory TEXT,
            importance_score INTEGER
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            request TEXT,
            intent TEXT,
            confidence REAL,
            agent TEXT,
            response TEXT,
            status TEXT,
            created_at TEXT
        );
        """
    )

    cursor.execute("DELETE FROM short_term_memory")
    cursor.execute("DELETE FROM long_term_memory")
    cursor.execute("DELETE FROM audit_logs")

    for row in data["short_term_memory"]:
        cursor.execute(
            """
            INSERT INTO short_term_memory (id, user_id, message, response)
            VALUES (?, ?, ?, ?)
            """,
            (row["id"], row["user_id"], row["message"], row["response"]),
        )

    for row in data["long_term_memory"]:
        cursor.execute(
            """
            INSERT INTO long_term_memory (id, user_id, memory, importance_score)
            VALUES (?, ?, ?, ?)
            """,
            (row["id"], row["user_id"], row["memory"], row["importance_score"]),
        )

    for row in data["audit_logs"]:
        cursor.execute(
            """
            INSERT INTO audit_logs
            (id, user_id, request, intent, confidence, agent, response, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["user_id"],
                row["request"],
                row["intent"],
                row["confidence"],
                row["agent"],
                row["response"],
                row["status"],
                row["created_at"],
            ),
        )

    connection.commit()
    connection.close()


class ApiEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_data = load_mock_data()
        fd, raw_path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(fd)
        cls.db_path = Path(raw_path)
        create_temp_db(cls.db_path, cls.mock_data)
        cls.client = TestClient(app)
        cls.captured_request_state = None

        def fake_get_connection():
            connection = sqlite3.connect(cls.db_path)
            connection.row_factory = sqlite3.Row
            return connection

        def fake_graph_invoke(initial_state):
            cls.captured_request_state = initial_state
            return cls.mock_data["request_result"]

        cls.get_connection_patch = patch("app.api.routes.get_connection", new=fake_get_connection)
        cls.graph_invoke_patch = patch("app.api.routes.graph.invoke", new=fake_graph_invoke)
        cls.get_connection_patch.start()
        cls.graph_invoke_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_connection_patch.stop()
        cls.graph_invoke_patch.stop()
        if cls.db_path.exists():
            cls.db_path.unlink()

    def test_root_lists_endpoints(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["service"], "HR Multi-Agent System")
        self.assertEqual(payload["status"], "running")
        self.assertEqual(len(payload["endpoints"]), 5)

    def test_request_routes_to_graph(self):
        response = self.client.post(
            "/request",
            json={"user_id": "u-100", "message": "Schedule a meeting"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.mock_data["request_result"])
        self.assertEqual(
            self.captured_request_state,
            {"user_id": "u-100", "user_input": "Schedule a meeting"},
        )

    def test_audit_returns_newest_first(self):
        response = self.client.get("/audit")
        self.assertEqual(response.status_code, 200)

        rows = response.json()
        self.assertEqual(rows[0]["created_at"], "2026-05-22 10:00:00")
        self.assertEqual(rows[1]["created_at"], "2026-05-21 10:00:00")

    def test_memory_returns_stm_and_ltm(self):
        response = self.client.get("/memory/u-100")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["user_id"], "u-100")
        self.assertEqual(
            [row["message"] for row in payload["short_term_memory"]],
            ["Newer memory", "Older memory"],
        )
        self.assertEqual(
            [row["memory"] for row in payload["long_term_memory"]],
            ["High priority memory", "Low priority memory"],
        )

    def test_health_returns_ok(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy", "service": "hr_multi_agent_system"})


if __name__ == "__main__":
    unittest.main()
