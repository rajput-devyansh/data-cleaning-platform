from core.db.duckdb_client import DuckDBClient

def count_nulls(table_name: str, column: str):
    duck = DuckDBClient()
    r = duck.execute(
        f'SELECT COUNT(*) FROM {table_name} WHERE "{column}" IS NULL'
    ).fetchone()
    duck.close()
    return r[0]

def count_empty_strings(table_name: str, column: str):
    duck = DuckDBClient()
    r = duck.execute(
        f'''
        SELECT COUNT(*) FROM {table_name}
        WHERE TRIM("{column}") = ''
        '''
    ).fetchone()
    duck.close()
    return r[0]

def count_duplicates(table_name: str, columns: list[str]):
    cols = ", ".join(f'"{c}"' for c in columns)
    duck = DuckDBClient()
    r = duck.execute(
        f"""
        SELECT SUM(cnt - 1)
        FROM (
            SELECT COUNT(*) AS cnt
            FROM {table_name}
            GROUP BY {cols}
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()
    duck.close()
    return r[0] or 0