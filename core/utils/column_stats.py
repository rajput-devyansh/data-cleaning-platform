from core.db.duckdb_client import DuckDBClient

def column_null_stats(table_name: str, column: str):
    duck = DuckDBClient()
    result = duck.execute(
        f'''
        SELECT
            COUNT(*) AS total,
            COUNT("{column}") AS non_null,
            COUNT(*) - COUNT("{column}") AS nulls
        FROM {table_name}
        '''
    ).fetchone()
    duck.close()

    return {
        "total": result[0],
        "non_null": result[1],
        "nulls": result[2],
    }