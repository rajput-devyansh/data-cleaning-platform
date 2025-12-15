import json
import uuid
from core.db.sqlite_client import SQLiteClient

class ActionLogger:
    def __init__(self):
        self.db = SQLiteClient()

    def log_action(
        self,
        dataset_id: str,
        step: str,
        operation: str,
        parameters: dict | None = None,
    ):
        action_id = str(uuid.uuid4())

        self.db.execute(
            """
            INSERT INTO actions
            (action_id, dataset_id, step, operation, parameters)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                action_id,
                dataset_id,
                step,
                operation,
                json.dumps(parameters or {}),
            ),
        )

        return action_id