from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
DUCKDB_DIR = DATA_DIR / "duckdb"
SQLITE_DIR = DATA_DIR / "sqlite"
UPLOADS_DIR = DATA_DIR / "uploads"
EXPORTS_DIR = DATA_DIR / "exports"
QUARANTINE_DIR = DATA_DIR / "quarantine"

# Ensure dirs exist
for d in [
    DATA_DIR,
    DUCKDB_DIR,
    SQLITE_DIR,
    UPLOADS_DIR,
    EXPORTS_DIR,
    QUARANTINE_DIR,
]:
    d.mkdir(parents=True, exist_ok=True)

# App settings
APP_NAME = os.getenv("APP_NAME", "Local Data Cleaning Platform")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"