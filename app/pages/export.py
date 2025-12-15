import streamlit as st
from core.versioning.version_manager import VersionManager
from core.exporter.exporter import export_dataset

st.header("Export Data")

dataset_id = st.text_input("Dataset ID")
vm = VersionManager()

if not dataset_id:
    st.stop()

dataset = vm.get_dataset(dataset_id)

if not dataset:
    st.error("Dataset not found.")
    st.stop()

# 🔒 GUARDRAIL
if dataset["status"] != "pii_checked":
    st.error("PII check must be completed before export.")
    st.stop()

active = vm.get_active_version(dataset_id)

if active and st.button("Export"):
    _, table = active["version"], active["table_name"]
    data, meta = export_dataset(table, dataset_id)

    st.success("Export complete")
    st.write(data)
    st.write(meta)