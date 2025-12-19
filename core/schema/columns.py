from core.db.duckdb_client import DuckDBClient


def get_dataset_columns(dataset_id: str, version: int) -> list[str]:
    table_name = f"{dataset_id}_v{version}"

    duck = DuckDBClient()
    result = duck.execute(f"PRAGMA table_info('{table_name}')").fetchall()
    duck.close()

    # PRAGMA table_info returns rows where column name is at index 1
    return [row[1] for row in result]