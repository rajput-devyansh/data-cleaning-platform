import json
from core.db.duckdb_client import DuckDBClient
from core.db.sqlite_client import SQLiteClient
from core.audit.action_logger import ActionLogger
from core.versioning.naming import dataset_table_name
from core.utils.impact import count_rows

def apply_schema(
    dataset_id: str,
    source_version: int,
    target_version: int,
    schema: dict,
):
    source_table = dataset_table_name(dataset_id, source_version)
    target_table = dataset_table_name(dataset_id, target_version)
    quarantine_table = f"{target_table}_quarantine"

    duck = DuckDBClient()

    select_expr = []
    invalid_conditions = []

    for col, dtype in schema.items():
        cast_expr = f'TRY_CAST("{col}" AS {dtype})'
        select_expr.append(f"{cast_expr} AS \"{col}\"")
        invalid_conditions.append(f"{cast_expr} IS NULL AND \"{col}\" IS NOT NULL")

    # 1️⃣ Clean table (only valid rows)
    duck.execute(f"""
        CREATE TABLE {target_table} AS
        SELECT {', '.join(select_expr)}
        FROM {source_table}
        WHERE NOT ({' OR '.join(invalid_conditions)})
    """)

    # 2️⃣ Quarantine table (invalid rows)
    duck.execute(f"""
        CREATE TABLE {quarantine_table} AS
        SELECT *
        FROM {source_table}
        WHERE {' OR '.join(invalid_conditions)}
    """)

    duck.close()

    rows_before = count_rows(source_table)
    rows_after = count_rows(target_table)
    rows_quarantined = count_rows(quarantine_table)

    # 3️⃣ Store schema & lock
    db = SQLiteClient()
    db.execute(
        """
        INSERT INTO schemas
        (dataset_id, version, schema_json, is_locked)
        VALUES (?, ?, ?, 1)
        """,
        (dataset_id, target_version, json.dumps(schema)),
    )
    db.execute(
        "UPDATE datasets SET status = ? WHERE dataset_id = ?",
        ("schema_locked", dataset_id),
    )

    ActionLogger.log_action(
        dataset_id,
        step="Schema",
        operation="schema_lock",
        parameters={
            "schema": schema,
            "rows_before": rows_before,
            "rows_after": rows_after,
            "rows_quarantined": rows_quarantined,
        },
    )

    return {
        "clean_table": target_table,
        "quarantine_table": quarantine_table,
    }