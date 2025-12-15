from core.db.duckdb_client import DuckDBClient
from core.versioning.naming import dataset_table_name
from core.versioning.version_manager import VersionManager
from core.audit.action_logger import ActionLogger
from core.utils.impact import count_rows
from core.utils.column_stats import column_null_stats

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

        rows_before = count_rows(source_table)
        
        column_stats_before = None
        if "column" in parameters:
            column_stats_before = column_null_stats(
                source_table,
                parameters["column"],
            )

        duck = DuckDBClient()

        duck.execute(rule_sql.format(
            source_table=source_table,
            target_table=target_table,
        ))
        
        duck.close()

        rows_after = count_rows(target_table)

        self.vm.create_version(
            dataset_id,
            target_version,
            target_table,
        )

        self.vm.db.execute(
            "UPDATE datasets SET status = ? WHERE dataset_id = ?",
            ("cleaned", dataset_id),
        )

        log_params = {
            **parameters,
            "rows_before": rows_before,
            "rows_after": rows_after,
            "rows_changed": rows_before - rows_after,
        }

        if column_stats_before:
            log_params["column_stats_before"] = column_stats_before

        self.logger.log_action(
            dataset_id,
            step="Cleaning",
            operation=operation,
            parameters=log_params,
        )

        return target_version