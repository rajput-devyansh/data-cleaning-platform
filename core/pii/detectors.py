import re
from core.db.duckdb_client import DuckDBClient

PII_PATTERNS = {
    "email": r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    "phone": r"^\+?[0-9\s\-()]{7,}$",
}

def detect_pii_columns(table_name: str, sample_size: int = 500):
    duck = DuckDBClient()

    cols = duck.execute(f"DESCRIBE {table_name}").fetchall()
    results = {}

    for col in cols:
        col_name = col[0]

        matches = {}
        for pii_type, pattern in PII_PATTERNS.items():
            r = duck.execute(f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE CAST("{col_name}" AS VARCHAR) ~ '{pattern}'
                USING SAMPLE {sample_size} ROWS
            """).fetchone()

            matches[pii_type] = r[0]

        if any(v > 0 for v in matches.values()):
            results[col_name] = matches

    duck.close()
    return results