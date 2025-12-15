from core.db.duckdb_client import DuckDBClient

def count_rows(table_name: str) -> int:
    duck = DuckDBClient()
    result = duck.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()
    duck.close()
    return result[0]