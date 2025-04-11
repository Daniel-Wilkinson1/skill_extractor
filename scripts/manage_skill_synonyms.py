
import streamlit as st
import pandas as pd
import os

# File path for the synonym table
DATA_PATH = "../data/skill_synonyms.xlsx"
os.makedirs("../data", exist_ok=True)

# Load or initialize synonym DataFrame
if os.path.exists(DATA_PATH):
    df = pd.read_excel(DATA_PATH)
else:
    df = pd.DataFrame(columns=["skill", "synonym"])

st.title("🧠 Skill Synonym Manager")

# Show existing synonyms
st.subheader("📋 Current Synonyms")
if df.empty:
    st.info("No synonyms yet.")
else:
    st.dataframe(df)

# Add new synonym
st.subheader("➕ Add New Synonym")
with st.form("add_form"):
    new_skill = st.text_input("Canonical Skill (e.g., cad)", "")
    new_synonym = st.text_input("Synonym (e.g., computer-aided design)", "")
    submitted = st.form_submit_button("Add Synonym")

    if submitted:
        if new_skill and new_synonym:
            new_entry = {"skill": new_skill.strip().lower(), "synonym": new_synonym.strip().lower()}
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_excel(DATA_PATH, index=False)
            st.success(f"Added synonym '{new_synonym}' for skill '{new_skill}'.")
            st.rerun()
        else:
            st.error("Please fill out both fields.")

# Delete selected synonyms
st.subheader("🗑️ Delete Synonyms")
if not df.empty:
    to_delete = st.multiselect("Select rows to delete", df.apply(lambda row: f"{row['skill']} → {row['synonym']}", axis=1))
    if st.button("Delete Selected"):
        mask = df.apply(lambda row: f"{row['skill']} → {row['synonym']}", axis=1).isin(to_delete)
        df = df[~mask]
        df.to_excel(DATA_PATH, index=False)
        st.success("Selected synonyms deleted.")
        st.experimental_rerun()
