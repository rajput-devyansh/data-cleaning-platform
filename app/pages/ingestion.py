import streamlit as st
from pathlib import Path

from core.config import UPLOADS_DIR
from core.ingestion.sniffing import (
    detect_encoding,
    detect_delimiter,
    detect_header,
)
from core.ingestion.preview import load_preview
from core.ingestion.loader import load_csv_to_duckdb
from core.versioning.version_manager import VersionManager
from core.audit.action_logger import ActionLogger

st.header("Step 1: Data Ingestion (CSV)")

uploaded = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded:
    file_path = UPLOADS_DIR / uploaded.name
    file_path.write_bytes(uploaded.getbuffer())

    # Detect properties
    encoding = detect_encoding(file_path)
    delimiter = detect_delimiter(file_path, encoding)
    has_header = detect_header(file_path, encoding, delimiter)

    st.subheader("Detected Properties")
    st.write(f"Encoding: `{encoding}`")
    st.write(f"Delimiter: `{delimiter}`")
    st.write(f"Header: `{has_header}`")

    # Preview
    preview_df = load_preview(
        file_path, encoding, delimiter, has_header
    )
    st.subheader("Preview")
    st.dataframe(preview_df)

    dataset_id = st.text_input("Dataset ID", value=Path(uploaded.name).stem)

    if st.button("Confirm & Ingest"):
        vm = VersionManager()
        logger = ActionLogger()

        vm.register_dataset(dataset_id, dataset_id)

        table_name = load_csv_to_duckdb(
            dataset_id=dataset_id,
            version=0,
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter,
            has_header=has_header,
        )

        vm.create_version(
            dataset_id=dataset_id,
            version=0,
            table_name=table_name,
        )

        logger.log_action(
            dataset_id=dataset_id,
            step="Ingestion",
            operation="csv_ingest",
            parameters={
                "encoding": encoding,
                "delimiter": delimiter,
                "header": has_header,
                "file": uploaded.name,
            },
        )

        st.success(f"Dataset `{dataset_id}` ingested successfully!")