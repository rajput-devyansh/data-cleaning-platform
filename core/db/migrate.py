from pathlib import Path
from core.db.sqlite_client import SQLiteClient

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

def run_migrations():
    client = SQLiteClient()

    for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        with open(sql_file, "r") as f:
            sql = f.read()
            client.conn.executescript(sql)

    client.close()