from core.db.sqlite_client import SQLiteClient

class UndoEngine:
    def __init__(self):
        self.db = SQLiteClient()

    def set_active_version(self, dataset_id: str, version: int):
        # deactivate all
        self.db.execute(
            """
            UPDATE dataset_versions
            SET is_active = 0
            WHERE dataset_id = ?
            """,
            (dataset_id,),
        )

        # activate selected
        self.db.execute(
            """
            UPDATE dataset_versions
            SET is_active = 1
            WHERE dataset_id = ? AND version = ?
            """,
            (dataset_id, version),
        )