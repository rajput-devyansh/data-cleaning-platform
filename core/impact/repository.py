import json
from core.db.sqlite_client import SQLiteClient


class ImpactRepository:
    def __init__(self):
        self.db = SQLiteClient()

    def get_actions_for_dataset(self, dataset_id: str):
        rows = self.db.fetchall(
            """
            SELECT
                action_id,
                step,
                operation,
                parameters,
                created_at
            FROM actions
            WHERE dataset_id = ?
            ORDER BY created_at ASC
            """,
            (dataset_id,),
        )

        actions = []
        for r in rows:
            params = {}
            if r["parameters"]:
                try:
                    params = json.loads(r["parameters"])
                except Exception:
                    params = {}

            actions.append(
                {
                    "action_id": r["action_id"],
                    "step": r["step"],
                    "operation": r["operation"],
                    "parameters": params,
                    "created_at": r["created_at"],
                    "version_before": params.get("version_before"),
                    "version_after": params.get("version_after"),
                }
            )

        return actions