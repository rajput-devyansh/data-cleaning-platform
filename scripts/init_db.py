from core.config import DATA_DIR
from core.db.migrate import run_migrations
from core.db.duckdb_client import DuckDBClient

def main():
    print("Initializing local databases...")

    # Initialize DuckDB
    duck = DuckDBClient()
    duck.execute("SELECT 1")
    duck.close()
    print("DuckDB initialized")

    # Initialize SQLite + migrations
    run_migrations()
    print("SQLite metadata DB initialized")

    print("Initialization complete.")

if __name__ == "__main__":
    main()