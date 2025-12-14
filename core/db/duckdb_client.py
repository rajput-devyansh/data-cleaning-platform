import duckdb
from core.config import DUCKDB_DIR

class DuckDBClient:
    def __init__(self, db_name: str = "data.duckdb"):
        self.db_path = DUCKDB_DIR / db_name
        self.conn = duckdb.connect(str(self.db_path))

    def execute(self, query: str, params=None):
        if params:
            return self.conn.execute(query, params)
        return self.conn.execute(query)

    def fetch_df(self, query: str):
        return self.conn.execute(query).fetchdf()

    def close(self):
        self.conn.close()