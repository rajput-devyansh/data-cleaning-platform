import json
from core.db.duckdb_client import DuckDBClient
from core.config import EXPORTS_DIR

def export_dataset(table_name: str, dataset_id: str):
    duck = DuckDBClient()

    data_path = EXPORTS_DIR / f"{dataset_id}.csv"
    meta_path = EXPORTS_DIR / f"{dataset_id}_metadata.json"

    duck.execute(f"""
        COPY {table_name}
        TO '{data_path.as_posix()}'
        (HEADER, DELIMITER ',')
    """)

    duck.close()

    meta = {
        "dataset": dataset_id,
        "table": table_name,
    }

    meta_path.write_text(json.dumps(meta, indent=2))

    return data_path, meta_path