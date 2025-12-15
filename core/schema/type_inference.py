from core.db.duckdb_client import DuckDBClient

def infer_column_type(table_name: str, column: str):
    duck = DuckDBClient()

    col = f'CAST("{column}" AS VARCHAR)'

    query = f"""
        SELECT
            SUM(CASE WHEN {col} ~ '^[0-9]+$' THEN 1 ELSE 0 END) AS ints,
            SUM(CASE WHEN {col} ~ '^[0-9]+\\.[0-9]+$' THEN 1 ELSE 0 END) AS floats,
            SUM(CASE WHEN {col} ~ '^\\d{{4}}-\\d{{2}}-\\d{{2}}$' THEN 1 ELSE 0 END) AS dates,
            COUNT(*) AS total
        FROM {table_name}
        WHERE "{column}" IS NOT NULL
        USING SAMPLE 5000 ROWS
    """

    r = duck.execute(query).fetchone()
    duck.close()

    total = r[3] or 1  # avoid div by zero

    return {
        "int_ratio": r[0] / total,
        "float_ratio": r[1] / total,
        "date_ratio": r[2] / total,
    }