def drop_nulls_sql(source_table: str, target_table: str, column: str):
    return f"""
    CREATE TABLE {target_table} AS
    SELECT *
    FROM {source_table}
    WHERE "{column}" IS NOT NULL
    """

def fill_nulls_sql(
    source_table: str,
    target_table: str,
    column: str,
    value,
):
    return f"""
    CREATE TABLE {target_table} AS
    SELECT
        *,
        COALESCE("{column}", '{value}') AS "{column}"
    FROM {source_table}
    """

def drop_duplicates_sql(
    source_table: str,
    target_table: str,
    columns: list[str],
):
    cols = ", ".join(f'"{c}"' for c in columns)
    return f"""
    CREATE TABLE {target_table} AS
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY {cols}) AS rn
        FROM {source_table}
    )
    WHERE rn = 1
    """