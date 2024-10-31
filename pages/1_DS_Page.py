import streamlit as st
from utils import load_json, save_json
from datetime import datetime
import dashboard

st.set_page_config(page_title="DS/Evaluations", page_icon="📅", layout="wide")


if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You must be logged in to access this page.")
    st.stop()  # Prevents the rest of the page from loading if not authenticated


st.write("# Manage DS and Evaluations")

col1, col2 = st.columns([1, 2])

# Column 1: Add a new DS/Evaluation
with col1:
    st.write("## Add a New DS/Evaluation")
    dashboard.add_manual_entry()
    

# Column 2: Display all DS/Evaluations
with col2:
    st.write("## All DS/Evaluations")
    dashboard.display_ds_evals()
