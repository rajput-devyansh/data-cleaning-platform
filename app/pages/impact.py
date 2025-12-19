import streamlit as st
import pandas as pd

from core.impact.repository import ImpactRepository
from core.impact.aggregations import (
    build_dataset_timeline,
    build_row_count_series,
    build_action_impact,
    build_column_overwrite_summary,
)

st.header("📊 Impact Dashboard")

dataset_id = st.text_input("Dataset ID")

if not dataset_id:
    st.stop()

repo = ImpactRepository()
actions = repo.get_actions_for_dataset(dataset_id)

if not actions:
    st.warning("No actions found for this dataset.")
    st.stop()

st.subheader("Dataset Evolution Timeline")

timeline = build_dataset_timeline(actions)
df_timeline = pd.DataFrame(timeline)

st.dataframe(df_timeline, use_container_width=True)

st.subheader("Row Count Over Time")

row_series = build_row_count_series(actions)
df_rows = pd.DataFrame(row_series)

if not df_rows.empty:
    st.line_chart(df_rows.set_index("timestamp")["rows"])

st.subheader("Action Impact Breakdown")

impact = build_action_impact(actions)
df_impact = pd.DataFrame(impact)

if not df_impact.empty:
    st.bar_chart(
        df_impact.groupby("operation")["rows_changed"].sum()
    )

st.subheader("Column Overwrite Frequency")

col_summary = build_column_overwrite_summary(actions)
df_cols = pd.DataFrame(col_summary)

if not df_cols.empty:
    st.bar_chart(
        df_cols.set_index("column")["overwrite_count"]
    )

st.subheader("Inspect Action")

action_options = [
    f'[{a["action_id"]}] {a["operation"]} (v{a["version_before"]} → v{a["version_after"]})'
    for a in actions
    if a.get("version_before") is not None and a.get("version_after") is not None
]

if not action_options:
    st.info("No versioned actions available for diff inspection.")
    st.stop()

selected_action_label = st.selectbox(
    "Select an action to inspect row-level changes",
    action_options,
)

selected_action = None
for a in actions:
    label = f'[{a["action_id"]}] {a["operation"]} (v{a["version_before"]} → v{a["version_after"]})'
    if label == selected_action_label:
        selected_action = a
        break

if selected_action:
    if st.button("🔍 Open Diff Explorer"):
        st.session_state["diff_dataset_id"] = dataset_id
        st.session_state["diff_v_from"] = selected_action["version_before"]
        st.session_state["diff_v_to"] = selected_action["version_after"]

        st.experimental_set_query_params(
            page="diff"
        )

        st.rerun()