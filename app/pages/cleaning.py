import streamlit as st
from core.cleaning.detectors import (
    count_nulls,
    count_empty_strings,
    count_duplicates,
)
from core.cleaning.rules import (
    drop_nulls_sql,
    fill_nulls_sql,
    drop_duplicates_sql,
)
from core.cleaning.engine import CleaningEngine
from core.versioning.version_manager import VersionManager

st.header("Step 6: Data Cleaning (MVP)")

vm = VersionManager()
engine = CleaningEngine()

dataset_id = st.text_input("Dataset ID")

if not dataset_id:
    st.stop()

dataset = vm.get_dataset(dataset_id)

if not dataset:
    st.error("Dataset not found.")
    st.stop()

# 🔒 GUARDRAIL (THIS IS STEP 5)
if dataset["status"] != "schema_locked":
    st.error("Schema must be locked before cleaning.")
    st.stop()

active = vm.get_active_version(dataset_id)

if active:
    version, table_name = active["version"], active["table_name"]

    st.subheader("Null Checks")

    column = st.text_input("Column name")

    if column:
        nulls = count_nulls(table_name, column)
        st.write(f"Null values: {nulls}")

        if nulls > 0:
            action = st.radio(
                "Fix nulls",
                ["Drop rows", "Fill with value"],
            )

            if action == "Fill with value":
                fill_val = st.text_input("Fill value")

            if st.button("Apply Null Fix"):
                if action == "Drop rows":
                    sql = drop_nulls_sql(
                        "{source_table}",
                        "{target_table}",
                        column,
                    )
                    params = {"column": column, "method": "drop"}
                else:
                    sql = fill_nulls_sql(
                        "{source_table}",
                        "{target_table}",
                        column,
                        fill_val,
                    )
                    params = {
                        "column": column,
                        "method": "fill",
                        "value": fill_val,
                    }

                engine.apply_rule(
                    dataset_id,
                    version,
                    sql,
                    operation="null_fix",
                    parameters=params,
                )

                st.success("Nulls cleaned successfully!")

    st.subheader("Duplicate Checks")

    dup_cols = st.text_input(
        "Columns for duplicate detection (comma-separated)"
    )

    if dup_cols:
        cols = [c.strip() for c in dup_cols.split(",")]
        dup_count = count_duplicates(table_name, cols)

        st.write(f"Duplicate rows: {dup_count}")

        if dup_count > 0 and st.button("Drop Duplicates"):
            sql = drop_duplicates_sql(
                "{source_table}",
                "{target_table}",
                cols,
            )

            engine.apply_rule(
                dataset_id,
                version,
                sql,
                operation="drop_duplicates",
                parameters={"columns": cols},
            )

            st.success("Duplicates removed!")