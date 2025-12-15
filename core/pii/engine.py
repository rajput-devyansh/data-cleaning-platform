from core.db.duckdb_client import DuckDBClient
from core.versioning.naming import dataset_table_name
from core.versioning.version_manager import VersionManager
from core.audit.action_logger import ActionLogger

class PIIEngine:
    def __init__(self):
        self.vm = VersionManager()
        self.logger = ActionLogger()

    def apply_masking(
        self,
        dataset_id: str,
        source_version: int,
        masking_rules: dict,
    ):
        target_version = source_version + 1
        source = dataset_table_name(dataset_id, source_version)
        target = dataset_table_name(dataset_id, target_version)

        select_expr = []
        for col, expr in masking_rules.items():
            select_expr.append(f"{expr} AS \"{col}\"")

        duck = DuckDBClient()
        duck.execute(f"""
            CREATE TABLE {target} AS
            SELECT
                *,
                {', '.join(select_expr)}
            FROM {source}
        """)
        duck.close()

        self.vm.create_version(dataset_id, target_version, target)

        self.logger.log_action(
            dataset_id,
            step="PII",
            operation="masking",
            parameters=masking_rules,
        )

        return target_version