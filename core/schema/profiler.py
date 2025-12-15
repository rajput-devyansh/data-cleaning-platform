from core.db.duckdb_client import DuckDBClient

SAMPLE_SIZE = 5000

def profile_columns(table_name: str):
    duck = DuckDBClient()

    columns = duck.execute(f"DESCRIBE {table_name}").fetchall()
    profiles = {}

    for col in columns:
        col_name = col[0]

        stats = duck.execute(f"""
            SELECT
                COUNT(*) AS total,
                COUNT({col_name}) AS non_null,
                COUNT(*) - COUNT({col_name}) AS nulls
            FROM {table_name}
            USING SAMPLE {SAMPLE_SIZE} ROWS
        """).fetchone()

        profiles[col_name] = {
            "total_sampled": stats[0],
            "non_null": stats[1],
            "nulls": stats[2],
        }

    duck.close()
    return profiles