import sqlite3
from core.config import SQLITE_DIR

class SQLiteClient:
    def __init__(self, db_name: str = "metadata.db"):
        self.db_path = SQLITE_DIR / db_name
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query: str, params=None):
        cur = self.conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        self.conn.commit()
        return cur

    def fetchall(self, query: str, params=None):
        cur = self.execute(query, params)
        return cur.fetchall()

    def close(self):
        self.conn.close()