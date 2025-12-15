CREATE TABLE IF NOT EXISTS schemas (
    dataset_id TEXT,
    version INTEGER,
    schema_json TEXT,
    is_locked BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (dataset_id, version)
);