-- datasets
CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- dataset versions
CREATE TABLE IF NOT EXISTS dataset_versions (
    dataset_id TEXT,
    version INTEGER,
    table_name TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (dataset_id, version)
);

-- actions
CREATE TABLE IF NOT EXISTS actions (
    action_id TEXT PRIMARY KEY,
    dataset_id TEXT,
    step TEXT,
    operation TEXT,
    parameters TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);