import streamlit as st
from core.versioning.version_manager import VersionManager
from core.exporter.exporter import export_dataset

st.header("Export Data")

dataset_id = st.text_input("Dataset ID")
vm = VersionManager()

active = vm.get_active_version(dataset_id)

if active and st.button("Export"):
    _, table = active["version"], active["table_name"]
    data, meta = export_dataset(table, dataset_id)

    st.success("Export complete")
    st.write(data)
    st.write(meta)