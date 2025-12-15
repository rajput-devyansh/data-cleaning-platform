import streamlit as st
from core.versioning.version_manager import VersionManager
from core.pii.detectors import detect_pii_columns
from core.pii.masking import mask_email, mask_phone
from core.pii.engine import PIIEngine

st.header("Step 7: PII Detection & Redaction")

vm = VersionManager()
engine = PIIEngine()

dataset_id = st.text_input("Dataset ID")
active = vm.get_active_version(dataset_id)

if active:
    version, table_name = active["version"], active["table_name"]

    pii_cols = detect_pii_columns(table_name)

    if not pii_cols:
        st.success("No PII detected")
    else:
        st.warning("Potential PII detected")

        masking_rules = {}

        for col, matches in pii_cols.items():
            st.write(f"Column: `{col}`")
            st.json(matches)

            choice = st.selectbox(
                f"Masking strategy for {col}",
                ["None", "Email Mask", "Phone Mask"],
                key=col,
            )

            if choice == "Email Mask":
                masking_rules[col] = mask_email(f'"{col}"')
            elif choice == "Phone Mask":
                masking_rules[col] = mask_phone(f'"{col}"')

        if masking_rules and st.button("Apply Masking"):
            engine.apply_masking(
                dataset_id,
                version,
                masking_rules,
            )
            st.success("PII masking applied successfully")