from core.db.duckdb_client import DuckDBClient
from core.versioning.naming import dataset_table_name
from core.versioning.version_manager import VersionManager
from core.audit.action_logger import ActionLogger

class CleaningEngine:
    def __init__(self):
        self.vm = VersionManager()
        self.logger = ActionLogger()

    def apply_rule(
        self,
        dataset_id: str,
        source_version: int,
        rule_sql: str,
        operation: str,
        parameters: dict,
    ):
        target_version = source_version + 1
        source_table = dataset_table_name(dataset_id, source_version)
        target_table = dataset_table_name(dataset_id, target_version)

        duck = DuckDBClient()
        duck.execute(rule_sql.format(
            source_table=source_table,
            target_table=target_table,
        ))
        duck.close()

        self.vm.create_version(
            dataset_id,
            target_version,
            target_table,
        )

        self.logger.log_action(
            dataset_id,
            step="Cleaning",
            operation=operation,
            parameters=parameters,
        )

        return target_version