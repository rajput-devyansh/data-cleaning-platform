from pathlib import Path
from core.db.duckdb_client import DuckDBClient
from core.versioning.naming import dataset_table_name

def load_csv_to_duckdb(
    dataset_id: str,
    version: int,
    file_path: Path,
    encoding: str,
    delimiter: str,
    has_header: bool,
):
    table_name = dataset_table_name(dataset_id, version)

    duck = DuckDBClient()

    duck.execute(f"""
    CREATE TABLE {table_name} AS
    SELECT
        ROW_NUMBER() OVER () AS _row_id,
        *
    FROM read_csv_auto(
        '{file_path.as_posix()}',
        delim='{delimiter}',
        header={str(has_header).lower()},
        encoding='{encoding}'
        )
    """)

    duck.close()
    return table_name