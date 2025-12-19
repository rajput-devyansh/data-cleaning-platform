import streamlit as st
from core.versioning.version_manager import VersionManager
from core.diff.engine import diff_datasets

st.header("🔍 Dataset Diff Explorer")

vm = VersionManager()
dataset_id = st.text_input(
    "Dataset ID",
    value=st.session_state.get("diff_dataset_id", ""),
)

if not dataset_id:
    st.stop()

versions = vm.list_versions(dataset_id)
if not versions:
    st.error("No versions found.")
    st.stop()

version_numbers = [v["version"] for v in versions]

default_from = (
    version_numbers.index(st.session_state["diff_v_from"])
    if "diff_v_from" in st.session_state and st.session_state["diff_v_from"] in version_numbers
    else 0
)

default_to = (
    version_numbers.index(st.session_state["diff_v_to"])
    if "diff_v_to" in st.session_state and st.session_state["diff_v_to"] in version_numbers
    else 1
)

v_from = st.selectbox("Compare FROM version", version_numbers, index=default_from)
v_to = st.selectbox("Compare TO version", version_numbers, index=default_to)

auto_run = (
    "diff_v_from" in st.session_state and
    "diff_v_to" in st.session_state and
    "diff_dataset_id" in st.session_state
)

if v_from == v_to and not auto_run:
    st.warning("Select two different versions.")
    st.stop()

if st.button("Run Diff") or auto_run:
    table_a = f"{dataset_id}_v{v_from}"
    table_b = f"{dataset_id}_v{v_to}"

    diff = diff_datasets(table_a, table_b)
    st.session_state["diff_result"] = diff

    st.subheader("Summary")
    st.json(diff.summary.__dict__)

    st.subheader("Added Rows")
    st.write(diff.added_row_ids[:20])

    st.subheader("Removed Rows")
    st.write(diff.removed_row_ids[:20])

    st.subheader("Modified Rows (sample)")
    for row in diff.modified_rows:
        with st.expander(f"Row {row.row_id}"):
            st.json(row.changes)

    st.session_state.pop("diff_v_from", None)
    st.session_state.pop("diff_v_to", None)
    st.session_state.pop("diff_dataset_id", None)

from core.diff.export import diff_to_json, diff_to_csv

if "diff_result" in st.session_state:
    st.session_state["diff_result"] = diff
    st.session_state["diff_meta"] = {
        "dataset_id": dataset_id,
        "v_from": v_from,
        "v_to": v_to,
    }
    meta = st.session_state["diff_meta"]

    st.subheader("Export Diff")

    col1, col2 = st.columns(2)

    with col1:
        json_data = diff_to_json(diff)
        st.download_button(
            label="⬇️ Download Diff (JSON)",
            data=json_data,
            file_name=f"{meta['dataset_id']}_diff_v{meta['v_from']}_to_v{meta['v_to']}.json",
            mime="application/json",
        )

    with col2:
        csv_data = diff_to_csv(diff)
        st.download_button(
            label="⬇️ Download Modified Rows (CSV)",
            data=csv_data,
            file_name=f"{meta['dataset_id']}_diff_v{meta['v_from']}_to_v{meta['v_to']}.csv",
            mime="text/csv",
        )