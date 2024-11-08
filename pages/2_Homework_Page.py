import streamlit as st
from utils import load_json, save_json
import dashboard

st.set_page_config(page_title="Homework", page_icon="📓", layout="wide")

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You must be logged in to access this page.")
    st.stop()  # Stops the rest of the page from loading if not authenticated

st.write("# Manage Homework")

col1, col2 = st.columns([1, 2])

# Column 1: Add new homework
with col1:
    st.write("## Add New Homework")
    dashboard.add_manual_homework()

# Column 2: Display all Homework within the next week if desired
with col2:
    st.write("## Upcoming Homework")
    dashboard.display_homework(show_week_only=True)  # Only show homework for the current week
