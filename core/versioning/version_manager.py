from core.db.sqlite_client import SQLiteClient

class VersionManager:
    def __init__(self):
        self.db = SQLiteClient()

    def register_dataset(self, dataset_id: str, name: str):
        self.db.execute(
            """
            INSERT OR IGNORE INTO datasets (dataset_id, name)
            VALUES (?, ?)
            """,
            (dataset_id, name),
        )

    def create_version(
        self,
        dataset_id: str,
        version: int,
        table_name: str,
        make_active: bool = True,
    ):
        if make_active:
            # deactivate existing versions
            self.db.execute(
                """
                UPDATE dataset_versions
                SET is_active = 0
                WHERE dataset_id = ?
                """,
                (dataset_id,),
            )

        self.db.execute(
            """
            INSERT INTO dataset_versions
            (dataset_id, version, table_name, is_active)
            VALUES (?, ?, ?, ?)
            """,
            (dataset_id, version, table_name, make_active),
        )

    def get_active_version(self, dataset_id: str):
        rows = self.db.fetchall(
            """
            SELECT version, table_name
            FROM dataset_versions
            WHERE dataset_id = ? AND is_active = 1
            """,
            (dataset_id,),
        )
        return rows[0] if rows else None

    def list_versions(self, dataset_id: str):
        return self.db.fetchall(
            """
            SELECT version, table_name, is_active
            FROM dataset_versions
            WHERE dataset_id = ?
            ORDER BY version
            """,
            (dataset_id,),
        )
    
    def get_dataset(self, dataset_id: str):
        rows = self.db.fetchall(
            """
            SELECT dataset_id, name, status
            FROM datasets
            WHERE dataset_id = ?
            """,
            (dataset_id,),
        )
        return rows[0] if rows else None