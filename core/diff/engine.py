from core.db.duckdb_client import DuckDBClient
from core.diff.models import DatasetDiff, DiffSummary, RowDiff

def find_added_and_removed_rows(
    table_a: str,
    table_b: str,
):
    """
    Returns:
        added_row_ids, removed_row_ids
    """
    duck = DuckDBClient()

    added = duck.execute(f"""
        SELECT _row_id
        FROM {table_b}
        WHERE _row_id NOT IN (
            SELECT _row_id FROM {table_a}
        )
    """).fetchall()

    removed = duck.execute(f"""
        SELECT _row_id
        FROM {table_a}
        WHERE _row_id NOT IN (
            SELECT _row_id FROM {table_b}
        )
    """).fetchall()

    duck.close()

    return (
        [r[0] for r in added],
        [r[0] for r in removed],
    )

def _get_data_columns(table_name: str):
    duck = DuckDBClient()
    cols = duck.execute(
        f"DESCRIBE {table_name}"
    ).fetchall()
    duck.close()

    return [c[0] for c in cols if c[0] != "_row_id"]

def find_modified_rows(
    table_a: str,
    table_b: str,
    limit: int = 100,
):
    duck = DuckDBClient()
    columns = _get_data_columns(table_a)

    # Build diff detection + value retrieval in ONE query
    select_exprs = ["a._row_id"]
    diff_conditions = []

    for col in columns:
        select_exprs.append(f'a."{col}" AS a_{col}')
        select_exprs.append(f'b."{col}" AS b_{col}')
        diff_conditions.append(f'a."{col}" IS DISTINCT FROM b."{col}"')

    query = f"""
        SELECT {", ".join(select_exprs)}
        FROM {table_a} a
        JOIN {table_b} b
          ON a._row_id = b._row_id
        WHERE {" OR ".join(diff_conditions)}
        LIMIT {limit}
    """

    rows = duck.execute(query).fetchall()
    duck.close()

    modified = []

    for row in rows:
        row_id = row[0]
        values = row[1:]

        changes = {}
        for i, col in enumerate(columns):
            before = values[2 * i]
            after = values[2 * i + 1]
            if before != after:
                changes[col] = {
                    "before": before,
                    "after": after,
                }

        modified.append(RowDiff(row_id=row_id, changes=changes))

    return modified

def diff_datasets(
    table_a: str,
    table_b: str,
):
    added, removed = find_added_and_removed_rows(table_a, table_b)
    modified = find_modified_rows(table_a, table_b)

    summary = DiffSummary(
        rows_added=len(added),
        rows_removed=len(removed),
        rows_modified=len(modified),
    )

    return DatasetDiff(
        summary=summary,
        added_row_ids=added,
        removed_row_ids=removed,
        modified_rows=modified,
    )