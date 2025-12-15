import streamlit as st
from core.schema.profiler import profile_columns
from core.schema.type_inference import infer_column_type
from core.schema.schema_lock import apply_schema
from core.versioning.version_manager import VersionManager
from core.audit.action_logger import ActionLogger

st.header("Step 3: Schema Profiling & Locking")

vm = VersionManager()
logger = ActionLogger()

dataset_id = st.text_input("Dataset ID")
active = vm.get_active_version(dataset_id)

if active:
    version, table_name = active["version"], active["table_name"]

    st.subheader("Column Profiles")
    profiles = profile_columns(table_name)

    schema = {}

    for col, stats in profiles.items():
        st.markdown(f"### {col}")
        st.write(stats)

        inferred = infer_column_type(table_name, col)
        st.subheader("Inferred Value Types")

        st.metric("Integer values", f"{inferred['int_ratio'] * 100:.1f}%")
        st.metric("Float values", f"{inferred['float_ratio'] * 100:.1f}%")
        st.metric("Date values", f"{inferred['date_ratio'] * 100:.1f}%")

        max_ratio = max(inferred.values())

        if max_ratio < 0.5:
            st.info("⚠️ No dominant type detected. Column likely categorical or identifier.")
        elif inferred["int_ratio"] == max_ratio:
            st.success("Suggested type: INTEGER")
        elif inferred["float_ratio"] == max_ratio:
            st.success("Suggested type: DOUBLE")
        elif inferred["date_ratio"] == max_ratio:
            st.success("Suggested type: DATE")

        dtype = st.selectbox(
            f"Select type for `{col}`",
            ["VARCHAR", "INTEGER", "DOUBLE", "DATE"],
            key=col,
        )

        schema[col] = dtype

    if st.button("Lock Schema"):
        apply_schema(
            dataset_id,
            source_version=version,
            target_version=version + 1,
            schema=schema,
        )

        vm.create_version(
            dataset_id,
            version + 1,
            table_name=f"{dataset_id}_v{version + 1}",
        )

        logger.log_action(
            dataset_id,
            step="Schema",
            operation="schema_lock",
            parameters=schema,
        )

        st.success("Schema locked successfully!")